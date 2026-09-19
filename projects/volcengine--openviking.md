# volcengine/OpenViking

以 `viking://` 虚拟文件系统统一资源、用户记忆与技能，并在会话提交后抽取和演化长期记忆。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | context_database / coding_agent / memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `4bccb1294c013e1485c72377afcbba5ffc435cc7` |
| 许可证 | GitHub API 识别为 AGPL-3.0；未作法律审查 |
| 证据等级 | code_inspected；检查提交/diff 与 Experience Memory skill，未运行上游代码 |

## 机制

上游将 `resources`、`memories`、`skills` 等统一到虚拟文件系统；L0/L1/L2 分层用于先读摘要再按需加载细节。Session commit 后可进行记忆抽取和演化。

## 本轮代码级变化

- [`ov-experience-memory`](https://github.com/volcengine/OpenViking/blob/4bccb1294c013e1485c72377afcbba5ffc435cc7/agent-plugins/skills/ov-experience-memory/SKILL.md)：新增面向可执行任务的 Experience Memory skill。它要求在 coding、文件/数据修改、配置、部署、工作流执行或失败恢复前按需搜索当前用户的 Experience root，再读取少量高相关经验；经验只作为 advisory guidance，当前用户请求、当前环境和真实工具结果仍具有更高优先级。
- 该 skill 对 Codex、Claude Code、OpenCode、OpenClaw 等运行时映射不同 search/read 工具名，并限制一次初始检索和至多一次基于新失败证据的补充检索，避免无限扩张记忆搜索。
- 与上轮 HEAD 相比共有 25 个新增提交；diff 还包含 skill package retrieval、memory template、semantic queue/DAG、Hermes plugin 与可靠性测试等工程变化。

## Coding Agent / 部署

上游明确维护 Claude Code、Codex、Cursor、OpenClaw、Hermes、OpenCode、Pi 等集成，并提供 Python 包、服务端、CLI、SDK 与本地/云模型配置路线。这里未验证完整离线运行。

## Release 水位

当前最新 Release 为 [`python-sdk@0.1.12`](https://github.com/volcengine/OpenViking/releases/tag/python-sdk@0.1.12)，发布时间 2026-09-18T10:17:32Z。该 Release 本身没有提供足以单独形成机制结论的说明，因此本轮重点采用代码级 Experience Memory 证据。

## 证据边界

[当前代码版本](https://github.com/volcengine/OpenViking/tree/4bccb1294c013e1485c72377afcbba5ffc435cc7)。未执行上游代码，也未复现任何 benchmark 数值。
