# Agent Memory 简报｜2026-11-16

Graphiti 合并了移除 Kuzu 驱动的改动，claude-mem 和 Letta Code 发布了规则加载与会话持久化修复。
受影响的是使用 Kuzu 的 Graphiti 部署、加载自定义规则的 Claude Code 会话，以及依赖 Letta Code 恢复中断会话的部署。
Kuzu 用户应在升级前规划后端迁移。另两项已随版本发布，可按实际规则路径和低磁盘场景验证。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [getzep/graphiti](https://github.com/getzep/graphiti/pull/2151) | Graphiti 移除了 Kuzu 驱动及安装选项。 | 已合并，本轮未见发布 | 仍使用 Kuzu 的部署应在更新 Graphiti 前准备替换后端，并验证现有图数据可迁移。 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/6179) | claude-mem 在 Claude Code 中通过 Markdown 导入链加载规则与工具说明。已有说明匹配时，MCP 初始化省略重复文本。 | 已发布 [v15.18.4](https://github.com/thedotmack/claude-mem/releases/tag/v15.18.4) | 使用自定义规则文件或数据目录的 Claude Code 用户可核对导入路径和启动时出现的说明。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/5734) | Letta Code 把中断会话记录的加锁与写入纳入磁盘预留机制。遇到空间不足可释放预留空间并重试一次，仍失败则返回错误。 | 已发布 [v0.34.62](https://github.com/letta-ai/letta-code/releases/tag/v0.34.62) | 依赖中断会话恢复的部署可在升级前后核对低磁盘空间下的记录与错误处理。 |

**getzep/graphiti**。源码差异删除了 GraphProvider.KUZU 和 Kuzu 安装选项。此次只核对实现，未迁移数据。

**thedotmack/claude-mem**。MCP 省略说明有宿主、导入链和文本匹配条件。未执行 Claude Code 会话。

**letta-ai/letta-code**。读取了中断记录写入包装和锁目录 ENOSPC 的上游回归用例，未实际模拟满盘。

## Star 变化：真实间隔约 23.62–23.64 小时

7日/30日合格基线分别为 21/21、0/21，容差±6小时。下表比较两次实际观测的 Star 净变化，各项目起止时间见证据区。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68953 | 69009 | +56 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32807 | 32821 | +14 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12398 | 12405 | +7 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 117013 | 117290 | +277 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3838 | 3845 | +7 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 61030 | 61178 | +148 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30901 | 30920 | +19 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2957 | 2958 | +1 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 608 | 609 | +1 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 42231 | 42257 | +26 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 326 | 326 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33309 | 33328 | +19 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 500 | 500 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4317 | 4319 | +2 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 869 | 869 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1215 | 1215 | +0 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 202 | 202 | +0 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1219 | 1221 | +2 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 210 | 211 | +1 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 168 | 169 | +1 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25437 | 25448 | +11 |

## 新候选对比

两条无 Star 下限查询共取得 34 条原始结果。候选代码初审 0 项、收录 0 项，登记池保持 47/50。下表只是搜索描述对照，依赖、宿主和评测尚未独立核实。

| 未审线索 | 搜索描述（上游自述） | 许可 API 线索 | 实现/评测/成熟度 |
| --- | --- | --- | --- |
| [zensation-ai/zenbrain](https://github.com/zensation-ai/zenbrain) | Agent memory for LLM agents: 7 neuroscience-inspired layers (working, episodic, semantic, procedural) with FSRS-style spaced repetition and memory consolidation. TypeScript, no third-party dependencies in the core packages; Model Context Pr | Apache-2.0 | 未核实 |
| [timoncool/dream-skill](https://github.com/timoncool/dream-skill) | Memory consolidation skills for Claude Code — read-only dream pass, checkbox/validator gate, full-auto mode, snapshot + one-command rollback. No rm, ever. | MIT | 未核实 |
| [yzhang-master/episodic-memory-consolidation-agent](https://github.com/yzhang-master/episodic-memory-consolidation-agent) | Episodic and semantic memory with recency-importance-relevance retrieval and contradiction-aware consolidation | MIT | 未核实 |

## 方法与边界

21 个项目的元数据、HEAD 和增量 Release 均已采集。三项变化已核对合并记录、源码差异与发布覆盖，其余变化待审。发现覆盖每条查询的第一页。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261115T160501Z-local`；观测汇总 UTC 2026-11-15T16:11:31.515Z，展示日期按北京时间计算。[原始快照](../data/snapshots/2026/11/20261115T160501Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。发行状态按本轮采集窗口判断。

### getzep/graphiti

[PR](https://github.com/getzep/graphiti/pull/2151) 合并UTC 2026-11-15T00:42:48Z，SHA `3a8a78c997a07cceeb3411ede533b0f342d71c64`；发布UTC 未确认。审读观察UTC 2026-11-15T16:13:23.440Z。本轮完整增量 Release 未见合并后的对应版本。

阅读范围：[graphiti_core/driver/driver.py](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/graphiti_core/driver/driver.py)；[pyproject.toml](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/pyproject.toml)。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/6179) 合并UTC 2026-11-15T05:48:47Z，SHA `ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774`；发布UTC 2026-11-15T05:54:37Z。审读观察UTC 2026-11-15T16:13:24.397Z。发行说明直接列出该 PR。

阅读范围：[src/shared/claude-code-rules-import.ts](https://github.com/thedotmack/claude-mem/blob/ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774/src/shared/claude-code-rules-import.ts)；[src/servers/mcp-server.ts](https://github.com/thedotmack/claude-mem/blob/ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774/src/servers/mcp-server.ts)。

### letta-ai/letta-code

[PR](https://github.com/letta-ai/letta-code/pull/5734) 合并UTC 2026-11-14T22:53:29Z，SHA `21f39b92ca690b4ef16889509ca53d3d88cbef7b`；发布UTC 2026-11-15T01:16:48Z。审读观察UTC 2026-11-15T16:13:30.867Z。发行说明直接列出该 PR。

阅读范围：[src/websocket/listener/interrupted-turn-disk-reserve.ts](https://github.com/letta-ai/letta-code/blob/21f39b92ca690b4ef16889509ca53d3d88cbef7b/src/websocket/listener/interrupted-turn-disk-reserve.ts)；[src/websocket/listener/interrupted-turn-disk-reserve.test.ts](https://github.com/letta-ai/letta-code/blob/21f39b92ca690b4ef16889509ca53d3d88cbef7b/src/websocket/listener/interrupted-turn-disk-reserve.test.ts)。

### 逐项目Star观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-14T16:30:55.147Z | 2026-11-15T16:08:14.894Z | 23.6222 |
| letta-ai/letta | 2026-11-14T16:30:57.809Z | 2026-11-15T16:08:15.793Z | 23.6217 |
| getzep/graphiti | 2026-11-14T16:31:00.625Z | 2026-11-15T16:08:35.285Z | 23.6263 |
| MemTensor/MemOS | 2026-11-14T16:31:03.942Z | 2026-11-15T16:08:36.171Z | 23.6256 |
| thedotmack/claude-mem | 2026-11-14T16:31:07.224Z | 2026-11-15T16:08:51.305Z | 23.6289 |
| xiaowu0162/LongMemEval | 2026-11-14T16:31:11.916Z | 2026-11-15T16:08:52.226Z | 23.6279 |
| xiaowu0162/LongMemEval-V2 | 2026-11-14T16:31:16.162Z | 2026-11-15T16:09:06.962Z | 23.6308 |
| letta-ai/letta-code | 2026-11-14T16:31:18.307Z | 2026-11-15T16:09:07.855Z | 23.6304 |
| vectorize-io/hindsight | 2026-11-14T16:31:25.304Z | 2026-11-15T16:09:22.692Z | 23.6326 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-14T16:31:42.123Z | 2026-11-15T16:09:23.627Z | 23.6282 |
| VectorSpaceLab/general-agentic-memory | 2026-11-14T16:31:44.715Z | 2026-11-15T16:09:39.428Z | 23.6319 |
| agiresearch/A-mem | 2026-11-14T16:31:47.540Z | 2026-11-15T16:09:40.360Z | 23.6313 |
| memodb-io/memobase | 2026-11-14T16:31:50.724Z | 2026-11-15T16:09:54.911Z | 23.6345 |
| neo4j-labs/agent-memory | 2026-11-14T16:31:53.903Z | 2026-11-15T16:09:55.829Z | 23.6339 |
| volcengine/OpenViking | 2026-11-14T16:31:56.355Z | 2026-11-15T16:10:10.121Z | 23.6372 |
| vectorize-io/agent-memory-benchmark | 2026-11-14T16:31:59.720Z | 2026-11-15T16:10:11.120Z | 23.6365 |
| redis/agent-memory-server | 2026-11-14T16:32:04.970Z | 2026-11-15T16:10:25.915Z | 23.6392 |
| topoteretes/cognee | 2026-11-14T16:32:15.975Z | 2026-11-15T16:10:26.957Z | 23.6364 |
| MemTensor/MemRL | 2026-11-14T16:32:19.883Z | 2026-11-15T16:10:42.173Z | 23.6395 |
| obra/episodic-memory | 2026-11-14T16:32:26.155Z | 2026-11-15T16:10:43.141Z | 23.6381 |
| tigerless-labs/agent-memory | 2026-11-14T16:32:33.907Z | 2026-11-15T16:10:58.826Z | 23.6403 |

### 发现与参考覆盖

- `"memory consolidation" in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-15T16:11:30.313Z。
- `"memory consolidation" in:name,description created:>=2026-10-16 archived:false fork:false`：page=1，returned=14，sort=updated，incomplete_results=False，pagination_complete=True；UTC 2026-11-15T16:11:31.515Z。
- 外部榜单沿用[已登记参考版本](../docs/references.md)，本轮未刷新其当前版本，不新增跨协议分数比较。

</details>
