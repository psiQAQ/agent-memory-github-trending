# 数据契约 1.0

本文件与 `AGENTS.md`、`docs/api-native-maintenance.md` 共同定义 Scheduled runtime 的规范。`scripts/tracker.py` / `scripts/manifest_validation.py` 仅为离线参考实现，Scheduled 运行时不依赖它们。

所有 JSON 使用 UTF-8，UTC 时间以 Z 结尾；未知值用 null，不能用 0 或空列表伪装成功。先查项目和批次格式，再区分 API-native 运行限制与离线实现的接口。

## 项目登记

`data/projects.json` 包含 schema_version 和 projects。正式条目的字段为：repository_id（稳定整数）、full_name、status、kind、tags、first_discovered_at、created_at、first_public_at、summary、source_url、source_version_or_sha、evidence_level、implementation_evidence、card。

status 可为 tracked/reference/watchlist/candidate/retired；kind 为 engineering/research/benchmark/reference。未审查线索另存于 candidates.json；不能根据名称推断实现质量。

## 观测批次

每轮在运行上下文中构造 batch 对象，参考仓库已有快照的实际结构；无需本地文件。顶层必填：

```text
schema_version = "1.0"
run_id = YYYYMMDDTHHMMSSZ-scheduled（同一轮重试复用，不重新造 ID）
run_type = scheduled | interactive | interactive_baseline
observed_at = 批次完成 UTC 时间
base_commit_sha = 本轮读取的目标仓库 HEAD
expected_repository_ids = 本轮预定覆盖的 ID 数组
observations = 每个预定 ID 恰好一个对象
discovery = 实际查询日志（无搜索时空数组，同时解释原因）
events = 已核实实质变化（无变化时空数组）
```

每个 observation 包含 repository_id、full_name，以及 metadata/head/releases 三个 source 对象。source 对象统一包含 status（ok/error/not_collected）、observed_at、source_url、value。失败或未采集必须 value=null 并给 reason，不遗漏对象。source_url 必须是对应上游仓库的实际 GitHub API URL。

- metadata.value：stars、forks 为非负整数；archived 为布尔；default_branch；created_at；pushed_at（未知可 null）；license_spdx（未知可 null）。
- head.value：完整 40 位 commit SHA。
- releases.value：列表，每项含 id、tag、published_at、url。releases.status=ok 时，必须提供 complete 布尔值，说明是否完成本轮所需分页范围。成功取得空列表与没有采集是不同状态。

初期读 `GET /repos/{owner}/{repo}`、`GET /repos/{owner}/{repo}/git/ref/heads/{default_branch}` 和 `GET /repos/{owner}/{repo}/releases?per_page=30&page=1`，按需要继续分页。记录 GitHub 连接器实际返回，不用 get_repo 的精简包装冒充完整计数。通过 README/代码差异/相关 PR 做技术解读；不在快照里保存个人 profile、权限或完整长 README。

## 事件与发现

事件必填 repository_id、type、claim、source_url、source_version_or_sha、event_at、observed_at、evidence_level、event_id。用脚本 event_id(event) 计算稳定键。第一次看到过去事件不等于刚发生；同源同版本的多次报道不重复。改写旧结论需新 source_version_or_sha 并附 supersedes。事件保存在不可变快照内，不另外复制一份相同原始内容。

每条 discovery 包含 query、page、returned、sort、observed_at、incomplete_results、pagination_complete。候选队列记录来源、稳定 ID 和审查状态。

连接器未返回 total_count/incomplete_results 时，保留未知值，不能猜测。

## API-native Scheduled 限制

Routine Scheduled 不依赖 Python 或本地文件系统。新 snapshot 的完整 UTF-8 JSON 直接提交给 GitHub `create_blob`，GitHub 返回的 blob SHA 作为 validation-index 与发布 readback 的权威身份。

为避免在没有本地 cryptographic helper 时伪造 legacy `event_id()`，API-native scheduled batch 对**新发现**固定写 `events=[]`。核实的重要技术变化仍可：

- 更新对应 `projects/*.md`；
- 更新 `reports/latest.md` 或到期周报；
- 在 `state/status.json.pending_work` 记录 structured-event backfill 待办，包含 repository_id、type、source_url、source_version_or_sha、claim、event_at/observed_at/evidence_level。

