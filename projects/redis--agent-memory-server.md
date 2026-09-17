# redis/agent-memory-server

Redis Agent Memory 的公开仓库同时承载当前产品说明、benchmark harness 与原始 V0 开源研究实现。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / session_memory / long_term_memory |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `94192c39e2a4a154f441a5411e3d73c4f54974a6` |
| 许可证 | GitHub API 为 NOASSERTION；仓库 README 声明 Apache-2.0，未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

上游说明区分 session memory 与 long-term memory：前者保留活跃会话状态，后者保存从历史会话抽取的事实与向量表示。仓库 `V0/` 保留原 Agent Memory Server 的公开实现，包含服务端源码与 Docker 配置。

## 部署和依赖

当前产品路线包含托管服务；V0 作为开放研究/自托管实现保留。是否可以完全离线运行未验证。

## 证据边界

[当前代码版本](https://github.com/redis/agent-memory-server/tree/94192c39e2a4a154f441a5411e3d73c4f54974a6)。首次纳入时只建立当前 Release 水位，不把旧版本当作本轮新事件。
