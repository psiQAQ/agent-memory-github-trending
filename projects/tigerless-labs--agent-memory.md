# tigerless-labs/agent-memory

以 Markdown 文件为事实源的本地优先长期记忆运行时。SQLite/FTS 与可选向量索引均为可重建缓存；Claude Code 与 Codex 可共享同一 store。

## 记忆机制

读取路径组合 MEMORY.md 固定注入、FTS5/BM25 与可选向量 RRF，以及直接文件系统浏览；会话边界触发写入，sleep-time Manage 层负责合并和提出删除建议。

## 部署和依赖

上游声明本地安装、无 API key 的基本读写路径，并提供 Claude Code/Codex hook 与 MCP；本仓库未验证完全离线运行。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent / local_first / memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `34d12a2f8678d5561aba27bd8ff73c5ae4b6a258` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据边界

[记录的代码版本](https://github.com/tigerless-labs/agent-memory/tree/34d12a2f8678d5561aba27bd8ff73c5ae4b6a258)。README 中 LongMemEval-S 和跨宿主实验数据是上游测量，不是本仓库复现结果。

## 2026-10-16：可复用的记忆写入工具契约（仅静态检查）

默认分支 [`c395acc`](https://github.com/tigerless-labs/agent-memory/tree/c395acc4708c545c4b5395f8a2cb1e3a3ababd14) 新增 [WriteToolkit](https://github.com/tigerless-labs/agent-memory/blob/c395acc4708c545c4b5395f8a2cb1e3a3ababd14/packages/core/src/agent_memory/core/toolkit.py)，统一 `recall`、`read`、`submit_operations`，提交的操作经校验后交由库的统一写入路径，而不是由工具直接写 Store。[MCP write session](https://github.com/tigerless-labs/agent-memory/blob/c395acc4708c545c4b5395f8a2cb1e3a3ababd14/packages/mcp/src/agent_memory/mcp/write_session.py)复用相同工具接口。状态：默认分支已合并，未确认正式 Release；证据 `code_inspected`，尚未实测宿主、事务一致性或安全性。

## 2026-10-19 Muse 工具调用兼容性

- 新增 loopback 的 Muse/OpenRouter namespace 适配，将 namespaced MCP 子工具转换为 `<namespace>__<tool>` 格式，暂时改写独立设置并在退出时恢复。仅静态检查实现与测试，未执行 Muse 1.4.x 实验。
- 状态：已进入默认分支，无正式 Release 证据。固定版本：[实现](https://github.com/tigerless-labs/agent-memory/blob/327bc51106e854aab63a7a769842a4872f6adb01/packages/executor/src/agent_memory/executor/muse_namespaces.py)、[测试](https://github.com/tigerless-labs/agent-memory/blob/327bc51106e854aab63a7a769842a4872f6adb01/tests/unit/test_muse_namespaces.py)；证据等级 `code_inspected`，事件时间未核实。
