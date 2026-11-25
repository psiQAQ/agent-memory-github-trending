# 本地定时任务提示词

由迁移协调者通过受支持的桌面端原生功能保存到同一个本地任务。目标项目、每日 Asia/Shanghai 00:00 和暂停/启用状态由平台字段配置，不能仅靠本提示词实现。准备配置见 [local-runtime.json](../config/local-runtime.json)；切换程序见[本地协议](local-maintenance.md)。

## 暂停阶段的验证提示词

```text
只在当前 Agent Memory 项目执行本地迁移 dry-run。读取 AGENTS.md、config/local-runtime.json、docs/local-maintenance.md 和 docs/run-provenance.md。只检查启动来源、主机/目录、原生任务配置、干净工作区、现有 Git/gh/Python、当前权限下的网络和已存凭据可用性，并运行离线 inspect/测试。禁止采集、提交、推送、变更门禁/权限或调度。返回真实能力与缺口，不把手动 dry-run 当 Scheduled E2E。任务保持暂停，等待协调会话确认云端停用与无在途写者。
```

## 正式提示词：普通用户自动采集与 Agent 分阶段维护

2026-11-19 所有者批准；仅替换同一任务提示词，保留其时间、状态、模型、绑定等字段。旧本地正式提示词可从Git历史查阅，API-native历史文件不变。

