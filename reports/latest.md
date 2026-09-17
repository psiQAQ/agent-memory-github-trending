# Agent Memory 技术追踪 · 2026-09-18

本轮完成 16 个登记项目（15 个正式跟踪 + 1 个历史参照）的 metadata、默认分支 HEAD 与当前 Release 水位采集。6 个既有项目 HEAD 发生变化；深度代码复核聚焦于存在实质 Agent Memory / Coding Agent 变化的 Hindsight 与 Letta Code，其余 4 个变化区间为文档、签名或非实质内容。监测历史仍不足 7 天，不生成 7/30 日增长结论。

## 重要变化

**Hindsight 把多 Agent bank 拓扑从“全部共享/全部隔离”扩展为可显式分组。** [`a2d95f9`](https://github.com/vectorize-io/hindsight/commit/a2d95f9efe99c7976c7bbab610a831f1bfb2cd0f) 新增 `agentBankMap`，允许指定 Agent 共享一个命名 memory bank，未映射 Agent 继续使用原动态推导；retain、recall 与 knowledge tools 统一走该映射。

**Memory bank 可以在服务端单调用克隆。** [`a71b062`](https://github.com/vectorize-io/hindsight/commit/a71b06245a7fb0f34fcaa8cf09ae0e56996f759a) 新增异步 clone API，在同一进程连续完成 export/import，不经客户端传输 archive；源 bank 使用单事务读取，副本创建后独立演化。可选择继承 data、bank config 和 history。

**Coding Agent 的知识页从固定 taxonomy 变为可配置/可扩展。** [`dd80672`](https://github.com/vectorize-io/hindsight/commit/dd80672bea2cc403ed08a84f4286c93c1248166b) 新增 `pages` 和 `customPages`，可禁用或改写内置知识页，也可创建自定义页面；配置文件成为页面 query 的持久 source of truth。

**后台 mental-model refresh 可以与交互 reflect 分离模型预算。** [`311a2d4`](https://github.com/vectorize-io/hindsight/commit/311a2d495db6d81c76c8dfdd7b94fe7dc6bb31bc) 新增独立 `MENTAL_MODEL_REFRESH_LLM_*` 配置与并发桶，未配置时保持向 reflect 配置回退。该设计直接针对单 GPU 自托管中后台刷新与交互推理争用资源的问题。

**Letta Code 发布 v0.32.12，并继续补强 subagent 生命周期。** [v0.32.12](https://github.com/letta-ai/letta-code/releases/tag/v0.32.12) 新增/修复包括 Desktop credentials 向 subagent 传递、Cloud 部署中断恢复等；随后 [`41f2e7a`](https://github.com/letta-ai/letta-code/commit/41f2e7abc7ca06be7413db5e6cbfe273ec2fcab3) 把停止操作扩展为清理完整子进程树，避免 launcher 退出后 descendant 残留。

## 正式跟踪扩展

新增 2 个项目，均在读过上游 README、metadata、HEAD 与 Release 水位后收录，而非按 Star 自动入池：

- [OpenViking](../projects/volcengine--openviking.md)：context database / coding-agent integration，统一资源、记忆与技能，支持 session memory extraction。
- [Agent Memory Benchmark](../projects/vectorize-io--agent-memory-benchmark.md)：补充 benchmark 覆盖，公开评测 harness，并把准确率与速度/token 成本分开记录。

正式跟踪由 13 增至 15，另保留 1 个历史参照；候选队列保持 16 个（移除 OpenViking，同时加入本轮新发现但尚未审查的 A-mem-sys）。

## 证据边界

本轮没有执行任何被跟踪项目代码，也没有复现上游 benchmark。Hindsight 与 Letta Code 的上述代码变化为 commit/diff 级 `code_inspected`；OpenViking 与 Agent Memory Benchmark 的项目机制仍为 `upstream_statement`。Letta Code 的 Release 分页读取到上一水位 v0.32.11 后才视为本轮 Release 区间完整；新收录项目的旧 Release 仅作为基线。两条发现查询仅取得第一页，GitHub connector 未暴露 total_count/incomplete_results，因此不能声称生态搜索完整。
