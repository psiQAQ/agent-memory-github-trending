# Agent Memory 简报｜2026-11-04

Claude-mem 发布安装向导上传前明确征求同意的修复；Hindsight 发布删除 bank 时补清维护队列的修复。
前者影响使用浏览器安装向导的编码 Agent 用户，后者影响依赖 bank 删除或清空操作的数据管理部署。
建议按实际使用路径评估升级并复测；升级不删除旧版已上传的提示词，审计日志也有独立保留策略。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v15.8.3) | 浏览器安装向导先在本地扫描历史，再等待明确同意才向 cmem.ai 上传选中工具的提示词；匿名结果共享默认关闭，独立于上传同意。 | 已发布 v15.8.3 | 使用 v15.2.0 起浏览器安装向导的用户应评估升级并检查上传选项。扫描仍先读取本地历史；升级不删除旧版本已上传的数据，也未核验服务端保留策略。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/releases/tag/v1.2.0) | 删除或清空 bank 时，purge_bank_rows 显式删除 graph_maintenance_queue 与 entity_maintenance_queue 的同 bank 行，补上没有外键级联的清理缺口。 | 已发布 v1.2.0 | 依赖 bank 删除隔离数据的部署可升级后复测两个队列。audit_log 仍按保留期留存；本次未执行数据库测试，不能据此宣称所有后端或历史残留已清除。 |

## Star 变化：真实间隔约 71.88–71.89 小时

以下按类别与登记顺序比较上轮与本轮真实观测，不外推日增长或整周增长。7日/30日合格基线分别为 0/21、0/21（容差 ±6 小时）；起止 UTC 与精确间隔见折叠区。关注度不代表技术质量。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 实际区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68158 | 68337 | +179 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32390 | 32486 | +96 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12207 | 12240 | +33 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 107312 | 111504 | +4192 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3748 | 3775 | +27 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 56895 | 58390 | +1495 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30303 | 30386 | +83 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2943 | 2947 | +4 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 597 | 602 | +5 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41245 | 41446 | +201 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 324 | 325 | +1 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 32954 | 33026 | +72 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 494 | 500 | +6 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4303 | 4301 | -2 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 864 | 867 | +3 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1212 | 1213 | +1 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 194 | 195 | +1 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1184 | 1191 | +7 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 199 | 201 | +2 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 159 | 163 | +4 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25306 | 25331 | +25 |

## 新候选对比

两条无 Star 门槛查询各取第一页，共40条原始线索；初审0项、晋升0项，登记池保持 47/50。下表仅转述搜索描述与 API 许可证线索，尚未确认实现或成熟度。