后续交互式工程运行可用离线脚本计算 legacy event_id 并以新 snapshot 形式回填，不修改旧 snapshot。普通 Scheduled 不得自行编造 24 位 event_id。

`state/validation-index.json` 仍保存 snapshot path/blob SHA、run_id、observed_at、成功 metadata 的 Stars 紧凑历史、source 成功覆盖数和既有 event ID 集。新增 snapshot 时只追加一条摘要并保留全部旧项原样；其 snapshot blob SHA 必须来自本轮 `create_blob` 的实际返回。

## 执行输出

以下为离线参考实现的输出约定：

- prepare：输出本轮待提交路径和到期周报列表，不调用 GitHub。
- render：输出当前 Markdown。
- receipt：在真实 GitHub 提交完成且回读比对之后运行，生成逐来源成功游标。不能仅因自行填入两个相同 SHA 就声称验证通过。

`reports/current.md` 的“fresh”只表示本轮得到新元数据，不代表其余来源全量覆盖。缺失增长显示“—”；具体区间由 growth() 返回。每轮应在简报或状态说明释放/PR/深读的实际覆盖范围。


## Manifest 校验模式

`validate-batch` 只验证本轮 batch 与项目登记契约，不依赖历史工作树。它必须在任何 prepare/index 更新之前执行。

临时 `manifest.json` 不入库，字段为 `schema_version`、`repository`、`base_commit_sha`、`base_tree_sha`、`truncated`、`entry_count`、`entries`。entries 覆盖完整 tree；当前只接受普通 `100644 blob` 和 `040000 tree`。校验器用 Git tree 序列化规则重算每个子树和根 SHA，因此 manifest 不能靠路径列表伪造完整性。

`state/validation-index.json` 是已验证历史的紧凑索引。每个 snapshot 条目固定 `path`、`blob_sha`、`run_id`、`observed_at`、成功 metadata 的 `[repository_id, observed_at, Stars]` 紧凑序列、三个 source 的成功覆盖计数及 event_id 列表；events 只保存全局稳定 event_id 集合。新 batch 若再次提交已经存在的 event_id 会失败，纠错必须按既有契约使用新的 source identity 与 supersedes。完整历史仍保存在只追加的 snapshot blob 中，index 不能替代它。只有 index 的路径集合和 blob SHA 与完整 Git tree 完全一致时，索引才有效。

manifest-aware prepare 新增 snapshot 后必须同时更新 validation index；manifest-aware receipt 则在发布后用新的完整 tree + index 验证该 snapshot 的实际 blob SHA，再生成 checkpoints。index 缺失/冲突时必须停止或走完整工作树 fallback，不能自动根据未验证内容重新生成。


## 每轮最小运行指标（API-native，schema 1.0）

历史文件采用只追加路径 `state/run-metrics/YYYY/MM/<run_id>.json`；同一 `run_id` 若内容 SHA 相同则幂等，否则停止，不覆盖。只有 Data commit 发布并且**全部变更路径与 snapshot/index 回读完成**后，才允许在独立 Receipt commit 中新建该指标文件。该文件不是 snapshot，不纳入 `state/validation-index.json` 的 snapshot 路径集合，也不修改既有历史快照。只保存用户要求的最小指标；`state/status.json.latest_run_metrics` 保留与历史记录一致的最新指标摘要和 `path`，不得追加历次列表。首次启用前设为 `null`，不回填未知的旧 API 调用数。

指标文件使用 JSON，时间为 UTC Z；比例取值 0–1，以小数表示，不加百分号。字段如下：

