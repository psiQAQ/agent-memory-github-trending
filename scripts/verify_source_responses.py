"""Compare a local GitHub collection batch with its retained CLI responses."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import local_maintenance as local
import tracker

API = "https://api.github.com/"


def read_response(record: dict, path: Path, allow_legacy_text: bool) -> tuple[bool, object]:
    ref = record.get("stdout_file")
    if ref is None:
        tracker.require(allow_legacy_text, f"{path.name}: stdout byte file is required")
        raw = record["stdout"].encode("utf-8")
    else:
        tracker.require(ref == path.with_suffix(".stdout").name, f"{path.name}: unexpected stdout filename")
        byte_path = path.with_suffix(".stdout")
        tracker.require(byte_path.resolve() == path.parent.resolve() / ref, f"{path.name}: stdout must be run-local")
        raw = byte_path.read_bytes()
    tracker.require(
        len(raw) == record["stdout_bytes"] and hashlib.sha256(raw).hexdigest() == record["stdout_sha256"],
        f"{path.name}: stdout fingerprint mismatch",
    )
    parts = re.split(rb"\r?\n\r?\n", raw, maxsplit=1)
    tracker.require(len(parts) == 2 and re.match(rb"HTTP/\S+ 2\d\d(?: |\r?\n|$)", parts[0]) is not None,
                    f"{path.name}: expected a successful gh --include response")
    headers, payload = parts
    link_headers = re.findall(rb"^link:[^\r\n]*", headers, re.I | re.M)
    has_next = any(re.search(rb'rel="next"', header, re.I) for header in link_headers)
    return has_next, json.loads(payload)


def api_endpoint(args: list[str]) -> str:
    args = args[1:] if args[0] == "gh" else args
    tracker.require(args[0] == "api" and ("--include" in args or "-i" in args),
                    "expected gh api with response headers")
    tracker.require("--method" in args and args[args.index("--method") + 1] == "GET",
                    "expected explicit gh api --method GET")
    endpoints = [a for a in args[1:] if a.startswith("repos/") or a == "search/repositories"]
    tracker.require(len(endpoints) == 1, "expected one public source endpoint")
    return endpoints[0]


def discovery_args(args: list[str]) -> dict:
    endpoint = api_endpoint(args)
    tracker.require(endpoint == "search/repositories", "expected repository search endpoint")
    flags = {"-F", "-f", "--field", "--raw-field"}
    pairs = [args[i + 1].split("=", 1) for i, arg in enumerate(args) if arg in flags]
    params = dict(pairs)
    tracker.require(len(params) == len(pairs) and "q" in params, "missing or repeated discovery field")
    return dict(query=params["q"], page=int(params["page"]), per_page=int(params["per_page"]),
                sort=params.get("sort"), order=params.get("order"))


def release_projection(name: str, source: dict, captures: list, previous: dict) -> dict:
    page_specs = source["pagination"]
    per_page_values = {int(parse_qs(urlsplit(url).query)["per_page"][0]) for _, url, _, _ in captures}
    tracker.require(len(per_page_values) == 1, f"{name}: mixed Release page sizes")
    per_page = per_page_values.pop()
    captures.sort(key=lambda entry: int(parse_qs(urlsplit(entry[1]).query)["page"][0]))
    prior = previous.get("value")
    known_ids = [v["id"] for v in prior or []]
    overlaps = False
    exhausted = False
    pages, releases = [], []
    for page, (record, url, has_next, values) in enumerate(captures, 1):
        tracker.require(not overlaps and not exhausted, f"{name}: pages follow a completed Release range")
        tracker.require(url == local.release_page_url(record["args"], name, page, per_page),
                        f"{name}: Release URL differs from actual arguments")
        tracker.require(isinstance(values, list) and len(values) <= per_page, f"{name}: invalid Release page")
        published = [dict(id=v["id"], tag=v["tag_name"], published_at=v["published_at"], url=v["html_url"])
                     for v in values if not v["draft"]]
        releases.extend(published)
        overlaps = any(v["id"] in known_ids for v in published)
        exhausted = len(values) < per_page or not has_next
        pages.append(dict(page=page, observed_at=record["returned_at"], returned=len(values), source_url=url))
    tracker.require(source["complete"] == (overlaps or exhausted), f"{name}: Release completeness mismatch")
    if source["complete"]:
        reason = "prior_release_id_reached" if overlaps else "collection_exhausted"
        tracker.require(page_specs["stop_reason"] == reason, f"{name}: Release stop reason mismatch")
    tracker.require(
        page_specs["pages_obtained"] == len(pages) and source["value"] == releases
        and source["observed_at"] == pages[-1]["observed_at"] and source["source_url"] == pages[0]["source_url"],
        f"{name}: Release snapshot projection mismatch",
    )
    return dict(per_page=per_page, pages=pages, previous_success_release_ids=known_ids,
                stop_reason=page_specs["stop_reason"])


def validate_observations(batch: dict, captures: dict, prior: dict, checkpoints: dict | None) -> int:
    release_count = 0
    for observation in batch["observations"]:
        ident, name = observation["repository_id"], observation["full_name"]
        for kind in tracker.SOURCES:
            source = observation[kind]
            entries = captures.pop((kind, ident), [])
            if source["status"] != "ok":
                tracker.require(not entries, f"{name}: successful response recorded as {source['status']}")
                continue
            tracker.require(bool(entries), f"{name}: missing captured {kind} response")
            if kind == "releases":
                projection = release_projection(name, source, entries, prior.get(str(ident), {}).get(kind, {}))
                release_count += len(source["value"])
                if checkpoints is not None and source["complete"] and (
                    source["pagination"]["scope"] == "incremental_since_previous_success"
                ):
                    slot = checkpoints[str(ident)][kind]
                    tracker.require(slot["incremental_pagination"] == projection,
                                    f"{name}: Receipt Release paging projection mismatch")
            else:
                tracker.require(len(entries) == 1, f"{name}: duplicated successful {kind} response")
                record, url, _, obj = entries[0]
                expected_url = API + "repos/" + name
                if kind == "metadata":
                    tracker.require(obj["id"] == ident and obj["full_name"] == name and obj["private"] is False,
                                    f"{name}: metadata identity mismatch")
                    actual = dict(stars=obj["stargazers_count"], forks=obj["forks_count"],
                                  archived=obj["archived"], default_branch=obj["default_branch"],
                                  created_at=obj["created_at"], pushed_at=obj["pushed_at"],
                                  license_spdx=(obj["license"] or {}).get("spdx_id"))
                else:
                    tracker.require(obj["ref"].startswith("refs/heads/") and obj["object"]["type"] == "commit",
                                    f"{name}: invalid branch HEAD response")
                    if observation["metadata"]["status"] == "ok":
                        tracker.require(obj["ref"] == "refs/heads/" + observation["metadata"]["value"]["default_branch"],
                                        f"{name}: HEAD does not refer to the captured default branch")
                    expected_url += "/git/ref/" + obj["ref"][5:]
                    actual = obj["object"]["sha"]
                tracker.require(url == expected_url == source["source_url"]
                                and source["observed_at"] == record["returned_at"] and source["value"] == actual,
                                f"{name}: {kind} snapshot projection mismatch")
    tracker.require(not captures, "captured repository responses are missing from the batch")
    return release_count


def validate_discovery(queries: list, captures: dict) -> None:
    checked = set()
    for q in sorted(queries, key=lambda value: value["page"]):
        key = q["query"], q["page"], q["sort"], q.get("order")
        tracker.require(key in captures, "missing captured discovery page")
        record, params, has_next, item = captures.pop(key)
        items = [dict(repository_id=v["id"], full_name=v["full_name"], source_url=v["html_url"],
                      description=v.get("description"), license_spdx=(v.get("license") or {}).get("spdx_id"))
                 for v in item["items"]]
        checked.add(key)
        earlier_pages_checked = all((key[0], p, key[2], key[3]) in checked for p in range(1, q["page"]))
        total = item.get("total_count")
        incomplete = item.get("incomplete_results")
        exhausted = (incomplete is False and earlier_pages_checked
                     and total == (q["page"] - 1) * params["per_page"] + len(items))
        completeness = False if has_next else True if exhausted else None
        tracker.require(
            q["per_page"] == params["per_page"] and q["returned"] == len(items) and q["items"] == items
            and q["total_count"] == total and q["incomplete_results"] == incomplete
            and q["pagination_complete"] == completeness and q["observed_at"] == record["returned_at"],
            "discovery snapshot projection mismatch",
        )
    tracker.require(not captures, "captured discovery responses are missing from the batch")


def verify(batch: dict, results: Path, previous: dict, checkpoints: dict | None = None,
           evidence: dict | None = None, allow_legacy_text: bool = False) -> dict:
    tracker.validate_batch(batch, set(batch["expected_repository_ids"]))
    tracker.require(results.is_dir(), "response directory is missing")
    prior = previous["sources"]
    frozen = None if evidence is None else {
        c["id"]: c for segment in evidence["segments"] for c in segment["calls"]
    }
    if evidence is not None:
        tracker.require(evidence["run_id"] == batch["run_id"], "evidence run ID mismatch")
    sources = defaultdict(list)
    discovery = {}
    counts = dict.fromkeys((*tracker.SOURCES, "discovery"), 0)
    seen = set()
    for path in sorted(results.glob("*.json")):
        row = tracker.load(path)
        if row.get("tool") != "gh" or row.get("state") != "returned" or row.get("exit_code") != 0:
            continue
        kind = "discovery" if "search/repositories" in row["args"] else row.get("kind")
        if kind not in counts:
            continue
        tracker.require(path.stem == row["id"] and row["id"] not in seen, f"{path.name}: response identity mismatch")
        seen.add(row["id"])
        if frozen is not None:
            fixed = frozen[row["id"]]
            fields = ("tool", "args", "returned_at", "stdout_bytes", "stdout_sha256")
            tracker.require(all(fixed[field] == row[field] for field in fields),
                            f"{path.name}: Receipt response summary mismatch")
        has_next, item = read_response(row, path, allow_legacy_text)
        counts[kind] += 1
        if kind == "discovery":
            params = discovery_args(row["args"])
            key = params["query"], params["page"], params["sort"], params["order"]
            tracker.require(key not in discovery, f"{path.name}: duplicated discovery page")
            discovery[key] = row, params, has_next, item
        else:
            sources[kind, row["repository_id"]].append((row, API + api_endpoint(row["args"]), has_next, item))

    if checkpoints is not None:
        tracker.require(checkpoints["last_completed_run_id"] == batch["run_id"], "checkpoint run ID mismatch")
        local.validate_receipt_release_pages(batch, checkpoints)
    release_count = validate_observations(batch, sources, prior, None if checkpoints is None else checkpoints["sources"])
    validate_discovery(batch["discovery"], discovery)
    return dict(status="passed", run_id=batch["run_id"], source_responses=counts, total_responses=len(seen),
                release_entries=release_count, receipt_pages_checked=checkpoints is not None,
                receipt_fingerprints_checked=frozen is not None)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--previous-checkpoints", type=Path, required=True)
    parser.add_argument("--checkpoints", type=Path)
    parser.add_argument("--receipt-evidence", type=Path)
    parser.add_argument("--allow-legacy-text", action="store_true")
    args = parser.parse_args()
    try:
        result = verify(tracker.load(args.batch), args.results, tracker.load(args.previous_checkpoints),
                        tracker.load(args.checkpoints) if args.checkpoints else None,
                        tracker.load(args.receipt_evidence) if args.receipt_evidence else None,
                        args.allow_legacy_text)
    except (ValueError, OSError, KeyError, IndexError, TypeError, AttributeError) as error:
        parser.exit(1, f"Source response verification failed: {error}\n")
    print(tracker.encoded(result), end="")


if __name__ == "__main__":
    main()
