# xiaowu0162/LongMemEval-V2

用于评测长期任务经验和多模态 Web Agent 轨迹记忆。

## 记忆机制

从历史轨迹构建可供后续任务查询的经验；包含数据准备、memory_modules 与评价程序。

## 部署和依赖

不同公开规模、读取模型、embedding 和记忆基线需按协议记录。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / benchmark |
| 分类 | task_experience_evaluation |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `2cc8c540bdb87fe6761629b585e727e1c4704520` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/xiaowu0162/LongMemEval-V2/blob/main/README.md)；[该次记录的代码版本](https://github.com/xiaowu0162/LongMemEval-V2/tree/2cc8c540bdb87fe6761629b585e727e1c4704520)。实现/评测资产线索：data/、evaluation/、memory_modules/。README 阅读与 HEAD 采集并非同时完成；这部分证据属于上游说明，不等于代码审计。写入的具体触发条件、删除保证、隔离和存储后端，仍需结合对应实现进一步核实。

[元数据来源](https://api.github.com/repos/xiaowu0162/LongMemEval-V2)；[HEAD 来源](https://api.github.com/repos/xiaowu0162/LongMemEval-V2/git/ref/heads/main)。首次公开日期尚不明确，不能用仓库创建日期替代。

## 限制与本轮变化

不是 V1 简单追加样本；本文不复现 leaderboard，也不把两个版本得分直接相减。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。
