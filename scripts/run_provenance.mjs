// Structural reference only. No tools, filesystem, network or authentication.
// Private input identities are compared in memory and never copied to public output.
export function assessRunProvenance(input = {}) {
  const errors = [], missing = [], conflicts = [];
  const text = v => typeof v === "string" && v.length > 0;
  const time = v => text(v) && /(Z|[+-]\d\d:\d\d)$/.test(v) && Number.isFinite(Date.parse(v));
  const sameTime = (a, b) => time(a) && time(b) && Date.parse(a) === Date.parse(b);
  const task = input.task_record ?? null;
  const run = task?.run_details?.last_run ?? null;
  const entry = input.invocation ?? null;
  const latest = task?.run_details?.latest_result ?? null;
  const legacy = input.legacy_run_type ?? null;
  if (!text(input.capture_id)) errors.push("capture_id_required");
  if (!time(input.captured_at)) errors.push("captured_at_requires_explicit_timezone");
  if (!["scheduled", "interactive", "interactive_baseline"].includes(legacy)) errors.push("legacy_run_type");
  if (!task) missing.push("task_record");
  if (!run) missing.push("platform_last_run");
  if (!entry) missing.push("current_invocation");
  if (entry && entry.source_origin !== "platform_invocation") missing.push("independent_platform_invocation");
  const compare = (a, b, key) => {
    if (!text(a) || !text(b)) missing.push(key);
    else if (a !== b) conflicts.push(key);
  };
  if (entry && task) {
    compare(entry.task_id, task.id, "task_identity");
    const kind = entry.binding?.kind;
    const bound = kind === "codex" ? task.thread_id : kind === "chatgpt" ? task.conversation_id : null;
    compare(entry.binding?.id, bound, "binding_identity");
  }
  if (entry && run) {
    compare(entry.run_id, run.id, "platform_run_identity");
    compare(entry.receipt_ref, input.platform_receipt_ref, "current_receipt_correlation");
    if (!["scheduled", "manual"].includes(entry.trigger_kind)) missing.push("explicit_trigger_kind");
    // A platform field, when exposed, must not contradict the current invocation.
    if (text(run.trigger_kind) && text(entry.trigger_kind) && run.trigger_kind !== entry.trigger_kind)
      conflicts.push("trigger_kind");
    for (const key of ["started_at", ...(entry.trigger_kind === "scheduled" ? ["scheduled_for"] : [])]) {
      if (!time(entry[key]) || !time(run[key])) missing.push(key);
      else if (!sameTime(entry[key], run[key])) conflicts.push(key);
    }
  }
  const matched = !errors.length && !missing.length && !conflicts.length;
  const candidate = matched && input.evidence_origin === "actual" ? entry.trigger_kind : "unknown";
  const staleResult = latest && run ? !!(
    latest.run_id !== run.id ||
    !time(latest.created_at) || !time(run.started_at) ||
    Date.parse(latest.created_at) < Date.parse(run.started_at)
  ) : null;
  const publicEvidence = {
    schema_version: "1.0",
    capture_id: text(input.capture_id) ? input.capture_id : null,
    captured_at: time(input.captured_at) ? new Date(input.captured_at).toISOString() : null,
    legacy_run_type: legacy,
    label_is_trigger_proof: false,
    trigger_kind: "unknown",
    verification_status: "unverified",
    platform_lookup: task ? "available" : "missing",
    invocation_match: conflicts.length ? "unmatched" : matched ? "matched" : "unknown",
    time_scope: run ? "platform_last_run_not_assumed_current" : "none",
    scheduled_for: time(run?.scheduled_for) ? new Date(run.scheduled_for).toISOString() : null,
    started_at: time(run?.started_at) ? new Date(run.started_at).toISOString() : null,
    identity_presence: {
      task_id: text(task?.id),
      platform_run_id: text(run?.id),
      binding_id: text(task?.thread_id) || text(task?.conversation_id),
      invocation_run_id: text(entry?.run_id),
      private_receipt_ref: text(input.platform_receipt_ref)
    },
    unknown_reasons: [...new Set(missing), "structural_checker_does_not_authenticate_platform_sources"],
    conflicts: [...new Set(conflicts)]
  };
  return {
    valid: errors.length === 0,
    authenticated: false,
    candidate_kind: candidate,
    candidate_match: matched,
    stale_latest_result: staleResult,
    errors,
    public_evidence: publicEvidence
  };
}
