# Agent Memory 研究简报｜2026-10-16

> **本轮最值得关注：** Hindsight 将可配置决策模型用于 recall 重排序；tigerless 的记忆写入改为可调用工具的“读取—检查—提交”流程。两项均已进入默认分支，**尚未核实进入正式发布包**。
>
> **对谁有影响：** 评估跨会话检索精度、Coding Agent 记忆写入控制、MCP/原生工具宿主接入的开发者。
>
> **现在是否行动：** 可阅读代码并安排小规模对照测试；没有独立性能、费用或延迟实测，不建议仅凭这次变更迁移生产系统。

## 已确认合并/发布的变更

| 项目 | 变化及其意义 | 状态 | 影响面 |
| --- | --- | --- | --- |
| [Hindsight](https://github.com/vectorize-io/hindsight) | 新增 decision-model reranker，允许模型参与 recall 候选排序；全局决策模型提供者默认 `none`，需显式配置。是否改善召回质量、成本与延迟均未测试。 | 已进入默认分支，未确认发布 | 检索策略、模型调用预算 |
| [tigerless Agent Memory](https://github.com/tigerless-labs/agent-memory) | `recall/read/submit_operations` 共用 WriteToolkit，MCP 适配器与宿主工具调用共用验证路径；工具提交操作后由库统一写入，不直接修改 Store。 | 已进入默认分支，无新 Release | 写入控制、宿主接入与操作校验 |
| [OpenViking](https://github.com/volcengine/OpenViking) | OpenCode 插件识别服务端已丢失的 session 并清理过期映射；嵌入输入可按配置 token 上限截断。 | 已进入默认分支，未确认发布 | 宿主会话恢复、嵌入兼容性 |
| [TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | Proxy 路由增加 dsh 前缀，补齐辅助端点识别；另外有 SQLite 时间戳转换和 Hono 请求 body 缓存修正。 | 已进入默认分支，未确认发布 | 部分宿主代理兼容性 |
| [Graphiti v0.31.1](https://github.com/getzep/graphiti/releases/tag/v0.31.1) | 2026-10-15 15:02 UTC 正式发布；本轮所见相对前次 HEAD 的文件变化集中在版本号、锁文件和贡献者签名，**未发现可支持“记忆算法改进”表述的代码证据**。 | 已发布 | 升级与版本管理 |

<details markdown="1">
<summary>展开：代码证据、固定版本与发布边界</summary>

**证据索引（代码静态检查，非运行时验收）：** [Hindsight reranker](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/engine/search/decision_reranker.py) · [默认配置](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/config.py) · [Tigerless 工具契约](https://github.com/tigerless-labs/agent-memory/blob/c395acc4708c545c4b5395f8a2cb1e3a3ababd14/packages/core/src/agent_memory/core/toolkit.py) · [MCP write session](https://github.com/tigerless-labs/agent-memory/blob/c395acc4708c545c4b5395f8a2cb1e3a3ababd14/packages/mcp/src/agent_memory/mcp/write_session.py) · [OpenViking OpenCode 适配](https://github.com/volcengine/OpenViking/blob/84cc2b412a7ef9e89ba52f58bb90a53f284b0499/examples/opencode-plugin/lib/memory-session.mjs) · [Tencent 变更范围](https://github.com/TencentCloud/TencentDB-Agent-Memory/compare/37b162963ce6cf73d8ae1807e3f3614ad23511ae...e9a82935b52741e0c798c75326e90b7144eb4d5f)。


</details>

## Star 变化：两次真实观测（约 6–7 小时）

| 项目 | 上次 Stars | 本轮 Stars | 净变化 |
| --- | ---: | ---: | ---: |
| Hindsight | 49,867 | 49,976 | +109 |
| claude-mem | 100,876 | 100,947 | +71 |
| OpenViking | 39,968 | 39,996 | +28 |
| tigerless/agent-memory | 3,715 | 3,742 | +27 |
| Graphiti | 31,774 | 31,786 | +12 |

数据来自 [本轮快照](../data/snapshots/2026/10/20261015T160632Z-scheduled.json) 与[上一轮真实观测](../data/snapshots/2026/10/20261015T100012Z-interactive.json)，上一轮采集于 **2026-10-15 09:56–09:58 UTC**，本轮采集于 **2026-10-15 16:06–16:16 UTC**（不同项目的实际采集时刻以快照为准），相隔约 6–7 小时；**这不是 24h／7d 增长，也不用于推断质量**。7 日、30 日要求目标时刻 ±6 小时内有真实历史基线；按现有采样条件，分别最早约 10 月 21 日和 11 月 13 日可能出现合格窗口，仍取决于后续实际采集。

## 新候选：仅供比较，未正式收录

| 候选 | 存储/载体线索 | 读取/评估方式 | 许可证 | 成熟度与待核实项 |
| --- | --- | --- | --- | --- |
| [Jev-Mem](https://github.com/libingzheren/Jev-Mem) | 关系图／语义与时间线索 | 语义、时间、因果联合推理（作者描述） | 未核实 | 研究原型；效果未复现 |
| [dolphinbench](https://github.com/mem0ai/dolphinbench) | 评测数据与 runner，不是通用记忆存储 | 模拟工具动作的长时记忆评测 | 未核实 | 发布方与被测产品有关联，非独立认证 |
| [MemTrace](https://github.com/Homy-Xu/MemTrace) | 与仓库状态绑定的执行记录 | 当前任务证据对齐／恢复（作者描述） | 未核实 | 需核对数据协议与评测配置 |
| [MemNexus](https://github.com/zhangjinhan-nudt/MemNexus) | SQLite／长短期记忆 | 证据约束抽取、更正与混合检索 | 未核实 | 宿主接入和评测尚待审查 |
| [tiramisu](https://github.com/buildsip/tiramisu) | Git 文件 | CLI／MCP 读写 | 未核实 | 作者标注 Alpha，冲突处理待核实 |
| [gomem](https://github.com/alpdeniz/gomem) | SQLite | 语义＋关键词混合召回 | 未核实 | Python 桥接和 Windows 路径待验收 |

候选信息目前仅为 README 与资产路径初筛（`upstream_statement`），无法可靠比较准确率、Token 节省、延迟、许可证条款或最近真实提交。**未发现证据 ≠ 功能不存在**。完整入库需核实实现、依赖、许可证和版本后再更新表格。

## 方法与边界

正式追踪 20 个项目、1 个历史参照，Metadata／HEAD／相对于上次成功水位的 Release 增量均为 **21/21**；两条发现查询各查第一页（20 与 8 条），不是全量 GitHub 调查。本轮深读聚焦 5 个 HEAD 或版本变化项目，不代表检查了所有变更文件或全历史发布。证据等级 `code_inspected` 表示核对过固定 SHA 的实现，并**不表示已运行测试、独立复现或验证性能**；供应商分数不与独立评测混用。原始状态、API 调用测量及未深读工作统一放在[运行与指标](../state/status.json)，参见[方法](../docs/methodology.md)。

[上一期读者简报](briefs/2026-10-15.md) · [当前全量 Star 表](current.md) · [项目与证据卡](../data/projects.json)
