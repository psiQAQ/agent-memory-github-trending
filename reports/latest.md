# Agent Memory 研究简报｜2026-10-24

> **变化：** OpenViking v0.5.2 涵盖 Session 隐私、持久写入和多项迁移；Letta Code v0.34.21 调整 MCP 调用来源隔离与远程子代理归属；Cognee v1.6.6rc1 更改搜索历史删除语义。
>
> **影响谁：** 正升级记忆服务、依赖 LangChain/Pi/MCP 接口、需要保留历史审计轨迹或运行多 Agent 的开发团队。
>
> **是否行动：** OpenViking/Cognee 升级前先评估破坏性变更并保留可恢复备份；Letta Code 使用多租户 MCP 或子代理时测试授权归属。没有独立复现证据证明性能提升。

## 已确认合并/发布的变更

| 项目 | 变化、理由与行动 | 状态 | 影响面 |
| --- | --- | --- | --- |
| [OpenViking v0.5.2](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2) | 上游声明新增 Session 隐私树、写入持久任务、增量 Compile；LangChain 导入改用 `langchain_openviking` 独立包，Pi 0.4.0 工具名改为 `openviking_*`，Watch 重导入不再重置原任务，Working Memory 默认关闭。需按具体版本排查旧插件、配置和数据迁移。 | 正式发布；上游说明 | 兼容迁移、隐私、持久化 |
| [Letta Code v0.34.21](https://github.com/letta-ai/letta-code/releases/tag/v0.34.21) | 声明在队列化会话与工具执行间传递和隔离 MCP originator，并修复远端子代理错误声明父运行时所有权；升级方应检查连接源身份、权限与子代理生命周期。 | 正式发布；上游说明 | 多租户 MCP 与子代理隔离 |
| [Cognee v1.6.6rc1](https://github.com/topoteretes/cognee/releases/tag/v1.6.6rc1) | 新增 `forget(clean_history=True)` 和个人搜索历史删除 API；Dataset 删除开始清理关联历史、清理失败会报错，`run_info` 不再携带原始 data。依赖审计轨迹与旧字段者必须预先迁移。 | GitHub Release 已发布（rc1 标签）；上游说明 | 数据清理、审计、兼容性 |

<details markdown="1">
<summary>一手证据、日期与审查边界</summary>

| 项目 | 官方版本来源 | 发布时间 UTC | 证据等级 |
| --- | --- | --- | --- |
| OpenViking | [v0.5.2 Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2) · [迁移文档](https://github.com/volcengine/OpenViking/blob/v0.5.2/docs/en/agent-integrations/07-langchain-langgraph.md) | 2026-10-23T12:43:54Z | `upstream_statement` |
| Letta Code | [v0.34.21 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.21) · [PR #5210](https://github.com/letta-ai/letta-code/pull/5210) | 2026-10-22T19:02:59Z | `upstream_statement` |
| Cognee | [v1.6.6rc1 Release](https://github.com/topoteretes/cognee/releases/tag/v1.6.6rc1) | 2026-10-23T01:46:26Z | `upstream_statement` |

上述证据说明版本已发布且官方声称具备相应功能，不表示本仓库已经运行代码、验证兼容性、检索质量或安全性。其他 HEAD 变化暂未深读，不当作技术事件。
</details>

## Star 真实观测区间（不是 7/30 日增长）

使用同一仓库 ID 的两次 Metadata 样本，真实采样窗口约 39 小时；不转换为 24 小时涨幅，不据此评价技术质量或判刷 Star。

| 项目 | UTC 观测起止 | 实际间隔 | Stars 起止 | 净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](../projects/mem0ai--mem0.html) | 2026-10-22 03:33 UTC → 2026-10-23 18:45 UTC | 39.2 小时 | 67606 → 67707 | +101 |
| [getzep/graphiti](../projects/getzep--graphiti.html) | 2026-10-22 03:33 UTC → 2026-10-23 18:46 UTC | 39.2 小时 | 32118 → 32167 | +49 |
| [thedotmack/claude-mem](../projects/thedotmack--claude-mem.html) | 2026-10-22 03:33 UTC → 2026-10-23 18:47 UTC | 39.2 小时 | 102174 → 102506 | +332 |
| [letta-ai/letta-code](../projects/letta-ai--letta-code.html) | 2026-10-22 03:33 UTC → 2026-10-23 18:48 UTC | 39.2 小时 | 3677 → 3696 | +19 |
| [vectorize-io/hindsight](../projects/vectorize-io--hindsight.html) | 2026-10-22 03:34 UTC → 2026-10-23 18:48 UTC | 39.2 小时 | 52432 → 53088 | +656 |
| [TencentCloud/TencentDB-Agent-Memory](../projects/tencentcloud--tencentdb-agent-memory.html) | 2026-10-22 03:34 UTC → 2026-10-23 18:49 UTC | 39.2 小时 | 29767 → 29863 | +96 |
| [volcengine/OpenViking](../projects/volcengine--openviking.html) | 2026-10-22 03:34 UTC → 2026-10-23 18:50 UTC | 39.3 小时 | 40544 → 40680 | +136 |
| [topoteretes/cognee](../projects/topoteretes--cognee.html) | 2026-10-22 03:35 UTC → 2026-10-23 18:51 UTC | 39.3 小时 | 32640 → 32700 | +60 |
| [tigerless-labs/agent-memory](../projects/tigerless-labs--agent-memory.html) | 2026-10-22 03:35 UTC → 2026-10-23 18:53 UTC | 39.3 小时 | 4341 → 4554 | +213 |

本轮 21/21 个项目均有新的 Metadata，但 **0/21** 有符合 ±6 小时误差条件的 7 日基线、**0/21** 有符合条件的 30 日基线，因此正式 7/30 日变化仍显示“—”。后续只有在历史样本目标时刻附近再次成功采集，才可生成合格区间；此处不预测增长。

## 未审候选横向比较

| 候选 | 记忆机制或用途 | 依赖、宿主及许可 | 审查边界 |
| --- | --- | --- | --- |
| [mempal](https://github.com/ZhangHanDong/mempal) | SQLite/向量融合、决策来源回溯（上游描述） | Rust CLI / MCP；许可证与运行要求未核实 | 候选；未实测 |
| [Engram](https://github.com/Gentleman-Programming/engram) | Coding Agent 跨会话记忆 | 本地/云与多宿主系上游自述；许可未核实 | 候选；未实测 |
| [MemoryAgentBench](https://github.com/HUST-AI-HYZ/MemoryAgentBench) | 研究型多轮记忆评测 | Python、模型等依赖；协议需要另审 | 评测资产，不是记忆服务 |
| [DolphinBench](https://github.com/mem0ai/dolphinbench) | 工具使用场景下的记忆评测 | Agent harness、模型及配置未独立核对 | 厂商评测，非独立认证 |

未审候选不因搜索排名自动晋升。两种 discovery 查询各只查看 1 页、每页 20 个结果，无法推断候选生态规模；本轮未新增正式项目。

## 方法与边界

本轮覆盖 21 个登记项目的 Metadata、默认分支 HEAD 与增量 Release（各 21/21），对 3 个实际新 Release 深读官方说明，未运行上游代码、MCP、Jekyll 或付费 benchmark。仅核对增量发布水位，不宣称穷尽上游历史或 HEAD 变更。调用计数因外部 pre/post 证据链不完整而记为未知；运维详见状态文件。参见 [当前观测](current.html) · [原始快照](../data/snapshots/2026/10/20261023T184223Z-interactive.json) · [筛选方法](../docs/methodology.html)。
