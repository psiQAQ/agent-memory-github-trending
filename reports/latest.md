# 最新研究简报

数据批次：`20261014T160956Z-scheduled`，原始观测完成于 2026-10-14T16:09:56Z（北京时间 2026-10-15 00:09:56）。
2026-10-15 进行交互式恢复发布；下列五份 Release 在恢复阶段重新读取。发布日、来源观察日和原始计数时间分别保留。

## 已核实的发布变化

### thedotmack/claude-mem v13.39.0

v13.39.0 修复 Codex 子代理在线程压缩后丢失记忆时间线：PostCompact 按 session_id/agent_id 标记线程，下一次 PostToolUse 恢复一次 timeline；SessionStart 清理标记以免根线程重复注入。

该结论来自正式 Release 说明；未检查本版本实现，也未验证各宿主实际行为。

来源：[官方 Release](https://github.com/thedotmack/claude-mem/releases/tag/v13.39.0)；发布（UTC）：2026-10-13T21:31:41Z；重新观察（UTC）：2026-10-15T04:56:26Z；证据等级：`upstream_statement`。

### vectorize-io/hindsight v1.0.0

v1.0.0 修复 Coding Agent 的会话留存与记忆注入、Windows hook 和进程启动，并拒绝 tag-scoped 调用方访问整 bank 操作；OpenClaw 移除旧 agent-sdk 和 agent_knowledge_* 工具，加入原生 memory provider。

版本号 1.0.0 本身不代表性能提升；以上为 Release 声明，相关迁移和运行结果未独立验证。

来源：[官方 Release](https://github.com/vectorize-io/hindsight/releases/tag/v1.0.0)；发布（UTC）：2026-10-13T14:08:48Z；重新观察（UTC）：2026-10-15T04:56:27Z；证据等级：`upstream_statement`。

### volcengine/OpenViking v0.5.0

v0.5.0 发布 Gateway Beta，通过模型协议代理检索并注入记忆，保存对话以供后续抽取；Working Memory 默认关闭，仍保留原始消息归档与长期记忆抽取。宿主插件需要单独升级，显式开启旧策略的部署也需核对升级后的实际配置。

Gateway、服务端与宿主插件是不同部署环节；本仓库未安装或运行。该版本的 Working Memory 默认值及兼容性说明来自正式 Release。

来源：[官方 Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.0)；发布（UTC）：2026-10-09T15:46:55Z；重新观察（UTC）：2026-10-15T04:56:27Z；证据等级：`upstream_statement`。

### letta-ai/letta-code v0.34.14

v0.34.14 改进本地 transcript 的有界恢复和流式 JSONL 读取，遵守 memfs:false；同时修复子进程 OOM 误结束父子代理以及 Cloud 子代理 sandbox 选择。

上游还声明调整 Claude Code/Codex 子代理的权限运行方式；该行为需要部署者核对，本仓库未验证其隔离或权限效果。这里只记录 Release 声明。

来源：[官方 Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.14)；发布（UTC）：2026-10-14T04:52:03Z；重新观察（UTC）：2026-10-15T04:56:26Z；证据等级：`upstream_statement`。

### TencentCloud/TencentDB-Agent-Memory v2.0.3-beta.1

v2.0.3-beta.1 新增可替换的决策服务，集中处理 Skill 选择与 Memory L3 更新判定，并加入按需加载 Skill 和 Proxy 会话轨迹记录；这些新能力默认关闭。

按 beta 标签记录该版本，不据 GitHub 的 prerelease=false 推断稳定性；未运行 Proxy、决策服务或 MemoryCore。

来源：[官方 Release](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.3-beta.1)；发布（UTC）：2026-10-13T10:43:52Z；重新观察（UTC）：2026-10-15T04:56:27Z；证据等级：`upstream_statement`。

## 发现与覆盖

Metadata、默认分支 HEAD、Release 当前页均为 21/21；Release 增量分页完整为 17/21。四个未完成来源保留旧成功游标，不能据当前页推断其余发布历史。

与上一已发布快照相比，11 个 HEAD 变化；本次只核对上述五个项目的 Release 说明，其余相关 PR、文档和实现差异保留为待办。

原始批次执行两个 memory consolidation 查询，broad 和无 Star 门槛 new 通道各 2 页，共 65 条；incomplete_results 未暴露时为 null。查询日志已保存，搜索结果明细未随遗留批次留存，因此不新增候选或晋升项目，明细复查进入待办。正式项目仍为 20 个，历史参照 1 个，未审查候选 20 个。

7/30 日窗口均没有容差内的可比基线，增长为空。API-native 批次保持 events=[]，上述五项 Release 结论进入 structured-event backfill 队列，不编造 event_id。

外部参考已重新读取 [Verging Labs 方法页](https://verginglabs.com/methodology)、[机器可读数据](https://verginglabs.com/index/memory.json)和[变更记录](https://verginglabs.com/changelog)：仍显示 v0.2、2026-09-16、datasetId=6b0dd2681430eca3。未将托管工具分数归给 OSS 仓库，未进行跨协议性能排行。

本次补齐 [2026-W39](weekly/2026-W39.md)、[W40](weekly/2026-W40.md)、[W41](weekly/2026-W41.md) 周报；其中 W40/W41 缺少当周已发布观测，报告明确保留缺口。

本仓库未执行上游代码、安装或独立评测；当前 Scheduled 管理视图未找到原任务，原对话任务入口无法加载。此次交互式恢复不证明新的无人值守运行成功。
