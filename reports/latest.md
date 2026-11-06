# Agent Memory 简报｜2026-11-06

Claude-mem v15.10.0 增加记忆捕获开关；Letta Code v0.34.41 修正 Memory Palace 对 MemFS 核心文件的分类。
前者影响希望暂停本机 observation 与摘要模型调用的用户；后者影响使用 MemFS v2、在界面看到核心记忆误分类的用户。
建议按用途评估对应版本，并核对下列服务器边界；本轮没有独立运行或效果评测，不据此建议迁移记忆系统。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/5353) | 新增记忆捕获开关：精确字符串 `CLAUDE_MEM_OBSERVER_ENABLED="false"` 停止新的 observation/session-summary 模型调用，已有记忆、搜索与 SessionStart 上下文保持可用。 | 已发布 v15.10.0 | 需要暂停本机捕获的用户可评估 v15.10.0。默认仍启用，错误值不会关闭；服务器已排队任务及其他客户端不受这个本机设置控制，不应把它当成全局停采或删除记忆。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/4888) | Memory Palace 按 MemFS 布局识别核心记忆：v2 的根目录 Markdown（含 MEMORY.md）归入 core；v1 保留 system/ 目录分类。 | 已发布 v0.34.41 | 使用 MemFS v2 且在界面看到核心文件误分类的用户可评估 v0.34.41。这是展示分类修正，不证明改变 Agent 的记忆投影、检索或效果。 |

## Star 变化：真实间隔约 35.84–35.94 小时

比较两次真实观测，不外推为固定日增长。7日/30日合格基线分别为 0/21、0/21，容差 ±6 小时；缺失窗口显示“—”。逐项目起止 UTC 与精确时长见折叠区。Stars 反映关注度，不是质量分。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 实际区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68392 | 68485 | +93 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32514 | 32574 | +60 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12251 | 12287 | +36 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 112573 | 113621 | +1048 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3778 | 3787 | +9 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 58728 | 59161 | +433 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30437 | 30542 | +105 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2948 | 2949 | +1 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 604 | 604 | +0 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41528 | 41649 | +121 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 325 | 325 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33060 | 33099 | +39 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 501 | 499 | -2 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4306 | 4307 | +1 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 867 | 868 | +1 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1213 | 1214 | +1 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 196 | 197 | +1 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1194 | 1197 | +3 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 201 | 203 | +2 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 163 | 164 | +1 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25348 | 25362 | +14 |

## 新候选对比

两条无 Star 下限查询共取得 32 条原始结果，未做候选代码初审，未新增或晋升项目；登记池保持 47/50。下表只比较搜索结果中的方向，不能作为接入推荐。

