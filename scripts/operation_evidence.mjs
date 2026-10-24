// Offline/reference structural validator; never authenticates a trace or executes tools.
// Scheduled applies the same checks to visible evidence; no Node/filesystem dependency.
export function validateOperationLedger(ledger) {
  const errors = [];
  const fail = (s) => errors.push(s);
  const stamp = (s) => typeof s === "string" && /Z$/.test(s) && Number.isFinite(Date.parse(s));
  const ids = new Set();
  let attempted = 0, failed = 0, previousOrder = -1;
  const segmentIds = new Set(), eventOrders = new Set(), actualCalls = [];
  const event = n => { if (!Number.isInteger(n) || n < 0 || eventOrders.has(n)) fail("duplicate/invalid trace order"); eventOrders.add(n); };
  if (!ledger || !Array.isArray(ledger.segments)) return {valid:false, authenticated:false, errors:["segments required"], candidate_counts:null};
  if (!ledger.run_id || !["scheduled","interactive","interactive_baseline"].includes(ledger.run_type)) fail("run identity");
  if (ledger.segments.length === 0) fail("empty scope");
  if (!["actual","synthetic"].includes(ledger.evidence_origin)) fail("evidence_origin");
  if (ledger.scope !== "bootstrap_through_data_readback") fail("scope");
  if (!ledger.first_call_ref || !ledger.data_readback_ref) fail("scope boundary references");
  for (const segment of ledger.segments) {
    if (!segment || typeof segment !== "object") { fail("segment shape"); continue; }
    const pre = segment.pre, post = segment.post;
    if (!segment.id || segmentIds.has(segment.id)) fail("segment identity");
    segmentIds.add(segment.id);
    if (!pre || !post) { fail("missing external pre/post"); continue; }
    event(pre.trace_order); event(post.trace_order);
    if (!pre.external_trace_ref || !post.external_trace_ref) fail("external trace references");
    if (!Number.isInteger(pre.trace_order) || !Number.isInteger(post.trace_order) || pre.trace_order >= post.trace_order) fail("external trace ordering");
    if (!pre.pre_call_id || post.pre_call_id !== pre.pre_call_id || ids.has(pre.pre_call_id)) fail("pre/post identity");
    ids.add(pre.pre_call_id);
    if (pre.trace_order <= previousOrder) fail("cross-segment ordering");
    previousOrder = post.trace_order;
    if (!pre.source_text && !(pre.source_ref && pre.source_fingerprint)) fail("actual source identity");
    if (pre.source_representation !== "original_nonsecret" && pre.source_representation !== "redacted") fail("source representation");
    if (pre.emitted_at == null && !pre.unknown_reasons?.emitted_at) fail("missing emitted_at reason");
    if (pre.emitted_at != null && !stamp(pre.emitted_at)) fail("invalid emitted_at");
    if (post.emitted_at == null && !post.unknown_reasons?.emitted_at) fail("missing post emitted_at reason");
    if (post.emitted_at != null && !stamp(post.emitted_at)) fail("invalid post emitted_at");
    if (pre.emitted_at != null && post.emitted_at != null && Date.parse(pre.emitted_at) > Date.parse(post.emitted_at)) fail("emission order");
    if (!Array.isArray(pre.calls) || !Array.isArray(post.calls)) { fail("call manifests"); continue; }
    if (pre.calls.length < 1 || pre.calls.length > 6 || post.calls.length !== pre.calls.length) fail("bounded exact call manifest");
    if (pre.before_attempted !== attempted || pre.before_failed !== failed) fail("cumulative before");
    if (pre.calls.some(c => !c || typeof c !== "object") || post.calls.some(c => !c || typeof c !== "object")) { fail("call shape"); continue; }
    const results = new Map(post.calls.map(c => [c.id,c]));
    if (results.size !== post.calls.length) fail("duplicate result id");
    for (const call of pre.calls) {
      if (!call.id || ids.has(call.id)) fail("duplicate/missing call id");
      ids.add(call.id);
      const result = results.get(call.id);
      if (!call.tool || !call.args || typeof call.args !== "object" || Array.isArray(call.args)) fail("actual args/tool");
      if (!result) { fail("missing result"); continue; }
      event(result.trace_order);
      if (!result.response_ref || result.tool !== call.tool || JSON.stringify(result.args) !== JSON.stringify(call.args)) fail("result identity/args");
      if (!Number.isInteger(result.trace_order) || result.trace_order <= pre.trace_order || result.trace_order >= post.trace_order) fail("subcall trace ordering");
      if (result.evidence_origin !== ledger.evidence_origin) fail("mixed evidence origin");
      for (const key of ["request_id","decision_id"]) if (result[key] == null && !result.unknown_reasons?.[key]) fail("missing ID reason");
      if (result.state === "not_executed") {
        if (!result.nonexecution_evidence_ref || !["explicit_not_dispatched","cancelled_before_dispatch"].includes(result.nonexecution_kind) || result.dispatch_at != null || result.returned_at != null) fail("unproven nonexecution");
        continue;
      }
      if (!stamp(result.dispatch_at)) fail("actual dispatch timestamp");
      const previous = actualCalls.at(-1);
      if (previous && (result.trace_order <= previous.trace_order || Date.parse(result.dispatch_at) < Date.parse(previous.returned_at))) fail("serial call order");
      attempted++; actualCalls.push(result);
      if (result.clock_source !== "client_observed_utc") fail("timestamp provenance");
      if (pre.emitted_at != null && Date.parse(pre.emitted_at) > Date.parse(result.dispatch_at)) fail("pre after dispatch");
      if (post.emitted_at != null && Date.parse(post.emitted_at) < Date.parse(result.returned_at)) fail("post before return");
      if (result.state === "error") failed++;
      if (!["success","error"].includes(result.state)) fail("uncertain result");
      if (!stamp(result.returned_at) || Date.parse(result.returned_at) < Date.parse(result.dispatch_at)) fail("actual return timestamp");
      if (result.state === "success" && result.isError !== false) fail("false success");
      if (result.state === "error" && (result.isError !== true || !result.error_text)) fail("missing visible error");
    }
    if (post.after_attempted !== attempted || post.after_failed !== failed) fail("cumulative after");
    if (post.wrapper_state !== "returned") fail("wrapper incomplete");
  }
  if (!actualCalls.length || ledger.first_call_id !== actualCalls[0]?.id || ledger.data_readback_call_id !== actualCalls.at(-1)?.id ||
      ledger.first_call_ref !== actualCalls[0]?.response_ref || ledger.data_readback_ref !== actualCalls.at(-1)?.response_ref) fail("boundary identity");
  if (ledger.attempted !== attempted || ledger.failed !== failed) fail("final reconciliation");
  // Counts are only candidates: independent trace provenance/scope review remains mandatory.
  return {valid:errors.length===0, authenticated:false, errors, candidate_counts:errors.length===0 && ledger.evidence_origin==="actual"
    ? {attempted,failed,failure_rate:attempted ? failed/attempted : null} : null};
}
