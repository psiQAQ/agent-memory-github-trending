"""Manifest-mode validation for tracker.py without a materialized historical worktree."""
from __future__ import annotations
import hashlib
import html
import json
import re
from pathlib import Path, PurePosixPath

EVENT = re.compile(r"[0-9a-f]{24}")
SNAPSHOT = re.compile(r"data/snapshots/[0-9]{4}/[0-9]{2}/[^/]+\.json")


def git_blob_sha_bytes(content: bytes) -> str:
    header = b"blob " + str(len(content)).encode("ascii") + b"\0"
    return hashlib.sha1(header + content).hexdigest()


def _tree_hash(data: bytes) -> str:
    return hashlib.sha1(b"tree " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _compute_tree(core, blobs: dict[str, dict]) -> tuple[str, dict[str, str]]:
    root: dict = {}
    for path, entry in blobs.items():
        parts = PurePosixPath(path).parts
        node = root
        for part in parts[:-1]:
            existing = node.setdefault(part, {})
            core.require(isinstance(existing, dict) and "__blob__" not in existing, "path collision")
            node = existing
        core.require(parts[-1] not in node, "duplicate path")
        node[parts[-1]] = {"__blob__": entry}
    tree_shas: dict[str, str] = {}

    def walk(node: dict, prefix: str) -> str:
        rows, children = [], []
        for name, value in node.items():
            is_tree = "__blob__" not in value
            children.append((name + ("/" if is_tree else ""), name, value, is_tree))
        for _, name, value, is_tree in sorted(children, key=lambda x: x[0].encode("utf-8")):
            if is_tree:
                path = f"{prefix}/{name}" if prefix else name
                sha, mode = walk(value, path), "40000"
            else:
                entry = value["__blob__"]
                sha, mode = entry["sha"], entry["mode"]
            rows.append(f"{mode} {name}".encode("utf-8") + b"\0" + bytes.fromhex(sha))
        sha = _tree_hash(b"".join(rows))
        if prefix:
            tree_shas[prefix] = sha
        return sha

    return walk(root, ""), tree_shas


def validate_tree_manifest(core, manifest: dict) -> dict[str, dict]:
    core.require(manifest["schema_version"] == core.VERSION, "manifest version")
    core.require(manifest["repository"] == core.TARGET, "manifest repository")
    core.require(bool(core.SHA.fullmatch(manifest["base_commit_sha"])) and bool(core.SHA.fullmatch(manifest["base_tree_sha"])), "manifest commit/tree SHA")
    core.require(manifest.get("truncated") is False, "manifest tree must be explicitly untruncated")
    entries = manifest["entries"]
    core.require(type(entries) is list and manifest.get("entry_count") == len(entries), "manifest entry count")
    seen, blobs, declared_trees = set(), {}, {}
    for entry in entries:
        path = entry["path"]
        core.safe_path(path)
        core.require(path not in seen, "duplicate manifest path")
        seen.add(path)
        core.require(bool(core.SHA.fullmatch(entry["sha"])), "manifest entry SHA")
        if entry["type"] == "blob":
            core.require(entry["mode"] == "100644", "unsupported blob mode")
            core.require(type(entry.get("size")) is int and entry["size"] >= 0, "manifest blob size")
            blobs[path] = {"path": path, "mode": "100644", "type": "blob", "sha": entry["sha"], "size": entry["size"]}
        else:
            core.require(entry["type"] == "tree" and entry["mode"] == "040000", "unsupported manifest entry")
            declared_trees[path] = entry["sha"]
    root_sha, computed_trees = _compute_tree(core, blobs)
    core.require(root_sha == manifest["base_tree_sha"], "manifest root tree mismatch")
    core.require(set(declared_trees) == set(computed_trees), "manifest tree path set mismatch")
    for path, sha in declared_trees.items():
        core.require(computed_trees[path] == sha, "manifest subtree mismatch: " + path)
    return blobs


def _normalized_event(event: dict) -> dict:
    return {k: v for k, v in event.items() if k != "observed_at"}


def summarize_batch(core, batch: dict) -> dict:
    stars = []
    coverage = {name: 0 for name in core.SOURCES}
    for obs in batch["observations"]:
        for name in core.SOURCES:
            if obs[name]["status"] == "ok":
                coverage[name] += 1
        meta = obs["metadata"]
        if meta["status"] == "ok":
            stars.append([obs["repository_id"], meta["observed_at"], meta["value"]["stars"]])
    return {
        "run_id": batch["run_id"],
        "observed_at": batch["observed_at"],
        "stars": stars,
        "coverage": coverage,
        "event_ids": sorted(e["event_id"] for e in batch["events"]),
    }


def empty_index(core) -> dict:
    return {"schema_version": core.VERSION, "snapshots": [], "events": []}


def validate_index(core, index: dict, ids: set[int] | None = None) -> dict:
    core.require(index["schema_version"] == core.VERSION, "validation index version")
    snapshots = index["snapshots"]
    core.require(type(snapshots) is list and type(index["events"]) is list, "validation index structure")
    known_events = set(index["events"])
    core.require(len(known_events) == len(index["events"]) and all(bool(EVENT.fullmatch(eid)) for eid in known_events), "validation index events")
    paths, runs = set(), set()
    for item in snapshots:
        path = item["path"]
        core.safe_path(path)
        core.require(bool(SNAPSHOT.fullmatch(path)), "validation index snapshot path")
        core.require(path not in paths and item["run_id"] not in runs, "duplicate indexed snapshot")
        paths.add(path); runs.add(item["run_id"])
        core.require(bool(core.RUN.fullmatch(item["run_id"])) and bool(core.SHA.fullmatch(item["blob_sha"])), "indexed run/blob")
        core.stamp(item["observed_at"])
        expected_path = f"data/snapshots/{core.stamp(item['observed_at']):%Y/%m}/{item['run_id']}.json"
        core.require(path == expected_path, "indexed snapshot path/time mismatch")
        seen_ids = set()
        for row in item["stars"]:
            core.require(type(row) is list and len(row) == 3, "indexed star row")
            rid, observed_at, stars = row
            core.require(type(rid) is int and rid not in seen_ids and (ids is None or rid in ids), "indexed observation ID")
            seen_ids.add(rid)
            core.stamp(observed_at)
            core.require(type(stars) is int and stars >= 0, "indexed stars")
        core.require(set(item["coverage"]) == set(core.SOURCES), "indexed coverage source set")
        for value in item["coverage"].values():
            core.require(type(value) is int and value >= 0 and (ids is None or value <= len(ids)), "indexed coverage count")
        for eid in item["event_ids"]:
            core.require(bool(EVENT.fullmatch(eid)) and eid in known_events, "indexed event reference")
    return {"snapshots": len(snapshots), "unique_events": len(known_events)}


def index_add_batch(core, index: dict, batch: dict, blob_sha: str) -> dict:
    result = json.loads(json.dumps(index, ensure_ascii=False))
    summary = summarize_batch(core, batch)
    path = core.snapshot_path(batch)
    existing = next((x for x in result["snapshots"] if x["run_id"] == batch["run_id"]), None)
    if existing is not None:
        core.require(existing["path"] == path and existing["blob_sha"] == blob_sha, "run ID reused with different content")
        return result
    known_events = set(result["events"])
    for event in batch["events"]:
        core.require(event["event_id"] not in known_events, "event already exists in validated history")
        result["events"].append(event["event_id"])
        known_events.add(event["event_id"])
    result["events"].sort()
    result["snapshots"].append({"path": path, "blob_sha": blob_sha, **summary})
    result["snapshots"].sort(key=lambda x: (x["observed_at"], x["run_id"]))
    return result


def _index_observations(index: dict) -> list[dict]:
    rows = []
    for snap in index["snapshots"]:
        for rid, observed_at, stars in snap["stars"]:
            rows.append({"repository_id": rid, "metadata": {"status": "ok", "observed_at": observed_at, "value": {"stars": stars}}})
    return rows


def render_index(core, registry: dict, index: dict) -> str:
    core.require(bool(index["snapshots"]), "no indexed snapshots")
    latest = max(index["snapshots"], key=lambda x: x["observed_at"])
    observations = _index_observations(index)
    latest_ids = {row[0] for row in latest["stars"]}
    rows = ["# 当前观测", "", f"本轮：`{latest['run_id']}`；观测时间（UTC）：{latest['observed_at']}。", "", "这是观测表，不是技术质量排名。— 表示没有可比较基线；stale 表示本轮未取得新数值。", "", "| 项目 | 类别 | Stars | 7 日净变化 | 30 日净变化 | 新鲜度 |", "| --- | --- | ---: | ---: | ---: | --- |"]
    for p in sorted(registry["projects"], key=lambda p: (p["kind"], p["full_name"].lower())):
        if p["status"] not in ("tracked", "reference", "watchlist"):
            continue
        rid = p["repository_id"]
        good = [o for o in observations if o["repository_id"] == rid]
        if not good:
            continue
        current = max(good, key=lambda o: o["metadata"]["observed_at"])
        fresh = rid in latest_ids
        metrics = [core.growth(observations, rid, d) if fresh else None for d in (7, 30)]
        values = [str(m["net_stars"]) if m else "—" for m in metrics]
        name = html.escape(p["full_name"]).replace("|", "&#124;")
        rows.append(f"| [{name}](../{p['card']}) | {p['kind']} | {current['metadata']['value']['stars']} | {values[0]} | {values[1]} | {'fresh' if fresh else 'stale'} |")
    rows += ["", "增长的实际区间由 `growth()` 返回；基线容差为 6 小时，不把观察期外推成完整一周。", "", "## 本轮来源覆盖", ""]
    for source in core.SOURCES:
        rows.append(f"- {source}: {latest['coverage'][source]}/{len(registry['projects'])}")
    rows += ["", "来源未采集不代表没有发布或没有变更。项目卡片的机制说明均需查看其证据等级。", ""]
    return "\n".join(rows)


def _verify_bytes(core, path: str, content: bytes, blobs: dict[str, dict]) -> None:
    core.require(path in blobs, "required manifest file missing: " + path)
    entry = blobs[path]
    core.require(len(content) == entry["size"], "manifest byte size mismatch: " + path)
    core.require(git_blob_sha_bytes(content) == entry["sha"], "manifest blob mismatch: " + path)


def _overlay_changed(core, root: Path, blobs: dict[str, dict], paths: list[str]) -> dict[str, dict]:
    result = {k: dict(v) for k, v in blobs.items()}
    core.guard_paths(paths)
    for path in paths:
        file = root / path
        core.require(file.is_file(), "changed file not materialized: " + path)
        content = file.read_bytes()
        result[path] = {"path": path, "mode": "100644", "type": "blob", "sha": git_blob_sha_bytes(content), "size": len(content)}
    return result


def validate_manifest_state(core, manifest: dict, index: dict, config: dict, registry: dict, readme: bytes, config_bytes: bytes, registry_bytes: bytes, index_bytes: bytes, blobs: dict[str, dict] | None = None) -> dict:
    base_blobs = validate_tree_manifest(core, manifest)
    effective = blobs if blobs is not None else base_blobs
    core.require(config["repository"] == core.TARGET and config["approval_state"] == "approved", "repository/approval gate")
    ids = core.validate_registry(registry)
    _verify_bytes(core, "config/tracker.json", config_bytes, effective)
    _verify_bytes(core, "data/projects.json", registry_bytes, effective)
    _verify_bytes(core, "README.md", readme, effective)
    _verify_bytes(core, "state/validation-index.json", index_bytes, effective)
    core.require(len(readme.decode("utf-8").splitlines()) <= config["settings"]["readme_max_lines"], "README too long")
    for p in registry["projects"]:
        if p["status"] in ("tracked", "reference"):
            core.require(p["card"] in effective, "missing project card: " + p["card"])
    stats = validate_index(core, index, ids)
    snapshot_paths = {p for p in effective if SNAPSHOT.fullmatch(p)}
    indexed_paths = {x["path"] for x in index["snapshots"]}
    core.require(snapshot_paths == indexed_paths, "validation index snapshot set does not match tree")
    for item in index["snapshots"]:
        core.require(effective[item["path"]]["sha"] == item["blob_sha"], "validation index snapshot blob mismatch: " + item["path"])
    effective_root, _ = _compute_tree(core, effective)
    return {"status": "passed", "snapshots": stats["snapshots"], "projects": len(ids), "unique_events": stats["unique_events"], "effective_tree_sha": effective_root}


def validate_batch_file(core, batch_path: Path, registry_path: Path) -> dict:
    registry = core.load(registry_path)
    ids = core.validate_registry(registry)
    batch = core.load(batch_path)
    core.validate_batch(batch, ids)
    return {"status": "passed", "run_id": batch["run_id"], "projects": len(ids), "observations": len(batch["observations"]), "events": len(batch["events"])}


def validate_manifest_files(core, root: Path, manifest_path: Path, index_path: Path, config_path: Path, registry_path: Path, readme_path: Path, changed_file_list: Path | None = None) -> dict:
    manifest = core.load(manifest_path)
    base_blobs = validate_tree_manifest(core, manifest)
    paths = core.load(changed_file_list) if changed_file_list else []
    effective = _overlay_changed(core, root, base_blobs, paths) if paths else base_blobs
    index_bytes = index_path.read_bytes(); config_bytes = config_path.read_bytes(); registry_bytes = registry_path.read_bytes(); readme = readme_path.read_bytes()
    result = validate_manifest_state(core, manifest, json.loads(index_bytes), json.loads(config_bytes), json.loads(registry_bytes), readme, config_bytes, registry_bytes, index_bytes, effective)
    result["changed_paths"] = paths
    return result


def prepare_manifest(core, root: Path, batch: dict, manifest_path: Path, index_path: Path, config_path: Path, registry_path: Path, readme_path: Path) -> dict:
    manifest = core.load(manifest_path)
    index_bytes = index_path.read_bytes(); config_bytes = config_path.read_bytes(); registry_bytes = registry_path.read_bytes(); readme = readme_path.read_bytes()
    index = json.loads(index_bytes); config = json.loads(config_bytes); registry = json.loads(registry_bytes)
    base_blobs = validate_tree_manifest(core, manifest)
    validate_manifest_state(core, manifest, index, config, registry, readme, config_bytes, registry_bytes, index_bytes, base_blobs)
    core.require(config["approval_state"] == "approved", "not approved")
    if batch["run_type"] == "scheduled":
        core.require(config["automation_enabled"] and config["implementation_ready"], "scheduled gate closed")
    ids = core.validate_registry(registry)
    core.validate_batch(batch, ids)
    snapshot_bytes = core.encoded(batch).encode("utf-8")
    snapshot_sha = git_blob_sha_bytes(snapshot_bytes)
    existing = next((x for x in index["snapshots"] if x["run_id"] == batch["run_id"]), None)
    if existing is not None:
        core.require(existing["blob_sha"] == snapshot_sha and existing["path"] == core.snapshot_path(batch), "run ID reused with different content")
        return {"status": "duplicate", "paths": []}
    new_index = index_add_batch(core, index, batch, snapshot_sha)
    path = core.snapshot_path(batch)
    paths = [path, "reports/current.md", "state/validation-index.json"]
    core.guard_paths(paths)
    core.save(root / path, batch)
    (root / "reports").mkdir(parents=True, exist_ok=True)
    (root / "reports/current.md").write_text(render_index(core, registry, new_index), encoding="utf-8")
    core.save(root / "state/validation-index.json", new_index)
    effective = _overlay_changed(core, root, base_blobs, paths)
    planned_index_bytes = (root / "state/validation-index.json").read_bytes()
    validation = validate_manifest_state(core, manifest, new_index, config, registry, readme, config_bytes, registry_bytes, planned_index_bytes, effective)
    first = min(x["observed_at"] for x in new_index["snapshots"])
    due = [w for w in core.closed_weeks(first, batch["observed_at"]) if f"reports/weekly/{w}.md" not in effective]
    return {"status": "prepared", "paths": paths, "weekly_reports_due": due, "validation": validation}


def _apply_receipt_state(core, state: dict, batch: dict, commit: str) -> dict:
    for obs in batch["observations"]:
        slot = state["sources"].setdefault(str(obs["repository_id"]), {})
        for name in core.SOURCES:
            source = obs[name]
            previous = slot.get(name, {})
            if source["observed_at"] < previous.get("last_attempt_at", ""):
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
        state["latest_snapshot_path"] = core.snapshot_path(batch)
        state["last_verified_observed_at"] = batch["observed_at"]
    return state


def receipt_manifest(core, root: Path, batch: dict, commit: str, readback_commit: str, manifest_path: Path, index_path: Path, config_path: Path, registry_path: Path, readme_path: Path, checkpoints_path: Path) -> dict:
    core.require(bool(core.SHA.fullmatch(commit)) and commit == readback_commit, "unverified publication")
    manifest = core.load(manifest_path)
    core.require(manifest["base_commit_sha"] == commit, "published manifest commit mismatch")
    index_bytes = index_path.read_bytes(); config_bytes = config_path.read_bytes(); registry_bytes = registry_path.read_bytes(); readme = readme_path.read_bytes()
    index = json.loads(index_bytes); config = json.loads(config_bytes); registry = json.loads(registry_bytes)
    blobs = validate_tree_manifest(core, manifest)
    validate_manifest_state(core, manifest, index, config, registry, readme, config_bytes, registry_bytes, index_bytes, blobs)
    expected_sha = git_blob_sha_bytes(core.encoded(batch).encode("utf-8"))
    item = next((x for x in index["snapshots"] if x["run_id"] == batch["run_id"]), None)
    core.require(item is not None and item["path"] == core.snapshot_path(batch) and item["blob_sha"] == expected_sha, "snapshot not reconciled")
    checkpoint_bytes = checkpoints_path.read_bytes()
    _verify_bytes(core, "state/checkpoints.json", checkpoint_bytes, blobs)
    state = _apply_receipt_state(core, json.loads(checkpoint_bytes), batch, commit)
    core.save(root / "state/checkpoints.json", state)
    return state
