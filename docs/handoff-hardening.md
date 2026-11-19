# 交接故障的固定处理

2026-11-19 所有者要求把本次交接中仍留在临时入口或手工处理中的修复固化。本页约束后续本地维护；不扩大网络、发布、恢复或调度授权。已经完成的研究批次保持原件，不用它复测联网、提交、推送或网页。

## 对照结果

| 实际问题或边界 | 固定实现 | 下次如何处理 |
| --- | --- | --- |
| Codex初始化1223、历史共享沙箱端口切换与已返回网络请求混在一起 | 保留原本地协议的外部pre/post、首次错误、一次最小只读检查与人工交接边界；不修改Codex运行时 | 初始化失败不推断请求未执行或认证失败；历史10809重配的具体调用者未确认，未应用沙箱修复，不以用户终端成功替代后台环境验收 |
| SSH ProxyCommand 的 `exec` 被 PowerShell 解析，Git 远端读取退出128 | `owner_pipeline.git_child_env` 在 Git 子进程环境中选择当前 Git 安装内已有的 Bash；父进程及代理变量保留 | 缺失 Bash 就停止，不安装、不改 SSH、代理或安全配置；不先故意触发失败再重试 |
| 切回旧 main 后，新模块消失；日志器在合并前读取自身文件失败 | `WRAPPER_SHA256` 在模块导入时固定执行代码身份；`create-entry` 从指定本地 Git commit 生成不受检出影响的固定源包 | 可能切分支时先生成并验证交接包；启动时再次逐 blob 与原 commit 比对，不从切分支后的工作区重新导入 |
| 临时前置检查把分支名传给仅接受 SHA 的 pin | 保留 `local_maintenance.pin` 的 HEAD/完整SHA约束；交接包在生成时解析并固定完整SHA | 查分支用只读 `git rev-parse refs/heads/...`；不能放宽固定版本门禁 |
| 成功远端读取、fetch、切分支后中断，再运行会撞回执或重做步骤 | `resume-draft`、`--resume-evidence` 绑定首次失败、原 HEAD/锁和所有留存字节；传输层复用精确参数一致的成功回执 | Agent 先核对宿主/进程/写结果；未知确认项保持 null。首次 FAILED 不删除；失败或不确定网络动作不能据此重放 |
| CMD 嵌套引号被 Python 参数列表再次转义；默认沙箱身份不等于所有者普通用户 | `test_handoff_hardening` 在真实 CMD 和中文空格路径执行生成入口，核对0/7退出码，并真实切换隔离仓库分支 | 只通过语法检查不能交付；运行身份、启动/收尾、退出码、重入分别验收。默认沙箱受阻仍按原协议，不换工具绕过 |
| Contents 对超大文件返回 encoding=none，提取器却当成完整正文 | `extract-review` 将其记为 missing，保留 SHA/size 和缺失原因；可生成显式 Git blob GET 线索 | 不当作零内容或整文件已读；如需全文，由 Agent 另列同范围固定 SHA 请求，所有者运行原入口，不自动追加网络 |
| 注释 tag 未剥离，PR文件/compare有界返回不证明发行包含关系或全范围完整 | 提取工具标 unpeeled，并核对 PR 总文件数、实际页码和末页；显式计划支持 Git tag/blob GET | compare 达300文件保留未知完整性；未核实的发行状态保留未知，不能用时间先后或版本号猜包含关系 |
| Receipt 继承了旧 tracked/候选池统计，需要手动改20/47 | `staged_publication.prepare_receipt` 从当前已发布 Data 的登记与候选重新推导统计 | 不从旧 status 复制当前计数；CLI/API跨交接缺口继续 null，不因脚本化就追认完整计量 |
| 网页只核对标题/要点，变更表的合并/发行状态另用临时脚本核对 | `webpage_checks` 从本轮 Data Markdown 的变更表生成预期，逐行比对实际 HTML | 首页、最新稿、原 run_id 归档分开验收；HTTP200和构建成功各自不能代替内容 |
| 本地内容断言错误时，已有正确URL/HTTP200字节却无法安全复用 | `staged_publication recheck-web` 只读已留存 bytes，核对原URL、实际URL、HTTP状态与字节指纹；另写 rechecked 回执 | 原 Failed 保留；无下载、传输失败、URL不符或字节冲突一律停止，不能借离线复核重试网络 |
| 同一已完成批次再次调用 prepare/commit/pages 等会报错或写准备文件 | 两套固定 CLI 优先核对 final-completion 与实际 Receipt 身份，返回 already_complete | 不拿锁、不写准备文件、不采集/提交/推送/请求网页；历史 run_id 不替换成新日期 |

