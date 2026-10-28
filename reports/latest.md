# Agent Memory 简报｜2026-10-28

OpenViking v0.5.2.1 暂停新敏感值自动识别；Claude Mem 与 Letta Code 也有正式版本更新。
受影响的主要是依赖 Session 自动脱敏、保存 Agent 交付文件或读取大量图片历史的使用者。
升级前先核对隐私值登记与文件副本保留策略；Hindsight、Graphiti 的下列主分支修改仍需等待适用版本并验证。

## 已确认合并/发布的变更

| 项目 | 变化 | 发布状态 | 影响与行动 |
| --- | --- | --- | --- |
| [OpenViking](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2.1) | 暂停 Session 新敏感值探测；保留已登记值替换与历史引用还原 | 已发布 v0.5.2.1 | 新值可能原样保存，不能继续依赖自动发现；核对已登记范围。没有运行时开关，也不清理旧隐私记录。SDK 最低依赖升至0.1.17。 |
| [Claude Mem](https://github.com/thedotmack/claude-mem/releases/tag/v15.3.0) | Stop/SubagentStop 保存交付文件副本，在 My Work 提供入口；此前的检查点和可选数据库快照进入版本 | 已发布 v15.3.0 | 本地副本可超出原工作树生命周期；每次最多50文件、单文件512 MiB，私密回合及远端 worker 跳过。检查磁盘与保留策略，必要时关闭捕获。 |
| [Letta Code](https://github.com/letta-ai/letta-code/releases/tag/v0.34.26) | 流式读取本地历史，在内存中省略上下文外图片；反思配置404兼容修复进入版本 | 已发布 v0.34.26 | 适用于图片密集长会话；原始 JSONL 不改写。空上下文 ID 列表仍保留图片，内存收益未测量。 |
| [Hindsight](https://github.com/vectorize-io/hindsight/commit/e68ff798a9c1434e7c486c969d8226713661da05) | 保存事实的 where 维度；抽取持续超限且不能再分割时明确失败，替代静默返回空事实 | 已合并，未确认新 Release（本轮最新为 v1.1.0） | 使用主分支者应处理错误与重试；不能把该失败路径视为已成功保存。 |
| [Graphiti](https://github.com/getzep/graphiti/commit/5f7cda913854ab932b91c02e6a50970598641ecd) | 移除 Gemini 提示词中重复的 schema，保留原生结构化输出及解析 | 已合并，未确认新 Release（本轮最新为 v0.31.2） | Gemini 适配器用户可跟踪；未测量 Token、质量或延迟变化。 |

## Star 变化：两次真实观测，间隔约35.38–35.40小时

起点为 UTC 2026-10-26 16:09–16:14，终点为 UTC 2026-10-28 03:33–03:37，逐项目精确时刻见下方证据区。7日与30日目标时刻均没有 ±6小时内的合格基线（0/21）；以下净变化不外推为日增长或周增长。按类别排列，类别内沿用登记顺序，关注度不代表质量。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 实际区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 67849 | 67949 | +100 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32242 | 32291 | +49 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12111 | 12136 | +25 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 103325 | 103768 | +443 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3711 | 3720 | +9 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 54046 | 54466 | +420 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 29979 | 30033 | +54 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2938 | 2939 | +1 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 592 | 595 | +3 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 40877 | 40977 | +100 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 323 | 323 | 0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 32776 | 32830 | +54 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 493 | 493 | 0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4733 | 4741 | +8 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 863 | 863 | 0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1208 | 1210 | +2 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 192 | 192 | 0 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1174 | 1177 | +3 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 197 | 198 | +1 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 158 | 157 | -1 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25262 | 25270 | +8 |

## 新候选对比

两条发现查询各读取一页、各返回20条；本轮未完成新候选初审，未新增登记或晋升。以下仅为新建仓库查询命中的待审线索，不能据名称推断记忆实现。现有登记池仍为20个正式项目、1个历史参考和26个待审候选。

| 线索 | 来源 | 记忆载体与检索 | 依赖、许可证与成熟度 | 本轮处理 |
| --- | --- | --- | --- | --- |
| [AgentMemoryRepo/agentmemoryrepo](https://github.com/AgentMemoryRepo/agentmemoryrepo) | 新建仓库查询，ID 1404874984 | 未核实 | 未核实 | 保留发现记录，等待初审 |
| [hsuanshao/AgentMemory](https://github.com/hsuanshao/AgentMemory) | 新建仓库查询，ID 1424257839 | 未核实 | 未核实 | 保留发现记录，等待初审 |
| [rlaope/deepseek-bot](https://github.com/rlaope/deepseek-bot) | 新建仓库查询，ID 1406980768 | 未核实 | 未核实 | 保留发现记录，等待初审 |

## 方法与边界

21个项目的元数据、HEAD 和 Release 增量来源均取回；深读限于预选的5个项目和下列文件。代码阅读支持实现描述，Release 是上游发布声明；未运行上游、未独立复现效果。搜索结果的总量、排序与分页完整性未知，不代表全网普查；已核实的5项变化不代表8个变动 HEAD 的全部差异均已审查。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261028T033033Z-interactive`；完成观察 UTC 2026-10-28T03:46:20.814Z。兼容标签 `interactive` 不是触发来源证明，本轮来源仍为 unknown/unverified。[原始快照](../data/snapshots/2026/10/20261028T033033Z-interactive.json)；[索引](../state/validation-index.json)；[运行状态](../state/status.json)。

### thedotmack/claude-mem

- Stop/SubagentStop 将符合条件的交付文件复制到本地项目目录，并在 My Work 提供入口；每次最多50个文件、单文件512 MiB，私密回合和远端 worker 跳过。可通过 CLAUDE_MEM_DELIVERABLES_ENABLED=false 关闭；用户应检查副本保留与磁盘占用。上一轮检查的转录检查点与可选数据库快照也已列入此版本。
- 状态 `released`；证据等级 `code_inspected`（仅下列实现）；Release 正文仍属 `upstream_statement`。
- [一手来源](https://github.com/thedotmack/claude-mem/releases/tag/v15.3.0)；事件 UTC 2026-10-26T23:57:00Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 来源版本 `43c5b2ead715859fce70c56c95fff5a6d77804c0`；本轮默认分支采样 `96737c36e49efeaf33497c2710ff16ffa558fcc4`，UTC 2026-10-28T03:35:38.430Z。
- 已读：[src/cli/deliverables-capture.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/cli/deliverables-capture.ts)；[src/cli/handlers/summarize.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/cli/handlers/summarize.ts)；[src/shared/deliverables.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/shared/deliverables.ts)。

### letta-ai/letta-code

- 完整历史按 JSONL 流式读取；不在当前上下文中的图片内容在内存里替换为短占位符，原 messages.jsonl 不重写，空上下文 ID 列表保留所有图片。Release 也列入上一轮的反思配置404兼容修复。图片密集长会话的内存影响未测量。
- 状态 `released`；证据等级 `code_inspected`（仅下列实现）；Release 正文仍属 `upstream_statement`。
- [一手来源](https://github.com/letta-ai/letta-code/releases/tag/v0.34.26)；事件 UTC 2026-10-28T02:48:19Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 来源版本 `a3f7ee2d90732d36fd35c4baf97156d50f128987`；本轮默认分支采样 `5dea67021b99810707ff753db35e4534f70ff1fd`，UTC 2026-10-28T03:35:53.634Z。
- 已读：[src/backend/local/local-transcript-history.ts](https://github.com/letta-ai/letta-code/blob/a3f7ee2d90732d36fd35c4baf97156d50f128987/src/backend/local/local-transcript-history.ts)。

### volcengine/OpenViking

- 为减少误报造成的内容替换与无效隐私记录，新敏感值的规则探测及敏感字段捕获在代码中禁用，没有运行时开关；已登记值的替换与历史引用还原保留。未登记的新敏感内容可能原样持久化，升级者需核对已有登记范围；本次不清理旧记录。Release 同时列入 SDK 最低依赖0.1.17。
- 状态 `released`；证据等级 `code_inspected`（仅下列实现）；Release 正文仍属 `upstream_statement`。
- [一手来源](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2.1)；[合并 PR](https://github.com/volcengine/OpenViking/pull/6680)；事件 UTC 2026-10-27T13:44:25Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 来源版本 `3f85145b71a8e011df4deba1eced057b0409f147`；本轮默认分支采样 `54d4c0fac91fae976325ebed618d7278ff9b5c77`，UTC 2026-10-28T03:36:54.304Z。
- 已读：[openviking/privacy/session_extractor.py](https://github.com/volcengine/OpenViking/blob/3f85145b71a8e011df4deba1eced057b0409f147/openviking/privacy/session_extractor.py)；[docs/zh/concepts/13-privacy.md](https://github.com/volcengine/OpenViking/blob/3f85145b71a8e011df4deba1eced057b0409f147/docs/zh/concepts/13-privacy.md)。

### getzep/graphiti

- Gemini 客户端移除提示词中重复的 schema 文本，保留原生 response_schema、JSON MIME 和响应模型解析。使用该适配器的部署可跟踪此修改；没有证据量化 Token 或质量收益。
- 状态 `merged_unreleased`；证据等级 `code_inspected`（仅下列实现）；Release 正文仍属 `upstream_statement`。
- [一手来源](https://github.com/getzep/graphiti/commit/5f7cda913854ab932b91c02e6a50970598641ecd)；事件 UTC 2026-10-27T18:02:32Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 来源版本 `5f7cda913854ab932b91c02e6a50970598641ecd`；本轮默认分支采样 `efc40d21b0afe28d6fc31d8c2c3e05752b02a9f1`，UTC 2026-10-28T03:34:44.026Z。
- 已读：[graphiti_core/llm_client/gemini_client.py](https://github.com/getzep/graphiti/blob/5f7cda913854ab932b91c02e6a50970598641ecd/graphiti_core/llm_client/gemini_client.py)。

### vectorize-io/hindsight

- 事实抽取结果包含 where 维度；输出持续超限且内容已无法继续分割时抛出 RuntimeError，替代返回空事实后静默丢弃。调用方应处理失败与重试，不能继续将该情形视为成功保存；尚未确认进入新 Release。
- 状态 `merged_unreleased`；证据等级 `code_inspected`（仅下列实现）；Release 正文仍属 `upstream_statement`。
- [一手来源](https://github.com/vectorize-io/hindsight/commit/e68ff798a9c1434e7c486c969d8226713661da05)；事件 UTC 2026-10-27T09:57:15Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 来源版本 `e68ff798a9c1434e7c486c969d8226713661da05`；本轮默认分支采样 `1e3a4841a7eed5d76e796d2f31e5f0a13e78e5cf`，UTC 2026-10-28T03:36:09.831Z。
- 已读：[hindsight-api-slim/hindsight_api/engine/retain/fact_extraction.py](https://github.com/vectorize-io/hindsight/blob/e68ff798a9c1434e7c486c969d8226713661da05/hindsight-api-slim/hindsight_api/engine/retain/fact_extraction.py)。


### Star 实际区间

| 项目 | 起点 UTC | 终点 UTC | 经过小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-10-26T16:09:55.058Z | 2026-10-28T03:33:36.386Z | 35.3948 |
| letta-ai/letta | 2026-10-26T16:09:55.582Z | 2026-10-28T03:33:36.490Z | 35.3947 |
| getzep/graphiti | 2026-10-26T16:10:20.016Z | 2026-10-28T03:34:27.157Z | 35.4020 |
| MemTensor/MemOS | 2026-10-26T16:10:20.539Z | 2026-10-28T03:34:27.255Z | 35.4019 |
| thedotmack/claude-mem | 2026-10-26T16:11:20.123Z | 2026-10-28T03:35:24.533Z | 35.4012 |
| xiaowu0162/LongMemEval | 2026-10-26T16:11:20.546Z | 2026-10-28T03:35:24.501Z | 35.4011 |
| xiaowu0162/LongMemEval-V2 | 2026-10-26T16:11:53.748Z | 2026-10-28T03:35:45.672Z | 35.3978 |
| letta-ai/letta-code | 2026-10-26T16:11:54.290Z | 2026-10-28T03:35:45.616Z | 35.3976 |
| vectorize-io/hindsight | 2026-10-26T16:12:24.140Z | 2026-10-28T03:36:01.170Z | 35.3936 |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-26T16:12:24.881Z | 2026-10-28T03:36:01.104Z | 35.3934 |
| VectorSpaceLab/general-agentic-memory | 2026-10-26T16:12:46.357Z | 2026-10-28T03:36:20.928Z | 35.3929 |
| agiresearch/A-mem | 2026-10-26T16:12:46.821Z | 2026-10-28T03:36:21.074Z | 35.3928 |
| memodb-io/memobase | 2026-10-26T16:13:11.217Z | 2026-10-28T03:36:35.602Z | 35.3901 |
| neo4j-labs/agent-memory | 2026-10-26T16:13:11.966Z | 2026-10-28T03:36:35.762Z | 35.3899 |
| volcengine/OpenViking | 2026-10-26T16:13:36.726Z | 2026-10-28T03:36:48.586Z | 35.3866 |
| vectorize-io/agent-memory-benchmark | 2026-10-26T16:13:37.367Z | 2026-10-28T03:36:48.702Z | 35.3865 |
| redis/agent-memory-server | 2026-10-26T16:14:02.383Z | 2026-10-28T03:37:02.819Z | 35.3835 |
| topoteretes/cognee | 2026-10-26T16:14:02.930Z | 2026-10-28T03:37:02.891Z | 35.3833 |
| MemTensor/MemRL | 2026-10-26T16:14:24.367Z | 2026-10-28T03:37:20.749Z | 35.3823 |
| obra/episodic-memory | 2026-10-26T16:14:24.796Z | 2026-10-28T03:37:20.846Z | 35.3822 |
| tigerless-labs/agent-memory | 2026-10-26T16:14:46.832Z | 2026-10-28T03:37:39.044Z | 35.3812 |

### 发现范围

- 查询 `"agent memory" in:name,description archived:false fork:false`，page=1，per_page=20，返回20，UTC 2026-10-28T03:37:59.900Z；sort/incomplete_results/pagination_complete/total_count 均未暴露，记为 null。
- 查询 `"agent memory" in:name,description created:>=2026-09-28 archived:false fork:false`，page=1，per_page=20，返回20，UTC 2026-10-28T03:37:59.707Z；sort/incomplete_results/pagination_complete/total_count 均未暴露，记为 null。

原始线索保存在快照的 discovery 中，未自动纳入候选池。外部方法对照本轮未确认新变化；ISO 2026-W43 已有归档，W44 尚未闭合。后续审查与结构化事件回填保留在运行待办。

</details>
