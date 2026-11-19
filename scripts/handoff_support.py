"""Offline, run-bound handoff tools. Confirmation fields are never authenticated here."""
import base64
import hashlib
import json
import textwrap
from pathlib import Path


def ledger(owner, run):
    owner.retained(run)  # failed, uncertain or corrupted responses cannot authorize replay
    return {p.relative_to(run).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((run / "results").glob("*")) if p.suffix in (".json", ".stdout")}


def resume_draft(owner, root, run, command):
    failure = run / "owner-pipeline/FAILED.json"
    target = run / "owner-pipeline/resume-draft.json"
    if target.exists():
        previous = owner.tracker.load(target)
        owner.tracker.require(previous["run_id"] == run.name and previous["command"] == command, "existing draft identity differs")
        return dict(status="existing_draft_requires_recheck", path=str(target), network="Not Run")
    lock = owner.local.lock_status(root)
    result = dict(schema_version="1.0", repository=owner.REPO, run_id=run.name,
        command=command, checked_at=owner.now(), failure_sha256=hashlib.sha256(failure.read_bytes()).hexdigest(),
        local_head_sha=owner.local.pin(root, "HEAD"), lock_sha256=lock.get("lock_sha256"),
        retained_ledger=ledger(owner, run), original_writer_stopped=None,
        single_writer_confirmed=None, writes_reconciled=None, source_refs=[],
        notice="Draft only. Agent must check host/process/write outcomes before confirming; no retry permission.")
    owner.save_consistent(target, result)
    return dict(status="draft_only", path=str(target), network="Not Run")


def validate_resume(owner, root, run, command, path):
    path = path.resolve()
    owner.tracker.require(path.is_relative_to(run.resolve()), "resume evidence must be in this run")
    value = owner.tracker.load(path)
    owner.tracker.require(value["schema_version"] == "1.0" and value["repository"] == owner.REPO
                          and value["run_id"] == run.name and value["command"] == command, "resume identity differs")
    owner.tracker.stamp(value["checked_at"])
    for key in ("original_writer_stopped", "single_writer_confirmed", "writes_reconciled"):
        owner.tracker.require(value.get(key) is True, "unconfirmed resume field: " + key)
    owner.tracker.require(value.get("source_refs") and all(isinstance(x, str) and x for x in value["source_refs"]),
                          "actual host/process/write source references required")
    owner.tracker.require(value["failure_sha256"] == hashlib.sha256((run / "owner-pipeline/FAILED.json").read_bytes()).hexdigest(), "first failure changed")
    owner.tracker.require(value["local_head_sha"] == owner.local.pin(root, "HEAD"), "resume HEAD differs")
    owner.tracker.require(value["lock_sha256"] == owner.local.lock_status(root).get("lock_sha256"), "resume lock differs")
    owner.tracker.require(value["retained_ledger"] == ledger(owner, run), "retained ledger changed")
    return value


def extract_review(owner, root, run, plan):
    owner.validate_review_plan(plan)
    owner.tracker.require(plan["run_id"] == run.name, "review run differs")
    transport = owner.Transport(root, run)
    out = run / "agent-review/extracted"
    catalog = []
    for request in plan["requests"]:
        row, = [x for x in transport.rows if x.get("kind") == "review-evidence" and x["args"][4] == request["endpoint"]]
        more, obj = transport.response(row)
        entry = dict(repository_id=request["repository_id"], full_name=request["full_name"],
            endpoint=request["endpoint"], record=row["id"], observed_at=row["returned_at"], more=more)
        endpoint = request["endpoint"]
        if "/contents/" in endpoint or "/git/blobs/" in endpoint:
            entry.update(kind="file", encoding=obj["encoding"], sha=obj["sha"], size=obj["size"])
            if "/git/blobs/" in endpoint:
                owner.tracker.require(obj["sha"] == endpoint.rsplit("/", 1)[1], "requested review blob SHA differs")
            if obj["encoding"] == "base64":
                raw = base64.b64decode(obj["content"])
                owner.tracker.require(len(raw) == obj["size"] and owner.manifest.git_blob_sha_bytes(raw) == obj["sha"], "review blob bytes differ")
                # Content-addressed names avoid collisions between PRs or path traversal.
                path = out / "blobs" / obj["sha"]
                if path.exists():
                    owner.tracker.require(path.read_bytes() == raw, "extracted blob changed")
                else:
                    path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
                entry.update(body_status="verified", body_file=path.relative_to(run).as_posix())
            else:
                entry.update(body_status="missing", reason="Contents returned metadata only; not a full-file read",
                    suggested_get="repos/" + request["full_name"] + "/git/blobs/" + obj["sha"])
        elif "/pulls/" in endpoint:
            if isinstance(obj, list):
                entry.update(kind="pull_files", number=int(endpoint.split("/pulls/")[1].split("/")[0]),
                             count=len(obj), files=[x["filename"] for x in obj])
            else:
                entry.update(kind="pull", number=obj["number"], changed_files=obj["changed_files"],
                             merged_at=obj["merged_at"], merge_sha=obj["merge_commit_sha"], head_sha=obj["head"]["sha"])
        else:
            entry.update(kind="git_object", value=obj,
                         resolution="unpeeled" if obj.get("object", {}).get("type") == "tag" else "observed")
        catalog.append(entry)
    for entry in catalog:
        if entry["kind"] != "pull":
            continue
        pages = [x for x in catalog if x["kind"] == "pull_files" and x["repository_id"] == entry["repository_id"] and x["number"] == entry["number"]]
        page_numbers = sorted(int(x["endpoint"].rsplit("page=", 1)[1]) for x in pages)
        returned = {f for x in pages for f in x["files"]}
        last = max(pages, key=lambda x: int(x["endpoint"].rsplit("page=", 1)[1])) if pages else None
        entry["files_complete"] = bool(pages) and page_numbers == list(range(1, len(pages)+1)) and len(returned) == entry["changed_files"] and last["more"] is False
    owner.save(run / "agent-review/source-catalog.json", catalog)
    return dict(status="extracted", responses=len(catalog), missing_bodies=sum(x.get("body_status") == "missing" for x in catalog),
                catalog=str(run / "agent-review/source-catalog.json"), network="Not Run", semantic_review="Not Run")


