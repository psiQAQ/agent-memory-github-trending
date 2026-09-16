# getzep/graphiti

面向 Agent 的动态、时间感知知识图谱。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_temporal_memory |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `c035afb7990b6077331a81e98b04efcfd9bf8184` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

以 episode 保存来源，将实体与事实关系组织为图，保留事实有效时间与失效历史。

## 部署和依赖

自托管图数据库和模型配置需由部署者提供；不要把 Zep 托管平台能力等同于 Graphiti。

## 证据与核实范围

阅读了[上游 README](https://github.com/getzep/graphiti/blob/main/README.md)；[本轮记录的代码版本](https://github.com/getzep/graphiti/tree/c035afb7990b6077331a81e98b04efcfd9bf8184)。实现/评测资产线索：graphiti_core/ 与 tests/。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/getzep/graphiti)；[HEAD 来源](https://api.github.com/repos/getzep/graphiti/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

本轮未执行索引、检索或性能实验；吞吐和延迟不作独立保证。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
