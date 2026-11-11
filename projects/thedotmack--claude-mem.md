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
