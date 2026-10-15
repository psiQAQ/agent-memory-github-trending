import {legacyDestination, starsCSV, nextTheme} from './reader-core.mjs';
const base = new URL('../', import.meta.url);
function routeLegacy(hash = location.hash) {
  const destination = legacyDestination(hash);
  if (!destination) return false;
  const target = new URL(destination, base);
  if (target.href !== location.href) location.replace(target.href);
  return true;
}
routeLegacy();
window.addEventListener('hashchange', () => routeLegacy());
document.addEventListener('click', event => {
  if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  const link = event.target.closest?.('a[href^="#doc="]');
  if (link && routeLegacy(link.getAttribute('href'))) { event.preventDefault(); event.stopImmediatePropagation(); }
}, true);
const feedback = document.querySelector('#reader-feedback');
const announce = text => { if (feedback) feedback.textContent = text; };
const button = document.querySelector('#reader-theme');
let theme = 'auto';
try { const saved = localStorage.getItem('am-reader-theme'); if (['auto','light','dark'].includes(saved)) theme = saved; } catch { /* Storage may be disabled; reading still works. */ }
function applyTheme() {
  if (theme === 'auto') delete document.documentElement.dataset.theme;
  else document.documentElement.dataset.theme = theme;
  if (button) button.textContent = '主题：' + ({auto:'跟随系统',light:'浅色',dark:'深色'})[theme];
}
if (document.body.hasAttribute('data-reader')) applyTheme();
if (button) {
  button.hidden = false;
  button.addEventListener('click', () => { theme = nextTheme(theme); applyTheme(); try { localStorage.setItem('am-reader-theme', theme); } catch { /* Optional preference. */ } });
}
const article = document.querySelector('article');
const toc = document.querySelector('#reader-toc');
if (article && toc) {
  const headings = [...article.querySelectorAll('h2')].filter(node => !node.closest('details'));
  if (headings.length) {
    const label = document.createElement('strong'); label.textContent = '本页目录';
    const list = document.createElement('ol');
    headings.forEach((node, index) => {
      if (!node.id) node.id = 'section-' + (index + 1);
      const item = document.createElement('li'), link = document.createElement('a');
      link.href = '#' + encodeURIComponent(node.id); link.textContent = node.textContent;
      item.append(link); list.append(item);
    });
    toc.replaceChildren(label, list); toc.hidden = false;
  }
  const progress = document.querySelector('#reading-progress');
  if (progress) {
    progress.hidden = false;
    const update = () => {
      const start = article.getBoundingClientRect().top + scrollY;
      const distance = Math.max(1, article.offsetHeight - innerHeight + 120);
      progress.value = Math.min(100, Math.max(0, (scrollY - start + 120) / distance * 100));
    };
    let queued = false;
    const request = () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; update(); }); } };
    window.addEventListener('scroll', request, {passive:true}); window.addEventListener('resize', request); update();
  }
}
const copy = document.querySelector('#copy-link');
if (copy) {
  copy.hidden = false;
  copy.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(location.href); announce('链接已复制'); }
    catch { announce('请从地址栏复制本页链接'); }
  });
}
const exportButton = document.querySelector('#export-stars');
if (exportButton) {
  exportButton.hidden = false;
  exportButton.addEventListener('click', async () => {
    exportButton.disabled = true;
    try {
      const fetchJSON = async path => {
        const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 15000);
        try { const response = await fetch(new URL(path, base), {cache:'no-store', credentials:'omit', signal:controller.signal}); if (!response.ok) throw Error('HTTP ' + response.status); return await response.json(); }
        finally { clearTimeout(timer); }
      };
      const [registry, index] = await Promise.all([fetchJSON('data/projects.json'), fetchJSON('state/validation-index.json')]);
      const csv = starsCSV(registry, index), blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
      const url = URL.createObjectURL(blob), link = document.createElement('a');
      link.href = url; link.download = 'agent-memory-star-observations.csv'; document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000); announce('已导出索引中的真实观测点；不是连续日线');
    } catch (error) { announce('导出失败：' + error.message + '；原始 JSON 链接仍可使用'); }
    finally { exportButton.disabled = false; }
  });
}
function revealAnchor() {
  try { const target = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (!target) return; let parent = target.parentElement; while (parent) { if (parent.tagName === 'DETAILS') parent.open = true; parent = parent.parentElement; } }
  catch { /* Invalid fragment is not executable. */ }
}
window.addEventListener('hashchange', revealAnchor); revealAnchor();
