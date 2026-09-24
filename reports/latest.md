# 最新研究简报

本轮：`20260924T081121Z-scheduled`；观测时间（UTC）：2026-09-24T08:11:21Z。

本轮 21/21 个登记项目的 metadata、默认分支 HEAD 和当前 Release 水位均成功采集。11 个既有项目默认分支 HEAD 发生变化；按每轮最多 5 个项目的深审预算，优先检查 Mem0、Letta Code、Hindsight、TencentDB-Agent-Memory 与 Claude Mem。其余 Graphiti、MemOS、Neo4j Agent Memory、OpenViking、Agent Memory Benchmark、tigerless Agent Memory 只记录 HEAD 变化并留待后续深审，不据此生成技术事件。

## 已核实的重要变化

### Mem0：Coding Agent 的记忆搜索从“强制/并行”转向“按需聚焦”

PR #7420 实际修改了 Claude Code、Cursor、Codex、Kimi、Antigravity、OpenCode、Pi、DeepSeek Harness、OpenClaw 等插件共享的 prompt / tool description。新的策略不再要求“只要回答可能依赖历史就必须搜索”，而是在重复调查，或历史决策、修复、命令、结果可能有帮助时进行一次聚焦搜索；OpenCode 等路径还移除了 2–4 个并行搜索的默认要求。证据等级：`code_inspected`。这说明插件正在把 memory retrieval 从高频强制调用收敛为任务相关调用，但本仓库没有独立评测 token、延迟或答案质量收益。

同日发布的 v2.2.0 还新增 User Profiles Python SDK API，可生成/读取按 schema 组织的结构化用户画像并管理 profile settings、sample 与异步 job。该部分依据 Release notes，证据等级：`upstream_statement`。

### Letta Code：把旁路记忆维护变成独立后台工作流

PR #4627 引入静默 background `memory` worker：主 Agent 可把“当前任务之外顺手记住某件事”的工作交给后台 worker，worker 使用只读会话快照与精确 memory checkout，在 checkout lease 下写入并同步提交；完成结果不唤醒主 Agent。PR #4628 则把 post-turn Git merge/rebase 冲突交给 repair-only memory worker，并保存冲突尝试状态以避免每轮重复启动。证据等级：`code_inspected`。

相关的 #4626 为 memory checkout 的 harness writer 加跨进程 lease，#4634 将 prompt policy 明确为：旁路记忆请求委托后台 worker，记忆本身是主请求时由主 Agent 直接编辑、提交并验证。v0.33.0 已包含这组变化。

### Hindsight v0.10.1：修正 reflect budget、Codex transcript 与超长会话 retain

对 v0.10.1 关联实现的检查确认三类变化：configured recall token budget 现在能真正传入 reflect tools，并限制模型给出的单次 token ask；Codex transcript reader 改为从 `UserMessage` events 获取真实用户输入，避免把 startup context、AGENTS、environment、compaction 等注入内容当作用户记忆；同时移除 32MB transcript tail cap，改为流式读取全量 transcript，避免长会话越过窗口后每轮重新 retain 全部历史。证据等级：`code_inspected`。未独立运行其上游测试或 benchmark。

### TencentDB Agent Memory v1.0.3：OpenClaw 安装与 sqlite-vec 本地兼容性

上游 Release 声明 v1.0.3 适配 OpenClaw 9.5 gateway 化插件安装，并处理首次安装时 `enabled` 字段的竞态；sqlite-vec native extension 改为优先发现 staged `package-N/vec0.so`，保留旧路径 fallback，并在 native extension 无法加载时允许 degraded mode。证据等级：`upstream_statement`，未独立执行。

### Claude Mem：限制可执行路径写入并加强 telemetry 脱敏

PR #4166 将 `CLAUDE_CODE_PATH` 从未认证的 HTTP settings 写入白名单移除，改为仅允许文件/环境配置；来自不同 localhost 端口 Origin 的浏览器 settings POST 会被拒绝。Telemetry scrub 同时增加 residual query string、assignment secret 与 Slack webhook path secret 的脱敏，并对允许上报的字符串字段再次经过 redaction pipeline。证据等级：`code_inspected`。

## 发现与覆盖边界

- broad 与“新建、无 Star 门槛”发现通道均检查 2 页，每页 20 条；第 2 页仍满，因此明确标记为非穷尽，连接器也未暴露 `total_count/incomplete_results`。
- 正式项目已达到批准的 20 个目标（另有 1 个历史参照），本轮不为凑数新增正式项目，也不自动提升搜索结果。
- 7/30 日增长仍不报告：当前没有落在目标窗口 ±6 小时内的可比较基线，禁止将不足窗口的数据外推。
- 本轮没有执行任何被跟踪项目代码，也没有独立复现 benchmark、release 测试或性能声明。
- 当前 ISO 周尚未结束，因此没有新的周报到期。
