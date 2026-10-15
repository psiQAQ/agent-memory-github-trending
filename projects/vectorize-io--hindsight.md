# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `e9f456df857c6185efac9a8b7a0f733a9dab8b5d` |
| HEAD 观察（UTC） | 2026-10-15T08:46:16Z |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | 固定版本实现为 code_inspected；最近 Release 为 upstream_statement；未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责启动上下文注入、知识页和宿主适配。

## 已检查的实现证据

- [`knowledge-injection.ts@0a58d69`](https://github.com/vectorize-io/hindsight/blob/0a58d695adee239c8990ef30eacf66ebca54094f/hindsight-integrations/coding-agents/src/core/knowledge-injection.ts)：Coding Agent 对“新目标、bug、测试、新实现、解释 why、提交前检查”等场景改为先搜索 curated knowledge pages，再读取命中的页面；只有页面深度不足时才退到 `hindsight_reflect`。实现还刻意不把完整页面标题/ID roster 直接塞入上下文，避免 Agent 绕过检索而只按标题选择页面。
- 对应固定版本与其前次记录相比共新增 37 个提交；该版本 diff 还显示 time-window filter、Cursor LLM provider、fact extraction、coding-agent system eval 与 Hermes integration 等变化。这里没有把所有改动都作为独立技术事件，避免把大范围工程变化等同于已验证的记忆机制变化。

## 既有代码级变化

- [`475cc02`](https://github.com/vectorize-io/hindsight/commit/475cc0278cdc638240d58e1cc816d8cb31ec4ff4)：reflect tools prompt 为 disposition level 增加语义说明和兼容性测试。
- [`81e4a67`](https://github.com/vectorize-io/hindsight/commit/81e4a674a96e0b9687712746295fd9f451a6b600)：bank 列表先分页再只对页内 bank 做 fact count，避免分页前聚合整个 `memory_units` 表；上游性能数据未由本仓库复现。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成。

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

Release 增量已覆盖到上次成功水位；不代表穷尽历史发布或独立验收上游测试。

## 2026-10-16：Decision-model recall 重排序（仅静态检查）

默认分支 [`466c2b6`](https://github.com/vectorize-io/hindsight/tree/466c2b6c8d39f440e77589b259f26bd66c95702b) 新增 [`DecisionModelReranker`](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/engine/search/decision_reranker.py)，借助决策模型处理 recall 候选排序；[配置](https://github.com/vectorize-io/hindsight/blob/466c2b6c8d39f440e77589b259f26bd66c95702b/hindsight-api-slim/hindsight_api/config.py)中 `DEFAULT_DECISION_MODEL_PROVIDER = "none"`，不是默认启用。状态：已进入默认分支，尚未核实进入正式 Release；证据 `code_inspected`，未执行测试、未比较检索质量、费用或延迟。
