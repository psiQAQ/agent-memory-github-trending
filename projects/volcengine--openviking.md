# volcengine/OpenViking

以 `viking://` 虚拟文件系统统一资源、用户记忆与技能，并在会话提交后抽取和演化长期记忆。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | context_database / coding_agent / memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `20ec78a149a0889a85b038627dddc70b46dceae3` |
| 许可证 | GitHub API 识别为 AGPL-3.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 机制

上游 README 描述 `resources`、`memories`、`skills` 等统一在虚拟文件系统中；L0/L1/L2 分层帮助 Agent 先读摘要再按需加载详细内容。Session commit 后启动后台记忆抽取，策略控制候选记忆的创建、合并或跳过。

## Coding Agent / 部署

上游明确列出 Claude Code、Codex、Cursor、OpenClaw、Hermes、OpenCode、Pi 等集成，并提供 Python 包、服务端、CLI、SDK 与本地/云模型配置路线。这里仅记录“上游文档支持”，未验证离线完整运行。

## Release 基线

首次正式跟踪时当前 Release 水位为 [v0.4.20](https://github.com/volcengine/OpenViking/releases/tag/v0.4.20)。这是基线，不作为本轮新事件。Release 说明涉及 Compile 托管任务、记忆策略/Agent Experience、受限 Python DSL 抽取、长会话分批以及插件记忆链路可靠性。

## 证据边界

[README](https://github.com/volcengine/OpenViking/blob/main/README.md)；[当前代码版本](https://github.com/volcengine/OpenViking/tree/20ec78a149a0889a85b038627dddc70b46dceae3)。未执行上游代码，也未复现 README/Release 中的 benchmark 数值。
