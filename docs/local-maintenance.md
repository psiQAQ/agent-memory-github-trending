# 本地 Git 维护协议

用户于 2026-10-27 明确授权把日常维护迁移到自己的 Windows 电脑，保留每天北京时间 00:00，并要求先验证本地、再由协调会话停用云端。本文件是该工程迁移的独立执行配置，不表示定时任务已创建、已启用或无人值守验收通过。

现有 [API-native 协议](api-native-maintenance.md)和[旧定时提示词](scheduled-task-prompt.md)保留。只有 `config/local-runtime.json.cutover_state=active`、`config/tracker.json.settings.runtime_mode=local_git` 且协调会话已核对唯一运行者时，本协议才替代其运行时专属步骤。三个既有批准门禁保持原值且每轮检查。准备状态下仅允许迁移工程的离线/只读检查；不得据本文件开始日常采集或发布。

## 1. 原生调度和两阶段切换

采用桌面端原生 Codex 本地定时任务，固定同一项目目录，在现有 Windows 用户环境运行。无 Windows Task Scheduler、自制服务、CLI 后台循环或第二云端任务。平台的暂停/启用、时区、绑定目录、下一次触发时间都以真实工具/UI 回读为准，不直接写自动化 TOML、数据库或内部状态。

1. 检查既有本地任务，避免重复；创建本地任务时先暂停。保存的正式提示词见 [local-scheduled-task-prompt.md](local-scheduled-task-prompt.md)，先只配置 dry-run 入口。
2. 验证主机/目录、干净工作区、Git 身份、现有认证、远端、依赖、离线测试和本次工程文件的非强制推送/回读。交互式提权后的成功不证明无人值守可用：须在任务实际权限下验证 `.git` 写入、联网和已有凭据访问，不能自行改变安全设置。
3. 协调会话确认本地配置可回读且任务权限满足后，暂停原云端任务并确认没有正在执行/待恢复的云端写入。保留原任务及历史；不删除。无法证实没有并发写入时停止切换。
4. 协调会话以单独工程提交把上述两个 runtime 选择字段改为 active/local_git，并回读；不更改三个批准门禁。随后更新同一已暂停本地任务为正式提示词，核对每天 Asia/Shanghai 00:00 后启用。启用失败时保持本地停用，由协调者处理恢复，不允许两边同时活动。
5. 第一次真实自然触发按来源、覆盖、Data 与 Receipt 回读分别验收。手动 Run now、配置成功、工程推送和离线测试都不算 Scheduled E2E。

电脑关机、休眠、退出应用或网络断开时不能保证准时运行，也不承诺补跑。应保持电脑开机、可联网且桌面应用运行；不擅自修改电源策略。若系统时区不再是北京时间，停止并核对原生任务的实际时区/下一次时间，不改变系统设置。

## 已验证的原生执行方式

2026-10-29 的一次原生后台固定入口验收通过：普通用户、非管理员令牌、既有认证、公开仓库读取及一个无分支引用的 Git 对象写入和回读均成功，13 个子调用返回 0。该轮实际采用 `on-request` 与 `auto_review`，通过一次 `exec_command` 的 `sandbox_permissions="require_escalated"` 请求执行。它证明该轮后台能力；实际后台 push、自然定时触发以及自然定时 Data/Receipt 全链路仍待实际执行验收。

正式维护只对本协议已授权、确需访问本用户既有凭据/网络或受保护 Git 路径的具体操作请求该执行方式。调用前说明目标仓库、路径、操作和读写范围；每次由平台规则或审批决定。普通工作区读取和文件生成仍用默认执行方式。此方式不扩大例行写入目录、研究范围或发布权限，不新增通用 Python/Git/Shell allow 规则，不修改凭据、管理员权限、代理变量、网络或审批配置。固定验收入口只用于能力检查，不承担日常采集或发布。

当轮工具契约不允许 `require_escalated`、平台拒绝或操作失败时，停止该动作并报告，不换路径、不删除代理变量、不自行修改权限或重试来绕过拒绝。日程启用不改变工具契约；后续实际权限与本次不同，按当轮可见策略处理。首次自然触发后分别核对来源、源覆盖、Data 回读与 Receipt 回读，不能沿用本次成功作为自然定时验收。

