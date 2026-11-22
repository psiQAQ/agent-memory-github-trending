# vectorize-io/agent-memory-benchmark

面向现代长上下文 Agent Memory 的开放评测框架，分别观察准确率、检索/摄取耗时和 token 成本。

## 评测方式

上游 README 将流程拆成 ingest → retrieve → generate → judge，并单独记录 retrieval 与 ingestion 时间；部分 retrieval-only 数据集直接检查必须/不得召回的 memory ID 集合。仓库公开数据集接入、prompt、scoring logic 和运行 harness。

## 适用性

相对于仅面向长对话问答的记忆测试，该项目明确增加 Agent 场景并跟踪成本与速度，因此作为 benchmark 类项目补充工程项目占比较高的正式池。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / benchmark |
| 分类 | memory_benchmark / agentic_tasks / retrieval_evaluation |
| 首次发现（UTC） | 2026-09-17T16:27:32Z |
| 记录的 HEAD | `309e0065dade533f2c9c64511d20090d6cad4129` |
| 许可证 | GitHub API 未返回 SPDX；未作法律审查 |
| 证据等级 | upstream_statement；未运行评测 |

## 证据边界

[README](https://github.com/vectorize-io/agent-memory-benchmark/blob/main/README.md)；[记录的代码版本](https://github.com/vectorize-io/agent-memory-benchmark/tree/309e0065dade533f2c9c64511d20090d6cad4129)。没有执行 benchmark，未把上游结果当作独立复现。

## 2026-11-21｜LegalBench-RAG mini 增加字符级检索评测

AMB 加入 LegalBench-RAG mini，按返回证据覆盖的标注字符计算 recall@5。 已合并，已见上游结果更新。

该 split 覆盖 714 份合同与 776 道问题，每组 194 题。评估只运行检索，最多取五个结果，配置检索文本预算为 4096 tokens。评分将命中文本定位回文档，合并重叠片段，再计算覆盖的标注字符比例。默认上传中性文件名，AMB_LEGALBENCH_NAMES=original 使用语料原名。上游 #90 声称以 Hindsight fdae5ed70 与默认知识库配置重跑两种文件名设置，#83 的初始结果对应更早实现。Vectorize 同时维护 AMB 和参评系统 Hindsight，本轮仅核对协议代码和上游结果说明。

合并时间 2026-11-19T22:33:10Z，观测时间 2026-11-20T16:05:40.689Z，合并提交 5d422bea3ae4d971c84121cad2b38e6f64779401。在 2026-11-20T16:05:41.831Z 取得全部 11 个 PR 文件条目，按相关入口做静态审读。

[PR 与完整文件列表](https://github.com/vectorize-io/agent-memory-benchmark/pull/83) · [knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/dataset/knowledge.py) · [knowledge_data.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/dataset/knowledge_data.py) · [test_knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/tests/test_knowledge.py) · [hindsight_knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/memory/hindsight_knowledge.py) · [补充来源 1](https://github.com/vectorize-io/agent-memory-benchmark/pull/90) · [补充来源 2](https://github.com/vectorize-io/agent-memory-benchmark/blob/9738aa01da59cb73dae43ac0f05ea3b16a55aa99/src/memory_bench/dataset/knowledge.py)

[本轮日期稿](../reports/briefs/20261120T160119Z-local.md)。

## 2026-11-23

ATM-Bench 主表恢复 Hindsight fdae5ed70 那次摄取和检索的结果条目。 已合并，上游结果更新。

变更后的 results-manifest.json 将该条目标为 ATM-Bench 检索、1013 个查询和 recall@10。上游运行说明称 ATM-Bench 的摄取和检索均使用 fdae5ed70，ViDoRe V3 的检索另用 80bd005fc。Vectorize 同时维护该评测和 Hindsight。本次核对了结果清单和上游版本标注，压缩明细及差异原因未复核。

合并于 2026-11-21T08:24:47Z，观测于 2026-11-22T16:24:37.407Z。合并提交 f6004888820f59df2ee7b5178aae74e08b272876，PR 文件列表完整（5 个文件）。 证据等级 upstream_statement。 [PR #93](https://github.com/vectorize-io/agent-memory-benchmark/pull/93) · [results-manifest.json](https://github.com/vectorize-io/agent-memory-benchmark/blob/f6004888820f59df2ee7b5178aae74e08b272876/results-manifest.json) · [hindsight_knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/f6004888820f59df2ee7b5178aae74e08b272876/src/memory_bench/memory/hindsight_knowledge.py) · [本次简报](../reports/briefs/20261122T162043Z-local.md)
