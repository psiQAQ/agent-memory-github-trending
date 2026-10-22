# API-native Scheduled 分段执行与完整留证（2026-10-22）

适用：唯一仓库 `psiQAQ/agent-memory-github-trending` 的每天北京时间 00:00 Scheduled。此为用户授权的交互式协议工程变更，不授予额外写入权限、调度器、费用或工具。原有 AGENTS、数据契约、三重门禁、Git tree/index 完整性、Data/Receipt 双提交与回读、候选/深读上限及通知规则仍适用。

## 1. 分段规模与状态传递

1. 禁止将 21 个仓库的完整抓取放入一次 `functions.exec`。**每个包装器最多包含 6 次 GitHub connector 调用；采集每批最多 2 个仓库**。GitHub 实际工具上限未知；如果 6 次仍有工具上限错误，下轮经正常修改协议后再调整，不能在同轮拒绝后拆分重试绕过。
2. 用三类微批：`metadata`（至多 2 个已知 repo URL）→ **在包装器之外**读取其真实 default_branch、登记结果 → `head+release`（至多 2 个仓库、至多 4 次 GitHub 调用，完整实际 URL 已确定）→ 必要时单独 `release-next-page` 批。全程串行，以便每个真实开始/返回均可对账。默认分支含斜杠时，Git ref URL 使用路径层级 `.../git/ref/heads/feat/server_team` 而不是 `feat%2Fserver_team`；如连接器不支持，则来源失败，不能伪造成功。
3. Release 采用 `per_page=30`，仅当页面条数小于 30 或与上一成功 release-id 水位存在真实重叠（并已覆盖所有较新页）才可标为增量 `complete=true`；否则继续按页采集并记录实际页码、范围和失败。首次建立基线不冒充已穷举全部历史。
4. 其他环节：bootstrap、必读文档、索引校验、discovery、最多 5 项深读、写 blob、data tree/commit/ref 和回读、receipt 都遵守 **每包装器 ≤6 次实际 GitHub 调用**。Tree 创建的一次参数可包含全部完整 blob 条目，它仍只算一次真实 connector 调用。超大返回只输出必要的规范化值和调用结果，不重复打印整页 Release。
5. 各微批的标准化 `observations`、release 分页状态、run_id、固定 HEAD/tree、操作计数和证据从工具响应返回到本次 Scheduled 上下文；不能依赖每次 `functions.exec` 的 V8 局部变量跨调用持续存在。跨批合并时按稳定 repository_id 校验恰好一个 observation、不可混用不同 pinned target tree；恢复未回执 Data 优先，不能重复采集覆盖已发 snapshot。不得把 orphan staging blob 视作已发布数据或回读成功。

## 2. 外部 pre_call / post_call：严格一一对应

每次 `functions.exec` 或其他包装器调用**之前**，先在包装器之外的可见运行轨迹输出一条脱敏结构化 `pre_call`（禁止只在将被调用的代码内部打印）。至少：
- `run_id, run_type, segment_id, wrapper_id, attempt_id, pre_call_id, emitted_at(UTC), phase`；
- `source_identity`：实际将发送的脱敏包装器源文本，或能访问且与实际文本一致的固定版本/可靠指纹；单独写“第 N 段”不合格。可安全保留时提供原始非秘密文本 byte_count/可验证身份；否则标 `null` 与原因，不能将脱敏文本指纹当原始指纹；
- 按调用顺序列明 `subcall_id, tool, exact_nonsecret_args, supplied-parameter flags, payload_identity, dependencies`，以及串行/并行关系。每个待定动态参数必须明确上游依赖；应优先拆为两段，让实际分支名、URL、SHA 在外部发出子调用之前已经确定；
- `intended_subcalls_count<=6` 和进入该段前的累计 `attempted/failed`（若尚可证明）。

在包装器内部，对每个真实 GitHub connector 动作：动作开始前形成 `started` 记录，真实返回或抛错后形成 `result`；返回至包装器外的摘要包含真实尝试 ID、URL/非秘密参数、成功与否、脱敏错误及可获得的 response SHA/ID 和源状态。**调用结束或被拒绝后**，在外部输出与原 `pre_call_id` 关联的 `post_call`，区分 intended、started、returned、explicit_not_executed、uncertain，连同包装器层的状态和可见错误；不得从“已计划”或“无返回”推断子调用结果。若包装器在外部 pre_call 之前没有合格清单，则停止该包装器并报告证据缺口；若拒绝，禁止为了取证在同轮改路由/拆分重试。所有输出不得泄露秘密、内部策略、账户任务 ID 或私有聊天全文。日常轨迹不是单独用户通知，归档仅随原本正常 Receipt。

## 3. API 完整计数：逐段守恒