- `schema_version="1.0"`；`run_id` 与新 snapshot 相同；`run_type` 与 batch 相同；`measured_at` 为指标冻结 UTC 时间；`data_commit_sha` 为**已经回读验证**的 40 位 Data SHA；`measurement_scope="bootstrap_through_data_readback"`。
- `api`：`unit="observable_github_connector_invocations"`、`instrumentation_complete` 布尔、`attempted` / `failed` 非负整数或 `null`、`failure_rate` 数值或 `null`。从本轮首次 GitHub 连接器动作至 Data commit 最后一项回读（含）逐调用计数，重试每次另计；实际工具/HTTP 错误计失败，数据内容未通过研究审查不是 API 失败。调用由多片段发起时必须汇总，不能将模型调用、内部 HTTP 数、GitHub rate-limit 数冒充工具调用数。`instrumentation_complete=false` 时这三个数一律 `null`，不得填入不完整估计。计数截止后新增指标/Receipt blob、tree、commit、ref、回读不在本轮统计范围。
- `source_coverage`：`metadata`、`head`、`releases` 均含 `expected`、`ok`、`rate`；分母为预定项目总数，只有 metadata/head 的 `status=ok`、Release 的 `status=ok && complete=true` 才计入分子。来源失败/未采集仍进入分母，已成功重试的来源计成功。不得把三类来源的覆盖率等同于整个 GitHub 生态覆盖。
- `deep_review`：`due`、`completed`、`rate`；`due` 为本轮在待办/新差异中去重选择且**实际需要深读**的数量，最大 5；`completed` 只计查阅一手代码/相关 PR 或正式版本并记录证据的实际完成项。仅 HEAD 变化、compare 元信息或搜索命中不算完成。
- `data_readback`：`status="passed"`、`expected_paths`、`verified_paths`；仅 Git commit parent/tree、每个 changed-path blob SHA、snapshot/index 对账均通过才可标记 `passed`，并要求 `verified_paths == expected_paths`。若失败，禁止生成 Receipt/成功指标记录，按已有恢复协议保留不确定状态。

上述比例的统一公式为 `numerator/denominator`，分母为 0/未知时用 `null`；绝不写空值为 0 或将部分覆盖冒充 100%。写入 Receipt 前验证指标内容、run_id/data SHA、单个历史路径及 `status.latest_run_metrics` 一致性；Receipt 发布后回读 checkpoints、status、metrics 三份真实 blob 与 commit。Receipt **自身**的回读结果只在真实核验结束后报告或在后续恢复轮更新，不能预先写入自身即将验证成功。

## 操作对照留证（schema 1.0）

本节用于比较 Scheduled 与 interactive 的真实同类调用。任务协议、助手总结或提交父节点都不能充当实际请求参数。

留证不增加权限，不改变调度、发布门禁、失败恢复或最小指标计数范围，也不能用来追溯编造历史错误。

从本轮首次 GitHub 调用开始，在运行上下文保留：**首次失败调用**（读或写）和本轮所有实际写调用的成功/失败结果，包括完整性证明用的 create_tree、create_blob、create_commit、update_ref。每次重试单独记录；没有失败时 first_failure_attempt_id=null。正常无变化轮次仍沿用静默通知规则，不为留证制造测试写入。

每条记录至少包含以下字段。未知值为 null，并在 unknown_reasons 中逐字段说明缺失原因：

- identity：schema_version、run_id、run_type、attempt_id（本轮顺序号）、started_at/finished_at（UTC Z）、phase、tool。
- request：repository、branch/ref、force、expected_sha_present（实际是否传入）、expected_sha、target_sha、base_tree_sha、parent_sha；只记录实际发出的适用参数，不能由规则或返回值反推。保留脱敏后的必要其他参数，禁止复制整个长内容。
- content_identity：blob UTF-8 byte_count、fingerprint_algorithm/fingerprint、fingerprint_source。create_blob 成功时用实际返回的 Git blob SHA；失败前若已有可靠内容指纹则保留其来源。无可用计算能力时写 null+原因，不新增 Python/本地文件依赖，不用字符数冒充字节数或伪造哈希。不同请求用相同指纹必须有真实证据。
- observation：pre_head_sha/post_head_sha 及各自 observed_at、returned_blob/tree/commit_sha、visible_success、execution_outcome（executed / not_executed / uncertain）、denied（true/false/null）、verified_outcome 与 readback_refs。拒绝只有明确未执行证据时才填 not_executed；缺少返回或回读不能宣称成功。ref 写入前读取 HEAD，失败或不确定后仅在允许的只读工具可用时核对，不能由“计划没改”推断 main 未变。
- error：脱敏后原样保留可见的 error_text、error_code、http_status、request_id、decision_id、reported_layer；工具未提供则 null。区分平台拒绝、GitHub HTTP 错误和未知来源；仅凭“安全拦截”的转述不能指定具体层或根因。
- context：实际可获得的已保存任务提示词版本/公开仓库协议 commit、用户授权证据引用、工具/客户端版本与可用工具差异；缺失写 null+原因。仅记录获准公开的版本与非敏感引用，不保存聊天全文、账户级任务ID、内部策略/推理、隐藏提示词、凭据或令牌；完整私有证据仅向用户展示。
- retry_of（原 attempt_id/run_id 或 null）、retry_kind（none / exact_request_retry / new_batch / receipt_recovery / reconciled_retry）、changed_fields。只有实际参数与内容身份可核对时才能标 exact_request_retry；新批次或人工补回执不得当成同一请求的受控对照。