入口必须能通过默认执行在项目内已忽略的 `.cache` 创建本轮目录，并获取、读回下述真实独占锁。`WinError 5` 是该动作的本地访问失败；`orchestrator_helper_incomplete` 发生在命令进程创建前，不能当作 GitHub、Git 或认证失败。保留首次阶段、精确动作、可见错误和原 `run_id`，停止受影响动作；例行任务不自行修改 ACL、换缓存目录或换工具绕过。用户另行修复或重启后，先核对原写者已停止、唯一写者、已发布 Data/Receipt 和留存来源，再依原 `run_id` 恢复；单次恢复成功不证明永久修复或自然 Scheduled 验收通过。

## 2. 入口、锁与固定版本

先按 [run-provenance.md](run-provenance.md)记录宿主提供的启动来源，用受支持的本地任务读取/运行回执与当前 invocation 核对。云端 peek 不能认证本地任务；缺少原生启动字段时仍是 unknown/unverified，不能从文件名、时钟、提示词或本地 TOML 推断。身份和平台回执留在私有轨迹，公开文件只保留白名单摘要。

所有本地轮次使用同一根目录，不自行另建 worktree 绕开互斥锁。运行 ID 在入口生成一次，重试/恢复复用。调用：

```powershell
python scripts/local_maintenance.py acquire --run-id <run_id>
```

该工具以独占创建 `.cache/local-maintenance.lock` 防止第二个本地写者；返回的 owner_token 与运行日志留在忽略目录。锁存在即停止，不根据年龄自动删锁。中断后先核对原 run_id、原进程/平台运行状态与远端 Data/Receipt，再由拥有该锁的恢复者或协调者释放；不能在无法确认原写者已停止时接管。此锁不能阻止云端，云端停用门禁不可省略。

`git status --porcelain=v1 --untracked-files=all` 必须为空；否则保留用户改动并停止，不 stash、reset、clean 或自动提交用户工作。核对 origin fetch/push 均是本仓库，默认分支须解析为 main，不凭旧记录假定。只用现有 Git 身份和凭据，不打印令牌、不新增持久凭据。可在当前 Git 子进程设置 GIT_TERMINAL_PROMPT=0；本机 SSH 如需 SHELL，仅用当前进程的 Git Bash 路径，不修改全局 SSH/代理。

从 `git ls-remote --symref origin HEAD` 取得真实默认分支/HEAD，`git fetch --no-tags origin main` 后仅在干净、无分叉时 `git merge --ff-only origin/main`。固定完整 commit SHA；`git ls-tree -r -t -l -z` 枚举其完整树，`git cat-file blob <sha>` 读取固定 blob。本地模式用 Git 序列化规则重算全部子树和根树 SHA 替代 API-native 的服务器端 orphan create_tree；所有必读文件、每个快照/索引 SHA 和项目卡仍严格验证。

```powershell
python scripts/local_maintenance.py preflight --remote-head <fresh_remote_sha> --active
```

`inspect --commit <sha>` 是可在准备阶段运行的离线检查；preflight 的 remote SHA 必须来自刚完成的网络回执，参数本身不认证远端。必读文件同 AGENTS.md，并包括本地两份文档、配置、run-provenance、segmented-execution。Python 3.10+、Git、GitHub CLI（现有登录）须可用；时区数据库必须能解析 Asia/Shanghai。不得自动安装依赖或执行上游仓库代码。

## 3. 来源、研究与计数

研究要求、21 个当前预定来源、完整 Release 增量分页、最多 10 新候选和 5 深读、总池不超 50、读者格式与历史保存完全继承既有协议；预期项目集合按当轮登记实际确定，不永久写死 21。先恢复未回执 Data，后采集。初见旧 Release 只建基线。

