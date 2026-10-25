# letta-ai/letta-code

带身份和持久记忆的有状态 Agent harness。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | stateful_agent, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `6f4e4886caa0934341eea75c306fc0364509218e` |
| HEAD 观察（UTC） | 2026-10-25T06:03:10.405Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | 固定版本提交为 code_inspected；最近 Release 为 upstream_statement；未运行上游代码 |

## 记忆机制

上游介绍 memory blocks、消息搜索、MemFS 的 Git 跟踪及周期性整理，允许上下文与技能随运行变化。

## 已检查的版本证据

- [v0.32.12](https://github.com/letta-ai/letta-code/releases/tag/v0.32.12) 于 2026-09-16T19:11:27Z 发布；Release 说明包含向 subagent 转发 Desktop credentials、Cloud deployment interruption 恢复、teleport/slack/CI 等修复。
- [`41f2e7a`](https://github.com/letta-ai/letta-code/commit/41f2e7abc7ca06be7413db5e6cbfe273ec2fcab3)：停止 subagent 时从“只杀 launcher”改为终止完整进程树；POSIX 使用独立进程组并支持强制升级，Windows 使用 `taskkill /t /f`，`task_stop` 等待实际清理完成后再结束状态。

## 部署和依赖

CLI 可配置自己的模型连接；Cloud 的状态存储和远程计算是另一个部署边界。子 Agent 生命周期管理属于 harness 可靠性而非新的记忆算法。

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

Release 增量已覆盖到上次成功水位；不代表穷尽历史发布或独立验收上游测试。

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
