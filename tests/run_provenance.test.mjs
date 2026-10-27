import { assessRunProvenance } from "../scripts/run_provenance.mjs";
export function runProvenanceTests(assess = assessRunProvenance) {
  const fixture = {
    capture_id: "synthetic-entry-01", captured_at: "2026-10-27T00:00:02Z",
    legacy_run_type: "interactive", evidence_origin: "actual",
    platform_receipt_ref: "private-fixture-receipt",
    invocation: {source_origin:"platform_invocation", task_id:"private-fixture-task",
      run_id:"private-fixture-run", binding:{kind:"codex",id:"private-fixture-thread"},
      trigger_kind:"scheduled", scheduled_for:"2026-10-27T00:00:00Z",
      started_at:"2026-10-27T00:00:01Z", receipt_ref:"private-fixture-receipt"},
    task_record: {id:"private-fixture-task", thread_id:"private-fixture-thread",
      prompt:"scheduled by assertion", last_run_time:"2026-10-27T00:00:01Z",
      run_details:{last_run:{id:"private-fixture-run",scheduled_for:"2026-10-27T00:00:00Z",
        started_at:"2026-10-27T00:00:01Z"},latest_result:null}}
  };
  const results = [];
  const check = (name, mutate, predicate) => {
    const input = JSON.parse(JSON.stringify(fixture)); mutate(input);
    const result = assess(input);
    if (!predicate(result)) throw new Error(name + ": " + JSON.stringify(result));
    if (result.authenticated !== false || result.public_evidence.verification_status !== "unverified")
      throw new Error("structural validation promoted to authentication: " + name);
    results.push(name);
  };
  check("matching records are only a candidate",()=>{},r=>r.candidate_kind==="scheduled");
  check("missing entry is not scheduled",x=>x.invocation=null,r=>r.candidate_kind==="unknown");
  check("null last_run is unknown despite enabled schedule",x=>{
    x.task_record.is_enabled=true; x.task_record.schedule="FREQ=DAILY";
    x.task_record.run_details.last_run=null;
  },r=>r.candidate_kind==="unknown");
  check("legacy interactive is not manual proof",x=>{
    x.invocation=null;x.task_record.run_details.last_run=null;
  },r=>r.public_evidence.legacy_run_type==="interactive"&&r.public_evidence.trigger_kind==="unknown"&&!r.public_evidence.label_is_trigger_proof);
  check("scheduled legacy label is not proof",x=>{
    x.legacy_run_type="scheduled";x.invocation=null;
  },r=>r.candidate_kind==="unknown");
  check("task identity mismatch",x=>x.invocation.task_id="other",r=>r.public_evidence.conflicts.includes("task_identity"));
  check("run identity mismatch",x=>x.invocation.run_id="other",r=>r.public_evidence.conflicts.includes("platform_run_identity"));
  check("binding mismatch",x=>x.invocation.binding.id="other",r=>r.public_evidence.conflicts.includes("binding_identity"));
  check("latest record alone is not current invocation",x=>x.invocation=null,r=>r.public_evidence.invocation_match==="unknown");
  check("missing explicit trigger kind",x=>delete x.invocation.trigger_kind,r=>r.candidate_kind==="unknown");
  check("platform manual contradicts scheduled entry",x=>x.task_record.run_details.last_run.trigger_kind="manual",r=>r.candidate_kind==="unknown"&&r.public_evidence.conflicts.includes("trigger_kind"));
  check("platform scheduled contradicts manual entry",x=>{
    x.invocation.trigger_kind="manual";x.task_record.run_details.last_run.trigger_kind="scheduled";
  },r=>r.candidate_kind==="unknown"&&r.public_evidence.conflicts.includes("trigger_kind"));
  check("matching explicit platform trigger remains structural only",x=>x.task_record.run_details.last_run.trigger_kind="scheduled",r=>r.candidate_kind==="scheduled"&&!r.authenticated);
  check("prompt-derived entry rejected",x=>x.invocation.source_origin="prompt",r=>r.candidate_kind==="unknown");
  check("unmatched private receipt",x=>x.invocation.receipt_ref="other",r=>r.public_evidence.conflicts.includes("current_receipt_correlation"));
  check("started_at conflict",x=>x.invocation.started_at="2026-10-27T00:00:02Z",r=>r.public_evidence.conflicts.includes("started_at"));
  check("timezone-normalized times compare equal",x=>x.invocation.started_at="2026-10-27T08:00:01+08:00",r=>r.candidate_kind==="scheduled");
  check("manual candidate needs explicit matching entry",x=>{
    x.invocation.trigger_kind="manual";x.invocation.scheduled_for=null;
    x.task_record.run_details.last_run.scheduled_for=null;
  },r=>r.candidate_kind==="manual"&&r.public_evidence.trigger_kind==="unknown");
  check("old result is stale, not current output",x=>x.task_record.run_details.latest_result={
    run_id:"old-run",created_at:"2026-10-26T00:00:00Z"
  },r=>r.stale_latest_result);
  check("same run older result still stale",x=>x.task_record.run_details.latest_result={
    run_id:"private-fixture-run",created_at:"2026-10-26T00:00:00Z"
  },r=>r.stale_latest_result);
  check("synthetic input never supplies a real candidate",x=>x.evidence_origin="synthetic",r=>r.candidate_kind==="unknown"&&!r.authenticated);
  check("public output omits private IDs, receipts and prompt",()=>{},r=>{
    const p=JSON.stringify(r.public_evidence);
    return !p.includes("private-fixture-")&&!p.includes("scheduled by assertion");
  });
  check("capture time cannot be silently filled",x=>x.captured_at=null,r=>!r.valid&&r.public_evidence.captured_at===null);
  const legacy = JSON.stringify(fixture);
  assess(fixture);
  if (JSON.stringify(fixture)!==legacy) throw new Error("input or legacy record mutated");
  results.push("input and legacy labels remain immutable");
  return {passed:results.length,results,evidence_origin:"synthetic",authenticated:false};
}
