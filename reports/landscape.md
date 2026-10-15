# Agent Memory 生态与选型路线

这是一份基于已登记证据的选型导图，不是完整生态普查、性能排名或购买推荐。分类允许重叠；本页沿用 2026-10-15 的材料，不把仓库名猜成架构，也不把观察版本当作实时最新版。

## 四层生态视角

<a id="storage"></a>
### 01 存储与组织：记忆以什么形式保存？

**图与时序关系 → Graphiti**：用 episode 保留来源，组织实体与事实关系，记录有效时间和失效历史。适合研究关系随时间变化的建模；还要承担图数据库与模型配置的成本。[项目卡](../projects/getzep--graphiti.md)

**虚拟文件系统 → OpenViking**：以 viking:// 统一资源、记忆、技能，以 L0/L1/L2 摘要层级逐步加载。这是组织和按需读取的路线，不应据此填入未经测量的 Token 节省比例。[项目卡](../projects/volcengine--openviking.md)

**Git/SQLite → 候选路线**：tiramisu 的 Git 文件与 gomem/MemNexus 的 SQLite 来自初审说明。可对比可读性、协作冲突、部署依赖，但尚不构成正式选型推荐。[候选比较](latest.md#新候选对比)

<a id="framework"></a>
### 02 记忆服务：怎样写入、检索与维护？

**retain / recall / reflect → Hindsight**：保存信息、查询记忆、基于记忆回应，memory bank 组织命名空间。评估时应分别检查持久化、检索和生成阶段，不能用一次回答质量替代全部机制验证。[项目卡](../projects/vectorize-io--hindsight.md)

**独立记忆层 → Mem0**：以记忆写入和检索接口服务 Agent；具体依赖、部署与协议按对应版本核查，而不是只看框架总 Stars。[项目卡](../projects/mem0ai--mem0.md)

<a id="clients"></a>
### 03 客户端与宿主：记忆怎样进入实际工作流？

**有状态工作流 → Letta Code**；**会话观察与注入 → Claude-Mem**；Hindsight/OpenViking 也包含 Coding Agent 集成。宿主支持必须区分“上游文档列出”“存在指定版本实现”“本仓库运行验证”，不能将列出 Codex/Claude Code/Cursor 名称当作所有平台实测通过。[Letta Code](../projects/letta-ai--letta-code.md) · [Claude-Mem](../projects/thedotmack--claude-mem.md)

<a id="benchmarks"></a>
### 04 评测与基准：质量是怎样测出来的？

LongMemEval / LongMemEval-V2、Agent Memory Benchmark 属于评测资产，不能与记忆服务按总 Star 混成质量榜。dolphinbench 仍在候选队列；需要标注发布方 Mem0 与被评系统的关系。[LongMemEval](../projects/xiaowu0162--longmemeval.md) · [AMB](../projects/vectorize-io--agent-memory-benchmark.md) · [外部参考](../docs/references.md)

## 已有证据能支持的横向比较

| 项目 | 组织 / 存储路线 | 检索与维护 | 依赖 / 宿主边界 | 许可证记录 | Token / 性能收益 | 证据入口 |
| --- | --- | --- | --- | --- | --- | --- |
| Graphiti | 动态时序知识图谱；episode 来源 | 事实有效期/失效历史；删除与隔离仍需专项审查 | 需图数据库与模型配置；不能等同 Zep 托管平台 | API 识别 Apache-2.0 | 未独立测量 | [项目卡](../projects/getzep--graphiti.md) |
| Hindsight | memory bank 命名空间；具体后端选项此处未复核 | retain/recall/reflect；Coding Agent 知识页先检索再按需读取 | 上游提供自托管、嵌入式与 Cloud；完整离线未验证 | API 识别 MIT | 未独立测量 | [项目卡](../projects/vectorize-io--hindsight.md) |
| OpenViking | viking:// 统一资源/记忆/技能；L0/L1/L2 分层 | 会话提交后抽取/演化；按相关性读取经验 | 上游列出 Claude Code、Codex、Cursor 等；服务端/插件单独升级 | API 识别 AGPL-3.0 | 未独立测量 | [项目卡](../projects/volcengine--openviking.md) |
| Letta Code | 有身份和持久记忆的有状态 Agent；具体存储未在此复核 | 工作流 worker 工具继承与校验 | 需要区分全局 mod 工具与父 Agent 私有工具 | 此页未核实 | 未独立测量 | [项目卡](../projects/letta-ai--letta-code.md) |

许可证列只是指定时点的元数据，不是法律适用结论；实际使用应阅读对应版本许可证。候选的 SQLite/Git 路线及评测资产另见[本期六项候选表](latest.md#新候选对比)，不把未审查对象混入已验证推荐清单。

## 技术节点时间线

只列本仓库已收集到的节点，**不是 2025–2026 年的完整历史**。日期使用 UTC 的事件时间，不用首次发现时间代替发布日；对应来源均保留完整时间。状态截至本期检查。

| 事件日期（UTC） | 节点 | 状态与读者含义 | 一手来源 |
| --- | --- | --- | --- |
| 2026-10-09 | OpenViking Gateway Beta / v0.5.0 | 已发布；模型协议代理参与检索、注入和保存，宿主插件仍需独立升级 | [Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.0) |
| 2026-10-13 | Hindsight v1.0.0 | 已发布；会话留存、注入及集成修复，不以版本号推断性能 | [Release](https://github.com/vectorize-io/hindsight/releases/tag/v1.0.0) |
| 2026-10-14 | Graphiti v0.31.0 | 已发布；默认模型与请求配置变化 | [Release](https://github.com/getzep/graphiti/releases/tag/v0.31.0) |
| 2026-10-15 | Letta Code v0.34.15 | 已发布；工作流工具接入变化 | [Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.15) |
| 2026-10-15 | Hindsight scope / OpenViking 写入状态修复 | 已合并未发布；关注正确性和升级回归 | [Hindsight PR](https://github.com/vectorize-io/hindsight/pull/5596) · [OpenViking PR](https://github.com/volcengine/OpenViking/pull/5803) |

## 怎样读评测，而不是只看分数

先核对数据集与公开/私有拆分、模型版本、记忆构建和检索设置、提示词与评分程序，再分别比较召回质量、任务完成、摄取/检索时间、Token 和费用。发布方自己的评测可提供有用线索，但利益关系必须展示；托管产品分数不归给同名开源库。

本次只整理现有资产，没有新增运行上游 benchmark、调用付费模型或宣称任何节省百分比。轻量本地评测可作为后续独立项目：先批准任务/环境/预算/基线和指标，再运行并公开失败样例。未完成这一步，表中的收益保持未知。
