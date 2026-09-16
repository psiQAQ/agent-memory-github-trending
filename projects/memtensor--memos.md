# MemTensor/MemOS

记忆组织、检索、更新与跨任务经验复用的操作层。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `de8069428a9247bfa7a3d35f59a9b39fa8f231d2` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

关注记忆单元、图组织、调度和反馈修正，以及经验到可复用策略的转化。

## 部署和依赖

本地插件与云服务是不同组件；宿主支持和外部模型依赖应逐组件核对。

## 证据与核实范围

阅读了[上游 README](https://github.com/MemTensor/MemOS/blob/main/README.md)；[本轮记录的代码版本](https://github.com/MemTensor/MemOS/tree/de8069428a9247bfa7a3d35f59a9b39fa8f231d2)。实现/评测资产线索：src/、packages/ 与 evaluation/。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/MemTensor/MemOS)；[HEAD 来源](https://api.github.com/repos/MemTensor/MemOS/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

节省 token 等数字目前只属于作者报告；本轮不将其横排为性能优劣。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
