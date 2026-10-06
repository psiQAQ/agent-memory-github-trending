# 首版验证记录

日期：2026-09-16。验证仅执行本仓库程序和合成测试数据，没有运行任何被追踪项目的代码。

| 项目 | 实际结果 |
| --- | --- |
| `python -m unittest discover -s tests -v` | 25 项测试全部通过 |
| 真实基线 `prepare` | 9 个项目、1 个快照、0 条伪造技术事件 |
| 相同输入再次 `prepare` | 返回 duplicate、paths=[]；未生成第二份快照 |
| `python scripts/tracker.py validate` | passed |
| 当前报告渲染 | 元数据/HEAD 均 9/9，Release 为 0/9；未采集明确显示 |
| 7/30 日窗口 | 9 个项目均没有历史基线，未填造增长值 |
| 上游实验与宿主安装 | 未执行，不作独立性能认证 |
| 真实定时执行 | 尚未运行；不能用交互式成功替代 |

测试覆盖：UTC 时间、非法计数、冷启动、负净增长、零基数、短窗口拒绝外推、6 小时容差、重命名稳定 ID、重复 ID、来源失败保留旧值、Release 分页不全、同输入幂等、同 run_id 不同内容冲突、事件去重与纠错、越界路径、回读 SHA 不匹配、缺失观测、来源仓库不匹配、未来时间、上游文本不执行、无变化不造事件、北京时间 ISO 周边界和跨年、README 长度与启用门禁。

这些测试不声称模拟了 GitHub 全部网络和并发情形。真实发布采用非强制分支更新，回读文件后才保存状态回执；其真实数据 commit SHA 记录在 state/status.json 和 state/checkpoints.json。后续真实定时 E2E 验收由首次 scheduled 运行填入状态。

## 2026-09-28 GitHub API 工作树引导验证

固定 `main` HEAD `871c69911ea91cac94131ec5b1ed163b4169e94d` 后，通过 Git Data recursive tree 取得完整响应：`truncated=false`，共 61 个 tree entry，其中 49 个 blob、12 个目录；49 个 blob 当前均为普通 `100644` 文件，没有 symlink、submodule 或 executable mode。

本次交互验证对 tree 中 **49/49 个 blob** 都通过当前 GitHub connector 逐一读取，并按 Git 对象规则重算 byte size 与 SHA-1；49/49 均与 pinned tree 的 `size` 和 blob SHA 完全一致。其中执行契约、配置/数据契约、项目登记与全部 21 张项目卡等 34 个 blob 还实际物化到了新的临时目录并再次校验。由此可确认：对当前仓库结构，仅依赖 GitHub Git Data/tree/blob 读取就具备无 `git clone` 重建完整工作树所需的路径、模式和原始字节。定时运行仍必须真正物化当轮全部 blob 并完成路径集合与 **49/49（或未来 tree 的实际 blob 总数）** SHA 校验；本次交互验证不是 scheduled E2E。

本次改动只调整维护契约和说明，没有执行任何被跟踪上游项目代码，也没有改变调度频率、权限、付费能力、`config/tracker.json`、`scripts/tracker.py` 或测试逻辑。

## 2026-09-29 按需工作树交互验证

基线 HEAD：`0ad7beb8513e11e871b7a8959aef27e36e02dfe3`；根 tree：`3d48a66d6882a4e435754c8be3229c0e5fdfa382`。通过完整根目录与全部子树响应枚举 49 个 blob、12 个目录，并重算包含根在内的 13 个 tree 对象，全部一致。

实际物化并核验 48 个执行/编辑输入文件；仅省略不参与本轮执行或修改的 `.gitignore`，发布时保留原 blob。全部 8 份历史快照、21 张项目卡、脚本、测试、配置和检查点均为原始 SHA 一致的文件，没有占位文件。较长 JSON 使用 UTF-8 blob 读取并在落盘后校验，无需 Base64 长串传抄。

原有 25 项单测通过；原始仓库 validate 通过，确认 21 个项目、8 份快照、27 条唯一事件。此次为交互式工程验证；维护数据提交与回执的真实结果另记 state/status.json，不据此新增 scheduled E2E 声明。既有历史验证段落保持为当时记录；当前执行规则以 AGENTS.md 和 maintenance.md 为准。


## 2026-10-02 Manifest 模式交互验证

新增 `scripts/manifest_validation.py` 与 `tests/test_manifest_validation.py`，不删除 legacy 全工作树路径。原有核心合成测试 25/25 通过；新增 8 项 manifest 合成测试 8/8 通过，合计 33 项。新增覆盖：Git tree 根/子树重建、truncated manifest 拒绝、历史 snapshot/index 集合或 blob 不一致拒绝、不落盘历史工作树的 prepare、幂等重试、无本地 snapshot 的 receipt，以及 changed path 必须真实物化。

初始 validation index 仅从固定 HEAD `935e443c0db6577cc3ea53852545f2156a3dae7b` 的 8 个既有 snapshot blob 构造；其 8 个 path/SHA、27 个稳定事件以及最新一轮 21/21 metadata/head/releases 覆盖与 2026-09-29 已记录的完整工作树验证结果一致。该索引只在完整 Git tree 的 snapshot path/blob 链保持一致时有效。

本次仍未执行任何被追踪上游项目代码，也不把交互式工程验证当作新的 scheduled E2E。恢复平台定时任务只表示调度恢复，下一次真实 scheduled 发布/回读结果仍由后续 run 的 commit/receipt 证明。


## 2026-10-07 API-native runtime 验收

针对此前 Scheduled 无法完成 GitHub connector → 本地文件系统 → Python 的跨工具交接，运行协议改为纯 GitHub API。当前基线 HEAD `21c3da019dc37a9349db9ef1404f003a4687101a` / tree `3372b76344a6e27e0ca08131f084acd5a01cdca6` 上进行了 API-only bootstrap 验收：

- recursive tree 明确 `truncated=false`，66 个 entry、54 个 blob；
- 将全部 54 个现有 blob path/mode/type/SHA 直接交给 GitHub `create_tree`（不使用 base tree），返回 tree SHA 与真实 root tree 完全一致；
- tree 中 8 个 snapshot 与 `state/validation-index.json` 的 8 个 snapshot 路径集合完全一致，8/8 blob SHA 一致；
- `data/projects.json` 中全部 tracked/reference card 均存在；
- 该验收没有使用 Python、本地文件系统、shell 联网、git clone 或历史附件。

因此 Scheduled 的启动/完整性阶段现在只依赖 GitHub connector。后续真实 scheduled data commit + receipt 仍需下一次计划运行实际成功后才能记为新的 scheduled E2E。

### 对 2026-10-02 测试记录的澄清

2026-10-02 段落中的“25/25 + 8/8”描述的是实现构造时的预期/合成验证结论，并没有可回读的 Scheduled Python 测试日志；不得把它当作 10 月 3–6 日失败任务实际执行了 33 项测试的证据。API-native 协议不依赖该测试执行结果；脚本测试只作为交互式工程变更的离线回归门禁。
