# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `81e4a674a96e0b9687712746295fd9f451a6b600` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | code_inspected；检查提交/diff，未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责启动上下文注入、知识页和宿主适配。

## 本轮代码级变化

- [`475cc02`](https://github.com/vectorize-io/hindsight/commit/475cc0278cdc638240d58e1cc816d8cb31ec4ff4)：reflect tools prompt 不再只传 `skepticism=5` 这类裸数值，而是补充 disposition level 的语义说明，降低模型把性格参数当作无意义 metadata 的风险，并增加兼容性测试。
- [`81e4a67`](https://github.com/vectorize-io/hindsight/commit/81e4a674a96e0b9687712746295fd9f451a6b600)：`list_banks` 不再在分页前聚合整个 `memory_units` 表；先确定返回页，再只对页内 bank 做 SQL fact count，使 bank 列表成本从全库规模转为主要受页大小约束。上游提交报告在 365 banks / 1.8M memory units / 11k documents / 543 MB 数据上主查询 131 ms→6 ms，50-bank 页的 index-only count 约 44 ms；本仓库未复现这些性能数字。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成。

## 证据边界

[当前代码版本](https://github.com/vectorize-io/hindsight/tree/81e4a674a96e0b9687712746295fd9f451a6b600)。本轮结论来自 2 个新增默认分支提交的 commit/diff 检查，不是运行时复现；Release 水位仍为 v0.10.0。
