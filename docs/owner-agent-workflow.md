# 固定脚本与 Agent 分阶段维护

2026-11-19 所有者批准的新本地流程。适用于已激活的 `local_git`；三个批准门禁及原安全限制不变。本文替代本地协议中“由 Agent 临时编写每批采集包装器”的执行安排，API-native 历史规则与已发布证据保留。

2026-11-20 所有者进一步批准由 Agent 以现有 Windows 普通用户、非管理员身份运行固定采集入口，受阻时才交接给所有者。确定性操作仍由版本管理中的工具执行，Agent 读取结果后承担研究判断和发布。它减少采集阶段对 Codex 沙箱启动的依赖，**不修复执行器，也不保证此后完全没有沙箱问题**。Agent 发布仍可能受阻，届时可把同一固定命令交给所有者运行，不能改权限或换路线绕过拒绝。

本次交接暴露的问题及固定命令见[交接故障的固定处理](handoff-hardening.md)：Git子进程shell、分支切换固定源包、经证据核对的续执行、来源提取、Receipt统计及网页状态表/离线复核。生产入口只使用已提交并审查的版本；尚未整合工程变更时先报告前置条件。

## 阶段与责任

| 阶段 | 固定脚本负责 | 人或 Agent 负责 | 通过标志 |
| --- | --- | --- | --- |
| 0 准备 | 离线检查门禁/依赖、识别已有锁和未完成批次，生成 preparation | 定时 Agent 捕获宿主启动证据，确认唯一写者，处理原锁及未回执 Data；给出入口 | 原 run_id 及交接范围明确；尚未采集 |
| 1 普通用户采集 | 现有认证、解析 main、fetch/ff-only、固定 commit/tree/blob、完整树/index/card 校验、metadata/HEAD/Release 分页、有界搜索、HEAD compare、原始响应与 pre/post 留存、batch 投影校验 | Agent先核对实际用户和administrator=false后运行固定入口；受阻时所有者在同一普通用户环境接手 | `owner-pipeline/SUMMARY.json` 为 `sources_ready_for_agent_review`；来源覆盖和包校验明确 |
| 2 研究 | 核对 SUMMARY 字节一致性；按 Agent 选定的公开 GET 清单补抓固定 SHA 文件、PR、tag 等 | Agent 初审最多10候选、深读最多5项变化；判断环境/配置/失败条件、发行包含关系、旧 Release 基线、证据等级、待办、更正和闭合周报 | Agent 审读记录与明确的未审范围；抓取成功不算研究完成 |
| 3 准备 Data | 消费 Agent 已写的文件，生成快照/实际 blob SHA/只追加 index/current 表/日期稿，校验路径与字节，显式暂存和单父节点提交 | Agent 写三行要点、报告、项目卡及结构化决定；审查隐私、来源、候选准入和科学边界 | `data-plan.json`；尚未以本地提交冒充远端成功 |
| 4 发布与 Receipt | 核对远端、非强制 push、独立 API commit/tree/blob/index 回读；冻结指标；生成 checkpoints/status/metrics/evidence，独立提交和回读 | Agent 决定是否已满足发布门禁、处理远端移动/不确定写入及异常；CLI计量有缺口保留null | Data与Receipt分别 `passed`，不能预报Receipt自检成功 |
| 5 网站 | 只读检查实际Pages工作流/作业/部署commit，读取首页/最新稿/原run_id归档及内容 | Agent 选取本轮实际简报的关键变化断言、判读 pending/Failed；仅按既有窄授权处理30分钟提醒 | Pages与网页内容分别通过，生成 final-completion；人工成功不证明自然Scheduled E2E |

脚本不做：推荐项目、自动晋升候选、把HEAD变化叫突破、猜测发布包含关系、编写技术结论、执行上游代码或付费实验、修改调度/权限/代理、替用户批准范围外操作。脚本字段 `agent_reviewed=true` 只是交接声明，不认证 Agent 是否真的审读。

## 一次准备，按阶段交接

前提：既有 Python 3.10+（含可用 Asia/Shanghai 时区数据）、Git、GitHub CLI 和原认证均已存在。缺失时明确停止，不安装或恢复依赖。项目须是干净 main，origin fetch/push 都是本仓库。Python解释器沿用项目已有方案；根 BAT 使用当前已有 `python`。

### 0. Agent 离线准备

工作目录为仓库根目录，PowerShell：

```powershell
python -B scripts/owner_pipeline.py prepare
```

