"""Deterministic preparation/commit and website checks after Agent review.

No conclusions are generated here. Agent supplies reviewed UTF-8 files and a
decision manifest; code validates structure, never authenticates the review.
"""
from __future__ import annotations

import argparse
import copy
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import owner_pipeline as owner
import local_maintenance as local
import manifest_validation as mv
import tracker as core
import verify_source_responses as responses


def context(root, run_id):
    run = owner.run_dir(root, run_id)
    stage = run / "owner-pipeline"
    return run, stage, stage / "fixed", core.load(stage / "batch.json")


def check_review(review, run_id):
    core.require(review["repository"] == core.TARGET and review["run_id"] == run_id, "review identity")
    due, done = review["selected_change_reviews"], review["completed_change_reviews"]
    core.require(len(due) == len(set(due)) <= 5 and len(done) == len(set(done)) and set(done) <= set(due), "review budget")
    core.require(0 <= review["candidate_reviews"] <= 10, "candidate review budget")
    core.require(review.get("agent_reviewed") is True, "Agent review required; this flag is not authentication")
    core.require(isinstance(review["pending_work"], list), "Agent must supply remaining work")


def prepare_data(root, run_id, review_path):
    run, stage, fixed, batch = context(root, run_id)
    review = core.load(review_path); check_review(review, run_id)
    core.require(local.pin(root, "HEAD") == batch["base_commit_sha"], "publication base moved; reconcile once first")
    core.require(not local.git(root, "status", "--porcelain=v1", "--untracked-files=all"), "preserve dirty worktree")
    responses.verify(batch, run / "results", core.load(fixed / "state/checkpoints.json"))
    files = {}
    for path, rel in review["files"].items():
        core.safe_path(path)
        core.require(path.startswith(("projects/", "reports/")) or path in ("data/projects.json", "data/candidates.json"), "Agent file outside scope")
        core.require(not path.startswith(("reports/briefs/", "reports/current")), "archive/current generated separately")
        source = (review_path.parent / rel).resolve()
        core.require(source.is_relative_to((run / "agent-review").resolve()), "Agent payload must be in this run's agent-review")
        raw = source.read_bytes(); raw.decode("utf-8")
        core.require(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw, "UTF-8 LF required")
        if path.startswith("reports/weekly/"):
            core.require(not (root / path).exists(), "preserve closed weekly archive")
        files[path] = raw
    registry = json.loads(files["data/projects.json"]) if "data/projects.json" in files else core.load(fixed / "data/projects.json")
    candidates = json.loads(files["data/candidates.json"]) if "data/candidates.json" in files else core.load(fixed / "data/candidates.json")
    ids = core.validate_registry(registry)
    old_ids = core.validate_registry(core.load(fixed / "data/projects.json"))
    core.require(len(ids) + len(candidates["candidates"]) <= 50, "combined project/candidate pool exceeds 50")
    core.require(len(ids - old_ids) <= review["candidate_reviews"], "new admissions exceed actual candidate review count")
    core.require("reports/latest.md" in files, "Agent must author the brief")
    brief = files["reports/latest.md"].decode()
    core.require("## 已确认合并/发布的变更" in brief and run_id in brief, "brief heading/run identity missing")
    corrections = correction_items(core.load(fixed / "state/status.json"))
    for item in corrections:
        core.require(item["brief_text"] in brief and all(url in brief for url in item["source_urls"]), "pending correction not included")
    # An explicit archive transformation, never a global run/date replacement.
    archive = brief.replace("](../", "](../../")
    files["reports/briefs/" + run_id + ".md"] = archive.encode()
    for path in files:
        core.require(not (root / path).exists() or not path.startswith(local.IMMUTABLE), "immutable path exists")
    snap = run / "owner-pipeline/snapshot.json"
    owner.save(snap, batch)
    transport = owner.Transport(root, run)
    record = transport.call("git", ["hash-object", "-w", "--no-filters", str(snap)], "local-data-snapshot-object")
    actual = (run / "results" / record["stdout_file"]).read_text(encoding="ascii").strip()
    core.require(actual == mv.git_blob_sha_bytes(snap.read_bytes()), "actual snapshot object differs")
    output_stage = stage / "data-output"
    prepared = mv.prepare_manifest(core, output_stage, batch, stage / "base-manifest.json", fixed / "state/validation-index.json",
        fixed / "config/tracker.json", fixed / "data/projects.json", fixed / "README.md")
    core.require(prepared["status"] == "prepared", "already prepared: reconcile, do not overwrite")
    for week in prepared["weekly_reports_due"]:
        core.require("reports/weekly/" + week + ".md" in files, "Agent must write due closed-week report: " + week)
    for path in prepared["paths"]:
        files[path] = (output_stage / path).read_bytes()
    for path, raw in files.items():
        target = root / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
    index = core.load(root / "state/validation-index.json")
    core.require(index["snapshots"][-1]["blob_sha"] == actual, "snapshot/index identity")
    owner.save(stage / "data-paths.json", sorted(set(prepared["paths"]) | set(files)), exclusive=True)
    owner.save(stage / "agent-decisions.json", review, exclusive=True)
    return dict(status="prepared", phase="data", paths=core.load(stage / "data-paths.json"), snapshot_blob_sha=actual)


