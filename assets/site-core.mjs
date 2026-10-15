// Pure presentation helpers. No network, storage, or mutation of research data.
export const REPO = 'https://github.com/psiQAQ/agent-memory-github-trending';
export const KINDS = {engineering:'工程实现', research:'研究代码', benchmark:'评测基准', reference:'历史参照'};
export const EVIDENCE = {upstream_statement:'上游说明', code_inspected:'代码静态核查', independently_reproduced:'独立复现'};
export const numeric = n => typeof n === 'number' && Number.isFinite(n);
export const ratio = (n,d) => numeric(n) && numeric(d) && n >= 0 && d > 0 ? n/d : null;
export const percent = n => numeric(n) ? `${(n*100).toFixed(1)}%` : '—';
export const number = n => numeric(n) ? n.toLocaleString('zh-CN') : '—';
export function repoPath(p) {
  return typeof p === 'string' && !/[\\%?#\u0000-\u0020]/.test(p) && !p.split('/').some(x=>x==='..'||x==='.'||!x) && /^(?:README\.md|AGENTS\.md|(?:docs|projects|reports|state|data|config)\/[\w./-]+)$/.test(p);
}
export function sourceURL(path, commit='main') {
  return repoPath(path) && /^(?:main|[a-f0-9]{40})$/.test(commit) ? `${REPO}/blob/${commit}/${path}` : REPO;
}
export function linkTarget(raw, source, allowed = new Set()) {
  try {
    if (/[\u0000-\u0020\\]/.test(raw)) return null;
    const url = new URL(raw, `https://repository.invalid/${source}`);
    if (!['https:','http:'].includes(url.protocol) || url.username || url.password) return null;
    if (url.origin !== 'https://repository.invalid') return {href:url.href, external:true};
    const path = decodeURIComponent(url.pathname.slice(1));
    if (!repoPath(path)) return null;
    if (allowed.has(path) && path.endsWith('.md')) return {href:`#doc=${encodeURIComponent(path)}${url.hash ? `&anchor=${encodeURIComponent(decodeURIComponent(url.hash.slice(1)))}`:''}`, external:false};
    return {href:sourceURL(path)+url.hash, external:true};
  } catch { return null; }
}
export function history(index, id, until=Infinity) {
  return (index.snapshots || []).flatMap(s=>s.stars || [])
    .filter(r=>r[0]===id && numeric(r[2]) && Number.isFinite(Date.parse(r[1])) && Date.parse(r[1])<=until)
    .map(r=>({at:r[1], stars:r[2]})).sort((a,b)=>Date.parse(a.at)-Date.parse(b.at));
}
export function growth(index, id, stars, at, days, toleranceHours=6) {
  if (!numeric(stars) || !Number.isFinite(Date.parse(at))) return null;
  const now=Date.parse(at), target=now-days*86400000;
  const closest=history(index,id,now-1).map(r=>({...r,distance:Math.abs(Date.parse(r.at)-target)}))
    .filter(r=>r.distance<=toleranceHours*3600000).sort((a,b)=>a.distance-b.distance)[0];
  return closest ? {net:stars-closest.stars, baseline_at:closest.at, elapsed_days:(now-Date.parse(closest.at))/86400000} : null;
}
export function coverage(batch) {
  const expected = new Set(batch.expected_repository_ids || []);
  return Object.fromEntries(['metadata','head','releases'].map(k=>{
    const ok = new Set((batch.observations || []).filter(o=>expected.has(o.repository_id)&&o[k]?.status==='ok'&&(k!=='releases'||o[k].complete===true)).map(o=>o.repository_id)).size;
    return [k,{expected:expected.size,ok,rate:ratio(ok,expected.size)}];
  }));
}
export function validateSnapshot(status,index,batch,sha=null) {
  const record=(index.snapshots || []).find(r=>r.path===status.latest_snapshot_path);
  if (!record || record.run_id!==batch.run_id || record.observed_at!==batch.observed_at || batch.run_id!==status.last_completed_run_id) throw Error('快照、运行状态和历史索引不一致，请在发布完成后刷新。');
  if (sha && record.blob_sha!==sha) throw Error('快照内容的 Git blob SHA 校验失败。');
  const expected=batch.expected_repository_ids, observations=batch.observations;
  if (!Array.isArray(expected)||!Array.isArray(observations)||expected.length!==new Set(expected).size||expected.length!==observations.length||new Set(observations.map(o=>o.repository_id)).size!==expected.length||observations.some(o=>!expected.includes(o.repository_id))) throw Error('快照项目集合不完整或存在重复。');
  return record;
}
