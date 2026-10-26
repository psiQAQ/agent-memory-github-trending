# Agent Memory 研究简报｜2026-10-27

> **变化：** Claude Mem 与 Hindsight 都修正缓冲写入和检查点的先后关系；腾讯 Agent Memory 发布 v2.0.3，OpenViking 发布 Python SDK 0.1.17。
>
> **影响谁：** 依赖转录恢复、缓冲存储扩展，或从源码部署代理、反思配置与 SDK 集成的团队。
>
> **建议行动：** 核对实际部署 commit 和包版本，再安排持久化、超时与兼容性检查；本轮静态阅读不足以建议所有用户立即升级或迁移。

## 已确认合并/发布的变更

| 项目 | 变化、记录理由与行动 | 状态 | 影响面 |
| --- | --- | --- | --- |
| Claude Mem | 转录检查点等对应缓冲工作保存后才推进，避免恢复时跳过尚未持久化的内容；自动数据库快照为可选项，首次约5分钟后执行，默认24小时、保留7份。关注崩溃恢复的团队可审查实现并另行安排恢复演练。 | 主分支已合并；均在 v15.2.1 之后 | 转录采集与本地 SQLite；磁盘空间查询失败会跳过容量检查，未验证断电/恢复效果 |
| Claude Mem v15.2.1 | 发布说明改为 OIDC 可信发布以修复 npm 发布链路。该版本已发布，不能据此认为之后合入的检查点与备份已进入安装包。 | 正式发布；发布链路说明为上游自述 | 包发布方式；本轮未检查 npm 注册表或安装结果 |
| Letta Code | 反思配置读取遇到 APIError 404 返回 null，其他错误继续抛出。对接较旧或未提供此接口的服务端时，应区分接口不存在与真正服务故障。 | 已合并，位于 v0.34.24 之后；选定源码静态检查 | 反思配置兼容；不能把所有错误都当作可回退 |
| Hindsight | 缓冲 retain session 在 commit 前不登记文档完成；失败重试重新抽取。SQL 原地分批写入路径仍保留原检查点。使用缓冲存储扩展的团队应重点审查这一差异。 | 已合并，位于 v1.1.0 之后；选定源码与已合并 PR | 持久性与恢复正确性；上游回归测试未由本仓库运行 |
| 腾讯 Agent Memory v2.0.3 | 发布说明新增用户默认 Team/Agent/Task 组合与文档导入，默认转发超时改为60分钟，显式配置不变。选定源码中，重试共享转发总截止时间，设置成功日志延后至 upsert 成功。升级时核对原有超时配置。 | 正式发布；发布说明＋选定源码静态检查 | 会话默认配置、代理超时与错误排查；其余发布功能未逐项审计 |
| OpenViking | Python SDK 0.1.17 已发布；主分支把 SDK 依赖下限从0.1.15提高到0.1.17，锁文件同步。源码部署应核对实际解析版本；没有证据建议仅凭此项迁移服务端。 | SDK 已发布；服务端依赖改动已合并；观测服务端 Release 仍为 v0.5.2 | SDK/服务端兼容；SDK Release 无正文，Compile API 关联来自提交说明 |

<details markdown="1">
<summary>证据与时间</summary>