def correction_items(status):
    unique = {}
    for item in status["pending_work"]:
        if item["type"] == "brief_correction":
            key = item["correction_id"]
            core.require(key not in unique or unique[key] == item, "conflicting correction ID")
            unique[key] = item
    return list(unique.values())


def prepare_receipt(root, run_id):
    run, stage, fixed, batch = context(root, run_id)
    proof = core.load(stage / "data-readback.json"); plan = core.load(stage / "data-plan.json")
    core.require(proof["status"] == "passed" and proof["commit_sha"] == plan["commit_sha"]
                 and proof["expected_paths"] == proof["verified_paths"] == len(plan["changed_blobs"]), "Data readback gate")
    core.require(local.pin(root, "HEAD") == plan["commit_sha"], "Receipt parent moved")
    core.require(not local.git(root, "status", "--porcelain=v1", "--untracked-files=all"), "preserve dirty worktree")
    decisions = core.load(stage / "agent-decisions.json"); check_review(decisions, run_id)
    checkpoints = mv.receipt_manifest(core, stage / "receipt-stage", batch, plan["commit_sha"], proof["commit_sha"],
        stage / "data-remote-manifest.json", stage / "data-remote/state/validation-index.json", fixed / "config/tracker.json",
        fixed / "data/projects.json", fixed / "README.md", fixed / "state/checkpoints.json")
    prior = core.load(fixed / "state/checkpoints.json")
    pages = core.load(stage / "release-pages.json")
    for obs in batch["observations"]:
        key = str(obs["repository_id"]); src = obs["releases"]
        if src["status"] == "ok" and src["complete"]:
            checkpoints["sources"][key]["releases"]["incremental_pagination"] = dict(per_page=30, pages=pages[key],
                previous_success_release_ids=[x["id"] for x in prior["sources"].get(key, {}).get("releases", {}).get("value") or []],
                stop_reason=src["pagination"]["stop_reason"])
    local.validate_receipt_release_pages(batch, checkpoints)
    rows = owner.retained(run)
    evidence = dict(schema_version="1.0", run_id=run_id, scope="bootstrap_through_data_readback",
        note="Actual retained responses; consistency does not authenticate historical timing or host trigger.",
        segments=[dict(id=x["id"], calls=[{k: x.get(k) for k in ("id", "tool", "args", "state", "exit_code", "dispatch_at", "returned_at", "stdout_bytes", "stdout_sha256")}])
                  for x in (core.load(p) for p in sorted((run / "results").glob("*.json")))
                  if x.get("tool") == "gh" or x.get("tool") == "git" and x.get("args", [None])[0] in ("ls-remote", "fetch", "push")])
    responses.verify(batch, run / "results", prior, checkpoints, evidence)
    total = len(batch["observations"])
    coverage = {k:dict(expected=total, ok=sum(o[k]["status"] == "ok" and (k != "releases" or o[k]["complete"])
                      for o in batch["observations"])) for k in core.SOURCES}
    for v in coverage.values(): v["rate"] = v["ok"] / total if total else None
    due, completed = len(decisions["selected_change_reviews"]), len(decisions["completed_change_reviews"])
    nulls = dict(instrumentation_complete=False, attempted=None, failed=None, failure_rate=None)
    metrics = dict(schema_version="1.0", run_id=run_id, run_type=batch["run_type"], measured_at=owner.now(),
        data_commit_sha=plan["commit_sha"], measurement_scope="bootstrap_through_data_readback",
        api=dict(unit="observable_github_connector_invocations", **nulls),
        local_transport=dict(unit="observable_gh_and_git_network_invocations", **nulls), source_coverage=coverage,
        deep_review=dict(due=due, completed=completed, rate=completed/due if due else None),
        data_readback=dict(status="passed", expected_paths=proof["expected_paths"], verified_paths=proof["verified_paths"]),
        trigger_evidence=batch.get("trigger_evidence"), unknown_reasons=["Cross-owner/Agent invocation instrumentation not authenticated; do not infer counts."])
    at = core.stamp(batch["observed_at"])
    metric_path = f"state/run-metrics/{at:%Y/%m}/{run_id}.json"
    evidence_path = f"state/run-evidence/{at:%Y/%m}/{run_id}/owner-operations.json"
    status = copy.deepcopy(core.load(fixed / "state/status.json"))
    corrections = correction_items(status)
    for correction in corrections:
        for name in ("reports/latest.md", "reports/briefs/" + run_id + ".md"):
            core.require(name in plan["changed_blobs"], "correction brief not in verified Data")
            text = (stage / "data-remote" / name).read_text(encoding="utf-8")
            core.require(correction["brief_text"] in text and all(url in text for url in correction["source_urls"]), "correction readback absent")
        core.require(not any(x.get("correction_id") == correction["correction_id"] for x in status["completed_work"]), "correction already completed")
        status["completed_work"].append(dict(correction, published_in_run_id=run_id, data_commit_sha=plan["commit_sha"]))
    status["pending_work"] = [x for x in status["pending_work"] if x["type"] != "brief_correction"]
    for item in decisions["pending_work"]:
        if item not in status["pending_work"]:
            status["pending_work"].append(item)
    status.update(last_completed_run_id=run_id, last_verified_data_commit_sha=plan["commit_sha"],
        latest_snapshot_path=core.snapshot_path(batch), last_verified_collection_at=batch["observed_at"],
        last_successful_collection_at=batch["observed_at"],
        latest_run_metrics=dict(metrics, path=metric_path))
    status["latest_local_run"] = dict(run_id=run_id, runtime_mode="local_git", scope="owner_collection_agent_review",
                                     observed_at=batch["observed_at"], trigger_verification="unverified")
    report_coverage = status.setdefault("coverage", {})
    for kind in core.SOURCES:
        report_coverage.setdefault(kind, {}).update(expected=coverage[kind]["expected"], ok=coverage[kind]["ok"])
    report_coverage["releases"].update(pages_obtained=sum(len(x) for x in pages.values()),
        pagination_complete=coverage["releases"]["ok"], partial=total-coverage["releases"]["ok"])
    report_coverage.update(source_run_id=run_id, semantic_review=decisions["coverage_note"],
        pr_change_review=dict(due=due, completed=completed, full_change_ranges_reviewed=False, note=decisions["coverage_note"]),
        discovery=dict(queries=len(batch["discovery"]), pages=len(batch["discovery"]),
            returned=sum(q["returned"] for q in batch["discovery"]),
            pagination_complete=all(q["pagination_complete"] is True for q in batch["discovery"])))
    outputs = {"state/checkpoints.json":checkpoints, "state/status.json":status, metric_path:metrics, evidence_path:evidence}
    for path in outputs:
        core.require(not path.startswith(local.IMMUTABLE) or not (root / path).exists(), "immutable Receipt exists")
    for path, value in outputs.items():
        owner.save(root / path, value)
    owner.save(stage / "receipt-paths.json", list(outputs), exclusive=True)
    return dict(status="prepared", phase="receipt", paths=list(outputs))


