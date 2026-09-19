# Agent Memory 技术追踪 · 2026-09-20

本轮完成 21 个登记项目（20 个正式跟踪 + 1 个历史参照）的 metadata、默认分支 HEAD 与当前 Release 水位采集，三类来源均为 21/21。9 个项目的默认分支 HEAD 相比上次成功检查发生变化；按单轮预算深度检查了 5 个项目。监测历史仍不足可比较的 7 日窗口，因此不生成 7/30 日增长结论。

## 重要变化

**Hindsight 把 Coding Agent 的长期记忆入口从“先深度 reflect”进一步调整为“先检索 curated knowledge pages，再按需 reflect”。** 当前 [`knowledge-injection.ts`](https://github.com/vectorize-io/hindsight/blob/0a58d695adee239c8990ef30eacf66ebca54094f/hindsight-integrations/coding-agents/src/core/knowledge-injection.ts) 明确把新目标、bug、测试、新实现、解释历史决策和提交前检查列为先搜索 knowledge pages 的触发点；只有页面信息不够深时才调用 `hindsight_reflect`。这是代码级 `code_inspected`，未运行上游项目。

**OpenViking 增加可执行任务导向的 Experience Memory skill。** [`ov-experience-memory`](https://github.com/volcengine/OpenViking/blob/4bccb1294c013e1485c72377afcbba5ffc435cc7/agent-plugins/skills/ov-experience-memory/SKILL.md) 要求 Agent 在 coding、配置、部署、工作流执行和失败恢复等场景中，按需搜索当前用户 Experience root 并读取少量相关经验；同时明确 Experience 只是建议性过程知识，不能覆盖当前请求、权限和实时工具证据。这是代码级 `code_inspected`。

**TencentDB-Agent-Memory v2.0.2-beta.2 扩展本地存储路线并修复记忆链路问题。** [Release](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.2-beta.2) 声明新增可选 MongoDB 后端/本地开源部署路径，并包含 memory recall fallback、解析/历史重复及观测能力相关改进。该结论为 `upstream_statement`。

**Cognee v1.6.0 继续强化本地模型和数据集隔离。** [Release](https://github.com/topoteretes/cognee/releases/tag/v1.6.0) 声明支持 keyless/local-model workflow、按 dataset 限定 recall 以降低跨数据集泄漏、保存每个 dataset 的 embedding model，并改进 MCP 和失败处理。该结论为 `upstream_statement`。

**Letta Code v0.32.13 主要是 Coding Agent 运行可靠性与本地分发改进。** [Release](https://github.com/letta-ai/letta-code/releases/tag/v0.32.13) 声明修复 subagent process-tree、gateway lifecycle 和 local memory-filesystem sync，并新增 self-contained Python wheel；这属于 Agent harness / 本地部署层变化，而不是新的记忆算法。该结论为 `upstream_statement`。

## 发现与覆盖

本轮实际轮换关键词为 `"memory consolidation"`。普通发现通道执行 2 页，每页 20 条；第 2 页仍满，因此只记录为非穷尽。新建且无 Star 门槛通道使用 `created:>=2026-08-20`，第 1 页 20 条、第 2 页 2 条，在本轮页预算内结束。GitHub connector 未暴露 `total_count/incomplete_results`，对应字段保持 unknown/null。正式跟踪已达到 20 个目标，本轮没有为了扩大数字而强行收录候选。

9 个 changed HEAD 中，本轮深度检查 5 个：mem0、letta-code、Hindsight、TencentDB-Agent-Memory、OpenViking。Graphiti、claude-mem、Neo4j Agent Memory 与 Cognee 的 HEAD 变化保留为后续 change-review backlog；Cognee 本轮只依据正式 Release 形成对外结论。

## 证据边界

本轮没有执行任何被跟踪项目代码，也没有复现上游 benchmark。仅执行本仓库 tracker 的 25 个 synthetic unit tests 与 prepare/validate。Release 历史继续采用 forward watermark / 增量分页语义；首次看到的旧发布不会作为新事件。当前观察历史尚不足 7 天，Star 增长列继续保持“—”。