| 原始线索 | 描述中的载体、维护与宿主 | 依赖与评测资产 | API 许可证线索 | 处理 |
| --- | --- | --- | --- | --- |
| [Jpgomesf/kioku](https://github.com/Jpgomesf/kioku) | 描述称通过 MCP 为 coding agent 提供 Markdown 笔记、混合检索与链接图 | 描述提及 PostgreSQL、Qdrant、Ollama；实现、成熟度和评测未核实 | MIT | 待初审，不入正式池 |
| [Treetreewu/astrbot_plugin_whale_dream](https://github.com/Treetreewu/astrbot_plugin_whale_dream) | 描述称 AstrBot 插件提供闲时记忆整理与 persona 演进 | LivingMemory 桥接要求、实现和评测未核实 | AGPL-3.0 | 待初审，不入正式池 |

## 方法与边界

21个登记项目的 metadata、HEAD 和 Release 增量范围均已取得；两项预选变化完成 PR、实际 tag 包含关系与固定版本源码核对，其他变化仍待审。发现是两条查询的有界样本，不代表 GitHub 全量生态。未执行上游程序、测试或付费评测；代码阅读不能证明效果、性能或所有宿主兼容性。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261105T160051Z-local`；完成 UTC 2026-11-06T04:07:56.131Z。[原始快照](../data/snapshots/2026/11/20261105T160051Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。本次沿原批次恢复，各来源保留实际观测时间；触发来源 unknown/unverified，interactive 兼容标签不证明人工或定时触发。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/5353)：合并 UTC 2026-11-05T10:26:14Z，合并 SHA `0ff39ac38275d75b51030cfb595f9cdfc622d83d`。[正式 Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.10.0)：发布 UTC 2026-11-05T19:57:39Z；实际 tag 对应 commit `c2bca506d853e867cfa02341672869354b85e18a`，compare 确认包含上述合并。观察 UTC 2026-11-06T04:07:56.131Z，证据等级 code_inspected，未独立复现。

阅读范围：[src/shared/observer-capture.ts](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/src/shared/observer-capture.ts)；[src/services/worker/SessionManager.ts](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/src/services/worker/SessionManager.ts)；[docs/public/configuration.mdx](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/docs/public/configuration.mdx)。

### letta-ai/letta-code

[PR](https://github.com/letta-ai/letta-code/pull/4888)：合并 UTC 2026-11-05T00:49:22Z，合并 SHA `f4f9e37dd51d207f4e4cf16510b8081d5a470f4f`。[正式 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.41)：发布 UTC 2026-11-05T04:23:03Z；实际 tag 对应 commit `233c0034492b9782c9bec01002226b891e514745`，compare 确认包含上述合并。观察 UTC 2026-11-06T04:07:56.131Z，证据等级 code_inspected，未独立复现。

阅读范围：[src/agent/memory-format.ts](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/agent/memory-format.ts)；[src/web/generate-memory-viewer.ts](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/web/generate-memory-viewer.ts)；[src/web/memory-viewer-template.txt](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/web/memory-viewer-template.txt)。

### 逐项目 Star 观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-04T16:02:59.673Z | 2026-11-06T03:53:36.585Z | 35.8436 |
| letta-ai/letta | 2026-11-04T16:03:00.606Z | 2026-11-06T03:53:37.487Z | 35.8436 |
| getzep/graphiti | 2026-11-04T16:03:25.087Z | 2026-11-06T03:54:17.488Z | 35.8479 |
| MemTensor/MemOS | 2026-11-04T16:03:26.008Z | 2026-11-06T03:54:18.385Z | 35.8479 |
| thedotmack/claude-mem | 2026-11-04T16:03:54.797Z | 2026-11-06T03:54:40.999Z | 35.8462 |
| xiaowu0162/LongMemEval | 2026-11-04T16:03:55.651Z | 2026-11-06T03:54:41.843Z | 35.8462 |
| xiaowu0162/LongMemEval-V2 | 2026-11-04T16:04:18.029Z | 2026-11-06T03:54:59.738Z | 35.8449 |
| letta-ai/letta-code | 2026-11-04T16:04:18.938Z | 2026-11-06T03:55:00.611Z | 35.8449 |
| vectorize-io/hindsight | 2026-11-04T16:04:38.595Z | 2026-11-06T03:55:22.007Z | 35.8454 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-04T16:04:39.606Z | 2026-11-06T03:55:22.876Z | 35.8454 |
| VectorSpaceLab/general-agentic-memory | 2026-11-04T16:05:00.627Z | 2026-11-06T03:55:40.648Z | 35.8445 |
| agiresearch/A-mem | 2026-11-04T16:05:01.642Z | 2026-11-06T03:55:41.539Z | 35.8444 |
| memodb-io/memobase | 2026-11-04T16:05:21.187Z | 2026-11-06T03:55:57.725Z | 35.8435 |
| neo4j-labs/agent-memory | 2026-11-04T16:05:22.179Z | 2026-11-06T03:55:58.714Z | 35.8435 |
| volcengine/OpenViking | 2026-11-04T16:05:41.142Z | 2026-11-06T03:56:18.715Z | 35.8438 |
| vectorize-io/agent-memory-benchmark | 2026-11-04T16:05:42.125Z | 2026-11-06T03:56:19.625Z | 35.8438 |
| redis/agent-memory-server | 2026-11-04T16:06:03.836Z | 2026-11-06T03:56:37.721Z | 35.8427 |
| topoteretes/cognee | 2026-11-04T16:06:04.804Z | 2026-11-06T03:56:38.676Z | 35.8427 |
| MemTensor/MemRL | 2026-11-04T16:06:25.597Z | 2026-11-06T04:03:02.686Z | 35.9436 |
| obra/episodic-memory | 2026-11-04T16:06:26.501Z | 2026-11-06T04:03:03.786Z | 35.9437 |
| tigerless-labs/agent-memory | 2026-11-04T16:06:49.651Z | 2026-11-06T04:03:24.200Z | 35.9429 |

### 发现与参考覆盖

- `"long-term memory" in:name,description archived:false fork:false`：page=1，per_page=20，sort=updated，order=desc，returned=20，total_count=4733，incomplete_results=False，pagination_complete=False；观察 UTC 2026-11-06T04:04:18.291Z。
- `"memory consolidation" in:name,description created:>=2026-10-07 archived:false fork:false`：page=1，per_page=20，sort=updated，order=desc，returned=12，total_count=12，incomplete_results=False，pagination_complete=True；观察 UTC 2026-11-06T04:04:19.564Z。
- [Verging Labs JSON](https://verginglabs.com/index/memory.json)工具返回缓存版本 v0.2（2026-09-16、datasetId=6b0dd2681430eca3），标记6天前抓取；未证实源站实时刷新。[changelog](https://verginglabs.com/changelog)本轮返回404，未能核对其当前变更。参考覆盖不完整，不新增榜单技术结论。

</details>
