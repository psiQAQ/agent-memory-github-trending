# Agent Memory 简报｜2026-10-29

Claude Mem v15.5.0 扩展可选通用脱敏；Letta Code v0.34.29 修复断线时待完成工具请求的重发。
受影响的主要是保存工具输出、处理凭据文本，或依赖远端外部工具完成操作的使用者。
升级前核对脱敏开关与服务端去重；源码核对支持上述实现描述，实际效果仍需在自己的环境验证。

## 已确认合并/发布的变更

| 项目 | 变化 | 发布状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v15.5.0) | 可选通用脱敏规则识别配置形态中的裸 token、secret、api_key 键；通用规则默认关闭，值仍须至少8个允许字符且含字母。 | 已发布 v15.5.0 | 依赖工具输出脱敏的使用者应核对 CLAUDE_MEM_REDACT_GENERIC_ENABLED 与禁用规则列表，并用自己的输入验证；不能假定所有同名标识符或历史记录都会被处理。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/releases/tag/v0.34.29) | 临时断线重连后，以原 request_id 重发仍待响应的外部工具请求；当前连接已发送的请求会跳过，失效或取消的所属回合会拒绝重发。 | 已发布 v0.34.29 | 使用外部工具的部署应核对服务端按 request_id 去重。默认总等待仍为5分钟，工具可覆盖超时；超时后远端结果未知，写操作重试前先核对目标。 |

## Star 变化：两次真实观测，间隔约27.64–27.66小时

起点为 UTC 2026-10-28 的逐项目观测，终点为 UTC 2026-10-29；精确时刻见证据区。7日/30日目标时刻在 ±6小时内的合格基线分别为 21/21、0/21；下表只比较两次真实观测，不外推日增长或周增长。按类别与登记顺序排列，关注度不代表质量。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 实际区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 67949 | 68026 | +77 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32291 | 32322 | +31 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12136 | 12167 | +31 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 103768 | 104118 | +350 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3720 | 3732 | +12 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 54466 | 55758 | +1292 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30033 | 30076 | +43 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2939 | 2941 | +2 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 595 | 596 | +1 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 40977 | 41090 | +113 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 323 | 323 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 32830 | 32874 | +44 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 493 | 493 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4741 | 4373 | -368 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 863 | 864 | +1 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1210 | 1210 | +0 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 192 | 193 | +1 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1177 | 1180 | +3 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 198 | 198 | +0 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 157 | 159 | +2 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25270 | 25281 | +11 |

tigerless-labs/agent-memory 在同一仓库 ID 下减少368 Stars，Hindsight 增加1292 Stars；原因未核实，不能据此判断操纵或技术质量。

## 新候选对比

两条查询分别返回20条，本轮不新增候选或晋升，登记池保持20个正式项目、1个历史参考、26个待审候选。下列仅为发现线索，未读源码或完成初审；完整命中列表保留在原始快照。

