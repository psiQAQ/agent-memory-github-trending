"""Offline, run-bound handoff tools. Confirmation fields are never authenticated here."""
import base64
import hashlib
import json
import re
import textwrap
from pathlib import Path


REVIEW_ENDPOINT_ERROR = "review GET endpoint not allowed"
REVIEW_PLAN_RECOVERY = "owner-pipeline/review-plan-recovery.json"


def original_review_not_found(owner, run):
    failure = owner.tracker.load(run / "owner-pipeline/FAILED.json")
    match = re.fullmatch(r"action failed; retained without retry: (owner-[a-f0-9]{20})", failure.get("error", ""))
    if not match or failure.get("action") != "review-fetch":
        return None
    owner.tracker.require(failure.get("repository") == owner.REPO and failure.get("run_id") == run.name
                          and failure.get("status") == "Failed", "review failure identity differs")
    path = run / "results" / (match[1] + ".json")
    row = owner.tracker.load(path)
    args = row["args"]
    if (row.get("state") != "returned" or row.get("exit_code") != 1 or row.get("tool") != "gh"
            or row.get("kind") != "review-evidence" or len(args) != 5
            or args[:4] != ["api", "--method", "GET", "--include"]):
        return None
    endpoint = re.fullmatch(r"repos/([^/]+/[^/]+)/pulls/(\d+)", args[4])
    if not endpoint or not owner.tracker.NAME.fullmatch(endpoint[1]):
        return None
    raw = owner.result_bytes(path, row)
    parts = re.split(rb"\r?\n\r?\n", raw, maxsplit=1)
    if len(parts) != 2 or not re.match(rb"HTTP/\S+ 404(?: |\r?\n|$)", parts[0]):
        return None
    payload = json.loads(parts[1])
    owner.tracker.require(isinstance(payload, dict) and payload.get("message") == "Not Found"
                          and str(payload.get("status")) == "404", "unexpected GitHub 404 body")
    owner.tracker.require(re.search(rb"^x-github-request-id: [^\r\n]+", parts[0], re.I | re.M) is not None,
                          "review 404 has no GitHub request identity")
    batch = owner.tracker.load(run / "owner-pipeline/batch.json")
    owner.tracker.require(batch["run_id"] == run.name and any(
        o["repository_id"] == row["repository_id"] and o["full_name"] == endpoint[1]
        and o["metadata"]["status"] == "ok" for o in batch["observations"]),
        "review 404 must belong to a registered repository in this batch")
    return row


def ledger(owner, run, missing_review=None):
    owner.retained(run, missing_review=missing_review)
    return {p.relative_to(run).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((run / "results").glob("*")) if p.suffix in (".json", ".stdout")}


def resume_draft(owner, root, run, command):
    failure = run / "owner-pipeline/FAILED.json"
    target = run / "owner-pipeline/resume-draft.json"
    lock = owner.local.lock_status(root)
    missing_review = original_review_not_found(owner, run) if command == "review-fetch" else None
    result = dict(schema_version="1.0", repository=owner.REPO, run_id=run.name,
        command=command, checked_at=owner.now(), failure_sha256=hashlib.sha256(failure.read_bytes()).hexdigest(),
        local_head_sha=owner.local.pin(root, "HEAD"), lock_sha256=lock.get("lock_sha256"),
        retained_ledger=ledger(owner, run, missing_review), original_writer_stopped=None,
        single_writer_confirmed=None, writes_reconciled=None, source_refs=[],
        notice="Draft only. Agent must check host/process/write outcomes before confirming; no retry permission.")
    if missing_review:
        result["review_not_found_id"] = missing_review["id"]
        owner.verify_package(root, run)
    if target.exists():
        previous = owner.tracker.load(target)
        fields = ("repository", "run_id", "command", "failure_sha256", "local_head_sha", "lock_sha256",
                  "retained_ledger", "review_not_found_id")
        state = {k: result.get(k) for k in fields}
        if all(previous.get(k) == result.get(k) for k in fields):
            return dict(status="existing_draft_requires_recheck", path=str(target), network="Not Run")
        suffix = hashlib.sha256(owner.tracker.encoded(state).encode()).hexdigest()[:16]
        target = run / "owner-pipeline" / ("resume-draft-" + suffix + ".json")
        if target.exists():
            return dict(status="existing_draft_requires_recheck", path=str(target), network="Not Run")
    owner.save_consistent(target, result)
    return dict(status="draft_only", path=str(target), network="Not Run")