- **thedotmack/claude-mem**：[一手证据](https://github.com/thedotmack/claude-mem/compare/35e24ba7f50f357b81bdafd823f89b41d65679fc...7325fb7818ff7426665d85922db642ec0931bdcd)；事件 UTC 2026-10-26T11:34:44Z，观察 UTC 2026-10-26T16:15:39.239Z。版本 `7325fb7818ff7426665d85922db642ec0931bdcd`；证据等级 `code_inspected`。已读范围：`src/services/transcripts/watcher.ts`、`src/services/transcripts/types.ts`、`src/services/transcripts/processor.ts`、`src/services/worker/SessionMessageBuffer.ts`、`src/services/worker-service.ts`、`src/services/backup/BackupManager.ts`。转录 watcher 按缓冲消息序号延后检查点，worker 接入 gate；自动 SQLite 快照需启用配置，首次约5分钟后执行，默认间隔24小时保留7份。两项均在 v15.2.1 真实 tag 之后。磁盘检查不可用时会跳过容量检查，未独立验证恢复/断电一致性。
- **letta-ai/letta-code**：[一手证据](https://github.com/letta-ai/letta-code/commit/1d63f9eba75ad7de94b9befa7a9da5ddd0eb08be)；事件 UTC 2026-10-25T17:44:50Z，观察 UTC 2026-10-26T16:15:39.939Z。版本 `1d63f9eba75ad7de94b9befa7a9da5ddd0eb08be`；证据等级 `code_inspected`。已读范围：`src/agent/reflection-runs.ts`。retrieveReflectionConfig 仅对 APIError 404 返回 null，其他错误继续抛出，避免把未提供反思配置接口的服务端视为已接管配置；不代表任意服务端故障都能回退。选定修复在 v0.34.24 之后。
- **vectorize-io/hindsight**：[一手证据](https://github.com/vectorize-io/hindsight/pull/6100)；事件 UTC 2026-10-26T09:56:57Z，观察 UTC 2026-10-26T16:15:40.848Z。版本 `1da5f03241de742aaf37f78399061636077d2aad`；证据等级 `code_inspected`。已读范围：`hindsight-api-slim/hindsight_api/engine/retain/orchestrator.py`、`PR6100 merged state and reported test scope`。仅在 retain_session 为 None 时保留原分批检查点；使用缓冲 session 时不在 commit 前登记完成，重试重新抽取。SQL 原地分批写入路径保持检查点；上游描述的回归测试未由本仓库运行。修复在 v1.1.0 之后。
- **TencentCloud/TencentDB-Agent-Memory**：[一手证据](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.3)；事件 UTC 2026-10-26T14:09:03Z，观察 UTC 2026-10-26T16:15:42.090Z。版本 `084bed45cad6bb7f877455082cee82835d65671a`；证据等级 `code_inspected`。已读范围：`v2.0.3 upstream release statement`、`MemoryCore/src/metadata/service/user-session-default-service.ts`、`MemoryProxy/src/pipeline/stages/forward-with-retry.ts`。正式发布说明新增用户 Team/Agent/Task 默认组合、文档导入和默认转发超时60分钟（显式配置不变）。选定源码显示转发重试共享总截止时间，设置成功日志放到 upsert 之后；发布声明的全部功能未逐项审计或运行。
- **volcengine/OpenViking**：[一手证据](https://github.com/volcengine/OpenViking/commit/009c483f20806d63979cec0f3a7fb1304fd600df)；事件 UTC 2026-10-26T03:40:46Z，观察 UTC 2026-10-26T16:15:43.546Z。版本 `009c483f20806d63979cec0f3a7fb1304fd600df`；证据等级 `code_inspected`。已读范围：`pyproject.toml`、`uv.lock`、`python-sdk@0.1.17 release metadata`。python-sdk@0.1.17 已发布但无 Release 正文；主分支 pyproject.toml 把 openviking-sdk 下限0.1.15改为0.1.17，锁文件同步。相关 commit 将其描述为 Compile API 兼容要求；不能据此宣称服务端已发布新版本，观测服务端 Release 仍为 v0.5.2。
- Claude Mem [v15.2.1](https://github.com/thedotmack/claude-mem/releases/tag/v15.2.1) 发布 UTC 2026-10-25T19:45:33Z；注解 tag `49c7236b1f3754c31c49dde2fbc16add8db274fd` 指向真实 commit `35e24ba7f50f357b81bdafd823f89b41d65679fc`。tag→观察 HEAD 的13项提交包含检查点与备份修复。[发布后差异](https://github.com/thedotmack/claude-mem/compare/35e24ba7f50f357b81bdafd823f89b41d65679fc...7325fb7818ff7426665d85922db642ec0931bdcd)。
- [Hindsight v1.1.0→观察 HEAD](https://github.com/vectorize-io/hindsight/compare/v1.1.0...326ad524f5999d6b90520e358f17c657d1c429f5) 包含修复 `1da5f03241de742aaf37f78399061636077d2aad`；[Letta Code v0.34.24→观察 HEAD](https://github.com/letta-ai/letta-code/compare/v0.34.24...1fb6ea4d30942ef9220b096ba7f4185f18184fc1) 包含修复 `1d63f9eba75ad7de94b9befa7a9da5ddd0eb08be`。
- OpenViking [python-sdk@0.1.17](https://github.com/volcengine/OpenViking/releases/tag/python-sdk%400.1.17) 发布 UTC 2026-10-26T03:25:33Z，Release 正文为空；依赖下限变更 UTC 2026-10-26T03:40:46Z。没有读取/执行 SDK 分发包。

</details>

## Star 变化：两次真实观测，约23.96–23.97小时

7日与30日窗口的合格基线均为0/21；索引内没有落在目标时刻 ±6小时的样本，因此显示“—”。下表比较两次实际观测，按类别分组并沿用登记顺序，不是跨类别质量排行；关注度变化不证明技术效果。

| 类别 | 项目 | 起点 Stars | 本轮 Stars | 净变化 | 实际间隔（小时） |
| --- | --- | ---: | ---: | ---: | ---: |
| engineering | [mem0ai/mem0](https://github.com/mem0ai/mem0) | 67784 | 67849 | +65 | 23.9687 |
| engineering | [getzep/graphiti](https://github.com/getzep/graphiti) | 32203 | 32242 | +39 | 23.9609 |
| engineering | [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | 12091 | 12111 | +20 | 23.9609 |
| engineering | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 103023 | 103325 | +302 | 23.9686 |
| engineering | [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | 3709 | 3711 | +2 | 23.9720 |
| engineering | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | 53638 | 54046 | +408 | 23.9734 |
| engineering | [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | 29914 | 29979 | +65 | 23.9735 |
| engineering | [memodb-io/memobase](https://github.com/memodb-io/memobase) | 2938 | 2938 | 0 | 23.9732 |
| engineering | [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | 591 | 592 | +1 | 23.9733 |
| engineering | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | 40783 | 40877 | +94 | 23.9721 |
| engineering | [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | 323 | 323 | 0 | 23.9728 |
| engineering | [topoteretes/cognee](https://github.com/topoteretes/cognee) | 32734 | 32776 | +42 | 23.9729 |
| engineering | [obra/episodic-memory](https://github.com/obra/episodic-memory) | 493 | 493 | 0 | 23.9713 |
| engineering | [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | 4726 | 4733 | +7 | 23.9611 |
| research | [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | 863 | 863 | 0 | 23.9736 |
| research | [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | 1207 | 1208 | +1 | 23.9736 |
| research | [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | 190 | 192 | +2 | 23.9713 |
| benchmark | [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | 1172 | 1174 | +2 | 23.9686 |
| benchmark | [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | 194 | 197 | +3 | 23.9720 |
| benchmark | [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | 158 | 158 | 0 | 23.9721 |
| reference | [letta-ai/letta](https://github.com/letta-ai/letta) | 25252 | 25262 | +10 | 23.9687 |

<details markdown="1">
<summary>Star 原始时刻与取数边界</summary>

| 项目 | 起点（UTC） | 终点（UTC） |
| --- | --- | --- |
| mem0ai/mem0 | 2026-10-25T16:11:47.851Z | 2026-10-26T16:09:55.058Z |
| letta-ai/letta | 2026-10-25T16:11:48.256Z | 2026-10-26T16:09:55.582Z |
| getzep/graphiti | 2026-10-25T16:12:40.777Z | 2026-10-26T16:10:20.016Z |
| MemTensor/MemOS | 2026-10-25T16:12:41.202Z | 2026-10-26T16:10:20.539Z |
| thedotmack/claude-mem | 2026-10-25T16:13:13.034Z | 2026-10-26T16:11:20.123Z |
| xiaowu0162/LongMemEval | 2026-10-25T16:13:13.411Z | 2026-10-26T16:11:20.546Z |
| xiaowu0162/LongMemEval-V2 | 2026-10-25T16:13:34.506Z | 2026-10-26T16:11:53.748Z |
| letta-ai/letta-code | 2026-10-25T16:13:34.946Z | 2026-10-26T16:11:54.290Z |
| vectorize-io/hindsight | 2026-10-25T16:13:59.822Z | 2026-10-26T16:12:24.140Z |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-25T16:14:00.306Z | 2026-10-26T16:12:24.881Z |
| VectorSpaceLab/general-agentic-memory | 2026-10-25T16:14:21.346Z | 2026-10-26T16:12:46.357Z |
| agiresearch/A-mem | 2026-10-25T16:14:21.728Z | 2026-10-26T16:12:46.821Z |
| memodb-io/memobase | 2026-10-25T16:14:47.564Z | 2026-10-26T16:13:11.217Z |
| neo4j-labs/agent-memory | 2026-10-25T16:14:48.116Z | 2026-10-26T16:13:11.966Z |
| volcengine/OpenViking | 2026-10-25T16:15:17.188Z | 2026-10-26T16:13:36.726Z |
| vectorize-io/agent-memory-benchmark | 2026-10-25T16:15:17.643Z | 2026-10-26T16:13:37.367Z |
| redis/agent-memory-server | 2026-10-25T16:15:40.161Z | 2026-10-26T16:14:02.383Z |
| topoteretes/cognee | 2026-10-25T16:15:40.594Z | 2026-10-26T16:14:02.930Z |
| MemTensor/MemRL | 2026-10-25T16:16:07.649Z | 2026-10-26T16:14:24.367Z |
| obra/episodic-memory | 2026-10-25T16:16:08.041Z | 2026-10-26T16:14:24.796Z |
| tigerless-labs/agent-memory | 2026-10-25T16:17:06.693Z | 2026-10-26T16:14:46.832Z |

两端来自已校验历史索引与本轮 GitHub metadata；没有插值、补齐缺日或外推为一周增长。当前7/30日缺口不会因短间隔比较而消失；后续只有成功采到合格窗口才提供对应指标。

</details>

## 待审候选比较

本轮两类项目检索分别返回20项、9项，去重29项原始线索；正式候选初审0项、晋升0项。研究预算用于5个已登记项目的实质变化。以下仅列近期查询中的待审线索，尚未加入登记池，不能据名称判断机制或成熟度。

| 待审线索 | 存储/记忆载体 | 检索与维护 | 依赖/宿主 | 评测资产 | 许可证 | 成熟度/观察版本 |
| --- | --- | --- | --- | --- | --- | --- |
| [tty-pt/pi-mm](https://github.com/tty-pt/pi-mm) | 未核实 | 未核实 | 未核实 | 未核实 | 未核实 | 未初审；未固定源码版本 |
| [liruiluo/agentmemorygym](https://github.com/liruiluo/agentmemorygym) | 未核实 | 未核实 | 未核实 | 未核实 | 未核实 | 未初审；未固定源码版本 |
| [Mukul-svg/laya-swe](https://github.com/Mukul-svg/laya-swe) | 未核实 | 未核实 | 未核实 | 未核实 | 未核实 | 未初审；未固定源码版本 |

## 方法与边界

21个正式/参考项目的 metadata、HEAD、完整增量 Release 均为21/21；预选5项实质变化完成5项选定一手材料深读，未审查全部提交。mem0 与 Agent Memory Benchmark 的新 HEAD、其余变更范围和29项原始发现留待后续核查。所有技术结论来自上游发布/PR 与选定代码差异，未运行上游、未付费实验、未独立复现。项目登记池仍为47项，发现查询不代表 GitHub 全量生态。W43 周报已有归档，本轮没有新到期自然周。可继续[比较正式项目](current.html)、[核对方法](../docs/methodology.html)、[查看术语](../docs/glossary.html)和[获取本轮原始数据](../data/snapshots/2026/10/20261026T160515Z-interactive.json)。

<details markdown="1">
<summary>运行记录</summary>

- run_id：`20261026T160515Z-interactive`；批次完成 UTC 2026-10-26T16:22:27.196Z（北京时间2026-10-27）。
- 本轮按 `interactive` 记录：宿主未提供可独立关联的 Scheduled 触发证据；不代替自然 Scheduled 验收，未改平台任务。
- 基线 commit：`9aefdb57d2b866f6a89fd8336f2853ed58bd0442`；真实 root tree：`e4ebb6119cc3c9ea5723455062a937624fe88e8a`。117个 blob 的完整重建一致，19份历史 Snapshot 索引与21张项目卡校验通过。
- 外部 pre/post 已逐段输出；宿主没有暴露可回读外部 trace/响应引用及可信事件顺序，正式 API 指标保留 null，`instrumentation_complete=false`。详细操作证据随独立 Receipt 归档，本文不预宣称发布/回读成功。

</details>
