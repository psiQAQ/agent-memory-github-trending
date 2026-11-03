"""Synthetic local Git fixtures. No network, credential, scheduler or upstream code."""
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
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

    def recovery_evidence(self, **changes):
        evidence = {"schema_version": "1.0", "run_id": self.run_id,
                    "lock_sha256": hashlib.sha256(local.lock_path(self.root).read_bytes()).hexdigest(),
                    "checked_at": "2026-09-17T00:01:00Z", "original_writer_stopped": True,
                    "single_writer_confirmed": True, "writes_reconciled": True,
                    "remote_head_sha": self.base, "local_head_sha": self.base,
                    "next_phase": "data-write", "source_refs": ["synthetic test receipt"]}
        evidence.update(changes)
        path = self.root / ".cache/recovery-evidence.json"
        self.save(".cache/recovery-evidence.json", evidence)
        return path

    def test_lock_status_redacts_token_and_never_infers_liveness(self):
        owner = local.acquire(self.root, self.run_id)
        before = local.lock_path(self.root).read_bytes()
        status = local.lock_status(self.root)
        self.assertEqual(status["run_id"], self.run_id)
        self.assertEqual(status["writer_state"], "unknown")
        self.assertNotIn(owner["owner_token"], json.dumps(status))
        self.assertEqual(local.lock_path(self.root).read_bytes(), before)

    def test_lock_status_handles_absent_empty_and_invalid_records(self):
        self.assertEqual(local.lock_status(self.root)["state"], "unlocked")
        path = local.lock_path(self.root)
        path.parent.mkdir()
        for raw in (b"", b"[]", b'{"run_id":"../outside"}', b"\xff"):
            path.write_bytes(raw)
            self.assertEqual(local.lock_status(self.root)["state"], "invalid_lock")
            self.assertEqual(path.read_bytes(), raw)

    def test_existing_lock_error_names_original_run_and_recovery_action(self):
        local.acquire(self.root, self.run_id)
        with self.assertRaisesRegex(FileExistsError, self.run_id + ".*lock-status"):
            local.acquire(self.root, "20260918T000000Z-another")

    def test_resume_accepts_legacy_lock_rotates_token_and_fences_old_release(self):
        owner = local.acquire(self.root, self.run_id)
        legacy = {key: owner[key] for key in ("run_id", "owner_token", "host", "acquired_at")}
        self.save(".cache/local-maintenance.lock", legacy)
        evidence = self.recovery_evidence()
        resumed = local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        self.assertNotEqual(resumed["owner_token"], owner["owner_token"])
        self.assertEqual(resumed["acquired_at"], owner["acquired_at"])
        self.assertEqual(resumed["recovery"]["verification"], "caller_confirmed_not_independently_authenticated")
        with self.assertRaisesRegex(ValueError, "ownership mismatch"):
            local.release(self.root, self.run_id, owner["owner_token"])
        local.release(self.root, self.run_id, resumed["owner_token"])

    def test_resume_rejects_unknown_confirmation_without_mutating_lock(self):
        owner = local.acquire(self.root, self.run_id)
        before = local.lock_path(self.root).read_bytes()
        for key in ("original_writer_stopped", "single_writer_confirmed", "writes_reconciled"):
            evidence = self.recovery_evidence(**{key: None})
            with self.assertRaisesRegex(ValueError, "confirmation missing"):
                local.resume(self.root, self.run_id, owner["owner_token"], evidence)
            self.assertEqual(local.lock_path(self.root).read_bytes(), before)

    def test_resume_rejects_wrong_owner_stale_lock_and_changed_head(self):
        owner = local.acquire(self.root, self.run_id)
        evidence = self.recovery_evidence()
        with self.assertRaisesRegex(ValueError, "ownership mismatch"):
            local.resume(self.root, self.run_id, "wrong", evidence)
        evidence = self.recovery_evidence(lock_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "lock changed"):
            local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        evidence = self.recovery_evidence(local_head_sha="a" * 40)
        with self.assertRaisesRegex(ValueError, "local HEAD changed"):
            local.resume(self.root, self.run_id, owner["owner_token"], evidence)

    def test_resume_rejects_missing_refs_wrong_run_and_external_evidence(self):
        owner = local.acquire(self.root, self.run_id)
        for changes in ({"source_refs": []}, {"run_id": "20260918T000000Z-other"}):
            evidence = self.recovery_evidence(**changes)
            with self.assertRaises(ValueError):
                local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        self.save("outside.json", {})
        with self.assertRaisesRegex(ValueError, "ignored .cache"):
            local.resume(self.root, self.run_id, owner["owner_token"], self.root / "outside.json")

    def test_atomic_replacement_failure_preserves_original_lock(self):
        owner = local.acquire(self.root, self.run_id)
        evidence = self.recovery_evidence()
        before = local.lock_path(self.root).read_bytes()
        with patch.object(local.os, "replace", side_effect=OSError("synthetic replacement failure")):
            with self.assertRaises(OSError):
                local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        self.assertEqual(local.lock_path(self.root).read_bytes(), before)
        self.assertFalse(list((self.root / ".cache").glob("local-maintenance.lock.*")))

    def test_resume_rejects_malformed_time_and_lock_without_deleting_them(self):
        owner = local.acquire(self.root, self.run_id)
        for checked_at in (None, "not-a-time"):
            evidence = self.recovery_evidence(checked_at=checked_at)
            with self.assertRaises(ValueError):
                local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        evidence = self.recovery_evidence()
        local.lock_path(self.root).write_bytes(b"[]")
        with self.assertRaisesRegex(ValueError, "invalid lock"):
            local.resume(self.root, self.run_id, owner["owner_token"], evidence)
        with self.assertRaisesRegex(ValueError, "invalid lock"):
            local.release(self.root, self.run_id, owner["owner_token"])
        self.assertEqual(local.lock_path(self.root).read_bytes(), b"[]")

    def test_guard_blocks_overlapping_mutations(self):
        with local.lock_mutation(self.root):
            with self.assertRaises(OSError):
                local.acquire(self.root, self.run_id)
        self.assertFalse(local.lock_path(self.root).exists())
        local.acquire(self.root, self.run_id)

    def test_guard_is_released_by_os_after_crash(self):
        script = ("import os,sys;from pathlib import Path;"
                  f"sys.path.insert(0,{str(Path(local.__file__).parent)!r});"
                  "import local_maintenance as local;"
                  f"guard=local.lock_mutation(Path({str(self.root)!r}));"
                  "guard.__enter__();os._exit(0)")
        subprocess.run([sys.executable, "-B", "-c", script], check=True)
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
