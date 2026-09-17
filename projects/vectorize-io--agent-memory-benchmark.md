# vectorize-io/agent-memory-benchmark

面向现代长上下文 Agent Memory 的开放评测框架，覆盖准确率、检索/摄取耗时和 token 成本。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / benchmark |
| 分类 | memory_benchmark / agentic_tasks / retrieval_evaluation |
| 首次发现（UTC） | 2026-09-17T16:27:32Z |
| 本次 HEAD | `309e0065dade533f2c9c64511d20090d6cad4129` |
| 许可证 | GitHub API 未返回 SPDX；未作法律审查 |
| 证据等级 | upstream_statement；未运行评测 |

## 评测方式

上游 README 将流程拆成 ingest → retrieve → generate → judge，并单独记录 retrieval 与 ingestion 时间；部分 retrieval-only 数据集直接检查必须/不得召回的 memory ID 集合。仓库公开数据集接入、prompt、scoring logic 和运行 harness。

## 适用性

相对于仅面向长对话问答的记忆测试，该项目明确增加 Agent 场景并跟踪成本与速度，因此作为 benchmark 类项目补充工程项目占比较高的正式池。

## 证据边界

[README](https://github.com/vectorize-io/agent-memory-benchmark/blob/main/README.md)；[当前代码版本](https://github.com/vectorize-io/agent-memory-benchmark/tree/309e0065dade533f2c9c64511d20090d6cad4129)。没有执行 benchmark，未把上游结果当作独立复现。
