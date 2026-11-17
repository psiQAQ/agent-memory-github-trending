# Tin11Mn/chrono-hybrid-mem

源于记忆挑战赛的证据检索系统，按用户存储会话，返回可追溯的原文片段。

## 记忆机制

[FastAPI 的 Add/Search 入口](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/app/main.py)调用 [MemoryStore](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/app/storage.py)，用 SQLite 保存会话原文，用 FTS5 索引消息、事实与上下文。Search 按用户范围召回证据，可由[模型适配器](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/app/model.py)做查询规划和重排。证据图与提及锚点都有独立开关，证据图默认关闭。参见[图路由实现](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/app/graph_routing.py)。

## 部署和依赖

Python/FastAPI 与支持 FTS5 的 SQLite。未配置 OpenAI API key 时标准服务仍有词法路径，若显式设置 `MEMORY_REQUIRE_MODEL=true`，缺密钥会在[配置入口](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/app/model.py)报错。本地语义和模型选项见[固定 README](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/README.en.md)，当前 HEAD 与公开比赛 Release 分开记录。

## 评测证据

从 [MemDev-Bench v1 附录 F 表 9](https://arxiv.org/html/2610.27524v1) 的参评名单发现。[参评版本说明](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/README.en.md)将第一周期文字记忆参赛结果对应到 `v0.2.0`。[组织方榜单](https://agentmemoryleaderboard.ai/home)和[仓库 LoCoMo 检索脚本](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/scripts/evaluate_locomo_retrieval.py)分别提供参评和后续本地研究线索。本卡不把后续实验结果合并为正式榜单成绩。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / research |
| 仓库 ID | 1326480520 |
| 创建时间（UTC） | 2026-08-07T09:37:45Z |
| 首次发现（UTC） | 2026-11-17T08:45:30.725Z |
| 首次公开 | 未核实 |
| 审读版本 | [固定提交](https://github.com/Tin11Mn/chrono-hybrid-mem/tree/a8411527aa803f84b984227a455fd51ba193de1f)，证据观察至 2026-11-17T08:47:59.197Z |
| 观察到的 GitHub Release | [v0.2.0](https://github.com/Tin11Mn/chrono-hybrid-mem/releases/tag/v0.2.0)，发布于 2026-08-07T10:13:37Z |
| 许可证 | [固定版本 LICENSE](https://github.com/Tin11Mn/chrono-hybrid-mem/blob/a8411527aa803f84b984227a455fd51ba193de1f/LICENSE)，GitHub API 识别为 MIT |
| 证据等级 | code_inspected；尚无本仓库运行或评测结果 |

Release 记录用于建立跟踪基线。每日采集将分别记录元数据、默认分支 HEAD 和完整增量 Release。
