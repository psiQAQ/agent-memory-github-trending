# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `0a58d695adee239c8990ef30eacf66ebca54094f` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | code_inspected；检查提交/diff 与当前实现文件，未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责启动上下文注入、知识页和宿主适配。

## 本轮代码级变化

- [`knowledge-injection.ts@0a58d69`](https://github.com/vectorize-io/hindsight/blob/0a58d695adee239c8990ef30eacf66ebca54094f/hindsight-integrations/coding-agents/src/core/knowledge-injection.ts)：Coding Agent 对“新目标、bug、测试、新实现、解释 why、提交前检查”等场景改为先搜索 curated knowledge pages，再读取命中的页面；只有页面深度不足时才退到 `hindsight_reflect`。实现还刻意不把完整页面标题/ID roster 直接塞入上下文，避免 Agent 绕过检索而只按标题选择页面。
- 与上轮 HEAD 相比共新增 37 个提交；本轮 diff 还显示 time-window filter、Cursor LLM provider、fact extraction、coding-agent system eval 与 Hermes integration 等变化。这里没有把所有改动都作为独立技术事件，避免把大范围工程变化等同于已验证的记忆机制变化。

## 既有代码级变化

- [`475cc02`](https://github.com/vectorize-io/hindsight/commit/475cc0278cdc638240d58e1cc816d8cb31ec4ff4)：reflect tools prompt 为 disposition level 增加语义说明和兼容性测试。
- [`81e4a67`](https://github.com/vectorize-io/hindsight/commit/81e4a674a96e0b9687712746295fd9f451a6b600)：bank 列表先分页再只对页内 bank 做 fact count，避免分页前聚合整个 `memory_units` 表；上游性能数据未由本仓库复现。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成。

## 证据边界

[当前代码版本](https://github.com/vectorize-io/hindsight/tree/0a58d695adee239c8990ef30eacf66ebca54094f)。本轮结论来自 commit/diff 与指定实现文件检查，不是运行时复现；当前 Release 水位仍为 v0.10.0。
