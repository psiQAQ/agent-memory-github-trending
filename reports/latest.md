# Agent Memory 简报｜2026-11-07

Claude-mem v15.10.1 保留被 429 限流拒绝的记忆批次；OpenViking 的 langchain-openviking 0.2.0 修正 Store 持久化边界和 Unicode 查询词约束。
主要影响 Claude observer 遇到限流文本的用户，以及使用该 LangChain/LangGraph 集成包、依赖路径型 key 或中文归档查询的用户。
建议受影响者评估对应版本并检查恢复写入与错误处理；本轮静态阅读不足以判断记忆质量或建议迁移系统。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/5430) | 识别 Claude CLI 以助手文本返回的 429 限流拒绝，把当前记忆批次重置为 pending 并暂停生成，避免第二次非 XML 回复导致批次被确认后丢弃。 | 已发布 [v15.10.1](https://github.com/thedotmack/claude-mem/releases/tag/v15.10.1) | 受影响者是使用 Claude observer、遇到这类限流文本的用户；可评估 v15.10.1，并在恢复后核对批次是否实际写入。普通提及数字 429 的文本及有效 observation/summary XML 不按此规则重排队。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7038) | LangGraph Store 以单个 URI 段编码含分隔符的 key；index=[] 保留 JSON 值并移除语义索引投影；写入与列举只忽略对应的明确缺失/已存在情形，其他后端错误向上抛出。归档文本搜索同时保留 Unicode 查询词约束。 | 已发布 [langchain-openviking@0.2.0](https://github.com/volcengine/OpenViking/releases/tag/langchain-openviking%400.2.0) | 受影响者是该 LangChain/LangGraph 集成包的使用者。可评估集成包 0.2.0，核对路径型 key 的往返读写、index=[] 的语义检索行为，并让上层区分“空结果”和权限/可用性错误。 |

本项限于识别到的限流拒绝；不能据此保证所有排队工作永久保留。该版本另有“持续无响应且恢复次数耗尽后丢弃缓冲”的不同策略，本轮未把它等同于限流保留。

这是 langchain-openviking 集成包发布，不是 OpenViking 主包新版本。Unicode 修正没有增加规范化或更宽的大小写等价，原有短 ASCII 词过滤仍保留；上述错误传播结论限于已审的 Store 路径。

## Star 变化：真实间隔约 12.15–12.55 小时

只比较两次实际观测，不外推为日增长。7日/30日合格基线分别为 21/21、0/21（容差 ±6 小时）；没有合格窗口的指标为“—”。逐项目起止 UTC 与时长见折叠区。Stars 反映关注度，不是质量或性能分。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 | 约7日净变化 | 实际天数 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68485 | 68515 | +30 | +408 | 7.0058 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32574 | 32593 | +19 | +226 | 7.0059 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12287 | 12301 | +14 | +102 | 7.0059 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 113621 | 113852 | +231 | +8165 | 7.0057 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3787 | 3793 | +6 | +52 | 7.0056 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 59161 | 59372 | +211 | +2916 | 7.0056 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30542 | 30571 | +29 | +316 | 7.0056 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2949 | 2950 | +1 | +8 | 7.0053 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 604 | 604 | +0 | +8 | 7.0053 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41649 | 41690 | +41 | +497 | 7.0053 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 325 | 325 | +0 | +2 | 7.0052 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33099 | 33112 | +13 | +185 | 7.0052 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 499 | 499 | +0 | +5 | 7.0051 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4307 | 4310 | +3 | -69 | 7.0217 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 868 | 868 | +0 | +4 | 7.0054 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1214 | 1214 | +0 | +2 | 7.0054 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 197 | 197 | +0 | +4 | 7.0051 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1197 | 1199 | +2 | +15 | 7.0057 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 203 | 202 | -1 | +3 | 7.0056 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 164 | 165 | +1 | +6 | 7.0053 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25362 | 25369 | +7 | +77 | 7.0058 |

## 新候选对比

两条无 Star 下限查询共取得 40 条原始结果；未做候选代码初审，未新增或晋升项目，登记池保持 47/50。下表只比较本次搜索描述，不能作为接入推荐。

| 原始线索 | 描述中的载体与维护 | 依赖/宿主线索 | 评测与成熟度 | API 许可线索 |
| --- | --- | --- | --- | --- |
| [synuns/flint](https://github.com/synuns/flint) | 带版本的 Agent 记忆；描述提及人类笔记与 Agent 记忆衔接 | Doltgres、MCP、Obsidian；实际必需关系未核实 | 未核实 | 未提供 |
| [AstrBot whale_dream](https://github.com/Treetreewu/astrbot_plugin_whale_dream) | 描述称闲时记忆整理与长期 persona 演进 | AstrBot、固定版本 LivingMemory bridge；实现未核实 | 未核实 | AGPL-3.0 |

## 方法与边界

21个登记项目的 metadata、HEAD 与 Release 增量覆盖均已核对；两项预选 Release 完成相关 PR、实际 tag 包含关系和固定源码审读，其他变化仍待审。未运行上游代码、测试或付费评测，证据等级为 code_inspected；上游测试声明不算本项目独立复现。发现查询是有界样本，不代表 GitHub 全量生态。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261106T160206Z-local`；观测汇总 UTC 2026-11-06T16:36:35.428Z，展示日期按北京时间计算，与 run_id 分别保存。[原始快照](../data/snapshots/2026/11/20261106T160206Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。本轮复用已完成采集，各来源保留真实返回时间；触发来源 unknown/unverified，人工恢复不证明自然 Scheduled 执行。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/5430) 合并 UTC 2026-11-06T05:27:34Z，合并 SHA `0df5cfec2590c0e47002191a9f249a40be53f43a`。[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.10.1) 发布 UTC 2026-11-06T11:52:02Z，实际 tag commit `016c4c34c01f77790b3d47f867319fadf300e49d`。审读观察 UTC 2026-11-06T16:40:39.338Z。annotated tag 解引用至 016c4c3；其到已读 HEAD 51fb777 的 compare 只有 docs/CHANGELOG.md，两个版本的所读 classifier/ResponseProcessor 代码一致；GeneratorRunner 直接按 tag commit 读取。

阅读范围：[src/sdk/output-classifier.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/sdk/output-classifier.ts)；[src/services/worker/agents/ResponseProcessor.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/services/worker/agents/ResponseProcessor.ts)；[src/services/worker/session/GeneratorRunner.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/services/worker/session/GeneratorRunner.ts)。

### volcengine/OpenViking

[PR](https://github.com/volcengine/OpenViking/pull/7038) 合并 UTC 2026-11-06T10:05:35Z，合并 SHA `f5ffab0a73ab3a54f83db7ea6b264bd9505e76be`。[Release](https://github.com/volcengine/OpenViking/releases/tag/langchain-openviking%400.2.0) 发布 UTC 2026-11-06T11:06:58Z，实际 tag commit `b8e88959f3ab437b4d08514eceaa7221cca470dc`。审读观察 UTC 2026-11-06T16:39:37.116Z。实际轻量 tag 指向 b8e8895；分别从 PR7038、PR7040 合并 commit 到该 tag 的 compare 均确认包含关系。

阅读范围：[integrations/frameworks/langchain/src/langchain_openviking/store.py](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/src/langchain_openviking/store.py)；[integrations/frameworks/langchain/src/langchain_openviking/tools.py](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/src/langchain_openviking/tools.py)；[integrations/frameworks/langchain/pyproject.toml](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/pyproject.toml)。

[Unicode 查询 PR](https://github.com/volcengine/OpenViking/pull/7040) 合并 UTC 2026-11-06T10:05:45Z，合并 SHA `8dc1121102ab80378bac6e29a5ec2be798839717`。

### 逐项目 Star 观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-06T03:53:36.585Z | 2026-11-06T16:09:03.863Z | 12.2576 |
| letta-ai/letta | 2026-11-06T03:53:37.487Z | 2026-11-06T16:09:04.809Z | 12.2576 |
| getzep/graphiti | 2026-11-06T03:54:17.488Z | 2026-11-06T16:09:40.671Z | 12.2564 |
| MemTensor/MemOS | 2026-11-06T03:54:18.385Z | 2026-11-06T16:09:41.582Z | 12.2564 |
| thedotmack/claude-mem | 2026-11-06T03:54:40.999Z | 2026-11-06T16:09:54.950Z | 12.2539 |
| xiaowu0162/LongMemEval | 2026-11-06T03:54:41.843Z | 2026-11-06T16:09:55.842Z | 12.2539 |
| xiaowu0162/LongMemEval-V2 | 2026-11-06T03:54:59.738Z | 2026-11-06T16:10:10.390Z | 12.2530 |
| letta-ai/letta-code | 2026-11-06T03:55:00.611Z | 2026-11-06T16:10:11.296Z | 12.2530 |
| vectorize-io/hindsight | 2026-11-06T03:55:22.007Z | 2026-11-06T16:10:36.152Z | 12.2539 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-06T03:55:22.876Z | 2026-11-06T16:10:37.104Z | 12.2540 |
| VectorSpaceLab/general-agentic-memory | 2026-11-06T03:55:40.648Z | 2026-11-06T16:10:52.505Z | 12.2533 |
| agiresearch/A-mem | 2026-11-06T03:55:41.539Z | 2026-11-06T16:10:53.564Z | 12.2533 |
| memodb-io/memobase | 2026-11-06T03:55:57.725Z | 2026-11-06T16:11:06.820Z | 12.2525 |
| neo4j-labs/agent-memory | 2026-11-06T03:55:58.714Z | 2026-11-06T16:11:07.844Z | 12.2525 |
| volcengine/OpenViking | 2026-11-06T03:56:18.715Z | 2026-11-06T16:11:31.401Z | 12.2535 |
| vectorize-io/agent-memory-benchmark | 2026-11-06T03:56:19.625Z | 2026-11-06T16:11:32.378Z | 12.2535 |
| redis/agent-memory-server | 2026-11-06T03:56:37.721Z | 2026-11-06T16:11:47.727Z | 12.2528 |
| topoteretes/cognee | 2026-11-06T03:56:38.676Z | 2026-11-06T16:11:48.724Z | 12.2528 |
| MemTensor/MemRL | 2026-11-06T04:03:02.686Z | 2026-11-06T16:12:03.915Z | 12.1503 |
| obra/episodic-memory | 2026-11-06T04:03:03.786Z | 2026-11-06T16:12:04.810Z | 12.1503 |
| tigerless-labs/agent-memory | 2026-11-06T04:03:24.200Z | 2026-11-06T16:36:29.212Z | 12.5514 |

### 约7日窗口的真实基线

| 项目 | 基线 UTC | 终点 UTC | 实际天数 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-10-30T16:00:41.086Z | 2026-11-06T16:09:03.863Z | 7.005819 |
| letta-ai/letta | 2026-10-30T16:00:42.539Z | 2026-11-06T16:09:04.809Z | 7.005813 |
| getzep/graphiti | 2026-10-30T16:01:09.257Z | 2026-11-06T16:09:40.671Z | 7.005919 |
| MemTensor/MemOS | 2026-10-30T16:01:10.251Z | 2026-11-06T16:09:41.582Z | 7.005918 |
| thedotmack/claude-mem | 2026-10-30T16:01:41.876Z | 2026-11-06T16:09:54.950Z | 7.005707 |
| xiaowu0162/LongMemEval | 2026-10-30T16:01:42.723Z | 2026-11-06T16:09:55.842Z | 7.005707 |
| xiaowu0162/LongMemEval-V2 | 2026-10-30T16:02:07.260Z | 2026-11-06T16:10:10.390Z | 7.005592 |
| letta-ai/letta-code | 2026-10-30T16:02:08.149Z | 2026-11-06T16:10:11.296Z | 7.005592 |
| vectorize-io/hindsight | 2026-10-30T16:02:33.957Z | 2026-11-06T16:10:36.152Z | 7.005581 |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-30T16:02:34.859Z | 2026-11-06T16:10:37.104Z | 7.005582 |
| VectorSpaceLab/general-agentic-memory | 2026-10-30T16:03:04.725Z | 2026-11-06T16:10:52.505Z | 7.005414 |
| agiresearch/A-mem | 2026-10-30T16:03:05.641Z | 2026-11-06T16:10:53.564Z | 7.005416 |
| memodb-io/memobase | 2026-10-30T16:03:29.150Z | 2026-11-06T16:11:06.820Z | 7.005297 |
| neo4j-labs/agent-memory | 2026-10-30T16:03:30.143Z | 2026-11-06T16:11:07.844Z | 7.005297 |
| volcengine/OpenViking | 2026-10-30T16:03:54.266Z | 2026-11-06T16:11:31.401Z | 7.005291 |
| vectorize-io/agent-memory-benchmark | 2026-10-30T16:03:55.204Z | 2026-11-06T16:11:32.378Z | 7.005291 |
| redis/agent-memory-server | 2026-10-30T16:04:19.608Z | 2026-11-06T16:11:47.727Z | 7.005187 |
| topoteretes/cognee | 2026-10-30T16:04:20.648Z | 2026-11-06T16:11:48.724Z | 7.005186 |
| MemTensor/MemRL | 2026-10-30T16:04:44.805Z | 2026-11-06T16:12:03.915Z | 7.005082 |
| obra/episodic-memory | 2026-10-30T16:04:45.671Z | 2026-11-06T16:12:04.810Z | 7.005083 |
| tigerless-labs/agent-memory | 2026-10-30T16:05:12.440Z | 2026-11-06T16:36:29.212Z | 7.021722 |

### 发现与参考覆盖

- `"memory consolidation" in:name,description archived:false fork:false`：page=1，per_page=20，sort=updated，order=desc，returned=20，total_count=312，incomplete_results=False，pagination_complete=False；观察 UTC 2026-11-06T16:36:33.774Z。
- `"agentic memory" in:name,description created:>=2026-10-07 archived:false fork:false`：page=1，per_page=20，sort=updated，order=desc，returned=20，total_count=652，incomplete_results=False，pagination_complete=False；观察 UTC 2026-11-06T16:36:35.428Z。
- 外部评测沿用[已有参考版本](../docs/references.md)，本轮未重新读取榜单，不判断其当前版本是否变化，也不新增跨协议分数比较。

</details>
