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
