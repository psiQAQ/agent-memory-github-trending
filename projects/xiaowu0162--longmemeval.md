# xiaowu0162/LongMemEval

用于评测长期聊天交互中的记忆能力。

## 记忆机制

测试长期对话中的信息检索、跨会话综合、时间与更新相关记忆；不是可部署的记忆层。

## 部署和依赖

评测数据、检索模块和评价脚本需要各自的环境配置。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / benchmark |
| 分类 | conversational_memory_evaluation |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `9e0b455f4ef0e2ab8f2e582289761153549043fc` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/xiaowu0162/LongMemEval/blob/main/README.md)；[该次记录的代码版本](https://github.com/xiaowu0162/LongMemEval/tree/9e0b455f4ef0e2ab8f2e582289761153549043fc)。实现/评测资产线索：src/evaluation/evaluate_qa.py 及数据说明。README 阅读与 HEAD 采集并非同时完成；这部分证据属于上游说明，不等于代码审计。写入的具体触发条件、删除保证、隔离和存储后端，仍需结合对应实现进一步核实。

[元数据来源](https://api.github.com/repos/xiaowu0162/LongMemEval)；[HEAD 来源](https://api.github.com/repos/xiaowu0162/LongMemEval/git/ref/heads/main)。首次公开日期尚不明确，不能用仓库创建日期替代。

## 限制与本轮变化

S/M/oracle 的输入条件不同；不得与 V2 结果混表比较。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
