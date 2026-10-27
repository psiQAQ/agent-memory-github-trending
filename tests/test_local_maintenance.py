"""Synthetic local Git fixtures. No network, credential, scheduler or upstream code."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_manifest_validation import batch, config, registry
import local_maintenance as local
import manifest_validation as m
import tracker as t


class LocalMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run_id = "20260917T000000Z-local-test"
        self.g("init", "-b", "main")
        self.g("remote", "add", "origin", "git@github.com:psiQAQ/agent-memory-github-trending.git")
        self.b1 = batch()
        snap = t.snapshot_path(self.b1)
        encoded = t.encoded(self.b1).encode("utf-8")
        self.index = m.index_add_batch(t, m.empty_index(t), self.b1, m.git_blob_sha_bytes(encoded))
        for path in local.REQUIRED:
            self.write(path, b"{}\n")
        self.write(".gitignore", b".cache/\n")
        self.write("README.md", b"# fixture\n")
        self.write("projects/test.md", b"# fixture\n")
        self.save("config/tracker.json", config())
        self.save("data/projects.json", registry())
        self.save("state/validation-index.json", self.index)
        self.save("config/local-runtime.json", {"repository": t.TARGET, "runtime_mode": "local_git", "cutover_state": "prepared"})
        self.write(snap, encoded)
        self.base = self.commit()

    def tearDown(self):
        self.temp.cleanup()

    def g(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, check=True)
        return result.stdout.decode().strip()

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def save(self, path, data):
        self.write(path, t.encoded(data).encode("utf-8"))

    def commit(self):
        self.g("add", ".")  # Synthetic fixture only; production uses explicit paths.
        self.g("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
               "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "commit", "-m", "synthetic fixture")
        return self.g("rev-parse", "HEAD")

    def make_data(self):
        b2 = batch("2026-09-17T00:00:00Z", self.run_id, 11)
        b2["base_commit_sha"] = self.base
        encoded = t.encoded(b2).encode("utf-8")
        self.write(t.snapshot_path(b2), encoded)
        self.save("state/validation-index.json", m.index_add_batch(t, self.index, b2, m.git_blob_sha_bytes(encoded)))
        return self.commit()

    def test_complete_git_tree_and_index(self):
        result, _, _ = local.inspect(self.root, self.base)
        self.assertEqual(result["snapshots"], 1)
        self.assertEqual(result["tree_sha"], self.g("rev-parse", self.base + "^{tree}"))
        self.assertFalse(result["remote_readback_verified"])

    def test_pinned_raw_bytes_ignore_crlf_worktree(self):
        self.write("README.md", b"# fixture\r\n")
        self.assertEqual(local.inspect(self.root, self.base)[0]["status"], "passed")

    def test_preflight_clean_checkout(self):
        self.assertEqual(local.preflight(self.root, self.base)["status"], "passed")

    def test_dirty_worktree_stops(self):
        self.write("manual.txt", b"preserve me\n")
        with self.assertRaisesRegex(ValueError, "dirty worktree"):
            local.preflight(self.root, self.base)
        self.assertEqual((self.root / "manual.txt").read_bytes(), b"preserve me\n")

    def test_remote_movement_stops(self):
        with self.assertRaisesRegex(ValueError, "HEAD mismatch"):
            local.preflight(self.root, "f" * 40)

    def test_other_push_remote_stops(self):
        self.g("remote", "set-url", "--push", "origin", "git@github.com:other/repo.git")
        with self.assertRaisesRegex(ValueError, "push origin"):
            local.preflight(self.root, self.base)

    def test_prepared_profile_cannot_activate_itself(self):
        with self.assertRaisesRegex(ValueError, "not active"):
            local.preflight(self.root, self.base, active=True)

    def test_missing_policy_stops(self):
        (self.root / "docs/run-provenance.md").unlink()
        self.commit()
        with self.assertRaisesRegex(ValueError, "required file missing"):
            local.inspect(self.root)

    def test_snapshot_index_mismatch_stops(self):
        self.write(t.snapshot_path(self.b1), t.encoded(batch(stars=12)).encode())
        self.commit()
        with self.assertRaisesRegex(ValueError, "snapshot blob mismatch"):
            local.inspect(self.root)

    def test_summary_tampering_stops(self):
        self.index["snapshots"][0]["stars"][0][2] = 999
        self.save("state/validation-index.json", self.index)
        self.commit()
        with self.assertRaisesRegex(ValueError, "summary mismatch"):
            local.inspect(self.root)

    def test_atomic_lock_and_ownership(self):
        owner = local.acquire(self.root, self.run_id)
        with self.assertRaises(FileExistsError):
            local.acquire(self.root, self.run_id)
        with self.assertRaisesRegex(ValueError, "ownership mismatch"):
            local.release(self.root, self.run_id, "wrong")
        self.assertTrue(local.lock_path(self.root).exists())
        local.release(self.root, self.run_id, owner["owner_token"])
        self.assertFalse(local.lock_path(self.root).exists())

    def test_empty_interrupted_lock_is_not_replaced(self):
        path = local.lock_path(self.root)
        path.parent.mkdir()
        path.write_bytes(b"")
        with self.assertRaises(FileExistsError):
            local.acquire(self.root, self.run_id)

    def test_data_commit_plan(self):
        commit = self.make_data()
        result = local.publication_plan(self.root, commit, "data", self.run_id)
        self.assertEqual(result["parent_sha"], self.base)
        self.assertEqual(len(result["changed_blobs"]), 2)
        self.assertIn("not_remote_readback", result["scope"])

    def test_wrong_batch_base_stops(self):
        self.base = "b" * 40
        commit = self.make_data()
        with self.assertRaisesRegex(ValueError, "batch base"):
            local.publication_plan(self.root, commit, "data", self.run_id)

    def test_missing_brief_archive_stops(self):
        self.write("reports/latest.md", b"new brief\n")
        commit = self.make_data()
        with self.assertRaisesRegex(ValueError, "archive missing"):
            local.publication_plan(self.root, commit, "data", self.run_id)

    def test_policy_write_in_routine_data_stops(self):
        self.write("AGENTS.md", b"unexpected policy change\n")
        commit = self.make_data()
        with self.assertRaisesRegex(ValueError, "outside scope"):
            local.publication_plan(self.root, commit, "data", self.run_id)

    def test_old_snapshot_replacement_stops(self):
        changed = batch(stars=99)
        encoded = t.encoded(changed).encode()
        self.write(t.snapshot_path(changed), encoded)
        self.index = m.index_add_batch(t, m.empty_index(t), changed, m.git_blob_sha_bytes(encoded))
        commit = self.make_data()
        with self.assertRaisesRegex(ValueError, "immutable history"):
            local.publication_plan(self.root, commit, "data", self.run_id)

    def test_new_receipt_requires_metrics_and_separate_commit(self):
        data_sha = self.make_data()
        self.save("state/checkpoints.json", {"last_verified_data_commit_sha": data_sha})
        self.save("state/status.json", {"local_mode": True})
        receipt_sha = self.commit()
        with self.assertRaisesRegex(ValueError, "missing checkpoints/status/metrics"):
            local.publication_plan(self.root, receipt_sha, "receipt", self.run_id)

    def test_json_save_is_byte_stable_on_windows(self):
        value = {"text": "中文\nfixture"}
        target = self.root / ".cache/bytes.json"
        t.save(target, value)
        self.assertEqual(target.read_bytes(), t.encoded(value).encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
