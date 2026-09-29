# 外部记忆评测参考

用途：作为 Agent Memory 评测方法、候选发现和证据边界的参考，不替代本仓库的 Star 关注度统计，也不自动提升候选。

## Verging Labs Agentic Memory Index

- 榜单：https://verginglabs.com/
- 方法：https://verginglabs.com/methodology
- 机器可读数据：https://verginglabs.com/index/memory.json
- 变更记录：https://verginglabs.com/changelog
- 当前核实版本：`v0.2`，发布日期 `2026-09-16`，`datasetId=6b0dd2681430eca3`。
- 方法页说明该版本覆盖 12 个 memory tools；每个 tool 有 150 个 scored probes，跨 56 sessions 的模拟多周工作关系。因此“1,800”是 12×150 的执行量，不是 1,800 个不同真实生产任务。
- 公开 JSON 中 Cognee 与 Karpathy Wiki 的 `indexScore` 都是 97.1；这里只记录该版本来源结果，不把它改写成通用准确率、质量总榜或“任意 Markdown 优于图数据库”。Karpathy Wiki 被来源描述为 published/open method，而不是已核实的独立产品仓库。
- scored task split 为私有；质量、成本和延迟应分开解释。未做独立复现，也未核实到该评测本身的官方公开代码仓库，因此不得虚构 owner/repo、Stars 或 repository_id。

## vectorize-io/agent-memory-benchmark（AMB）

- 仓库：https://github.com/vectorize-io/agent-memory-benchmark
- 本仓库已有项目卡：`projects/vectorize-io--agent-memory-benchmark.md`，沿用其稳定 repository_id，不重复收录。
- AMB README 公开 ingest → retrieve → generate → judge 的分阶段评测，并分别记录摄取/检索耗时；部分 retrieval-only 数据集使用独立断言协议。
- AMB 与 Verging Labs 是不同评测协议，分数不得互换或直接横排。AMB 由 Vectorize 发布且用于评估包括 Hindsight 在内的系统，报告时保留发布方与参评产品关系。

每轮只读取公开一手材料，不执行安装、MCP、上游测试或需要模型 API key 的评测，不产生额外费用。首次观察旧榜单只建立参考基线；只有版本、方法或经核实结果发生变化时才更新说明。