这些修复不证明 Codex 的1223启动错误已永久消失。它仍属于执行器初始化边界；按已有规则保留首次阶段、精确动作和可见错误，不解释为上游认证失败。用户手动执行成功也不证明自然 Scheduled E2E。

## 失败后从原步骤恢复

以下命令在仓库根 PowerShell 执行；`<run_id>` 必须是未完成的原批次。

```powershell
python -B scripts/owner_pipeline.py resume-draft --run-id <run_id> --resume-command collect
```

生成 `owner-pipeline/resume-draft.json`，三个确认项均为 null，**不是恢复许可**。Agent 核对原宿主/进程、独占锁、是否有在途调用、实际本地与远端 Data/Receipt，以及首次失败前每个动作后，另写本轮 `agent-review/resume-evidence.json`。保留全部摘要字段，填入实际确认与可核对来源；工具校验结构和字节，不能认证声明真伪。同一状态重入复用首次草稿；HEAD/锁/留存清单变化时生成带状态指纹的新草稿，三项确认仍为 null，旧草稿保留，不能直接盖成 true。

```powershell
.\collect-owner.bat collect --run-id <run_id> --resume-evidence ".cache/<run_id>/agent-review/resume-evidence.json"
```

原锁还存在时，仍需另行满足本地锁恢复证据和 `--clearance`；`--resume-evidence` 不能代替它。恢复采集会复用成功的 fetch/ff-only 和来源回执，并在同一固定基线下作一次新的远端 HEAD 核对；远端移动就停。已存在且一致的 batch/pages/线索直接复用，不覆盖不同内容。失败、未知或被拒的工具请求不在这个恢复范围；Git 写结果不明仍走 `readback`，不能重新 `publish`。

## 生成不受切分支影响的入口

已经批准、已本地提交且包含全部固定脚本的版本，才可用于生成交接包。下例只生成原批次的采集入口，不做工程合并、推送，也不授予执行许可：

```powershell
python -B scripts/owner_pipeline.py create-entry --run-id <run_id> --program-commit <完整程序commitSHA> --entry-program owner_pipeline --entry-command collect
```

目录位于 `.cache/ssh-user-check/<run_id>/owner_pipeline-collect/`。BAT保持短ASCII、UTF-8无BOM/CRLF；相邻 entry.py 为UTF-8 LF，依赖源码来自同一 commit 的实际 blob，逐个校验。入口绑定 repository、项目根、run_id、程序commit及固定阶段；调用方不能用参数改 root/run_id。其他已授权固定阶段可选择 `review-fetch/publish/readback`，或 `staged_publication` 的准备、提交及网页阶段。未授权的工程推送不因此获得授权。

先用返回的绝对路径执行 `entry.bat --check`（不联网）；需要恢复时再传实际 `--resume-evidence`、`--clearance` 等阶段参数。生成状态是 `generated_not_runtime_verified`；须通过真实CMD、中文空格路径、退出码及分支切换测试后才能作为人工交付入口。不要再次手写每批临时 Python 运输器，也不要全局替换旧批次脚本的日期或 run_id。

## 离线提取与网页复核

所有者补抓返回后，Agent 使用已留存结果生成审读目录：

```powershell
python -B scripts/owner_pipeline.py extract-review --run-id <run_id> --plan ".cache/<run_id>/agent-review/review-requests.json"
```

输出 `agent-review/source-catalog.json` 与按 blob SHA 命名的已核验正文；不执行上游代码，不取缺失页面。每轮补充清单累计最多50个不同请求，仍受最多5个已登记项目/10个候选及原分段预算约束。文件提取、抓取成功不等于研究判读完成。

只修正本地网页断言、复用正确请求的留存正文时：

```powershell
python -B scripts/staged_publication.py recheck-web --run-id <run_id> --review ".cache/<run_id>/agent-review/website.json"
```

它没有网络动作，保留原失败，并将新校验绑定到原记录。传输失败不能用此命令恢复；已完整验收的批次直接返回完成态，不额外写复核记录。网页检查始终排除冻结的API/CLI指标，不回写 Receipt 补宣称它自身成功。

## 本轮固化的验收

```powershell
python -B -m unittest discover -s tests -p test_owner_pipeline.py
python -B -m unittest discover -s tests -p test_handoff_hardening.py
```

相关测试包含原14项合成采集/Data/Receipt流程和12项交接回归：实际隔离Git分支切换导致文件消失、固定源包在真实CMD中文空格路径启动、成功回执复用、失败网络禁止重放、来源缺正文/注释tag、网页状态表和离线复核、已完成批次无写入，以及Receipt统计由当前Data推导。网络响应使用合成输入；不重跑已完成批次的联网/发布/网页步骤。真实已完成批次及原始响应另按字节清单只读核对保留。