本地 profile 明确授权 `gh api` 读取公开 GitHub REST：元数据、固定 HEAD/tree/blob、Release/PR/compare 和专用 `/search/repositories` endpoint。它是本地方案的正式传输方式，不是被拒绝后的替代路线；若收到权限/安全拒绝，停止该动作，不能换连接器绕过。发现调用使用 `gh api --method GET search/repositories` 的 q/page/per_page 及实际 sort 参数，保留真实 items、total_count、incomplete_results、Link/页码/停止原因。逐页操作便于核对；有限页数不等于普查。连接器若用于发现则仍使用当前专用 search_repositories schema。失败或工具缺失不是零结果。

每段最多 6 个实际 GitHub CLI/connector 网络调用、最多 2 个项目；调用前在包装器外留脱敏 source identity 与有序参数清单，之后外部关联真实结果。命令、stdout/stderr 的必要字段、UTC 时间、返回码、commit/tree/blob 身份及重试关联保存在忽略的本轮目录；不得记录秘密或完整私有启动回执。脚本测试不是来源采集。

`api.unit=observable_github_connector_invocations` 保留原含义，不能把 gh/git 次数混入。全程改用 CLI 时，原 api 三项设 null、instrumentation_complete=false，并注明 connector 口径不适用；不追填历史。新指标可增加 `local_transport`，unit=`observable_gh_and_git_network_invocations`，同样从首次目标 GitHub 网络动作累计到 Data 全量回读，字段 attempted/failed/failure_rate/instrumentation_complete；单个可见 gh/git 网络调用计一次，不声称其内部 HTTP 数，缺漏就全部 null。源码、外部 pre/post、实际开始/结束及命令回执可对账才写完整计数。来源、深读、Data readback 指标维持原契约；本地验收看此明确口径，不伪称 API-native 埋点验收。

## 4. 本地生成与 Data 提交

全部输出为 UTF-8 LF；Windows CRLF 转换不能改变用作索引的 blob 身份。先 validate-batch，再使用现有 manifest-aware prepare；不要使用未更新 validation-index 的普通 prepare 路径。历史读取从固定 blob 得到原始 bytes，不能拿 checkout 的 CRLF 文本冒充原始 SHA。manifest 由 `local_maintenance.manifest(root, pinned_sha)` 得到；固定输入用 cat-file 原字节物化到忽略目录，manifest-aware prepare 的 --validation-index/--config/--registry/--readme 显式指向这些输入。

新 snapshot 的实际 Git blob SHA 以 `git hash-object -w --no-filters <snapshot>` 返回为准；与 LF bytes 的 Git blob 哈希相符才追加 validation-index。所有旧 index entries 必须原样保留，且恰好增加一条。本地虽有 cryptographic helper，本次迁移仍采用 events=[] 与 pending_work，不自动扩展事件回填。报告、项目卡、最新稿与不可覆盖的同 run_id 日期稿按原规则生成。只暂存明确的允许路径，禁止 git add -A。

完成本轮所有检查后，只创建单父节点 Data commit；parent 必须是固定/经协调的新 HEAD，snapshot.base_commit_sha 与其一致，索引与 staged/committed blob 相同。调用 `plan --phase data --run-id <run_id> --commit <data_sha>`，检查所有 changed paths/parent/tree、旧历史不可变和同 run_id 日期稿。

推送前重新读取远端 HEAD；移动时最多一次基于新 HEAD/tree 重做受影响输出/校验，保留其他人内容，不把旧树接在新 parent 上，不自动变基用户提交。普通 `git push origin <data_sha>:refs/heads/main`；禁止 force、force-with-lease、历史改写或绕过保护。若非快进被拒，停止并保留本地提交用于对账。超时/无回执是 uncertain，先只读按 run_id 与 SHA 对账再决定恢复，禁止盲重推或新造批次。

## 5. 必须独立远端回读，随后 Receipt

本地对象、fetch 命中本地缓存、push 的成功文本和两个相同 SHA 参数都不等于 GitHub 逐文件回读。用独立 `gh api repos/psiQAQ/agent-memory-github-trending/git/commits/<data_sha>`、固定 tree 和每个 changed-path blob 接口实际读取：commit SHA/parent/tree，完整 tree（截断则完整枚举子树），每个 path 的 mode/type/SHA 和每个 blob 的实际解码 bytes/size/Git blob 哈希都必须与预先冻结的 plan 一致。重新核对远端 snapshot/index 和全部旧 entries；远端 main 必须仍包含该 Data commit。任何失败不能进入 Receipt。

