# memodb-io/memobase

将用户画像与事件时间线组织为长期记忆的工程系统。

## 记忆机制

重点不是通用 Agent 自治记忆，而是把长期用户信息整理成可配置 profile 与 event timeline，并以批处理降低在线记忆提取成本。

## 部署和依赖

上游描述服务基于 FastAPI、Postgres、Redis，支持 Docker 自托管，同时提供 Python/Node/Go 客户端和 MCP。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | user_memory / temporal_memory |
| 首次发现（UTC） | 2026-09-16T07:36:37Z |
| 记录的 HEAD | `358c16bbc6d687937d79bc2f984a11c3be8da901` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

[上游 README](https://github.com/memodb-io/memobase/blob/main/readme.md)；[记录的代码版本](https://github.com/memodb-io/memobase/tree/358c16bbc6d687937d79bc2f984a11c3be8da901)。性能与成本数字均保留为作者声明，未复现。
