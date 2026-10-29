# 网站设计与发布

本站用于阅读原始 JSON/Markdown：从首页看最新要点，在仪表盘检索项目与观测，再沿正文链接核对证据。网站只展示内容，不负责上游研究采集、Git 提交或变更 Scheduled。编辑要求见[项目偏好](project-preferences.md)。

## 信息架构

首页展示最新简报的三行要点，并提供生态/选型、开放数据和阅读归档入口。GitHub Pages 原生 Jekyll 将完整 Markdown 生成为独立 `.html` 阅读页。

Tabler 风格的交互式仪表盘保留在 `dashboard.html`，提供项目筛选、真实观测曲线、候选与运行指标；这些页面共用仓库数据，不另存一套业务数据。

读者页面采用自编写布局 `_layouts/reader.html` 与 `assets/reader.css`；没有引入 React/Vue、npm 运行时库、远程字体或分析脚本。静态生成依赖 GitHub Pages 自带 Jekyll 及白名单插件，不再将“零构建”作为架构描述。

## 阅读增强与兼容

阅读正文不需要 JS；目录、阅读进度、复制链接、系统/手动主题和 CSV 导出由 JS 增强。移动端保留完整内容，宽表仅在表内横向滚动。

长证据块采用 details/summary，默认折叠；即使禁用 JS，仍可展开。旧 `#doc=` 链接转到独立 HTML，旧 `#view=`/`#project=` 链接转到仪表盘，既有分享链接不直接丢失。

`assets/reader-core.mjs` 实现 URL 白名单、CSV 校验/转义和主题状态；`assets/reader.js` 只调用同源只读数据。CSV 从 `state/validation-index.json` 的真实 Star 观测生成，不补齐缺失日期，也不宣称重新复核过每个原始 blob。数据与客户端交互的验证边界沿用 [数据契约](data-contract.md)。

## 发布方式

发布源继续使用 main 根目录，域名为 `https://notes.psiqaq.cn/agent-memory-github-trending/`；不修改主知识库域名或路由，不新增自定义采集工作流。

网站改造已移除根目录 `.nojekyll`，并增加 `_config.yml`，由 GitHub Pages 在发布阶段生成静态内容。`jekyll-optional-front-matter` 处理没有 YAML 头的 Markdown，`remove_originals: false` 保留原始 `.md` 供仪表盘和下载使用；原 JSON 是静态文件，字节不应被重写。`jekyll-relative-links` 将 Markdown 内部文档链接转为对应阅读页面；`jekyll-titles-from-headings` 提取标题。配置的 `baseurl` 适配现有项目子路径。

首页在构建时直接读取 `reports/latest.md`，展示 `## 已确认合并/发布的变更` 之前的内容。每轮只更新 Markdown，不能维护另一份容易过期的手写 HTML。`archive.html` 从已生成页面中发现 `reports/briefs/`、`reports/weekly/`、`projects/`，以后新增文件会自动进入归档；`sitemap.xml` 提供静态链接列表。

日常采集的运行方式由 config/tracker.json 与 config/local-runtime.json 的授权配置共同选择；激活 local_git 时，须保持本机开机、联网且桌面应用运行，并遵守[本地 Git 维护协议](local-maintenance.md)。原 API-native 协议保留。Jekyll 继续由 GitHub Pages 在发布端运行，不要求本地任务安装或执行 Ruby/Jekyll。源码推送、Data/Receipt 逐 blob 回读、Pages 构建与部署、线上网页内容须分别验收；具体要求见本地协议的“发布后网页验收”。

官方依据：[Pages 与 Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)、[发布源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[可选 front matter 插件](https://github.com/benbalter/jekyll-optional-front-matter)。GitHub 文档推荐可定制 Actions，但本仓库当前不需要额外框架/自定义插件，原生分支发布即可满足需求。

## 安全与维护

保留 CSP，只允许本站脚本/样式；不引入第三方跟踪，不通过 URL 接收任意站点地址，不自动加载上游图片。HTML/Liquid 发布前检查来自研究材料的文本；不要将未审查的上游 HTML 或模板定界符直接贴入正文。主题可在 localStorage 禁用时使用；导出 CSV 转义引号并防止文本公式执行。

`state/` 维护文档不进入 sitemap。需要追溯时，可查看运行页或对应原始文件。尚未完成的计划不能标为成功；文字或阅读界面的改造也不能改变历史快照和运行指标。

## 开发验证

```sh
# 只用于交互式网站开发，不是 Scheduled 的依赖。
node --test tests/reader.test.mjs
node --test tests/site.test.mjs
```

第一组覆盖静态阅读配置、源内容、旧路由、安全 CSV、主题和数据口径；第二组是已有仪表盘测试。无 JS 首屏、证据折叠、移动端、主题和 TOC 另用浏览器检查。没有本地 Jekyll 环境时，不将替代 Markdown 预览称为 Jekyll 构建验收；发布后的 Pages workflow 才能确认该环境的实际构建结果。

## 统一视觉系统（2026-10-16）

原 Dashboard 是全站视觉基准：深色固定侧栏、统一顶部面包屑、浅灰页面底色、青绿色交互色、白色细边框卡片和相同的深色模式。`_layouts/reader.html` 复用 Dashboard 的 `sidebar`、`shell`、`topbar`、`footer` 结构；`assets/site.css` 提供全站唯一视觉变量与共享布局，`assets/reader.css` 保留正文排版，`assets/reader-unified.css` 仅覆盖静态阅读页和首页的局部布局。移动端侧栏使用与 Dashboard 一致的菜单开关。

首页按 Dashboard 风格分为主题 Hero、深色研究原则卡、简报卡、选型分类卡和延伸阅读卡。文章页沿用相同外壳，并提供目录、阅读进度与复制链接。JS 关闭时仍能读取全部静态正文、真实 `<a href>` 导航和原生 `<details>`，JS 只负责增强。主题状态与 Dashboard 共用 `localStorage.am-theme`，且跟随同一系统深色默认；无存储权限时回退到系统偏好。
