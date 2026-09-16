# 筛选、分类与统计方法

方法版本：0.1-draft；待确认。本文是统计口径的唯一说明，具体默认值在 `config/tracker.json`。阈值是本项目拟定的工作规则，不是 GitHub 官方标准或经过验证的预测模型。

## 收录边界

核心对象是为 LLM Agent 提供可检查的持久化/工作记忆机制、记忆操作或记忆评测的 GitHub 项目。优先记录实际写入、组织、检索、更新、压缩、删除/遗忘或经验复用路径，而非只因描述中出现 memory 就收录。

工程分类：通用记忆层、有状态 Agent、Coding Agent 记忆插件、图/时间/层级记忆、记忆压缩与维护、经验/程序性记忆、评测基准。允许多标签，但项目计数按稳定仓库 ID 去重。

另存研究标签：载体（显式文本/结构化、参数、潜在状态）、功能（事实、经验、工作记忆）、操作（形成、演化、检索）。灵感来自 [Agent Memory Survey 项目](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)，不是简单套用其全部定义。

排除纯内存分配/缓存优化、泛化聊天 UI、未体现记忆机制的普通 RAG、SEO 空壳、重复镜像和没有独立贡献的 fork。通用数据库/Agent 框架仅在有明确 memory 模块证据时进入相关基础设施视图，不能用整个框架的总 Star 代表子模块热度。静态 AGENTS/提示词模板可作背景材料；可持久保存并回用经验的实现可进入工程视图。闭源服务与许可证不明代码明确标注，不写成已确认开源。

## 发现与入池

同时使用已知项目 seed、GitHub repository search/topic、官方 Trending（辅助）、可靠的综述/Awesome List 新链接及上游 release/文档关联。新建搜索与近期活动搜索并行，不只搜索最近创建的仓库。

搜索词组分开执行，避免一个巨大 OR 查询：`agent memory`、`long-term memory`、`episodic memory`、`agentic memory`、`coding agent memory`、`memory consolidation`、`memory benchmark`、`记忆 智能体`。使用 [GitHub 官方 repository qualifiers](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories) 的 `in:name,description,readme`、`topic:`、`created:`、`pushed:` 等，具体查询保存到配置与每轮日志。不要把 GitHub Search、Code Search 的语法混用。

发现查询同时保留有 Star 门槛的高信号通道和无 Star 门槛的新项目通道。候选入池不设全局最低 Star；正式收录至少需要明确相关性证据、可识别实现或评测资产、可靠来源链接。工程可用性未知时标注未知，不为凑数量自动判定可用。

记录：GitHub created_at、首次被本项目发现时间、可证实的首次公开日期（未知为 null）、当前状态和入选/排除理由。仓库很早创建、后来公开，不能仅凭 created_at 断言它不是新发布项目。

每轮保存查询、检索时间、排序方式、分页范围、返回/检查/入选数量、截断/错误标记。搜索结果不是全量 GitHub 普查；搜索条数不能直接当作整个方向的新建仓库数量。[GitHub Search API](https://docs.github.com/en/rest/search/search) 有结果和执行限制，必须检查 incomplete_results 和分页状态。

## 三个独立视图

1. 新发现：展示首次发现日期、仓库年龄、实际机制与为什么入选；不要求已经热门。
2. 关注度变化：按可比较窗口的 Star 净变化排列，并列时用稳定仓库标识排序；同时展示基数和增长率。不产生“技术质量分”。
3. 实质进展：已发布功能/破坏性变更、记忆算法改变、新宿主集成、许可证变化、公开安全通告、上游基准更新。已合并未发布、仍在 PR 中、仅作者声称分别标注。

Benchmark 与工程库不混在一个 Star 总榜。成熟参考项目与新项目可分组，不让绝对量吞没小项目，也不让小基数百分比主导判断。

## 数值口径

快照至少记录 `repository_id`、`full_name`、`observed_at`、来源 URL、stars、forks、archived、default_branch、HEAD SHA；release 数据单独记录实际发布时间。API 取不到的字段为 null，并记录 error/stale 状态，不能从搜索摘要补造精确计数。

设两次成功观测为 (t0,S0)、(t1,S1)：

- `star_delta = S1 - S0`：净变化，可为负。
- `stars_per_day = (S1 - S0) / ((t1-t0)/86400)`：按实际秒数换算，不默认任务准时。
- `relative_growth = (S1-S0)/S0`，仅在 S0>0 时定义，同时展示基数；S0=0 时为 null。
- 7/30 日视图必须有真实的相应历史基线。拟按最接近目标时刻、偏差不超过 6 小时的成功观测比较，并展示实际窗口；否则为 null，不用半日数据外推一周。
- 初期只有基线，不发布“过去 7 天增长”或加速度排行。第三方历史数据仅在来源/定义可核实且与快照明确分开时作为补充。

候选热度提醒建议：24 小时净增至少 100；或 7 日净增至少 100 且相对增长至少 20%。这些只是筛查提示，不自动认定技术突破，也不据此指控刷 Star。仅关注度异常而无技术变化默认进入榜单/周报，不独立推送重要技术通知。

Release、merged PR、issue 事件优先保存 ID 和链接。Issue 数不是问题严重程度，贡献者总数不是活跃贡献者数，最近 pushed 时间不是代码质量。跨项目评测必须核对数据集版本、模型、配置和评价协议；否则只记录作者报告，禁止直接横排性能数字。

## 证据等级和项目卡片

每项重要结论保存 `claim`、`source_url`、`source_version_or_sha`、`event_at`、`observed_at`、`evidence_level`。等级为：`upstream_statement`（作者说明）、`code_inspected`（检查了对应实现）、`independently_reproduced`（本仓库实际独立运行，必须有实验记录）。初期不执行上游项目，因此不得出现无实验记录的 independently_reproduced。

卡片回答：解决什么问题；在哪里、以何种表示保存记忆；何时写入/检索/更新/遗忘；与哪些 Agent 接入；本地部署和外部服务依赖；许可证；有何测试或基准证据；本次实际变化；已知局限。稳定事实尽量链接固定 commit；已发布版本与 default branch 进度分别记录。

## 趋势而非单项目炒作

周报先在同一组已跟踪仓库上比较，再说明本周新增/移出样本造成的样本变化。至少有多个独立项目的明确证据才讨论共同方向；否则写“单项目观察”。不从少量搜索命中推导整个开源生态占比。所有覆盖率和缺失项公开，暂不使用不透明的加权 TrendScore。
