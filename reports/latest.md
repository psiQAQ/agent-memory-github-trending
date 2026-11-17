# Agent Memory 简报｜2026-11-18

四项记忆相关变更已合并：涉及导入停止、本地召回计数、追加标签和会话写入失败处理。
OpenViking 同期发布 React 0.1.13 和 SuperAgent 0.5.4 预览。两条发布记录不足以确认会话记忆修复已随包交付。
需要修复的部署先核对发行标签；做导入或会话写入时，分别确认未应答的上传和失败的写入目标。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| OpenViking | 面向 macOS、Linux 或 WSL2 的 SuperAgent 安装预览；该条发布说明的资产不涵盖原生 Windows。 | 已发布预览 [openviking-superagent@0.5.4-preview](https://github.com/volcengine/OpenViking/releases/tag/openviking-superagent%400.5.4-preview) | 按各自包和平台选择版本。 |
| OpenViking | React 控制台包加入具名编译流程及配置切换，并调整 Wiki 快照历史与冲突界面。 | 已发布 [react@0.1.13](https://github.com/volcengine/OpenViking/releases/tag/react%400.1.13) | 按各自包和平台选择版本。 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/6233) | 导入界面增加停止操作：中止正在等待的上传并阻止继续发送；未收到答复的在途批次标为未确认。 | 已合并，未核实随版本交付 | 迁移时先核对已确认与未确认的条目，再决定是否重新开始。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/5772) | 本地后端修正系统提示中的召回计数：按本地 transcript 中已不在当前上下文的不同消息 ID 计数。 | 已合并，未核实随版本交付 | 用本地会话压缩前后的提示核对计数；该数值不代表成功召回的条数。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6590) | 增量追加文档省略 tags 时继承现有标签，避免文档及其存量记忆被意外清空标签。 | 已合并，未核实随版本交付 | 使用 append 的调用方可关注后续版本；需要清除标签时，按文档标签 PATCH 语义处理。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7801) | 会话内同一记忆 URI 的写入优先于单纯删除；模型解析重试用尽或单个 URI 写入失败后，仍可保留独立目标的成功写入。 | 已合并，未核实随版本交付 | 排查会话提交时应检查逐 URI 的跳过和失败信息，不能从提交继续推断全部写入成功。 |

**thedotmack/claude-mem**。适用于新版本地设置流程向 cmem.ai 上传历史观察。已确认上传会保留，停止不会删除两端数据，也不能保证服务器没收到最后一个批次。

**letta-ai/letta-code**。用于本地后端重编译系统提示；未建立上下文 ID 列表时计零。这项修复只改变提示中的统计口径。

**vectorize-io/hindsight**。引擎仅在未指定批次 document_tags、指定 document_id、且项目为 append 并省略 tags 时继承；读标签在写入前，并发标签 PATCH 仍可能被覆盖。

**volcengine/OpenViking**。限于会话记忆更新路径；解析失败会抑制涉及该目标的链接，非法的解析后计划仍然失败。未证实相关发行包包含该修复。

## Star 变化：真实间隔约 23.74–23.98 小时

7日/30日合格基线分别为 21/24、21/24，容差±6小时。下表比较两次实际观测的 Star 净变化，各项目起止时间见证据区。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 69067 | 69115 | +48 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32848 | 32885 | +37 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12416 | 12434 | +18 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 117584 | 117904 | +320 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3853 | 3863 | +10 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 61369 | 61559 | +190 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30938 | 30968 | +30 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2960 | 2960 | +0 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 609 | 609 | +0 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 42310 | 42371 | +61 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 326 | 326 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 33347 | 33371 | +24 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 503 | 505 | +2 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4322 | 4322 | +0 |
| [memorax-ai/memorax-code](https://github.com/memorax-ai/memorax-code) | engineering | — | 2150 | 首次观测 |
| [JingxuanC/causal-memory](https://github.com/JingxuanC/causal-memory) | engineering | — | 107 | 首次观测 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 869 | 869 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1215 | 1216 | +1 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 202 | 202 | +0 |
| [Tin11Mn/chrono-hybrid-mem](https://github.com/Tin11Mn/chrono-hybrid-mem) | research | — | 2 | 首次观测 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1225 | 1228 | +3 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 211 | 211 | +0 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 169 | 169 | +0 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25463 | 25470 | +7 |

## 新候选对比

4 条无 Star 下限查询取得 80 条原始结果，可能重复。按 README 初审 2 项，收录 0 项，登记池保持 50/50。

| 候选 | 用途与机制线索 | 核实边界 |
| --- | --- | --- |
| [aoci-spec/aoci-code](https://github.com/aoci-spec/aoci-code/blob/main/README.md) | 本地 Go MCP/CLI 维护 Git 版本化代码库地图；面向编码代理的工程记忆。README 自报候选版本和许可 FSL 1.1 MIT，待核实实现与许可正文。 | 上游自述，未审实现、未复现。 |
| [electricsheephq/bicentennial](https://github.com/electricsheephq/bicentennial/blob/main/README.md) | 以跨重启、压缩和会话的实际行动评价长期记忆；README 明列预试点阶段。待核实评测代码、预注册版本与公开结果。 | 上游自述，未审实现、未复现。 |

## 方法与边界

24 个项目的元数据、HEAD 和本轮所需的 Release 分页均已采集；三项新登记来源仅建立首次基线。四项变更核对了合并记录和固定版本源码。搜索覆盖每条查询的第一页。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261117T160225Z-local`；观测汇总 UTC 2026-11-17T16:09:37.866Z，展示日期按北京时间计算。[原始快照](../data/snapshots/2026/11/20261117T160225Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。发行状态按本轮采集窗口判断。
- [openviking-superagent@0.5.4-preview](https://github.com/volcengine/OpenViking/releases/tag/openviking-superagent%400.5.4-preview)：发布 UTC 2026-11-17T12:34:22Z，tag 指向 `ae336f80dc2c122f05f1691dd8266f1bf749cfac`，核对 UTC 2026-11-17T16:13:24.344Z。发布说明仅作该包的上游陈述。
- [react@0.1.13](https://github.com/volcengine/OpenViking/releases/tag/react%400.1.13)：发布 UTC 2026-11-16T19:06:29Z，tag 指向 `1c25783ee63c911e57e1795a76839de7b8347ad4`，核对 UTC 2026-11-17T16:13:25.269Z。发布说明仅作该包的上游陈述。
- [aoci-spec/aoci-code README](https://github.com/aoci-spec/aoci-code/blob/main/README.md)：blob `2dec45b80db9a1d70cda907b4fe1d5b4af46a761`，观测 UTC 2026-11-17T16:12:56.203Z。
- [electricsheephq/bicentennial README](https://github.com/electricsheephq/bicentennial/blob/main/README.md)：blob `062685b23f1b3430a4555b6080e624cb2b19bb98`，观测 UTC 2026-11-17T16:12:57.134Z。

### thedotmack/claude-mem

[PR](https://github.com/thedotmack/claude-mem/pull/6233) 合并UTC 2026-11-17T10:56:12Z，SHA `3d1aa47ec6406c88a76bf9289c4a4248282303e6`；发布UTC 未确认。审读观察UTC 2026-11-17T16:11:56.101Z。本轮未核实覆盖该变更的发布包；固定源码已审读，未独立运行。

阅读范围：[src/ui/my-work/src/setup/screens/import-screen.tsx](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/src/ui/my-work/src/setup/screens/import-screen.tsx)；[src/services/setup/history-import.ts](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/src/services/setup/history-import.ts)；[tests/worker/http/routes/setup-import-routes.test.ts](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/tests/worker/http/routes/setup-import-routes.test.ts)。

### letta-ai/letta-code

[PR](https://github.com/letta-ai/letta-code/pull/5772) 合并UTC 2026-11-17T02:00:09Z，SHA `108c736afdbb31aedf18f6ed45aba54e0f38cdcd`；发布UTC 未确认。审读观察UTC 2026-11-17T16:11:57.778Z。本轮未核实覆盖该变更的发布包；固定源码已审读，未独立运行。

阅读范围：[src/backend/local/local-transcript-history.ts](https://github.com/letta-ai/letta-code/blob/108c736afdbb31aedf18f6ed45aba54e0f38cdcd/src/backend/local/local-transcript-history.ts)；[src/backend/local/system-prompt-compilation.ts](https://github.com/letta-ai/letta-code/blob/108c736afdbb31aedf18f6ed45aba54e0f38cdcd/src/backend/local/system-prompt-compilation.ts)。

### vectorize-io/hindsight

[PR](https://github.com/vectorize-io/hindsight/pull/6590) 合并UTC 2026-11-16T18:41:42Z，SHA `42e58226385ecb3239e6b24d8ccef834d93b9032`；发布UTC 未确认。审读观察UTC 2026-11-17T16:13:23.503Z。本轮未核实覆盖该变更的发布包；固定源码已审读，未独立运行。

阅读范围：[hindsight-api-slim/hindsight_api/engine/memory_engine.py](https://github.com/vectorize-io/hindsight/blob/42e58226385ecb3239e6b24d8ccef834d93b9032/hindsight-api-slim/hindsight_api/engine/memory_engine.py)；[hindsight-system-tests/tests/test_12_append_document.py](https://github.com/vectorize-io/hindsight/blob/42e58226385ecb3239e6b24d8ccef834d93b9032/hindsight-system-tests/tests/test_12_append_document.py)。

### volcengine/OpenViking

[PR](https://github.com/volcengine/OpenViking/pull/7801) 合并UTC 2026-11-17T07:49:47Z，SHA `31b66ad384faa659d9869f0a328ba584dcf08a0f`；发布UTC 未确认。审读观察UTC 2026-11-17T16:12:49.346Z。本轮未核实覆盖该变更的发布包；固定源码已审读，未独立运行。

阅读范围：[openviking/session/memory/streaming_memory_updater.py](https://github.com/volcengine/OpenViking/blob/31b66ad384faa659d9869f0a328ba584dcf08a0f/openviking/session/memory/streaming_memory_updater.py)；[openviking/session/memory/memory_updater.py](https://github.com/volcengine/OpenViking/blob/31b66ad384faa659d9869f0a328ba584dcf08a0f/openviking/session/memory/memory_updater.py)；[tests/session/test_session_commit.py](https://github.com/volcengine/OpenViking/blob/31b66ad384faa659d9869f0a328ba584dcf08a0f/tests/session/test_session_commit.py)。

### 逐项目Star观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-11-16T16:06:05.906Z | 2026-11-17T16:05:11.531Z | 23.9849 |
| letta-ai/letta | 2026-11-16T16:06:06.859Z | 2026-11-17T16:05:12.507Z | 23.9849 |
| getzep/graphiti | 2026-11-16T16:06:27.966Z | 2026-11-17T16:05:30.990Z | 23.9842 |
| MemTensor/MemOS | 2026-11-16T16:06:28.863Z | 2026-11-17T16:05:31.954Z | 23.9842 |
| thedotmack/claude-mem | 2026-11-16T16:06:50.821Z | 2026-11-17T16:05:50.185Z | 23.9832 |
| xiaowu0162/LongMemEval | 2026-11-16T16:06:51.696Z | 2026-11-17T16:05:51.159Z | 23.9832 |
| xiaowu0162/LongMemEval-V2 | 2026-11-16T16:07:17.408Z | 2026-11-17T16:06:06.177Z | 23.9802 |
| letta-ai/letta-code | 2026-11-16T16:07:18.358Z | 2026-11-17T16:06:07.318Z | 23.9803 |
| vectorize-io/hindsight | 2026-11-16T16:21:59.329Z | 2026-11-17T16:06:39.984Z | 23.7446 |
| TencentCloud/TencentDB-Agent-Memory | 2026-11-16T16:22:00.359Z | 2026-11-17T16:06:41.000Z | 23.7446 |
| VectorSpaceLab/general-agentic-memory | 2026-11-16T16:22:19.551Z | 2026-11-17T16:07:00.454Z | 23.7447 |
| agiresearch/A-mem | 2026-11-16T16:22:20.667Z | 2026-11-17T16:07:01.410Z | 23.7447 |
| memodb-io/memobase | 2026-11-16T16:22:37.024Z | 2026-11-17T16:07:15.265Z | 23.7440 |
| neo4j-labs/agent-memory | 2026-11-16T16:22:38.110Z | 2026-11-17T16:07:16.271Z | 23.7439 |
| volcengine/OpenViking | 2026-11-16T16:22:54.900Z | 2026-11-17T16:07:33.505Z | 23.7441 |
| vectorize-io/agent-memory-benchmark | 2026-11-16T16:22:55.978Z | 2026-11-17T16:07:34.606Z | 23.7441 |
| redis/agent-memory-server | 2026-11-16T16:23:13.143Z | 2026-11-17T16:07:52.282Z | 23.7442 |
| topoteretes/cognee | 2026-11-16T16:23:14.347Z | 2026-11-17T16:07:53.477Z | 23.7442 |
| MemTensor/MemRL | 2026-11-16T16:23:31.019Z | 2026-11-17T16:08:09.101Z | 23.7439 |
| obra/episodic-memory | 2026-11-16T16:23:31.941Z | 2026-11-17T16:08:10.358Z | 23.7440 |
| tigerless-labs/agent-memory | 2026-11-16T16:23:47.628Z | 2026-11-17T16:08:27.414Z | 23.7444 |
| memorax-ai/memorax-code | — | 2026-11-17T16:08:28.379Z | — |
| JingxuanC/causal-memory | — | 2026-11-17T16:08:49.272Z | — |
| Tin11Mn/chrono-hybrid-mem | — | 2026-11-17T16:08:50.247Z | — |

### 发现与参考覆盖

- `coding agent memory in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-17T16:09:32.318Z。
- `agent memory in:name,description archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-17T16:09:34.303Z。
- `agent memory in:name,description created:>=2026-10-18 archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-17T16:09:36.041Z。
- `memory benchmark in:name,description created:>=2026-10-18 archived:false fork:false`：page=1，returned=20，sort=updated，incomplete_results=False，pagination_complete=False；UTC 2026-11-17T16:09:37.866Z。
- 外部榜单沿用[已登记参考版本](../docs/references.md)，本轮未刷新其当前版本，不新增跨协议分数比较。

</details>
