# API-native 定时维护协议

本协议用于 ChatGPT Scheduled。目标是完全消除 Scheduled 对 connector→filesystem、Python、shell、git clone 和持久工作树的依赖。

## 运行时必须具备

- GitHub 只读：repo metadata、refs、commits、trees、files/blobs、releases/search 等。
- GitHub 已授权写入：create_blob、create_tree、create_commit、update_ref。
- 运行上下文可保存本轮结构化数据直到当前轮结束。

不要求 Python、本地文件、Code Interpreter、Work/Codex、Actions 或第二调度器。

## 完整性证明

1. 固定默认分支 HEAD 与其真实 tree SHA。
2. 优先读取 recursive tree，必须明确 `truncated=false`。
3. 用完整 tree 中所有 blob 的 path/mode/type/sha 调用 `create_tree`，不传 base tree。
4. 返回 SHA 必须等于 pinned root tree SHA。
5. validation-index 中历史 snapshot 集合必须与 tree 的 `data/snapshots/YYYY/MM/*.json` 集合完全相同，逐项 blob SHA 相同。
6. data/projects.json 中 tracked/reference card 必须全部存在。
7. 所有必读文件 fetch 返回的 blob SHA 必须与 pinned tree 一致。

任一步失败都停止发布。

## 新批次

- 对正式项目采集 metadata、default-branch HEAD、releases；按 maintenance.md 做 bounded discovery/deep review。
- 逐字段按 data-contract 校验。
- Scheduled 新 batch 使用 `events=[]`；实质技术变化写项目卡/报告并进入 pending_work。
- 生成 snapshot JSON 后调用 `create_blob`，记录返回 blob SHA。
- 基于旧 validation-index 仅追加该 snapshot 的 path/blob/run/time、Stars 摘要和 source coverage，调用 `create_blob`。
- 其他计划变更文件也分别 create_blob。

## 发布

发布前重读 HEAD；若移动则基于新 HEAD/tree 重做受影响校验，最多一次。

使用真实最新 tree SHA 作为 `base_tree_sha`，只替换 allowlist 路径；create_commit 的 parent 是同一个最新 HEAD；update_ref 必须 force=false。

发布后：
- fetch data commit；
- 重新读取完整 tree；
- 回读全部 changed paths；
- 每个实际 blob SHA 必须等于 create_blob 返回值；
- 新 snapshot/index 对账必须通过。

## Receipt

基于 data commit 的 tree 直接生成新的 checkpoints/status blob，只推进真正成功且分页完整的 source。单独 create_tree/create_commit/update_ref(force=false)，再回读 receipt commit 与 state blob（启用最小指标后还需回读同一 receipt 中的 run-metrics blob）。

## 最小运行指标与独立 Receipt

从本轮首次可观测 GitHub 工具调用开始建立逐调用计数账本，直到 Data commit/完整 tree/全部 changed paths 的回读验证完成；包括失败及重试，不包括连接器内部不可见的 HTTP 请求。每次跨执行片段都应显式合并计数；无法证明全覆盖时标记 `instrumentation_complete=false` 且 API 次数/失败率为 `null`，不得猜测。按 `docs/data-contract.md` 计算 metadata、HEAD、完整 Release 三类覆盖，以及至多 5 项深读完成率和 Data readback 路径数。

Data commit readback 全部通过后，冻结上述计数（`measurement_scope=bootstrap_through_data_readback`），生成 `state/run-metrics/YYYY/MM/<run_id>.json` 的完整 UTF-8 JSON，调用 `create_blob` 获取真实 SHA；`state/status.json.latest_run_metrics` 只保留最新指标副本加文件路径，首次启用为 `null`。将该指标 blob 与新的 checkpoints/status 两个 blob 放进**同一独立 Receipt tree/commit**；调用 `update_ref(force=false)`，再回读 Receipt commit、tree 和全部三个 blob SHA。指标文件只追加、同 run_id 冲突即停；不加入 snapshot validation-index，不伪造历史值。

Receipt create_blob/create_tree/create_commit/update_ref/回读在计数冻结之后，所以不算在本轮可证明的 API 调用次数内；它自己的回读结果也不得预标成功。若计数缺失仍可按现有验证门禁正常发布，但显式记录未知；任何 data-readback 失败必须先停止而不能为写指标绕过回执前置条件。

## 单句故障通知

执行中一旦出现需要用户处理的故障，先用一句中文报告首次失败环节、可核查原因和针对性的修复/核查办法，以及已验证 Data SHA（否则写“无”）：`故障环节：{环节}；原因：{原因/待核实}；解决办法：{可执行办法}；Data SHA：{SHA/无}。` 不把猜测写成事实，不自动修改/暂停日程；相同且无变化的故障按原去重约定处理。触发前平台故障和 bootstrap 前无法持久化的失败，不保证能写入本仓库。

## 恢复

写入结果不确定时先按 run_id 和 snapshot path 检查 main；已存在且内容/SHA一致则继续 receipt，不重复发布。存在同 run_id 不同 blob 时停止并报告冲突。

## 操作对照证据

执行 [数据契约的操作对照留证](data-contract.md#操作对照留证schema-10)：留存首次失败调用和所有实际写调用（含成功）的脱敏参数、内容身份、可见错误/ID、pre/post HEAD、可获得的上下文及 retry_of。未知字段为 null+原因，不引入本地执行依赖。冻结记录只随原本允许的正常 Receipt 追加到 state/run-evidence，并回读全部新增 evidence blob；不额外发布诊断批次。冻结后的 Receipt 动作不得预宣称成功，其失败在单句通知后附结构化证据；后续获准的正常恢复可追加有来源的 segment。无法持久化时同样附证据，这是单句通知的例外，不是绕过拒绝或扩大权限的理由。

必须同时执行数据契约“调用前记录与调用后结果”：包装器外先输出 pre_call（脱敏实际代码/可靠来源身份及有序子调用参数清单），再调用，最后在包装器外关联 post_call 和可观测逐子调用结果。计划不等于执行，无返回不等于未执行；动态参数须在实际子调用前补录。紧凑轨迹不是逐请求通知，不保证平台自动埋点或持久化；拒绝后不重试、拆分绕过或重启采集。完整字段、隐私、未知值与正常 Receipt 归档限制以数据契约为准。