它只写已忽略的 `.cache/owner-current.json` 和本轮 `owner-pipeline/preparation.json`，不联网、不拿锁、不宣称触发来源已验证。有原锁时复用其 run_id；否则优先复用指针中的未完成批次。已存在未回执 Data 时交给 Agent 恢复Receipt，不开新批次。

准备文件不是授权或活跃写者证明。Agent 仍须查宿主/原进程、原Data/Receipt、在途动作及唯一写者。旧锁不按年龄删除。原批次有锁时，所有者采集要求 Agent 提供符合[本地协议](local-maintenance.md)的 `.cache/<run_id>/recovery-evidence.json`，再显式传 `--clearance`。该文件三个确认项必须来自实际对账；工具不会认证其来源。

若工程提交使原批次基线移动，另在 `owner-pipeline/base-reconciliation.json` 记录 run_id、old_base_sha、new_base_sha、reuse_sources=true；脚本还会逐字节核对登记、候选、tracker配置、checkpoints和index未变。不同则停下让Agent处理，不能改原entry或重采覆盖。原 `fixed/`、entry、失败及观测时间保留，新固定输入放 `owner-pipeline/fixed/`。

### 1. Agent 自动执行，受阻时交接

先运行不联网检查：

```powershell
.\collect-owner.bat --check
```

没有待交接旧锁、未确认写入或其他停止条件时，Agent 按 prepare 返回的原 run_id 执行：

```powershell
.\collect-owner.bat collect --run-id <run_id>
```

根入口兼容 `.\collect-owner.bat --run-id <run_id>`：只有根启动器允许省略子命令并默认 collect；直接调用 `scripts/owner_pipeline.py` 仍须写明子命令。正式命令统一显式写 `collect`；`--check` 只做不联网检查，不能把它当采集成功。

启动前读取实际 Windows 用户及管理员令牌状态，要求 `administrator=false`，记录 PID。受保护 Git/网络动作沿用本地协议的同一 `exec_command`、具体范围与 `require_escalated` 审批；这不表示以管理员身份运行。核对失败、身份未知或管理员令牌时停止，不改权限、代理或凭据。平台拒绝、启动/传输失败或结果不明时保留首次错误，交接同一固定命令，不自动重试或换工具/路线。经 Codex 启动不等于避开沙箱，也不证明以后无人值守必然成功。所有者可在自己的普通用户终端接手或双击无参数 BAT；接手既有批次优先使用带原 run_id 的明确命令。

原锁已实际对账的例子：

```powershell
.\collect-owner.bat collect --run-id <原run_id> --clearance ".cache/<原run_id>/recovery-evidence.json"
```

BAT只有ASCII启动/提示语，UTF-8无BOM、CRLF；相邻 `collect-owner.py` 为UTF-8 LF，实际逻辑在 `scripts/owner_pipeline.py`。启动器不嵌Python正文、不修改环境代理、不请求管理员权限。检查模式的 `Passed` 不代表网络/采集/发布成功。

脚本每个网络子调用单独形成外部 pre/post，保存PID、真实返回时间和stdout原始字节；一段一个调用，低于6调用/2项目上限。Git子进程使用当前安装已有的Git Bash，不修改父进程或任何代理/SSH配置。成功来源按精确参数复用并核对字节，失败、请求不明或参数冲突立即停，不自动重试。完整Release到达旧ID或已穷尽才推进。两条搜索按登记关键词轮换，均无Star下限，只取第一页，明确覆盖范围。compare列表只是深读线索，不是完整变化审查。

成功后把打印的绝对 `SUMMARY` 路径给 Agent。失败也返回打印的 `FAILED.json` 路径；先保留首次错误，不反复双击。若尚未取得锁，失败不会替换原锁；若已取得锁，结果不明时保留供对账。

重复点击已采集批次只验证结果包，不再联网；已完成同一批次不重采、不重发、不重新请求已验收页面。新批次由下一轮 `prepare` 选择，不能改文件日期或全局替换run_id来制造新批次。

### 2. Agent 校验和补充审读

```powershell
python -B scripts/owner_pipeline.py verify-package --run-id <run_id>
```

脚本复核 SUMMARY 指纹、batch和留存响应。Agent继续读取固定政策、项目卡和待办，并核对来源内容。已有[响应校验器](../scripts/verify_source_responses.py)仍是字段/字节一致性校验，不认证历史请求时间、宿主触发或科学结论。