def check_resume_confirmation(owner, run, command, value):
    owner.tracker.require(value["schema_version"] == "1.0" and value["repository"] == owner.REPO
                          and value["run_id"] == run.name and value["command"] == command, "resume identity differs")
    owner.tracker.stamp(value["checked_at"])
    for key in ("original_writer_stopped", "single_writer_confirmed", "writes_reconciled"):
        owner.tracker.require(value.get(key) is True, "unconfirmed resume field: " + key)
    owner.tracker.require(value.get("source_refs") and all(isinstance(x, str) and x for x in value["source_refs"]),
                          "actual host/process/write source references required")
    owner.tracker.require(value["failure_sha256"] == hashlib.sha256((run / "owner-pipeline/FAILED.json").read_bytes()).hexdigest(), "first failure changed")


def validate_resume(owner, root, run, command, path):
    path = path.resolve()
    owner.tracker.require(path.is_relative_to(run.resolve()), "resume evidence must be in this run")
    value = owner.tracker.load(path)
    check_resume_confirmation(owner, run, command, value)
    owner.tracker.require(value["local_head_sha"] == owner.local.pin(root, "HEAD"), "resume HEAD differs")
    owner.tracker.require(value["lock_sha256"] == owner.local.lock_status(root).get("lock_sha256"), "resume lock differs")
    missing_review = original_review_not_found(owner, run) if command == "review-fetch" else None
    owner.tracker.require(value.get("review_not_found_id") == (missing_review["id"] if missing_review else None),
                          "resume review 404 identity differs")
    owner.tracker.require(value["retained_ledger"] == ledger(owner, run, missing_review), "retained ledger changed")
    if missing_review:
        owner.verify_package(root, run)
        batch = owner.tracker.load(run / "owner-pipeline/batch.json")
        owner.tracker.require(batch["base_commit_sha"] == value["local_head_sha"], "review recovery base differs")
    return value


def recovered_review(owner, run):
    value = owner.tracker.load(run / "owner-pipeline/review-recovery.json")
    check_resume_confirmation(owner, run, "review-fetch", value)
    row = original_review_not_found(owner, run)
    owner.tracker.require(row and row["id"] == value.get("review_not_found_id"), "recovered review 404 differs")
    for suffix in (".json", ".stdout"):
        name = "results/" + row["id"] + suffix
        owner.tracker.require(value["retained_ledger"].get(name) == hashlib.sha256((run / name).read_bytes()).hexdigest(),
                              "recovered review response changed: " + name)
    return row


def original_review_plan_failure(owner, run):
    first = owner.tracker.load(run / "owner-pipeline/FAILED.json")
    owner.tracker.require(first.get("repository") == owner.REPO and first.get("run_id") == run.name
                          and first.get("status") == "Failed" and first.get("action") == "review-fetch"
                          and first.get("error") == REVIEW_ENDPOINT_ERROR, "first failure is not a review endpoint rejection")
    return first


