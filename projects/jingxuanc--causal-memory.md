# JingxuanC/causal-memory

Rust 本地记忆库与 MCP 服务，在 SQLite 中保留事实和决策–结果关系。

## 记忆机制

[SQLite schema](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/crates/causal-memory/src/store/mod.rs)把原始会话日志与可检索片段分表，[写入代码](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/crates/causal-memory/src/store/write.rs)保存带类型的 `caused`、`enabled`、`prevented` 等关系。[检索入口](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/crates/causal-memory/src/store/retrieve/mod.rs)提供关键词、语义、实体与多跳关系查询。边类型表示系统记录的关系，因果判断的可靠性仍需实验核实。

## 部署和依赖

[Rust workspace](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/Cargo.toml)使用 bundled SQLite。[CLI](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/crates/causal-memory-cli/src/lib.rs)默认启动 stdio MCP，数据库路径可配置。语义功能取决于所用构建和模型配置。此处已核对本地存储和入口，离线运行及宿主接入待实测。

## 评测证据

从 [MemDev-Bench v1 附录 F 表 9](https://arxiv.org/html/2610.27524v1) 的参评名单发现。该表覆盖相关历史条件下的固定 150 项任务，每个参评系统只运行一次。[上游 AMC 说明](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/docs/benchmarks/amc-2026.md)指出第一周期另用了参评检索实现。这里的固定源码、MemDev-Bench 参评配置和 AMC 服务分别保留证据。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 仓库 ID | 1312924592 |
| 创建时间（UTC） | 2026-07-26T15:37:51Z |
| 首次发现（UTC） | 2026-11-17T08:45:22.765Z |
| 首次公开 | 未核实 |
| 审读版本 | [固定提交](https://github.com/JingxuanC/causal-memory/tree/b05d671fc45d1f73c99c36a58f05c0bdd673cb88)，证据观察至 2026-11-17T08:47:44.561Z |
| 观察到的 GitHub Release | [v0.10.0](https://github.com/JingxuanC/causal-memory/releases/tag/v0.10.0)，发布于 2026-10-16T07:12:13Z |
| 许可证 | [固定版本 LICENSE](https://github.com/JingxuanC/causal-memory/blob/b05d671fc45d1f73c99c36a58f05c0bdd673cb88/LICENSE)，GitHub API 识别为 Apache-2.0 |
| 证据等级 | code_inspected；尚无本仓库运行或评测结果 |

Release 记录用于建立跟踪基线。每日采集将分别记录元数据、默认分支 HEAD 和完整增量 Release。
