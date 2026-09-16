# neo4j-labs/agent-memory

用图结构统一短期会话、长期实体事实和推理轨迹记忆。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_memory / reasoning_memory / MCP |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `f801acc654398e5bbe5551b49af66c17d3da5d5e` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

短期层保存会话与消息；长期层保存实体、偏好和事实知识图谱；reasoning memory 保存推理步骤和工具使用，并支持相似任务检索。

## 部署和依赖

上游同时提供托管 NAMS 和自托管 Neo4j/Bolt 路线，并提供 MCP 与多 Agent 框架集成。空气隔离能力是上游声明，本仓库未测试。

## 证据与核实范围

[上游 README](https://github.com/neo4j-labs/agent-memory/blob/main/README.md)；[本轮代码版本](https://github.com/neo4j-labs/agent-memory/tree/f801acc654398e5bbe5551b49af66c17d3da5d5e)。最新 Release 水位为 `python-v0.6.0`；本轮首次纳入，因此不把该旧发布当成新事件。
