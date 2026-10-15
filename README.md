# Agent Memory GitHub Trending

面向 Agent Memory 的中文技术观察站。GPT 负责发现、阅读与分析，GitHub API 用于定时运行的完整性校验与发布，Python 工具保留为离线参考；GitHub 保存证据与跨会话状态。这里不是 GitHub 官方榜单，也不以 Star 数认证项目质量。

## 从这里阅读

| 入口 | 内容 |
| --- | --- |
| [最新研究简报](reports/latest.md) | 本轮值得关注的机制与证据边界 |
| [当前观测表](reports/current.md) | 项目分类、真实计数、7/30 日可比较增长 |
| [项目登记表](data/projects.json) | 正式跟踪与历史参照，以及项目卡片路径 |
| [候选队列](data/candidates.json) | 尚未审查的新发现，不等于推荐 |
| [运行状态](state/status.json) | 实际启用、验证、最近提交与故障状态 |
| [执行规则](AGENTS.md) | GPT 每轮必须读取的权限和行为边界 |

## 当前覆盖

目前有 **20 个正式跟踪项目 + 1 个历史参照**，已达到初始正式跟踪目标；候选队列继续保留未审查线索，用于后续替补和新方向发现，不为扩大数量自动收录。

最新观测批次为 `20261014T160956Z-scheduled`（北京时间 2026-10-15 00:09:56），由交互式恢复完成发布。Metadata、默认分支 HEAD、Release 当前页均取得 21/21；Release 增量分页完整为 **17/21**，其余 4 个来源保留旧成功水位。历史发布未全量回灌。所有上游项目均未在本仓库运行安装或性能测试。7/30 日缺少足够历史观测时显示“—”，而不是 0 或推算值。

## 定时维护

已批准：ChatGPT **每天北京时间 00:00（Asia/Shanghai）**执行一次检查；UTC 保存原始时间，中文报告使用北京时间。日常数据和报告直写 `main`；后续规则和代码修改另行提议。重要技术变化、需处理故障、周报和首次定时验收才通知。

每轮按[已批准的 API-native 协议](docs/api-native-maintenance.md)固定 HEAD 与真实 tree，通过 GitHub 重建 tree、核对 snapshot/index、创建数据对象并逐 blob 回读，然后独立提交 receipt。离线 Python 工具不是 Scheduled 运行门禁。

2026-10-15 的 Scheduled 管理视图搜索不到原“Agent Memory 追踪”任务，原对话中的任务入口无法加载，当前启用状态待核实。批准的 cadence 仍为每天北京时间 00:00；本次没有重建或修改平台任务，也不以交互式恢复证明新的无人值守成功。历史验收与当前核实状态分别见[运行状态](state/status.json)。

## 方法和维护

[筛选统计方法](docs/methodology.md) · [维护操作手册](docs/maintenance.md) · [API-native 协议](docs/api-native-maintenance.md) · [外部评测参考](docs/references.md) · [定时任务描述](docs/scheduled-task-prompt.md) · [设计与决策](docs/design.md) · [已批准决策](docs/decisions.md) · [数据契约](docs/data-contract.md) · [验证记录](docs/validation.md)

快照按年月保存在 `data/snapshots/`，每个快照同时保存本轮事件和发现查询；事件以稳定 ID 去重。项目卡片保存当前理解，周报解释共同方向。README 不追加无穷日报。

本仓库不访问无关私有仓库，不公开聊天历史或个人资料，不执行上游代码，不自动扩大权限或引入费用。
