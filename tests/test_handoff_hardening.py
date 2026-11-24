"""Offline regressions for failures observed during the owner/Agent handoff."""
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import test_owner_pipeline as fixtures
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import owner_pipeline as owner
import handoff_support as support
import staged_publication as publication
import webpage_checks

ROOT = Path(__file__).resolve().parents[1]


class HardeningTests(unittest.TestCase):
    setUp = fixtures.OwnerPipelineTests.setUp
    tearDown = fixtures.OwnerPipelineTests.tearDown
    capture = fixtures.OwnerPipelineTests.capture

    def git(self, root, *args):
        child = subprocess.Popen(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw, err = child.communicate()
        self.assertEqual(child.returncode, 0, err.decode("utf-8", "replace"))
        return raw.decode().strip()

    def repository(self):
        root = self.root / "中文 空格仓库"; root.mkdir()
        self.git(root, "init", "-b", "main")
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false")):
            self.git(root, "config", key, value)
        (root / ".gitignore").write_text(".cache/\n", encoding="utf-8")
        owner.save(root / "config/tracker.json", dict(repository=owner.REPO, approval_state="approved",
            implementation_ready=True, automation_enabled=True, settings=dict(runtime_mode="local_git")))
        owner.save(root / "config/local-runtime.json", dict(repository=owner.REPO, cutover_state="active", runtime_mode="local_git"))
        self.git(root, "add", "--", ".gitignore", "config")
        self.git(root, "commit", "-m", "old main without runner")
        old = self.git(root, "rev-parse", "HEAD")
        self.git(root, "remote", "add", "origin", "git@github.com:psiQAQ/agent-memory-github-trending.git")
        self.git(root, "switch", "-c", "engineering/fixture")
        for name in support.BUNDLE_FILES:
            target = root / "scripts" / name; target.parent.mkdir(exist_ok=True)
            target.write_bytes((ROOT / "scripts" / name).read_bytes())
        self.git(root, "add", "--", "scripts")
        self.git(root, "commit", "-m", "fixed runner")
        return root, old, self.git(root, "rev-parse", "HEAD")

    def test_git_shell_is_only_in_git_child_and_preserves_proxy(self):
        original = {**os.environ, "SHELL": "existing-powershell", "HTTPS_PROXY": "unchanged-proxy"}
        with patch.object(owner.os, "environ", original):
            env = owner.git_child_env()
            self.assertTrue(env["SHELL"].lower().endswith("bash.exe"))
            self.assertEqual(env["HTTPS_PROXY"], "unchanged-proxy")
            self.assertEqual(os.environ["SHELL"], "existing-powershell")
            child = unittest.mock.Mock(pid=123, returncode=0); child.communicate.return_value = (b"", b"")
            with patch.object(subprocess, "Popen", return_value=child) as launch, contextlib.redirect_stdout(io.StringIO()):
                owner.Transport(self.root, self.run).call("gh", ["api", "--include", "x"], "test")
            self.assertEqual(launch.call_args.kwargs["env"]["SHELL"], "existing-powershell")

    def test_real_checkout_removes_module_but_cached_source_identity_survives(self):
        root, old, new = self.repository()
        spec = importlib.util.spec_from_file_location("isolated_owner", root / "scripts/owner_pipeline.py")
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        t = module.Transport(root, root / ".cache/test")
        with contextlib.redirect_stdout(io.StringIO()):
            t.call("git", ["switch", "main"], "fixture-switch")
            self.assertFalse(Path(module.__file__).exists())
            t.call("git", ["merge", "--ff-only", new], "fixture-merge")
        self.assertEqual(self.git(root, "rev-parse", "HEAD"), new)
        self.assertEqual(len(t.rows), 2)

    def test_frozen_entry_real_cmd_check_survives_branch_switch(self):
        root, old, new = self.repository()
        run = root / ".cache" / self.run.name; run.mkdir(parents=True)
        entry = support.create_entry(owner, root, run, new, "owner_pipeline", "collect")
        self.git(root, "commit", "--allow-empty", "-m", "reviewed runner revision")
        revised = self.git(root, "rev-parse", "HEAD")
        revised_entry = support.create_entry(owner, root, run, revised, "owner_pipeline", "collect")
        self.assertNotEqual(revised_entry["entry"], entry["entry"])
        self.assertEqual(support.create_entry(owner, root, run, revised, "owner_pipeline", "collect"), revised_entry)
        self.assertEqual(support.create_entry(owner, root, run, new, "owner_pipeline", "collect"), entry)
        self.git(root, "switch", "main")
        self.assertFalse((root / "scripts/owner_pipeline.py").exists())
        bat = Path(entry["entry"]); raw = bat.read_bytes()
        self.assertTrue(raw.isascii() and raw.startswith(b"@echo off\r\nchcp 65001 >nul\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        for arg, expected in (("--check", 0), ("--check-exit", 7)):
            p = subprocess.Popen('cmd.exe /d /s /c ""'+str(bat)+'" '+arg+'"', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            self.assertEqual(p.returncode, expected, (p.pid, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")))
        p = subprocess.Popen('cmd.exe /d /s /c ""' + revised_entry["entry"] + '" --check"',
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.assertEqual(p.returncode, 0, err.decode("utf-8", "replace"))
        self.assertEqual(json.loads(out)["program_commit"], revised)
        self.assertEqual(self.git(root, "rev-parse", "HEAD"), old)
        self.assertFalse((root / ".cache/local-maintenance.lock").exists())
        module=bat.parent/"bundle/owner_pipeline.py";module.write_bytes(module.read_bytes()+b"\n# changed\n")
        p=subprocess.Popen('cmd.exe /d /s /c ""'+str(bat)+'" --check"',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=p.communicate()
        self.assertEqual(p.returncode,1)
        self.assertIn(b"SUMMARY:",err)
        self.assertTrue((bat.parent/"ENTRY-FAILED.json").exists())
        self.assertEqual(self.git(root,"rev-parse","HEAD"),old)

    def test_resume_requires_confirmations_original_failure_head_lock_and_all_bytes(self):
        owner.save(self.run / "owner-pipeline/FAILED.json", dict(error="local wrapper stopped before next call"))
        self.capture("returned", ["api", "--include", "test"])
        with patch.object(owner.local, "pin", return_value="a"*40), patch.object(owner.local, "lock_status", return_value=dict(state="unlocked")):
            support.resume_draft(owner, self.root, self.run, "collect")
            path = self.run / "owner-pipeline/resume-draft.json"
            with self.assertRaisesRegex(ValueError, "unconfirmed"):
                support.validate_resume(owner, self.root, self.run, "collect", path)
            value = owner.tracker.load(path)
            value.update(original_writer_stopped=True, single_writer_confirmed=True, writes_reconciled=True, source_refs=["actual process proof"])
            owner.save(path, value)
            support.validate_resume(owner, self.root, self.run, "collect", path)
            self.assertEqual(owner.Transport(self.root, self.run).call("gh", ["api", "--include", "test"], "metadata")["id"], "returned")
            (self.run / "results/returned.stdout").write_bytes(b"corrupted")
            with self.assertRaises(ValueError):
                support.validate_resume(owner, self.root, self.run, "collect", path)

    def test_resume_draft_cannot_authorize_failed_network_replay(self):
        owner.save(self.run / "owner-pipeline/FAILED.json", dict(error="denied"))
        row = self.capture("denied", ["api", "--include", "test"])
        row["exit_code"] = 1; owner.save(self.run / "results/denied.json", row)
        with patch.object(owner.local, "pin", return_value="a"*40), patch.object(owner.local, "lock_status", return_value=dict(state="unlocked")):
            with self.assertRaisesRegex(ValueError, "failed/uncertain"):
                support.resume_draft(owner, self.root, self.run, "collect")

    def review_failure(self, status):
        args = ["api", "--method", "GET", "--include", "repos/test/memory/pulls/2"]
        ident = "owner-" + hashlib.sha256(owner.tracker.encoded(["gh", args, "review-evidence"]).encode()).hexdigest()[:20]
        row = self.capture(ident, args, kind="review-evidence")
        raw = (f'HTTP/2.0 {status} Error\r\nX-GitHub-Request-Id: example\r\n\r\n'
               f'{{"message":"Not Found","status":"{status}"}}').encode()
        path = self.run / "results" / (ident + ".json")
        row.update(exit_code=1, stdout_bytes=len(raw), stdout_sha256=hashlib.sha256(raw).hexdigest())
        owner.save(path, row)
        path.with_suffix(".stdout").write_bytes(raw)
        stage = self.run / "owner-pipeline"
        owner.save(stage / "FAILED.json", dict(repository=owner.REPO, run_id=self.run.name, status="Failed",
            action="review-fetch", error="action failed; retained without retry: " + ident))
        owner.save(stage / "batch.json", dict(run_id=self.run.name, base_commit_sha="a" * 40,
            observations=[dict(repository_id=1, full_name="test/memory", metadata=dict(status="ok"))]))
        owner.save(stage / "fixed/data/projects.json", dict(schema_version="1.0", projects=[]))
        return row, path

    def test_review_404_requires_acknowledgment_and_never_replays_failed_pr(self):
        missing, path = self.review_failure(404)
        first_failure = (self.run / "owner-pipeline/FAILED.json").read_bytes()
        first_response = path.with_suffix(".stdout").read_bytes()
        self.capture("public-metadata", ["api", "--method", "GET", "--include", "repos/test/memory"],
                     payload=dict(id=1, full_name="test/memory", private=False))
        with patch.object(owner.local, "pin", return_value="a" * 40), patch.object(owner, "verify_package"):
            with self.assertRaisesRegex(ValueError, "failed/uncertain"):
                owner.Transport(self.root, self.run)
            draft = Path(support.resume_draft(owner, self.root, self.run, "review-fetch")["path"])
            value = owner.tracker.load(draft)
            self.assertEqual(value["review_not_found_id"], missing["id"])
            with self.assertRaisesRegex(ValueError, "unconfirmed"):
                support.validate_resume(owner, self.root, self.run, "review-fetch", draft)
            evidence = self.run / "agent-review/resume-evidence.json"
            value.update(original_writer_stopped=True, single_writer_confirmed=True,
                         writes_reconciled=True, source_refs=["fixture proof"])
            later = self.run / "owner-pipeline/failures/local-check.json"
            owner.save(later, dict(error="timestamp must be UTC ending Z"))
            owner.save(evidence, value)
            support.validate_resume(owner, self.root, self.run, "review-fetch", evidence)
            transport = owner.Transport(self.root, self.run, missing_review=missing)
            request = dict(repository_id=1, full_name="test/memory", endpoint=missing["args"][4])
            plan = dict(repository=owner.REPO, run_id=self.run.name, requests=[request])
            with patch.object(transport, "gh", wraps=transport.gh) as gh, \
                 patch.object(owner.subprocess, "Popen") as launch, contextlib.redirect_stdout(io.StringIO()):
                for endpoint in (missing["args"][4], missing["args"][4] + "/files?per_page=100&page=1"):
                    request["endpoint"] = endpoint
                    with self.assertRaisesRegex(ValueError, "cannot be requested again"):
                        owner.fetch_review(transport, plan)
                self.assertEqual(gh.call_count, 0)
                self.assertEqual(launch.call_count, 0)
            request["endpoint"] = "repos/test/memory/pulls/3"
            plan_path = self.run / "agent-review/review-requests.json"
            owner.save(plan_path, plan)
            owner.save(self.run / "owner-pipeline/SUMMARY.json", dict(run_id=self.run.name))
            child = unittest.mock.Mock(pid=123, returncode=0)
            child.communicate.return_value = (b'HTTP/2.0 200 OK\r\n\r\n{"number":3}', b"")
            argv = ["owner_pipeline.py", "review-fetch", "--root", str(self.root), "--run-id", self.run.name,
                    "--plan", str(plan_path), "--resume-evidence", str(evidence)]
            with patch.object(sys, "argv", argv), patch.object(owner, "gates"), patch.object(owner, "ordinary_user"), \
                 patch.object(owner.subprocess, "Popen", return_value=child) as launch, contextlib.redirect_stdout(io.StringIO()):
                owner.main()
                self.assertEqual(launch.call_count, 1)
                self.assertEqual(launch.call_args.args[0], ["gh", *missing["args"][:4], request["endpoint"]])
            self.assertEqual(owner.tracker.load(self.run / "owner-pipeline/review-recovery.json"), value)
            self.assertEqual(owner.local.lock_status(self.root)["state"], "unlocked")
            self.assertEqual(len(owner.retained(self.run)), 2)
            self.assertEqual((self.run / "owner-pipeline/FAILED.json").read_bytes(), first_failure)
            self.assertEqual(path.with_suffix(".stdout").read_bytes(), first_response)
            self.assertTrue(later.exists())
            later_call = self.capture("later-call", ["api", "--method", "GET", "--include", "repos/test/memory/pulls/4"])
            later_call["state"] = "uncertain"
            owner.save(self.run / "results/later-call.json", later_call)
            with self.assertRaisesRegex(ValueError, "failed/uncertain"):
                owner.retained(self.run)
            self.assertEqual(len(owner.retained(self.run, allow_unresolved=True)), 2)
            path.with_suffix(".stdout").write_bytes(first_response + b"changed")
            with self.assertRaisesRegex(ValueError, "response changed"):
                owner.retained(self.run)

    def test_review_authentication_failure_cannot_prepare_continuation(self):
        self.review_failure(403)
        with patch.object(owner.local, "pin", return_value="a" * 40):
            with self.assertRaisesRegex(ValueError, "failed/uncertain"):
                support.resume_draft(owner, self.root, self.run, "review-fetch")

    def test_later_resume_gets_new_null_confirmation_draft_without_replacing_first(self):
        owner.save(self.run/"owner-pipeline/FAILED.json",dict(error="first local failure"))
        with patch.object(owner.local,"pin",return_value="a"*40),patch.object(owner.local,"lock_status",return_value=dict(state="unlocked")):
            first=support.resume_draft(owner,self.root,self.run,"collect");raw=Path(first["path"]).read_bytes()
            same=support.resume_draft(owner,self.root,self.run,"collect")
            self.assertEqual(first["path"],same["path"])
            self.capture("next-returned",["api","--include","new-purpose"])
            later=support.resume_draft(owner,self.root,self.run,"collect")
        self.assertNotEqual(first["path"],later["path"])
        self.assertEqual(Path(first["path"]).read_bytes(),raw)
        self.assertIsNone(owner.tracker.load(Path(later["path"]))["writes_reconciled"])

    def test_collect_resume_reuses_fetch_merge_and_checks_remote_once(self):
        sha="a"*40; remote=("ref: refs/heads/main\tHEAD\n"+sha+"\tHEAD\n").encode()
        for number,(args,kind,raw) in enumerate((
            (["ls-remote","--symref","origin","HEAD"],"owner-bootstrap-head",remote),
            (["fetch","--no-tags","origin","main"],"owner-fetch",b""),
            (["merge","--ff-only","origin/main"],"owner-ff-only",b""))):
            ident="old"+str(number);p=self.run/"results"/(ident+".json")
            owner.save(p,dict(id=ident,tool="git",args=args,kind=kind,state="returned",exit_code=0,
                returned_at="2026-11-18T16:00:00Z",stdout_file=ident+".stdout",stdout_bytes=len(raw),stdout_sha256=hashlib.sha256(raw).hexdigest()))
            p.with_suffix(".stdout").write_bytes(raw)
        t=owner.Transport(self.root,self.run); child=unittest.mock.Mock(pid=123,returncode=0);child.communicate.return_value=(remote,b"")
        with patch.object(owner.local,"git",return_value=b""),patch.object(subprocess,"Popen",return_value=child) as launch, \
             patch.object(owner.local,"preflight",side_effect=ValueError("stop before frozen inputs")),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError,"frozen inputs"):owner.collect(t,None)
        self.assertEqual(launch.call_count,1)
        self.assertEqual(launch.call_args.args[0],["git","ls-remote","--symref","origin","HEAD"])

    def test_extract_metadata_only_and_annotated_tag_without_network(self):
        endpoints = ["repos/test/memory/contents/large.py?ref="+"a"*40, "repos/test/memory/git/ref/tags/v1"]
        self.capture("large", ["api","--method","GET","--include",endpoints[0]], "review-evidence",
                     dict(path="large.py",sha="b"*40,size=1276781,encoding="none",content=""))
        self.capture("tag", ["api","--method","GET","--include",endpoints[1]], "review-evidence",
                     dict(object=dict(type="tag",sha="c"*40)))
        plan=dict(repository=owner.REPO,run_id=self.run.name,requests=[dict(repository_id=1,full_name="test/memory",endpoint=e) for e in endpoints])
        with patch.object(subprocess,"Popen",side_effect=AssertionError("must not fetch or execute")):
            result=support.extract_review(owner,self.root,self.run,plan)
        catalog=owner.tracker.load(self.run/"agent-review/source-catalog.json")
        self.assertEqual(result["missing_bodies"],1)
        self.assertEqual(catalog[0]["body_status"],"missing")
        self.assertEqual(catalog[1]["resolution"],"unpeeled")
        self.assertFalse((self.run/"agent-review/extracted/blobs").exists())

    def test_extract_verifies_blob_bytes_and_marks_incomplete_pr_pages(self):
        raw=b"source bytes only; never execute";sha=owner.manifest.git_blob_sha_bytes(raw)
        objects=[("repos/test/memory/git/blobs/"+sha,dict(encoding="base64",size=len(raw),sha=sha,content=base64.b64encode(raw).decode())),
            ("repos/test/memory/pulls/1",dict(number=1,changed_files=2,merged_at=None,merge_commit_sha=None,head=dict(sha="a"*40))),
            ("repos/test/memory/pulls/1/files?per_page=100&page=1",[dict(filename="one.py")])]
        for n,(e,v) in enumerate(objects):self.capture("r"+str(n),["api","--method","GET","--include",e],"review-evidence",v)
        plan=dict(repository=owner.REPO,run_id=self.run.name,requests=[dict(repository_id=1,full_name="test/memory",endpoint=e) for e,v in objects])
        with patch.object(subprocess,"Popen",side_effect=AssertionError("offline only")):
            support.extract_review(owner,self.root,self.run,plan)
        catalog=owner.tracker.load(self.run/"agent-review/source-catalog.json")
        self.assertEqual((self.run/catalog[0]["body_file"]).read_bytes(),raw)
        self.assertFalse(catalog[1]["files_complete"])

    def test_status_table_check_rejects_correct_title_with_wrong_merge_state(self):
        brief="# Title\n\nSummary\nWho\nAction\n\n## 已确认合并/发布的变更\n\n| 项目 | 变化 | 状态 | 影响 |\n| --- | --- | --- | --- |\n| [Repo](https://example.invalid) | Changed | Merged only | Check tag |\n"
        raw=b"<h1>Title</h1><p>Summary</p><table><tr><td>Repo</td><td>Changed</td><td>Released</td><td>Check tag</td></tr></table>"
        with self.assertRaisesRegex(ValueError,"status row"):
            webpage_checks.check_bytes(owner.tracker,raw,brief,["Title","Summary"],"latest",self.run.name)
        result=webpage_checks.check_bytes(owner.tracker,raw.replace(b"Released",b"Merged only"),brief,["Title"],"latest",self.run.name)
        self.assertEqual(result["change_status_rows"],1)

    def test_offline_web_recheck_preserves_failure_and_never_retries_transport(self):
        stage=self.run/"owner-pipeline"
        owner.save(stage/"batch.json",{})
        for phase,sha in (("data","a"*40),("receipt","b"*40)):
            owner.save(stage/(phase+"-readback.json"),dict(status="passed",commit_sha=sha))
        brief="# Title\n\nSummary\nWho\nAction\n\n## 已确认合并/发布的变更\n\n| 项目 | 变化 | 状态 | 影响 |\n| --- | --- | --- | --- |\n| Repo | Changed | Merged | Check |\n\n"+self.run.name
        p=stage/"data-remote/reports/latest.md";p.parent.mkdir(parents=True);p.write_text(brief,encoding="utf-8")
        plan=dict(run_id=self.run.name,data_sha="a"*40,receipt_sha="b"*40,homepage=["Summary"],latest=["Summary"],archive=["Summary"])
        owner.save(self.run/"website.json",plan)
        raw=("<h1>Title</h1><p>Summary Who Action 已确认合并/发布的变更 "+self.run.name+"</p><table><tr><td>Repo</td><td>Changed</td><td>Merged</td><td>Check</td></tr></table>").encode()
        original={}
        for name,suffix in (("homepage",""),("latest","reports/latest.html"),("archive","reports/briefs/"+self.run.name+".html")):
            url="https://notes.psiqaq.cn/agent-memory-github-trending/"+suffix
            record=stage/("website-"+name+".json")
            owner.save(record,dict(status="Failed",url=url,actual_url=url,http_status=200,body_sha256=hashlib.sha256(raw).hexdigest(),error="old local assertion"))
            (stage/("website-"+name+".html")).write_bytes(raw);original[name]=record.read_bytes()
        with patch.object(publication,"urlopen",side_effect=AssertionError("no retry")),patch.object(owner,"Transport",side_effect=AssertionError("no API")):
            result=publication.recheck_web(self.root,self.run.name,self.run/"website.json")
        self.assertEqual(result["status"],"Passed")
        for name in original:self.assertEqual((stage/("website-"+name+".json")).read_bytes(),original[name])
        value=owner.tracker.load(stage/"website-homepage.json");value["actual_url"]+="wrong";owner.save(stage/"website-homepage.json",value)
        with self.assertRaises(ValueError):publication.recheck_web(self.root,self.run.name,self.run/"website.json")

    def test_completed_staged_cli_and_prepare_return_before_any_write(self):
        for command in ("prepare-data","prepare-receipt","commit","pages","recheck-web"):
            with patch.object(sys,"argv",["staged_publication.py",command,"--root",str(self.root),"--run-id",self.run.name]), \
                 patch.object(owner,"ordinary_user"),patch.object(owner,"gates"),patch.object(owner,"completed",return_value=True), \
                 patch.object(owner,"save",side_effect=AssertionError("completed batch must not mutate")), \
                 patch.object(subprocess,"Popen",side_effect=AssertionError("completed batch must not dispatch")),contextlib.redirect_stdout(io.StringIO()):
                publication.main()
        with patch.object(owner,"check"),patch.object(owner,"completed",return_value=True),patch.object(owner,"save",side_effect=AssertionError("no writes")):
            self.assertEqual(owner.prepare(self.root,self.run.name)["status"],"already_complete")


if __name__=="__main__":unittest.main()
