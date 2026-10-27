"""Local Git inspection and single-writer guard. No network, scheduler or publishing.

This helper reads immutable Git objects, not line-ending-transformed worktree bytes.
Passing it never proves a remote push/readback, trigger origin or source coverage.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

import manifest_validation as manifest_mode
import tracker as core

REQUIRED = (
    "AGENTS.md", "config/tracker.json", "docs/maintenance.md",
    "docs/api-native-maintenance.md", "docs/segmented-execution.md",
    "docs/methodology.md", "docs/project-preferences.md", "docs/data-contract.md",
    "docs/references.md", "docs/run-provenance.md", "state/status.json",
    "state/checkpoints.json", "state/validation-index.json", "data/projects.json",
    "data/candidates.json", "config/queries.json", "README.md",
)
ORIGINS = {
    "git@github.com:psiQAQ/agent-memory-github-trending.git",
    "https://github.com/psiQAQ/agent-memory-github-trending.git",
    "https://github.com/psiQAQ/agent-memory-github-trending",
}
IMMUTABLE = ("data/snapshots/", "state/run-metrics/", "state/run-evidence/", "reports/briefs/")


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if result.returncode:
        raise ValueError("git " + args[0] + " failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def pin(root: Path, revision: str) -> str:
    core.require(revision == "HEAD" or bool(core.SHA.fullmatch(revision)), "use HEAD or a full commit SHA")
    return git(root, "rev-parse", "--verify", revision + "^{commit}").decode().strip()


def manifest(root: Path, commit: str) -> dict:
    commit = pin(root, commit)
    entries = []
    for row in git(root, "ls-tree", "-r", "-t", "-l", "-z", "--full-tree", commit).split(b"\0"):
        if not row:
            continue
        header, path = row.split(b"\t", 1)
        mode, kind, sha, size = header.decode("ascii").split()
        entry = dict(path=path.decode("utf-8"), mode=mode, type=kind, sha=sha)
        if size != "-":
            entry["size"] = int(size)
        entries.append(entry)
    return dict(schema_version="1.0", repository=core.TARGET, base_commit_sha=commit,
                base_tree_sha=git(root, "rev-parse", commit + "^{tree}").decode().strip(),
                truncated=False, entry_count=len(entries), entries=entries)


def read_blob(root: Path, blobs: dict, path: str) -> bytes:
    core.require(path in blobs, "required file missing: " + path)
    content = git(root, "cat-file", "blob", blobs[path]["sha"])
    manifest_mode._verify_bytes(core, path, content, blobs)
    return content


def inspect(root: Path, revision: str = "HEAD") -> tuple[dict, dict, dict]:
    tree = manifest(root, revision)
    blobs = manifest_mode.validate_tree_manifest(core, tree)
    files = {p: read_blob(root, blobs, p) for p in REQUIRED}
    config = json.loads(files["config/tracker.json"])
    registry = json.loads(files["data/projects.json"])
    index = json.loads(files["state/validation-index.json"])
    result = manifest_mode.validate_manifest_state(
        core, tree, index, config, registry, files["README.md"],
        files["config/tracker.json"], files["data/projects.json"],
        files["state/validation-index.json"], blobs)
    ids = core.validate_registry(registry)
    # Verify the actual historical content as well as its indexed byte identity.
    for item in index["snapshots"]:
        batch = json.loads(read_blob(root, blobs, item["path"]))
        core.validate_batch(batch, ids)
        summary = manifest_mode.summarize_batch(core, batch)
        core.require(all(item[key] == value for key, value in summary.items()),
                     "indexed summary mismatch: " + item["path"])
    for key in ("implementation_ready", "automation_enabled"):
        core.require(config.get(key) is True, "closed tracker gate: " + key)
    result.update(commit_sha=tree["base_commit_sha"], tree_sha=tree["base_tree_sha"],
                  entry_count=len(tree["entries"]), scope="local_git_objects_only",
                  remote_readback_verified=False, scheduled_trigger_verified=False)
    return result, blobs, index


def preflight(root: Path, remote_head: str, active: bool = False) -> dict:
    core.require(bool(core.SHA.fullmatch(remote_head)), "fresh remote HEAD SHA required")
    core.require(git(root, "remote", "get-url", "origin").decode().strip() in ORIGINS, "unexpected origin")
    core.require(git(root, "remote", "get-url", "--push", "origin").decode().strip() in ORIGINS, "unexpected push origin")
    core.require(not git(root, "status", "--porcelain=v1", "--untracked-files=all"), "dirty worktree; preserve user work")
    core.require(git(root, "branch", "--show-current").decode().strip() == "main", "expected main checkout")
    result, blobs, _ = inspect(root)
    core.require(result["commit_sha"] == remote_head, "local/remote HEAD mismatch; reconcile first")
    if active:
        profile = json.loads(read_blob(root, blobs, "config/local-runtime.json"))
        config = json.loads(read_blob(root, blobs, "config/tracker.json"))
        core.require(profile.get("repository") == core.TARGET and profile.get("cutover_state") == "active", "local cutover not active")
        core.require(profile.get("runtime_mode") == "local_git" and config["settings"].get("runtime_mode") == "local_git", "local runtime not selected")
        for path in ("docs/local-maintenance.md", "docs/local-scheduled-task-prompt.md"):
            read_blob(root, blobs, path)
    result["remote_head_supplied"] = remote_head
    result["remote_head_provenance"] = "caller_must_retain_fresh_network_receipt"
    return result


def publication_plan(root: Path, revision: str, phase: str, run_id: str) -> dict:
    core.require(bool(core.RUN.fullmatch(run_id)), "invalid run ID")
    result, blobs, index = inspect(root, revision)
    commit = result["commit_sha"]
    parents = git(root, "rev-list", "--parents", "-n", "1", commit).decode().split()
    core.require(len(parents) == 2, "publication requires exactly one parent")
    parent = parents[1]
    _, old_blobs, old_index = inspect(root, parent)
    changed = {p for p in set(blobs) | set(old_blobs) if blobs.get(p) != old_blobs.get(p)}
    core.require(bool(changed), "empty publication")
    core.guard_paths(sorted(changed))
    for path in changed:
        core.require(path in blobs, "deletions are not routine publication: " + path)
        core.require(not (path in old_blobs and path.startswith(IMMUTABLE)), "immutable history changed: " + path)
    old_entries = {x["path"]: x for x in old_index["snapshots"]}
    new_entries = {x["path"]: x for x in index["snapshots"]}
    core.require(all(new_entries.get(p) == v for p, v in old_entries.items()), "historical index changed")
    if phase == "data":
        added = set(new_entries) - set(old_entries)
        core.require(len(added) == 1, "Data must append exactly one snapshot")
        entry = new_entries[next(iter(added))]
        core.require(entry["run_id"] == run_id, "Data run ID mismatch")
        batch = json.loads(read_blob(root, blobs, entry["path"]))
        core.require(batch["base_commit_sha"] == parent, "batch base is not Data parent")
        core.require(not (changed & {"state/checkpoints.json", "state/status.json"}), "Receipt state in Data commit")
        core.require(not any(p.startswith(("state/run-metrics/", "state/run-evidence/")) for p in changed), "Receipt evidence in Data commit")
        if "reports/latest.md" in changed:
            core.require("reports/briefs/" + run_id + ".md" in changed, "brief archive missing")
    else:
        core.require(phase == "receipt", "unknown publication phase")
        core.require(index == old_index, "Receipt changed snapshot index")
        snapshot = next((x for x in index["snapshots"] if x["run_id"] == run_id), None)
        core.require(snapshot is not None, "Receipt snapshot missing")
        at = core.stamp(snapshot["observed_at"])
        metric_path = f"state/run-metrics/{at:%Y/%m}/{run_id}.json"
        required = {"state/checkpoints.json", "state/status.json", metric_path}
        core.require(required <= changed, "Receipt missing checkpoints/status/metrics")
        prefix = f"state/run-evidence/{at:%Y/%m}/{run_id}/"
        core.require(all(p in required or p.startswith(prefix) for p in changed), "unexpected Receipt path")
    return dict(schema_version="1.0", phase=phase, run_id=run_id, commit_sha=commit,
                parent_sha=parent, tree_sha=result["tree_sha"],
                changed_blobs={p: blobs[p]["sha"] for p in sorted(changed)},
                scope="local_commit_plan_not_remote_readback")


def lock_path(root: Path) -> Path:
    return root.resolve() / ".cache" / "local-maintenance.lock"


def acquire(root: Path, run_id: str) -> dict:
    core.require(bool(core.RUN.fullmatch(run_id)), "invalid run ID")
    path = lock_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = dict(run_id=run_id, owner_token=uuid.uuid4().hex, host=socket.gethostname(),
                acquired_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    # Exclusive create is atomic. An interrupted/empty lock remains blocking.
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(core.encoded(data))
        stream.flush()
        os.fsync(stream.fileno())
    return data


def release(root: Path, run_id: str, owner_token: str) -> dict:
    path = lock_path(root)
    data = json.loads(path.read_text(encoding="utf-8"))
    core.require(data.get("run_id") == run_id and data.get("owner_token") == owner_token,
                 "lock ownership mismatch; reconcile before release")
    path.unlink()
    return {"released": True, "run_id": run_id}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("inspect", "preflight", "plan", "acquire", "release"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--remote-head")
    parser.add_argument("--active", action="store_true")
    parser.add_argument("--phase", choices=("data", "receipt"))
    parser.add_argument("--run-id")
    parser.add_argument("--owner-token")
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            result = inspect(args.root, args.commit)[0]
        elif args.command == "preflight":
            result = preflight(args.root, args.remote_head or "", args.active)
        elif args.command == "plan":
            result = publication_plan(args.root, args.commit, args.phase or "", args.run_id or "")
        elif args.command == "acquire":
            result = acquire(args.root, args.run_id or "")
        else:
            result = release(args.root, args.run_id or "", args.owner_token or "")
        print(core.encoded(result), end="")
    except (ValueError, KeyError, TypeError, OSError, UnicodeError) as exc:
        parser.exit(1, f"Local maintenance stopped: {exc}\n")


if __name__ == "__main__":
    main()
