# Agent Memory 技术追踪 · 2026-09-17

本轮是首次实际定时维护。完成 14 个登记项目（13 个正式跟踪 + 1 个历史参照）的 metadata、默认分支 HEAD 与当前 Release 水位采集，并在代码差异层面复核 3 个发生 HEAD 变化的项目。7/30 日增长仍无足够历史窗口，不做外推。

## 本轮重要变化

**Hindsight 的 Coding Agent 注入从单一 autoReflect 扩展为可选择的数据源。** [提交 `9ef0d901`](https://github.com/vectorize-io/hindsight/commit/9ef0d901cbb5085e4fc4b54e3b1116a778eb2292) 新增 `autoInject`，首轮提示可在 `reflect`、`pages`、`recall` 或关闭之间选择，并统一 recall options。这直接改变了 Coding Agent 启动时如何从长期记忆获取上下文。

**插件安装路径补齐 companion skill。** [提交 `d73c517b`](https://github.com/vectorize-io/hindsight/commit/d73c517b42358e167eb20f797f1f084d288e5b52) 修复通过宿主自身 plugin manager 安装时插件工具已加载但 skill 缺失的问题；OpenCode v2 则改为通过宿主 skill transform 在内存注册。该变化降低“插件装上了但记忆使用说明没有生效”的宿主差异。

**Memory bank 可迁移范围显著扩大。** [提交 `6e6098a0`](https://github.com/vectorize-io/hindsight/commit/6e6098a03426b49446cd3a344242988e526f54aa) 统一 bank export/import API，可选择 memories/data、bank config 和 history，并修复同实例复制时 directives/webhooks 因 ID 冲突被静默跳过的问题。对长期 Agent 的迁移、备份和环境复制更直接相关。

**Reflect 的 Anthropic 长输出截断得到修复。** [提交 `4f1b0629`](https://github.com/vectorize-io/hindsight/commit/4f1b06293453c966752102464442352769b756db) 把未显式限额时的 fallback 从 4096 调到 64000，并向工具调用循环传递 reflect completion 配置；上游提交说明此前可能在 `done` payload 完成前被截断。这里只确认了代码差异，没有运行时复现。

## 正式跟踪扩展

本轮按候选审查预算新增 5 个项目，而不是直接按搜索结果凑到 20：

- [TencentDB-Agent-Memory](../projects/tencentcloud--tencentdb-agent-memory.md)：团队级 Chat Memory / Skill / Wiki / CodeGraph 资产中枢，明确覆盖多种 Coding Agent 与本地部署。
- [General Agentic Memory](../projects/vectorspacelab--general-agentic-memory.md)：研究型分层文件系统记忆，覆盖长文本、视频和 Agent trajectory。
- [A-MEM](../projects/agiresearch--a-mem.md)：Zettelkasten 风格动态记忆链接与演化研究实现。
- [Memobase](../projects/memodb-io--memobase.md)：用户画像 + 事件时间线的长期记忆工程系统，可自托管。
- [Neo4j Agent Memory](../projects/neo4j-labs--agent-memory.md)：短期会话、长期图事实和 reasoning trace 三层图记忆，含 MCP/自托管路线。

因此正式跟踪从 8 增至 13，另保留 1 个历史参照。候选队列在移除已收录项目并加入本轮搜索线索后为 16 个。

## 其他 HEAD 变化

Mem0 从上一水位到当前 HEAD 仅发现文档变化，没有生成技术事件。MemOS 的 7 个新增提交主要落在按模型 QPS 的分布式 LLM 限流、Redis GCRA、配置与测试；它属于运行基础设施可靠性，本轮更新项目卡片但没有把它包装成新的记忆算法。

## 证据边界

本轮没有执行任何被追踪项目的代码，也没有复现上游 benchmark。Hindsight 的四项变化为 commit/diff 级 `code_inspected`；新收录项目的机制分类仍为 `upstream_statement`。Release 扫描确认了当前水位，但首次纳入项目没有回灌全部旧发布历史，旧 Release 不能冒充本轮新事件。
