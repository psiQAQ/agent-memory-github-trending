# 最新研究简报

本轮：`20261015T085418Z-interactive`；完成（UTC）：2026-10-15T08:54:18Z（北京时间 2026-10-15 16:54:18）。

本轮是手动 API-native 维护。21 个项目的 metadata、HEAD 和相对于旧成功水位的 Release 增量均完成；历史发布并未穷尽回灌。4 个 HEAD 变化不直接等同于技术进展，下列结论绑定到具体 PR、实现与状态。

## 已核实的变化

### Graphiti v0.31.0：默认模型与请求参数适配

OpenAI 客户端的常规与 small 默认模型改为 gpt-6-luna，重排序默认模型改为 gpt-4.1-mini；客户端为 GPT-6 请求构造显式缓存选项，并按模型版本选择 reasoning 参数。这是调用兼容性和默认配置变化，未验证实际费用、延迟或检索质量。

正式发布证据：[v0.31.0](https://github.com/getzep/graphiti/releases/tag/v0.31.0)；发布（UTC）：2026-10-14T23:58:36Z。

状态：`released`；发布版本：`v0.31.0`。来源：[PR #1999](https://github.com/getzep/graphiti/pull/1999)，合并 commit `82db2a4c57e2a9995f5e9526f51d76799db60740`；合并（UTC）：2026-10-14T21:09:02Z；观察（UTC）：2026-10-15T08:50:08Z。证据等级：`code_inspected`，仅作静态检查。

[实现 1](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/llm_client/openai_base_client.py) · [实现 2](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/cross_encoder/openai_reranker_client.py)

### Letta Code v0.34.15：工作流子代理恢复全局 mod 工具

Workflow worker 可继承可解析的全局 mod 工具；显式 allowedTools 中未知工具或 agent-scoped 工具会报错，避免静默得到零工具 worker。代码区分全局工具与仅属于父 Agent 的工具，未独立运行该工作流。

正式发布证据：[v0.34.15](https://github.com/letta-ai/letta-code/releases/tag/v0.34.15)；发布（UTC）：2026-10-15T05:10:26Z。

状态：`released`；发布版本：`v0.34.15`。来源：[PR #5078](https://github.com/letta-ai/letta-code/pull/5078)，合并 commit `5333d2060f0719882d622d0f05b1c9feffc987b8`；合并（UTC）：2026-10-14T18:06:21Z；观察（UTC）：2026-10-15T08:50:08Z。证据等级：`code_inspected`，仅作静态检查。

[实现 1](https://github.com/letta-ai/letta-code/blob/cc4654acc3b424a68c385bce0fe0c00edaad5d7e/src/tools/workflow/sdk-spawner.ts) · [实现 2](https://github.com/letta-ai/letta-code/blob/cc4654acc3b424a68c385bce0fe0c00edaad5d7e/src/tools/impl/workflow.ts)

### Hindsight：按实际 observation scope 变化决定重建

re-retain 与 tags PATCH 使用解析后的 scope 集合判断是否失效；shared 或不依赖标签的显式 scope 下，标签变化保留既有 observations，避免无意义的整文档重新 consolidation。该改动已合并，但本轮最新正式 Release 仍为 v1.0.0，尚未包含这次 10 月 15 日的提交。

状态：`merged_unreleased`。来源：[PR #5596](https://github.com/vectorize-io/hindsight/pull/5596)，合并 commit `e9f456df857c6185efac9a8b7a0f733a9dab8b5d`；合并（UTC）：2026-10-15T08:27:16Z；观察（UTC）：2026-10-15T08:50:08Z。证据等级：`code_inspected`，仅作静态检查。

[实现 1](https://github.com/vectorize-io/hindsight/blob/e9f456df857c6185efac9a8b7a0f733a9dab8b5d/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py) · [实现 2](https://github.com/vectorize-io/hindsight/blob/e9f456df857c6185efac9a8b7a0f733a9dab8b5d/hindsight-api-slim/hindsight_api/engine/memories/pg/retain.py)

### OpenViking：可选的 Redis 空闲会话提交调度

新增 Redis expiry 调度与会话适配器，按到期时间处理空闲 session，并复用既有提交路径；默认仍为 legacy backend。该能力已合并、尚未发布，未验证多进程故障恢复、吞吐或 Windows 运行。

状态：`merged_unreleased`。来源：[PR #6046](https://github.com/volcengine/OpenViking/pull/6046)，合并 commit `89fbcb96822c6aaab2828395b9f65e91846de001`；合并（UTC）：2026-10-15T03:42:40Z；观察（UTC）：2026-10-15T08:50:08Z。证据等级：`code_inspected`，仅作静态检查。

[实现 1](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/service/session_expiry.py) · [实现 2](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/scheduling/expiry/config.py)

### OpenViking：原生存储失败不再被当作成功写入

StoreEngineProxy 的 write/delete/clear/两个 batch 入口开始检查原生返回状态，非零状态抛出 RuntimeError；这防止底层未持久化时上层仍返回成功 ID。该修复已合并、尚未发布；PR 中的测试和真实 I/O 复现属于上游声明，本仓库没有重复运行。

状态：`merged_unreleased`。来源：[PR #5803](https://github.com/volcengine/OpenViking/pull/5803)，合并 commit `f75b6141dc477d7f35049fb1782c937bfc29a60c`；合并（UTC）：2026-10-15T08:12:47Z；观察（UTC）：2026-10-15T08:50:08Z。证据等级：`code_inspected`，仅作静态检查。

[实现 1](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/storage/vectordb/store/local_store.py)

## 新线索与筛选

broad 与无 Star 门槛 new 两个 agentic memory 查询各检查 2 页，共 80 条结果、78 个不同仓库 ID。连接器未给 sort、total_count 或 incomplete_results，原始日志保留 null；页预算结束时仍满页，不能声称穷尽。搜索结果明细保存在快照中，和正式观察池分开。

本轮按 pinned HEAD 阅读 9 条线索的 README，并核对完整 tree 中的资产路径。以下 6 条仅进入待审队列，尚未正式收录或推荐：

- [libingzheren/Jev-Mem](https://github.com/libingzheren/Jev-Mem/blob/7ab0c73c6d8f4f611ad252c1e6ba8083f8df0e44/README.md)：以轻量控制器组织语义、时间、因果与实体关系，并由语言模型综合答案；公开实现和评测入口存在，效果声明未复现。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。
- [mem0ai/dolphinbench](https://github.com/mem0ai/dolphinbench/blob/81cb6f8405b40a9e76089cef650806a80af06ea2/README.md)：通过模拟应用中的工具动作评估长期记忆，公开数据、runner 与 grader；发布方是 Mem0，不能将其参评成绩视为独立产品质量认证。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。
- [Homy-Xu/MemTrace](https://github.com/Homy-Xu/MemTrace/blob/5508f8be81025d8aa90726b1e06aef4ea484e577/README.md)：把不可变执行记忆与仓库状态绑定，再对齐当前任务后恢复证据；公开 runtime 和 benchmark adapter，DeepSWE 等复现声明未验证。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。
- [zhangjinhan-nudt/MemNexus](https://github.com/zhangjinhan-nudt/MemNexus/blob/41df6ca3cb49c9d13eba656d03068aee5b5e0f88/MemNexus/memory-system/README.md)：SQLite 权威事实、长短期记忆和证据约束的抽取/更正/混合检索；存在实现路径，宿主集成和评测完整性仍需审查。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。
- [buildsip/tiramisu](https://github.com/buildsip/tiramisu/blob/9f1d7c62cc24b54e76737182d63f4a0e514a1e40/README.md)：以 Git 中的文件保存项目、个人与团队记忆，并提供 CLI/MCP 读写路径；作者标为 Alpha，尚未检查权限和冲突处理。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。
- [alpdeniz/gomem](https://github.com/alpdeniz/gomem/blob/c069da2b1c8c02bc444594c23558071c14997043/README.md)：Go/SQLite 持久记忆与语义/关键词混合召回，支持遗忘和维护；Python 为需构建的 ctypes 桥接，Windows 路径未验收。 证据为 `upstream_statement`，实现资产存在性不代表质量验收。

其余三条的实际边界：

- [SIAT-INVS/OpenMAMS](https://github.com/SIAT-INVS/OpenMAMS/blob/3258125b6cdba73ca6429ec652a1748e66cb5600/README.md)：README 明确当前仅公开采集器与卫星回传工具，论文的记忆估值、GAE 和 MemCen 优化实现尚未包含；暂不收录为公开记忆实现。
- [simplearm/SimpleARM](https://github.com/simplearm/SimpleARM/blob/9c6c69bfb79c2d5d890bb7308623fddcb866c636/README.md)：完整 tree 仅有 README；作者声明代码尚未发布，仅作论文背景，不纳入可检查实现候选。
- [AgentMemoryRepo/agentmemoryrepo](https://github.com/AgentMemoryRepo/agentmemoryrepo/blob/8798cb26c817d451a5ed6cba0ad8d9eca8d5ec3e/README.md)：公开格式规范与宿主 Skill；按背景方法记录，未把静态规范等同于独立持久记忆引擎。

正式项目数量保持 20 个，另有 1 个历史参照、26 个待审候选；总池 47 个。剩余搜索命中仍是原始检索证据，不自动进入候选池，后续发现继续受 50 个上限和审查预算约束。

## 覆盖与验证边界

Release 的旧成功水位已经逐来源到达，四项分页待办可以关闭。既有未深读区间仍保留，当前这五项检查不能替代全部实现/文档/PR 审查；OpenViking compare 的 300 文件返回值也不能当成完整文件覆盖。

API-native batch 保持 events=[]，五项结论进入 structured-event backfill 队列，不伪造 event_id。7/30 日增长无容差内基线，继续为空。W39–W41 周报已存在，本周 W42 尚未结束，没有新周报到期。

外部参考的[机器可读数据](https://verginglabs.com/index/memory.json)和[变更记录](https://verginglabs.com/changelog)仍显示 v0.2、2026-09-16、datasetId=6b0dd2681430eca3；未把托管产品分数归给 OSS 库，也未比较不兼容协议。

未执行任何上游安装、测试或付费 API。当前 Scheduled 管理页仍搜索不到原任务；本轮不改变平台任务、cadence 或启用门禁，不计作新的无人值守验收。
