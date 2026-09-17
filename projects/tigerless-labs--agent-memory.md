# tigerless-labs/agent-memory

本地优先的长期记忆运行时：Markdown 文件是事实源，SQLite/FTS 与可选向量索引都是可重建缓存，Claude Code 与 Codex 可共享同一 store。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent / local_first / memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `34d12a2f8678d5561aba27bd8ff73c5ae4b6a258` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

读取路径组合 MEMORY.md 固定注入、FTS5/BM25 与可选向量 RRF，以及直接文件系统浏览；会话边界触发写入，sleep-time Manage 层负责合并和提出删除建议。

## 部署和依赖

上游声明本地安装、无 API key 的基本读写路径，并提供 Claude Code/Codex hook 与 MCP；本仓库未验证完全离线运行。

## 证据边界

[当前代码版本](https://github.com/tigerless-labs/agent-memory/tree/34d12a2f8678d5561aba27bd8ff73c5ae4b6a258)。README 中 LongMemEval-S 和跨宿主实验数据是上游测量，不是本仓库复现结果。
