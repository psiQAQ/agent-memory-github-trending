# 触发来源、入口取证与 Receipt 恢复

本规范于2026-10-27经用户明确授权加入，适用于后续运行；不更改调度、权限或历史数据。入口取证解决“有什么记录、能证明什么”，平台未暴露的启动信息仍不能由提示词补造。

## 1. 在入口取证，随后读取固定版本

在首个 GitHub 动作前，先检查当前宿主是否实际提供 invocation envelope、任务/运行回执或当前运行的只读入口；用受支持的 automations.peek 私下查找原任务，按任务身份、唯一匹配及绑定核对，不能沿用旧任务 ID。查明 ID 后再 peek(jawbone_id=实际ID) 读取 run_details。不得为取证调用 run_now、创建/替换/暂停任务或改变绑定。

在目标包装器之外输出私有 trigger_entry，使用独立 capture_id 与实际 captured_at，保留以下真实字段或 null+原因：

- automation_id、platform_run_id、scheduled_for、started_at、trigger_kind；
- 当前宿主 invocation/run 引用、实际绑定线程/对话和与原任务绑定的核对；
- 获取工具及实际参数、回执/可回读引用、字段来源、缺口和冲突。

先记录再调用；不能把记录代码放在可能无法启动的包装器里充当外部记录。入口私有轨迹没有宿主持久化保证时须明确说明。进入 GitHub 阶段仍遵守所有外部 pre/post 和 API 计数规则；task lookup 不是 GitHub connector 动作，另列 scope，不能混入 GitHub 指标。

随后按当轮当前 HEAD/tree 固定版本，读取本文件和既有必读文件。所有后续输出引用同一 capture_id；不依赖跨包装器的 JS 局部状态或假定中断后内存仍在。

## 2. 什么能证明当前触发

必须先有当前 invocation 的独立平台记录，再将其真实 automation_id/platform_run_id、绑定、trigger_kind、scheduled_for/started_at 与任务运行回执精确关联。字段相同仅是结构上的必要条件，执行者还须核对来源确为平台、引用可访问；纯函数不能认证字段真伪。工具未暴露 trigger_kind 时不能从 schedule 推导。manual 也需要实际平台手动触发记录，不能由 unknown 的兜底标签推出。

peek 的 last_run 只是最近记录，未必属于当前 invocation；latest_result 可能更旧。分别比对 last_run.id、latest_result.run_id，以及 latest_result.created_at 是否早于该 run.started_at；发现旧结果只标 stale，不转给新轮。任务 last_run_time、enabled、午夜附近执行、提示词自称 Scheduled、run_id 后缀均不能独立证明当前触发。状态 in_progress 不证明当前存活，completed 不证明交付成功，交付未知应保留 unknown。

没有可匹配的当前 invocation 或 last_run 时 trigger_kind=unknown、verification_status=unverified；记录已有信息和缺口。不同 ID/绑定/时间是 conflicts，不通过改标签消除。不得把 null 历史解释为任务不存在或从未运行。

## 3. 与旧结构兼容并保护私有身份

旧 run_type 仍是 scheduled|interactive|interactive_baseline，历史值不改写。新记录另加 trigger_evidence，legacy_run_type 保留原标签，label_is_trigger_proof 固定 false；未核验来源的新轮为兼容可使用 interactive 标签，但必须明确“不是人工触发证明”。verified 的来源结论、API instrumentation_complete 和 Data/Receipt 回读分别验收，任何一项不能替代另外两项。

公开 trigger_evidence 的字段为 schema_version="1.0"、capture_id、captured_at、legacy_run_type、label_is_trigger_proof=false、trigger_kind=scheduled|manual|unknown、verification_status=verified|unverified、platform_lookup=available|missing|not_exposed、invocation_match=matched|unmatched|unknown、scheduled_for/started_at、time_scope、identity_presence、unknown_reasons、conflicts。time_scope 明确时间来自 platform_last_run_not_assumed_current 或 none，不能把最近记录时间当当前 invocation。只发布已允许公开的真实时间；未知为 null，不用 constructed_at/观察时间代替平台 started_at。身份存在不代表身份已匹配。

