# mem0ai/mem0

独立记忆层，向 Agent 提供记忆写入与检索接口。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `b51f7692f002d4f8719dd5c0f23d4d129003757d` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

记录语义、实体及时间相关的记忆；重点追踪提取和更新策略。

## 部署和依赖

上游同时提供 OSS SDK、自托管服务器和托管平台；自托管不自动等于离线运行。

## 证据与核实范围

阅读了[上游 README](https://github.com/mem0ai/mem0/blob/main/README.md)；[本轮记录的代码版本](https://github.com/mem0ai/mem0/tree/b51f7692f002d4f8719dd5c0f23d4d129003757d)。实现/评测资产线索：mem0/ 与 tests/。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/mem0ai/mem0)；[HEAD 来源](https://api.github.com/repos/mem0ai/mem0/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

README 的托管平台评测包含未进入 OSS SDK 的专有优化，不能直接作为开源版本性能。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