def confirm_review_plan_recovery(owner, root, run, failed_plan, corrected_plan, evidence):
    """Accept only a pre-transport endpoint rejection with verified, retained review results."""
    require = owner.tracker.require
    first = original_review_plan_failure(owner, run)
    require(owner.local.lock_status(root)["state"] == "unlocked", "release the reconciled review lock first")
    require(not any((run / "owner-pipeline/failures").glob("*.json")), "additional failures need reconciliation")
    for path in (failed_plan, corrected_plan):
        require(path.resolve().is_relative_to(run.resolve()), "review plans must be retained in this run")
    failed_bytes = failed_plan.read_bytes()
    rejected = json.loads(failed_bytes)
    require(rejected["run_id"] == run.name, "rejected review plan belongs to a different run")
    try:
        owner.validate_review_plan(rejected)
    except ValueError as exc:
        require(str(exc) == REVIEW_ENDPOINT_ERROR, "rejected plan does not match the original validation error")
    else:
        raise ValueError("original review plan does not reproduce the validation error")
    confirmation = validate_resume(owner, root, run, "review-fetch", evidence)
    owner.verify_package(root, run)
    batch = owner.tracker.load(run / "owner-pipeline/batch.json")
    require(batch["base_commit_sha"] == confirmation["local_head_sha"], "review recovery base differs")
    corrected_bytes = corrected_plan.read_bytes()
    plan = json.loads(corrected_bytes)
    owner.validate_review_plan(plan)
    require(plan["run_id"] == run.name and plan["requests"], "corrected review plan identity differs")

    failed_at = owner.tracker.stamp(first["at"])
    review = {}
    for row in owner.retained(run):
        if row["kind"] in ("review-evidence", "review-metadata"):
            require(owner.tracker.stamp(row["dispatch_at"]) > failed_at, "review transport predates the rejection")
            if row["kind"] == "review-evidence":
                key = (row["repository_id"], tuple(row["args"]))
                require(row["tool"] == "gh" and key not in review, "review response identity differs")
                owner.source_check.read_response(row, run / "results" / (row["id"] + ".json"), False)
                review[key] = row["id"]
        else:
            require(owner.tracker.stamp(row["returned_at"]) <= failed_at, "unrelated action after review plan rejection")
    expected = {(item["repository_id"], ("api", "--method", "GET", "--include", item["endpoint"]))
                for item in plan["requests"]}
    require(expected == review.keys() and len(expected) == len(plan["requests"]),
            "corrected plan does not match all retained review responses")
    previous = recovered_review_plan(owner, run)
    result = dict(schema_version="1.0", repository=owner.REPO, run_id=run.name,
                  status="confirmed", failure_phase="review-fetch", failure_error=REVIEW_ENDPOINT_ERROR,
                  failure_at=first["at"], failure_sha256=confirmation["failure_sha256"],
                  base_commit_sha=batch["base_commit_sha"], observed_at=batch["observed_at"],
                  network_dispatched_for_failure=False, verified_review_responses=len(review),
                  rejected_plan_sha256=hashlib.sha256(failed_bytes).hexdigest(),
                  corrected_plan_sha256=hashlib.sha256(corrected_bytes).hexdigest(),
                  confirmed_at=previous["confirmed_at"] if previous else owner.now())
    owner.save_consistent(run / REVIEW_PLAN_RECOVERY, result)
    return result


def recovered_review_plan(owner, run):
    path = run / REVIEW_PLAN_RECOVERY
    if not path.exists():
        return None
    result = owner.tracker.load(path)
    first = original_review_plan_failure(owner, run)
    batch = owner.tracker.load(run / "owner-pipeline/batch.json")
    owner.tracker.require(
        result["schema_version"] == "1.0" and result["status"] == "confirmed"
        and result["repository"] == owner.REPO and result["run_id"] == batch["run_id"] == run.name
        and result["base_commit_sha"] == batch["base_commit_sha"] and result["observed_at"] == batch["observed_at"]
        and result["failure_phase"] == "review-fetch" and result["failure_error"] == REVIEW_ENDPOINT_ERROR
        and result["network_dispatched_for_failure"] is False and result["verified_review_responses"] > 0
        and result["failure_at"] == first["at"]
        and result["failure_sha256"] == hashlib.sha256((run / "owner-pipeline/FAILED.json").read_bytes()).hexdigest(),
        "review plan recovery evidence differs")
    return result


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
    allowed = {"owner_pipeline": ("collect", "review-fetch", "confirm-review-recovery", "publish", "readback"),
               "staged_publication": ("prepare-data", "prepare-receipt", "commit", "pages", "recheck-web")}
    owner.tracker.require(command in allowed[program], "entry command outside fixed stages")
    commit = owner.local.pin(root, commit)  # HEAD or full SHA only, never a branch name
    directory = root / ".cache/ssh-user-check" / run.name / (program + "-" + command)
    existing = directory / "entry.json"
    if existing.exists() and owner.tracker.load(existing)["program_commit"] != commit:
        directory = directory.with_name(directory.name + "-" + commit)
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