BUNDLE_FILES = ("owner_pipeline.py", "local_maintenance.py", "tracker.py", "manifest_validation.py",
                "verify_source_responses.py", "staged_publication.py", "handoff_support.py", "webpage_checks.py")

ENTRY = '''"""Run-bound entry; execute only the reviewed local Git bundle."""
import hashlib,json,runpy,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
m=json.loads((here/"entry.json").read_bytes())
root=Path(m["root"])
assert m["repository"]=="psiQAQ/agent-memory-github-trending"
for name,sha in m["sources"].items():
    raw=(here/"bundle"/name).read_bytes()
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\\0"+raw).hexdigest()==sha
    assert subprocess.check_output(["git","show",m["program_commit"]+":scripts/"+name],cwd=root)==raw
sys.path.insert(0,str(here/"bundle"))
import owner_pipeline as owner
owner.ROOT=root
if sys.argv[1:] in (["--check"],["--check-exit"]):
    print(owner.tracker.encoded(dict(owner.check(root),run_id=m["run_id"],program_commit=m["program_commit"])))
    raise SystemExit(7 if sys.argv[1:]==["--check-exit"] else 0)
assert not any(x in ("--root","--run-id") or x.startswith(("--root=","--run-id=")) for x in sys.argv[1:]),"entry identity is fixed"
sys.argv=[m["program"],m["command"],"--root",str(root),"--run-id",m["run_id"],*sys.argv[1:]]
runpy.run_path(str(here/"bundle"/(m["program"]+".py")),run_name="__main__")
'''
ENTRY = ("from pathlib import Path\nimport json,os,sys\n"
         "def main():\n" + textwrap.indent(ENTRY, "    ") +
         '\nif __name__=="__main__":\n'
         '    try: main()\n'
         '    except Exception as exc:\n'
         '        path=Path(__file__).resolve().parent/"ENTRY-FAILED.json"\n'
         '        if not path.exists(): path.write_text(json.dumps({"status":"Failed","pid":os.getpid(),"error":str(exc)},indent=2)+"\\n",encoding="utf-8",newline="\\n")\n'
         '        print("Entry stopped without retry: "+str(exc),file=sys.stderr)\n'
         '        print("SUMMARY: "+str(path),file=sys.stderr)\n'
         '        raise SystemExit(1)\n')


def create_entry(owner, root, run, commit, program, command):
    allowed = {"owner_pipeline": ("collect", "review-fetch", "publish", "readback"),
               "staged_publication": ("prepare-data", "prepare-receipt", "commit", "pages", "recheck-web")}
    owner.tracker.require(command in allowed[program], "entry command outside fixed stages")
    commit = owner.local.pin(root, commit)  # HEAD or full SHA only, never a branch name
    directory = root / ".cache/ssh-user-check" / run.name / (program + "-" + command)
    sources, contents = {}, {}
    for name in BUNDLE_FILES:
        raw = owner.local.git(root, "show", commit + ":scripts/" + name)
        sha = owner.local.git(root, "rev-parse", commit + ":scripts/" + name).decode().strip()
        owner.tracker.require(owner.manifest.git_blob_sha_bytes(raw) == sha, "bundle blob differs")
        sources[name], contents[name] = sha, raw
    manifest = dict(repository=owner.REPO, root=str(root.resolve()), run_id=run.name,
                    program_commit=commit, program=program, command=command, sources=sources)
    owner.save_consistent(directory / "entry.json", manifest)
    for name, raw in contents.items():
        dest = directory / "bundle" / name
        if dest.exists():
            owner.tracker.require(dest.read_bytes() == raw, "existing bundle changed")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(raw)
    launcher = directory / "entry.py"
    bat = directory / "entry.bat"
    bat_bytes = ("@echo off\r\nchcp 65001 >nul\r\nsetlocal\r\ncd /d \"%~dp0\"\r\n"
                 "python -B \"%~dp0entry.py\" %*\r\nset \"entry_exit=%errorlevel%\"\r\n"
                 "if not \"%~1\"==\"\" exit /b %entry_exit%\r\necho Send the printed SUMMARY path to Codex.\r\n"
                 "pause\r\nexit /b %entry_exit%\r\n").encode("ascii")
    for path, raw in ((launcher, ENTRY.encode("utf-8")), (bat, bat_bytes)):
        if path.exists():
            owner.tracker.require(path.read_bytes() == raw, "entry changed; preserve and reconcile")
        else:
            path.write_bytes(raw)
    return dict(status="generated_not_runtime_verified", entry=str(bat), program_commit=commit,
                run_id=run.name, network="Not Run", note="Review source/approval, then verify in real CMD before delivery.")
