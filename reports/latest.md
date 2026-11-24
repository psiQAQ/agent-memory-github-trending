# Agent Memory 简报｜2026-11-25

Hindsight v1.3.0 发布 Knowledge Banks，可上传文件、摄取文本并检索文档片段。
Graphiti 的 Relate 驱动适合评估进程内图存储的 Python 应用。OpenViking 修正了 Compile 对未写出产物的状态记录。
接入 Knowledge Banks 前先核对知识库开关、嵌入配置与访问策略。评估 Graphiti 持久化时，给 Relate 显式指定磁盘路径。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [Hindsight](https://github.com/vectorize-io/hindsight/releases/tag/v1.3.0) | Knowledge Banks 支持文件上传、文本摄取与片段检索。 | 已发布 v1.3.0 | 有文档检索需求的服务可先验证嵌入配置和访问策略。 |
| [Graphiti](https://github.com/getzep/graphiti/commit/f70795371dd1bba79b2b85deec4978b4ed37bb00) | Relate 驱动可在 Python 进程内打开图存储。 | mcp-v1.1.4 标签的源码包含驱动 | 持久化需要显式路径及 Python 3.11 或更新版本的可选依赖。 |
| [OpenViking](https://github.com/volcengine/OpenViking/commit/dfad651fee8fede13dda3915477a452e1b31032a) | Compile 将校验拒绝的产物计入写入结果核对。 | 已合并，发行包含关系待核实 | 依赖增量编译的部署可检查覆盖记录中因产物缺失而失败的源。 |
| [claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.2) | 手机安装表单将操作区固定在底部，首次安装完成后可显示代理数量。 | 已发布 v16.1.2 | 这两项变化影响 My Work 安装流程。 |

### 适用条件

**Hindsight**。Knowledge Banks 走独立的 `/v1/default/knowledge-banks` 路由。发布版的 `HINDSIGHT_API_ENABLE_KB` 默认开启，关闭后路由返回 404。文本摄取默认等待文档可检索，选择异步则返回 202 和操作记录。服务先认证租户，配置了操作验证器时还会分别校验知识库读写。配置写入受服务端的 bank 配置开关约束。首次检索所需的向量维度由嵌入器提供。

**Graphiti**。`RelateDriver` 默认使用 `:memory:`，命名空间默认是 `neo4j`。驱动将显式路径交给本地 Relate 连接，并在打开失败后释放工作线程。项目的 `relate` extra 固定 `relate-db==1.0.1`，仅在 Python 3.11 起解析该依赖。MCP 1.1.4 默认声明的依赖是 `graphiti-core[falkordb]`。本轮核对了发行标签中的源码与依赖声明，未验证 MCP 部署能否选用 Relate。

**OpenViking**。Compile 对未通过格式校验的产物保留来源引用。最终写入结果传入后，产物缺失会令相应来源标记为失败。恢复路径还会比对来源集合和固定提交中的文件字节，读取失败或指纹不同便放弃该恢复证据。此处覆盖记录反映写入状态。

**claude-mem**。底部吸附样式只作用于宽度不超过 560 CSS 像素的安装表单。首次安装摘要要求扫描完成、无历史、无结果及读取错误，并且提取未运行也未失败。代理数量来自安装成功后的选择列表，普通继续和 Cloud Sync 试用依各自条件显示。

## Star 变化

相邻观测间隔约 11.11 小时。7 日和 30 日均采用 ±6 小时容差内的实际观测。

| 项目 | 前次 UTC | 本次 UTC | 本次 Stars | 相邻净变化 | 7 日净变化 | 30 日净变化 |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| mem0ai/mem0 | 11-24 05:05:05 | 11-24 16:11:31 | 69422 | +25 | +307 | +1638 |
| getzep/graphiti | 11-24 05:05:11 | 11-24 16:11:37 | 33057 | +16 | +172 | +854 |
| thedotmack/claude-mem | 11-24 05:05:17 | 11-24 16:11:43 | 119475 | +109 | +1571 | +16452 |
| vectorize-io/hindsight | 11-24 05:05:29 | 11-24 16:11:55 | 63100 | +150 | +1541 | +9462 |
| volcengine/OpenViking | 11-24 05:05:48 | 11-24 16:12:14 | 42691 | +22 | +320 | +1908 |

## 新候选线索对比

以下内容来自公开仓库的搜索描述，仍待核对实现。本轮没有新增准入。

| 线索 | 公开描述 | 待核实 |
| --- | --- | --- |
| [QuoteMem](https://github.com/edsml-jz2321/QuoteMem) | 以原文片段和版本关系记录记忆，支持标记遗忘。 | 删除标记能否覆盖后续检索与导出。 |
| [agent-memory-supabase](https://github.com/midcityhandyman/agent-memory-supabase) | 在 PostgreSQL 上结合文本、向量与历史结果做检索。 | 历史结果如何参与重排，部署需要哪些扩展。 |
| [larp-files](https://github.com/pal404error/larp-files) | 以单文件保存版本化记忆，结合 BM25、本地嵌入与 MCP。 | 写入冲突时怎样保留版本，索引如何恢复。 |

## 方法与覆盖边界

24 个登记项目均完成元数据、HEAD 和增量 Release 检查。两条搜索各取首页，共返回 40 条结果。四项变化完成有界源码审读。此次未运行上游软件或评测。Stars 表示关注度，表中净变化仅对应实际观测窗口。

<details markdown="1"><summary>证据与时间</summary>

本轮 `20261124T161051Z-local`，批次观察时刻 2026-11-24T16:12:47.333Z。

- Hindsight，发行于 2026-11-24T14:20:19Z。发行标签解析到 `937886199e0e3443f41f4d8180a16b12cc95c547`。[HTTP 路由](https://github.com/vectorize-io/hindsight/blob/937886199e0e3443f41f4d8180a16b12cc95c547/hindsight-api-slim/hindsight_api/knowledge/routes.py#L553-L590) · [配置默认值](https://github.com/vectorize-io/hindsight/blob/937886199e0e3443f41f4d8180a16b12cc95c547/hindsight-api-slim/hindsight_api/config.py#L2200) · [服务读写校验](https://github.com/vectorize-io/hindsight/blob/937886199e0e3443f41f4d8180a16b12cc95c547/hindsight-api-slim/hindsight_api/knowledge/service.py#L738-L805)
- Graphiti，驱动提交记录于 2026-11-23T03:22:04Z。MCP 发行于 2026-11-23T21:44:16Z，标签直接指向 `a61333edfa14cc483365ed7dd1e287ae6096db6c`。[发行](https://github.com/getzep/graphiti/releases/tag/mcp-v1.1.4) · [驱动默认值](https://github.com/getzep/graphiti/blob/a61333edfa14cc483365ed7dd1e287ae6096db6c/graphiti_core/driver/relate_driver.py#L212-L271) · [本地连接](https://github.com/getzep/graphiti/blob/a61333edfa14cc483365ed7dd1e287ae6096db6c/graphiti_core/driver/relate/_session/_store.py#L175-L211) · [可选依赖](https://github.com/getzep/graphiti/blob/a61333edfa14cc483365ed7dd1e287ae6096db6c/pyproject.toml#L39-L41) · [MCP 依赖](https://github.com/getzep/graphiti/blob/a61333edfa14cc483365ed7dd1e287ae6096db6c/mcp_server/pyproject.toml#L1-L14)
- OpenViking，变更提交于 2026-11-24T10:24:16Z。[拒绝产物记录](https://github.com/volcengine/OpenViking/blob/dfad651fee8fede13dda3915477a452e1b31032a/bot/vikingbot/compile/ops/finalize.py#L22-L45) · [写入覆盖判定](https://github.com/volcengine/OpenViking/blob/dfad651fee8fede13dda3915477a452e1b31032a/bot/vikingbot/compile/pipeline.py#L247-L280) · [恢复校验](https://github.com/volcengine/OpenViking/blob/dfad651fee8fede13dda3915477a452e1b31032a/bot/vikingbot/compile/sources.py#L79-L103)
- claude-mem，发行于 2026-11-24T05:29:04Z。发行标签解析到 `a046a6a9fd8fb1cc56466194487dca94e8212409`。[移动端样式](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/setup.css#L555-L585) · [首次安装条件](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/screens/reveal-screen.tsx#L203-L240) · [代理数量来源](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/setup-page.tsx#L333-L336)

| 项目 | 7 日基线 UTC | 实际小时 | 30 日基线 UTC | 实际小时 |
| --- | --- | ---: | --- | ---: |
| mem0 | 2026-11-17T16:05:11.531Z | 168.11 | 2026-10-25T16:11:47.851Z | 720.00 |
| Graphiti | 2026-11-17T16:05:30.990Z | 168.10 | 2026-10-25T16:12:40.777Z | 719.98 |
| claude-mem | 2026-11-17T16:05:50.185Z | 168.10 | 2026-10-25T16:13:13.034Z | 719.98 |
| Hindsight | 2026-11-17T16:06:39.984Z | 168.09 | 2026-10-25T16:13:59.822Z | 719.97 |
| OpenViking | 2026-11-17T16:07:33.505Z | 168.08 | 2026-10-25T16:15:17.188Z | 719.95 |

</details>