账户任务 ID、平台运行 ID、绑定线程/对话 ID、私有回执及其可逆替代值不入公开仓库。原值和绑定比较留在私有 trigger_entry；公开只保存存在性、比较结论及脱敏缺口，同 capture_id 关联。公开输出使用白名单，不能把整个 tool result、prompt、profile 或 invocation 原封不动附上。

入口记录在运行上下文保留，同 capture_id 的脱敏副本随正常 Receipt 的 run-evidence 归档；可在新 Snapshot/metrics 中附副本或引用，不改变最小指标原语义。bootstrap 前失败可能无法持久化，只能在允许的失败通知保留脱敏记录，不另开诊断提交。缺失旧入口不可追溯；后续查到资料只能新追加、有来源有补录时间，不能重写旧快照/索引/指标来追认 scheduled 或 manual。

## 4. 当前能力边界与最小可行方案

2026-10-27本次实际支持的 peek 已识别唯一原任务及其绑定；专用任务查询返回 last_run=null、latest_result=null、delivery_status=unknown。任务列表不是空，但运行明细不足以证明20261026T160515Z-interactive的触发来源。last_run_time 虽存在，不能代替当前运行记录。公开文档不保存账户级 ID。

最小可行方案是每轮入口立即捕获可取得的原始宿主记录、查询当前原任务、建立 capture_id 并在正常 Receipt 归档脱敏字段。若后续平台返回当前 invocation 与 run_details，则核对并记录可验证结论；如果仍不返回，继续 unknown/unverified 并报告实际缺口。完整解决仍依赖平台暴露可关联的每次启动记录，不能仅靠改提示词、时间或标签完成。未来自然 Scheduled 来源及全链路验收待实际记录与发布/回读通过后确认。

## 5. Receipt 写入中断后的恢复

先看[已核对事故](incidents/2026-10-27-receipt-interruption.md)。写调用无返回则 outcome=uncertain，不推定 started 或 not_executed。下次获授权恢复先只读核对：

1. 当前分支、原 run_id、Snapshot/index、Data commit 的 parent/tree 及每个 changed-path 实际 SHA；确认原 Data 是否已发布，历史是否保留。
2. 已收到真实 SHA 的 checkpoint/status/metrics/evidence 对象；若内容一致可复用。只有预计算 SHA 的待写对象须标 expected，不冒充 GitHub 返回。
3. Data 已发布且完整一致，只补独立 Receipt；不重采、不重发 Snapshot、不覆盖同 run_id 不同内容。并发变更按原协议协调一次，保留其他提交。
4. 只追加新 evidence segment，保留原失败/未知、原冻结指标和来源。遗失的完整账本/pre/post/时间/原因不能重构成“已认证”。
5. Receipt 自身发布/回读在实际执行后再报告，不能预写成功；提交前 pending 是事实快照，不因此制造另一轮诊断提交。

中断/超时不是权限拒绝；已见400/INVALID_ARGUMENT、401/403或权限/安全拒绝仍按原停止门禁处理，不换 URL、工具、路线或权限。幂等只读传输断连只可一次完全同参重试，写不确定不能照搬该规则。404仅说明对应观察时对象未解析到，不能解释更早中断的根因。

## 6. 控制重复体积与结构校验

包装器源文本存一次，其他段用可核对内容身份引用；大正文只留实际非秘密参数、UTF-8字节/可信指纹、返回对象和必要脱敏错误，不重复完整响应。不得因此省略每段外部 pre/post、唯一ID、实际开始/返回、写入参数或缺口。正常 Receipt 的冻结证据排除自身后续写/回读，不另加诊断发布轮次。精简成功不是已证明的大小限制修复。

[scripts/run_provenance.mjs](../scripts/run_provenance.mjs) 是无副作用的离线/交互式结构校验参考；[针对性测试](../tests/run_provenance.test.mjs) 使用合成数据。Scheduled 不运行仓库代码、不依赖 Node/本地文件系统。校验器始终 authenticated=false，返回 candidate_kind 仅是结构候选；把 synthetic 改写 actual 或 source 字段不能认证平台来源。
