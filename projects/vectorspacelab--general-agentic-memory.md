# VectorSpaceLab/general-agentic-memory

以分层 Agent 文件系统组织长文本、长视频与长时 Agent 轨迹记忆的研究实现。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / research |
| 分类 | hierarchical_memory / agent_trajectory |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `565db2cc2518d377e44389b82aecf3cc129d5fe5` |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

LLM 对输入分块后生成 Memory/TLDR，并按层级目录组织；支持增量加入内容。长时轨迹场景把复杂推理与工具调用日志压缩成可搜索、可记忆、可召回的结构。

## 部署和依赖

上游同时给出 Python SDK、CLI、REST API、Web 界面以及研究代码，可使用本地文件系统或 Docker 工作区。模型后端仍可能依赖外部服务，完全离线未核实。

## 证据与核实范围

[上游 README](https://github.com/VectorSpaceLab/general-agentic-memory/blob/main/README.md)；[本轮代码版本](https://github.com/VectorSpaceLab/general-agentic-memory/tree/565db2cc2518d377e44389b82aecf3cc129d5fe5)。未复现实验结果。
