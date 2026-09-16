# TencentCloud/TencentDB-Agent-Memory

面向多 Agent 团队的记忆资产中枢，将会话、文档和代码转成可复用资产。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | team_memory / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `8f2dc830317934e54548472bf62c5999f9bb1202` |
| 默认分支 | `feat/server_team` |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

上游把 Chat Memory、Skill、Wiki、CodeGraph 作为四类可治理资产，并支持团队共享、Agent 绑定、版本与权限管理。Proxy 路线面向多种 Coding Agent 复用同一 Memory Hub。

## 部署和依赖

上游提供本地多服务一键启动和面板，支持自托管；MongoDB 后端标记为实验性。自托管不代表不需要外部 LLM，离线运行未核实。

## 证据与核实范围

[上游 README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/README.md)；[本轮代码版本](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/8f2dc830317934e54548472bf62c5999f9bb1202)。本仓库没有执行安装脚本、Proxy 或 Memory Hub。
