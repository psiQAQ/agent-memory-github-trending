"""Synthetic manifest-mode fixtures only; no network or upstream code is executed."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tracker as t
import manifest_validation as m


def observation(at="2026-09-16T00:00:00Z", stars=10):
    base = {"repository_id": 1, "full_name": "test/memory"}
    for source in t.SOURCES:
        value = (
            {"stars": stars, "forks": 1, "archived": False, "default_branch": "main", "created_at": "2025-01-01T00:00:00Z", "pushed_at": at}
            if source == "metadata" else ("a" * 40 if source == "head" else [])
        )
        base[source] = {"status": "ok", "observed_at": at, "source_url": "https://api.github.com/repos/test/memory", "value": value}
    base["releases"]["complete"] = True
    return base


def batch(at="2026-09-16T00:00:00Z", run="20260916T000000Z-test", stars=10):
    return {
        "schema_version": "1.0", "run_id": run, "run_type": "interactive", "observed_at": at,
        "base_commit_sha": "a" * 40, "expected_repository_ids": [1], "observations": [observation(at, stars)],
        "events": [], "discovery": [],
    }


def registry():
    return {"schema_version": "1.0", "projects": [{
        "repository_id": 1, "full_name": "test/memory", "status": "tracked", "kind": "engineering",
        "first_discovered_at": "2026-09-16T00:00:00Z", "evidence_level": "upstream_statement",
        "source_url": "https://github.com/test/memory", "summary": "test",
        "implementation_evidence": "https://github.com/test/memory/tree/main", "card": "projects/test.md",
    }]}


def config():
    return {"repository": t.TARGET, "approval_state": "approved", "automation_enabled": True, "implementation_ready": True, "settings": {"readme_max_lines": 250}}


def manifest_for(files: dict[str, bytes], commit="c" * 40):
    blobs = {path: {"path": path, "mode": "100644", "type": "blob", "sha": m.git_blob_sha_bytes(content), "size": len(content)} for path, content in files.items()}
    root_sha, tree_shas = m._compute_tree(t, blobs)
    entries = [dict(v) for _, v in sorted(blobs.items())]
    entries.extend({"path": path, "mode": "040000", "type": "tree", "sha": sha} for path, sha in sorted(tree_shas.items()))
    entries.sort(key=lambda x: x["path"])
    return {"schema_version": "1.0", "repository": t.TARGET, "base_commit_sha": commit, "base_tree_sha": root_sha, "truncated": False, "entry_count": len(entries), "entries": entries}


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(t.encoded(value), encoding="utf-8")


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.inputs = self.base / "inputs"
        self.out = self.base / "out"
        self.inputs.mkdir(); self.out.mkdir()
        self.b1 = batch()
        snap_path = t.snapshot_path(self.b1)
        snap_bytes = t.encoded(self.b1).encode("utf-8")
        self.index = m.index_add_batch(t, m.empty_index(t), self.b1, m.git_blob_sha_bytes(snap_bytes))
        self.files = {
            "config/tracker.json": t.encoded(config()).encode("utf-8"),
            "data/projects.json": t.encoded(registry()).encode("utf-8"),
            "README.md": b"# test\n",
            "projects/test.md": b"# test\n",
            snap_path: snap_bytes,
            "state/validation-index.json": t.encoded(self.index).encode("utf-8"),
            "state/checkpoints.json": t.encoded({"schema_version": "1.0", "sources": {}}).encode("utf-8"),
        }
        self.manifest = manifest_for(self.files)
        write_json(self.inputs / "manifest.json", self.manifest)
        write_json(self.inputs / "config.json", config())
        write_json(self.inputs / "projects.json", registry())
        (self.inputs / "README.md").write_bytes(self.files["README.md"])
        write_json(self.inputs / "index.json", self.index)
        write_json(self.inputs / "checkpoints.json", {"schema_version": "1.0", "sources": {}})

    def tearDown(self): self.temp.cleanup()

    def test_manifest_tree_round_trip(self):
        blobs = m.validate_tree_manifest(t, self.manifest)
        self.assertIn("projects/test.md", blobs)

    def test_manifest_rejects_tampered_root(self):
        bad = copy.deepcopy(self.manifest); bad["base_tree_sha"] = "0" * 40
        with self.assertRaises(ValueError): m.validate_tree_manifest(t, bad)

    def test_manifest_rejects_truncated(self):
        bad = copy.deepcopy(self.manifest); bad["truncated"] = True
        with self.assertRaises(ValueError): m.validate_tree_manifest(t, bad)

    def test_manifest_rejects_unindexed_snapshot(self):
        bad_index = m.empty_index(t)
        files = dict(self.files); files["state/validation-index.json"] = t.encoded(bad_index).encode("utf-8")
        manifest = manifest_for(files)
        blobs = m.validate_tree_manifest(t, manifest)
        with self.assertRaises(ValueError):
            m.validate_manifest_state(t, manifest, bad_index, config(), registry(), files["README.md"], files["config/tracker.json"], files["data/projects.json"], files["state/validation-index.json"], blobs)

    def test_prepare_manifest_without_historical_worktree(self):
        b2 = batch("2026-09-16T12:00:00Z", "20260916T120000Z-test", 11)
        result = m.prepare_manifest(t, self.out, b2, self.inputs/"manifest.json", self.inputs/"index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md")
        self.assertEqual(result["status"], "prepared")
        self.assertFalse((self.out/"projects/test.md").exists())
        self.assertFalse((self.out/t.snapshot_path(self.b1)).exists())
        self.assertTrue((self.out/t.snapshot_path(b2)).is_file())
        changed = self.base/"changed.json"; write_json(changed, result["paths"])
        validated = m.validate_manifest_files(t, self.out, self.inputs/"manifest.json", self.out/"state/validation-index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md", changed)
        self.assertEqual(validated["snapshots"], 2)

    def test_prepare_manifest_idempotent(self):
        result = m.prepare_manifest(t, self.out, self.b1, self.inputs/"manifest.json", self.inputs/"index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md")
        self.assertEqual(result["status"], "duplicate")

    def test_receipt_manifest_without_snapshot_file(self):
        b2 = batch("2026-09-16T12:00:00Z", "20260916T120000Z-test", 11)
        result = m.prepare_manifest(t, self.out, b2, self.inputs/"manifest.json", self.inputs/"index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md")
        published = dict(self.files)
        for path in result["paths"]:
            published[path] = (self.out/path).read_bytes()
        pub_manifest = manifest_for(published, commit="d" * 40)
        write_json(self.inputs/"published-manifest.json", pub_manifest)
        write_json(self.inputs/"published-index.json", json.loads(published["state/validation-index.json"]))
        receipt_out = self.base/"receipt-out"; receipt_out.mkdir()
        state = m.receipt_manifest(t, receipt_out, b2, "d"*40, "d"*40, self.inputs/"published-manifest.json", self.inputs/"published-index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md", self.inputs/"checkpoints.json")
        self.assertEqual(state["last_completed_run_id"], b2["run_id"])
        self.assertFalse((receipt_out/t.snapshot_path(b2)).exists())
        self.assertTrue((receipt_out/"state/checkpoints.json").is_file())

    def test_manifest_changed_paths_must_be_materialized(self):
        changed = self.base/"changed.json"; write_json(changed, ["state/status.json"])
        with self.assertRaises(ValueError):
            m.validate_manifest_files(t, self.out, self.inputs/"manifest.json", self.inputs/"index.json", self.inputs/"config.json", self.inputs/"projects.json", self.inputs/"README.md", changed)


if __name__ == "__main__": unittest.main()
