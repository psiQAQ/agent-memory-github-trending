# Agent Memory 简报｜2026-11-15

Hindsight 更新知识库搜索与检索追踪，OpenViking 调整 Markdown 编译的工作单元。
变化分别影响调用 Hindsight 知识库搜索的应用，以及用 OpenViking VikingBot 编译 Markdown 的流程。
两项已合并，原采集窗口内未见对应发行版。试用固定提交时可分别核对检索排序和多源编译的实际产出。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6542) | 知识库搜索将关键词命中与向量结果融合，并可返回候选来源、排序和 token 预算保留情况。 | 已合并，本轮未见发布 | 依赖知识库检索的应用可用多语言关键词样例检查排序，并在排查时开启 trace。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7682) | Markdown 编译改为隔离的文件工作单元。仅采用正常完成的工作单元生成的 Markdown，队列受并发限制。 | 已合并，本轮未见发布 | 试用时可用多源 Markdown 小样检查产出范围和取消后的行为。 |

**vectorize-io/hindsight**。静态代码覆盖知识库搜索路径。关键词索引使用 PostgreSQL simple 配置，未复现多语言召回率或性能。

**volcengine/OpenViking**。静态核对覆盖 VikingBot Compile 路径。隔离的是工作单元的输出目录，未测吞吐、成本或编译质量。

## Star 变化：真实间隔约 13.65–13.69 小时

7日/30日合格基线分别为 21/21、21/21，容差±6小时。下表比较两次实际观测的 Star 净变化，各项目起止时间见证据区。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68928 | 68953 | +25 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32798 | 32807 | +9 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12391 | 12398 | +7 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 116870 | 117013 | +143 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3834 | 3838 | +4 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 60914 | 61030 | +116 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30882 | 30901 | +19 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2956 | 2957 | +1 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 607 | 608 | +1 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 42208 | 42231 | +23 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 326 | 326 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33299 | 33309 | +10 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 500 | 500 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4317 | 4317 | +0 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 869 | 869 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1214 | 1215 | +1 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 201 | 202 | +1 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1218 | 1219 | +1 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 209 | 210 | +1 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 168 | 168 | +0 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25433 | 25437 | +4 |

## 新候选对比

两条无 Star 下限查询共取得 40 条原始结果。候选代码初审0项、收录0项，登记池保持 47/50。下表只是搜索描述对照，依赖、宿主和评测尚未独立核实。

