# Agent Memory 简报｜2026-11-11

Claude-mem v15.15.1 收紧故障后补发范围。Hindsight v1.2.1 调整 Hermes 的会话追加写入。
依赖故障后补采的用户可能遇到采集缺口。依赖 Hermes 追加元数据的接入方需要核对字段。
升级时可分别核对 worker 可用性和追加文档的字段依赖。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/5663) | Cowork 遇到发送失败时丢弃提示、观察和摘要，补发队列只保留会话元数据；OpenCode 的会话初始化只发起一次请求。 | 已发布 [v15.15.1](https://github.com/thedotmack/claude-mem/releases/tag/v15.15.1) | 依赖停机后自动补采的用户可先核对采集缺口与 worker 可用性。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6291) | Hermes 向会话文档追加记忆时省去 retained_at、message_count 和 turn_index，避免随这些值变化反复更新旧记忆的元数据。 | 已发布 [v1.2.1](https://github.com/vectorize-io/hindsight/releases/tag/v1.2.1) | 从追加文档读取这些字段的接入方应核对字段依赖；非追加写入仍保留它们。 |

静态核对覆盖 Cowork 队列和 OpenCode 初始化。发布说明还称 transcript watcher 会跳过拒收行，本轮未对该路径做同等核对。

实现和回归测试均区分追加与非追加路径。写入量和延迟收益未实测。

OpenViking 本轮新增的是 [SuperAgent 0.5.1 预览版](https://github.com/volcengine/OpenViking/releases/tag/openviking-superagent%400.5.1-preview)。发布说明列出 macOS、Linux 和 WSL2 的安装入口，具体机制仍待核对。

## Star 变化：真实间隔约 24.10–24.11 小时

7日/30日合格基线分别为 21/21、0/21，容差±6小时。这里展示两次真实观测的净变化，不外推为日增长；Stars表示关注度，不是质量分。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68693 | 68755 | +62 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32679 | 32713 | +34 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12334 | 12342 | +8 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 115262 | 115698 | +436 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3806 | 3813 | +7 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 60059 | 60270 | +211 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30690 | 30744 | +54 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2955 | 2957 | +2 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 605 | 605 | +0 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41862 | 41943 | +81 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 326 | 326 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33180 | 33215 | +35 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 499 | 499 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4315 | 4309 | -6 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 869 | 869 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1214 | 1214 | +0 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 199 | 199 | +0 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1207 | 1208 | +1 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 207 | 208 | +1 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 165 | 165 | +0 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25394 | 25406 | +12 |

## 新候选对比

两条无Star下限查询共取得 34 条原始结果。候选代码初审0项、收录0项，登记池保持 47/50。下表只是搜索描述对照，依赖、宿主和评测尚未独立核实。

| 未审线索 | 搜索描述（上游自述） | 许可 API 线索 | 实现/评测/成熟度 |
| --- | --- | --- | --- |
| [linellazatin/nanomneme](https://github.com/linellazatin/nanomneme) | nanomneme is a small, deterministic SQLite core for coding-agent memory: useful context survives a session without becoming an opaque service | MIT | 未核实 |
| [chriswu727/agentdetox](https://github.com/chriswu727/agentdetox) | Protects coding agents&#x27; memory and instructions: blocks known-risk writes, detects suspicious changes, and supports reviewed cleanup and recovery. | Apache-2.0 | 未核实 |
| [tty-pt/pi-mm](https://github.com/tty-pt/pi-mm) | Pi coding agent &quot;memory mipmaps&quot; extension - persistent multi-resolution memory | BSD-2-Clause | 未核实 |

## 方法与边界

21个项目的 metadata、HEAD 与 Release 增量均已覆盖；两项预选变化完成固定源码及PR核对，其余变化范围保留待审。未运行上游代码、测试或付费评测；code_inspected不等于独立复现。有界发现不能代表GitHub全量生态。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261110T160048Z-local`；观测汇总 UTC 2026-11-10T16:09:21.792Z，展示日期按北京时间计算。[原始快照](../data/snapshots/2026/11/20261110T160048Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。触发来源unknown/unverified；人工执行不证明自然Scheduled。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/5663) 合并UTC 2026-11-10T06:50:02Z，SHA `856ee37c99119c817654e76af98df2a2de6d5f1f`；发布UTC 2026-11-10T07:06:39Z。审读观察UTC 2026-11-11T08:23:35.227Z。合并提交是发布提交的祖先，比较结果 ahead=1、behind=0。

阅读范围：[cowork/scripts/cmem-hook.mjs](https://github.com/thedotmack/claude-mem/blob/f00618f931cc21f2f871be7dee724029a772f017/cowork/scripts/cmem-hook.mjs)；[src/integrations/opencode-plugin/core.ts](https://github.com/thedotmack/claude-mem/blob/f00618f931cc21f2f871be7dee724029a772f017/src/integrations/opencode-plugin/core.ts)。

### vectorize-io/hindsight

[PR](https://github.com/vectorize-io/hindsight/pull/6291) 合并UTC 2026-11-03T14:25:59Z，SHA `acdc013b3c3508192c723d38392b716965ef3a3e`；发布UTC 2026-11-10T14:34:26Z。审读观察UTC 2026-11-11T08:23:38.541Z。合并提交是发布提交的祖先，比较结果 ahead=86、behind=0。

阅读范围：[hindsight-integrations/hermes/__init__.py](https://github.com/vectorize-io/hindsight/blob/0eb02d8c418eac6b489bc63883c993b2257dfac4/hindsight-integrations/hermes/__init__.py)；[hindsight-integrations/hermes/tests/test_provider.py](https://github.com/vectorize-io/hindsight/blob/0eb02d8c418eac6b489bc63883c993b2257dfac4/hindsight-integrations/hermes/tests/test_provider.py)。

### 逐项目Star观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-09T16:01:27.873Z | 2026-11-10T16:07:37.881Z | 24.1028 |
| letta-ai/letta | 2026-11-09T16:01:33.650Z | 2026-11-10T16:07:42.339Z | 24.1024 |
| getzep/graphiti | 2026-11-09T16:01:36.689Z | 2026-11-10T16:07:46.875Z | 24.1028 |
| MemTensor/MemOS | 2026-11-09T16:01:39.487Z | 2026-11-10T16:07:49.950Z | 24.1029 |
| thedotmack/claude-mem | 2026-11-09T16:01:42.593Z | 2026-11-10T16:07:52.936Z | 24.1029 |
| xiaowu0162/LongMemEval | 2026-11-09T16:01:45.089Z | 2026-11-10T16:07:56.124Z | 24.1031 |
| xiaowu0162/LongMemEval-V2 | 2026-11-09T16:01:48.175Z | 2026-11-10T16:07:59.745Z | 24.1032 |
| letta-ai/letta-code | 2026-11-09T16:01:51.980Z | 2026-11-10T16:08:03.698Z | 24.1033 |
| vectorize-io/hindsight | 2026-11-09T16:01:55.353Z | 2026-11-10T16:08:11.905Z | 24.1046 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-09T16:02:06.012Z | 2026-11-10T16:08:24.152Z | 24.1050 |
| VectorSpaceLab/general-agentic-memory | 2026-11-09T16:02:08.612Z | 2026-11-10T16:08:26.906Z | 24.1051 |
| agiresearch/A-mem | 2026-11-09T16:02:11.701Z | 2026-11-10T16:08:32.715Z | 24.1058 |
| memodb-io/memobase | 2026-11-09T16:02:15.089Z | 2026-11-10T16:08:36.706Z | 24.1060 |
| neo4j-labs/agent-memory | 2026-11-09T16:02:17.774Z | 2026-11-10T16:08:41.333Z | 24.1065 |
| volcengine/OpenViking | 2026-11-09T16:02:23.326Z | 2026-11-10T16:08:46.859Z | 24.1065 |
| vectorize-io/agent-memory-benchmark | 2026-11-09T16:02:28.586Z | 2026-11-10T16:08:55.529Z | 24.1075 |
| redis/agent-memory-server | 2026-11-09T16:02:32.897Z | 2026-11-10T16:08:58.212Z | 24.1070 |
| topoteretes/cognee | 2026-11-09T16:02:36.066Z | 2026-11-10T16:09:02.199Z | 24.1073 |
| MemTensor/MemRL | 2026-11-09T16:02:45.018Z | 2026-11-10T16:09:06.167Z | 24.1059 |
| obra/episodic-memory | 2026-11-09T16:02:48.346Z | 2026-11-10T16:09:09.827Z | 24.1060 |
| tigerless-labs/agent-memory | 2026-11-09T16:02:51.152Z | 2026-11-10T16:09:13.259Z | 24.1061 |

### 发现与参考覆盖

- `"coding agent memory" in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-10T16:09:18.273Z。
- `"memory consolidation" in:name,description created:>=2026-10-11 archived:false fork:false`：page=1，returned=14，sort=updated，incomplete_results=False，pagination_complete=True；UTC 2026-11-10T16:09:21.792Z。
- 外部榜单沿用[已登记参考版本](../docs/references.md)，本轮未刷新其当前版本，不新增跨协议分数比较。

</details>
