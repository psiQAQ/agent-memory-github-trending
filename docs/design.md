# 设计与入口

状态：默认方案已批准，首版实现；实际运行与验收状态见 `state/status.json`。决策记录见 [decisions.md](decisions.md)。

本项目不是按总 Star 排序的 Awesome List。它分别展示新发现、关注度净变化和实质技术进展。GPT 做研究判断，Python 做确定性检查，GitHub 保存跨会话状态。ChatGPT Scheduled 是唯一调度器，不配置常驻机器、模型 API key 或第二个调度平台。

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

`data/projects.json` 保存正式对象；`data/candidates.json` 保存未审查线索；`projects/` 保存当前说明；`data/snapshots/YYYY/MM/` 保存不可变观测、事件和查询；`state/checkpoints.json` 保存逐来源的成功游标；`state/status.json` 保存调度和验收事实。

`reports/current.md` 由脚本生成计数和增长视图；`reports/latest.md` 由 GPT 编写证据化分析；`reports/weekly/` 按已结束 ISO 周生成，未到期不创建空周报。首版把事件保存在快照内，使用稳定事件 ID 去重，不另存一份内容相同的月度事件文件。

`scripts/tracker.py` 是唯一执行实现，提供 validate/render/prepare/receipt；`tests/test_tracker.py` 使用合成数据测试边界。脚本不联网、不调用模型、不执行上游代码，也不持有 GitHub 凭据；连接器完成读写。

## GitHub API 工作树引导

维护运行不把 `git clone` 作为可信根。每轮先固定默认分支 HEAD，读取该 commit 的 `tree.sha`，再通过 Git Data recursive tree 枚举完整路径；只有 `truncated=false` 才继续。随后逐 blob 物化到一次性本地目录，并按 Git blob 对象格式重新计算 SHA；路径集合、数量和每个 blob SHA 全部与 pinned tree 对齐后，这个目录才成为本轮测试、prepare 和 validate 的工作树。

数据发布走相反方向：从已验证本地输出创建 blob/tree/commit，以发布瞬间最新 commit 的真实 tree SHA 为 base tree，并用非强制 ref 更新提交。若默认分支在 bootstrap 与发布之间移动，先基于新 HEAD 重建/协调并重新验证；发布后再逐路径回读 blob SHA，最后才运行 receipt。因而“容器不能直接访问 github.com 或不能 git clone”本身不是阻断条件；真正的阻断条件是无法取得完整 tree/blob、无法在本地执行确定性校验，或没有已授权的 GitHub 写能力。

数据流为：`default ref → pinned commit/tree → recursive tree + blobs → SHA-verified temporary worktree → tests/prepare/validate → create_blob/tree/commit → force=false ref update → blob readback → receipt`。

## 状态和限制

当前对话完成的读写和 Python 验证，仅能证明交互式路径。真实定时运行必须另行记录端到端验收。平台审批、连接权限变化或缺少 Python 都可能阻止运行；阻止时不更新成功游标，不声称无变化。

最初数值基线采用整批工具读取完成时间，非同一瞬间原子快照。首轮尚未逐项读取 Release/PR，已入后续队列。历史窗口不足不能外推。Git 历史随运行增长，分目录仅改善查找和上下文，不消除存储增长。

[ChatGPT Scheduled 官方说明](https://help.openai.com/en/articles/10291617-chatgpt-tasks)用于理解任务能力与审批边界；实际是否成功始终以工具回执和 Git 提交为准。不得默默切换到 GitHub Actions 或付费平台。