| 未审线索 | 搜索描述（上游自述） | 许可 API 线索 | 实现/评测/成熟度 |
| --- | --- | --- | --- |
| [fanjiahui-charix/Long_sequence_tasks_for_realmanrobot](https://github.com/fanjiahui-charix/Long_sequence_tasks_for_realmanrobot) | Embodied ReAct agent with working and episodic memory for long-horizon mobile manipulation on RealMan robots. 面向长时序移动操作任务的具身 Agent 与记忆增强执行框架。 | MIT | 未核实 |
| [Christianlamas062/aegis-sql-bridge](https://github.com/Christianlamas062/aegis-sql-bridge) | Self-Healing, Zero-Trust Read-Only SQL &amp; Episodic Memory MCP Gateway powered by SQLite, FastMCP, and Qdrant | 未提供 | 未核实 |
| [hussain-alsaibai/tiny-agent-memory](https://github.com/hussain-alsaibai/tiny-agent-memory) | Zero-dependency memory system for AI agents. Semantic + working + episodic memory in one file. | MIT | 未核实 |

## 方法与边界

21 个项目的元数据、HEAD 和增量 Release 均已采集。两项变化已核对合并提交、源码与发布覆盖，其余变化待审。发现覆盖每条查询的第一页。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261114T155538Z-local`；观测汇总 UTC 2026-11-14T16:32:38.900Z，展示日期按北京时间计算。[原始快照](../data/snapshots/2026/11/20261114T155538Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。发行状态按本轮采集窗口判断。

### vectorize-io/hindsight

[PR](https://github.com/vectorize-io/hindsight/pull/6542) 合并UTC 2026-11-14T09:16:50Z，SHA `5318be8ea572aa00ceae636c71c1d8d334f805b6`；发布UTC 未确认。审读观察UTC 2026-11-14T16:37:11.474Z。固定 HEAD 比较包含合并提交，原批次增量 Release 完整且没有在合并后发布的条目。

阅读范围：[hindsight-api-slim/hindsight_api/knowledge/service.py](https://github.com/vectorize-io/hindsight/blob/5318be8ea572aa00ceae636c71c1d8d334f805b6/hindsight-api-slim/hindsight_api/knowledge/service.py)；[hindsight-api-slim/hindsight_api/knowledge/store.py](https://github.com/vectorize-io/hindsight/blob/5318be8ea572aa00ceae636c71c1d8d334f805b6/hindsight-api-slim/hindsight_api/knowledge/store.py)；[hindsight-api-slim/hindsight_api/knowledge/routes.py](https://github.com/vectorize-io/hindsight/blob/5318be8ea572aa00ceae636c71c1d8d334f805b6/hindsight-api-slim/hindsight_api/knowledge/routes.py)。

### volcengine/OpenViking

[PR](https://github.com/volcengine/OpenViking/pull/7682) 合并UTC 2026-11-14T10:49:57Z，SHA `d462af04e651335261d4972cb546788a788b2a47`；发布UTC 未确认。审读观察UTC 2026-11-14T16:37:10.454Z。固定 HEAD 比较包含合并提交，原批次增量 Release 完整且没有在合并后发布的条目。

阅读范围：[bot/vikingbot/compile/pipeline.py](https://github.com/volcengine/OpenViking/blob/d462af04e651335261d4972cb546788a788b2a47/bot/vikingbot/compile/pipeline.py)；[bot/vikingbot/compile/pipeline_io.py](https://github.com/volcengine/OpenViking/blob/d462af04e651335261d4972cb546788a788b2a47/bot/vikingbot/compile/pipeline_io.py)；[bot/vikingbot/compile/ops/map.py](https://github.com/volcengine/OpenViking/blob/d462af04e651335261d4972cb546788a788b2a47/bot/vikingbot/compile/ops/map.py)。

### 逐项目Star观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-14T02:49:43.219Z | 2026-11-14T16:30:55.147Z | 13.6866 |
| letta-ai/letta | 2026-11-14T02:49:44.106Z | 2026-11-14T16:30:57.809Z | 13.6871 |
| getzep/graphiti | 2026-11-14T02:50:27.345Z | 2026-11-14T16:31:00.625Z | 13.6759 |
| MemTensor/MemOS | 2026-11-14T02:50:28.243Z | 2026-11-14T16:31:03.942Z | 13.6766 |
| thedotmack/claude-mem | 2026-11-14T02:50:45.200Z | 2026-11-14T16:31:07.224Z | 13.6728 |
| xiaowu0162/LongMemEval | 2026-11-14T02:50:46.027Z | 2026-11-14T16:31:11.916Z | 13.6739 |
| xiaowu0162/LongMemEval-V2 | 2026-11-14T02:51:02.713Z | 2026-11-14T16:31:16.162Z | 13.6704 |
| letta-ai/letta-code | 2026-11-14T02:51:03.658Z | 2026-11-14T16:31:18.307Z | 13.6707 |
| vectorize-io/hindsight | 2026-11-14T02:51:19.809Z | 2026-11-14T16:31:25.304Z | 13.6682 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-14T02:51:20.725Z | 2026-11-14T16:31:42.123Z | 13.6726 |
| VectorSpaceLab/general-agentic-memory | 2026-11-14T02:51:38.886Z | 2026-11-14T16:31:44.715Z | 13.6683 |
| agiresearch/A-mem | 2026-11-14T02:51:39.742Z | 2026-11-14T16:31:47.540Z | 13.6688 |
| memodb-io/memobase | 2026-11-14T02:51:56.992Z | 2026-11-14T16:31:50.724Z | 13.6649 |
| neo4j-labs/agent-memory | 2026-11-14T02:51:57.946Z | 2026-11-14T16:31:53.903Z | 13.6655 |
| volcengine/OpenViking | 2026-11-14T02:52:14.798Z | 2026-11-14T16:31:56.355Z | 13.6615 |
| vectorize-io/agent-memory-benchmark | 2026-11-14T02:52:15.804Z | 2026-11-14T16:31:59.720Z | 13.6622 |
| redis/agent-memory-server | 2026-11-14T02:52:34.248Z | 2026-11-14T16:32:04.970Z | 13.6585 |
| topoteretes/cognee | 2026-11-14T02:52:35.760Z | 2026-11-14T16:32:15.975Z | 13.6612 |
| MemTensor/MemRL | 2026-11-14T02:52:56.304Z | 2026-11-14T16:32:19.883Z | 13.6565 |
| obra/episodic-memory | 2026-11-14T02:52:57.642Z | 2026-11-14T16:32:26.155Z | 13.6579 |
| tigerless-labs/agent-memory | 2026-11-14T02:53:17.191Z | 2026-11-14T16:32:33.907Z | 13.6546 |

### 发现与参考覆盖

- `"episodic memory" in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-14T16:32:37.202Z。
- `"agentic memory" in:name,description created:>=2026-10-15 archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-14T16:32:38.900Z。
- 外部榜单沿用[已登记参考版本](../docs/references.md)，本轮未刷新其当前版本，不新增跨协议分数比较。

</details>
