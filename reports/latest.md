# Agent Memory 技术追踪 · 2026-09-18

本轮完成 21 个登记项目（20 个正式跟踪 + 1 个历史参照）的 metadata、默认分支 HEAD 与当前 Release 水位采集。既有项目中只有 Hindsight 默认分支 HEAD 发生变化；对 2 个新增提交做了 commit/diff 级检查。监测历史仍不足 7 天，不生成 7/30 日增长结论。

## 重要变化

**Hindsight 让 reflect 的 disposition 参数从“裸数值”变成带语义的行为指令。** [`475cc02`](https://github.com/vectorize-io/hindsight/commit/475cc0278cdc638240d58e1cc816d8cb31ec4ff4) 在 tools prompt 中解释 disposition level 的含义，并增加测试；目标是避免模型把 `skepticism=5`、`literalism=3` 等仅当作 metadata，而不影响生成行为。

**Hindsight 重写 bank 列表的 fact-count 路径，避免分页前扫描整个 memory_units。** [`81e4a67`](https://github.com/vectorize-io/hindsight/commit/81e4a674a96e0b9687712746295fd9f451a6b600) 先确定返回页，再只对页内 bank 进行 SQL count。上游提交报告在 365 banks / 1.8M memory units / 11k documents / 543 MB 数据上主列表查询从 131 ms 降到 6 ms，50-bank 页增加约 44 ms 的 index-only count；这些数字是上游测量，本仓库没有复现。

## 正式跟踪扩展

本轮在读过上游 README、metadata、HEAD、公开实现位置和 Release 水位后新增 5 个项目，正式跟踪达到初始目标 20 个：

- [Redis Agent Memory](../projects/redis--agent-memory-server.md)：session/long-term memory 工程；仓库保留 V0 开源研究实现。
- [Cognee](../projects/topoteretes--cognee.md)：自托管知识图谱/向量长期记忆，并提供 Claude Code、Codex 与 MCP 接入。
- [MemRL](../projects/memtensor--memrl.md)：运行时强化学习更新 episodic memory 的研究代码。
- [Episodic Memory](../projects/obra--episodic-memory.md)：本地索引多种 Coding Agent 会话并提供跨会话语义检索。
- [agent-memory](../projects/tigerless-labs--agent-memory.md)：Markdown 事实源 + 可重建本地索引 + sleep-time Manage 的 Coding Agent 长期记忆运行时。

候选队列移除上述 5 个后，又从两条非穷尽搜索第一页加入 9 个未审查线索，目前保留 20 个候选；它们不等于推荐。

## 证据边界

本轮没有执行任何被跟踪项目代码，也没有复现上游 benchmark。Hindsight 两项变化为 commit/diff 级 `code_inspected`；5 个新收录项目机制为 `upstream_statement`。新收录项目首次看到的旧 Release 只作为 forward watermark，不作为本轮新事件。两条 discovery 查询都只有第一页，GitHub connector 未暴露 total_count/incomplete_results，因此不能声称生态搜索完整。
