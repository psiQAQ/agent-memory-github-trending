# 本地维护迁移工程提案（已批准；本地调度待核验）

目标：在用户指定的 Windows 项目目录，通过桌面端原生 Codex 本地自动化，保留每天北京时间 00:00 的维护频率，使用本地文件和非强制 Git 提交/推送。由协调会话先确认本地可用，再暂停原云端，避免同时写入。不得使用隐藏数据库、Windows Task Scheduler、自制后台服务或新增云端替代任务。

用户已授权迁移方向与准备工作，并于 2026-10-27 明确批准下列十个文件的工程提案及向 origin/main 普通提交、非强制推送。本提案列明政策、配置和脚本的具体工程改动。此前自动审批审查因未确认单独工程提案授权而拒绝提交；该动作已只读确认未执行，新明确授权允许重试一次。此批准不启用本地任务、不停用云端；工程推送及回读结果以实际操作回执为准。

## 拟提交的十个文件

| 文件 | 变化与用途 |
| --- | --- |
| AGENTS.md | 增加独立 local_git profile 的入口和未激活边界；旧协议保留 |
| config/local-runtime.json | prepared 状态、本地原生调度、北京时间 00:00、四项切换前置条件 |
| docs/local-maintenance.md | 两阶段切换、固定树/索引、来源、锁、非强制 Data/Receipt、远端回读和恢复 |
| docs/local-scheduled-task-prompt.md | 暂停验证与正式运行两套可保存提示词 |
| docs/local-migration-proposal.md | 本次具体提案及已验证/未验证边界 |
| scripts/local_maintenance.py | 离线完整树/历史索引检查、清洁工作区门禁、提交计划、独占锁；不联网/发布/调度 |
| scripts/tracker.py | 生成 JSON/Markdown 显式 UTF-8 LF，修复 Windows 字节身份漂移 |
| scripts/manifest_validation.py | 生成报告显式 LF，保持本地 manifest 字节一致 |
| tests/test_local_maintenance.py | 19 项本地 Git、锁、历史保护、发布计划和 LF 回归测试 |
| tests/test_manifest_validation.py | 合成 fixture 使用 LF，与 manifest 的原始 bytes 一致 |

范围仅为本仓库。本次不修改 tracker 三个批准门禁和现有 runtime_mode，不变更任何调度状态，不改历史 snapshot/index/Receipt、研究数据、上游或站点。不新增凭据、付费 API 或安全/网络/电源配置。正式切换的 runtime 选择字段变更须由协调者在满足条件后另作可审阅步骤。

## 已取得的证据

- 本地原来干净，main 原落后 4 个提交；已使用 fast-forward 同步到 d800bd83fbfb79ceb6b049fab241675c06f40a36，没有覆盖用户工作。
- 固定该 SHA 的完整 157 项 tree 索引重算通过；root tree 为 802e0e02309f3680536a9c8c7a32be3edb84814a。20 份快照、21 个登记项目和全部索引摘要通过本地对象验证。
- Python 3.13.12、Git、GitHub CLI、Node 和 Asia/Shanghai 时区数据可用。52 项 Python 测试（含本次19项）、24 项触发来源测试、32 项操作证据测试通过；合成测试不认证真实来源。
- 现有认证在获准的交互式沙箱外检查中可读取本仓库并报告 push 权限；SSH ls-remote、fetch 和普通 git push --dry-run 通过。未新增或输出凭据。
- 原生项目列表两次及一次暂停任务创建均返回 Codex app tool request failed。没有取得自动化 ID/成功回执；随后只读检查未发现对应本地 automation.toml。创建结果仍不能当作成功，也不能仅凭缺文件证明从未执行；重试前须在受支持界面对账。

## 尚未取得的证据与风险

- 原生本地任务的创建、暂停状态、目录绑定、时区和下一次触发时间尚未确认。不能据官方支持说明代替本机实际成功。
- 当前默认沙箱下 SSH 解析失败、.git ref 写入无权限、gh 用户读取返回401；交互式获准沙箱外执行成功。这不证明自然定时任务有相同权限，也不授权修改安全设置。
- 首次工程提交被审查拒绝，之后只读核对 HEAD 仍是 d800bd8、索引未暂存。用户已补充明确批准；此次重试前仍无工程新 commit 或真实 push/readback。不能把 dry-run 或批准本身当实际发布成功。
- 尚未全量采集或执行本地 Scheduled E2E。电脑须开机、联网且桌面应用运行；关机/休眠/应用退出时不能保证准点或补跑。

## 后续最小步骤

1. 本提案的十文件工程提交/非强制推送已获明确批准。先核对 HEAD/工作区，针对已确认未执行的提交重试一次；保留新增用户/远端工作。若仍被拒则停止，不拆分或换路线绕过。
2. 在用户的真正本地 Codex 项目会话或原生 Scheduled 页面，先检查是否存在本次创建请求的任务；有则复用，无则创建暂停任务，使用本地验证提示词。不要手写自动化文件或数据库。
3. 在该任务实际权限下验证 dry-run、.git 写入及现有网络/凭据，记录真实任务回执。需要改变安全设置时单独说明并取得必要权限。
4. 协调者确认原云端停用且无在途写者后，按本地协议完成 runtime 选择和同一任务启用，并回读北京时间下一次执行。然后等待真实自然触发验收。现阶段不应停用云端。

参考：[官方原生定时任务说明](https://learn.chatgpt.com/docs/automations?surface=app)。官方支持本地项目运行且要求电脑和桌面应用保持可用；本机是否可用仍以上述实际回执为准。
