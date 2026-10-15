# 网站设计与发布

这是 Agent Memory 观察仓库的只读可视化前端；原始 JSON、Markdown、历史快照及维护协议仍是唯一内容来源。前端不参与采集、发布 Git commit 或更改 Scheduled。

## 模板选型

| 方案 | 与本仓库的匹配程度 | 取舍 |
| --- | --- | --- |
| [Tabler](https://tabler.io/admin-template) | 数据总览、分类表格、指标与状态视图高度匹配 | 采用其仪表盘信息架构作为设计参考 |
| [Just the Docs](https://just-the-docs.com/) | Markdown 文档和目录阅读匹配 | 单独使用时不足以承载项目筛选与指标展示 |
| [VitePress](https://vitepress.dev/guide/deploy) | 文档阅读与可定制首页匹配 | 需要 Node 依赖及构建；当前规模没有必要 |

最终实现是 **Tabler 风格的信息架构 + 自编写的零依赖静态前端**，不是 Tabler 的 fork，也没有复制或捆绑第三方模板代码。没有运行时 CDN、npm 包、远程字体或分析脚本。中文阅读、浅色/深色模式、移动端项目卡片均由本仓库 CSS 实现。

## 页面与数据

- 总览：项目规模、候选数、快照数、Release 增量覆盖及分类项目预览。
- 项目雷达：按工程/研究/评测/历史参照分组，搜索名称、机制和标签；按 Star、名称或首次发现时间排序。不同类别不混排为质量榜单。
- 项目详情：完整项目卡 Markdown、一手来源链接、真实时间轴的 Star 观测点和可访问的数据表。
- 研究简报、周报及维护文档：直接读取原 Markdown，保留事实限定与链接，不另存一套报告。
- 周报与快照归档：周报来自 `state/status.json.weekly_reports.closed_weeks_published`，快照来自 `state/validation-index.json`；不会把没有观测的日期补成连续数据。
- 候选队列：读取 `data/candidates.json`，明确标注未审查，不自动推荐或晋升。
- 运行指标：读取 `state/status.json.latest_run_metrics`，展示可观测 API 调用、API 失败率、深读完成率和 Data 回读结果；三类来源覆盖直接按本轮快照计算。字段未知时显示“—”。

浏览器先读取 `data/projects.json`、`config/tracker.json`、`state/status.json`、`state/validation-index.json`，再取得状态中指向的已确认 snapshot。核对 run_id、时间、项目集合，并在支持 Web Crypto 的安全上下文中计算原始响应字节的 Git blob SHA-1，与索引比对。它是网页侧的快照复核，不能代替维护协议中的完整 tree、全文件及独立 Receipt 验证。

失败时不把数据换成零；快照/索引不一致时停止展示并提供重试和 GitHub 原文入口。7/30 日增长只使用配置容差内的真实历史基线，并保留实际间隔。Release 的 `status=ok` 且 `complete=true` 才计入完整覆盖。图上的折线只连接观测点，不证明空白区间有连续采集。

## 首次启用 GitHub Pages

发布源必须是 **main 分支的根目录**，不是 `/docs`。原因是网页需要同源读取现有的 `data/`、`state/`、`projects/`、`reports/` 和 `docs/`。

在本仓库的 Settings → Pages → Build and deployment 中，将 Source 设为 **Deploy from a branch**，Branch 设为 **main**，目录设为 **/(root)**，点击 Save。根目录的 `.nojekyll` 使 GitHub 按静态文件发布，不要求 Jekyll front matter。

启用并成功部署后的预期地址：

`https://psiQAQ.github.io/agent-memory-github-trending/`

仓库文件提交本身不证明 Pages 已启用、部署已完成或网址可访问；首次上线需要独立检查。初次实现时，连接器提供 Git 对象写入，但未提供配置 Pages 发布源的动作，因此不能用源码提交成功冒充上线成功。

之后 Scheduled 仍只更新原有数据和报告。GitHub Pages 完成对应分支版本的发布后，浏览器即可读取新内容；无需增加第二个定时任务或要求本机保持开机。GitHub 自身可能使用官方 Pages workflow 执行发布，但本项目没有新增构建/采集工作流。

配置方式与限制以 [GitHub 官方发布源说明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)为准；如果将来改为通过 Actions 的 `GITHUB_TOKEN` 推送，需注意该方式不会自动触发 Pages 构建，不能直接套用当前更新路径。

## 开发与验证

源码入口是 `index.html`、`assets/site.css`、`assets/site.js`、`assets/site-core.mjs`。不改动原有数据契约和自动化任务。仅增加前端测试 `tests/site.test.mjs`，不执行上游研究代码。

```sh
# 以下仅供网站开发者预览，不是日常 Scheduled 的依赖。
python -m http.server 8000
# 浏览器打开 http://localhost:8000/，不要直接双击 file:// 页面。

# 只需 Node 内置测试运行器，不需要 npm install。
node --test tests/site.test.mjs
```

初次验证：16 项 Node 单元测试通过；另使用测试数据完成 29 项离线 Chromium 界面检查，覆盖筛选、文档、暗色模式、移动端、缺失数据与失败回退。离线检查不等同于线上 Pages、网络和真实数据端到端验收。

Markdown 渲染支持标题、段落、常用列表、表格、引用、代码块、强调和普通链接；原始 HTML 一律作为文本，不执行脚本。图片以说明链接显示，不自动加载外部追踪资源。复杂 Markdown 扩展不保证完整排版，可使用每篇文章的 GitHub 原文入口。内部文档路径使用允许列表；危险 URL 协议和带凭据的链接被拒绝。CSP 禁止第三方脚本、插件和表单提交。主题偏好仅保存在浏览器 localStorage。
