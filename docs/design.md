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

`data/projects.json` 保存正式对象；`data/candidates.json` 保存未审查线索；`projects/` 保存当前说明；`data/snapshots/YYYY/MM/` 保存不可变观测、事件和查询；`state/validation-index.json` 保存这些已验证 snapshot 的紧凑 path/blob/统计索引；`state/checkpoints.json` 保存逐来源的成功游标；`state/status.json` 保存调度和验收事实。

`reports/current.md` 由脚本生成计数和增长视图；`reports/latest.md` 由 GPT 编写证据化分析；`reports/weekly/` 按已结束 ISO 周生成，未到期不创建空周报。首版把事件保存在快照内，使用稳定事件 ID 去重，不另存一份内容相同的月度事件文件。

`scripts/tracker.py` 保留核心数据契约与 legacy validate/render/prepare/receipt；`scripts/manifest_validation.py` 提供 validate-batch、validate-manifest 以及 manifest-aware prepare/receipt。`tests/test_tracker.py` 与 `tests/test_manifest_validation.py` 使用合成数据覆盖两条路径。脚本都不联网、不调用模型、不执行上游代码，也不持有 GitHub 凭据；连接器完成读写。

## GitHub API Manifest 引导

每轮仍先固定默认分支 HEAD 和真实 tree SHA，并取得完整目录索引。区别是：完整性证明保存在当轮临时 manifest，而不是要求把完整执行依赖全部复制进本地目录。

manifest 模式只落盘当前程序实际执行和修改的少量输入。校验器根据完整 blob 索引重算全部子 tree/根 tree SHA，检查项目卡存在性，并用 `state/validation-index.json` 将全部历史 snapshot path 精确绑定到各自 Git blob SHA。这样增长统计和事件去重使用 index 摘要，而原始历史仍由不可变 snapshot blob 保留。

新数据流：
`固定 HEAD/tree → 完整 tree manifest → 校验最小输入 + validation index → unit tests → validate-batch → 采集/prepare → 人工证据更新 → validate-manifest(全部 changed paths) → 基于完整 base tree 发布 → 回读 changed blobs → 为数据 commit 重建 manifest → manifest-aware receipt → 单独回执提交`。

index 不是缓存逃生口：任一历史 snapshot 被修改、遗漏或增加但未登记，都会因 tree/path/blob 不一致而失败。index 缺失或冲突时只能停止发布，或显式回退到完整工作树并重新验证历史后重建。发布前 HEAD 移动仍最多协调重试一次。

## 状态和限制

当前对话完成的读写和 Python 验证，仅能证明交互式路径。真实定时运行必须另行记录端到端验收。平台审批、连接权限变化或缺少 Python 都可能阻止运行；阻止时不更新成功游标，不声称无变化。

最初数值基线采用整批工具读取完成时间，非同一瞬间原子快照。首轮尚未逐项读取 Release/PR，已入后续队列。历史窗口不足不能外推。Git 历史随运行增长，分目录仅改善查找和上下文，不消除存储增长。

[ChatGPT Scheduled 官方说明](https://help.openai.com/en/articles/10291617-chatgpt-tasks)用于理解任务能力与审批边界；实际是否成功始终以工具回执和 Git 提交为准。不得默默切换到 GitHub Actions 或付费平台。
