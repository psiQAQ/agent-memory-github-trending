import {REPO,KINDS,EVIDENCE,numeric,ratio,percent,number,repoPath,sourceURL,linkTarget,history,growth,coverage,validateSnapshot} from './site-core.mjs';
const $=s=>document.querySelector(s), app=$('#app'), base=new URL('../',import.meta.url);
const state={projects:[],candidates:null,index:null,status:null,batch:null,config:null,hashVerified:false};
const docs=[['docs/methodology.md','筛选与统计方法'],['docs/references.md','外部评测参考'],['docs/data-contract.md','数据契约'],['docs/maintenance.md','维护操作手册'],['docs/api-native-maintenance.md','API-native 维护协议'],['docs/scheduled-task-prompt.md','定时任务描述'],['docs/design.md','设计文档'],['docs/decisions.md','已批准决策'],['docs/validation.md','验证记录'],['AGENTS.md','执行规则'],['README.md','仓库介绍'],['docs/website.md','网站设计与发布']];
const allowed=new Set(docs.map(x=>x[0]).concat(['reports/latest.md','reports/current.md']));
const docCache=new Map(); let routeTicket=0,ready=false;
function el(tag,attrs={},...children){const n=document.createElement(tag);for(const [k,v] of Object.entries(attrs)){if(v===null||v===undefined)continue;if(k==='class')n.className=v;else if(k==='on')for(const [evt,fn] of Object.entries(v))n.addEventListener(evt,fn);else n.setAttribute(k,String(v));}for(const c of children.flat(Infinity)){if(c!==null&&c!==undefined)n.append(c instanceof Node?c:document.createTextNode(String(c)));}return n;}
const external=(text,href,cls='')=>el('a',{href,class:cls,target:'_blank',rel:'noopener noreferrer'},text);
const docLink=(text,path,cls='')=>el('a',{href:`#doc=${encodeURIComponent(path)}`,class:cls},text);
const badge=(text,type='')=>el('span',{class:`badge ${type}`},text);
const date=(v,full=false)=>{const d=new Date(v);return v&&Number.isFinite(d.getTime())?new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',...(full?{hour:'2-digit',minute:'2-digit',hour12:false}:{})}).format(d):'未知';};
function heading(title,subtitle,eyebrow='Agent Memory / 公开研究'){return el('div',{class:'page-head'},el('p',{class:'eyebrow'},eyebrow),el('h1',{},title),el('p',{},subtitle));}
function stat(label,value,note){return el('div',{class:'stat'},el('div',{class:'label'},label),el('div',{class:'value'},value),el('div',{class:'note'},note));}
function section(title,note,link=null){return el('div',{class:'section-title'},el('div',{},el('h2',{},title),note?el('p',{},note):null),link);}
function notify(text){$('#notice').hidden=!text;$('#notice').textContent=text;}
async function read(path,kind='json'){
  if(!repoPath(path))throw Error('文档路径不符合本站的读取规则。');
  const controller=new AbortController(), timer=setTimeout(()=>controller.abort(),15000);
  try{const r=await fetch(new URL(path,base),{cache:'no-store',credentials:'omit',signal:controller.signal});if(!r.ok)throw Error(`${path}：HTTP ${r.status}`);const bytes=new Uint8Array(await r.arrayBuffer());const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);if(kind==='bytes')return {bytes,text};if(kind==='text')return text;try{return JSON.parse(text);}catch{throw Error(`${path} 不是有效 JSON；请确认 Pages 发布的是 main 根目录。`);}}
  finally{clearTimeout(timer);}
}
async function blobSHA(bytes){if(!globalThis.crypto?.subtle)return null;const prefix=new TextEncoder().encode(`blob ${bytes.length}\0`), all=new Uint8Array(prefix.length+bytes.length);all.set(prefix);all.set(bytes,prefix.length);return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-1',all)),b=>b.toString(16).padStart(2,'0')).join('');}
async function load(){
  ready=false;app.setAttribute('aria-busy','true');$('#refresh').disabled=true;notify('');docCache.clear();
  try{
    const [registry,status,index,config]=await Promise.all([read('data/projects.json'),read('state/status.json'),read('state/validation-index.json'),read('config/tracker.json')]);
    if(!Array.isArray(registry.projects)||!Array.isArray(index.snapshots))throw Error('项目登记表或观测索引格式不正确。');
    if(!/^data\/snapshots\/\d{4}\/\d{2}\/[\w-]+\.json$/.test(status.latest_snapshot_path||''))throw Error('尚无有效的已验证快照路径。');
    const raw=await read(status.latest_snapshot_path,'bytes'), batch=JSON.parse(raw.text), sha=await blobSHA(raw.bytes);
    validateSnapshot(status,index,batch,sha);
    if(!/^[a-f0-9]{40}$/.test(status.last_verified_data_commit_sha||''))throw Error('缺少可追溯的数据提交 SHA。');
    Object.assign(state,{projects:registry.projects,status,index,batch,config,hashVerified:!!sha});
    for(const p of state.projects)if(repoPath(p.card))allowed.add(p.card);
    for(const w of status.weekly_reports?.closed_weeks_published||[])if(/^\d{4}-W\d{2}$/.test(w))allowed.add(`reports/weekly/${w}.md`);
    try{const c=await read('data/candidates.json');if(!Array.isArray(c.candidates))throw Error('候选格式错误');state.candidates=c.candidates;}catch{state.candidates=null;notify('待审候选暂时无法读取；项目观测仍可浏览，候选数量不作推测。');}
    const age=(Date.now()-Date.parse(batch.observed_at))/3600000;
    if(age>48)notify(`当前展示的是 ${date(batch.observed_at,true)} 的历史观测，已超过 48 小时；不代表上游实时状态。`);
    if(age<-.1)notify('快照时间晚于当前浏览器时间，请核对设备时钟与原始数据时间。');
    if(!sha)notify('当前浏览器无法执行 SHA-1；已核对快照身份，但未在浏览器复核内容哈希。');
    ready=true;await route();
  }catch(error){app.replaceChildren(el('section',{class:'card error'},el('p',{class:'eyebrow'},'数据加载失败'),el('h1',{},'暂时无法加载研究数据'),el('p',{},error.name==='AbortError'?'数据请求超时，请稍后重新加载数据。读取失败不代表项目数或观测值为零。':error.message),el('div',{class:'hero-actions'},el('button',{class:'button primary',on:{click:load}},'重新加载数据'),external('在 GitHub 阅读观测表 ↗',sourceURL('reports/current.md'),'button'))));}
  finally{app.setAttribute('aria-busy','false');$('#refresh').disabled=false;}
}
function observation(p){return state.batch.observations.find(o=>o.repository_id===p.repository_id);}
function starValue(p){const o=observation(p);if(o?.metadata?.status==='ok'&&numeric(o.metadata.value?.stars))return {stars:o.metadata.value.stars,at:o.metadata.observed_at,fresh:true};const previous=history(state.index,p.repository_id,Date.parse(state.batch.observed_at)).at(-1);return {stars:previous?.stars??null,at:previous?.at??null,fresh:false};}
function delta(p,days){const v=starValue(p);return v.fresh?growth(state.index,p.repository_id,v.stars,v.at,days,state.config.settings?.baseline_tolerance_hours??6):null;}
function projectBrowser(compact=false){
  const card=el('section',{class:'card'}),content=el('div',{class:'table-wrap'}),count=el('span',{class:'muted'}),search=el('input',{class:'search',type:'search',placeholder:'输入项目名称、记忆机制或标签', 'aria-label':'搜索项目'}),sort=el('select',{'aria-label':'项目排序'},el('option',{value:'stars'},'Star 数'),el('option',{value:'name'},'名称'),el('option',{value:'new'},'发现时间'));
  let kind='engineering';const tabs=el('div',{class:'tabs','aria-label':'项目类别'});
  const buttons=Object.entries(KINDS).map(([key,label])=>{const b=el('button',{class:`tab${key===kind?' selected':''}`,'aria-pressed':key===kind,on:{click:()=>{kind=key;for(const x of buttons){x.node.classList.toggle('selected',x.key===kind);x.node.setAttribute('aria-pressed',String(x.key===kind));}draw();}}},label);tabs.append(b);return {key,node:b};});
  function draw(){
    const q=search.value.trim().toLowerCase();let rows=state.projects.filter(p=>p.kind===kind&&[p.full_name,p.summary,...(p.tags||[])].join(' ').toLowerCase().includes(q));
    rows.sort((a,b)=>sort.value==='name'?a.full_name.localeCompare(b.full_name):sort.value==='new'?Date.parse(b.first_discovered_at)-Date.parse(a.first_discovered_at):(starValue(b).stars??-1)-(starValue(a).stars??-1));count.textContent=`${rows.length} 个项目${compact&&rows.length>6?' · 展示前 6 个':''}`;if(compact)rows=rows.slice(0,6);
    if(!rows.length){content.replaceChildren(el('div',{class:'empty'},'当前类别没有匹配项目。请缩短搜索词或切换类别。'));return;}
    const table=el('table',{class:'project-table'},el('thead',{},el('tr',{},['项目','记忆机制 / 定位','Stars','7 日净变化','30 日净变化','证据'].map(t=>el('th',{scope:'col'},t))))),body=el('tbody');
    for(const p of rows){const v=starValue(p),parts=p.full_name.split('/'),name=parts.slice(1).join('/');const diff=d=>{const g=delta(p,d);return el('td',{class:'numeric','data-label':`${d} 日净变化`,title:g?`基线 ${date(g.baseline_at,true)}；实际间隔 ${g.elapsed_days.toFixed(2)} 天`:'目标日期前后 6 小时内无真实可比观测'},g?`${g.net>0?'+':''}${number(g.net)}`:'—');};
      body.append(el('tr',{},el('td',{class:'project-title-cell'},el('div',{class:'project-cell'},el('span',{class:'avatar','aria-hidden':'true'},name.slice(0,2).toUpperCase()),el('div',{},el('a',{class:'project-name',href:`#project=${p.repository_id}`},name),el('div',{class:'owner'},parts[0])))),el('td',{class:'summary-cell'},p.summary||'尚无机制摘要',el('div',{},(p.tags||[]).slice(0,2).map(t=>el('span',{class:'tag'},t)))),el('td',{class:'numeric','data-label':'Stars'},number(v.stars),!v.fresh?el('div',{},badge('历史值','warn')):null),diff(7),diff(30),el('td',{class:'evidence-cell'},badge(EVIDENCE[p.evidence_level]||'未评估','neutral'))));}
    table.append(body);content.replaceChildren(table);
  }
  search.addEventListener('input',draw);sort.addEventListener('change',draw);
  card.append(el('div',{class:'filters'},tabs,el('div',{class:'filter-group'},el('label',{class:'field'},'搜索',search),el('label',{class:'field'},'排序',sort))),content,el('div',{class:'table-note'},count,' · 排序只比较当前类别；Star 表示关注度。缺少可比基线时显示 —。'));draw();return card;
}
function overview(){
  const cov=coverage(state.batch),tracked=state.projects.filter(p=>p.status==='tracked').length;
  const hero=el('section',{class:'hero'},el('div',{},el('p',{class:'eyebrow'},'开源 Agent 记忆 / 观测总览'),el('h1',{},'追踪 Agent Memory，',el('br'),el('span',{},'查看变化，核对证据。')),el('p',{class:'description'},'先阅读影响选型和接入的技术变化，再按类别检索项目、比较真实 Star 区间，并查看对应的一手证据。'),el('div',{class:'hero-actions'},docLink('阅读最新研究简报 →','reports/latest.md','button primary'),el('a',{class:'button',href:'#view=projects'},'检索全部项目')),el('p',{class:'owner'},`最近观测 ${date(state.batch.observed_at,true)}（北京时间） · ${state.batch.run_type==='scheduled'?'定时批次':'手动批次'}`)),el('aside',{class:'field-note'},el('span',{class:'tiny-label'},'研究原则 / 01'),el('h2',{},'从一手来源核对结论。'),el('p',{},'结论对应一手来源，比较采用真实时间。',el('br'),'缺失数据不补造，未审查候选不推荐。'),el('div',{class:'pipeline'},el('span',{},'发现'),el('span',{},'→'),el('span',{},'核查'),el('span',{},'→'),el('span',{},'记录'))));
  const stats=el('section',{class:'stats','aria-label':'观察规模'},stat('正式跟踪',number(tracked),'工程、研究与评测分别呈现'),stat('待审候选',state.candidates?number(state.candidates.length):'—','搜索线索，不代表推荐'),stat('历史快照',number(state.index.snapshots.length),'按实际观测留存，不补齐空白'),stat('Release 增量覆盖',`${cov.releases.ok}/${cov.releases.expected}`,'只表示本轮增量，不代表全部历史发布'));
  const method=el('section',{class:'card pad'},el('p',{class:'eyebrow'},'核对证据'),el('h2',{},'分别看关注度、技术变化和采集状态'),[['01','关注度','用真实观测比较 Star 变化，不把缺失窗口外推成增长。'],['02','实质进展','区分上游声明、代码核查、已发布与已合并未发布。'],['03','运行透明','采集覆盖、数据提交与未知指标都保留原始状态。']].map(([n,t,d])=>el('div',{class:'line-item'},el('span',{class:'step'},n),el('div',{},el('strong',{},t),el('p',{},d)))));
  const report=el('section',{class:'card pad'},el('p',{class:'eyebrow'},'研究记录'),el('h2',{},'从报告核对变化与证据'),el('p',{},'简报、项目卡和周报来自仓库 Markdown。阅读技术判断时，可沿原始链接核对来源及尚未验证的内容。'),el('div',{class:'line-item'},docLink('最新研究简报 ↗','reports/latest.md')),el('div',{class:'line-item'},docLink('本轮完整观测与覆盖 ↗','reports/current.md')),el('div',{class:'line-item'},el('a',{href:'#view=archive'},'周报与历史快照 ↗')));
  return [hero,stats,section('项目检索','按类别查找项目，分别比较关注度与技术证据。',el('a',{href:'#view=projects'},'查看全部项目 →')),projectBrowser(true),section('核对证据与获取完整记录'),el('div',{class:'split'},method,report)];
}
function coveragePanel(){const cov=coverage(state.batch);return el('section',{class:'card pad'},el('h2',{},'本轮来源覆盖'),Object.entries(cov).map(([k,v])=>el('div',{class:'coverage-row'},el('div',{class:'coverage-top'},el('span',{},k==='metadata'?'仓库元数据':k==='head'?'默认分支 HEAD':'完整 Release 增量'),el('span',{},`${v.ok}/${v.expected} · ${percent(v.rate)}`)),el('meter',{class:'meter',min:0,max:1,value:v.rate??0,'aria-label':`${k} ${v.ok}/${v.expected}`}))),el('p',{},'按本轮预期项目计算；Release 只有 status=ok 且 complete=true 才计成功。'));
}
function runStatus(){
  const s=state.status,m=s.latest_run_metrics,api=m?.api,dr=m?.deep_review,rb=m?.data_readback;
  const metricCards=el('div',{class:'stats'},stat('API 调用数',api?.instrumentation_complete?number(api.attempted):'—','仅可观测 GitHub 连接器调用'),stat('API 失败率',api?.instrumentation_complete?percent(api.failure_rate):'—','调用记录不完整时不显示估计值'),stat('深读完成率',dr?percent(ratio(dr.completed,dr.due)):'—',dr?`${number(dr.completed)} / ${number(dr.due)} 个计划审查项`:'暂无可核实的运行指标'),stat('数据回读',rb?.status==='passed'?'已通过':'—',rb?`${number(rb.verified_paths)} / ${number(rb.expected_paths)} 个变更文件`:'尚无数据回读验证结果'));
  const details=el('dl',{class:'definition'});for(const [label,value] of [['Run ID',state.batch.run_id],['运行类型',state.batch.run_type],['观测时间',`${date(state.batch.observed_at,true)}（北京时间）`],['Data commit',external(s.last_verified_data_commit_sha,`${REPO}/commit/${s.last_verified_data_commit_sha}`)],['浏览器复核',state.hashVerified?'快照 Git blob SHA 匹配索引':'未执行内容 SHA 校验']])details.append(el('dt',{},label),el('dd',{class:label.includes('ID')||label.includes('commit')?'mono':''},value));
  const schedule=el('section',{class:'card pad'},el('h2',{},'仓库记录的调度状态'),el('p',{},`仓库保存的状态：${s.scheduler?.current_state||'未记录'}；记录时间 ${date(s.scheduler?.status_checked_at,true)}。这不是对 ChatGPT 平台的实时查询。`),el('p',{},`API-native 定时验收：${s.api_native_scheduled_end_to_end_verification?.status||'未记录'}。手动更新不等于无人值守执行通过。`),docLink('查看执行与回执协议 →','docs/api-native-maintenance.md'));
  return [heading('运行与指标','分别查看来源采集、数据发布和回读验证的结果。','运行状态 / 来源覆盖'),!m?el('div',{class:'notice'},'最小指标协议已配置，但尚无本轮指标记录。API 次数、失败率和深读完成率保持未知，不显示为 0。'):el('p',{class:'muted'},`指标批次：${m.run_id||'未知'}；口径截至 Data 完整回读，不含 Receipt 写入与回读。`,m.path&&repoPath(m.path)?external(' 查看历史指标 ↗',sourceURL(m.path)):null),metricCards,el('div',{class:'split'},el('section',{class:'card pad'},el('h2',{},'可追溯的当前数据'),details),coveragePanel()),section('自动化与剩余工作'),el('div',{class:'split'},schedule,el('section',{class:'card pad'},el('h2',{},'尚未完成的工作'),el('p',{},`仓库当前保存 ${number(s.pending_work?.length??0)} 项待办；包含未完成深读和 结构化事件回填，不等同于本轮故障数。`),external('查看完整状态 JSON ↗',sourceURL('state/status.json'),'button')))];
}
function archive(){
  const weeks=(state.status.weekly_reports?.closed_weeks_published||[]).filter(w=>/^\d{4}-W\d{2}$/.test(w)).sort().reverse();
  const cards=el('div',{class:'grid'},weeks.map(w=>el('section',{class:'card pad'},el('p',{class:'eyebrow'},'周度观测'),el('h2',{},w),el('p',{},state.status.weekly_reports?.coverage_gaps?.includes(w)?'包含观测空缺；请阅读周报的覆盖说明。':'按报告原文核对观察时间与证据。'),docLink('阅读周报 →',`reports/weekly/${w}.md`,'button'))));
  const table=el('table',{},el('thead',{},el('tr',{},['观测时间（北京时间）','批次','元数据采集成功数','原始记录'].map(t=>el('th',{scope:'col'},t)))),el('tbody',{},[...state.index.snapshots].sort((a,b)=>Date.parse(b.observed_at)-Date.parse(a.observed_at)).map(r=>el('tr',{},el('td',{class:'numeric'},date(r.observed_at,true)),el('td',{class:'mono'},r.run_id),el('td',{class:'numeric'},number(r.coverage?.metadata)),el('td',{},external('JSON ↗',sourceURL(r.path)))))));
  return [heading('周报与快照','历史记录只追加。没有观测的日期保持空白，不补造连续时间线。','历史归档 / 版本记录'),section('研究周报'),weeks.length?cards:el('div',{class:'empty'},'尚无已发布周报。'),section('不可变观测快照',`${state.index.snapshots.length} 份历史观测；这里不将索引中的 Release 计数当作完整分页证明。`),el('section',{class:'card table-wrap'},table)];
}
function candidates(){
  const root=el('div'),search=el('input',{class:'search',type:'search',placeholder:'搜索候选名称或说明','aria-label':'搜索候选'}),grid=el('div',{class:'grid'}),counter=el('span',{class:'muted'});
  function draw(){const q=search.value.toLowerCase();const list=(state.candidates||[]).filter(c=>[c.full_name,c.preliminary_review?.claim].join(' ').toLowerCase().includes(q));counter.textContent=`${list.length} 条线索`;grid.replaceChildren(...list.map(c=>el('section',{class:'card pad candidate'},badge('待审线索','warn'),el('h2',{},c.full_name),el('p',{},c.preliminary_review?.claim||'尚未完成机制、实现和评测边界审查。'),el('p',{class:'owner'},`首次发现 ${date(c.first_discovered_at)}`),external('上游仓库 ↗',`https://github.com/${c.full_name.split('/').map(encodeURIComponent).join('/')}`,'button small'))));if(!list.length)grid.append(el('p',{class:'empty'},'没有匹配的候选，请调整搜索词。'));}
  root.append(heading('待审候选','这些项目尚未完成机制、实现和评测边界审查。搜索命中不代表推荐，也不会自动进入正式跟踪。','项目发现 / 尚未推荐'));
  if(state.candidates===null){root.append(el('div',{class:'notice'},'候选文件加载失败，当前无法确认候选数量。'));return root;}
  root.append(el('div',{class:'filters'},el('label',{class:'field'},'筛选',search),counter),grid);search.addEventListener('input',draw);draw();return root;
}
function inline(text,parent,path){
  const tokens=/(`[^`\n]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*|!?\[[^\]\n]+\]\([^\s)]+\))/g;let last=0;
  for(const m of text.matchAll(tokens)){parent.append(document.createTextNode(text.slice(last,m.index)));const t=m[0];if(t.startsWith('`'))parent.append(el('code',{},t.slice(1,-1)));else if(t.startsWith('**'))parent.append(el('strong',{},t.slice(2,-2)));else if(t.startsWith('*'))parent.append(el('em',{},t.slice(1,-1)));else{const parts=t.match(/^!?\[([^\]]+)\]\((.+)\)$/),target=linkTarget(parts[2],path,allowed);if(target){const a=el('a',{href:target.href,...(target.external?{target:'_blank',rel:'noopener noreferrer'}:{})},(t.startsWith('!')?'[图片] ':'')+parts[1]);parent.append(a);}else parent.append(document.createTextNode(t));}last=m.index+t.length;}
  parent.append(document.createTextNode(text.slice(last)));
}
function markdown(text,path){
  const article=el('article',{class:'card document'}),toc=el('aside',{class:'toc','aria-label':'文章目录'},el('strong',{},'本页目录')),lines=text.replace(/\r\n/g,'\n').split('\n'),slugs=new Map();let i=0;
  const appendText=(tag,line,attrs={})=>{const n=el(tag,attrs);inline(line,n,path);article.append(n);return n;};
  while(i<lines.length){const line=lines[i];if(!line.trim()){i++;continue;}
    if(/^\s*```/.test(line)){const code=[];i++;while(i<lines.length&&!/^\s*```/.test(lines[i]))code.push(lines[i++]);i++;article.append(el('pre',{},el('code',{},code.join('\n'))));continue;}
    const h=line.match(/^(#{1,6})\s+(.+)$/);if(h){const rawSlug=h[2].toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu,'').trim().replace(/\s+/g,'-')||'section',n=slugs.get(rawSlug)||0;slugs.set(rawSlug,n+1);const id=rawSlug+(n?`-${n}`:'');appendText(`h${h[1].length}`,h[2],{id});if(h[1].length<=3)toc.append(el('a',{href:`#doc=${encodeURIComponent(path)}&anchor=${encodeURIComponent(id)}`},h[2]));i++;continue;}
    if(/^\s*([-*_])(?:\s*\1){2,}\s*$/.test(line)){article.append(el('hr'));i++;continue;}
    if(line.includes('|')&&i+1<lines.length&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1])){const cells=s=>s.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(x=>x.trim());const table=el('table'),thead=el('thead'),row=el('tr');for(const x of cells(line)){const th=el('th',{scope:'col'});inline(x,th,path);row.append(th);}thead.append(row);table.append(thead);i+=2;const body=el('tbody');while(i<lines.length&&lines[i].includes('|')&&lines[i].trim()){const tr=el('tr');for(const x of cells(lines[i++])){const td=el('td');inline(x,td,path);tr.append(td);}body.append(tr);}table.append(body);article.append(el('div',{class:'table-wrap'},table));continue;}
    const list=line.match(/^\s*(?:([-*+])|(\d+)\.)\s+(.+)$/);if(list){const ordered=!!list[2],ul=el(ordered?'ol':'ul',ordered?{start:list[2]}:{});while(i<lines.length){const x=lines[i].match(/^\s*(?:([-*+])|(\d+)\.)\s+(.+)$/);if(!x||!!x[2]!==ordered)break;const li=el('li');inline(x[3],li,path);ul.append(li);i++;}article.append(ul);continue;}
    if(/^>\s?/.test(line)){const quote=[];while(i<lines.length&&/^>\s?/.test(lines[i]))quote.push(lines[i++].replace(/^>\s?/,''));appendText('blockquote',quote.join('\n'));continue;}
    const para=[line];i++;while(i<lines.length&&lines[i].trim()&&!/^\s*(?:#{1,6}\s|```|>|[-*+]\s|\d+\.\s|\|)/.test(lines[i])){if(i+1<lines.length&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1]))break;para.push(lines[i++]);}appendText('p',para.join('\n'));
  }
  return {article,toc};
}
async function documentView(path,ticket,anchor=''){
  if(!allowed.has(path))return el('section',{class:'card error'},el('h1',{},'文档不在本站索引中'),el('p',{},'请从项目卡、周报或维护文档入口访问；本站只读取已登记的文档路径。'));
  if(!docCache.has(path))docCache.set(path,read(path,'text').catch(e=>{docCache.delete(path);throw e;}));
  const text=await docCache.get(path);if(ticket!==routeTicket)return null;
  const {article,toc}=markdown(text,path),wrap=el('div');wrap.append(el('div',{class:'doc-toolbar'},el('a',{class:'button small',href:'#view=docs'},'文档目录'),external('在 GitHub 查看原文 ↗',sourceURL(path),'button small')));
  if(path.startsWith('reports/'))wrap.append(el('p',{class:'muted'},'以下保留报告原文与证据链接。报告生成时间可能早于最新数据快照，请以正文标注为准。'));
  wrap.append(el('div',{class:'doc-layout'},article,toc));if(anchor)setTimeout(()=>document.getElementById(anchor)?.scrollIntoView(),0);return wrap;
}
function sparkline(p){
  const rows=history(state.index,p.repository_id,Date.parse(state.batch.observed_at)),box=el('section',{class:'card pad'},el('h2',{},'Star 历史观测'));
  if(rows.length<2){box.append(el('p',{},'至少需要两次真实观测才绘制趋势。'));return box;}
  const NS='http://www.w3.org/2000/svg',svg=(tag,a,text)=>{const n=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(a))n.setAttribute(k,v);if(text)n.textContent=text;return n;};
  const chart=svg('svg',{viewBox:'0 0 720 190',class:'chart',role:'img','aria-label':`${p.full_name} 的 ${rows.length} 次真实 Star 观测`}),start=Date.parse(rows[0].at),end=Date.parse(rows.at(-1).at),lo=Math.min(...rows.map(r=>r.stars)),hi=Math.max(...rows.map(r=>r.stars));
  const xy=r=>[55+(Date.parse(r.at)-start)/(end-start||1)*635,145-(r.stars-lo)/(hi-lo||1)*110];
  chart.append(svg('line',{x1:55,x2:690,y1:145,y2:145}),svg('line',{x1:55,x2:690,y1:35,y2:35}),svg('text',{x:0,y:149},number(lo)),svg('text',{x:0,y:39},number(hi)),svg('text',{x:55,y:180},date(rows[0].at)),svg('text',{x:605,y:180},date(rows.at(-1).at)),svg('path',{d:rows.map((r,i)=>`${i?'L':'M'}${xy(r).join(' ')}`).join(' ')}));
  for(const r of rows){const[x,y]=xy(r),dot=svg('circle',{cx:x,cy:y,r:4});dot.append(svg('title',{},`${date(r.at,true)}：${number(r.stars)} Stars`));chart.append(dot);}box.append(chart,el('p',{class:'chart-note'},'横轴为真实时间；折线连接已取得的观测点，跨空白区间不代表连续采集或插值。'));
  const details=el('details',{},el('summary',{},'展开 Star 观测数据表')),table=el('table',{},el('thead',{},el('tr',{},el('th',{scope:'col'},'时间'),el('th',{scope:'col'},'Stars'))),el('tbody',{},rows.map(r=>el('tr',{},el('td',{},date(r.at,true)),el('td',{},number(r.stars))))));details.append(table);box.append(details);return box;
}
async function route(){
  if(!ready)return;const ticket=++routeTicket,p=new URLSearchParams(location.hash.slice(1));if(location.hash==='#main'){$('#main').focus();return;}
  const view=p.get('view')||'overview',doc=p.get('doc'),id=p.get('project');let content,title,nav=view;
  app.setAttribute('aria-busy','true');
  try{
    if(doc){title=docs.find(d=>d[0]===doc)?.[1]||(doc==='reports/latest.md'?'最新简报':'文档阅读');nav=doc==='reports/latest.md'?'brief':doc==='docs/methodology.md'?'method':doc==='docs/references.md'?'references':'docs';content=await documentView(doc,ticket,p.get('anchor')||'');}
    else if(id){const project=state.projects.find(x=>String(x.repository_id)===id);if(!project)throw Error('未找到这个项目，请从项目检索重新进入。');title=project.full_name;nav='projects';const v=starValue(project);const md=await documentView(project.card,ticket);content=[heading(project.full_name,`${KINDS[project.kind]||project.kind} · ${number(v.stars)} Stars · ${EVIDENCE[project.evidence_level]||'证据待评估'}`,'项目 / 证据卡'),sparkline(project),section('项目卡片','以下为仓库中的完整项目卡。请结合记录版本和证据等级阅读，Star 变化不代表实现质量。'),md];}
    else if(view==='projects'){title='项目检索';content=[heading('项目检索','先选择工程实现、研究代码、评测基准或历史参照，再按名称、机制或标签搜索。','项目 / 分类检索'),projectBrowser()];}
    else if(view==='status'){title='运行与指标';content=runStatus();}
    else if(view==='archive'){title='周报与快照';content=archive();}
    else if(view==='candidates'){title='待审候选';content=candidates();}
    else if(view==='docs'){title='维护文档';content=[heading('方法与维护文档','了解研究结论的形成方式，并查阅采集、校验、发布与恢复协议。','文档 / 方法与维护'),el('div',{class:'grid'},docs.map(([path,label])=>el('section',{class:'card pad'},el('h2',{},label),el('p',{class:'mono'},path),docLink('阅读文档 →',path,'button small'))))];}
    else{title='观察总览';nav='overview';content=overview();}
    if(ticket!==routeTicket)return;app.replaceChildren(...[content].flat(Infinity).filter(Boolean));$('#crumb').textContent=title;document.title=`${title} · Agent Memory Observatory`;
    for(const n of document.querySelectorAll('[data-nav]')){const active=n.dataset.nav===nav;n.classList.toggle('active',active);active?n.setAttribute('aria-current','page'):n.removeAttribute('aria-current');}
  }catch(error){if(ticket!==routeTicket)return;app.replaceChildren(el('section',{class:'card error'},el('h1',{},'暂时无法显示此页面'),el('p',{},error.message),el('a',{class:'button',href:'#view=overview'},'返回观察总览')));}
  finally{if(ticket===routeTicket)app.setAttribute('aria-busy','false');}
}
try{const saved=localStorage.getItem('am-theme');if(saved==='dark'||saved==='light')document.documentElement.dataset.theme=saved;else if(matchMedia('(prefers-color-scheme: dark)').matches)document.documentElement.dataset.theme='dark';}catch{}
$('#theme').addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=value;try{localStorage.setItem('am-theme',value);}catch{}});
$('#menu').addEventListener('click',()=>{const open=$('#sidebar').classList.toggle('open');$('#menu').setAttribute('aria-expanded',String(open));});
window.addEventListener('hashchange',()=>{$('#sidebar').classList.remove('open');$('#menu').setAttribute('aria-expanded','false');route();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){$('#sidebar').classList.remove('open');$('#menu').setAttribute('aria-expanded','false');}});
$('#refresh').addEventListener('click',load);load();