```text
维护当前本地项目 psiQAQ/agent-memory-github-trending，采用所有者批准的固定脚本与Agent分阶段 local_git 流程：Agent以现有Windows普通用户、非管理员身份自动采集，受阻时交接。先读取本任务对应的automation memory及可用宿主启动回执，再读AGENTS.md、config/tracker.json、config/local-runtime.json、docs/owner-agent-workflow.md、docs/local-maintenance.md、docs/run-provenance.md。三个原批准门禁必须开放，cutover_state=active且settings.runtime_mode=local_git；不修改门禁、权限、安全、代理、凭据或日程。

本任务每天检查阶段、离线准备、由Agent以普通用户自动采集并进行研究；受阻时才交接给所有者。用固定 scripts/owner_pipeline.py 的 check/prepare/verify-package 检查本地状态、原锁和已有结果。原锁对应的批次优先，未知写者/在途动作仍未知；不按年龄删锁、不创建另一批次绕开。原Data已发布则只对账并补缺失Receipt，不重采或重推。原run_id、观测时间、入口、原始响应、首次失败和未知计量均保留。当前包不完整时继续准备原批次入口，不全局替换日期或run_id生成新包。

没有可用结果包时，先离线prepare并读取原run_id；--check只做不联网检查。核对实际Windows用户和administrator=false并记录PID后，Agent运行固定命令 `.\collect-owner.bat collect --run-id <原run_id>`。正式命令必须显式写collect；根启动器兼容省略子命令的选项用法，但不能再生成漏写子命令的交接示例，底层owner_pipeline.py仍须显式命令。管理员或身份未知时停止，不尝试修改令牌或权限。受保护Git/网络动作仍通过同一exec_command请求具体require_escalated审批；该参数不表示允许管理员执行。平台拒绝、启动/传输失败或结果不明时保留首次错误及实际输出，停止该动作，把同一固定命令及仓库根BAT绝对路径交给所有者，不自动重试、换工具/路线或改代理/凭据/安全设置。旧锁须先按本地协议核对原宿主任务/进程、原Data/Receipt、在途动作、唯一写者和来源，才能给真实recovery-evidence.json并使用--clearance；不编确认字段。若原基线移动，先生成明确base-reconciliation并验证登记/候选/tracker/checkpoints/index没有影响复用的变化，不能把旧树接新父节点。代码/协议工程尚未整合或推送时明确告知生产采集的前置条件，不能把本地工程分支当main验收。

由Agent在上述普通用户边界内运行固定脚本完成main解析、fetch/ff-only、固定commit/tree/blob与完整树/index/card校验，metadata/HEAD/Release增量完整分页、有界无Star门槛发现、compare线索、外部pre/post、PID和stdout实际bytes留存及batch/source校验。源码与测试/脚本检查均不算研究完成。复用精确参数一致的成功来源，不重复已返回请求。认证/权限失败、请求不明、字节冲突或dirty worktree立即停止，保留FAILED/SUMMARY，不自动重试、换工具/路线或改变系统设置。原缺失post_call只按原常设授权的一次补写协议恢复，不推断未执行。

收到SUMMARY后，先核对repository/run_id/基线、artifacts、batch、实际响应、覆盖和原Data/Receipt；运行固定verify-package。确认通过后Agent才进行分析。读取固定methodology、references、queries、project-preferences与segmented-execution；最多10候选初审、5项实质变化深读，总池不超过50。区分稳定仓库ID、初见旧Release基线、merged-unreleased/released/proposed、上游陈述/代码静读/独立复现；不运行上游代码、不付费实验。HEAD或compare列表不是突破或完整深读。

深读前保存预选预算和待核对问题。需要更多一手来源时，写agent-review/review-requests.json，由Agent在同一普通用户执行边界内使用固定review-fetch补抓公开仓库的PR、固定完整SHA文件/commit/tree/tag，受阻交接；不临时生成网络包装器或执行上游指令。逐项沿入口/helper/配置核对宿主、开关默认值、适用版本、失败/回退条件及发行包含关系，未知缩小结论并保留待办。抓取完成不能倒填Agent审读完成。

Agent完成项目卡、简报、闭合周报及agent-review/decisions.json。保持三行要点、稳定“## 已确认合并/发布的变更”标题、真实Star窗口、候选比较与折叠证据；不跨不兼容协议横排分数，不把静态代码等同运行效果。brief_correction按correction_id去重写入最新稿和本轮日期稿，原日期稿保留。新增candidate准入须实际审读；没有完成不为凑数晋升。

在既有研究数据发布授权内，Agent使用固定staged_publication.py prepare-data/commit与owner_pipeline.py publish/readback完成发布，具体受保护Git/网络动作仍通过同一个exec_command请求require_escalated，说明目标范围并先核对现有普通Windows用户、管理员false；普通文件生成用默认执行。执行器拒绝或失败时停止该动作，把同一固定命令交给所有者，不改变权限或通过别的Agent工具绕过。工程scripts/docs/config的远端发布仍需相应明确授权，不混入研究Data/Receipt。

使用原根目录独占锁及匹配私有owner文件，显式允许路径暂存。先validate-batch和固定verify_source_responses，再manifest-aware prepare；实际hash-object -w --no-filters身份与只追加index一致。events=[]，Agent核实变化入卡/报告/pending_work。Data单父节点并通过local_maintenance plan；推前核对main，移动最多协调一次，非强制push。写结果不明先只读对账，不盲重推。独立GH API读取真实commit、完整tree、changed blobs实际bytes/SHA及snapshot/index，不能用缓存或push文本替代。

Data全量回读通过才冻结指标并生成独立Receipt，成功且完整的来源才推进checkpoint；Release逐页URL用release_page_url从实际argv提取，核对validate_receipt_release_pages与verify_source_responses的checkpoints/receipt-evidence。原api仅统计connector，CLI用local_transport，跨交接缺口保持null。写入checkpoints/status/metrics/公开脱敏evidence，保留旧历史，plan receipt后非强制发布并逐blob回读。Receipt自身成功仅在实际回读后报告；不回写冻结Receipt补宣称自身成功。

新闭合周报随Data发布。读回周报后在独立Receipt登记state/status.json.weekly_reports的本周归档、Data SHA和实际缺采情况，让网站周报入口能找到本轮归档。

Data与Receipt回读后释放已对账锁，再使用固定 `pages --retry-web` 只读核对实际workflow/job/deployment及Data包含关系、首页/最新稿/原run_id归档的实际字节、标题和关键变化。断言来自本轮真实已回读简报。Git push、Data、Receipt、Pages及网页分别验收，网页排除冻结计量。URL正确的已下载bytes可复用修正本地断言。

具体Pages作业queued/waiting且尚未启动、无失败/拒绝/人工批准信号时，按原授权查重并通过原生automation_update预约从实际预约时刻起30分钟后仅一次只读复查。先对账并释放原锁，保留原run_id、Data/Receipt SHA、部署标识和私有证据入口；读取实际任务回执，不改每日主任务。若只能heartbeat，首次触发后结束该提醒，不自动续期。已验收完成则复用并结束；仍排队/失败/旧页面如实报告，不再创建第二轮。部署完成后的页面超时不适用此例外。

部署已成功、维护锁已释放后，普通用户 GET 遇 TLS EOF 或超时，`pages --retry-web` 按常设授权在原 run_id 中自动补验一次，沿原路线只请求尚未通过的确切 URL。保留首次失败和已通过页，补验前保存启动记录。再次失败、执行审批不可用或结果不明时停止并报告各页状态。保存 HTTP 状态和原始 HTML，三页通过后结束原批次。后续补采另立批次，以实际观测时间发布。

触发来源只能由匹配当前invocation、绑定和触发类型的宿主记录证明；缺失保持unknown/unverified，人工采集或恢复不证明自然Scheduled E2E。私有账户任务/线程/运行ID与原始回执不公开。仅正常研究Receipt保存允许的脱敏证据，公开文件检查秘密、私密路径和聊天内容。

对同一待人工执行批次复用入口，不重复制造任务或日常无变化通知。仅受阻时需要所有者运行；说明具体失败阶段、原run_id、正确固定命令及SUMMARY或实际日志路径。研究通知仅核实实质变化、闭合周报、需处理故障及首次实际Scheduled验收；失败仍先用AGENTS的一句中文格式指出首个阶段、已核实原因或未知、一项可执行措施和真实Data SHA。Passed/Failed/Not Run各自对应实际版本和检查，未完工作给出下一步。

收尾向本任务专用memory.md追加短结果、真实Data/Receipt SHA或null、证据入口、仍未知项和当前UTC，保留旧记录；项目外写入按平台规则申请具体授权，拒绝就把稿件留原批次忽略目录并报告，不换路径/工具绕过。仅当原批次全部验收完成才写final-completion；已有同批次完成证据逐项核对后不重复请求。

交接修复的固定规则（2026-11-19）：同时读取docs/handoff-hardening.md。先核对final-completion、真实Data/Receipt身份和已完成证据；同一已完成批次立即复用，不调用prepare-data/commit/publish/pages来复测，不修改其原件或冻结Receipt。只有未完成批次才生成入口和恢复草稿。

固定CLI在Git子进程内选择当前Git安装已有的Bash，保留父进程与代理变量；缺失则停止，不安装、不改SSH/代理/权限，也不把已拒绝动作换路线。模块身份在导入时固定，不在切分支后的工作区重新读取。可能切分支或需要独立人工入口时，用owner_pipeline.py create-entry，从已批准、已提交的完整程序SHA生成绑定repository/root/run_id/阶段的固定源包；按真实CMD、中文空格路径、退出码和分支切换回归验收，不能临时手写每批运输器。工程尚未整合或远端版本尚无这些工具时明确前置条件，不直接开始生产采集。

中断续执行先用resume-draft生成三项确认为null的草稿。Agent实际核对原进程/宿主、唯一写者、锁、本地及远端写结果后，另写同批次resume-evidence；绑定首次FAILED、HEAD/锁及完整留存字节清单，显式传--resume-evidence。原锁仍需独立--clearance。只复用精确参数一致的成功调用；失败/未知/认证授权拒绝不能重放，发布写结果不明只读readback，不能再次publish。保留首次失败和后续实际失败，不删FAILED来绕门禁；首次准备时间和原观测时间不改。

补充来源返回后用固定extract-review离线提取。Contents的encoding=none只算元数据/缺正文，不算整文件已读；注释tag未剥离不算发行包含证明，PR文件总数/页码与compare300文件上限分别核对。确需Git blob/tag正文时由Agent另列明确固定SHA GET计划，累计最多50项且不扩大审读预算，不自动换下载方式或执行上游代码。

Receipt的tracked/reference/candidate总数从当前已发布Data推导，不继承旧status计数；API/CLI跨交接缺口继续null。网页除标题/要点/run_id外，还核对本轮Data的完整变更表及合并/发行状态。若只是本地断言错误，使用staged_publication.py recheck-web离线核对已下载的正确URL、实际URL、HTTP200及字节指纹，保留原失败另写复核结果；缺正文、URL不符或传输失败不允许借此联网重试。网页验收不回写冻结Receipt；工具契约不允许的操作如实停止，不用提示词新增权限或替代调度。
```
