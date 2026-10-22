import { validateOperationLedger } from "../scripts/operation_evidence.mjs";
export function runEvidenceTests(validate = validateOperationLedger) {
  const t0="2026-10-22T00:00:00.000Z", t1="2026-10-22T00:00:01.000Z";
  const args={query:"synthetic fixture",page:1,per_page:20};
  const fixture={evidence_origin:"synthetic",run_id:"synthetic-test",run_type:"interactive",
    scope:"bootstrap_through_data_readback",first_call_id:"s1",data_readback_call_id:"s1",first_call_ref:"fixture:result",data_readback_ref:"fixture:result",
    attempted:1,failed:0,segments:[{id:"seg1",pre:{pre_call_id:"p1",external_trace_ref:"fixture:pre",
      trace_order:1,emitted_at:null,unknown_reasons:{emitted_at:"fixture"},source_text:"SYNTHETIC SOURCE",
      source_representation:"original_nonsecret",before_attempted:0,before_failed:0,
      calls:[{id:"s1",tool:"github_search_repositories",args}]},
      post:{pre_call_id:"p1",external_trace_ref:"fixture:post",trace_order:3,emitted_at:null,unknown_reasons:{emitted_at:"fixture"},wrapper_state:"returned",
        after_attempted:1,after_failed:0,calls:[{id:"s1",tool:"github_search_repositories",args,
          evidence_origin:"synthetic",clock_source:"client_observed_utc",state:"success",dispatch_at:t0,returned_at:t1,trace_order:2,isError:false,response_ref:"fixture:result",
          request_id:null,decision_id:null,unknown_reasons:{request_id:"not supplied",decision_id:"not supplied"}}]}}]};
  const results=[];
  const check=(name,mutate,expected) => {
    const x=JSON.parse(JSON.stringify(fixture)); mutate(x);
    const r=validate(x); if(r.valid!==expected || (x.evidence_origin==="synthetic" && r.candidate_counts!==null)) throw Error(name);
    results.push({name,passed:true});
  };
  check("synthetic valid ledger never emits real candidate metrics",()=>{},true);
  check("missing external pre",x=>delete x.segments[0].pre,false);
  check("unknown dispatch timestamp",x=>x.segments[0].post.calls[0].dispatch_at=null,false);
  check("unknown return timestamp",x=>x.segments[0].post.calls[0].returned_at=null,false);
  check("uncertain call rejects complete count",x=>x.segments[0].post.calls[0].state="uncertain",false);
  check("wrapper denial rejects complete count",x=>x.segments[0].post.wrapper_state="denied",false);
  check("resolved isError true is not success",x=>x.segments[0].post.calls[0].isError=true,false);
  check("visible error counts once",x=>{Object.assign(x.segments[0].post.calls[0],{state:"error",isError:true,error_text:"SYNTHETIC 400"});x.failed=1;x.segments[0].post.after_failed=1;},true);
  check("wrapper not an extra API call",x=>x.attempted=2,false);
  check("args drift",x=>x.segments[0].post.calls[0].args.query="changed",false);
  check("missing source identity",x=>delete x.segments[0].pre.source_text,false);
  check("post before pre",x=>x.segments[0].post.trace_order=0,false);
  check("duplicate result",x=>x.segments[0].post.calls.push(x.segments[0].post.calls[0]),false);
  check("missing scope boundary",x=>delete x.data_readback_ref,false);
  check("no segments is not full run",x=>{x.segments=[];x.attempted=0;},false);
  check("nonexecution cannot be inferred",x=>{x.segments[0].post.calls[0].state="not_executed";x.attempted=0;x.segments[0].post.after_attempted=0;},false);
  check("ID absence needs reason",x=>delete x.segments[0].post.calls[0].unknown_reasons,false);
  check("unknown external emission allowed only with reason",x=>delete x.segments[0].pre.unknown_reasons,false);
  check("pre timestamp after dispatch",x=>x.segments[0].pre.emitted_at=t1,false);
  check("post timestamp before return",x=>x.segments[0].post.emitted_at=t0,false);
  check("boundary id mismatch",x=>x.first_call_id="absent",false);
  check("mixed synthetic result origin",x=>x.segments[0].post.calls[0].evidence_origin="actual",false);
  check("missing timestamp provenance",x=>delete x.segments[0].post.calls[0].clock_source,false);
  check("malformed segment fails closed",x=>x.segments[0]=null,false);
  check("malformed call fails closed",x=>x.segments[0].post.calls[0]=null,false);
  check("post time absence needs reason",x=>delete x.segments[0].post.unknown_reasons,false);
  check("not executed identity still checked",x=>{const r=x.segments[0].post.calls[0];Object.assign(r,{state:"not_executed",dispatch_at:null,returned_at:null,nonexecution_evidence_ref:"fixture:proof",nonexecution_kind:"explicit_not_dispatched",tool:"WRONG"});x.attempted=0;x.segments[0].post.after_attempted=0;},false);
  check("argument array is not named args",x=>{x.segments[0].pre.calls[0].args=[];x.segments[0].post.calls[0].args=[];},false);
  check("duplicate subcall event order",x=>{const s=x.segments[0];s.pre.calls.push({...s.pre.calls[0],id:"s2"});s.post.calls.push({...s.post.calls[0],id:"s2"});s.post.after_attempted=2;x.attempted=2;x.data_readback_call_id="s2";},false);
  {const x=JSON.parse(JSON.stringify(fixture)); x.evidence_origin="actual";x.segments[0].post.calls[0].evidence_origin="actual";
    const r=validate(x);if(!r.valid||r.authenticated!==false)throw Error("a relabeled fixture does not authenticate anything");
    results.push({name:"relabeled fixture remains unauthenticated (test only)",passed:true});}
  check("reversed temporal endpoints",x=>{const s=x.segments[0];s.post.trace_order=5;s.post.calls[0].trace_order=3;s.pre.calls.push({...s.pre.calls[0],id:"s2"});s.post.calls.push({...s.post.calls[0],id:"s2",trace_order:2,dispatch_at:t1,returned_at:t1});s.post.after_attempted=2;x.attempted=2;x.data_readback_call_id="s2";},false);
  check("overlapping dispatch rejected by serial contract",x=>{const s=x.segments[0];s.post.trace_order=5;s.pre.calls.push({...s.pre.calls[0],id:"s2"});s.post.calls.push({...s.post.calls[0],id:"s2",trace_order:3});s.post.after_attempted=2;x.attempted=2;x.data_readback_call_id="s2";},false);
  return results;
}
