# letta-ai/letta-code

带有身份和持久记忆的有状态 Agent harness，用于组织 Agent 运行与工作流。

## 记忆机制

上游介绍 memory blocks、消息搜索、MemFS 的 Git 跟踪及周期性整理，允许上下文与技能随运行变化。

## 部署和依赖

CLI 可配置自己的模型连接；Cloud 的状态存储和远程计算是另一个部署边界。子 Agent 生命周期管理属于 harness 可靠性而非新的记忆算法。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | stateful_agent, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `5dea67021b99810707ff753db35e4534f70ff1fd` |
| HEAD 观察（UTC） | 2026-10-28T03:35:53.634Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | 固定版本提交为 code_inspected；最近 Release 为 upstream_statement；未运行上游代码 |

## 已检查的版本证据

- [v0.32.12](https://github.com/letta-ai/letta-code/releases/tag/v0.32.12) 于 2026-09-16T19:11:27Z 发布；Release 说明包含向 subagent 转发 Desktop credentials、Cloud deployment interruption 恢复、teleport/slack/CI 等修复。
- [`41f2e7a`](https://github.com/letta-ai/letta-code/commit/41f2e7abc7ca06be7413db5e6cbfe273ec2fcab3)：停止 subagent 时从“只杀 launcher”改为终止完整进程树；POSIX 使用独立进程组并支持强制升级，Windows 使用 `taskkill /t /f`，`task_stop` 等待实际清理完成后再结束状态。

## 证据边界

[已检查实现版本](https://github.com/letta-ai/letta-code/tree/435e2cfbad64c2b5aa95482130b0c52fecf122f2)。v0.32.12 为上游发布声明；进程树清理为 commit/diff 级代码检查。没有执行上游 Agent、Cloud 服务或宿主集成测试。

## 最近核实的发布

v0.34.14 改进本地 transcript 的有界恢复和流式 JSONL 读取，遵守 memfs:false；同时修复子进程 OOM 误结束父子代理以及 Cloud 子代理 sandbox 选择。

上游还声明调整 Claude Code/Codex 子代理的权限运行方式；该行为需要部署者核对，本仓库未验证其隔离或权限效果。这里只记录 Release 声明。

[v0.34.14 官方 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.14)；发布（UTC）：2026-10-14T04:52:03Z；观察（UTC）：2026-10-15T04:56:26Z；此段证据等级：`upstream_statement`。

## 最近检查的实现与发布状态

Workflow worker 可继承可解析的全局 mod 工具；显式 allowedTools 中未知工具或 agent-scoped 工具会报错，避免静默得到零工具 worker。代码区分全局工具与仅属于父 Agent 的工具，未独立运行该工作流。

状态：`released`；版本 `v0.34.15`。[PR #5078](https://github.com/letta-ai/letta-code/pull/5078)，合并 commit `5333d2060f0719882d622d0f05b1c9feffc987b8`；事件（UTC）2026-10-14T18:06:21Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/letta-ai/letta-code/blob/cc4654acc3b424a68c385bce0fe0c00edaad5d7e/src/tools/workflow/sdk-spawner.ts) · [实现 2](https://github.com/letta-ai/letta-code/blob/cc4654acc3b424a68c385bce0fe0c00edaad5d7e/src/tools/impl/workflow.ts)

Release 增量已覆盖到上次成功采集位置；这不代表全部历史发布已收集，也不代表已独立验证上游测试。

正式发布证据：[v0.34.15](https://github.com/letta-ai/letta-code/releases/tag/v0.34.15)；发布（UTC）：2026-10-15T05:10:26Z。

## 2026-10-19 版本追踪：v0.34.16

- 上游发布远程子代理 steer/resume/stop、主 Agent vault 继承、无客户端订阅的计划轮次续跑与 Codex WebSocket 错误重试。适用于依赖跨进程/远端记忆状态的工作流，未独立运行验证。
- 状态：已发布；[v0.34.16](https://github.com/letta-ai/letta-code/releases/tag/v0.34.16)，2026-10-16T21:45:24Z；证据等级 `upstream_statement`。

## 2026-10-20 版本追踪：v0.34.17 / v0.34.18

- v0.34.17：避免对不减少上下文的压缩反复执行；恢复数据读取失败时不再当作无待审批；Reflection 对齐 MemFS v2。
- v0.34.18：新增维护 core/deferred memory Skills，工作流 `agent()` 可以传 Skills；改善共享记忆 mount 的浅复制和本地/监听器之间的对话 worker 恢复。
- 状态：两版均有正式 Release。只核实上游发布说明，未运行测试，不能推出回忆质量、性能或成本收益。
- 来源：[v0.34.17](https://github.com/letta-ai/letta-code/releases/tag/v0.34.17)（2026-10-18T22:58:47Z）、[v0.34.18](https://github.com/letta-ai/letta-code/releases/tag/v0.34.18)（2026-10-19T21:02:20Z）；证据等级 `upstream_statement`。
## 2026-10-24 新 Release：v0.34.21

- v0.34.21（2026-10-22T19:02:59Z）发布：MCP originator token 跨 queued turns 隔离并传递到 tool-run，修复远程子代理抢占父 runtime、BYOK 同名连接辨识和分页记录 ID。影响多租户 MCP 来源隔离与子代理状态归属；需检查升级后的授权链路和宿主版本，未独立执行。
- 证据：[官方 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.21)；事件时间按 Release UTC，观测时间 2026-10-23T18:48:24.635Z；等级 `upstream_statement`，未独立复现。
- 本轮默认分支 HEAD：`6c8b08fedfb6f3fb437163ede8320a387151693f`（2026-10-23T18:48:24.635Z）；仅为最新采样，不表示全部 HEAD 变更已逐项审查。

## 2026-10-24：listener 审批与轮次上限

- 静态阅读 `src/websocket/listener/turn-max-turns.ts`：达到 max_turns 后以 max_steps 结束；requires_approval 场景的待审批工具调用加入拒绝队列。适用于依赖步数限制和审批边界的 listener 部署。
- [固定实现](https://github.com/letta-ai/letta-code/blob/75d7921f1666b92b4a82acca64e5ef09001c1eb3/src/websocket/listener/turn-max-turns.ts)；[发布对照](https://github.com/letta-ai/letta-code/compare/v0.34.21...75d7921f1666b92b4a82acca64e5ef09001c1eb3) 包含提交 `a9a8bbea19fa1b16860339f917220a1200a1ccc2`。状态：已合入主分支，尚未进入本轮观测的最新 Release v0.34.21。
- 证据等级 `code_inspected`，只针对上述补丁；未运行上游，不能推断完整审批隔离或生产效果。其他范围未全部审查，保留待办。观察 UTC 2026-10-24T08:10:43.245Z。

## 2026-10-25：v0.34.24 已发布

官方 Release 列出 listener 队列输入再次随下一次模型请求发送、非 TTY spinner 修复与无用队列类型清理。已读选定 queue、originator-scope、turn-finalizer 差异，未验证完整权限隔离与宿主行为。此前记录的 max_turns 修复也在此次 Release 的 #5190 清单中，发布状态由此前未发布推进为已发布。

来源：[v0.34.24 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.24)（UTC 2026-10-25T05:39:26Z）、[固定差异](https://github.com/letta-ai/letta-code/compare/75d7921f1666b92b4a82acca64e5ef09001c1eb3...6f4e4886caa0934341eea75c306fc0364509218e)。Release 描述为 upstream_statement；选定补丁为 code_inspected；未运行上游。升级者应按部署版本核对队列与审批恢复，不从静态差异推断运行保障。

本轮观察 UTC：2026-10-25T06:03:10.405Z；本轮 Release 增量已覆盖旧成功水位，不表示穷尽历史。

## 2026-10-27：反思配置接口 404 兼容

retrieveReflectionConfig 仅对 APIError 404 返回 null，其他错误继续抛出，避免把未提供反思配置接口的服务端视为已接管配置；不代表任意服务端故障都能回退。选定修复在 v0.34.24 之后。

状态：`merged_unreleased`；证据等级 `code_inspected`。这是选定实现和一手发布材料的检查，未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/letta-ai/letta-code/commit/1d63f9eba75ad7de94b9befa7a9da5ddd0eb08be)；来源版本 `1d63f9eba75ad7de94b9befa7a9da5ddd0eb08be`。
- 事件 UTC 2026-10-25T17:44:50Z；观察 UTC 2026-10-26T16:15:39.939Z。
- 已读范围：`src/agent/reflection-runs.ts`。
- 记录的默认分支 HEAD：`1fb6ea4d30942ef9220b096ba7f4185f18184fc1`，采样 UTC 2026-10-26T16:12:11.147Z；不是实时最新版本，也不表示其他提交已经逐项审查。

</details>

## 2026-10-28：v0.34.26 调整本地历史读取

完整历史按 JSONL 流式读取；不在当前上下文中的图片内容在内存里替换为短占位符，原 messages.jsonl 不重写，空上下文 ID 列表保留所有图片。Release 也列入上一轮的反思配置404兼容修复。图片密集长会话的内存影响未测量。

状态：`released`；选定实现为 `code_inspected`，发布声明为 `upstream_statement`；未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/letta-ai/letta-code/releases/tag/v0.34.26)；来源版本 `a3f7ee2d90732d36fd35c4baf97156d50f128987`。
- 事件 UTC 2026-10-28T02:48:19Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 已读范围：[src/backend/local/local-transcript-history.ts](https://github.com/letta-ai/letta-code/blob/a3f7ee2d90732d36fd35c4baf97156d50f128987/src/backend/local/local-transcript-history.ts)。
- 默认分支记录为 `5dea67021b99810707ff753db35e4534f70ff1fd`，采样 UTC 2026-10-28T03:35:53.634Z；其余差异未全部审查，历史记录保留。

</details>

## 2026-10-29：v0.34.29 重点核对

临时断线重连后，以原 request_id 重发仍待响应的外部工具请求；当前连接已发送的请求会跳过，失效或取消的所属回合会拒绝重发。 使用外部工具的部署应核对服务端按 request_id 去重。默认总等待仍为5分钟，工具可覆盖超时；超时后远端结果未知，写操作重试前先核对目标。

[合并 PR](https://github.com/letta-ai/letta-code/pull/5309)；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.29)。合并 UTC 2026-10-29T04:57:21Z；发布 UTC 2026-10-29T05:59:38Z；观察 UTC 2026-10-29T07:26:10.343Z。证据等级 code_inspected，仅静态阅读 [src/websocket/listener/external-tools.ts](https://github.com/letta-ai/letta-code/blob/2cc372d61a7ea7363f48229dc3c52752347cfd6d/src/websocket/listener/external-tools.ts)、[src/websocket/listener/lifecycle.ts](https://github.com/letta-ai/letta-code/blob/2cc372d61a7ea7363f48229dc3c52752347cfd6d/src/websocket/listener/lifecycle.ts)；未独立复现。

## 2026-10-30：v0.34.31 重点核对

活动中的队列 pump 不再被当作等待输入，保留队列回合在下一工具返回或回合结束边界进行活动 Teleport 移交的路径。 使用队列输入与 Teleport 的部署应验证移交边界及消息通道是否延续。上游给出了回归测试说明，但明确表示实际 Cloud E2E 仍需重跑；本轮没有执行上游测试。

[合并 PR](https://github.com/letta-ai/letta-code/pull/5361)；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.31)。合并 UTC 2026-10-29T08:05:04Z；发布 UTC 2026-10-29T08:34:18Z；观察 UTC 2026-10-29T19:18:28.621Z。证据等级 code_inspected，静态阅读 [src/websocket/listener/teleport.ts](https://github.com/letta-ai/letta-code/blob/018a63d44e47034c158cbfb7f37cd8eee1de47be/src/websocket/listener/teleport.ts)；未独立复现。

## 2026-10-31：v0.34.32 重点核对

Windows 外部 worker 和 Codex app-server 改经 cross-spawn 启动，可解析 npm 的 .cmd 包装；模型发现保留启动错误，避免只暴露后续 EPIPE。 遇到命令可在 PowerShell 运行、worker 却报找不到或 EPIPE 的用户，可在升级后复测启动和进程退出。上游明确未在真实 Windows 机器验证，本轮也未运行。

[合并 PR](https://github.com/letta-ai/letta-code/pull/5365)；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.32)。合并 UTC 2026-10-29T16:30:30Z；发布 UTC 2026-10-30T02:20:03Z；观察 UTC 2026-10-30T16:09:30.647Z。静态源码版本 `0cd08ecf0585dfd5851826ad38b3f1440af51627`，已确认包含该合并；证据等级 code_inspected，未独立复现。阅读范围：[src/utils/package-manager-spawn.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/utils/package-manager-spawn.ts)、[src/agent/subagents/subagent-process.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/agent/subagents/subagent-process.ts)、[src/tools/impl/codex-app-server.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/tools/impl/codex-app-server.ts)。

## 2026-11-01：v0.34.36 重点核对

恢复带 role:subagent、但不带 git-memory-enabled 标签的子 Agent 时，保持无状态，阻止启动和 listener 修复路径自动开启 MemFS 与后续反思写入。 遇到恢复子 Agent 后固定记忆膨胀或频繁压缩的用户可升级复测。已带 git-memory-enabled 的旧子 Agent 保持原行为，既有膨胀数据不会自动清理；对未启用记忆的子 Agent 显式开启 MemFS 也会无操作返回。

[合并 PR](https://github.com/letta-ai/letta-code/pull/5397)；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.36)。合并 UTC 2026-10-30T22:45:09Z；发布 UTC 2026-10-31T02:29:58Z；观察 UTC 2026-10-31T16:11:56.075Z。静态源码版本 `8f72222dec142dfc2316692d68ada3ab2e439d46`，已确认包含该合并；证据等级 code_inspected，未独立复现。阅读范围：[src/agent/memory-filesystem.ts](https://github.com/letta-ai/letta-code/blob/8f72222dec142dfc2316692d68ada3ab2e439d46/src/agent/memory-filesystem.ts)、[src/headless-memfs-policy.ts](https://github.com/letta-ai/letta-code/blob/8f72222dec142dfc2316692d68ada3ab2e439d46/src/headless-memfs-policy.ts)、[src/agent/agent-tags.ts](https://github.com/letta-ai/letta-code/blob/8f72222dec142dfc2316692d68ada3ab2e439d46/src/agent/agent-tags.ts)、[src/headless.ts](https://github.com/letta-ai/letta-code/blob/8f72222dec142dfc2316692d68ada3ab2e439d46/src/headless.ts)、[src/websocket/listener/memfs-sync.ts](https://github.com/letta-ai/letta-code/blob/8f72222dec142dfc2316692d68ada3ab2e439d46/src/websocket/listener/memfs-sync.ts)。

## 2026-11-05：重点变更核对

MemFS pre-commit 将未改文件的既有约束问题降为警告，仍阻止涉及本次增删改路径的问题；audit、首次提交和获准的配置变化继续检查整树。 受无关旧记忆问题阻塞的用户可关注包含 PR #5499 的后续版本；本轮没有确认新 Release。根索引缺失与只读文件保护仍可能直接阻止提交，不能理解为关闭约束。

[合并 PR](https://github.com/letta-ai/letta-code/pull/5499)；合并 UTC 2026-11-04T05:39:18Z；观察 UTC 2026-11-04T16:09:54.352Z；状态 merged-unreleased。静态源码版本 `df234ac178ed4719ba72732342534a9255c487e1`，证据等级 code_inspected，未独立复现。阅读范围：[src/agent/memory-constraints.ts](https://github.com/letta-ai/letta-code/blob/df234ac178ed4719ba72732342534a9255c487e1/src/agent/memory-constraints.ts)、[src/memory-constraints.ts](https://github.com/letta-ai/letta-code/blob/df234ac178ed4719ba72732342534a9255c487e1/src/memory-constraints.ts)。

## 2026-11-06：重点变更核对

Memory Palace 按 MemFS 布局识别核心记忆：v2 的根目录 Markdown（含 MEMORY.md）归入 core；v1 保留 system/ 目录分类。 使用 MemFS v2 且在界面看到核心文件误分类的用户可评估 v0.34.41。这是展示分类修正，不证明改变 Agent 的记忆投影、检索或效果。

[PR](https://github.com/letta-ai/letta-code/pull/4888)；合并 UTC 2026-11-05T00:49:22Z；[正式版本 v0.34.41](https://github.com/letta-ai/letta-code/releases/tag/v0.34.41) 发布 UTC 2026-11-05T04:23:03Z；实际 tag 已核对包含该合并。观察 UTC 2026-11-06T04:07:56.131Z。静态源码版本 `233c0034492b9782c9bec01002226b891e514745`，证据等级 code_inspected，未独立复现。阅读范围：[src/agent/memory-format.ts](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/agent/memory-format.ts)、[src/web/generate-memory-viewer.ts](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/web/generate-memory-viewer.ts)、[src/web/memory-viewer-template.txt](https://github.com/letta-ai/letta-code/blob/233c0034492b9782c9bec01002226b891e514745/src/web/memory-viewer-template.txt)。

## 2026-11-14：重点变更核对

远程记忆同步明确收到 HTTP 403 时，Listener 会尝试删除经路径和 origin 校验的本地记忆检出。 在该检出目录保留未同步编辑的接入方，应先确认这些编辑已另行保存。

清理前核对真正路径、工作目录和匹配该 Agent 的 origin，并跳过本地后端。源码分支将权限拒绝后的删除限制在可核实的检出目录，未做运行验证。

[PR](https://github.com/letta-ai/letta-code/pull/5711) 合并UTC 2026-11-13T08:01:16Z；状态 released；发布UTC 2026-11-13T18:12:34Z。审读版本 `d82e13570aff8a2c08196d1c90d9773f18fc2268`，观察UTC 2026-11-14T02:55:55.192Z，证据等级code_inspected，未独立复现。发行标签包含合并提交：领先 3 个提交，落后 0。

阅读范围：[src/websocket/listener/memfs-sync.ts](https://github.com/letta-ai/letta-code/blob/d82e13570aff8a2c08196d1c90d9773f18fc2268/src/websocket/listener/memfs-sync.ts)。
