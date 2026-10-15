// Pure helpers shared by the static reader and its regression tests.
export function staticDocumentPath(hash) {
  const params = new URLSearchParams(String(hash).replace(/^#/, ''));
  const path = params.get('doc');
  if (!path || /[\\%?#\u0000-\u0020]/u.test(path)) return null;
  if (path.split('/').some(part => !part || part === '.' || part === '..')) return null;
  if (!/^(?:(?:docs|reports|projects|state)\/[\w./-]+|README|AGENTS)\.md$/.test(path)) return null;
  const anchor = params.get('anchor');
  return path.slice(0, -3) + '.html' + (anchor ? '#' + encodeURIComponent(anchor) : '');
}
export function legacyDestination(hash) {
  const doc = staticDocumentPath(hash);
  if (doc) return doc;
  const params = new URLSearchParams(String(hash).replace(/^#/, ''));
  const views = new Set(['overview', 'projects', 'archive', 'candidates', 'status', 'docs']);
  if (views.has(params.get('view')) || /^[1-9]\d*$/.test(params.get('project') || '')) return 'dashboard.html' + hash;
  return null;
}
export function csvCell(value) {
  let text = String(value ?? '');
  // Prevent spreadsheet formula evaluation for text values.
  if (/^\s*[=+@-]/u.test(text)) text = "'" + text;
  return '"' + text.replaceAll('"', '""') + '"';
}
export function starsCSV(registry, index) {
  if (!Array.isArray(registry?.projects) || !Array.isArray(index?.snapshots)) throw Error('项目登记或历史索引格式错误');
  const names = new Map(registry.projects.map(p => [p.repository_id, p.full_name]));
  const rows = [], seen = new Map();
  for (const snapshot of index.snapshots) {
    if (!Array.isArray(snapshot.stars)) throw Error('历史摘要缺少 stars 数组');
    for (const row of snapshot.stars) {
      if (!Array.isArray(row) || row.length !== 3) throw Error('Star 观测格式错误');
      const [id, at, stars] = row;
      if (!Number.isSafeInteger(id) || id <= 0 || typeof at !== 'string' || !at.endsWith('Z') || !Number.isFinite(Date.parse(at)) || !Number.isSafeInteger(stars) || stars < 0) throw Error('Star 观测包含无效值');
      const key = id + '/' + at;
      if (seen.has(key)) { if (seen.get(key) !== stars) throw Error('同一项目同一时刻的 Star 数冲突'); continue; }
      seen.set(key, stars);
      rows.push([id, names.get(id) || '', at, stars, snapshot.run_id || '', snapshot.path || '', snapshot.blob_sha || '']);
    }
  }
  rows.sort((a,b) => a[2].localeCompare(b[2]) || a[0] - b[0]);
  return '\uFEFF' + [['repository_id','full_name','observed_at_utc','stars','run_id','snapshot_path','snapshot_blob_sha'], ...rows].map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n';
}
export function nextTheme(theme) { return ({auto:'light', light:'dark', dark:'auto'})[theme] || 'auto'; }