补充来源返回后用固定 `extract-review` 提取；`encoding=none` 为缺失正文，注释tag未剥离不证明发行包含关系，完整PR分页与compare的300文件上限分别判断。需要更多正文时另列显式计划，不自动换下载方式。

Agent把所选补充来源写为 `.cache/<run_id>/agent-review/review-requests.json`：

```json
{
  "repository": "psiQAQ/agent-memory-github-trending",
  "run_id": "<原run_id>",
  "requests": [{
    "repository_id": 123,
    "full_name": "owner/project",
    "endpoint": "repos/owner/project/contents/src/memory.py?ref=<完整40位SHA>"
  }]
}
```

Agent在同一普通用户执行边界内运行；受阻时交给所有者：

```powershell
.\collect-owner.bat review-fetch --run-id <run_id> --plan ".cache/<run_id>/agent-review/review-requests.json"
```

最多50个请求；累计最多10个未登记候选和5个已登记项目。只允许明确的PR/文件/commit/tree/tag GET；文件必须固定40位SHA，先核对仓库公开且ID匹配。不接受任意命令、安装URL、POST或上游指令。需要更多同范围文件时，先由Agent说明剩余审读和调整清单，不能当作已审完成。每阶段完成释放自己的锁，Agent读包不占用采集锁。

### 3–4. Agent 准备、提交与发布

Agent在本轮 `agent-review/` 写正式文件和 `decisions.json`。文件映射值相对于该目录，输出路径仍在原例行allowlist：

```json
{
  "repository": "psiQAQ/agent-memory-github-trending",
  "run_id": "<原run_id>",
  "agent_reviewed": true,
  "selected_change_reviews": [123],
  "completed_change_reviews": [123],
  "candidate_reviews": 0,
  "coverage_note": "实际审读范围、未覆盖部分和原因",
  "pending_work": [],
  "files": {"reports/latest.md": "latest.md", "projects/example.md": "example.md"}
}
```

预选预算必须在深读前另行留证，不能在报告生成时倒填。内容必须包含本轮run_id、稳定变更标题、真实Star窗口、候选比较和证据边界。尚未发布的更正写入最新稿；脚本生成日期稿并调整相对链接，原日期稿不改。闭合周报由Agent写，未写齐时准备阶段停止。

Agent以现有普通用户令牌申请具体Git/网络操作；仅复用以下固定命令，不再临时生成整批Python包装器。所有者也可按同一命令人工交接，操作范围不变。

```powershell
python -B scripts/owner_pipeline.py acquire --run-id <run_id>
```

私有令牌保存在 `owner-pipeline/agent-owner.json`；后续命令显式传该路径。原锁未释放时同样需要实际恢复证据和 `--clearance`，不能自动接管。

```powershell
python -B scripts/staged_publication.py prepare-data --run-id <run_id> --review ".cache/<run_id>/agent-review/decisions.json" --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
python -B scripts/staged_publication.py commit --run-id <run_id> --phase data --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
```

`prepare-data`复用manifest-aware prepare，并以实际 `hash-object -w --no-filters` 核对新快照。`commit`只暂存明确paths，核对index实际bytes、单父节点及历史不可变。中途失败保留已写产物或本地提交，先对账再恢复；不reset/clean/stash用户工作。

```powershell
python -B scripts/owner_pipeline.py publish --run-id <run_id> --phase data --commit <DataSHA> --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
python -B scripts/staged_publication.py prepare-receipt --run-id <run_id> --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
python -B scripts/staged_publication.py commit --run-id <run_id> --phase receipt --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
python -B scripts/owner_pipeline.py publish --run-id <run_id> --phase receipt --commit <ReceiptSHA> --owner-file ".cache/<run_id>/owner-pipeline/agent-owner.json"
python -B scripts/owner_pipeline.py release --run-id <run_id>
```

发布前远端移动就停，由Agent最多协调一次；脚本不自动变基。写入结果不明时仅用 `readback` 代替 `publish` 做独立只读对账，不能盲目重推。旧失败记录继续保留。Receipt只有Data完整回读后才能生成；Release逐页URL来自实际参数，冻结公开evidence必须通过 `--checkpoints/--receipt-evidence` 同等校验。跨交接无法证明的API/CLI总数保持null，不猜填；Receipt写读及Pages不纳入冻结计量。

