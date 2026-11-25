# thedotmack/claude-mem

捕获并压缩 Agent 会话观察，在后续会话中检索记忆、注入上下文。

## 记忆机制

观察捕获→摘要/压缩→持久保存→按需检索与上下文回注；存储后端细节待代码核查。

## 部署和依赖

上游说明支持多种 Coding Agent；仅登记作者声明，不代表我们逐宿主安装验收。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent_memory, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `96737c36e49efeaf33497c2710ff16ffa558fcc4` |
| HEAD 观察（UTC） | 2026-10-28T03:35:38.430Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/thedotmack/claude-mem/blob/main/README.md)；[机制说明采用的固定版本](https://github.com/thedotmack/claude-mem/tree/dcfc44221deabc228b0698a0012f87ed2fe6bbe7)。实现/评测资产线索：src/ 与插件配置；以 README 的工作流说明为当前证据。README 阅读与 HEAD 采集并非同时完成；这部分证据属于上游说明，不等于代码审计。写入的具体触发条件、删除保证、隔离和存储后端，仍需结合对应实现进一步核实。

[元数据来源](https://api.github.com/repos/thedotmack/claude-mem)；[HEAD 来源](https://api.github.com/repos/thedotmack/claude-mem/git/ref/heads/main)。首次公开日期尚不明确，不能用仓库创建日期替代。

## 限制与本轮变化

部署路径可能涉及托管 observer 或外部模型；不能仅因插件在本地就认定数据不出网。

早期记录曾有 Release 增量缺口。本轮已取得与当前成功水位重叠的 Release 页；仅代表本轮增量范围完整，不对早期完整历史作追溯保证。

## 最近核实的发布

v13.39.0 修复 Codex 子代理在线程压缩后丢失记忆时间线：PostCompact 按 session_id/agent_id 标记线程，下一次 PostToolUse 恢复一次 timeline；SessionStart 清理标记以免根线程重复注入。

该结论来自正式 Release 说明；未检查本版本实现，也未验证各宿主实际行为。

[v13.39.0 官方 Release](https://github.com/thedotmack/claude-mem/releases/tag/v13.39.0)；发布（UTC）：2026-10-13T21:31:41Z；观察（UTC）：2026-10-15T04:56:26Z；此段证据等级：`upstream_statement`。

## 2026-10-19 版本追踪：v14

- v14.0.0 引入本地 My Work 查看 Agent 请求、状态和人工 Checked；v14.0.1 修复卡片的 Agent 归属。可选 TeamBrain 为独立商业团队服务，不将其收入开源功能范围。
- 状态：正式 Release；依据上游发布说明，未独立复现。
- 来源：[v14.0.0](https://github.com/thedotmack/claude-mem/releases/tag/v14.0.0)（2026-10-17T15:50:36Z）、[v14.0.1](https://github.com/thedotmack/claude-mem/releases/tag/v14.0.1)（2026-10-17T16:25:51Z）；证据等级 `upstream_statement`。

## 2026-10-24：v15.0.2 observer 输出预算修复

- 正式发布 UTC 2026-10-23T18:51:46Z；北京时间 2026-10-24。上游说明对 OpenRouter/cmem.ai/OpenAI-compatible observer 的推理预算与空回复重试作调整，防止输出预算用尽时零观测被当成正常结果。重试计入已有发送预算并累计用量；强制推理模型仍需按 provider 核对兼容性。
- [Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.0.2)；[PR #5029](https://github.com/thedotmack/claude-mem/pull/5029) 已合并，合并 SHA `edc9880d7733a88b9f56f5ca006a998f22a54ae3`，UTC 2026-10-23T18:47:12Z。
- 等级 `upstream_statement`：阅读正式 Release 和 PR 全文，未执行作者测试、未验证实际提供方效果或费用。其他 103 个提交的完整变更范围尚未全部深读。
- 观察 UTC 2026-10-24T08:07:38.578Z；当前 HEAD 如上表，不能以其移动认定全部变更属于本 Release。

## 2026-10-25：长叙事与刷新失败汇总

主分支增加 story-input 的 narrativeLimit / previousNarrativeChars，超长拒绝带实际长度；runAgentTask 汇总所有已尝试 Agent 的失败，而非仅最后一次回退错误。适用于排查工作进展叙事无法更新与刷新失败；不是记忆算法或性能收益结论。

状态：已合入，未进入本轮观测最新 Release v15.0.2。来源：[固定叙事实现](https://github.com/thedotmack/claude-mem/blob/a4469fd4fc036461c05257184fe6445755f8e370/src/services/work-view/request-groups.mjs)、[失败汇总](https://github.com/thedotmack/claude-mem/blob/a4469fd4fc036461c05257184fe6445755f8e370/src/services/agent-runner/run.ts)、[Release 对照](https://github.com/thedotmack/claude-mem/compare/v15.0.2...a4469fd4fc036461c05257184fe6445755f8e370)。事件 UTC 2026-10-24T23:18:19Z。证据等级 code_inspected，只针对选定源补丁；未审计 bundle，未执行上游。

本轮观察 UTC：2026-10-25T06:03:01.212Z；本轮 Release 增量已覆盖旧成功水位，不表示穷尽历史。

## 2026-10-26：首次设置的云依赖与记忆写入来源防护

- [v15.2.0](https://github.com/thedotmack/claude-mem/releases/tag/v15.2.0)于UTC2026-10-25T11:52:08Z发布，真实tag指向1ce03615ca3df37683baf22b5ac0a7b12d3e9866。新安装扫描近30天历史，向CMEM Cloud发送筛选后用户提示词，随后选择存储位置。At Home不构成首次设置离线保证；持续刷新与首次设置不同，不笼统说全部功能都云端。
- [已读HostedIntent](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/work-view/hosted-intent.ts)将ownerPrompts/improveProduct一起gzip上传/api/pro/intent；improveProduct=false并不在该函数中禁止上传。云端与完整筛选链未审计。
- [PR5039](https://github.com/thedotmack/claude-mem/pull/5039)于UTC2026-10-25T12:09:56Z合并；MemoryRoutes在saveMemory前检查浏览器Origin。无Origin本地客户端及同端口loopback保留信任模型，并非新增完整认证。[MemoryRoutes](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/worker/http/routes/MemoryRoutes.ts)与[实际helper](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/worker/http/routes/SettingsRoutes.ts)已读并与固定tree/blob比对；[版本对照](https://github.com/thedotmack/claude-mem/compare/1ce03615ca3df37683baf22b5ac0a7b12d3e9866...fa4e6e0fcc7cf16ca746940e92207d2159a6a2cf)确认防护尚不在v15.2.0。
- 上一节叙事预算/失败汇总已被本轮v15.1.0发布说明列入；保留上一轮当时观察，不改写成历史早已发布。
- code_inspected仅限选定文件；发布/托管效果为upstream_statement，未执行上游或复现实验。完整24提交范围未逐一审计，待办保留。观察UTC 2026-10-25T16:21:15.560Z。

## 2026-10-27：缓冲写入完成后再保存转录检查点；可选本地数据库备份

转录 watcher 按缓冲消息序号延后检查点，worker 接入 gate；自动 SQLite 快照需启用配置，首次约5分钟后执行，默认间隔24小时保留7份。两项均在 v15.2.1 真实 tag 之后。磁盘检查不可用时会跳过容量检查，未独立验证恢复/断电一致性。

状态：`merged_unreleased`；证据等级 `code_inspected`。这是选定实现和一手发布材料的检查，未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/thedotmack/claude-mem/compare/35e24ba7f50f357b81bdafd823f89b41d65679fc...7325fb7818ff7426665d85922db642ec0931bdcd)；来源版本 `7325fb7818ff7426665d85922db642ec0931bdcd`。
- 事件 UTC 2026-10-26T11:34:44Z；观察 UTC 2026-10-26T16:15:39.239Z。
- 已读范围：`src/services/transcripts/watcher.ts`、`src/services/transcripts/types.ts`、`src/services/transcripts/processor.ts`、`src/services/worker/SessionMessageBuffer.ts`、`src/services/worker-service.ts`、`src/services/backup/BackupManager.ts`。
- 记录的默认分支 HEAD：`7325fb7818ff7426665d85922db642ec0931bdcd`，采样 UTC 2026-10-26T16:11:36.314Z；不是实时最新版本，也不表示其他提交已经逐项审查。

</details>

## 2026-10-28：v15.3.0 保存交付文件副本

Stop/SubagentStop 将符合条件的交付文件复制到本地项目目录，并在 My Work 提供入口；每次最多50个文件、单文件512 MiB，私密回合和远端 worker 跳过。可通过 CLAUDE_MEM_DELIVERABLES_ENABLED=false 关闭；用户应检查副本保留与磁盘占用。上一轮检查的转录检查点与可选数据库快照也已列入此版本。

状态：`released`；选定实现为 `code_inspected`，发布声明为 `upstream_statement`；未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/thedotmack/claude-mem/releases/tag/v15.3.0)；来源版本 `43c5b2ead715859fce70c56c95fff5a6d77804c0`。
- 事件 UTC 2026-10-26T23:57:00Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 已读范围：[src/cli/deliverables-capture.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/cli/deliverables-capture.ts)；[src/cli/handlers/summarize.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/cli/handlers/summarize.ts)；[src/shared/deliverables.ts](https://github.com/thedotmack/claude-mem/blob/43c5b2ead715859fce70c56c95fff5a6d77804c0/src/shared/deliverables.ts)。
- 默认分支记录为 `96737c36e49efeaf33497c2710ff16ffa558fcc4`，采样 UTC 2026-10-28T03:35:38.430Z；其余差异未全部审查，历史记录保留。

</details>

## 2026-10-29：v15.5.0 重点核对

可选通用脱敏规则识别配置形态中的裸 token、secret、api_key 键；通用规则默认关闭，值仍须至少8个允许字符且含字母。 依赖工具输出脱敏的使用者应核对 CLAUDE_MEM_REDACT_GENERIC_ENABLED 与禁用规则列表，并用自己的输入验证；不能假定所有同名标识符或历史记录都会被处理。

[合并 PR](https://github.com/thedotmack/claude-mem/pull/5130)；[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.5.0)。合并 UTC 2026-10-28T04:39:09Z；发布 UTC 2026-10-29T00:48:22Z；观察 UTC 2026-10-29T07:26:10.343Z。证据等级 code_inspected，仅静态阅读 [src/utils/redaction.ts](https://github.com/thedotmack/claude-mem/blob/2bc22fa29d43045faafbd621abf14654c050d088/src/utils/redaction.ts)；未独立复现。

## 2026-11-01：v15.7.0 重点核对

My Work 自动刷新中，回答被自身规则拒绝后结束本次运行，不再因此转给下一个已登录 Agent；无法启动的 Agent 仍可触发回退。 同时登录 Claude Code 与 Codex 的用户可评估升级并复测后台调用。它没有新增 Codex 回退单独 opt-in，也未解决用量限制后的暂停诉求，不能当成彻底禁用回退。

[合并 PR](https://github.com/thedotmack/claude-mem/pull/5190)；[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.7.0)。合并 UTC 2026-10-30T16:57:55Z；发布 UTC 2026-10-30T18:18:54Z；观察 UTC 2026-10-31T16:11:56.075Z。静态源码版本 `35d8557840fc4105b55d8aeb499e6795d08afa65`，已确认包含该合并；证据等级 code_inspected，未独立复现。阅读范围：[src/services/agent-runner/run.ts](https://github.com/thedotmack/claude-mem/blob/35d8557840fc4105b55d8aeb499e6795d08afa65/src/services/agent-runner/run.ts)、[src/services/work-view/refresh-task.ts](https://github.com/thedotmack/claude-mem/blob/35d8557840fc4105b55d8aeb499e6795d08afa65/src/services/work-view/refresh-task.ts)。

## 2026-11-04：v15.8.3 重点核对

浏览器安装向导先在本地扫描历史，再等待明确同意才向 cmem.ai 上传选中工具的提示词；匿名结果共享默认关闭，独立于上传同意。 使用 v15.2.0 起浏览器安装向导的用户应评估升级并检查上传选项。扫描仍先读取本地历史；升级不删除旧版本已上传的数据，也未核验服务端保留策略。

[合并 PR](https://github.com/thedotmack/claude-mem/pull/5220)；[Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.8.3)。合并 UTC 2026-11-02T06:12:18Z；发布 UTC 2026-11-02T06:26:25Z；观察 UTC 2026-11-03T16:06:25.908Z。静态源码版本 `9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4` 已确认包含该合并；证据等级 code_inspected，未独立复现。阅读范围：[src/services/prompt-import/setup-scan.ts](https://github.com/thedotmack/claude-mem/blob/9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4/src/services/prompt-import/setup-scan.ts)、[src/services/worker/http/routes/WorkViewRoutes.ts](https://github.com/thedotmack/claude-mem/blob/9603d9bd7ba2bf1ed53595cf7eaa7e7b6a8013e4/src/services/worker/http/routes/WorkViewRoutes.ts)。

## 2026-11-06：重点变更核对

新增记忆捕获开关：精确字符串 `CLAUDE_MEM_OBSERVER_ENABLED="false"` 停止新的 observation/session-summary 模型调用，已有记忆、搜索与 SessionStart 上下文保持可用。 需要暂停本机捕获的用户可评估 v15.10.0。默认仍启用，错误值不会关闭；服务器已排队任务及其他客户端不受这个本机设置控制，不应把它当成全局停采或删除记忆。

[PR](https://github.com/thedotmack/claude-mem/pull/5353)；合并 UTC 2026-11-05T10:26:14Z；[正式版本 v15.10.0](https://github.com/thedotmack/claude-mem/releases/tag/v15.10.0) 发布 UTC 2026-11-05T19:57:39Z；实际 tag 已核对包含该合并。观察 UTC 2026-11-06T04:07:56.131Z。静态源码版本 `c2bca506d853e867cfa02341672869354b85e18a`，证据等级 code_inspected，未独立复现。阅读范围：[src/shared/observer-capture.ts](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/src/shared/observer-capture.ts)、[src/services/worker/SessionManager.ts](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/src/services/worker/SessionManager.ts)、[docs/public/configuration.mdx](https://github.com/thedotmack/claude-mem/blob/c2bca506d853e867cfa02341672869354b85e18a/docs/public/configuration.mdx)。

## 2026-11-07：重点变更核对

识别 Claude CLI 以助手文本返回的 429 限流拒绝，把当前记忆批次重置为 pending 并暂停生成，避免第二次非 XML 回复导致批次被确认后丢弃。 受影响者是使用 Claude observer、遇到这类限流文本的用户；可评估 v15.10.1，并在恢复后核对批次是否实际写入。普通提及数字 429 的文本及有效 observation/summary XML 不按此规则重排队。

本项限于识别到的限流拒绝；不能据此保证所有排队工作永久保留。该版本另有“持续无响应且恢复次数耗尽后丢弃缓冲”的不同策略，本轮未把它等同于限流保留。

[PR](https://github.com/thedotmack/claude-mem/pull/5430) 合并 UTC 2026-11-06T05:27:34Z；[正式版本 v15.10.1](https://github.com/thedotmack/claude-mem/releases/tag/v15.10.1) 发布 UTC 2026-11-06T11:52:02Z；实际 tag commit `016c4c34c01f77790b3d47f867319fadf300e49d` 已确认包含该合并。审读观察 UTC 2026-11-06T16:40:39.338Z；证据等级 code_inspected，未独立复现。annotated tag 解引用至 016c4c3；其到已读 HEAD 51fb777 的 compare 只有 docs/CHANGELOG.md，两个版本的所读 classifier/ResponseProcessor 代码一致；GeneratorRunner 直接按 tag commit 读取。

阅读范围：[src/sdk/output-classifier.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/sdk/output-classifier.ts)、[src/services/worker/agents/ResponseProcessor.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/services/worker/agents/ResponseProcessor.ts)、[src/services/worker/session/GeneratorRunner.ts](https://github.com/thedotmack/claude-mem/blob/016c4c34c01f77790b3d47f867319fadf300e49d/src/services/worker/session/GeneratorRunner.ts)。

## 2026-11-08：重点变更核对

本地 observer 在 quota/auth 失败时丢弃尚待处理的输入，恢复额度或凭据后不自动重放旧积压；其他可恢复暂停保留有界 RAM 缓冲。 依赖故障后补采的用户应先评估捕获缺口与费用取舍。不要把 429 限流保留策略等同于 quota/auth 恢复；原始 transcript 和既有记忆仍可用。

发布说明与生命周期文档规定输入五分钟过期、每会话最多128条及每worker最多1024条。本轮静态确认标签中的 quota/auth 丢弃分支；容量与时效未独立运行验证。这是减少旧任务消耗与允许捕获缺口的取舍，不能解释为记忆更完整。server/BullMQ 队列不在该本地 observer 结论内。

[PR](https://github.com/thedotmack/claude-mem/pull/5347) 合并UTC 2026-11-06T22:06:53Z；状态 released；发布UTC 2026-11-06T22:17:48Z。审读版本 `24802b13ef5e9bf61a84e650af446c4ff69ab399`，观察UTC 2026-11-07T16:44:08.399Z，证据等级code_inspected，未独立复现。实际 annotated tag 解引用至24802b13；PR合并commit到该tag的compare为ahead且behind_by=0。退出处理与生命周期文档均直接读取该tag commit；观察到v15.11.1也已发布，但本项以首次包含该行为的v15.11.0为界。

阅读范围：[src/services/worker/session/GeneratorExitHandler.ts](https://github.com/thedotmack/claude-mem/blob/24802b13ef5e9bf61a84e650af446c4ff69ab399/src/services/worker/session/GeneratorExitHandler.ts)；[docs/architecture/observer-lifecycle.md](https://github.com/thedotmack/claude-mem/blob/24802b13ef5e9bf61a84e650af446c4ff69ab399/docs/architecture/observer-lifecycle.md)。

## 2026-11-09：重点变更核对

删除会话后，以删除时刻为截止线恢复同一对话的新内容采集，旧事件仍被拦截。 曾删除并继续使用同一对话的用户可评估 v15.12.0；检查新内容捕获和删除前内容隔离。

源码中事件时间必须严格晚于删除时刻；未知时间仍跳过，Schema v74 增加截止线触发器。没有证明故障积压会重放，也未实测跨连接竞态。

[PR](https://github.com/thedotmack/claude-mem/pull/5463) 合并UTC 2026-11-07T16:38:12Z；状态 released；发布UTC 2026-11-07T19:51:33Z。审读版本 `2d8c08c182af68b20bb7528c7bf989aa871a7d2f`，观察UTC 2026-11-08T16:33:53.438Z，证据等级code_inspected，未独立复现。注释标签 fe4ccd67 解引用至 eb00299a；merge→tag compare ahead=2、behind=0，且 Release 正文列出 PR5463。

阅读范围：[src/services/sqlite/SessionStore.ts](https://github.com/thedotmack/claude-mem/blob/2d8c08c182af68b20bb7528c7bf989aa871a7d2f/src/services/sqlite/SessionStore.ts)；[src/services/worker/http/shared.ts](https://github.com/thedotmack/claude-mem/blob/2d8c08c182af68b20bb7528c7bf989aa871a7d2f/src/services/worker/http/shared.ts)；[src/services/transcripts/processor.ts](https://github.com/thedotmack/claude-mem/blob/2d8c08c182af68b20bb7528c7bf989aa871a7d2f/src/services/transcripts/processor.ts)。

## 2026-11-10：重点变更核对

Cursor 摘要改用与宿主一致的工作目录 slug，覆盖 Windows 盘符、下划线、空格和点目录。 使用 Cursor 且出现缺失会话摘要时，核对版本和实际 transcript 路径；修复进入 v15.13.0。

适配器把非 ASCII 字母数字替换为连字符、合并并去除首尾连字符，保留 session ID 与文件存在检查；仍由 homedir 推导路径，不读取 CURSOR_DATA_DIR。上游 PR 的本地测试和 Release 的效果表述不等于本项目验证了真实 Cursor 会话。

[PR](https://github.com/thedotmack/claude-mem/pull/5544) 合并UTC 2026-11-09T09:44:33Z；状态 released；发布UTC 2026-11-09T10:06:27Z。审读版本 `1ef2b44832d94bb48c04d3f6ca8050ff92609a73`，观察UTC 2026-11-09T16:13:47.241Z，证据等级code_inspected，未独立复现。注释标签已解引用到发布提交；合并提交至发布提交 compare 的 behind_by=0、ahead_by=2，Release 明确列出 PR #5544。

阅读范围：[src/cli/adapters/cursor.ts](https://github.com/thedotmack/claude-mem/blob/1ef2b44832d94bb48c04d3f6ca8050ff92609a73/src/cli/adapters/cursor.ts)；[tests/transcripts/cursor-extraction.test.ts](https://github.com/thedotmack/claude-mem/blob/1ef2b44832d94bb48c04d3f6ca8050ff92609a73/tests/transcripts/cursor-extraction.test.ts)。

## 2026-11-11：重点变更核对

Cowork 遇到发送失败时丢弃提示、观察和摘要，补发队列只保留会话元数据；OpenCode 的会话初始化只发起一次请求。 依赖停机后自动补采的用户可先核对采集缺口与 worker 可用性。

静态核对覆盖 Cowork 队列和 OpenCode 初始化。发布说明还称 transcript watcher 会跳过拒收行，本轮未对该路径做同等核对。

[PR](https://github.com/thedotmack/claude-mem/pull/5663) 合并UTC 2026-11-10T06:50:02Z；状态 released；发布UTC 2026-11-10T07:06:39Z。审读版本 `f00618f931cc21f2f871be7dee724029a772f017`，观察UTC 2026-11-11T08:23:35.227Z，证据等级code_inspected，未独立复现。合并提交是发布提交的祖先，比较结果 ahead=1、behind=0。

阅读范围：[cowork/scripts/cmem-hook.mjs](https://github.com/thedotmack/claude-mem/blob/f00618f931cc21f2f871be7dee724029a772f017/cowork/scripts/cmem-hook.mjs)；[src/integrations/opencode-plugin/core.ts](https://github.com/thedotmack/claude-mem/blob/f00618f931cc21f2f871be7dee724029a772f017/src/integrations/opencode-plugin/core.ts)。

## 2026-11-12：重点变更核对

新增 eve 记忆 provider。含用户文本的回合开始时调用 cmem.ai 检索，显式调用 remember 时写入。 接入 eve 前核对 cmem.ai 凭据和项目作用域。默认按作用域选项目，开启 searchAllProjects 会扩大检索范围。

源码显示，回合自动检索会转义召回文本，并在非取消的错误下给模型返回不可用提示。跨项目检索配置与显式写入的作用域是分别控制的。

[PR](https://github.com/thedotmack/claude-mem/pull/5863) 合并UTC 2026-11-11T06:09:07Z；状态 released；发布UTC 2026-11-11T06:13:38Z。审读版本 `5681b2a3a9ec1be2c53264e6009ab82ad11ae601`，观察UTC 2026-11-14T00:28:06.133Z，证据等级code_inspected，未独立复现。发布标签指向的提交比 PR 合并提交领先 1 个提交、落后 0 个，且两个版本的 provider 文件 blob 相同。

阅读范围：[integrations/eve/provider/src/index.ts](https://github.com/thedotmack/claude-mem/blob/5681b2a3a9ec1be2c53264e6009ab82ad11ae601/integrations/eve/provider/src/index.ts)。

## 2026-11-14：重点变更核对

Windows 的 Gemini CLI hook 命令加上 PowerShell 调用运算符 `&`，使带引号的 Bun 路径能以命令执行。 使用 Windows Gemini CLI 的用户升级后可重写既有 hook 配置，并核对一次会话记录。

同一安装器识别新旧命令格式。已静态核对发行版中的安装器和 PR 测试改动，未在 Gemini CLI 中运行。

[PR](https://github.com/thedotmack/claude-mem/pull/6079) 合并UTC 2026-11-12T17:19:46Z；状态 released；发布UTC 2026-11-12T17:40:57Z。审读版本 `df3f13f0ffda5693de994d65cf613d9606c4c189`，观察UTC 2026-11-14T02:56:32.785Z，证据等级code_inspected，未独立复现。发行标签包含合并提交：领先 2 个提交，落后 0。

阅读范围：[src/services/integrations/GeminiHooksInstaller.ts](https://github.com/thedotmack/claude-mem/blob/df3f13f0ffda5693de994d65cf613d9606c4c189/src/services/integrations/GeminiHooksInstaller.ts)。

## 2026-11-16：重点变更核对

claude-mem 在 Claude Code 中通过 Markdown 导入链加载规则与工具说明。已有说明匹配时，MCP 初始化省略重复文本。 使用自定义规则文件或数据目录的 Claude Code 用户可核对导入路径和启动时出现的说明。

MCP 省略说明有宿主、导入链和文本匹配条件。未执行 Claude Code 会话。

[PR](https://github.com/thedotmack/claude-mem/pull/6179) 合并UTC 2026-11-15T05:48:47Z；状态 released；发布UTC 2026-11-15T05:54:37Z。审读版本 `ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774`，观察UTC 2026-11-15T16:13:24.397Z，证据等级code_inspected，未独立复现。发行说明直接列出该 PR。

阅读范围：[src/shared/claude-code-rules-import.ts](https://github.com/thedotmack/claude-mem/blob/ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774/src/shared/claude-code-rules-import.ts)；[src/servers/mcp-server.ts](https://github.com/thedotmack/claude-mem/blob/ff25f7f3e8e101b9240ca1bbc9b2b922a95f7774/src/servers/mcp-server.ts)。

## 2026-11-17：重点变更核对

从 Mem0 Platform 或 Supermemory 单向导入记忆到指定项目 已有来源账号和本地 worker 的迁移用户可先用 dry-run 核对范围。

Mem0 按用户、Supermemory 按命名空间读取，需要来源 API 凭据和可访问的 worker。CLI 收齐并校验分页后才开始写入，写入中途报错会停止。Supermemory 文档模式导入提取文本，源端后续删除与过期不会同步。

[PR](https://github.com/thedotmack/claude-mem/pull/6106) 合并UTC 2026-11-15T19:52:44Z；状态 released；发布UTC 2026-11-16T02:04:44Z。审读版本 `01a86b235d3b9854c18e1841133d9a8e7fe1171a`，观察UTC 2026-11-16T16:25:40.713Z，证据等级code_inspected，未独立复现。发布标签包含合并提交，固定审读版本 01a86b235d3b9854c18e1841133d9a8e7fe1171a。

阅读范围：[src/npx-cli/commands/import-memory.ts](https://github.com/thedotmack/claude-mem/blob/01a86b235d3b9854c18e1841133d9a8e7fe1171a/src/npx-cli/commands/import-memory.ts)；[src/npx-cli/index.ts](https://github.com/thedotmack/claude-mem/blob/01a86b235d3b9854c18e1841133d9a8e7fe1171a/src/npx-cli/index.ts)；[docs/public/usage/import-providers.mdx](https://github.com/thedotmack/claude-mem/blob/01a86b235d3b9854c18e1841133d9a8e7fe1171a/docs/public/usage/import-providers.mdx)。

## 2026-11-18：重点变更核对

导入界面增加停止操作：中止正在等待的上传并阻止继续发送；未收到答复的在途批次标为未确认。 迁移时先核对已确认与未确认的条目，再决定是否重新开始。

适用于新版本地设置流程向 cmem.ai 上传历史观察。已确认上传会保留，停止不会删除两端数据，也不能保证服务器没收到最后一个批次。

[PR](https://github.com/thedotmack/claude-mem/pull/6233) 合并UTC 2026-11-17T10:56:12Z；状态 merged_unreleased；发布UTC 未确认。审读版本 `3d1aa47ec6406c88a76bf9289c4a4248282303e6`，观察UTC 2026-11-17T16:11:56.101Z，证据等级code_inspected，未独立复现。本轮未核实覆盖该变更的发布包；固定源码已审读，未独立运行。

阅读范围：[src/ui/my-work/src/setup/screens/import-screen.tsx](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/src/ui/my-work/src/setup/screens/import-screen.tsx)；[src/services/setup/history-import.ts](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/src/services/setup/history-import.ts)；[tests/worker/http/routes/setup-import-routes.test.ts](https://github.com/thedotmack/claude-mem/blob/3d1aa47ec6406c88a76bf9289c4a4248282303e6/tests/worker/http/routes/setup-import-routes.test.ts)。

## 2026-11-19：兼容性与可靠性修正

claude-mem 为已跟踪的转录文件增加默认三秒的追加检查，补足遗漏的文件通知。 主要排查 macOS/Bun 下长期开启的转录文件追加未被捕获；先确认文件已经建立 tailer。

TranscriptWatcher.start 在建立 watches 后启动追加轮询，默认间隔3000ms；间隔<=0不启动。每次仅遍历已有 tailer，按 readOffset 判断新增字节，再经 poke/requestRead 进入既有处理和状态保存路径，不负责发现所有新文件。逐个异步 stat；前一轮未结束时跳过下一 tick，stop 会取消计时并停止后续处理，大文件集合不能承诺三秒端到端延迟。

固定 HEAD 源码及完整两文件 PR 差异已读；v16.0.0 是注释 tag，本轮未剥离其对象，不把此修复默认标成已随该包交付。

[PR](https://github.com/thedotmack/claude-mem/pull/6285) 合并UTC 2026-11-17T18:08:57Z；审读材料观察UTC 2026-11-19T06:25:10.133Z。固定观察 HEAD `c1dc252bda98b1310ba3fa4b195efe49070d554b`，证据等级 code_inspected（上述有界范围），未独立运行；发行包含关系未确认。

阅读范围：[src/services/transcripts/watcher.ts](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/src/services/transcripts/watcher.ts)；[src/shared/SettingsDefaultsManager.ts](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/src/shared/SettingsDefaultsManager.ts)；[package.json](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/package.json)。

## 2026-11-20｜Codex 认证文件不再建立硬链接

私有 Codex home 改为优先符号链接；Windows 遇 EPERM、EACCES 或 ENOTSUP 时复制独立文件。

状态：已发布 v16.0.1；tag 含合并提交。

### thedotmack/claude-mem #6332

仅针对 claude-mem 的 Codex ChatGPT 登录路径，API key 不适用。其他符号链接错误继续抛出；复制使用 COPYFILE_EXCL，已有目标不会被覆盖。副本只是启动时快照，不向用户认证文件回写；recycle 后重新取当前登录。此处不建议更改系统权限或 Developer Mode。

合并 UTC 2026-11-19T11:01:27Z；PR观察 UTC 2026-11-19T16:34:38.887Z；固定合并提交 `833a0a834c8c91e6b4843cdba5c8bbe9035fb6d9`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/thedotmack/claude-mem/pull/6332)；[src/services/worker/CodexAppServerClient.ts](https://github.com/thedotmack/claude-mem/blob/833a0a834c8c91e6b4843cdba5c8bbe9035fb6d9/src/services/worker/CodexAppServerClient.ts)（blob `c2700c146041ef88d6f3828a10be91cb4ab62479`）

[发行](https://github.com/thedotmack/claude-mem/releases/tag/v16.0.1)：tag 解至 `e22c58353b950b15e6e16d98719801224840f046`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

来源批次 `20261119T160540Z-local`；[本轮日期稿](../reports/briefs/20261119T160540Z-local.md)。

## 2026-11-21｜Chroma 集合删除结果不明时先核对列表

Chroma MCP 删除请求丢失回执或超时后，通过一次完整集合列表确认目标是否已消失。 已合并，未确认随包交付。

该路径由同一集合的两个不同批次触发损坏确认，并合并同进程中的并发删除。MCP 管理器把删除回执丢失归为结果不明，重连后由调用方查询列表，支持多段文本、JSON 数组及空库标记。列表有效且目标缺席才记为已删除。目标仍存在、列表格式无效或查询失败会抛错，后续损坏批次可用至多三次的进程内失败预算。后台扫描仍会重启，预算耗尽后的进程内停止重试标记也不能作为数据库删除确认。

合并时间 2026-11-19T18:36:00Z，观测时间 2026-11-20T16:05:10.338Z，合并提交 c0f37d60b2e4860851575e3cbb003f23fc340d4e。在 2026-11-20T16:05:11.451Z 取得全部 5 个 PR 文件条目，按相关入口做静态审读。

[PR 与完整文件列表](https://github.com/thedotmack/claude-mem/pull/6338) · [ChromaSync.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/src/services/sync/ChromaSync.ts) · [ChromaMcpManager.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/src/services/sync/ChromaMcpManager.ts) · [chroma-sync-corrupt-collection.test.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/tests/services/sync/chroma-sync-corrupt-collection.test.ts)

[本轮日期稿](../reports/briefs/20261120T160119Z-local.md)。

## 2026-11-23

Knowledge Agent 的初始化与查询分别设 10 分钟总时限，Corpus POST 另设请求时限。 已发布 v16.0.3。

单次 prime 或 query 的期限包含 Claude CLI 定位、凭据刷新及会话失效后的自动重新 prime。代码使用总时限，允许 SDK 在大型语料预填充期间保持静默。Corpus POST 默认沿用 MCP 客户端的 15 分钟上限。JSON 路径返回 504，SSE 路径发出终止错误事件。若构建在 HTTP 超时后仍在写入，语料库的互斥限制持续到实际工作结束。

合并于 2026-11-21T18:29:19Z，观测于 2026-11-22T16:24:16.028Z。合并提交 18abce9e49c36b4d95b030658392e6390745fbc7，PR 文件列表完整（4 个文件）。v16.0.3 注释标签剥离为 4a04765b17c46d36d6ecdd91b41f1adffffa2a81，compare 保存的父链可达本项合并。 证据等级 code_inspected。 [PR #6368](https://github.com/thedotmack/claude-mem/pull/6368) · [KnowledgeAgent.ts](https://github.com/thedotmack/claude-mem/blob/18abce9e49c36b4d95b030658392e6390745fbc7/src/services/worker/knowledge/KnowledgeAgent.ts) · [CorpusRoutes.ts](https://github.com/thedotmack/claude-mem/blob/18abce9e49c36b4d95b030658392e6390745fbc7/src/services/worker/http/routes/CorpusRoutes.ts) · [corpus-routes-sse.test.ts](https://github.com/thedotmack/claude-mem/blob/18abce9e49c36b4d95b030658392e6390745fbc7/tests/worker/http/routes/corpus-routes-sse.test.ts) · [v16.0.3](https://github.com/thedotmack/claude-mem/releases/tag/v16.0.3) · [本次简报](../reports/briefs/20261122T162043Z-local.md)

## 2026-11-24

Mem0 导入接受生命周期字段为 null 的记录，继续按替换关系和到期时间筛选。 变更位于 `import-memory` 的 Mem0 分支。`lifecycle_state` 缺失或为 `null` 时通过该字段校验。其他陌生状态仍报错，替换或已到期的记录仍可被跳过。计划会校验来源账号和记录身份，并把原始来源字段保存在 `importSource`。上游测试源码覆盖了 `null` 的导入和重复导入。

v16.1.1 注释标签剥离为 `ecfc1c0bde70efc16839e3ffcdf02efce736512f`，留存的默认分支父链包含该变更。 提交记录日期 2026-11-23T17:28:22Z，来源读取于 2026-11-24T09:40:10.884Z。证据等级 `code_inspected`。

[固定提交](https://github.com/thedotmack/claude-mem/commit/42dd5db0be3fee9d70d26f83f202d56bacac3df7) · [导入校验与计划](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/src/npx-cli/commands/import-memory.ts#L262-L277) · [保存确认](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/src/npx-cli/commands/import-memory.ts#L327-L343) · [测试源码](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/tests/fixtures/import-provider-smoke.py#L80-L91) · [v16.1.1](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.1)

## 2026-11-25 | v16.1.2 My Work 安装

手机安装表单底部吸附操作区，符合首次安装条件时显示已设置的代理数量。

安装操作区的样式适用于宽度不超过 560 CSS 像素。首次安装摘要要求扫描完成、无历史与结果、无请求读取错误，且提取未运行也未失败。数量取自状态为 ready 的安装选择。发行标签已解析到该实现提交，安装流程未实际运行。

[一手来源](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.2)

- [移动端样式](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/setup.css#L555-L585)
- [首次安装条件](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/screens/reveal-screen.tsx#L203-L240)
- [数量来源](https://github.com/thedotmack/claude-mem/blob/a046a6a9fd8fb1cc56466194487dca94e8212409/src/ui/my-work/src/setup/setup-page.tsx#L333-L336)

观测时间：2026-11-24T16:16:16.671Z。证据等级为 `code_inspected`。

### 2026-11-26 · OpenRouter 的 HTTP 200 响应内若含临时上游错误，观察器会按实际错误分类

v16.1.3 发布，v16.1.5 源码仍包含。从已剥离的 v16.1.5 标签看，OpenRouter 返回 2xx 时，响应体内 400–599 的数字错误码参与分类。429 进入限流路径，5xx 进入短暂上游故障路径。已知的上游输出解析失败保留原 HTTP 状态，避免把可能已计费的请求当临时故障重发。短暂故障超过内部重试且观察器暂停时，批次保留，存在可用后备提供商时可继续处理。v16.1.3 [发行说明](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.3)登记了首发修复，v16.1.5 为本轮核对实现的版本。

证据等级 `code_inspected`。变更或发行 UTC 2026-11-24T18:32:35Z，源码观测截至 2026-11-25T16:04:52.190Z。本轮未做独立运行。 [变更记录](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.3) · [响应体分类](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/OpenRouterProvider.ts#L185-L201) · [响应体调用入口](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/OpenRouterProvider.ts#L1252-L1264) · [暂停与队列处理](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/session/GeneratorRunner.ts#L322-L357)
