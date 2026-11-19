"""Offline owner-stage tests. Fixtures stay in the repository's ignored .cache."""
import copy
import base64
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import owner_pipeline as owner
import staged_publication as publication
import tracker

BASE = Path(__file__).resolve().parents[1] / ".cache/owner-pipeline-tests"


class OwnerPipelineTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=BASE)
        self.root = Path(self.temp.name)
        self.run = self.root / ".cache/20261118T155903Z-local"
        self.run.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def capture(self, ident, args, kind="metadata", payload=None, rid=1, headers=b""):
        raw = b"HTTP/2.0 200 OK\r\n" + headers + b"\r\n" + json.dumps({} if payload is None else payload).encode()
        p = self.run / "results" / (ident + ".json")
        row = dict(id=ident, tool="gh", args=args, kind=kind, repository_id=rid,
                   state="returned", exit_code=0, dispatch_at="2026-11-18T16:00:00Z",
                   returned_at="2026-11-18T16:00:01Z", stdout_file=ident + ".stdout",
                   stdout_bytes=len(raw), stdout_sha256=hashlib.sha256(raw).hexdigest())
        owner.save(p, row); p.with_suffix(".stdout").write_bytes(raw)
        return row

    def test_retained_success_reused_without_process(self):
        args = ["api", "--method", "GET", "--include", "repos/test/memory"]
        row = self.capture("original", args)
        t = owner.Transport(self.root, self.run)
        with patch.object(owner.subprocess, "Popen", side_effect=AssertionError("must not recollect")):
            self.assertEqual(t.gh("repos/test/memory", "metadata", 1), row)

    def test_retained_tamper_and_uncertain_stop(self):
        self.capture("old", ["api", "--include"])
        p = self.run / "results/old.stdout"; p.write_bytes(p.read_bytes() + b"x")
        with self.assertRaisesRegex(ValueError, "changed"):
            owner.retained(self.run)
        row = tracker.load(self.run / "results/old.json"); row["state"] = "started"
        owner.save(self.run / "results/old.json", row)
        with self.assertRaisesRegex(ValueError, "uncertain"):
            owner.retained(self.run)

    def test_existing_lock_never_auto_taken(self):
        lock = owner.local.acquire(self.root, self.run.name)
        with self.assertRaisesRegex(ValueError, "clearance"):
            owner.acquire(self.root, self.run, None)
        self.assertEqual(tracker.load(self.root / ".cache/local-maintenance.lock"), lock)

    def test_review_plan_rejects_arbitrary_actions_and_unpinned_files(self):
        plan = dict(repository=tracker.TARGET, run_id=self.run.name,
                    requests=[dict(repository_id=1, full_name="test/memory",
                                   endpoint="repos/test/memory/contents/src/memory.py?ref=" + "a" * 40)])
        owner.validate_review_plan(plan)
        for endpoint in ("repos/test/memory/issues", "repos/test/memory/contents/a?ref=main",
                         "repos/other/private/contents/a?ref=" + "a" * 40,
                         "repos/test/memory/contents/../secret?ref=" + "a" * 40):
            plan["requests"][0]["endpoint"] = endpoint
            with self.assertRaises(ValueError): owner.validate_review_plan(plan)

    def test_review_budget_and_private_repository(self):
        fixed = self.run / "owner-pipeline/fixed/data/projects.json"
        owner.save(fixed, dict(schema_version="1.0", projects=[]))
        t = owner.Transport(self.root, self.run)
        plan = dict(repository=tracker.TARGET, run_id=self.run.name,
                    requests=[dict(repository_id=1, full_name="test/memory", endpoint="repos/test/memory/pulls/1")])
        row = dict(id="private")
        with patch.object(t, "gh", return_value=row) as fetch, patch.object(t, "response", return_value=(False, dict(id=1, full_name="test/memory", private=True))):
            with self.assertRaisesRegex(ValueError, "public repository"):
                owner.fetch_review(t, plan)
            self.assertEqual(fetch.call_count, 1)

    def test_exact_request_call_records_failure_and_never_retries(self):
        t = owner.Transport(self.root, self.run)
        child = unittest.mock.Mock(pid=123, returncode=1)
        child.communicate.return_value = (b"", b"authentication denied")
        with patch.object(owner.subprocess, "Popen", return_value=child) as launch:
            for _ in range(2):
                with self.assertRaises(ValueError):
                    t.gh("repos/test/memory", "metadata", 1)
            self.assertEqual(launch.call_count, 1)
        self.assertEqual(len(list((self.run / "owner-pipeline").glob("pre-*.json"))), 1)
        self.assertEqual(len(list((self.run / "owner-pipeline").glob("post-*.json"))), 1)

    def test_package_requires_original_bytes(self):
        p = self.run / "owner-pipeline/plain.json"; owner.save(p, dict(a=1))
        self.source_package()
        packet = tracker.load(self.run / "owner-pipeline/SUMMARY.json")
        packet['artifacts']['owner-pipeline/plain.json']=hashlib.sha256(p.read_bytes()).hexdigest()
        owner.save(self.run / "owner-pipeline/SUMMARY.json",packet)
        with patch.object(owner.source_check,'verify'):
            self.assertEqual(owner.verify_package(self.root, self.run)["status"], "Passed")
            p.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed"):
                owner.verify_package(self.root, self.run)

    def source_package(self):
        from test_manifest_validation import batch, registry
        b=batch(run=self.run.name)
        owner.save(self.run/'owner-pipeline/batch.json',b)
        owner.save(self.run/'owner-pipeline/fixed/data/projects.json',registry())
        owner.save(self.run/'owner-pipeline/fixed/state/checkpoints.json',dict(sources={}))
        owner.save(self.run/'owner-pipeline/SUMMARY.json',dict(status='sources_ready_for_agent_review',repository=tracker.TARGET,
            run_id=self.run.name,base_commit_sha=b['base_commit_sha'],artifacts=owner.artifacts(self.run)))

    def test_completed_collection_reentry_cannot_use_network_or_lock(self):
        self.source_package()
        with patch.object(sys, "argv", ["owner_pipeline.py", "collect", "--root", str(self.root), "--run-id", self.run.name]), \
             patch.object(owner, "ordinary_user"), patch.object(owner, "gates"), \
             patch.object(owner, "acquire", side_effect=AssertionError("no acquire")), \
             patch.object(owner, "Transport", side_effect=AssertionError("no transport")), patch.object(owner.source_check,'verify'):
            owner.main()

    def test_correction_dedup_and_conflict(self):
        item = dict(type="brief_correction", correction_id="x", brief_text="fixed")
        self.assertEqual(publication.correction_items(dict(pending_work=[item, copy.deepcopy(item)])), [item])
        with self.assertRaises(ValueError):
            publication.correction_items(dict(pending_work=[item, dict(item, brief_text="conflict")]))

    def test_agent_review_cannot_exceed_preselection(self):
        review = dict(repository=tracker.TARGET, run_id=self.run.name, selected_change_reviews=[1],
                      completed_change_reviews=[2], candidate_reviews=0, agent_reviewed=True, pending_work=[])
        with self.assertRaises(ValueError): publication.check_review(review, self.run.name)

    def test_batch_real_page_projection_and_prior_overlap(self):
        from test_manifest_validation import registry
        fixed = self.run / "owner-pipeline/fixed"
        owner.save(fixed / "data/projects.json", registry())
        owner.save(fixed / "state/checkpoints.json", dict(sources={"1":dict(releases=dict(value=[dict(id=99)]))}))
        owner.save(self.run / "owner-pipeline/preparation.json", dict(prepared_at="2026-11-18T15:59:00Z"))
        args = lambda endpoint: ["api", "--method", "GET", "--include", endpoint]
        self.capture("meta", args("repos/test/memory"), payload=dict(id=1, private=False, full_name="test/memory",
            stargazers_count=12, forks_count=2, archived=False, default_branch="main", created_at="2025-01-01T00:00:00Z",
            pushed_at="2026-11-18T16:00:00Z", license=None))
        self.capture("head", args("repos/test/memory/git/ref/heads/main"), "head",
                     dict(ref="refs/heads/main", object=dict(type="commit", sha="a"*40)))
        release = lambda i: dict(id=i, tag_name="v"+str(i), draft=False,
            published_at="2026-11-18T12:00:00Z", html_url="https://github.com/test/memory/releases/tag/v"+str(i))
        self.capture("release1", args("repos/test/memory/releases?per_page=30&page=1"), "releases",
                     [release(i) for i in range(100,130)], headers=b'Link: <https://api.github.com/next>; rel="next"\r\n')
        self.capture("release2", args("repos/test/memory/releases?per_page=30&page=2"), "releases", [release(99)])
        b, pages = owner.build_batch(owner.Transport(self.root, self.run), fixed, "b"*40)
        self.assertTrue(b["observations"][0]["releases"]["complete"])
        self.assertEqual(b["observations"][0]["releases"]["pagination"]["stop_reason"], "prior_release_id_reached")
        self.assertEqual(pages["1"][1]["source_url"], "https://api.github.com/repos/test/memory/releases?per_page=30&page=2")
        self.assertEqual(b["trigger_evidence"]["verification_status"], "unverified")

    def test_remote_bad_bytes_never_create_readback_proof(self):
        t = owner.Transport(self.root, self.run)
        p = dict(phase="data", commit_sha="a"*40, parent_sha="b"*40, tree_sha="c"*40,
                 changed_blobs={"reports/latest.md":"d"*40})
        def response(row):
            endpoint = row["endpoint"]
            if "/commits/" in endpoint:
                return False, dict(sha=p["commit_sha"], tree=dict(sha=p["tree_sha"]), parents=[dict(sha=p["parent_sha"])])
            if "/trees/" in endpoint: return False, dict(sha=p["tree_sha"], truncated=False, tree=[])
            return False, dict(sha="d"*40, encoding="base64", content="eA==", size=1)
        with patch.object(t, "gh", side_effect=lambda e,k:dict(endpoint=e)), patch.object(t,"response",side_effect=response), \
             patch.object(owner.manifest,"validate_tree_manifest",return_value={
                 "reports/latest.md":dict(sha="d"*40),"state/validation-index.json":dict(sha="e"*40)}):
            with self.assertRaisesRegex(ValueError,"bytes differ"): owner.readback(t,p)
        self.assertFalse((self.run / "owner-pipeline/data-readback.json").exists())

    def test_synthetic_collection_data_and_receipt_roundtrip(self):
        from test_local_maintenance import LocalMaintenanceTests
        from test_manifest_validation import config
        fixture = LocalMaintenanceTests()
        with patch.object(tempfile, "tempdir", str(BASE)):
            fixture.setUp()
        try:
            root = fixture.root
            for key, value in (("user.name","Fixture"),("user.email","fixture@example.invalid"),
                               ("core.autocrlf","false"),("commit.gpgsign","false")):
                fixture.g("config",key,value)
            cfg = config(); cfg["settings"]["runtime_mode"] = "local_git"
            fixture.save("config/tracker.json",cfg)
            fixture.save("config/local-runtime.json",dict(repository=tracker.TARGET,runtime_mode="local_git",cutover_state="active"))
            fixture.write("docs/local-maintenance.md",b"# fixture\n")
            fixture.write("docs/local-scheduled-task-prompt.md",b"# fixture\n")
            fixture.save("state/checkpoints.json",dict(schema_version="1.0",sources={}))
            fixture.save("data/candidates.json",dict(schema_version="1.0",candidates=[]))
            fixture.save("state/status.json",dict(pending_work=[],completed_work=[],last_completed_run_id=fixture.b1["run_id"],coverage=dict(tracked=20,total_observation_pool=47)))
            fixture.save("config/queries.json",dict(channels=[dict(id="broad",template='"{keyword}" archived:false fork:false'),
                dict(id="new",template='"{keyword}" created:>={since_30d} archived:false fork:false')],rotate_keywords=["agent memory"],per_page=20))
            base = fixture.commit()
            rid="20260917T000000Z-local-test"; run=owner.run_dir(root,rid);run.mkdir(parents=True)
            owner.save(run/"owner-pipeline/preparation.json",dict(prepared_at="2026-09-17T00:00:00Z"))
            lock=owner.local.acquire(root,rid)
            real_popen = subprocess.Popen
            def fake_popen(argv, **kwargs):
                if argv[0]=="git":
                    if argv[1]=="ls-remote": raw=("ref: refs/heads/main\tHEAD\n"+base+"\tHEAD\n").encode()
                    elif argv[1] in ("fetch","merge"): raw=b""
                    else: return real_popen(argv,**kwargs)
                else:
                    endpoint=argv[5]
                    if "/git/commits/" in endpoint:
                        sha=endpoint.rsplit('/',1)[1];parent=fixture.g('show','-s','--format=%P',sha)
                        obj=dict(sha=sha,tree=dict(sha=fixture.g('rev-parse',sha+'^{tree}')),parents=[dict(sha=p) for p in parent.split()])
                    elif "/git/trees/" in endpoint:
                        head=fixture.g('rev-parse','HEAD');m=owner.local.manifest(root,head)
                        obj=dict(sha=m['base_tree_sha'],truncated=False,tree=m['entries'])
                    elif "/git/blobs/" in endpoint:
                        sha=endpoint.rsplit('/',1)[1];data=owner.local.git(root,'cat-file','blob',sha)
                        obj=dict(sha=sha,encoding='base64',content=base64.b64encode(data).decode(),size=len(data))
                    elif endpoint=='repos/test/memory/git/ref/heads/main':
                        obj=dict(ref='refs/heads/main',object=dict(type='commit',sha='b'*40))
                    elif endpoint.endswith('/ref/heads/main'):
                        obj=dict(object=dict(sha=fixture.g('rev-parse','HEAD')))
                    elif endpoint=='repos/test/memory':
                        obj=dict(id=1,full_name='test/memory',private=False,default_branch='main',stargazers_count=12,
                            forks_count=1,archived=False,created_at='2025-01-01T00:00:00Z',pushed_at='2026-09-17T00:00:00Z',license=None)
                    elif '/releases?' in endpoint: obj=[]
                    elif '/compare/' in endpoint: obj=dict(files=[],commits=[],total_commits=0)
                    elif endpoint=='search/repositories': obj=dict(items=[],total_count=0,incomplete_results=False)
                    else: raise AssertionError(endpoint)
                    raw=b'HTTP/2.0 200 OK\r\n\r\n'+json.dumps(obj).encode()
                child=unittest.mock.Mock(pid=123,returncode=0);child.communicate.return_value=(raw,b'');return child
            with patch.object(subprocess,'Popen',side_effect=fake_popen), patch.object(owner,'now',return_value='2026-09-17T00:00:00Z'),contextlib.redirect_stdout(io.StringIO()):
                t=owner.Transport(root,run);packet=owner.collect(t,None)
                self.assertEqual(packet['source_coverage'],dict(metadata=1,head=1,releases=1))
                review_dir=run/'agent-review';review_dir.mkdir()
                (review_dir/'latest.md').write_text('# Fixture\n\nOne\nTwo\nThree\n\n## 已确认合并/发布的变更\n\n'+rid+'\n',encoding='utf-8',newline='\n')
                review=dict(repository=tracker.TARGET,run_id=rid,agent_reviewed=True,selected_change_reviews=[1],
                    completed_change_reviews=[1],candidate_reviews=0,pending_work=[],coverage_note='synthetic only',files={'reports/latest.md':'latest.md'})
                owner.save(review_dir/'decisions.json',review)
                prepared=publication.prepare_data(root,rid,review_dir/'decisions.json')
                self.assertEqual(prepared['status'],'prepared')
                data=publication.commit(root,rid,'data')
                owner.readback(owner.Transport(root,run),data)
                publication.prepare_receipt(root,rid)
                self.assertEqual(tracker.load(root/'state/status.json')['coverage']['tracked'],1)
                self.assertEqual(tracker.load(root/'state/status.json')['coverage']['total_observation_pool'],1)
                receipt=publication.commit(root,rid,'receipt')
                result=owner.readback(owner.Transport(root,run),receipt)
                self.assertEqual(result['status'],'passed')
                owner.local.release(root,rid,lock['owner_token'])
                accepted=dict(status='Passed',run_id=rid,data_sha=data['commit_sha'],receipt_sha=receipt['commit_sha'])
                owner.save(run/'owner-pipeline/pages-readback.json',accepted)
                with patch.object(owner,'Transport',side_effect=AssertionError('must reuse accepted Pages')):
                    self.assertEqual(publication.pages(root,rid,review_dir/'not-read.json'),accepted)
                    self.assertTrue(owner.completed(root,run))
                    self.assertEqual(publication.pages(root,rid,review_dir/'not-read.json'),accepted)
        finally:
            fixture.tearDown()

    def test_root_launcher_bytes_and_actual_cmd_modes(self):
        root = Path(__file__).resolve().parents[1]
        raw = (root / "collect-owner.bat").read_bytes()
        self.assertTrue(raw.isascii() and raw.startswith(b"@echo off\r\nchcp 65001 >nul\r\n"))
        self.assertNotIn(b"\n", raw.replace(b"\r\n", b""))
        result = subprocess.run(["cmd.exe", "/d", "/c", str(root / "collect-owner.bat"), "--check"], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        result = subprocess.run(["cmd.exe", "/d", "/c", str(root / "collect-owner.bat"), "--check-exit"], capture_output=True)
        self.assertEqual(result.returncode, 7)


if __name__ == "__main__":
    unittest.main()
