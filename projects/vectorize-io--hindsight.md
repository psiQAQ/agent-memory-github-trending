# vectorize-io/hindsight

通过 retain、recall、reflect 接口保存、查询和使用 Agent 记忆。

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责启动上下文注入、知识页和宿主适配。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `326ad524f5999d6b90520e358f17c657d1c429f5` |
| HEAD 观察（UTC） | 2026-10-26T16:12:32.531Z |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | 固定版本实现为 code_inspected；最近 Release 为 upstream_statement；未运行上游代码 |

## 已检查的实现证据

- [`knowledge-injection.ts@0a58d69`](https://github.com/vectorize-io/hindsight/blob/0a58d695adee239c8990ef30eacf66ebca54094f/hindsight-integrations/coding-agents/src/core/knowledge-injection.ts)：Coding Agent 对“新目标、bug、测试、新实现、解释 why、提交前检查”等场景改为先搜索 curated knowledge pages，再读取命中的页面；只有页面深度不足时才退到 `hindsight_reflect`。实现还刻意不把完整页面标题/ID roster 直接塞入上下文，避免 Agent 绕过检索而只按标题选择页面。
- 对应固定版本与其前次记录相比共新增 37 个提交；该版本 diff 还显示 time-window filter、Cursor LLM provider、fact extraction、coding-agent system eval 与 Hermes integration 等变化。这里没有把所有改动都作为独立技术事件，避免把大范围工程变化等同于已验证的记忆机制变化。

## 既有代码级变化

- [`475cc02`](https://github.com/vectorize-io/hindsight/commit/475cc0278cdc638240d58e1cc816d8cb31ec4ff4)：reflect tools prompt 为 disposition level 增加语义说明和兼容性测试。
- [`81e4a67`](https://github.com/vectorize-io/hindsight/commit/81e4a674a96e0b9687712746295fd9f451a6b600)：bank 列表先分页再只对页内 bank 做 fact count，避免分页前聚合整个 `memory_units` 表；上游性能数据未由本仓库复现。

## 证据边界

[已检查实现版本](https://github.com/vectorize-io/hindsight/tree/0a58d695adee239c8990ef30eacf66ebca54094f)。上述实现结论来自所链接的固定 commit/diff 与实现文件；本次 Release 观察见下节，未进行运行时复现。

## 最近核实的发布

v1.0.0 修复 Coding Agent 的会话留存与记忆注入、Windows hook 和进程启动，并拒绝 tag-scoped 调用方访问整 bank 操作；OpenClaw 移除旧 agent-sdk 和 agent_knowledge_* 工具，加入原生 memory provider。

版本号 1.0.0 本身不代表性能提升；以上为 Release 声明，相关迁移和运行结果未独立验证。

[v1.0.0 官方 Release](https://github.com/vectorize-io/hindsight/releases/tag/v1.0.0)；发布（UTC）：2026-10-13T14:08:48Z；观察（UTC）：2026-10-15T04:56:27Z；此段证据等级：`upstream_statement`。

## 最近检查的实现与发布状态

re-retain 与 tags PATCH 使用解析后的 scope 集合判断是否失效；shared 或不依赖标签的显式 scope 下，标签变化保留既有 observations，避免无意义的整文档重新 consolidation。该改动已合并，但本轮最新正式 Release 仍为 v1.0.0，尚未包含这次 10 月 15 日的提交。

状态：`merged_unreleased`。[PR #5596](https://github.com/vectorize-io/hindsight/pull/5596)，合并 commit `e9f456df857c6185efac9a8b7a0f733a9dab8b5d`；事件（UTC）2026-10-15T08:27:16Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/vectorize-io/hindsight/blob/e9f456df857c6185efac9a8b7a0f733a9dab8b5d/hindsight-api-slim/hindsight_api/engine/consolidation/consolidator.py) · [实现 2](https://github.com/vectorize-io/hindsight/blob/e9f456df857c6185efac9a8b7a0f733a9dab8b5d/hindsight-api-slim/hindsight_api/engine/memories/pg/retain.py)

Release 增量已覆盖到上次成功采集位置；这不代表全部历史发布已收集，也不代表已独立验证上游测试。

## 2026-10-16：Decision-model recall 重排序（仅静态检查）

默认分支 [`466c2b6`](https://github.com/vectorize-io/hindsight/tree/466c2b6c8d39f440e77589b259f26bd66c95702b) 新增 [`DecisionModelReranker`](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/engine/search/decision_reranker.py)，借助决策模型处理 recall 候选排序；[配置](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/config.py)中 `DEFAULT_DECISION_MODEL_PROVIDER = "none"`，不是默认启用。状态：已进入默认分支，尚未核实进入正式 Release；证据 `code_inspected`，未执行测试、未比较检索质量、费用或延迟。

## 2026-10-20 Document History：变更链条

- 默认分支代码引入按文档追踪 retain/append、事实编辑/失效、observation 更新等操作的 `DocumentEvent`，写入异步 operation 的 `result_metadata.document_events`，不另建永久事件表。
- 观察对象的 ID 示例每个事件最多保留 `MAX_IDS=100`，计数单独保存；历史依赖操作日志保留期，未走异步操作的同步流程不保证收录。
- 来源：[固定 HEAD 的实现](https://github.com/vectorize-io/hindsight/blob/c5f585f8f8568ed0677eb2e70fe830c4c483e2a2/hindsight-api-slim/hindsight_api/engine/document_history.py)；状态：`merged_unreleased`（默认分支可见，未证实进入正式 Release）；证据等级 `code_inspected`，未复现实效或审计完整性，事件时间未核实。

## 2026-10-25：Google ADK 集成依赖维护

[PR #6066](https://github.com/vectorize-io/hindsight/pull/6066) 已合并（UTC 2026-10-24T14:21:06Z）。固定配置覆盖 opentelemetry-api/sdk >=1.45.1，锁定版本从1.41.1升级至1.45.1；google-adk 按 Python 版本为2.13.0或2.11.0。上游说明与 tracestate 解析问题有关，未独立复现漏洞、作者测试或兼容性。

重要范围：override 只影响该集成自己的锁文件／开发环境，不进入发布 wheel 元数据。pip 安装者须核对实际依赖解析，不能把此修改视作所有部署已修复。

状态：主分支已合入，未进入本轮观测最新 Release v1.1.0。证据：[固定配置](https://github.com/vectorize-io/hindsight/blob/4822d66e093dadfd6b2b80186fd0395ef80926ca/hindsight-integrations/google-adk/pyproject.toml)、[锁文件](https://github.com/vectorize-io/hindsight/blob/4822d66e093dadfd6b2b80186fd0395ef80926ca/hindsight-integrations/google-adk/uv.lock)、[v1.1.0 对照](https://github.com/vectorize-io/hindsight/compare/v1.1.0...4822d66e093dadfd6b2b80186fd0395ef80926ca)。选定配置与锁版本为 code_inspected；安全影响为 upstream_statement；未执行上游。

本轮观察 UTC：2026-10-25T06:03:19.016Z；本轮 Release 增量已覆盖旧成功水位，不表示穷尽历史。

## 2026-10-26：集成依赖与开发锁文件范围

12项依赖维护提交进入主分支。选定检查[LiteLLM配置](https://github.com/vectorize-io/hindsight/blob/fa359876bcf5ed652c001dac5d40bfcc51d1d41d/hindsight-integrations/litellm/pyproject.toml)、[Flowise配置](https://github.com/vectorize-io/hindsight/blob/fa359876bcf5ed652c001dac5d40bfcc51d1d41d/hindsight-integrations/flowise/package.json)与对应diff，逐blob匹配固定tree。

[PR6087](https://github.com/vectorize-io/hindsight/pull/6087)合并UTC2026-10-25T14:40:54Z；作者说明filelock从3.29.0升至4.2.4，已检查开发锁文件patch。uv开发环境限定Python≥3.11，发布元数据的requires-python≥3.10与filelock≥3.20.3未变。不能从开发锁文件推导pip部署已修复；漏洞影响和作者测试未复现。Flowise manifest的Zod依赖从^3.23.0变^4.6.7，使用者需检查兼容性。

状态：已合并，未进入本轮观测最新GitHub Release v1.1.0；[对照](https://github.com/vectorize-io/hindsight/compare/v1.1.0...fa359876bcf5ed652c001dac5d40bfcc51d1d41d)包含选定提交，包注册表未查。code_inspected仅限选定配置/锁patch，不代表全部12项审计或运行时效果。观察UTC 2026-10-25T16:21:15.560Z。

## 2026-10-27：缓冲 retain session 不提前登记文档完成

仅在 retain_session 为 None 时保留原分批检查点；使用缓冲 session 时不在 commit 前登记完成，重试重新抽取。SQL 原地分批写入路径保持检查点；上游描述的回归测试未由本仓库运行。修复在 v1.1.0 之后。

状态：`merged_unreleased`；证据等级 `code_inspected`。这是选定实现和一手发布材料的检查，未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/vectorize-io/hindsight/pull/6100)；来源版本 `1da5f03241de742aaf37f78399061636077d2aad`。
- 事件 UTC 2026-10-26T09:56:57Z；观察 UTC 2026-10-26T16:15:40.848Z。
- 已读范围：`hindsight-api-slim/hindsight_api/engine/retain/orchestrator.py`、`PR6100 merged state and reported test scope`。
- 记录的默认分支 HEAD：`326ad524f5999d6b90520e358f17c657d1c429f5`，采样 UTC 2026-10-26T16:12:32.531Z；不是实时最新版本，也不表示其他提交已经逐项审查。

</details>
