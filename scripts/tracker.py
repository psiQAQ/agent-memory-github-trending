"""Offline tracker utilities. Network reads and Git publication belong to the authorized GPT task."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo

VERSION = "1.0"
TARGET = "psiQAQ/agent-memory-github-trending"
SOURCES = ("metadata", "head", "releases")
SHA = re.compile(r"[0-9a-f]{40}")
NAME = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
RUN = re.compile(r"[0-9]{8}T[0-9]{6}Z-[a-z0-9-]+")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def stamp(value: str) -> datetime:
    require(isinstance(value, str) and value.endswith("Z"), "timestamp must be UTC ending Z")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.utcoffset() == timedelta(0), "timestamp is not UTC")
    return result


def url(value: str) -> None:
    require(isinstance(value, str) and value.startswith("https://") and not any(c.isspace() for c in value), "invalid source URL")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded(value), encoding="utf-8")


def safe_path(value: str) -> None:
    p = PurePosixPath(value)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in value and str(p) == value, "unsafe relative path")


def guard_paths(paths: list[str]) -> None:
    for path in paths:
        safe_path(path)
        require(path == "README.md" or path.startswith(("data/", "projects/", "reports/", "state/")), "routine write outside scope: " + path)


def event_id(event: dict) -> str:
    identity = [event["repository_id"], event["type"], event["source_url"], event["source_version_or_sha"]]
    return hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode()).hexdigest()[:24]


def validate_registry(registry: dict) -> set[int]:
    require(registry["schema_version"] == VERSION, "registry version")
    ids, names = set(), set()
    for p in registry["projects"]:
        rid, name = p["repository_id"], p["full_name"]
        require(type(rid) is int and rid > 0 and rid not in ids, "duplicate/invalid repository ID")
        require(bool(NAME.fullmatch(name)) and name.lower() not in names, "duplicate/invalid repository name")
        require(p["status"] in ("tracked", "reference", "watchlist", "candidate", "retired"), "project status")
        require(p["kind"] in ("engineering", "research", "benchmark", "reference"), "project kind")
        stamp(p["first_discovered_at"])
        require(p["evidence_level"] in ("upstream_statement", "code_inspected"), "unverified reproduction")
        url(p["source_url"])
        if p["status"] in ("tracked", "reference"):
            safe_path(p["card"])
            require(bool(p["summary"]) and bool(p["implementation_evidence"]), "missing admission evidence")
            url(p["implementation_evidence"])
        ids.add(rid)
        names.add(name.lower())
    require(len(ids) <= 50, "project pool exceeds approved capacity")
    return ids


def validate_batch(batch: dict, ids: set[int]) -> None:
    require(batch["schema_version"] == VERSION and bool(RUN.fullmatch(batch["run_id"])), "batch version/run ID")
    require(batch["run_type"] in ("interactive_baseline", "scheduled", "interactive"), "run type")
    end = stamp(batch["observed_at"])
    require(bool(SHA.fullmatch(batch["base_commit_sha"])), "invalid base commit")
    expected = batch["expected_repository_ids"]
    require(len(expected) == len(set(expected)) and set(expected) <= ids, "expected IDs")
    seen = set()
    for obs in batch["observations"]:
        rid = obs["repository_id"]
        require(type(rid) is int and rid in expected and rid not in seen, "unexpected/duplicate observation")
        require(bool(NAME.fullmatch(obs["full_name"])), "observation repository name")
        seen.add(rid)
        for name in SOURCES:
            source = obs[name]
            require(source["status"] in ("ok", "error", "not_collected"), "source status")
            require(stamp(source["observed_at"]) <= end, "source observed after batch")
            url(source["source_url"])
            prefix = f"https://api.github.com/repos/{obs['full_name']}"
            require(source["source_url"] == prefix or source["source_url"].startswith(prefix + "/") or source["source_url"].startswith(prefix + "?"), "source repository mismatch")
            if source["status"] != "ok":
                require(source["value"] is None and bool(source.get("reason")), "failed source must be null with reason")
                continue
            val = source["value"]
            if name == "metadata":
                for field in ("stars", "forks"):
                    require(type(val[field]) is int and val[field] >= 0, "invalid count")
                require(type(val["archived"]) is bool and bool(val["default_branch"]), "metadata fields")
                stamp(val["created_at"])
                if val.get("pushed_at") is not None:
                    stamp(val["pushed_at"])
            elif name == "head":
                require(isinstance(val, str) and bool(SHA.fullmatch(val)), "invalid HEAD")
            else:
                require(isinstance(val, list) and type(source["complete"]) is bool, "release collection contract")
                release_ids = set()
                for release in val:
                    require(type(release["id"]) is int and release["id"] not in release_ids, "release ID")
                    release_ids.add(release["id"])
                    stamp(release["published_at"])
                    url(release["url"])
    require(seen == set(expected), "missing expected observation; record not_collected explicitly")
    events = set()
    for event in batch["events"]:
        require(event["repository_id"] in ids and event["event_id"] == event_id(event), "event identity")
        require(event["event_id"] not in events, "duplicate event")
        events.add(event["event_id"])
        url(event["source_url"])
        require(stamp(event["observed_at"]) <= end, "event observation after batch")
        if event["event_at"] is not None:
            require(stamp(event["event_at"]) <= end, "future event")
        require(event["evidence_level"] in ("upstream_statement", "code_inspected"), "reproduction not authorized")
        require(bool(event["claim"]) and bool(event["source_version_or_sha"]), "missing event evidence")
    for q in batch["discovery"]:
        require(bool(q["query"]) and q["page"] >= 1 and q["returned"] >= 0, "query log")
        stamp(q["observed_at"])
        require(q["incomplete_results"] in (None, True, False), "unknown search completeness")
        require(q["pagination_complete"] in (None, True, False), "unknown pagination")


def merge_events(old: list[dict], incoming: list[dict]) -> list[dict]:
    result = {e["event_id"]: e for e in old}
    for e in incoming:
        if e["event_id"] in result:
            # Observation time may differ on a retry; source identity and claim must not.
            a = {k: v for k, v in result[e["event_id"]].items() if k != "observed_at"}
            b = {k: v for k, v in e.items() if k != "observed_at"}
            require(a == b, "event changed: issue an explicit correction with a new source version")
        else:
            result[e["event_id"]] = e
    return sorted(result.values(), key=lambda e: (e["observed_at"], e["event_id"]))


def growth(observations: list[dict], rid: int, days: int, tolerance_hours: int = 6):
    good = sorted((o for o in observations if o["repository_id"] == rid and o["metadata"]["status"] == "ok"), key=lambda o: o["metadata"]["observed_at"])
    if len(good) < 2:
        return None
    current = good[-1]["metadata"]
    end = stamp(current["observed_at"])
    target = end - timedelta(days=days)
    candidates = [o["metadata"] for o in good[:-1] if stamp(o["metadata"]["observed_at"]) < end and abs(stamp(o["metadata"]["observed_at"]) - target) <= timedelta(hours=tolerance_hours)]
    if not candidates:
        return None
    base = min(candidates, key=lambda s: (abs(stamp(s["observed_at"]) - target), s["observed_at"]))
    start = stamp(base["observed_at"])
    before, after = base["value"]["stars"], current["value"]["stars"]
    elapsed = (end - start).total_seconds() / 86400
    return {"baseline_at": base["observed_at"], "observed_at": current["observed_at"], "actual_days": elapsed, "baseline_stars": before, "net_stars": after - before, "stars_per_day": (after - before) / elapsed, "relative_growth": (after - before) / before if before else None}


def closed_weeks(since: str, now: str) -> list[str]:
    tz = ZoneInfo("Asia/Shanghai")
    start, end = stamp(since).astimezone(tz), stamp(now).astimezone(tz)
    monday = (start - timedelta(days=start.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    result = []
    while monday + timedelta(days=7) <= end:
        y, w, _ = monday.isocalendar()
        result.append(f"{y}-W{w:02d}")
        monday += timedelta(days=7)
    return result


def snapshot_path(batch: dict) -> str:
    dt = stamp(batch["observed_at"])
    return f"data/snapshots/{dt:%Y/%m}/{batch['run_id']}.json"


def all_batches(root: Path) -> list[dict]:
    return [load(p) for p in sorted((root / "data/snapshots").glob("*/*/*.json"))]


def render(root: Path) -> str:
    registry = load(root / "data/projects.json")
    batches = all_batches(root)
    require(bool(batches), "no snapshots")
    batches.sort(key=lambda b: b["observed_at"])
    latest = batches[-1]
    observations = [o for b in batches for o in b["observations"]]
    rows = ["# 当前观测", "", f"本轮：`{latest['run_id']}`；观测时间（UTC）：{latest['observed_at']}。", "", "这是观测表，不是技术质量排名。— 表示没有可比较基线；stale 表示本轮未取得新数值。", "", "| 项目 | 类别 | Stars | 7 日净变化 | 30 日净变化 | 新鲜度 |", "| --- | --- | ---: | ---: | ---: | --- |"]
    for p in sorted(registry["projects"], key=lambda p: (p["kind"], p["full_name"].lower())):
        if p["status"] not in ("tracked", "reference", "watchlist"):
            continue
        rid = p["repository_id"]
        good = [o for o in observations if o["repository_id"] == rid and o["metadata"]["status"] == "ok"]
        if not good:
            continue
        current = max(good, key=lambda o: o["metadata"]["observed_at"])
        fresh = any(o["repository_id"] == rid and o["metadata"]["status"] == "ok" for o in latest["observations"])
        metrics = [growth(observations, rid, d) if fresh else None for d in (7, 30)]
        values = [str(m["net_stars"]) if m else "—" for m in metrics]
        name = html.escape(p["full_name"]).replace("|", "&#124;")
        rows.append(f"| [{name}](../{p['card']}) | {p['kind']} | {current['metadata']['value']['stars']} | {values[0]} | {values[1]} | {'fresh' if fresh else 'stale'} |")
    rows += ["", "增长的实际区间由 `growth()` 返回；基线容差为 6 小时，不把观察期外推成完整一周。", "", "## 本轮来源覆盖", ""]
    for source in SOURCES:
        ok = sum(o[source]["status"] == "ok" for o in latest["observations"])
        rows.append(f"- {source}: {ok}/{len(latest['observations'])}")
    rows += ["", "来源未采集不代表没有发布或没有变更。项目卡片的机制说明均需查看其证据等级。", ""]
    return "\n".join(rows)


def validate_repo(root: Path) -> dict:
    config = load(root / "config/tracker.json")
    require(config["repository"] == TARGET and config["approval_state"] == "approved", "repository/approval gate")
    registry = load(root / "data/projects.json")
    ids = validate_registry(registry)
    require(len((root / "README.md").read_text(encoding="utf-8").splitlines()) <= config["settings"]["readme_max_lines"], "README too long")
    for p in registry["projects"]:
        if p["status"] in ("tracked", "reference"):
            require((root / p["card"]).is_file(), "missing project card")
    batches = all_batches(root)
    run_ids, events = set(), []
    for b in batches:
        validate_batch(b, ids)
        require(b["run_id"] not in run_ids, "duplicate run")
        run_ids.add(b["run_id"])
        events = merge_events(events, b["events"])
    return {"status": "passed", "snapshots": len(batches), "projects": len(ids), "unique_events": len(events)}


def prepare(root: Path, batch: dict) -> dict:
    config = load(root / "config/tracker.json")
    require(config["approval_state"] == "approved", "not approved")
    if batch["run_type"] == "scheduled":
        require(config["automation_enabled"] and config["implementation_ready"], "scheduled gate closed")
    validate_repo(root)
    validate_batch(batch, validate_registry(load(root / "data/projects.json")))
    path = snapshot_path(batch)
    target = root / path
    if target.exists():
        require(load(target) == batch, "run ID reused with different content")
        return {"status": "duplicate", "paths": []}
    old = all_batches(root)
    old_events = [e for b in old for e in b["events"]]
    merge_events(old_events, batch["events"])
    paths = [path, "reports/current.md"]
    guard_paths(paths)
    save(target, batch)
    (root / "reports").mkdir(parents=True, exist_ok=True)
    (root / "reports/current.md").write_text(render(root), encoding="utf-8")
    first = min([b["observed_at"] for b in old] + [batch["observed_at"]])
    due = [w for w in closed_weeks(first, batch["observed_at"]) if not (root / f"reports/weekly/{w}.md").exists()]
    return {"status": "prepared", "paths": paths, "weekly_reports_due": due, "validation": validate_repo(root)}


def receipt(root: Path, batch: dict, commit: str, readback_commit: str) -> dict:
    require(bool(SHA.fullmatch(commit)) and commit == readback_commit, "unverified publication")
    require(load(root / snapshot_path(batch)) == batch, "snapshot not reconciled")
    validate_repo(root)
    path = root / "state/checkpoints.json"
    state = load(path) if path.exists() else {"schema_version": VERSION, "sources": {}}
    for obs in batch["observations"]:
        slot = state["sources"].setdefault(str(obs["repository_id"]), {})
        for name in SOURCES:
            source = obs[name]
            previous = slot.get(name, {})
            newer = source["observed_at"] >= previous.get("last_attempt_at", "")
            if not newer:
                continue
            previous.update(last_attempt_at=source["observed_at"], status=source["status"])
            if source["status"] == "ok" and (name != "releases" or source["complete"]):
                previous.pop("reason", None)
                previous.update(last_success_at=source["observed_at"], data_commit_sha=commit, value=source["value"])
            else:
                previous["reason"] = source.get("reason", "incomplete pagination; watermark retained")
                if source["status"] == "ok":
                    previous["status"] = "partial"
            slot[name] = previous
    if batch["observed_at"] >= state.get("last_verified_observed_at", ""):
        state["last_verified_data_commit_sha"] = commit
        state["last_completed_run_id"] = batch["run_id"]
        state["latest_snapshot_path"] = snapshot_path(batch)
        state["last_verified_observed_at"] = batch["observed_at"]
    save(path, state)
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "render", "prepare", "receipt"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--batch", type=Path)
    parser.add_argument("--changed-file-list", type=Path)
    parser.add_argument("--commit")
    parser.add_argument("--readback-commit")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            if args.changed_file_list:
                guard_paths(load(args.changed_file_list))
            result = validate_repo(args.root)
        elif args.command == "render":
            print(render(args.root), end="")
            return
        else:
            require(args.batch is not None, "--batch required")
            batch = load(args.batch)
            result = prepare(args.root, batch) if args.command == "prepare" else receipt(args.root, batch, args.commit or "", args.readback_commit or "")
        print(encoded(result), end="")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f"Validation failed: {exc}\n")


if __name__ == "__main__":
    main()