从**第一项** GitHub connector 调用（包括 bootstrap、重试、完整性 create_tree）开始，到 **Data commit/完整 tree/全部 changed paths/snapshot-index 最后一项回读**为止，维护一个外部累计 ledger；直接 connector 调用也必须计数，不允许遗漏包装器之外的调用。每段：`attempted_delta = 实际已开始的 connector 调用数`，`failed_delta = 其中真实工具/HTTP 返回错误数`；失败与重试独立计数，包装器本身不是额外的 GitHub API 调用。保存 `cumulative_before/after` 和已返回/结果不明 ID 集合；`sum(segment attempted_delta)+direct_attempts = final attempted`，`sum(segment failed_delta)+direct_failures = final failed`，且每项实际 GitHub 动作恰有一个 started 与一个结果或明确结果不明标识。任何意外终止、丢失片段、模糊返回、缺少外部 pre/post 或无法证明首尾连续时，`instrumentation_complete=false` 且 `attempted/failed/failure_rate=null`，不能猜填。数据内容审查未通过不是 API 工具失败，内部 HTTP 次数不计。仅当证据无缺口、所有 attempted 有可核对结局，方可 `instrumentation_complete=true` 并计算 `failure_rate=failed/attempted`（分母 0 写 null）。
`source_coverage` 独立按 21 个预定项目的 metadata/head/release complete 计算；`deep_review.due` 是实际选定待深读项（≤5），completed 只计一手证据审查；`data_readback` 只在逐路径和 index 通过后标 passed。指标冻结点在 Data 最后回读之后、Receipt 写入之前。Receipt 写/回读不计入该 API 统计，但按证据契约留证并真实回读。

## 4. 下一次 Scheduled 验收

正常 Data/Receipt 发布前不得以“包装器在交互式任务曾成功”替代本次 Scheduled 证据。真正的完整验收需同时满足：
- 每个实际包装器都有**在外部可见且彼此关联**的 pre_call/post_call，所有真实子调用的 ID、非秘密参数与 started/result 齐全；
- 所有分段、直接 GitHub 调用计数闭合，`instrumentation_complete=true`、API attempted/failed 是可复核整数、failure_rate 由这两者得出；
- 完整 tree 和 validation-index 门禁、batch/source、授权写入范围均通过，Data commit 的所有变更路径和 snapshot/index 已逐一回读；
- 独立 Receipt 包含 checkpoints/status/run-metrics 和冻结时能保存的 run-evidence，逐一回读其 blob/commit/ref；不得预先声明 Receipt 自检成功；
- 更新 Scheduled 验收状态仅在**真实定时触发**且这些要求确实通过时。手动运行只记录 interactive，不替代 Scheduled。

如 telemetry 未达标但原有数据提交门禁允许正常发布，可用 `null` 指标真实发布并报告缺口，**不得声称“完整埋点验收通过”**。若 GitHub 读写被拒绝，按原协议停止，不因留证增加诊断提交或绕过拒绝。定时任务仍每天 Asia/Shanghai 00:00，且仅正常的重要变化/到期周报/新故障/真实验收需通知。

## 5. Discovery：使用专用仓库搜索工具

仓库发现必须先检查当前工具 schema，使用专用 `search_repositories`（当前连接器名 `mcp__codex_apps__github_search_repositories`；其他宿主按实际暴露的同义工具名），不要再把 `/search/repositories` URL 交给通用 `fetch`。文件搜索 `search` 和仅安装仓库搜索不是全局仓库发现的等价替代。实际参数对象为 `{"query":"\"coding agent memory\" in:name,description archived:false fork:false","page":1,"per_page":20}`；新项目通道在实际 query 中追加本轮明确的 created 日期条件。该接口未暴露 sort 参数时不传造出的 sort，记录 sort=null+原因；不同时传 per_page 与 topn。

本次交互式有界测试（2026-10-22T17:11:22.495Z 至 17:11:24.023Z）上述专用工具返回 isError=false、structuredContent.repositories 共20项。解析实际 `repositories` 数组，不假设 REST `items`；缺失数组是响应形状错误，不归一化成成功空列表。保存 query/page/per_page/tool、returned 与实际返回的分页/完整性字段；未提供 total_count/incomplete_results 则 null+原因，本次满页只说明已读第一页，不能认定搜索完整。每页记录实际query/page/per_page、returned_count、去重仓库ID、next_page_attempted或stop_reason及coverage。缺连接器明确保证时，短页也不能单独证明全量完成；有界搜索默认为partial/unknown而非完整生态覆盖。最多按既有预算分页，继续下一页前另留证；不扩大候选审查范围。

若专用工具在 Scheduled 不可用，discovery 标记 not_collected 并说明工具缺失；不退回已知不支持的 fetch URL、不换其他工具绕过拒绝，也不把未搜索当零结果。工具返回错误则保留脱敏原文及当前结果不确定项，按既有失败/partial规则处理；这不是允许在原失败轮继续重跑。只在全部原发布门禁允许时发布有明确缺失覆盖的 partial，不宣称生态完整。本修复不更改平台任务或时间，也未解决此前8项 Release 空列表异常。

