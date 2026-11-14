# Agent Memory 简报｜2026-11-12

Claude-mem v15.17.0 发布 eve 记忆集成。Hindsight 合并对重复事件和历史状态的整理修订。
eve 应用可接入已有 cmem.ai 记忆。依赖 Hindsight 判断当前状态的应用可关注乱序事实与重复事件。
eve 接入前核对凭据和项目作用域。Hindsight 修订在采集窗口内尚无对应发行版，先准备回归样例。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/5863) | 新增 eve 记忆 provider。含用户文本的回合开始时调用 cmem.ai 检索，显式调用 remember 时写入。 | 已发布 [v15.17.0](https://github.com/thedotmack/claude-mem/releases/tag/v15.17.0) | 接入 eve 前核对 cmem.ai 凭据和项目作用域。默认按作用域选项目，开启 searchAllProjects 会扩大检索范围。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6505) | 调整整理与反思提示，将不同时刻重复发生的事件分别记录，并标明观察记录中的历史状态。评测裁判也区分事实到达顺序与陈述时间。 | 已合并，本轮未见发布 | 依赖事件先后或当前状态的接入方，可将乱序输入和重复事件列入回归场景，待包含该修订的发行版确认后再评估升级。 |

源码显示，回合自动检索会转义召回文本，并在非取消的错误下给模型返回不可用提示。跨项目检索配置与显式写入的作用域是分别控制的。

Hindsight 的发布状态按本轮 Release 观测窗口判断。代码和提示词已核对，效果与模型差异未复现。

## Star 变化：真实间隔约 23.95–34.83 小时

7日/30日合格基线分别为 8/21、0/21，容差±6小时。下表比较两次实际观测的 Star 净变化，各项目起止时间见证据区。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68755 | 68812 | +57 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32713 | 32747 | +34 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12342 | 12359 | +17 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 115698 | 116102 | +404 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3813 | 3818 | +5 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 60270 | 60531 | +261 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30744 | 30795 | +51 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2957 | 2957 | +0 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 605 | 607 | +2 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41943 | 42029 | +86 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 326 | 326 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33215 | 33256 | +41 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 499 | 499 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4309 | 4315 | +6 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 869 | 869 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1214 | 1214 | +0 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 199 | 200 | +1 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1208 | 1210 | +2 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 208 | 209 | +1 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 165 | 167 | +2 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25406 | 25419 | +13 |

## 新候选对比

两条无 Star 下限查询共取得 40 条原始结果。候选代码初审0项、收录0项，登记池保持 47/50。下表只是搜索描述对照，依赖、宿主和评测尚未独立核实。

| 未审线索 | 搜索描述（上游自述） | 许可 API 线索 | 实现/评测/成熟度 |
| --- | --- | --- | --- |
| [frankalcantara/Arestrix](https://github.com/frankalcantara/Arestrix) | Arestrix is an AI Agent Operating System that provides a visual environment for building, coordinating, and running autonomous and multi-agent applications. It combines workflow orchestration, episodic memory, real-time observability, and L | MIT | 未核实 |
| [solidaxelproject/affective-episodic-memory](https://github.com/solidaxelproject/affective-episodic-memory) | A memory system for AI agents modeled on human memory: episodic, affective, reconstructive. | MIT | 未核实 |
| [bdobrica/SecondContext](https://github.com/bdobrica/SecondContext) | A goal-conditioned cognitive context layer for LLMs that combines salience-ranked episodic memory, belief updates, person/topic models, social-role graphs, and scenario simulation to improve future interactions. | Apache-2.0 | 未核实 |

## 方法与边界

21个项目的 metadata、HEAD 与 Release 增量均已覆盖；两项预选变化已阅读固定源码与 PR，其余变化待审。发现仅覆盖两页检索样本。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261111T160034Z-local`；观测汇总 UTC 2026-11-12T02:58:32.768Z，展示日期按北京时间计算。[原始快照](../data/snapshots/2026/11/20261111T160034Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。其中 8 个项目沿用自动化中断前的观测，其余项目来自本批次的人工续采。上游源码于 2026-11-14 静态核对，发布状态按原采集窗口判断。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/5863) 合并UTC 2026-11-11T06:09:07Z，SHA `4ab29a4377ab299d5e14554f585211adac8e022d`；发布UTC 2026-11-11T06:13:38Z。审读观察UTC 2026-11-14T00:28:06.133Z。发布标签指向的提交比 PR 合并提交领先 1 个提交、落后 0 个，且两个版本的 provider 文件 blob 相同。

阅读范围：[integrations/eve/provider/src/index.ts](https://github.com/thedotmack/claude-mem/blob/5681b2a3a9ec1be2c53264e6009ab82ad11ae601/integrations/eve/provider/src/index.ts)。

### vectorize-io/hindsight

[PR](https://github.com/vectorize-io/hindsight/pull/6505) 合并UTC 2026-11-11T13:56:15Z，SHA `6d9edd0d852c1a8f4161b302ce0ade4c83edd643`；发布UTC 未确认。审读观察UTC 2026-11-14T00:28:20.385Z。本轮 Release 增量观察至 2026-11-12T02:57:56.818Z，最新取得 v1.2.1 的发布时间早于该合并。固定 HEAD 对比包含该合并提交。

阅读范围：[hindsight-api-slim/hindsight_api/engine/consolidation/prompts.py](https://github.com/vectorize-io/hindsight/blob/6d9edd0d852c1a8f4161b302ce0ade4c83edd643/hindsight-api-slim/hindsight_api/engine/consolidation/prompts.py)；[hindsight-api-slim/hindsight_api/engine/reflect/prompts.py](https://github.com/vectorize-io/hindsight/blob/6d9edd0d852c1a8f4161b302ce0ade4c83edd643/hindsight-api-slim/hindsight_api/engine/reflect/prompts.py)；[hindsight-system-evals/hindsight_system_evals/consolidation.py](https://github.com/vectorize-io/hindsight/blob/6d9edd0d852c1a8f4161b302ce0ade4c83edd643/hindsight-system-evals/hindsight_system_evals/consolidation.py)。

### 逐项目Star观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-10T16:07:37.881Z | 2026-11-11T16:04:27.969Z | 23.9472 |
| letta-ai/letta | 2026-11-10T16:07:42.339Z | 2026-11-11T16:04:28.881Z | 23.9463 |
| getzep/graphiti | 2026-11-10T16:07:46.875Z | 2026-11-11T16:04:45.911Z | 23.9497 |
| MemTensor/MemOS | 2026-11-10T16:07:49.950Z | 2026-11-11T16:04:47.021Z | 23.9492 |
| thedotmack/claude-mem | 2026-11-10T16:07:52.936Z | 2026-11-11T16:05:06.494Z | 23.9538 |
| xiaowu0162/LongMemEval | 2026-11-10T16:07:56.124Z | 2026-11-11T16:05:07.607Z | 23.9532 |
| xiaowu0162/LongMemEval-V2 | 2026-11-10T16:07:59.745Z | 2026-11-11T16:05:26.983Z | 23.9576 |
| letta-ai/letta-code | 2026-11-10T16:08:03.698Z | 2026-11-11T16:05:28.070Z | 23.9568 |
| vectorize-io/hindsight | 2026-11-10T16:08:11.905Z | 2026-11-12T02:57:48.909Z | 34.8269 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-10T16:08:24.152Z | 2026-11-12T02:57:57.622Z | 34.8260 |
| VectorSpaceLab/general-agentic-memory | 2026-11-10T16:08:26.906Z | 2026-11-12T02:58:00.566Z | 34.8260 |
| agiresearch/A-mem | 2026-11-10T16:08:32.715Z | 2026-11-12T02:58:03.251Z | 34.8251 |
| memodb-io/memobase | 2026-11-10T16:08:36.706Z | 2026-11-12T02:58:05.601Z | 34.8247 |
| neo4j-labs/agent-memory | 2026-11-10T16:08:41.333Z | 2026-11-12T02:58:07.729Z | 34.8240 |
| volcengine/OpenViking | 2026-11-10T16:08:46.859Z | 2026-11-12T02:58:11.046Z | 34.8234 |
| vectorize-io/agent-memory-benchmark | 2026-11-10T16:08:55.529Z | 2026-11-12T02:58:13.870Z | 34.8218 |
| redis/agent-memory-server | 2026-11-10T16:08:58.212Z | 2026-11-12T02:58:16.196Z | 34.8217 |
| topoteretes/cognee | 2026-11-10T16:09:02.199Z | 2026-11-12T02:58:18.710Z | 34.8213 |
| MemTensor/MemRL | 2026-11-10T16:09:06.167Z | 2026-11-12T02:58:22.127Z | 34.8211 |
| obra/episodic-memory | 2026-11-10T16:09:09.827Z | 2026-11-12T02:58:25.237Z | 34.8209 |
| tigerless-labs/agent-memory | 2026-11-10T16:09:13.259Z | 2026-11-12T02:58:27.674Z | 34.8207 |

### 发现与参考覆盖

- `"episodic memory" in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-12T02:58:31.211Z。
- `"agentic memory" in:name,description created:>=2026-10-12 archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-12T02:58:32.768Z。
- 外部榜单沿用[已登记参考版本](../docs/references.md)，本轮未刷新其当前版本，不新增跨协议分数比较。

</details>
