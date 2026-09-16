# xiaowu0162/LongMemEval

长期聊天交互记忆的评测基准。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / benchmark |
| 分类 | conversational_memory_evaluation |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `9e0b455f4ef0e2ab8f2e582289761153549043fc` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

测试长期对话中的信息检索、跨会话综合、时间与更新相关记忆；不是可部署的记忆层。

## 部署和依赖

评测数据、检索模块和评价脚本需要各自的环境配置。

## 证据与核实范围

阅读了[上游 README](https://github.com/xiaowu0162/LongMemEval/blob/main/README.md)；[本轮记录的代码版本](https://github.com/xiaowu0162/LongMemEval/tree/9e0b455f4ef0e2ab8f2e582289761153549043fc)。实现/评测资产线索：src/evaluation/evaluate_qa.py 及数据说明。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/xiaowu0162/LongMemEval)；[HEAD 来源](https://api.github.com/repos/xiaowu0162/LongMemEval/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

S/M/oracle 的输入条件不同；不得与 V2 结果混表比较。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
