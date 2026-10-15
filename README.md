# Agent Memory Observatory

面向选型、接入和研究的 Agent Memory 中文观察站。先说明技术变化对谁有影响、是否需要行动，再提供真实 Star 观测和可追溯证据。不是 GitHub 官方榜单，不以关注度认证项目质量。

**[进入观察站](https://notes.psiqaq.cn/agent-memory-github-trending/)** · [趋势仪表盘](https://notes.psiqaq.cn/agent-memory-github-trending/dashboard.html#view=projects) · [独立阅读归档](https://notes.psiqaq.cn/agent-memory-github-trending/archive.html)

## 从这里阅读

| 入口 | 内容 |
| --- | --- |
| [最新研究简报](reports/latest.md) | 三行要点、变更影响、Star 区间与候选比较 |
| [生态与选型路线](reports/landscape.md) | 存储、服务、宿主、评测四层视角与技术时间线 |
| [当前观测表](reports/current.md) | 项目分类、实际计数及覆盖范围 |
| [项目登记](data/projects.json) | 正式跟踪、历史参照与项目卡 |
| [候选队列](data/candidates.json) | 尚未完成审查的线索，不等于推荐 |
| [开放数据](docs/open-data.md) | 原始 JSON、快照索引与 CSV 导出说明 |
| [运行状态](state/status.json) | 来源覆盖、最近已验证提交、待办及最新运行指标 |

## 如何理解这些记录

工程、研究代码、评测和历史参照分开看；静态代码阅读不等于运行效果验证。7/30 日指标只有存在目标时刻 ±6 小时内的真实基线才显示，短时区间不外推。每条实质结论保留一手来源及版本，完整证据可在静态阅读页展开。

[筛选统计方法](docs/methodology.md) · [术语与证据等级](docs/glossary.md) · [外部评测参考](docs/references.md) · [项目编辑偏好](docs/project-preferences.md)

## 自动维护与数据

已批准的采集安排为每天北京时间 00:00（Asia/Shanghai），由 ChatGPT Scheduled 按 [API-native 协议](docs/api-native-maintenance.md)执行；是否真正成功，以实际数据提交、回读与独立 Receipt 为准，不以日程已创建代替无人值守验收。

原始快照保存在 `data/snapshots/`；运行指标历史保存在 `state/run-metrics/`（有成功记录后生成），`state/status.json` 只保留最新摘要。正文、原始 JSON、Markdown 和独立静态页面来自同一仓库；浏览器 JavaScript 仅增强筛选、图表和阅读工具。

本仓库不访问无关私有仓库、不公开聊天历史或个人资料、不执行上游研究代码、不自动增加权限或费用。普通无变化不发研究通知；重要变化、周报、验收及需处理故障按已保存任务规则通知。

## 维护者入口

[执行规则](AGENTS.md) · [维护手册](docs/maintenance.md) · [数据契约](docs/data-contract.md) · [定时任务描述](docs/scheduled-task-prompt.md) · [网站设计与发布](docs/website.md) · [设计文档](docs/design.md) · [批准决策](docs/decisions.md) · [验证记录](docs/validation.md)
