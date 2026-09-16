# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `be0e93997a35d517250181c4dfb2d86c2dd95bc1` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，文档列出 PostgreSQL 及本地/托管模型选项。

## 证据与核实范围

阅读了[上游 README](https://github.com/vectorize-io/hindsight/blob/main/README.md)；[本轮记录的代码版本](https://github.com/vectorize-io/hindsight/tree/be0e93997a35d517250181c4dfb2d86c2dd95bc1)。实现/评测资产线索：hindsight-api/、客户端与 README 示例。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/vectorize-io/hindsight)；[HEAD 来源](https://api.github.com/repos/vectorize-io/hindsight/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

上游声称存在第三方复现不等于本仓库已经复现；本轮没有运行服务。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