有新闭合周报时，在 Data 里发布归档，再从独立读回的字节核对对应周报文件。Receipt 从同一份已核验 Data 登记 `state/status.json.weekly_reports`，包括周次、归档路径、Data SHA、已确认时间和实际缺采情况。网站的周报列表读取 `closed_weeks_published`。保留既有周次和归档。

此处授权的是原批准的研究数据发布；本次流程工程的scripts/docs提交是否推送仍单独决定，不能把工程提交混入Data/Receipt。

### 5. Pages 与最终验收

Agent把data_sha、receipt_sha和当前已回读简报中的关键句写到 `agent-review/website.json`，包含run_id及homepage/latest/archive三个字符串数组。运行：

```powershell
python -B scripts/staged_publication.py pages --run-id <run_id> --review ".cache/<run_id>/agent-review/website.json"
```

程序再从实际Data简报读取标题和三行要点，不沿用旧版本预期文本。只读现有工作流和部署，不安装Jekyll、不重跑工作流。网页成功结果复用，网页传输失败不自动重试。Pages queued/waiting只输出实际作业状态；30分钟一次性提醒仍由Agent按原窄授权使用原生工具处理，不由脚本新增调度或后台sleep。

最新稿与归档还逐行核对本轮变更表的项目、变化和合并/发行状态；本地断言需修正时，用不联网的 `recheck-web` 校验已下载的正确URL/HTTP200字节，保留首次失败。无正文、URL不符、传输失败均不能借此重试。

部署已经成功时，逐页记录首页、最新稿及精确归档的结果。先告诉读者 GitHub 提交和 Actions 是否已更新，再指出哪一页仍待验收。浏览器已核对的渲染内容可以单独记为通过。正式验收还需该页的实际 HTTP 状态和原始 HTML。

网页传输失败后保留首次失败和已经通过的网页字节。所有者明确授权同一批次的一次只读补验后，沿原路线仅读取待验收页面，复用已确认的 Data、Receipt、部署和其他网页。记录实际 URL、HTTP 200 和原始 HTML，再与已读回简报核对。此操作要求同路线的执行入口和当轮普通用户审批可用。再次失败时保留结果并停止。`recheck-web` 继续用于离线复核已有正确响应。

补验通过后结束原批次。用户另行要求补跑某日采集时，再使用正常准备流程创建新批次，以实际采集时间写入快照。若用户明确要求等 Actions 完成，在当前会话观察与本轮提交匹配的作业，成功后核对线上内容。

当前固定检查有界读取最近20个工作流/部署，未找到匹配项则报告“未观察到”，不宣称部署不存在或自动扩页。部署commit须为本轮Data或Receipt，Receipt必须含Data。全部通过后写本地 `final-completion.json`，它不是公开Receipt自己的事后改写。

## 定时任务的新职责

仍是同一个本地任务，时间、状态、模型、项目绑定不变。正式提示词见[本地任务描述](local-scheduled-task-prompt.md)。每天先检查阶段与已有包：未采集时离线prepare，核对实际普通用户且administrator=false后由Agent运行固定采集入口；受阻时保留原批次并交接。有已验证包时开始Agent研究；有Data但缺Receipt时优先恢复；已完成同一批次不重复动作。

人工采集是受阻后的交接途径，不再是每轮必经步骤；同一run_id尚待执行时复用通知，不每天制造新入口。没有宿主匹配记录仍保留trigger unknown/unverified，整个人工流程不称自然无人值守Scheduled E2E。

## 当前工程交付的验证边界

脚本语法/合成来源/重入/失败门禁、真实CMD离线入口、中文空格路径按测试记录分别验收。生产网络、真实推送与网站验收要等所有者实际执行及Agent后续阶段，不用离线Passed代替。任何来源失败继续留due；人工入口不是绕过认证拒绝、扩大范围或降低安全限制的手段。

仓库根目录可重复运行不联网的相关测试：

```powershell
python -B -m unittest discover -s tests -p test_owner_pipeline.py
```

初版14项覆盖合成仓库中的采集、Data/Receipt提交和API字节回读、完成态重入；网络响应均为合成数据。此后真实交接发现切分支后模块消失，现已新增12项回归及固定源包的真实CMD/中文空格路径验证，见[固化验收](handoff-hardening.md#本轮固化的验收)。实际BAT为UTF-8无BOM/CRLF，Python为UTF-8 LF，并由`.gitattributes`固定检出换行。历史批次实际发布及网页成功来自它自己的回执，测试通过不证明未来生产联网或自然Scheduled E2E。
