# letta-ai/letta-code

带身份和持久记忆的有状态 Agent harness。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | stateful_agent, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `cc4654acc3b424a68c385bce0fe0c00edaad5d7e` |
| HEAD 观察（UTC） | 2026-10-15T08:46:16Z |
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
