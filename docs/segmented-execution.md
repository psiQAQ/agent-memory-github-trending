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
