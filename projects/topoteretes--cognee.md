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

## 2026-10-19 版本追踪：v1.6.5

- Release 声称优化 Trace backlog 和 cognify 批次、将 docstring 连接到代码图，并增加 memify API；自定义 graph_model 生成最低依赖 datamodel-code-generator >=0.56.0。
- 状态：已发布，效果/延迟没有本仓库实测；[v1.6.5](https://github.com/topoteretes/cognee/releases/tag/v1.6.5)，2026-10-16T20:10:50Z；证据等级 `upstream_statement`。