def commit(root, run_id, phase):
    run, stage, _, batch = context(root, run_id)
    paths = core.load(stage / (phase + "-paths.json"))
    core.guard_paths(paths)
    core.require(local.lock_status(root).get("run_id") == run_id, "acquire same-run lock before commit")
    expected = batch["base_commit_sha"] if phase == "data" else core.load(stage / "data-plan.json")["commit_sha"]
    core.require(local.pin(root, "HEAD") == expected, "commit parent differs")
    changed = set(local.git(root, "diff", "--name-only").decode().splitlines())
    changed |= set(local.git(root, "ls-files", "--others", "--exclude-standard").decode().splitlines())
    core.require(changed == set(paths) and not local.git(root, "diff", "--cached", "--name-only"), "only explicit task paths may be staged")
    for path in paths:
        raw = (root / path).read_bytes()
        core.require(b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 LF required")
        raw.decode("utf-8")
        core.require(b"owner_token" not in raw and b"C:\\Users\\" not in raw, "private handoff content in publication")
    transport = owner.Transport(root, run)
    transport.call("git", ["add", "--", *paths], "local-" + phase + "-add")
    for path in paths:
        core.require(local.git(root, "show", ":" + path) == (root / path).read_bytes(), "index byte conversion")
    local.git(root, "diff", "--cached", "--check")
    transport.call("git", ["commit", "-m", phase + ": " + run_id], "local-" + phase + "-commit")
    plan = local.publication_plan(root, local.pin(root, "HEAD"), phase, run_id)
    owner.save(stage / (phase + "-plan.json"), plan)
    return plan


def pages(root, run_id, assertions_path):
    run, stage, _, _ = context(root, run_id)
    data, receipt = (core.load(stage / (p + "-readback.json")) for p in ("data", "receipt"))
    core.require(data["status"] == receipt["status"] == "passed", "Data/Receipt gates")
    prior_result = stage / "pages-readback.json"
    if prior_result.exists():
        result = core.load(prior_result)
        core.require(result["status"] == "Passed" and result["run_id"] == run_id
                     and result["data_sha"] == data["commit_sha"] and result["receipt_sha"] == receipt["commit_sha"], "Pages completion differs")
        finish_run(root, run, result, data, receipt)
        return result
    assertions = core.load(assertions_path)
    core.require(assertions["run_id"] == run_id and assertions["data_sha"] == data["commit_sha"]
                 and assertions["receipt_sha"] == receipt["commit_sha"], "website identity")
    brief = (stage / "data-remote/reports/latest.md").read_text(encoding="utf-8")
    intro = [line.removeprefix("# ") for line in brief.splitlines() if line][:4]
    for name in ("homepage", "latest", "archive"):
        core.require(all(text in brief for text in assertions[name]), "assertion not from this run's actual brief")
        assertions[name] = intro + assertions[name]
        if name != "homepage":
            assertions[name] += ["已确认合并/发布的变更", run_id]
    t = owner.Transport(root, run)
    prefix = "repos/" + core.TARGET
    # All Pages actions are excluded from already-frozen transport metrics.
    _, site = t.response(t.gh(prefix + "/pages", "pages-site"))
    base = site["html_url"]
    core.require(base == "https://notes.psiqaq.cn/agent-memory-github-trending/", "unexpected deployment URL")
    _, workflows = t.response(t.gh(prefix + "/actions/runs?per_page=20", "pages-workflows"))
    candidates = [w for w in workflows["workflow_runs"] if w["name"] == "pages build and deployment"
                  and w["head_sha"] in (data["commit_sha"], receipt["commit_sha"])]
    core.require(candidates, "matching Pages workflow not observed; no automatic retry")
    w = candidates[0]
    _, jobs = t.response(t.gh(prefix + f"/actions/runs/{w['id']}/jobs?per_page=100", "pages-jobs"))
    if w["status"] != "completed":
        return dict(status="pending", workflow=w["html_url"], jobs=jobs["jobs"],
                    next_step="Agent checks queued/waiting eligibility for the authorized single 30-minute native reminder")
    core.require(w["conclusion"] == "success", "Pages workflow failed")
    for name in ("build", "deploy"):
        core.require(any(j["name"] == name and j["conclusion"] == "success" for j in jobs["jobs"]), "Pages job not successful")
    _, deps = t.response(t.gh(prefix + "/deployments?environment=github-pages&per_page=20", "pages-deployments"))
    dep = next(d for d in deps if d["sha"] == w["head_sha"])
    _, states = t.response(t.gh(prefix + f"/deployments/{dep['id']}/statuses?per_page=20", "pages-deployment-status"))
    core.require(states and states[0]["state"] == "success", "deployment not successful")
    local.git(root, "merge-base", "--is-ancestor", data["commit_sha"], w["head_sha"])
    outputs = []
    for name, suffix in (("homepage", ""), ("latest", "reports/latest.html"), ("archive", "reports/briefs/" + run_id + ".html")):
        dest = stage / ("website-" + name + ".json")
        if dest.exists():
            result = core.load(dest)
            core.require(result["status"] == "Passed", "prior webpage failure; explicit retry authorization required")
            outputs.append(result); continue
        url = base + suffix
        owner.save(dest, dict(status="started", url=url, at=owner.now()), exclusive=True)
        try:
            req = Request(url, headers={"User-Agent":"Agent Memory Tracker Pages readback"})
            with urlopen(req, timeout=30) as response:
                raw = response.read(); code = response.status; actual_url = response.geturl()
            (stage / ("website-" + name + ".html")).write_bytes(raw)
            text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw.decode("utf-8"))).split())
            core.require(assertions[name], "Agent must select actual report content assertions")
            core.require(code == 200 and actual_url == url and all(s in text for s in assertions[name]), "webpage bytes/content mismatch")
            result = dict(status="Passed", url=url, http_status=code, checks=assertions[name], at=owner.now())
        except Exception as exc:
            owner.save(dest, dict(status="Failed", url=url, error=str(exc), at=owner.now()))
            raise
        owner.save(dest, result); outputs.append(result)
    result = dict(status="Passed", run_id=run_id, data_sha=data["commit_sha"], receipt_sha=receipt["commit_sha"],
                  workflow=w["html_url"], deployment_id=dep["id"], pages=outputs, metrics_scope="excluded")
    owner.save(stage / "pages-readback.json", result, exclusive=True)
    finish_run(root, run, result, data, receipt)
    return result


