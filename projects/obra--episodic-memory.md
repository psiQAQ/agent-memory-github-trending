# obra/episodic-memory

面向 Coding Agent 会话历史的本地语义记忆层，统一索引 Claude Code、Codex、Cursor、OpenCode 与 OMP 会话。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent / conversation_memory / local_first |
| 首次发现（UTC） | 2026-09-17T16:27:32Z |
| 本次 HEAD | `7e06519357777badd7a115d2014a7ef845904310` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

同步不同 Coding Agent 的 transcript，在本地建立语义索引，通过 MCP/CLI 搜索和读取过去的讨论、决策和实现上下文；Codex 和 Claude Code 均有宿主集成。

## 部署和依赖

支持本地 npm 安装与手工 sync；摘要后端可使用宿主认证或外部 provider。完全离线行为未验证。

## 证据边界

[当前代码版本](https://github.com/obra/episodic-memory/tree/7e06519357777badd7a115d2014a7ef845904310)。首次纳入的 v1.6.0 只作为 Release 水位，不作为本轮新事件。