全部 Data 回读完成后冻结计数。用已验证 batch、固定旧 checkpoints 更新逐来源水位：metadata/head 仅 status=ok，Release 还须 complete=true；失败保留旧成功值。state/status.json 写真实 Data SHA、覆盖、pending_work 与 local_git 运行方式；不得预写 Receipt 自己已回读成功。生成本轮只追加 metrics 与脱敏冻结 evidence，同一独立 Receipt commit 包含 checkpoints/status/metrics/必要 evidence。指标路径不加入 snapshot index。

`plan --phase receipt --run-id <run_id> --commit <receipt_sha>` 检查独立 Receipt 路径与历史不变；它只辅助结构校验，执行者仍须逐项核对 metrics/data SHA、source coverage、状态和来源真实性。再次核对远端，常规 parent 为刚验证的 Data；其他提交介入时按原协议协调一次，不丢失新增内容。非强制 push 后同样从 GitHub API 回读 commit/tree/全部 Receipt blobs/main，至少验证 checkpoints/status/metrics 三份及每份 evidence。Receipt 写/读排除在冻结计数之外。

### 发布后网页验收

Data 与 Receipt 全量回读通过后，只读核对现有 GitHub Pages 构建、部署的真实 commit、完成状态与 URL。部署 commit 须为本轮 Data，或已确认包含该 Data 的后代；不要求部署恰好停留在 Data 提交。随后访问实际首页、最新简报和 `reports/briefs/<run_id>.html` 日期归档，核对本轮标题、关键变化和归档身份。分别记录推送、Data/Receipt 回读、Pages 构建/部署、网页内容的实际结果；push 成功或 Pages 构建成功不能替代线上内容验收。

此阶段发生在指标冻结及 Receipt 回读之后，不纳入本轮 `api` / `local_transport` 计数，也不回写已冻结的 Receipt 来预报或补写自己的成功。超时、拒绝、页面不可达或部署未完成须按实际观察保留 Failed、Not Run 或 unknown，并说明具体动作及已知 Data SHA；已验证的 Data/Receipt 结果保持原结论。不因网页验收失败重复采集、重发已完成批次、另开诊断提交，或改动站点模板、配置、工作流、权限和网络来绕过。网页构建继续由已有 GitHub Pages 承担，不在本地安装或运行 Jekyll。

恢复路径不得重发 `20261026T160515Z-interactive`：其 Data/Receipt 已确认，按当前 HEAD 的状态继续。后续中断按原 run_id 核对已发布对象；Data 已完成只补缺失 Receipt。已有相同 snapshot/blob 为 no-op，不同内容同 ID 立即停止。旧 metrics 不猜补；已存在 metrics 的恢复只读复用，`plan receipt` 的新批次模式不适用时用同等逐字段人工核验说明原因，不改工具来放宽历史保护。

完成或已确定没有在途写入时，由本轮 owner 调用 release（传原 run_id/owner_token）。若写入结果尚不明或进程中断，保留锁与本轮日志，报告恢复步骤。不得自动删除历史证据或用户文件。

## 6. 准备包的验证范围

local_maintenance.py 不采集、不联网、不提交、不推送、不操作调度。它提供完整 Git tree/index/历史快照校验、清洁工作区和 runtime gate 检查、提交计划及独占锁。它与既有 manifest helpers 是执行者的工具，不能替代来源审查、远端真实回读、触发认证、权限或平台可用性。

本地迁移必须逐项报告：配置是否创建/回读，暂停/启用状态，时区和下一次时间，真实权限下的网络/推送范围，第一次自然触发来源及 Data/Receipt 结果。未知项留 null/待验证。通知沿用中文实质变化、闭合周报、首次真实定时结果及可处理故障；失败先给原规范单句，再附必要脱敏证据。日常维护不得自行改调度。