留证采用追加文件 state/run-evidence/YYYY/MM/<run_id>/<segment_id>.json，包含 schema_version、run_id、run_type、segment_id、captured_through、first_failure_attempt_id、records、unknown_reasons、source_refs。segment_id 使用实际冻结 UTC 时间和本轮顺序号；同路径同 blob 幂等，不同内容停止，不覆盖旧记录。它不属于 snapshot，不加入 validation-index。

**不增加诊断专用发布轮次。** 仅在原本允许的正常独立 Receipt 中附带冻结的脱敏记录，并逐一回读所有新增 evidence blob；仍须先通过 Data 全部回读。先准备其他 Receipt blobs，再冻结 evidence、创建其 blob/tree/commit/ref，因此不能在文件里预先记录它自己的写入或后续 Receipt 已成功。冻结之后的失败必须通过下面的通知保留；后续正常授权的恢复/维护 Receipt 可按原 run_id 新增 segment，标明原始来源和补录时间，不猜测缺失字段。不修改既有三份 metrics/checkpoints/status 的语义或计数范围。

若失败阻止安全持久化，不为写日志绕过拒绝、完整性门禁或另开写入路线：故障通知保留一行结论，并追加首次失败的脱敏结构化记录及相关最近成功写调用的对照记录（可附文件；附件失败则用可复制文本）。这部分证据是“仅一句通知”的明确例外；未知字段必须保留，不用笼统建议替代错误证据。原始可见错误中的秘密、个人信息、内部策略文字必须先移除并标记已脱敏。

出现拒绝后不因留证自动重试或更换路线；遵守宿主授权/安全要求。执行结果 uncertain 时先只读对账。同类操作成功只能支持“此调用成功”，不能证明此前拒绝的根因或 Scheduled 已修复。

### 调用前记录与调用后结果

这是执行者必须遵循的留证规则，不代表平台已安装自动埋点或开放内部判定日志。对每个实际工具调用，尤其 functions.exec 等批量包装器，采用关联的 pre_call / post_call 记录；普通成功只读子调用可用紧凑清单，不复制响应正文。

