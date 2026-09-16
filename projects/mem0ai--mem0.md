# mem0ai/mem0

独立记忆层，向 Agent 提供记忆写入与检索接口。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `0df3e4b87df20785f0741370c75e44428796193e` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；本轮仅检查 HEAD 差异，未运行上游代码 |

## 记忆机制

记录语义、实体及时间相关的记忆；重点追踪提取和更新策略。

## 部署和依赖

上游同时提供 OSS SDK、自托管服务器和托管平台；自托管不自动等于离线运行。

## 证据与核实范围

阅读了[上游 README](https://github.com/mem0ai/mem0/blob/main/README.md)；[当前代码版本](https://github.com/mem0ai/mem0/tree/0df3e4b87df20785f0741370c75e44428796193e)。本轮从上一水位 `b51f7692...` 对比到当前 HEAD，只发现文档变化，没有据此生成技术事件。未运行服务或复现评测。

[元数据来源](https://api.github.com/repos/mem0ai/mem0)；[HEAD 来源](https://api.github.com/repos/mem0ai/mem0/git/ref/heads/main)。

## 限制与本轮变化

README 的托管平台评测包含未进入 OSS SDK 的专有优化，不能直接作为开源版本性能。本轮没有新 Release，HEAD 的文档差异不计为核心技术变化。
