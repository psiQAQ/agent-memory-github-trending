# letta-ai/letta-code

带身份和持久记忆的有状态 Agent harness。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | stateful_agent, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `3be3df32467613382713f017c207be7c1afb2281` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

上游介绍 memory blocks、消息搜索、MemFS 的 Git 跟踪及周期性整理，允许上下文与技能随运行变化。

## 部署和依赖

CLI 可配置自己的模型连接；Cloud 的状态存储和远程计算是另一个部署边界。

## 证据与核实范围

阅读了[上游 README](https://github.com/letta-ai/letta-code/blob/main/README.md)；[本轮记录的代码版本](https://github.com/letta-ai/letta-code/tree/3be3df32467613382713f017c207be7c1afb2281)。实现/评测资产线索：src/ 与 README 的 memory/MemFS 功能表。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/letta-ai/letta-code)；[HEAD 来源](https://api.github.com/repos/letta-ai/letta-code/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

记忆自修改的有效性、隔离和回滚需要进一步检查代码；本轮只核实公开说明。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
