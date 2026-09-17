# topoteretes/cognee

自托管 Agent Memory 平台，将文本、代码与会话经验组织成知识图谱、向量索引和可检索的长期上下文。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_memory / coding_agent / session_memory |
| 首次发现（UTC） | 2026-09-16T07:36:37Z |
| 本次 HEAD | `c0d18c80e24b7b78918e7642c03f6f128fdd2aee` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

`remember` 写入永久或 session memory，`recall` 在图、向量和代码上下文间检索，`improve` 用反馈和会话经验丰富长期记忆。上游还提供 Claude Code、Codex、OpenClaw 与 MCP 接入。

## 部署和依赖

上游明确提供本地安装、自托管和 Docker 路线，也支持本地模型；完全离线行为未在本仓库验证。

## 证据边界

[当前代码版本](https://github.com/topoteretes/cognee/tree/c0d18c80e24b7b78918e7642c03f6f128fdd2aee)。本轮只核对 README、metadata、HEAD 和 Release 水位，不复现检索质量。