| 线索 | 发现依据 | 记忆载体与检索 | 依赖、许可证、成熟度 | 处理 |
| --- | --- | --- | --- | --- |
| [Rangow4562/ThreadForge](https://github.com/Rangow4562/ThreadForge) | 新建仓库查询；ID 1426878857 | 未核实 | 未核实 | 待初审，不纳入质量比较 |
| [synuns/flint](https://github.com/synuns/flint) | 新建仓库查询；ID 1428177595 | 未核实 | 未核实 | 待初审，不纳入质量比较 |
| [zhongwei2023/agent-memory-metric-audit](https://github.com/zhongwei2023/agent-memory-metric-audit) | 新建仓库查询；ID 1437960608 | 未核实 | 未核实 | 待初审，不纳入质量比较 |

## 方法与边界

21个项目的元数据、HEAD、Release 增量范围均取回。本轮预选并完成2个项目的重点深读，未审查其他变动 HEAD 的全部差异；未运行上游程序或独立复现。两条搜索的 incomplete_results 均为 false，但均还有后续页面；每条只读第一页，不能当作完整普查。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261029T070619Z-interactive`；观察完成 UTC 2026-10-29T07:26:10.343Z。这是所有者要求的今日手动补跑；平台触发回执未暴露，公开来源认证仍为 unknown/unverified，不代表自然定时验收。[原始快照](../data/snapshots/2026/10/20261029T070619Z-interactive.json)；[索引](../state/validation-index.json)；[运行状态](../state/status.json)。

### thedotmack/claude-mem

- [合并 PR](https://github.com/thedotmack/claude-mem/pull/5130)，合并 UTC 2026-10-28T04:39:09Z；[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.5.0) 发布时间 UTC 2026-10-29T00:48:22Z。
- 实现版本 `2bc22fa29d43045faafbd621abf14654c050d088`；发布标签解析为 `1c6accf711b4962af9fa1073c656d0f60a2c1dd2`；GitHub compare 已确认该修复是发布提交的祖先。观察 UTC 2026-10-29T07:26:10.343Z。
- 静态阅读：[src/utils/redaction.ts](https://github.com/thedotmack/claude-mem/blob/2bc22fa29d43045faafbd621abf14654c050d088/src/utils/redaction.ts)。
- 可选通用脱敏规则识别配置形态中的裸 token、secret、api_key 键；通用规则默认关闭，值仍须至少8个允许字符且含字母。 依赖工具输出脱敏的使用者应核对 CLAUDE_MEM_REDACT_GENERIC_ENABLED 与禁用规则列表，并用自己的输入验证；不能假定所有同名标识符或历史记录都会被处理。 Release/PR 的测试和效果陈述属上游声明，本轮没有执行它们。

### letta-ai/letta-code

- [合并 PR](https://github.com/letta-ai/letta-code/pull/5309)，合并 UTC 2026-10-29T04:57:21Z；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.29) 发布时间 UTC 2026-10-29T05:59:38Z。
- 实现版本 `2cc372d61a7ea7363f48229dc3c52752347cfd6d`；发布标签解析为 `e43d5d3725c3b8b55da0ab2ec25a4e722353f44a`；GitHub compare 已确认该修复是发布提交的祖先。观察 UTC 2026-10-29T07:26:10.343Z。
- 静态阅读：[src/websocket/listener/external-tools.ts](https://github.com/letta-ai/letta-code/blob/2cc372d61a7ea7363f48229dc3c52752347cfd6d/src/websocket/listener/external-tools.ts)；[src/websocket/listener/lifecycle.ts](https://github.com/letta-ai/letta-code/blob/2cc372d61a7ea7363f48229dc3c52752347cfd6d/src/websocket/listener/lifecycle.ts)。
- 临时断线重连后，以原 request_id 重发仍待响应的外部工具请求；当前连接已发送的请求会跳过，失效或取消的所属回合会拒绝重发。 使用外部工具的部署应核对服务端按 request_id 去重。默认总等待仍为5分钟，工具可覆盖超时；超时后远端结果未知，写操作重试前先核对目标。 Release/PR 的测试和效果陈述属上游声明，本轮没有执行它们。

### 逐项目观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-10-28T03:33:36.386Z | 2026-10-29T07:13:10.947Z | 27.6596 |
| letta-ai/letta | 2026-10-28T03:33:36.490Z | 2026-10-29T07:13:13.884Z | 27.6604 |
| getzep/graphiti | 2026-10-28T03:34:27.157Z | 2026-10-29T07:13:40.559Z | 27.6537 |
| MemTensor/MemOS | 2026-10-28T03:34:27.255Z | 2026-10-29T07:13:44.329Z | 27.6547 |
| thedotmack/claude-mem | 2026-10-28T03:35:24.533Z | 2026-10-29T07:14:02.716Z | 27.6439 |
| xiaowu0162/LongMemEval | 2026-10-28T03:35:24.501Z | 2026-10-29T07:14:05.607Z | 27.6448 |
| xiaowu0162/LongMemEval-V2 | 2026-10-28T03:35:45.672Z | 2026-10-29T07:14:29.455Z | 27.6455 |
| letta-ai/letta-code | 2026-10-28T03:35:45.616Z | 2026-10-29T07:14:32.104Z | 27.6462 |
| vectorize-io/hindsight | 2026-10-28T03:36:01.170Z | 2026-10-29T07:14:55.587Z | 27.6484 |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-28T03:36:01.104Z | 2026-10-29T07:14:59.380Z | 27.6495 |
| VectorSpaceLab/general-agentic-memory | 2026-10-28T03:36:20.928Z | 2026-10-29T07:15:17.388Z | 27.6490 |
| agiresearch/A-mem | 2026-10-28T03:36:21.074Z | 2026-10-29T07:15:20.085Z | 27.6497 |
| memodb-io/memobase | 2026-10-28T03:36:35.602Z | 2026-10-29T07:15:43.717Z | 27.6523 |
| neo4j-labs/agent-memory | 2026-10-28T03:36:35.762Z | 2026-10-29T07:15:46.336Z | 27.6529 |
| volcengine/OpenViking | 2026-10-28T03:36:48.586Z | 2026-10-29T07:16:05.968Z | 27.6548 |
| vectorize-io/agent-memory-benchmark | 2026-10-28T03:36:48.702Z | 2026-10-29T07:16:10.145Z | 27.6560 |
| redis/agent-memory-server | 2026-10-28T03:37:02.819Z | 2026-10-29T07:16:31.996Z | 27.6581 |
| topoteretes/cognee | 2026-10-28T03:37:02.891Z | 2026-10-29T07:16:35.956Z | 27.6592 |
| MemTensor/MemRL | 2026-10-28T03:37:20.749Z | 2026-10-29T07:16:59.471Z | 27.6608 |
| obra/episodic-memory | 2026-10-28T03:37:20.846Z | 2026-10-29T07:17:02.530Z | 27.6616 |
| tigerless-labs/agent-memory | 2026-10-28T03:37:39.044Z | 2026-10-29T07:17:25.311Z | 27.6629 |

### 发现覆盖

- `"coding agent memory" in:name,description archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；返回20，total_count=76，incomplete_results=false，pagination_complete=false；观察 UTC 2026-10-29T07:18:12.151Z。
- `"agent memory" in:name,description created:>=2026-09-29 archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；返回20，total_count=905，incomplete_results=false，pagination_complete=false；观察 UTC 2026-10-29T07:18:13.610Z。

</details>
