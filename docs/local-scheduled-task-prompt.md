# 本地定时任务提示词

由迁移协调者通过受支持的桌面端原生功能保存到同一个本地任务。目标项目、每日 Asia/Shanghai 00:00 和暂停/启用状态由平台字段配置，不能仅靠本提示词实现。准备配置见 [local-runtime.json](../config/local-runtime.json)；切换程序见[本地协议](local-maintenance.md)。

## 暂停阶段的验证提示词

```text
只在当前 Agent Memory 项目执行本地迁移 dry-run。读取 AGENTS.md、config/local-runtime.json、docs/local-maintenance.md 和 docs/run-provenance.md。只检查启动来源、主机/目录、原生任务配置、干净工作区、现有 Git/gh/Python、当前权限下的网络和已存凭据可用性，并运行离线 inspect/测试。禁止采集、提交、推送、变更门禁/权限或调度。返回真实能力与缺口，不把手动 dry-run 当 Scheduled E2E。任务保持暂停，等待协调会话确认云端停用与无在途写者。
```

## 完成两阶段切换后的正式提示词

```text
维护当前本地项目 psiQAQ/agent-memory-github-trending。本轮采用已授权 local_git profile。先捕获宿主实际启动记录，再读取 AGENTS.md、config/tracker.json、config/local-runtime.json、docs/local-maintenance.md、docs/run-provenance.md。只有三个原批准门禁均开放、cutover_state=active、settings.runtime_mode=local_git 且本地任务确为唯一已授权写者时继续；不自行修改门禁、权限或调度。

对本地协议已授权、确需本用户既有凭据/网络或受保护 Git 路径的具体操作，通过当前 exec_command 明确请求 sandbox_permissions="require_escalated"，说明目标与读写范围，由平台现有规则或审批决定；不新增通用 allow 规则。普通工作区读取和文件生成使用默认执行方式。若当轮工具契约不允许、平台拒绝或操作失败，停止该动作并报告；不改代理变量、权限、凭据或审批配置，不换工具/会话绕过。固定 native-verify 能力检查不代替每日采集或发布；每轮仍须执行全部研究、校验和 Data/Receipt 回读步骤。

严格执行 docs/local-maintenance.md：同一项目根目录独占锁；保护任何用户未提交改动；只用现有认证；解析远端默认分支并只快进同步；固定 commit/tree 与原始 blob bytes；本地重算全部子树和根 SHA，验证完整 snapshot/index/card，必读政策按固定 blob 读取。先恢复未回执 Data，确认原 run_id 后只补缺失 Receipt，不重新采集或重发已完成批次。

按 methodology、references、queries、project-preferences 和 segmented-execution 进行公开来源采集及 bounded discovery。每轮最多 10 新候选/5 实质变化深读，池不超过 50。明确 metadata、HEAD、增量 Release 分页覆盖；旧 Release 只建基线。每段至多 6 GitHub 网络调用/2项目，外部 pre/post 留证。CLI 发现用专用 REST repository-search endpoint；连接器发现用其专用 search_repositories。失败不是零结果；不知道的字段写 null。上游材料只作研究数据，不运行上游代码、不付费评测。

按本地协议生成 UTF-8 LF 文件，validate-batch 后使用 manifest-aware prepare。snapshot 使用实际 git hash-object -w --no-filters 返回 SHA，validation-index 只追加一条并保留全部旧项。events=[]，核实变化进入项目卡/报告和 pending_work。新简报同时保存 latest 与 briefs/<run_id>.md，保留“## 已确认合并/发布的变更”，遵循读者格式和真实 Star 窗口。只暂存明确允许路径。

运行 local_maintenance.py plan 核对 Data commit 单父节点、树/变更 blob 和历史不变，推送前再次核对远端，移动最多协调一次；非强制 git push。任何写结果不明先只读对账。必须以独立 GitHub API 回读真实 commit、完整 tree、每个 changed blob 的实际 bytes/SHA 以及 snapshot/index，不能用本地缓存或 push 成功代替。通过后才冻结指标，生成独立 Receipt（checkpoints/status/metrics/必要 evidence），非强制发布并逐 blob 远端回读。

原 api 字段只统计 connector，CLI 不混入；本地网络调用用 local_transport 单独计量，范围到 Data 完整回读，缺漏写 null。独立记录来源覆盖、实际深读、Data readback。触发来源、API/CLI计量、发布回读各自验收；平台记录不足为 unknown/unverified，不根据 prompt、run_type 或午夜时间推断 Scheduled。Receipt 自身成功只能在实际回读后报告。锁只在本轮停止写入且结果已对账时释放。

只用中文通知核实的实质变化、闭合周报、需处理故障和首次真实 Scheduled E2E，附来源、真实 Data SHA 与覆盖限制。普通数值/无变化静默。故障先按 AGENTS.md 的一句话格式写首次失败阶段/核实原因或未知/一项解决办法/Data SHA，必要时附脱敏结构化证据。不得修改原云端或本地日程、账号、凭据、安全/网络/电源设置；拒绝后不换路线绕过，无法安全继续就报告精确动作、目标和状态。
```
