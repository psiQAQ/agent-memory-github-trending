# MemTensor/MemOS

用于组织、检索、更新记忆，并在不同任务间复用经验的操作层。

## 记忆机制

关注记忆单元、图组织、调度和反馈修正，以及经验到可复用策略的转化。

## 部署和依赖

本地插件与云服务是不同组件；宿主支持和外部模型依赖应逐组件核对。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `176d4f676a93e0e34ca9fd50091eff5ad3236506` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；本轮检查了 HEAD 差异，未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/MemTensor/MemOS/blob/main/README.md)；[记录的代码版本](https://github.com/MemTensor/MemOS/tree/176d4f676a93e0e34ca9fd50091eff5ad3236506)。本轮从上一水位 `de806942...` 检查了 7 个提交的差异，主要新增按模型 QPS 的分布式 LLM 限流、Redis GCRA、配置与测试；它更偏基础设施可靠性，不当作新的记忆算法结论。

[元数据来源](https://api.github.com/repos/MemTensor/MemOS)；[HEAD 来源](https://api.github.com/repos/MemTensor/MemOS/git/ref/heads/main)。

## 限制与本轮变化

节省 token 等数字仍只属于作者报告。本轮没有运行服务，也没有独立验证限流在生产环境的行为。
