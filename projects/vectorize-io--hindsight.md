# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `a6352534730659c137d734ebfecce1a558bfdbfc` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | code_inspected；检查提交/diff，未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责启动上下文注入、知识页和宿主适配。

## 本轮代码级变化

- [`a2d95f9`](https://github.com/vectorize-io/hindsight/commit/a2d95f9efe99c7976c7bbab610a831f1bfb2cd0f)：OpenClaw 新增 `agentBankMap`，可让指定 Agent 共享命名 bank，同时让其他 Agent 保持动态隔离；retain、recall 和 knowledge tools 走同一路由。
- [`a71b062`](https://github.com/vectorize-io/hindsight/commit/a71b06245a7fb0f34fcaa8cf09ae0e56996f759a)：新增单调用 bank clone；同一后台操作完成 export/import，源 bank 单事务读取，副本创建后独立演化。
- [`dd80672`](https://github.com/vectorize-io/hindsight/commit/dd80672bea2cc403ed08a84f4286c93c1248166b)：Coding Agent 的知识页支持 `pages` / `customPages`，可以关闭、重写内置页面查询或创建自定义页面，配置成为持久 source of truth。
- [`311a2d4`](https://github.com/vectorize-io/hindsight/commit/311a2d495db6d81c76c8dfdd7b94fe7dc6bb31bc)：automatic mental-model refresh 可使用独立 LLM 配置和并发桶；未配置时保持向 reflect LLM 回退。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成。独立 mental-model-refresh LLM 的变化尤其面向单 GPU 自托管时交互推理与后台刷新争用资源的场景。

## 证据边界

[当前代码版本](https://github.com/vectorize-io/hindsight/tree/a6352534730659c137d734ebfecce1a558bfdbfc)。本轮结论来自 commit/diff 检查，不是运行时复现；没有执行上游服务或 benchmark。当前 Release 水位仍为 v0.10.0，本轮变化来自默认分支提交。
