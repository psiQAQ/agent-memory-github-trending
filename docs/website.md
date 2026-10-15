# 网站设计与发布

网站是原始 JSON/Markdown 的只读展示层，不负责上游研究采集、Git 提交或变更 Scheduled。编辑要求见 [项目偏好](project-preferences.md)。

## 信息架构

首页显示最新简报的三行要点，并提供生态/选型、开放数据和阅读归档；完整 Markdown 由 GitHub Pages 原生 Jekyll 生成独立 `.html`。原有 Tabler 风格仪表盘保留在 `dashboard.html`，继续提供项目筛选、真实观测曲线、候选与运行指标，不另存一套业务数据。

读者页面采用自编写布局 `_layouts/reader.html` 与 `assets/reader.css`；没有引入 React/Vue、npm 运行时库、远程字体或分析脚本。静态生成依赖 GitHub Pages 自带 Jekyll 及白名单插件，不再将“零构建”作为架构描述。

## 发布方式

发布源继续使用 main 根目录，域名为 `https://notes.psiqaq.cn/agent-memory-github-trending/`；不修改主知识库域名或路由，不新增自定义采集工作流。

这次移除根目录 `.nojekyll` 并增加 `_config.yml`，让 GitHub 的 Pages 发布阶段生成静态内容。`jekyll-optional-front-matter` 处理没有 YAML 头的 Markdown，`remove_originals: false` 保留原始 `.md` 供仪表盘和下载使用；原 JSON 是静态文件，字节不应被重写。`jekyll-relative-links` 将 Markdown 内部文档链接转为对应阅读页面；`jekyll-titles-from-headings` 提取标题。配置的 `baseurl` 适配现有项目子路径。

首页在构建时直接读取 `reports/latest.md`，展示 `## 已确认合并/发布的变更` 之前的内容。每轮只更新 Markdown，不能维护另一份容易过期的手写 HTML。`archive.html` 从已生成页面中发现 `reports/briefs/`、`reports/weekly/`、`projects/`，以后新增文件会自动进入归档；`sitemap.xml` 提供静态链接列表。

日常采集仍完全 API-native，不需要本机开机或 Scheduled 执行 Ruby/Node/Python。Jekyll 是 GitHub Pages 的发布步骤，不是第二个研究调度器。源码合并、构建成功、线上 HTTP 和浏览器验收仍应分别记录。

官方依据：[Pages 与 Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)、[发布源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)、[可选 front matter 插件](https://github.com/benbalter/jekyll-optional-front-matter)。GitHub 文档推荐可定制 Actions，但本仓库当前不需要额外框架/自定义插件，原生分支发布即可满足需求。

## 阅读增强与兼容

正文无需 JS；JS 增强目录、阅读进度、复制链接、系统/手动主题和 CSV 导出。移动端保留内容，只在宽表内滚动。长证据块使用 details/summary，默认折叠，禁用 JS 也可展开。旧 `#doc=` 链接转到独立 HTML，旧 `#view=`/`#project=` 链接转到仪表盘，既有分享链接不直接丢失。

`assets/reader-core.mjs` 实现 URL 白名单、CSV 校验/转义和主题状态；`assets/reader.js` 只调用同源只读数据。CSV 从 `state/validation-index.json` 的真实 Star 观测生成，不补齐缺失日期，也不宣称重新复核过每个原始 blob。数据与客户端交互的验证边界沿用 [数据契约](data-contract.md)。

## 安全与维护

保留 CSP，只允许本站脚本/样式；不引入第三方跟踪，不通过 URL 接收任意站点地址，不自动加载上游图片。HTML/Liquid 发布前检查来自研究材料的文本；不要将未审查的上游 HTML 或模板定界符直接贴入正文。主题可在 localStorage 禁用时使用；导出 CSV 转义引号并防止文本公式执行。

`state/` 维护文档不进入 sitemap。读者需要追溯时可打开运行页或对应原始文件，不把尚未完成的计划标为成功。历史快照和运行指标不因编辑版改造而变更。

## 开发验证

```sh
# 只用于交互式网站开发，不是 Scheduled 的依赖。
node --test tests/reader.test.mjs
node --test tests/site.test.mjs
```

第一组覆盖静态阅读配置、源内容、旧路由、安全 CSV、主题和数据口径；第二组是已有仪表盘测试。无 JS 首屏、证据折叠、移动端、主题和 TOC 另用浏览器检查。没有本地 Jekyll 环境时，不将替代 Markdown 预览称为 Jekyll 构建验收；发布后的 Pages workflow 才能确认该环境的实际构建结果。