- **先留证，再调用。** 在调用包装器之前，在该包装器之外先输出脱敏、机器可读的 pre_call 到本轮可见运行轨迹/任务输出；不能只把日志代码放进待调用的 exec，因为包装器被拒绝时它可能根本不运行。记录 emitted_at、run_id/run_type、segment_id、attempt_id 和唯一 pre_call_id；每个子调用用唯一 subcall_id 关联。attempt_id 标识包装器尝试，子调用也保留自身可观测尝试身份，不把计划项计为实际 API 调用。此前已发生而无法取得的 bootstrap 记录写 null+原因，不倒填。
- pre_call 保存实际待发包装器的脱敏代码，或足以核对该代码的 source_identity（可访问的固定版本引用及版本/内容指纹，不接受仅写“第二批采集”）。按计划顺序给出 subcalls：subcall_id、tool、exact_nonsecret_args、参数是否传入、payload_identity，以及串行/并行/条件依赖。清单明确是 intended，不是 started；并行清单序号不是实际开始顺序。非秘密参数保留精确值，大载荷以可靠身份引用代替正文；动态参数尚不可知时显式记录依赖引用及 null+原因，仅在真实值可获得后、真正发出该子调用前追加 resolved_pre_call，不以模板冒充实际参数；内部补录不能替代包装器外的初始记录。已明确标注的合法未解析依赖本身不阻止包装器，也不阻止建立基线所需的正常元数据读取。若缺少本应可记录的包装器外必要清单或来源，记录证据缺口并停止该包装器，不原样重跑或为取证重启采集。
- source_identity / payload_identity 均注明 byte_count、fingerprint_algorithm/value、provenance、representation（original_nonsecret / redacted / returned_git_blob）及与实际载荷的关系。只对可安全保留的非秘密内容计算身份；不得存储或散列凭据、令牌及其他秘密，也不得保存隐藏指令、安全判定内部文字。脱敏文本的指纹不是原始请求指纹；无法证明原始字节身份就写 null+原因。Git blob SHA 与普通内容哈希明确区分，不用字符数冒充 UTF-8 字节数，不为算哈希引入本地执行依赖。
- 实际调用前可观测的 started 事件、每个子调用返回后立即可观测的 result 事件，均引用 pre_call_id / subcall_id，记录可获得的 started_at/returned_at、success/error、返回对象身份和脱敏原始可见错误及 code/request_id/decision_id。包装器结束或拒绝后，在包装器之外输出 post_call，关联同一 attempt_id，汇总真实已开始/已返回/明确未执行/结果不明的子调用及包装器本身的结果；未知时间和 ID 为 null+逐字段原因，不能用最终通知时间替代错误发生时间。仅有预调用记录或“准备开始”标记不证明调用已执行；没有返回也不等于没有执行。包装器拒绝不能自动推断每个子调用都未执行，需按可见证据分别判定，其他保留 uncertain。
- 运行轨迹中的记录按片段紧凑输出，属于诊断证据而非逐请求用户进度通知；保留现有通知去重/静默规则。记录输出引用和是否可回读，不能保证轨迹持久性或声称不可访问的记录已归档。失败通知附紧凑的 pre/post 关联、失败及结果不明项、相关成功对照和可访问的完整清单引用；无可访问引用时附必要脱敏清单，不只重复空字段总结。不能安全输出时报告留证阻碍，不把秘密塞进通知。
- 只有原本允许的正常 Receipt 才可归档这些前后记录，继续遵守冻结、自引用排除与逐 blob 回读规则；不得专为日志新建发布或提交。拒绝后停止相关动作，不重试该拒绝、不拆分或改路由绕过，也不重新开始采集。结果不明先做获准的只读对账；任何后续恢复仍受既有授权和安全门禁约束。

## 触发来源扩展（向后兼容，2026-10-27）

原 schema_version=1.0 与 run_type 枚举保持兼容，不修改历史文件。新 batch 可增加 trigger_evidence，正常 Receipt 的 run-evidence 必须保存同一入口 capture_id 的脱敏副本；metrics 可带该对象或引用，最小指标原语义不变。无字段的旧文件表示未记录，不默认 manual/scheduled。新增字段详见 [run-provenance.md](run-provenance.md)：schema_version、capture_id、captured_at、legacy_run_type、label_is_trigger_proof=false、trigger_kind=scheduled|manual|unknown、verification_status=verified|unverified、platform_lookup、invocation_match、scheduled_for、started_at、identity_presence、unknown_reasons/conflicts；时间未知为 null，不按观察时刻倒填。

verification_status=verified 需要独立平台启动记录与当前 invocation/绑定的真实关联，不能由字段自称、纯函数返回或旧 run_type 推导；不满足则 trigger_kind=unknown。未知时为兼容保留 run_type=interactive，仅是 legacy 执行标签，不能宣称人工触发。验证来源不等于完整 API 埋点或 Data/Receipt 验收；三者分别报告。账户任务/运行/线程 ID、私有回执及其可逆替代值不得出现在公开 JSON，身份核对在私有侧完成，只发布存在性和核对结论/缺口。

只读 task lookup 不计 GitHub connector API 指标；每个实际 GitHub 动作仍按原范围计数。补录历史来源仅可在新追加证据中列明原始来源和补录时间，不能改写旧 Snapshot/index/metrics 或猜补不可追溯字段。