## 6. 可执行的证据结构核对与真实轨迹复核

`scripts/operation_evidence.mjs` 导出纯函数 `validateOperationLedger`，无网络、文件、凭据或工具副作用；`tests/operation_evidence.test.mjs` 是合成回归。它们是离线/交互式参考，不新增 Scheduled 执行仓库代码或 Node 的依赖。Scheduled 必须在运行上下文逐条落实相同核对，不能把文件存在当作已自动埋点。

标准化 ledger 输入：evidence_origin=actual|synthetic、run_id/run_type、scope=bootstrap_through_data_readback、first_call_id/data_readback_call_id、first_call_ref/data_readback_ref（必须分别匹配首末实际调用的ID和response_ref）、attempted/failed、segments。每个 segment 含唯一 id、pre/post：
- pre：pre_call_id、external_trace_ref、trace_order、emitted_at（未知null并有unknown_reasons）、source_text 或 source_ref+source_fingerprint、source_representation、before_attempted/before_failed、calls[{id,tool,args}]。args 是实际精确非秘密参数（包含完整 URL 或 query 对象），不是事后概括；大载荷按数据契约保留身份和来源。source_text 是实际脱敏代码全文；任何指纹必须注明算法、表示和来源，不把脱敏哈希当原请求哈希。
- post：同 pre_call_id、external_trace_ref、trace_order、wrapper_state、after_attempted/after_failed、calls[{id,tool,args,state,dispatch_at,returned_at,trace_order,evidence_origin,clock_source,isError,response_ref,error_text,request_id,decision_id,unknown_reasons}]。直接 connector 动作也归一为一个单调用 segment，避免漏计。
- dispatch_at 在真实 await 工具调用紧前用可用时钟取得，returned_at 在返回/抛错后立即取得，明确 clock_source 和这只是客户端观察时间、不是服务端受理时间。外部 pre/post 的实际发出时间如宿主不暴露，emitted_at=null+原因，构造时间另记 constructed_at；以可查外部事件引用/顺序证明 pre 早于包装器、post 晚于返回，不能用构造时间冒充发出时间。缺 dispatch/return 时间仍是留证缺口，不因 emitted_at 允许未知而放宽。
- 先检查实际响应 isError 与可见错误，不能仅凭 Promise resolve 写 success。异常抛出且无法确认是否执行时标 uncertain；包装器拒绝不推出内部每项未执行。明确 not_executed 只用于有证据未真正发起的计划项，不计 attempted；已调用连接器而收到422/400仍是 attempted+failed，不因服务端未处理业务操作而从调用计数中删除。
- 先输出外部 pre，再调用；收到结果后立即输出外部 post，随后核对再进入下一段。内部日志不替代外部记录。全局唯一 ID、串行 trace_order、参数一致、≤6调用、逐段/最终累计必须闭合。结果不明、缺段、漏bootstrap或混入Receipt/测试调用时正式三指标null、instrumentation_complete=false；可另报告有依据的局部observed_counts并写清范围。

校验器始终返回 authenticated=false；即便人工把合成标签改成actual也不会变成真实证据。valid 仅表示提供的数据结构一致，candidate_counts 不是正式指标或执行真实性证明；synthetic 永不返回真实计数。必须独立核对引用确实可访问、源码/参数与实际调用相同、全程第一项至Data最后回读无遗漏，且Data回读门禁已经通过，才可将实际候选数用于正式指标。无法证明时保留所有缺口/null，不能填造trace_order、引用、时间或ID来使校验通过。该校验不代替隐私审查、载荷字节/指纹核验、Git树/index或发布门禁，也不证明每次未来Scheduled都会遵守。

可用的外部发出时间还须满足 pre≤dispatch、return≤post；所有事件 trace_order 不重复。not_executed 也必须核对 tool/args/结果引用/事件序号/ID缺失原因，且有 explicit_not_dispatched 或 cancelled_before_dispatch 类型的非执行证据；不能因该分支跳过身份验证。每项 evidence_origin 与全局一致，clock_source=client_observed_utc；标签本身不保证真实性。

合成测试可在单独授权的工程环境通过导入 `runEvidenceTests()` 运行；本次实际在内存V8执行相同函数体和测试，无clone、无整轮采集、无故意安全拒绝。测试覆盖缺外部pre、未知真实时间、uncertain/拒绝、假成功、实际错误计数、包装器误计数、参数漂移、缺源码、乱序、重复ID、空/错误scope、无证据未执行及缺ID原因。测试及本次单查询成功不构成Scheduled验收。

参考 ledger 采用串行调用：每项 trace_order 表示该调用结果事件，实际调用清单顺序必须与结果事件递增顺序一致，下一项 dispatch_at 不早于前项 returned_at；首项开始和末项返回构成本文 scope 的两端。并行调用不能冒充此串行结构通过校验，若宿主无法取得这些字段，保留不完整和未知指标，而非补造次序。
