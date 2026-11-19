"""Fixed owner/Agent maintenance stages; stdlib only, no upstream code execution.

Owner: collect and fetch an Agent-selected review plan. Agent: interpret evidence,
author reports, then explicitly invoke commit/publish/readback. No scheduler here.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import local_maintenance as local
import manifest_validation as manifest
import tracker
import verify_source_responses as source_check

ROOT = Path(__file__).resolve().parents[1]
REPO = tracker.TARGET
# Keep the identity of the executing code even when a checkout removes this file.
WRAPPER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def save(path: Path, value, *, exclusive=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8", newline="\n") as stream:
        stream.write(tracker.encoded(value))


def save_consistent(path: Path, value):
    if path.exists():
        tracker.require(tracker.load(path) == value, "existing artifact differs; preserve and reconcile: " + str(path))
    else:
        save(path, value, exclusive=True)


def run_dir(root: Path, run_id: str):
    tracker.require(bool(tracker.RUN.fullmatch(run_id)), "invalid run ID")
    return root / ".cache" / run_id


def gates(root: Path):
    config = tracker.load(root / "config/tracker.json")
    profile = tracker.load(root / "config/local-runtime.json")
    tracker.require(config["repository"] == profile["repository"] == REPO, "repository mismatch")
    tracker.require(config["approval_state"] == "approved" and config["automation_enabled"] is True
                    and config["implementation_ready"] is True, "approval gates closed")
    tracker.require(profile["cutover_state"] == "active" and profile["runtime_mode"] == "local_git"
                    and config["settings"]["runtime_mode"] == "local_git", "local profile inactive")
    for flag in ("--push", ""):
        args = ("remote", "get-url", flag, "origin") if flag else ("remote", "get-url", "origin")
        tracker.require(local.git(root, *args).decode().strip() in local.ORIGINS, "unexpected origin")


def ordinary_user():
    tracker.require(os.name == "nt", "owner entry requires native Windows")
    tracker.require(not ctypes.windll.shell32.IsUserAnAdmin(), "run as existing ordinary user, not administrator")


def check(root: Path):
    gates(root)
    ZoneInfo("Asia/Shanghai")
    for name in ("python", "git", "gh", "cmd.exe"):
        tracker.require(shutil.which(name), "missing existing dependency: " + name)
    if os.name == "nt":
        git_child_env()
    return dict(status="Passed", scope="offline_only", repository=REPO,
                head=local.pin(root, "HEAD"), lock=local.lock_status(root),
                network="Not Run", publication="Not Run")


def prepare(root: Path, run_id: str | None):
    """Offline preparation never takes over a lock or authenticates a trigger."""
    check(root)
    if run_id and completed(root, run_dir(root, run_id)):
        return dict(status="already_complete", run_id=run_id, network="Not Run")
    lock = local.lock_status(root)
    pointer = root / ".cache/owner-current.json"
    if lock["state"] != "unlocked":
        tracker.require(lock.get("run_id"), "invalid lock; preserve and reconcile")
        tracker.require(not run_id or run_id == lock["run_id"], "another batch owns the lock")
        run_id = lock["run_id"]
    elif not run_id and pointer.exists():
        prior = tracker.load(pointer)
        path = run_dir(root, prior["run_id"])
        if not completed(root, path):
            run_id = prior["run_id"]
    if not run_id:
        _, _, index = local.inspect(root)
        status = tracker.load(root / "state/status.json")
        if index["snapshots"] and index["snapshots"][-1]["run_id"] != status.get("last_completed_run_id"):
            run_id = index["snapshots"][-1]["run_id"]
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-local"
    run = run_dir(root, run_id)
    run.mkdir(parents=True, exist_ok=True)
    tracker.require(local.git(root, "check-ignore", str(run.relative_to(root))).strip(), ".cache must be ignored")
    existing = run / "owner-pipeline/preparation.json"
    if existing.exists():
        packet = tracker.load(existing)
        tracker.require(packet["repository"] == REPO and packet["run_id"] == run_id, "preparation identity differs")
        save(pointer, dict(repository=REPO, run_id=run_id))
        return packet
    packet = dict(schema_version="1.0", repository=REPO, run_id=run_id,
                  prepared_at=now(), program_commit_sha=local.pin(root, "HEAD"),
                  phase="awaiting_owner", lock=lock,
                  trigger_kind="unknown", trigger_verification="unverified",
                  instruction="Run collect-owner.bat; an existing lock requires explicit handoff clearance.")
    save(pointer, dict(repository=REPO, run_id=run_id))
    save(run / "owner-pipeline/preparation.json", packet)
    return packet


def completed(root, run):
    path = run / "final-completion.json"
    if not path.exists():
        return False
    proof = tracker.load(path)
    tracker.require(proof["repository"] == REPO and proof["run_id"] == run.name, "completion identity differs")
    tracker.require(proof.get("maintenance_complete") is True, "incomplete final proof")
    for phase in ("data", "receipt"):
        tracker.require(proof[phase + "_readback"]["status"].lower() == "passed"
                        and proof[phase + "_readback"]["commit_sha"] == proof[phase + "_sha"], "completion readback mismatch")
    tracker.require(proof["pages"]["status"].lower() == "passed", "Pages acceptance missing")
    status = json.loads(local.git(root, "show", proof["receipt_sha"] + ":state/status.json"))
    tracker.require(status["last_completed_run_id"] == run.name
                    and status["last_verified_data_commit_sha"] == proof["data_sha"], "completed Receipt differs")
    local.git(root, "merge-base", "--is-ancestor", proof["receipt_sha"], "HEAD")
    return True


def retained(run: Path, *, allow_unresolved=False):
    result = []
    for path in sorted((run / "results").glob("*.json")):
        row = tracker.load(path)
        if row.get("tool") == "git" and row.get("args", [])[:2] == ["push", "origin"]:
            # A read-back commit/ref may resolve a previously uncertain push;
            # retain the original outcome instead of rewriting it as success.
            target = row["args"][2] if len(row["args"]) == 3 else ""
            if re.fullmatch(r"[a-f0-9]{40}:refs/heads/main", target):
                proofs = [run / "owner-pipeline" / (p + "-readback.json") for p in ("data", "receipt")]
                if any(p.exists() and tracker.load(p).get("status") == "passed"
                       and tracker.load(p).get("commit_sha") == target[:40] for p in proofs):
                    if row.get("state") != "returned" or row.get("exit_code") != 0:
                        continue
        if allow_unresolved and (row.get("state") != "returned" or row.get("exit_code") != 0):
            # Reconciliation may issue new read-only requests, never replay this action.
            continue
        tracker.require(row.get("state") == "returned" and row.get("exit_code") == 0,
                        "failed/uncertain prior action; reconcile before continuing: " + path.name)
        raw = path.with_suffix(".stdout").read_bytes()
        tracker.require(row["id"] == path.stem and row["stdout_file"] == path.with_suffix(".stdout").name,
                        "response identity mismatch")
        tracker.require(len(raw) == row["stdout_bytes"] and hashlib.sha256(raw).hexdigest() == row["stdout_sha256"],
                        "retained response changed: " + path.name)
        result.append(row)
    return result


def git_child_env():
    """Select the installed Git shell for this child only; preserve proxy variables."""
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    if os.name == "nt":
        exe = shutil.which("git")
        tracker.require(exe, "existing Git executable required")
        prefix = Path(exe).resolve().parent.parent
        shell = prefix / "bin/bash.exe"
        if not shell.is_file() and prefix.name.lower() == "mingw64":
            shell = prefix.parent / "bin/bash.exe"
        tracker.require(shell.is_file(), "existing Git Bash missing; do not install or change SSH configuration")
        env["SHELL"] = str(shell)
    return env


class Transport:
    """Parent writes/emits pre/post outside each actual child invocation. No retries."""
    def __init__(self, root: Path, run: Path, *, allow_unresolved=False):
        self.root, self.run = root, run
        self.rows = retained(run, allow_unresolved=allow_unresolved)

    def call(self, tool, args, kind, repository_id=None, *, reuse=True):
        if reuse:
            hits = [x for x in self.rows if x["tool"] == tool and x["args"] == args and x.get("kind") == kind]
            tracker.require(len(hits) <= 1, "duplicate successful source requests")
            if hits:
                return hits[0]
        key = "owner-" + hashlib.sha256(tracker.encoded([tool, args, kind]).encode()).hexdigest()[:20]
        dest = self.run / "results" / (key + ".json")
        tracker.require(not dest.exists(), "action already recorded; reconcile, do not retry: " + key)
        prior = len(self.rows)
        intent = dict(id=key, tool=tool, args=args, kind=kind)
        if repository_id is not None:
            intent["repository_id"] = repository_id
        pre = dict(run_id=self.run.name, pre_call_id=key, phase=kind, calls=[intent],
                   wrapper="owner_pipeline.py", wrapper_sha256=WRAPPER_SHA256,
                   prepared_at=now(), cumulative_observed_before=prior, origin="local_cli_not_trigger_proof")
        save(self.run / "owner-pipeline" / ("pre-" + key + ".json"), pre, exclusive=True)
        print(tracker.encoded(dict(pre_call=pre)), flush=True)
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        if tool == "git":
            env = git_child_env()
        row = dict(intent, state="started", dispatch_at=now())
        save(dest, row, exclusive=True)
        child = None
        try:
            child = subprocess.Popen([tool, *args], cwd=self.root, env=env,
                                     stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            row["pid"] = child.pid
            save(dest, row)
            raw, err = child.communicate(timeout=90)
            dest.with_suffix(".stdout").write_bytes(raw)
            row.update(state="returned", exit_code=child.returncode, returned_at=now(),
                       stdout_file=dest.with_suffix(".stdout").name, stdout_bytes=len(raw),
                       stdout_sha256=hashlib.sha256(raw).hexdigest(), stderr=err.decode("utf-8", "replace")[:1600])
        except subprocess.TimeoutExpired:
            # This exact Popen handle belongs to this invocation; never kill by process name.
            child.kill()
            child.communicate()
            row.update(state="uncertain", exit_code=None, returned_at=now(), error="child timeout; reconcile")
        except OSError as exc:
            row.update(state="not_started" if child is None else "uncertain", exit_code=None,
                       returned_at=now(), error=str(exc))
        save(dest, row)
        post = dict(pre_call_id=key, run_id=self.run.name, returned_at=now(), calls=[row],
                    cumulative_observed_after=prior + 1)
        save(self.run / "owner-pipeline" / ("post-" + key + ".json"), post, exclusive=True)
        print(tracker.encoded(dict(post_call=post)), flush=True)
        tracker.require(row["state"] == "returned" and row["exit_code"] == 0,
                        "action failed; retained without retry: " + key)
        self.rows.append(row)
        return row

    def gh(self, endpoint, kind, rid=None, fields=()):
        return self.call("gh", ["api", "--method", "GET", "--include", endpoint, *fields], kind, rid)

    def response(self, row):
        return source_check.read_response(row, self.run / "results" / (row["id"] + ".json"), False)


def remote_head(transport, kind, *, reuse=False):
    row = transport.call("git", ["ls-remote", "--symref", "origin", "HEAD"], kind, reuse=reuse)
    raw = (transport.run / "results" / row["stdout_file"]).read_bytes()
    match = re.fullmatch(rb"ref: refs/heads/main\tHEAD\r?\n([a-f0-9]{40})\tHEAD\r?\n", raw)
    tracker.require(match, "remote default branch must resolve to main")
    return match[1].decode()


def acquire(root, run, clearance):
    status = local.lock_status(root)
    if status["state"] == "unlocked":
        return local.acquire(root, run.name)
    tracker.require(clearance, "existing lock: Agent must reconcile and provide --clearance; no automatic takeover")
    evidence = tracker.load(clearance)
    tracker.require(evidence["run_id"] == status.get("run_id") == run.name, "clearance run differs")
    owner_path = run / "owner-pipeline/owner.json"
    if not owner_path.exists():
        owner_path = run / "lock-owner.json"
    return local.resume(root, run.name, tracker.load(owner_path)["owner_token"], clearance)


def frozen_inputs(root, run, base):
    _, blobs, index = local.inspect(root, base)
    fixed = run / "owner-pipeline/fixed"
    paths = (*local.REQUIRED, "config/local-runtime.json", "docs/local-maintenance.md",
             "docs/local-scheduled-task-prompt.md")
    for path in paths:
        target = fixed / path
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = local.read_blob(root, blobs, path)
        if target.exists():
            tracker.require(target.read_bytes() == raw, "fixed baseline changed; Agent reconciliation required")
        else:
            target.write_bytes(raw)
    save(run / "owner-pipeline/base-manifest.json", local.manifest(root, base))
    if index["snapshots"]:
        prior = local.read_blob(root, blobs, index["snapshots"][-1]["path"])
        (run / "owner-pipeline/previous-batch.json").write_bytes(prior)
    return fixed


def source_value(transport, row, value):
    return dict(status="ok", observed_at=row["returned_at"],
                source_url="https://api.github.com/" + source_check.api_endpoint(row["args"]), value=value)


def build_batch(transport, fixed, base):
    registry = tracker.load(fixed / "data/projects.json")
    prior = tracker.load(fixed / "state/checkpoints.json")["sources"]
    observations, pages_by_id = [], {}
    for project in registry["projects"]:
        rid, name = project["repository_id"], project["full_name"]
        rows = [r for r in transport.rows if r.get("repository_id") == rid]
        met, = [r for r in rows if r["kind"] == "metadata"]
        head, = [r for r in rows if r["kind"] == "head"]
        _, m = transport.response(met)
        _, h = transport.response(head)
        tracker.require(m["id"] == rid and m["private"] is False, "source identity differs")
        tracker.require(h["ref"] == "refs/heads/" + m["default_branch"], "HEAD branch differs")
        tracker.require(h["object"]["type"] == "commit", "HEAD is not a commit")
        name = m["full_name"]
        releases = sorted([r for r in rows if r["kind"] == "releases"],
                          key=lambda x: int(x["args"][4].rsplit("=", 1)[1]))
        values, pages = [], []
        known = {v["id"] for v in prior.get(str(rid), {}).get("releases", {}).get("value") or []}
        for number, row in enumerate(releases, 1):
            more, items = transport.response(row)
            values += [dict(id=x["id"], tag=x["tag_name"], published_at=x["published_at"], url=x["html_url"])
                       for x in items if not x["draft"]]
            pages.append(dict(page=number, observed_at=row["returned_at"], returned=len(items),
                              source_url=local.release_page_url(row["args"], name, number, 30)))
        overlap = any(x["id"] in known for x in values)
        complete = overlap or len(items) < 30 or not more
        rel = source_value(transport, releases[0], values)
        rel.update(observed_at=releases[-1]["returned_at"], complete=complete,
                   pagination=dict(pages_obtained=len(releases),
                       scope="incremental_since_previous_success" if str(rid) in prior else "initial_baseline",
                       stop_reason="prior_release_id_reached" if overlap else "collection_exhausted" if complete else "next_page_due"))
        meta = dict(stars=m["stargazers_count"], forks=m["forks_count"], archived=m["archived"],
                    default_branch=m["default_branch"], created_at=m["created_at"], pushed_at=m["pushed_at"],
                    license_spdx=(m.get("license") or {}).get("spdx_id"))
        observations.append(dict(repository_id=rid, full_name=name, metadata=source_value(transport, met, meta),
                                 head=source_value(transport, head, h["object"]["sha"]), releases=rel))
        pages_by_id[str(rid)] = pages
    discovery = []
    for row in transport.rows:
        if row.get("kind") != "discovery":
            continue
        more, obj = transport.response(row)
        params = source_check.discovery_args(row["args"])
        items = [dict(repository_id=x["id"], full_name=x["full_name"], source_url=x["html_url"],
                      description=x.get("description"), license_spdx=(x.get("license") or {}).get("spdx_id")) for x in obj["items"]]
        discovery.append(dict(params, returned=len(items), items=items, total_count=obj.get("total_count"),
            incomplete_results=obj.get("incomplete_results"), observed_at=row["returned_at"],
            pagination_complete=False if more else True if obj.get("incomplete_results") is False
                and obj.get("total_count") == len(items) else None, stop_reason="bounded_first_page"))
    batch = dict(schema_version="1.0", run_id=transport.run.name, run_type="interactive", base_commit_sha=base,
                 observed_at=max([o[k]["observed_at"] for o in observations for k in tracker.SOURCES]
                                 + [q["observed_at"] for q in discovery]),
                 expected_repository_ids=[p["repository_id"] for p in registry["projects"]],
                 observations=observations, discovery=discovery, events=[])
    prep = tracker.load(transport.run / "owner-pipeline/preparation.json")
    batch["trigger_evidence"] = dict(schema_version="1.0", capture_id=transport.run.name + "-owner-handoff",
        captured_at=prep["prepared_at"], legacy_run_type="interactive", label_is_trigger_proof=False,
        trigger_kind="unknown", verification_status="unverified", platform_lookup="not_exposed",
        invocation_match="unknown", scheduled_for=None, started_at=None, time_scope="none",
        identity_presence=dict(automation_id=False, platform_run_id=False, current_invocation=False, binding=False),
        unknown_reasons=["Owner collection does not authenticate the native automation trigger."], conflicts=[])
    tracker.validate_batch(batch, tracker.validate_registry(registry))
    source_check.verify(batch, transport.run / "results", tracker.load(fixed / "state/checkpoints.json"))
    return batch, pages_by_id


def collect(transport, base):
    root, run = transport.root, transport.run
    tracker.require(not local.git(root, "status", "--porcelain=v1", "--untracked-files=all"), "preserve dirty worktree")
    resuming = any(x.get("kind") == "owner-bootstrap-head" for x in transport.rows)
    fresh = remote_head(transport, "owner-bootstrap-head", reuse=True)
    if resuming:
        tracker.require(remote_head(transport, "owner-resume-bootstrap-head-" + str(len(transport.rows))) == fresh,
                        "remote moved since interrupted bootstrap; Agent reconciliation required")
    transport.call("git", ["fetch", "--no-tags", "origin", "main"], "owner-fetch")
    transport.call("git", ["merge", "--ff-only", "origin/main"], "owner-ff-only")
    local.preflight(root, fresh, active=True)
    base = fresh
    old_entry = run / "entry.json"
    if old_entry.exists() and tracker.load(old_entry)["base"] != base:
        original = tracker.load(old_entry)["base"]
        reconciliation = tracker.load(run / "owner-pipeline/base-reconciliation.json")
        tracker.require(reconciliation["run_id"] == run.name and reconciliation["old_base_sha"] == original
                        and reconciliation["new_base_sha"] == base and reconciliation["reuse_sources"] is True,
                        "Agent must explicitly reconcile changed base; preserve original entry")
        for path in ("config/tracker.json", "data/projects.json", "data/candidates.json",
                     "state/checkpoints.json", "state/validation-index.json"):
            tracker.require(local.git(root, "show", original + ":" + path) == local.git(root, "show", base + ":" + path),
                            "base contract changed; Agent must reconcile sources: " + path)
    fixed = frozen_inputs(root, run, base)
    index = tracker.load(fixed / "state/validation-index.json")
    tracker.require(not any(x["run_id"] == run.name for x in index["snapshots"]),
                    "Data already exists; recover Receipt/readback, never collect this run again")
    tree = local.manifest(root, base)
    _, remote_commit = transport.response(transport.gh(f"repos/{REPO}/git/commits/{base}", "owner-base-commit"))
    _, remote_tree = transport.response(transport.gh(f"repos/{REPO}/git/trees/{tree['base_tree_sha']}?recursive=1", "owner-base-tree"))
    tracker.require(remote_commit["sha"] == base and remote_commit["tree"]["sha"] == tree["base_tree_sha"], "remote base differs")
    remote_manifest = dict(tree, entries=remote_tree["tree"], truncated=remote_tree["truncated"])
    tracker.require(remote_tree["sha"] == tree["base_tree_sha"], "remote root tree differs")
    tracker.require(manifest.validate_tree_manifest(tracker, remote_manifest) == manifest.validate_tree_manifest(tracker, tree),
                    "remote/local complete tree differ")
    registry = tracker.load(fixed / "data/projects.json")
    prior = tracker.load(fixed / "state/checkpoints.json")["sources"]
    for project in registry["projects"]:
        rid = project["repository_id"]
        row = transport.gh("repos/" + project["full_name"], "metadata", rid)
        _, obj = transport.response(row)
        tracker.require(obj["id"] == rid and obj["private"] is False, "metadata identity differs")
        endpoint = "repos/" + obj["full_name"]
        transport.gh(endpoint + "/git/ref/heads/" + obj["default_branch"], "head", rid)
        known = {v["id"] for v in prior.get(str(rid), {}).get("releases", {}).get("value") or []}
        page = 1
        while True:
            row = transport.gh(endpoint + f"/releases?per_page=30&page={page}", "releases", rid)
            local.release_page_url(row["args"], obj["full_name"], page, 30)
            more, values = transport.response(row)
            tracker.require(isinstance(values, list) and len(values) <= 30, "invalid Release page")
            if len(values) < 30 or not more or any(v["id"] in known for v in values if not v["draft"]):
                break
            page += 1
    cfg = tracker.load(fixed / "config/queries.json")
    templates = {x["id"]: x["template"] for x in cfg["channels"]}
    date = datetime.strptime(run.name[:8], "%Y%m%d").date()
    keywords = cfg["rotate_keywords"]
    for offset, channel in enumerate(("broad", "new")):
        query = templates[channel].format(keyword=keywords[(date.toordinal() + offset) % len(keywords)],
                                          since_30d=(date - timedelta(days=30)).isoformat())
        fields = ["-f", "q=" + query, "-f", "page=1", "-f", "per_page=" + str(cfg["per_page"]),
                  "-f", "sort=updated", "-f", "order=desc"]
        transport.gh("search/repositories", "discovery", fields=fields)
    batch, pages = build_batch(transport, fixed, base)
    save_consistent(run / "owner-pipeline/batch.json", batch)
    save_consistent(run / "owner-pipeline/release-pages.json", pages)
    previous_path = run / "owner-pipeline/previous-batch.json"
    previous = {o["repository_id"]: o for o in tracker.load(previous_path)["observations"]} if previous_path.exists() else {}
    changes = [dict(repository_id=o["repository_id"], full_name=o["full_name"],
                    old_head=previous[o["repository_id"]]["head"]["value"], head=o["head"]["value"])
               for o in batch["observations"] if o["repository_id"] in previous
               and previous[o["repository_id"]]["head"]["value"] != o["head"]["value"]]
    for change in changes:
        transport.gh(f"repos/{change['full_name']}/compare/{change['old_head']}...{change['head']}",
                     "review-compare", change["repository_id"])
    save_consistent(run / "owner-pipeline/change-leads.json", changes)
    return dict(status="sources_ready_for_agent_review", repository=REPO, run_id=run.name,
                base_commit_sha=base, completed_at=now(), expected=len(batch["observations"]),
                source_coverage={k: sum(o[k]["status"] == "ok" and (k != "releases" or o[k]["complete"])
                                       for o in batch["observations"]) for k in tracker.SOURCES},
                batch="owner-pipeline/batch.json", review_leads="owner-pipeline/change-leads.json",
                agent_review="Not Run", publication="Not Run", trigger="unknown/unverified",
                instrumentation_complete=False, reason="manual package does not authenticate host trigger or prior cross-turn accounting")


def validate_review_plan(plan):
    tracker.require(plan["repository"] == REPO and bool(tracker.RUN.fullmatch(plan["run_id"])), "review plan identity")
    tracker.require(len(plan["requests"]) <= 50, "review plan too large")
    tracker.require(len({r["repository_id"] for r in plan["requests"]}) <= 15, "review budget: max 10 candidates + 5 change projects")
    for item in plan["requests"]:
        tracker.require(type(item["repository_id"]) is int and tracker.NAME.fullmatch(item["full_name"]), "review identity")
        endpoint = item["endpoint"]
        prefix = "repos/" + item["full_name"] + "/"
        tracker.require(endpoint.startswith(prefix) and not any(s in endpoint for s in ("..", "\\", "#", "\n")), "unsafe review endpoint")
        tail = endpoint[len(prefix):]
        allowed = (re.fullmatch(r"pulls/\d+(?:/files\?per_page=100&page=\d+)?", tail)
                   or re.fullmatch(r"contents/[^?]+\?ref=[a-f0-9]{40}", tail)
                   or re.fullmatch(r"git/(?:(?:commits|blobs|tags)/[a-f0-9]{40}|trees/[a-f0-9]{40}\?recursive=1|ref/tags/[^?]+)", tail))
        tracker.require(allowed, "review GET endpoint not allowed")


def fetch_review(transport, plan):
    validate_review_plan(plan)
    tracker.require(plan["run_id"] == transport.run.name, "review batch mismatch")
    registry = tracker.load(transport.run / "owner-pipeline/fixed/data/projects.json")
    known = tracker.validate_registry(registry)
    selected = {r["repository_id"] for r in plan["requests"]}
    selected |= {r["repository_id"] for r in transport.rows if r.get("kind") == "review-evidence"}
    endpoints = {r["args"][4] for r in transport.rows if r.get("kind") == "review-evidence"}
    endpoints |= {r["endpoint"] for r in plan["requests"]}
    tracker.require(len(endpoints) <= 50, "cumulative review request budget exceeded")
    tracker.require(len(selected & known) <= 5 and len(selected - known) <= 10, "cumulative review budget exceeded")
    for request in plan["requests"]:
        # A review plan is data, not permission to read private repositories.
        matches = [r for r in transport.rows if r.get("repository_id") == request["repository_id"]
                   and r.get("kind") in ("metadata", "review-metadata")]
        metadata = matches[0] if matches else transport.gh("repos/" + request["full_name"], "review-metadata", request["repository_id"])
        _, obj = transport.response(metadata)
        tracker.require(obj["id"] == request["repository_id"] and obj["full_name"] == request["full_name"]
                        and obj["private"] is False, "review requires matching public repository")
        transport.gh(request["endpoint"], "review-evidence", request["repository_id"])
    return dict(status="review_evidence_ready", run_id=transport.run.name, requests=len(plan["requests"]),
                semantic_review="Not Run")


def readback(transport, plan):
    """Independently retrieve actual commit/tree/changed bytes, then validate history."""
    prefix = "repos/" + REPO + "/git/"
    phase = plan["phase"]
    _, commit = transport.response(transport.gh(prefix + "commits/" + plan["commit_sha"], phase + "-commit-readback"))
    tracker.require(commit["sha"] == plan["commit_sha"] and commit["tree"]["sha"] == plan["tree_sha"]
                    and [p["sha"] for p in commit["parents"]] == [plan["parent_sha"]], "remote commit differs")
    _, tree = transport.response(transport.gh(prefix + "trees/" + plan["tree_sha"] + "?recursive=1", phase + "-tree-readback"))
    remote_manifest = dict(schema_version="1.0", repository=REPO, base_commit_sha=plan["commit_sha"],
                           base_tree_sha=plan["tree_sha"], truncated=tree["truncated"],
                           entries=tree["tree"], entry_count=len(tree["tree"]))
    tracker.require(tree["sha"] == plan["tree_sha"], "remote tree identity")
    blobs = manifest.validate_tree_manifest(tracker, remote_manifest)
    actual_bytes = {}
    # Index/snapshot are read independently even in Receipt, where they did not change.
    names = set(plan["changed_blobs"]) | {"state/validation-index.json"}
    for name in sorted(names):
        _, obj = transport.response(transport.gh(prefix + "blobs/" + blobs[name]["sha"], phase + "-blob-readback"))
        raw = base64.b64decode(obj["content"], validate=False)
        tracker.require(obj["encoding"] == "base64" and obj["sha"] == blobs[name]["sha"]
                        and len(raw) == obj["size"] and manifest.git_blob_sha_bytes(raw) == obj["sha"], "remote blob bytes differ")
        tracker.require(raw == local.git(transport.root, "cat-file", "blob", blobs[name]["sha"]), "remote/local bytes differ")
        actual_bytes[name] = raw
    index = json.loads(actual_bytes["state/validation-index.json"])
    tracker.require({e["path"]: e["blob_sha"] for e in index["snapshots"]} ==
                    {p: v["sha"] for p, v in blobs.items() if re.fullmatch(r"data/snapshots/\d{4}/\d{2}/[^/]+\.json", p)}, "remote snapshot/index mismatch")
    snapshot = next(e for e in index["snapshots"] if e["run_id"] == transport.run.name)
    _, obj = transport.response(transport.gh(prefix + "blobs/" + snapshot["blob_sha"], phase + "-snapshot-readback"))
    raw = base64.b64decode(obj["content"])
    tracker.require(manifest.git_blob_sha_bytes(raw) == snapshot["blob_sha"] == obj["sha"] and len(raw) == obj["size"], "snapshot bytes differ")
    tracker.require(raw == local.git(transport.root, "cat-file", "blob", snapshot["blob_sha"]), "snapshot local/remote differ")
    _, ref = transport.response(transport.gh(prefix + "ref/heads/main", phase + "-ref-readback"))
    tracker.require(ref["object"]["sha"] == plan["commit_sha"], "remote main moved; reconcile ancestry before claiming readback")
    for name, value in actual_bytes.items():
        dest = transport.run / "owner-pipeline" / (phase + "-remote") / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(value)
    result = dict(status="passed", phase=phase, commit_sha=plan["commit_sha"], verified_paths=len(plan["changed_blobs"]),
                  expected_paths=len(plan["changed_blobs"]), completed_at=now())
    save(transport.run / "owner-pipeline" / (phase + "-remote-manifest.json"), remote_manifest, exclusive=True)
    save(transport.run / "owner-pipeline" / (phase + "-readback.json"), result, exclusive=True)
    return result


def artifacts(run):
    paths = [*sorted((run / "results").glob("*.json")), *sorted((run / "results").glob("*.stdout")),
             *sorted((run / "owner-pipeline/fixed").rglob("*"))]
    paths += [p for p in (run / "owner-pipeline").glob("*.json")
              if p.name not in ("SUMMARY.json", "owner.json", "preparation.json", "FAILED.json")]
    return {p.relative_to(run).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def verify_package(root, run):
    packet = tracker.load(run / "owner-pipeline/SUMMARY.json")
    tracker.require(packet["repository"] == REPO and packet["run_id"] == run.name, "SUMMARY identity differs")
    tracker.require(packet.get("status") == "sources_ready_for_agent_review" and bool(packet.get("artifacts")), "SUMMARY is not a source package")
    required = {"owner-pipeline/batch.json", "owner-pipeline/fixed/data/projects.json", "owner-pipeline/fixed/state/checkpoints.json"}
    tracker.require(required <= packet["artifacts"].keys(), "package is missing required inputs")
    for rel, digest in packet["artifacts"].items():
        p = (run / rel).resolve()
        tracker.require(p.is_relative_to(run.resolve()) and hashlib.sha256(p.read_bytes()).hexdigest() == digest,
                        "package artifact changed: " + rel)
    fixed = run / "owner-pipeline/fixed"
    batch = tracker.load(run / "owner-pipeline/batch.json")
    tracker.require(batch["run_id"] == run.name and batch["base_commit_sha"] == packet["base_commit_sha"], "package batch/base mismatch")
    tracker.validate_batch(batch, tracker.validate_registry(tracker.load(fixed / "data/projects.json")))
    source_check.verify(batch, run / "results", tracker.load(fixed / "state/checkpoints.json"))
    return dict(status="Passed", scope="offline_package_consistency_not_trigger_authentication", run_id=run.name)


def main(*, default_collect=False):
    parser = argparse.ArgumentParser(description=__doc__)
    command_default = dict(nargs="?", default="collect") if default_collect else {}
    parser.add_argument("command", choices=("check", "prepare", "collect", "review-fetch", "verify-package", "acquire", "release", "publish", "readback", "resume-draft", "extract-review", "create-entry"), **command_default)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--run-id")
    parser.add_argument("--clearance", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--phase", choices=("data", "receipt"))
    parser.add_argument("--commit")
    parser.add_argument("--owner-file", type=Path)
    parser.add_argument("--resume-evidence", type=Path)
    parser.add_argument("--resume-command", choices=("collect", "review-fetch"))
    parser.add_argument("--program-commit")
    parser.add_argument("--entry-program", choices=("owner_pipeline", "staged_publication"), default="owner_pipeline")
    parser.add_argument("--entry-command", default="collect")
    args = parser.parse_args()
    root = args.root.resolve()
    run = None
    try:
        if args.command == "check":
            print(tracker.encoded(check(root))); return
        if args.command == "prepare":
            print(tracker.encoded(prepare(root, args.run_id))); return
        if not args.run_id:
            args.run_id = tracker.load(root / ".cache/owner-current.json")["run_id"]
        run = run_dir(root, args.run_id)
        tracker.require(run.is_dir(), "prepare this run first")
        if args.command == "verify-package":
            print(tracker.encoded(verify_package(root, run))); return
        ordinary_user(); gates(root)
        if completed(root, run):
            print("Already complete. No network, lock or publication action. SUMMARY: " + str(run / "final-completion.json")); return
        if args.command in ("resume-draft", "extract-review", "create-entry"):
            import handoff_support as support
            if args.command == "resume-draft":
                tracker.require(args.resume_command, "--resume-command required")
                result = support.resume_draft(sys.modules[__name__], root, run, args.resume_command)
            elif args.command == "extract-review":
                tracker.require(args.plan, "--plan required")
                result = support.extract_review(sys.modules[__name__], root, run, tracker.load(args.plan))
            else:
                tracker.require(args.program_commit, "--program-commit required")
                result = support.create_entry(sys.modules[__name__], root, run, args.program_commit, args.entry_program, args.entry_command)
            print(tracker.encoded(result)); return
        if args.command == "acquire":
            token = acquire(root, run, args.clearance)
            owner_path = run / "owner-pipeline/agent-owner.json"
            save(owner_path, token)
            tracker.require(tracker.load(local.lock_path(root)) == token, "lock readback differs")
            print("Agent lock saved privately: " + str(owner_path)); return
        if args.command == "release":
            token = tracker.load(run / "owner-pipeline/agent-owner.json")
            print(tracker.encoded(local.release(root, run.name, token["owner_token"]))); return
        summary = run / "owner-pipeline/SUMMARY.json"
        if args.command == "collect" and summary.exists():
            print(tracker.encoded(verify_package(root, run)))
            print("Already collected. No network, lock or publication action. SUMMARY: " + str(summary)); return
        if args.command in ("publish", "readback") and args.phase and args.commit:
            proof_path = run / "owner-pipeline" / (args.phase + "-readback.json")
            if proof_path.exists():
                proof = tracker.load(proof_path)
                tracker.require(proof["status"] == "passed" and proof["commit_sha"] == args.commit, "existing phase proof differs")
                print(tracker.encoded(proof)); print("Phase already read back; no network or lock action."); return
        if (run / "owner-pipeline/FAILED.json").exists() and args.command != "readback":
            import handoff_support as support
            tracker.require(args.resume_evidence, "prior failure retained; reviewed --resume-evidence required")
            tracker.require(args.command in ("collect", "review-fetch"), "published/uncertain writes require explicit readback, not replay")
            support.validate_resume(sys.modules[__name__], root, run, args.command, args.resume_evidence)
        borrowed = args.owner_file is not None
        if borrowed:
            tracker.require(args.owner_file.resolve().is_relative_to(run.resolve()), "owner file must be run-local")
            owner = tracker.load(args.owner_file)
        else:
            owner = acquire(root, run, args.clearance)
            save(run / "owner-pipeline/owner.json", owner)
        tracker.require(tracker.load(local.lock_path(root)) == owner, "lock readback differs")
        transport = Transport(root, run, allow_unresolved=args.command == "readback")
        if args.command == "collect":
            result = collect(transport, None)
        elif args.command == "review-fetch":
            tracker.require(args.plan, "--plan required")
            result = fetch_review(transport, tracker.load(args.plan))
        else:
            tracker.require(args.phase and args.commit, "--phase and --commit required")
            plan = local.publication_plan(root, args.commit, args.phase, run.name)
            save(run / "owner-pipeline" / (args.phase + "-plan.json"), plan)
            if args.command == "publish":
                tracker.require(local.pin(root, "HEAD") == plan["commit_sha"], "publication is not current HEAD")
                tracker.require(remote_head(transport, args.phase + "-pre-push-head") == plan["parent_sha"], "remote moved; reconcile once, no blind push")
                if args.phase == "receipt":
                    proof = tracker.load(run / "owner-pipeline/data-readback.json")
                    tracker.require(proof["status"] == "passed" and proof["commit_sha"] == plan["parent_sha"], "Data readback gate")
                transport.call("git", ["push", "origin", plan["commit_sha"] + ":refs/heads/main"], args.phase + "-push", reuse=False)
            result = readback(transport, plan)
        if not borrowed:
            local.release(root, run.name, owner["owner_token"])
            tracker.require(local.lock_status(root)["state"] == "unlocked", "release readback failed")
        if args.command == "collect":
            result.update(lock_released=True, artifacts=artifacts(run))
            save(summary, result, exclusive=True)
        elif args.command == "review-fetch":
            # Additional evidence extends the package, never rewrites retained source bytes.
            packet = tracker.load(summary); packet["artifacts"] = artifacts(run)
            save(summary, packet)
        print(tracker.encoded(result)); print("SUMMARY: " + str(summary))
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as exc:
        if run is not None and run.is_dir():
            path = run / "owner-pipeline/FAILED.json"
            failure = dict(status="Failed", repository=REPO, run_id=run.name, pid=os.getpid(),
                           at=now(), action=args.command, error=str(exc),
                           lock="preserved if acquired; Agent must reconcile before release")
            if not path.exists():
                save(path, failure, exclusive=True)
            else:
                save(run / "owner-pipeline/failures" / (now().replace(":", "") + "-" + str(os.getpid()) + ".json"), failure, exclusive=True)
            print("SUMMARY: " + str(path), file=sys.stderr)
        parser.exit(1, "Stage stopped without retry: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