| 搜索线索 | 上游描述的机制 | 宿主、依赖、成熟度 | API 许可证线索 | 处理 |
| --- | --- | --- | --- | --- |
| [qyiun666/MemHop](https://github.com/qyiun666/MemHop) | 嵌入式长期记忆数据库，描述提及知识图、混合检索与休眠期整理 | 描述称 Go 单文件；实现与依赖未核实 | Apache-2.0 | 待初审 |
| [ideator-labs/memfence](https://github.com/ideator-labs/memfence) | 描述称 SQLite 存储拒绝基于过时记忆的写入 | 并发与中断演示未运行，成熟度未核实 | MIT | 待初审 |
| [damian-rafael-lattenero/agent-brain](https://github.com/damian-rafael-lattenero/agent-brain) | 描述提及记忆提取、衰减与召回门禁 | 描述称 Kotlin、pgvector；实现未核实 | 未提供 | 待初审 |

## 方法与边界

21个登记项目的 metadata、HEAD、Release 增量范围均已取得；两项预选变化完成发布源码、合并与版本包含关系核对，其他变化保留待审。发现仅覆盖两条查询的第一页，不代表生态普查。未运行上游程序、测试、性能实验或付费评测；静态阅读不能证明运行效果。

[已闭合的 2026-W44 周报](weekly/2026-W44.md)采用周内实际样本，明确保留缺采边界。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261103T155646Z-local`，完成 UTC 2026-11-03T16:06:25.908Z。[原始快照](../data/snapshots/2026/11/20261103T155646Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。触发来源 unknown/unverified，legacy interactive 不证明人工或自然定时触发。

### thedotmack/claude-mem

[合并 PR](https://github.com/thedotmack/claude-mem/pull/5220)，合并 UTC 2026-11-02T06:12:18Z；[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.8.3)，发布 UTC 2026-11-02T06:26:25Z。合并 `52a1dfea2556e126c959c26d8e25f6fa7da14521` 已确认是发布提交 `9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4` 的祖先。观察 UTC 2026-11-03T16:06:25.908Z，证据等级 code_inspected。
静态阅读范围：[src/services/prompt-import/setup-scan.ts](https://github.com/thedotmack/claude-mem/blob/9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4/src/services/prompt-import/setup-scan.ts)；[src/services/worker/http/routes/WorkViewRoutes.ts](https://github.com/thedotmack/claude-mem/blob/9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4/src/services/worker/http/routes/WorkViewRoutes.ts)。

### vectorize-io/hindsight

[合并 PR](https://github.com/vectorize-io/hindsight/pull/5958)，合并 UTC 2026-10-22T09:37:55Z；[Release](https://github.com/vectorize-io/hindsight/releases/tag/v1.2.0)，发布 UTC 2026-11-03T11:38:19Z。合并 `517192d3bfef0bd7b3efcdedc7829445a55c3ae9` 已确认是发布提交 `34a138684a899b6ec34175f7a2b633860466d289` 的祖先。观察 UTC 2026-11-03T16:06:25.908Z，证据等级 code_inspected。
静态阅读范围：[hindsight-api-slim/hindsight_api/engine/memories/pg/engine_curation.py](https://github.com/vectorize-io/hindsight/blob/34a138684a899b6ec34175f7a2b633860466d289/hindsight-api-slim/hindsight_api/engine/memories/pg/engine_curation.py)。

### 逐项目观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-10-31T16:05:26.810Z | 2026-11-03T15:58:18.860Z | 71.8811 |
| letta-ai/letta | 2026-10-31T16:05:27.695Z | 2026-11-03T15:58:19.849Z | 71.8812 |
| getzep/graphiti | 2026-10-31T16:05:57.916Z | 2026-11-03T15:58:45.980Z | 71.8800 |
| MemTensor/MemOS | 2026-10-31T16:05:59.336Z | 2026-11-03T15:58:46.956Z | 71.8799 |
| thedotmack/claude-mem | 2026-10-31T16:06:24.097Z | 2026-11-03T15:59:11.274Z | 71.8798 |
| xiaowu0162/LongMemEval | 2026-10-31T16:06:25.451Z | 2026-11-03T15:59:12.230Z | 71.8797 |
| xiaowu0162/LongMemEval-V2 | 2026-10-31T16:06:43.675Z | 2026-11-03T15:59:40.781Z | 71.8825 |
| letta-ai/letta-code | 2026-10-31T16:06:44.537Z | 2026-11-03T15:59:41.825Z | 71.8826 |
| vectorize-io/hindsight | 2026-10-31T16:07:08.964Z | 2026-11-03T16:00:03.099Z | 71.8817 |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-31T16:07:09.845Z | 2026-11-03T16:00:04.103Z | 71.8817 |
| VectorSpaceLab/general-agentic-memory | 2026-10-31T16:07:33.647Z | 2026-11-03T16:00:36.438Z | 71.8841 |
| agiresearch/A-mem | 2026-10-31T16:07:34.531Z | 2026-11-03T16:00:37.462Z | 71.8841 |
| memodb-io/memobase | 2026-10-31T16:07:55.400Z | 2026-11-03T16:01:01.824Z | 71.8851 |
| neo4j-labs/agent-memory | 2026-10-31T16:07:56.288Z | 2026-11-03T16:01:02.980Z | 71.8852 |
| volcengine/OpenViking | 2026-10-31T16:08:20.767Z | 2026-11-03T16:01:29.075Z | 71.8856 |
| vectorize-io/agent-memory-benchmark | 2026-10-31T16:08:21.654Z | 2026-11-03T16:01:30.190Z | 71.8857 |
| redis/agent-memory-server | 2026-10-31T16:08:44.016Z | 2026-11-03T16:01:56.518Z | 71.8868 |
| topoteretes/cognee | 2026-10-31T16:08:44.897Z | 2026-11-03T16:01:57.512Z | 71.8868 |
| MemTensor/MemRL | 2026-10-31T16:09:10.332Z | 2026-11-03T16:02:22.431Z | 71.8867 |
| obra/episodic-memory | 2026-10-31T16:09:11.169Z | 2026-11-03T16:02:23.374Z | 71.8867 |
| tigerless-labs/agent-memory | 2026-10-31T16:09:29.320Z | 2026-11-03T16:02:49.208Z | 71.8889 |

### 发现与参考覆盖

- `"memory consolidation" in:name,description archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；returned=20，total_count=316，incomplete_results=false，pagination_complete=false；观察 UTC 2026-11-03T16:03:53.476Z。
- `"agent memory" in:name,description created:>=2026-10-04 archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；returned=20，total_count=924，incomplete_results=false，pagination_complete=false；观察 UTC 2026-11-03T16:03:55.120Z。
- 读取的 [Verging Labs JSON](https://verginglabs.com/index/memory.json)及[变更记录](https://verginglabs.com/changelog)仍列 v0.2、2026-09-16、datasetId=6b0dd2681430eca3。工具分别标记3天前/2天前抓取，未证实源站实时刷新；仅复核参考基线，不作为新技术事件。

</details>
