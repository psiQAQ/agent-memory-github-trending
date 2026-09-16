# 首轮研究基线 · 2026-09-16

本轮完成 8 个正式跟踪项目和 1 个历史参照的元数据与 HEAD 采集，另有 14 个未审查候选。它们不是按质量排出的 Top 9。数值与证据见[当前观测表](current.md)及[项目登记](../data/projects.json)。

本轮事件范围是“首次建立研究基线”，不是“过去 12 小时新闻”。尚未逐个建立 Release/PR 基线，后续检查优先补齐。正式项目目标 20 个尚未达到，不用搜索结果直接凑数。没有历史窗口，因此所有 7/30 日净增长暂为空。

## 值得继续跟踪的区别

**有状态 harness 与独立记忆层不是同一种产品。** [Letta Code 的上游说明](https://github.com/letta-ai/letta-code/blob/main/README.md)介绍 memory blocks、跨消息搜索和以 Git 跟踪上下文的 MemFS；[Mem0](https://github.com/mem0ai/mem0/blob/main/README.md)则是供其他应用接入的记忆层。研究时需要分别检查“整个 Agent 如何控制记忆”和“外部记忆服务提供什么操作”，不能按总 Star 横排架构优劣。

**必须跟随真实代码入口。** [Letta 旧仓库](https://github.com/letta-ai/letta/blob/main/README.md)已把当前代码指向 letta-code，并保留 archive 中的旧 V1 server。本仓库把旧项目列为历史参照，两个仓库独立记录 Stars。迁移实际发生日期尚未定位，不把发现日期当成迁移日期。

**托管平台的成绩不应归给开源组件。** [Mem0 README](https://github.com/mem0ai/mem0/blob/main/README.md)说明其平台评测含 OSS SDK 之外的专有优化；[Graphiti README](https://github.com/getzep/graphiti/blob/main/README.md)也区分开源图工具与 Zep 托管平台。后续比较优先核对具体组件、版本和模型设置，而不是复制宣传图上的最高分。

**长期聊天记忆与任务经验记忆的评测协议不同。** [LongMemEval](https://github.com/xiaowu0162/LongMemEval/blob/main/README.md)以长期交互为中心；[LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2/blob/main/README.md)包含多模态 Web Agent 轨迹、记忆模块和新的评价程序。两者单独建卡，不把不同基准中的得分相减来宣布进步。

**记忆维护和检索接口值得独立观察。** [Hindsight](https://github.com/vectorize-io/hindsight/blob/main/README.md)显式提供 retain/recall/reflect；[MemOS](https://github.com/MemTensor/MemOS/blob/main/README.md)覆盖记忆管理与经验复用；[claude-mem](https://github.com/thedotmack/claude-mem/blob/main/README.md)着重会话观察、压缩和上下文回注。这是机制分类，不是已经证明某一路线更有效。

## 核实等级和下一轮覆盖

以上均为阅读上游公开说明后的分类，证据等级为 upstream_statement；未安装服务、运行代码、复现 benchmark 或验证每个宿主。项目卡片已记录版本和未知项。正式代码审计与独立性能复现不能由 README 说明替代。

下一轮优先建立发布基线、检查新的 HEAD 差异，并从候选队列中按相关性与实现证据逐项收录。首次真正定时执行还将检查 Python 校验、GitHub 写入及回读能否在定时环境完成；交互式测试不替代这个验收。
