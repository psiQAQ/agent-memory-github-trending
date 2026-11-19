# Agent Memory 简报｜2026-11-19

五项已合并修正涉及参数选择、转录追加捕获、完成事件、轮询和恢复停止条件。
macOS/Bun 转录捕获、Hindsight 存储繁忙与 Letta listener 恢复的部署者需重点核对适用条件；同期另有客户端和连接器发行。
升级前核对发行标签，分别检查记忆已写入、事件已交付与恢复记录是否保留，避免把其中一项成功当作全部成功。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [mem0ai/mem0](https://github.com/mem0ai/mem0/pull/7939) | Mem0 调整名称识别：连字符 GPT-5 名称及 GPT-6 家族进入推理参数分支。 | 已合并，未核实随包交付 | 使用 OpenAILLM 的单模型 Chat Completions 路径时，先核对模型名与显式 is_reasoning_model 设置。 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/6285) | claude-mem 为已跟踪的转录文件增加默认三秒的追加检查，补足遗漏的文件通知。 | 已合并，未核实随包交付 | 主要排查 macOS/Bun 下长期开启的转录文件追加未被捕获；先确认文件已经建立 tailer。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6625) | Hindsight 在 retain 已成功、完成事件 outbox 遭存储暂拒时增加有界重试。 | 已合并，未核实随包交付 | 区分记忆已写入与完成事件已交付；持续繁忙时仍需检查 outbox write failed 日志。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7782) | OpenViking 本地 Compile 后端改用配置的轮询间隔，移除固定30000ms赋值。 | 已合并，未核实随包交付 | 仅针对 configure_local_backend 路径核对 CompileApiConfig.poll_interval_ms；调短查询间隔不代表编译更快。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/5785) | Letta Code 为重复明确404的 OTID 恢复查询设置停止条件。 | 已合并，未核实随包交付 | 将空成功流、暂时错误和明确404分开排查；仅满足条件的未变化普通记录才可退休。 |
| [claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v16.0.0) | v16.0.0 发布；发布说明聚焦 My Work 界面调整。 | 已发布；上游说明 | 本轮没有剥离注释 tag，不据此认定上表修复已随包交付。 |
| [OpenViking React](https://github.com/volcengine/OpenViking/releases/tag/react%400.1.14) | React 0.1.14 发布，说明列出 Console 与接入流程调整。 | 已发布；上游说明 | 这是 React 包发行，不能替代 Python 本地 Compile 后端的版本核对。 |
| [Cognee](https://github.com/topoteretes/cognee/releases/tag/v1.6.9) | v1.6.9 发布；说明列出连接器、摄取与嵌入调整。 | 已发布；上游说明 | 升级前阅读破坏性变更；本轮没有深读其188个新增提交。 |

### 适用条件

**mem0ai/mem0**。仅核对单模型 OpenAILLM 路径；默认按名称识别，显式 `is_reasoning_model` 优先。点号 GPT-5 名称另处理；服务端参数兼容性未实测。

**thedotmack/claude-mem**。仅补查已有 tailer 的文件，默认3000ms；不负责扫描发现新文件。前一轮未结束时不叠加下一轮，大文件集合不能承诺三秒端到端延迟。

**vectorize-io/hindsight**。仅对 `StoreWriteUnavailable` 重试完成事件事务，最多5次，不重做 retain。持续失败时记忆仍可已写入而事件缺失，需检查错误日志。

**volcengine/OpenViking**。仅限本地 Compile 后端改用配置值；文档默认30000ms。轮询间隔不等于编译耗时；整个服务和配置类未逐行审读。

**letta-ai/letta-code**。同一 OTID/revision 三次明确404、至少经过30秒后，才可能退休未变更且无恢复完成声明的普通记录；空成功流仍等待。v0.34.65 在该修复之前。

## Star 变化：相邻实测区间与合格长期窗口

工程项目按登记顺序展示；关注度不代表质量。相邻观测不外推为完整一天，7/30日基线按±6小时容差选取，实际区间见折叠证据。

| 项目 | 本次 Stars | 相邻观测净变化 | 相邻实际时长 | 7日窗口净变化 | 30日窗口净变化 |
| --- | ---: | ---: | ---: | ---: | ---: |
| mem0ai/mem0 | 69187 | +72 | 23.92小时 | +375 | 无合格基线 |
| thedotmack/claude-mem | 118170 | +266 | 23.92小时 | +2068 | 无合格基线 |
| letta-ai/letta-code | 3867 | +4 | 23.92小时 | +49 | 无合格基线 |
| vectorize-io/hindsight | 61782 | +223 | 23.92小时 | 无合格基线 | 无合格基线 |
| volcengine/OpenViking | 42418 | +47 | 23.92小时 | 无合格基线 | 无合格基线 |

## 新候选线索对比

本轮未新增正式对象或候选：24个登记对象与26个候选已占满50个位置。以下仅是实际搜索返回的元数据线索，尚未核对 README、实现或评测，不作推荐。

| 原始线索 | 描述宣称的载体/机制 | 需核实的内容 |
| --- | --- | --- |
| [bryn-rm/adaptive-experience-compression](https://github.com/bryn-rm/adaptive-experience-compression) | 将已结束轨迹丢弃、保留为情景记忆或压缩为程序技能 | 具体实现、环境依赖、许可正文和独立评测均未核实 |
| [ontogr/ontogr-agent-memory](https://github.com/ontogr/ontogr-agent-memory) | Python库；情景、实体/事实、双时间轴与预算上下文 | 存储依赖、冲突处理、宿主和可重复评测均未核实 |

## 方法与覆盖边界

24个对象的 metadata、HEAD 和增量 Release 均有留存来源；9个 HEAD 区间中只完成上述5项有界静读。3份 compare 达到300文件，不能据此宣称全范围审查。两条无 Star 门槛搜索各读第一页、共40条原始结果，分页未完成；候选线索仅做元数据分流。Hindsight 超大整文件正文未返回，相关结论限定于完整 PR 差异与测试；OpenViking 也未取得整个服务/配置类。未运行上游代码或评测，不把代码静读、上游声明当成独立复现。

<details markdown="1"><summary>证据与时间</summary>

批次 `20261118T155903Z-local`；基线 `e6214f056315c2e34572a831f1abc115e688578c`；来源批次最大观察UTC 2026-11-18T18:40:47.176Z。补充审读按其实际读取时间记录，不改写原来源时间。

### mem0ai/mem0 #7939

OpenAIConfig.is_reasoning_model 默认 None 时才按名称判断；显式 True/False 优先。gpt-5.4 等点号 GPT-5 名称仍不因本次前缀规则进入该分支。_get_supported_params 在推理分支不传 temperature/top_p，也不传旧 max_tokens；不能据此声称所有调用都会发送 max_completion_tokens。OpenRouter 多模型路由及实际服务端参数支持未实测。

已读固定 HEAD 的入口、参数 helper、配置和上游测试；未运行 API 或上游测试。

合并UTC 2026-11-18T07:24:33Z；审读材料实际读取UTC 2026-11-19T06:24:55.194Z；固定 HEAD `fff8a6472512d1bc1a4bccab8c645b65a1df7fe5`。

[PR](https://github.com/mem0ai/mem0/pull/7939)；[mem0/llms/base.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/llms/base.py)；[mem0/llms/openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/llms/openai.py)；[mem0/configs/llms/openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/configs/llms/openai.py)；[tests/llms/test_openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/tests/llms/test_openai.py)

### thedotmack/claude-mem #6285

TranscriptWatcher.start 在建立 watches 后启动追加轮询，默认间隔3000ms；间隔<=0不启动。每次仅遍历已有 tailer，按 readOffset 判断新增字节，再经 poke/requestRead 进入既有处理和状态保存路径，不负责发现所有新文件。逐个异步 stat；前一轮未结束时跳过下一 tick，stop 会取消计时并停止后续处理，大文件集合不能承诺三秒端到端延迟。

固定 HEAD 源码及完整两文件 PR 差异已读；v16.0.0 是注释 tag，本轮未剥离其对象，不把此修复默认标成已随该包交付。

合并UTC 2026-11-17T18:08:57Z；审读材料实际读取UTC 2026-11-19T06:25:10.133Z；固定 HEAD `c1dc252bda98b1310ba3fa4b195efe49070d554b`。

[PR](https://github.com/thedotmack/claude-mem/pull/6285)；[src/services/transcripts/watcher.ts](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/src/services/transcripts/watcher.ts)；[src/shared/SettingsDefaultsManager.ts](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/src/shared/SettingsDefaultsManager.ts)；[package.json](https://github.com/thedotmack/claude-mem/blob/c1dc252bda98b1310ba3fa4b195efe49070d554b/package.json)

### vectorize-io/hindsight #6625

只在完成事件回调事务抛出 StoreWriteUnavailable 时重试该事务，固定上限5次；等待时已释放连接，退避从0.5–1秒随机间隔倍增。它不重新执行已成功的 retain。其他异常进入外层错误记录；五次仍失败时 retain 仍报告成功，事件可能缺失。不能把它解释为数据与通知的原子事务或无条件 exactly-once 保证。

审读完整两文件 PR 差异及已取回的完整测试，核对 _run_retain_execution、回调事务、常量和最终失败分支。memory_engine.py 为1276781字节，Contents 响应 encoding=none，未取得整文件正文；没有把它算作整文件审读。

合并UTC 2026-11-18T09:03:11Z；审读材料实际读取UTC 2026-11-19T06:25:17.851Z；固定 HEAD `522f82bff163720290ab6b56f1aa41e55cf83b70`。

[PR](https://github.com/vectorize-io/hindsight/pull/6625)；[hindsight-api-slim/tests/test_retain_outbox_session.py](https://github.com/vectorize-io/hindsight/blob/522f82bff163720290ab6b56f1aa41e55cf83b70/hindsight-api-slim/tests/test_retain_outbox_session.py)；[hindsight-api-slim/hindsight_api/config.py](https://github.com/vectorize-io/hindsight/blob/522f82bff163720290ab6b56f1aa41e55cf83b70/hindsight-api-slim/hindsight_api/config.py)

### volcengine/OpenViking #7782

PR 差异把 poll_interval_ms=30000 改为 self._config.poll_interval_ms，local=True 不变。上游测试显式传250ms并断言 poll_interval_seconds 为0.25；本轮只读测试。固定配置文档列 poll_interval_ms 默认30000ms，但未获取配置类与整个服务文件，因此不扩大到所有后端或所有部署初始化路径。

完整两文件 PR 差异、测试及固定文档已读；React 0.1.14 的发布不能证明 Python 后端修复随包交付。

合并UTC 2026-11-18T07:00:21Z；审读材料实际读取UTC 2026-11-19T06:25:37.636Z；固定 HEAD `989e6c784283b7895b3f0b7db82b5a070e40f33f`。

[PR](https://github.com/volcengine/OpenViking/pull/7782)；[docs/en/configuration/01-server.md](https://github.com/volcengine/OpenViking/blob/989e6c784283b7895b3f0b7db82b5a070e40f33f/docs/en/configuration/01-server.md)；[README.md](https://github.com/volcengine/OpenViking/blob/989e6c784283b7895b3f0b7db82b5a070e40f33f/README.md)

### letta-ai/letta-code #5785

resolveRecordedRunId 对同一 recoveryScope、OTID 和 revision 计数；三次明确404且距首次至少30秒才返回 not_found，查询间隔跨15秒窗口，单次查询超时5秒且 SDK maxRetries=0。空成功流仍 deferred，其他错误不走404退休分支。recoverRecordedTurns 再核对 unchanged；retireMissingRun 还要求无 recoveryClaimCompletion，并按 revision 条件删除。

固定 HEAD 的入口/helper/记录删除与调度路径已读。v0.34.65 的实际 tag commit 在本修复之前；本轮未核实后续包含它的版本。

合并UTC 2026-11-17T23:32:21Z；审读材料实际读取UTC 2026-11-19T06:25:43.237Z；固定 HEAD `7cd55dcdf723eff6169663b1d0b28b40fd5a607e`。

[PR](https://github.com/letta-ai/letta-code/pull/5785)；[src/websocket/listener/recorded-run-resolution.ts](https://github.com/letta-ai/letta-code/blob/7cd55dcdf723eff6169663b1d0b28b40fd5a607e/src/websocket/listener/recorded-run-resolution.ts)；[src/websocket/listener/recover-recorded-turn.ts](https://github.com/letta-ai/letta-code/blob/7cd55dcdf723eff6169663b1d0b28b40fd5a607e/src/websocket/listener/recover-recorded-turn.ts)；[src/websocket/listener/interrupted-turn-record.ts](https://github.com/letta-ai/letta-code/blob/7cd55dcdf723eff6169663b1d0b28b40fd5a607e/src/websocket/listener/interrupted-turn-record.ts)；[src/websocket/listener/lifecycle.ts](https://github.com/letta-ai/letta-code/blob/7cd55dcdf723eff6169663b1d0b28b40fd5a607e/src/websocket/listener/lifecycle.ts)

### Star 真实窗口

- mem0ai/mem0：相邻观测 2026-11-17T16:05:11.531Z → 2026-11-18T16:00:32.311Z；7日窗口 2026-11-11T16:04:27.969Z → 2026-11-18T16:00:32.311Z，实际6.997天；30日窗口 无±6小时内合格基线
- thedotmack/claude-mem：相邻观测 2026-11-17T16:05:50.185Z → 2026-11-18T16:01:07.328Z；7日窗口 2026-11-11T16:05:06.494Z → 2026-11-18T16:01:07.328Z，实际6.997天；30日窗口 无±6小时内合格基线
- letta-ai/letta-code：相邻观测 2026-11-17T16:06:07.318Z → 2026-11-18T16:01:29.027Z；7日窗口 2026-11-11T16:05:28.070Z → 2026-11-18T16:01:29.027Z，实际6.997天；30日窗口 无±6小时内合格基线
- vectorize-io/hindsight：相邻观测 2026-11-17T16:06:39.984Z → 2026-11-18T16:01:45.182Z；7日窗口 无±6小时内合格基线；30日窗口 无±6小时内合格基线
- volcengine/OpenViking：相邻观测 2026-11-17T16:07:33.505Z → 2026-11-18T16:02:38.434Z；7日窗口 无±6小时内合格基线；30日窗口 无±6小时内合格基线

### 搜索

- `"episodic memory" in:name,description archived:false fork:false`；page=1，返回20，total_count=738，incomplete_results=False，分页完整=False，观察UTC 2026-11-18T18:40:45.415Z
- `"agentic memory" in:name,description created:>=2026-10-19 archived:false fork:false`；page=1，返回20，total_count=635，incomplete_results=False，分页完整=False，观察UTC 2026-11-18T18:40:47.176Z

</details>
