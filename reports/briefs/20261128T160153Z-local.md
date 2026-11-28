# Agent Memory 简报｜2026-11-29

Hindsight Coding Agents v0.9.0 的标签已确认包含会话启动记忆配置。
OpenViking 合并了可配置的 Compile 状态存储。Letta Code v0.34.72 修复了监听器重试前对排队消息的处理。
准备切换 OpenViking Compile 后端时，先迁移现有配置和历史。Hindsight 用户可按 v0.9.0 核对启动时要载入的页面或 mental model。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [Hindsight](https://github.com/vectorize-io/hindsight/tree/integrations/coding-agents/v0.9.0) | 会话启动可载入指定页面和 mental model | Coding Agents v0.9.0 标签已确认 | 配置了启动上下文的团队可核对引用和客户端支持。 |
| [OpenViking](https://github.com/volcengine/OpenViking/commit/1e21e5396eeef334c29b5c31035a93668b84f8df) | Compile 配置和命名运行历史可使用关系数据库 | 已合并，发行包含关系待核实 | 切换存储前迁移现有配置和历史，并核对数据库前置条件。 |
| [Letta Code](https://github.com/letta-ai/letta-code/releases/tag/v0.34.72) | 监听器在符合条件的 provider 重试前合并一批排队消息 | v0.34.72 已发布 | 适用于通过监听器发送追加指令的会话。provider 流超时最多重试一次。 |

### 适用条件

**Hindsight**。启动配置支持页面和 mental model，读取正文时使用 5 秒超时参数。客户端须同时提供两种读取方法。单条读取失败或为空时，记录警告并略过该条。这里确认的是 Coding Agents 的 Git 标签，软件包分发仍待核实。该标签下也有一组真实 Claude Code 系统评测用例，以新 HOME、新代码目录和同一 memory bank 检查跨会话规则与纠正。用例需满足 macOS、已登录的 Claude Code 和评测服务条件，默认模型为 Opus。本轮只核对用例设计和入口。

**OpenViking**。默认使用原文件路径。SQLite、MySQL 和 PostgreSQL 可保存 Compile 配置与命名运行历史，Task/Work 的存储另行配置。SQLite 启动时建表，MySQL 与 PostgreSQL 需要预建表。切换后端不会自动搬迁旧数据，相关依赖缺失时服务报告配置错误。

**Letta Code**。监听器在退避后、重新发送前检查队列。部署中断恢复和 `noCoalesce` 模式跳过合并。停止信号可中断重试。流超时类错误最多重试一次，其他可重试 provider 错误仍采用三次上限，由错误分类决定是否重试。

## Star 变化

时间为 UTC，三组相邻观测均约 24.06 小时。本轮这三个项目均无落在 7 日 ±6 小时内的基线。30 日增量采用容差内最接近目标时刻的真实观测。

| 项目 | 前次观测 | 本次观测 | 本次 Stars | 相邻净变化 | 30 日基线（实际间隔） | 30 日净变化 |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Hindsight | 11-27 16:00:21 | 11-28 16:03:40 | 63967 | +158 | 10-29 16:33:55（29.979 日） | +7879 |
| OpenViking | 11-27 16:00:40 | 11-28 16:03:58 | 42974 | +46 | 10-29 19:11:51（29.870 日） | +1838 |
| Letta Code | 11-27 16:00:18 | 11-28 16:03:38 | 3928 | +5 | 10-29 16:33:32（29.979 日） | +192 |

## 新候选线索对比

下列机制来自搜索描述，公开实现、依赖和评测资产仍待核实。

| 线索 | 描述中的机制 | 许可证（搜索元数据） | 待核实 |
| --- | --- | --- | --- |
| [projectmem](https://github.com/riponcm/projectmem) | 记录尝试、修复和决策，通过本地 MCP 提醒宿主避免重复失败 | MIT | 提醒触发条件、数据落盘和宿主兼容性 |
| [pi-mm](https://github.com/tty-pt/pi-mm) | Pi 的持久化多分辨率记忆扩展 | BSD-2-Clause | 各分辨率的生成、淘汰和检索入口 |
| [meristem-bench](https://github.com/kaustubhsawant-it/meristem-bench) | 测量代码事实过期后，记忆工具是否还会返回旧事实 | Apache-2.0 | 任务固定版本、失效标注和评分方式 |

本轮覆盖 24 个登记项目的元数据、HEAD 和完整增量 Release，完成三个项目的静态审读。发现范围为两条无 Star 门槛查询的首页，共 40 条结果。未运行上游代码或评测。

<details markdown="1"><summary>证据与时间</summary>

批次 `20261128T160153Z-local`。来源观测截至 2026-11-28T16:04:27.474Z。表中实现结论等级均为 `code_inspected`。

- **Hindsight**。版本提交与注释标签分别为 2026-11-27T17:16:59Z、17:17:00Z，标签目标在 2026-11-28T16:07:33.505Z 核实。[标签](https://github.com/vectorize-io/hindsight/tree/integrations/coding-agents/v0.9.0) · [会话启动](https://github.com/vectorize-io/hindsight/blob/bd3ecdde448909a1b8af02a69c81618991a4c3f3/hindsight-integrations/coding-agents/src/core/session-start.ts#L438-L445) · [正文读取](https://github.com/vectorize-io/hindsight/blob/bd3ecdde448909a1b8af02a69c81618991a4c3f3/hindsight-integrations/coding-agents/src/core/session-context.ts#L42-L79) · [评测用例设计](https://github.com/vectorize-io/hindsight/blob/bd3ecdde448909a1b8af02a69c81618991a4c3f3/hindsight-system-evals/evals/coding_agents/test_coding_agents.py#L243-L281) · [环境判断](https://github.com/vectorize-io/hindsight/blob/bd3ecdde448909a1b8af02a69c81618991a4c3f3/hindsight-system-evals/hindsight_system_evals/coding_agents/sandbox.py#L86-L94)
- **OpenViking**。提交 2026-11-28T06:20:21Z，最后一份本项源码或配置证据返回于 2026-11-28T16:06:22.993Z。[合并提交](https://github.com/volcengine/OpenViking/commit/1e21e5396eeef334c29b5c31035a93668b84f8df) · [后端选择](https://github.com/volcengine/OpenViking/blob/1e21e5396eeef334c29b5c31035a93668b84f8df/openviking_cli/utils/config/storage_config.py#L252-L274) · [服务接线](https://github.com/volcengine/OpenViking/blob/1e21e5396eeef334c29b5c31035a93668b84f8df/openviking/service/core.py#L878-L899) · [迁移与依赖](https://github.com/volcengine/OpenViking/blob/1e21e5396eeef334c29b5c31035a93668b84f8df/docs/en/guides/01-configuration.md#compile-store)
- **Letta Code**。发行 2026-11-27T21:32:53Z，最后一份本项源码证据返回于 2026-11-28T16:08:17.071Z。[发行](https://github.com/letta-ai/letta-code/releases/tag/v0.34.72) · [原修复提交](https://github.com/letta-ai/letta-code/commit/c315f381db8b0d18512b7921f16182953a6e7c9a) · [监听入口](https://github.com/letta-ai/letta-code/blob/e8a2d05ecc6615f7fe1f8475a463ca61bc1103e1/src/websocket/listener/turn.ts#L674-L726) · [重试判定与消息合并](https://github.com/letta-ai/letta-code/blob/e8a2d05ecc6615f7fe1f8475a463ca61bc1103e1/src/websocket/listener/turn-send.ts#L113-L229)
- 两条搜索各返回 20 条，响应均有下一页。只从搜索描述初筛表中三条线索。

</details>
