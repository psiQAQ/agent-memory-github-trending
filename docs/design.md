# 设计与入口

状态：默认方案已批准，首版实现；实际运行与验收状态见 `state/status.json`。决策记录见 [decisions.md](decisions.md)。

本项目不是按总 Star 排序的 Awesome List。它分别展示新发现、关注度净变化和实质技术进展。GPT 做研究判断，Python 做确定性检查，GitHub 保存跨会话状态。ChatGPT Scheduled 是唯一调度器，不配置常驻机器、模型 API key 或第二个调度平台。Scheduled runtime 采用 API-native 协议，不依赖 Python、本地文件系统或 git checkout。

## 组织方式参考

| 一手参考 | 本仓库采用的部分 |
| --- | --- |
| [best-of-lists/best-of](https://github.com/best-of-lists/best-of) | 结构化项目登记与生成视图分离，不复制不透明综合分数 |
| [trackawesomelist-source](https://github.com/trackawesomelist/trackawesomelist-source) | 同时按项目和时间组织内容 |
| [bonfy/github-trending](https://github.com/bonfy/github-trending) | 保存历史快照，但按年月分区而非根目录堆积 |
| [vitalets/github-trending-repos](https://github.com/vitalets/github-trending-repos) | 数据保存与通知分开；这里用 GPT 通知而非无限增长 Issue |
| [Agent-Memory-Paper-List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List) | 辅助研究分类和论文代码发现，不作为热度排行 |

## 文件职责

`AGENTS.md` 是执行边界；`config/tracker.json` 是已批准配置；`docs/methodology.md` 是统计方法；`docs/maintenance.md` 是执行手册；`docs/data-contract.md` 是输入格式。

`data/projects.json` 保存正式对象；`data/candidates.json` 保存未审查线索；`projects/` 保存当前说明；`data/snapshots/YYYY/MM/` 保存不可变观测、事件和查询；`state/validation-index.json` 保存这些已验证 snapshot 的紧凑 path/blob/统计索引；`state/checkpoints.json` 保存逐来源的成功游标；`state/status.json` 保存调度和验收事实。

`reports/current.md` 由脚本生成计数和增长视图；`reports/latest.md` 由 GPT 编写证据化分析；`reports/weekly/` 按已结束 ISO 周生成，未到期不创建空周报。首版把事件保存在快照内，使用稳定事件 ID 去重，不另存一份内容相同的月度事件文件。

`scripts/tracker.py` 保留核心数据契约与 legacy validate/render/prepare/receipt；`scripts/manifest_validation.py` 提供 validate-batch、validate-manifest 以及 manifest-aware prepare/receipt。`tests/test_tracker.py` 与 `tests/test_manifest_validation.py` 使用合成数据覆盖两条路径。脚本都不联网、不调用模型、不执行上游代码，也不持有 GitHub 凭据；连接器完成读写。

## GitHub API-native 引导

每轮固定默认分支 HEAD 和真实 tree SHA，取得完整目录索引。Scheduled 不再把 GitHub blob 搬到本地执行，而是在 GitHub API 层完成完整性证明和发布。

对于明确 `truncated=false` 的 recursive tree，用全部 blob path/mode/type/SHA 创建一个不带 base tree 的 orphan tree；GitHub 返回的 SHA 必须等于 pinned root tree SHA。这把“重建根 tree”从本地 Python 计算改成 GitHub 服务器端确定性验证。

`state/validation-index.json` 将历史 snapshot path 精确绑定到 Git blob SHA，并保存增长计算所需的紧凑 Stars 历史与 source coverage。完整 tree 仍是权威文件集合；index 只是 authenticated summary，任何 snapshot 路径或 SHA 不一致都会停止发布。

Scheduled 数据流：
`固定 HEAD/tree → recursive tree + GitHub-side create_tree 校验 → 必读文件 blob 对账 → validation-index/snapshot/card 对账 → GitHub API 采集 → 内存 batch 校验 → create_blob(snapshot/index/reports/cards) → create_tree(base_tree) → create_commit → update_ref(force=false) → readback → API-native receipt → 独立 receipt commit/readback`。

`scripts/tracker.py`、`scripts/manifest_validation.py` 和 tests 保留用于交互式开发、回归验证和协议参考，不是 Scheduled runtime dependency。Scheduled 不具备 Python/文件系统时仍属于受支持路径。

## 状态和限制

当前对话完成的读写和 Python 验证，仅能证明交互式路径。真实定时运行必须另行记录端到端验收。平台审批、连接权限变化或缺少 Python 都可能阻止运行；阻止时不更新成功游标，不声称无变化。

最初数值基线采用整批工具读取完成时间，非同一瞬间原子快照。首轮尚未逐项读取 Release/PR，已入后续队列。历史窗口不足不能外推。Git 历史随运行增长，分目录仅改善查找和上下文，不消除存储增长。

[ChatGPT Scheduled 官方说明](https://help.openai.com/en/articles/10291617-chatgpt-tasks)用于理解任务能力与审批边界；实际是否成功始终以工具回执和 Git 提交为准。不得默默切换到 GitHub Actions 或付费平台。