def finish_run(root, run, result, data, receipt):
    core.require(local.lock_status(root)["state"] == "unlocked", "release reconciled maintenance lock before final completion")
    path = run / "final-completion.json"
    if path.exists():
        owner.completed(root, run)
        return
    owner.save(path, dict(repository=core.TARGET, run_id=run.name,
        maintenance_complete=True, data_sha=data["commit_sha"], receipt_sha=receipt["commit_sha"],
        data_readback=data, receipt_readback=receipt, pages=result, lock_released=True,
        trigger="unknown/unverified", scheduled_end_to_end="Not Run: owner/Agent workflow is not unattended proof",
        checked_at=owner.now()), exclusive=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare-data", "prepare-receipt", "commit", "pages"))
    parser.add_argument("--root", type=Path, default=owner.ROOT)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--phase", choices=("data", "receipt"))
    parser.add_argument("--owner-file", type=Path)
    args = parser.parse_args()
    try:
        owner.ordinary_user(); owner.gates(args.root)
        if args.command != "pages":
            run = owner.run_dir(args.root, args.run_id)
            core.require(args.owner_file and args.owner_file.resolve().is_relative_to(run.resolve()), "--owner-file in this run required")
            core.require(core.load(args.owner_file) == core.load(local.lock_path(args.root)), "lock owner token differs")
        if args.command == "prepare-data":
            core.require(args.review, "--review required"); result = prepare_data(args.root, args.run_id, args.review)
        elif args.command == "prepare-receipt": result = prepare_receipt(args.root, args.run_id)
        elif args.command == "commit":
            core.require(args.phase, "--phase required"); result = commit(args.root, args.run_id, args.phase)
        else:
            core.require(args.review, "--review website assertions required"); result = pages(args.root, args.run_id, args.review)
        print(core.encoded(result))
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError, StopIteration) as exc:
        parser.exit(1, "Publication stage stopped without retry: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
