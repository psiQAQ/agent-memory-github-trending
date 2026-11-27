# Agent Memory 简报｜2026-11-27

claude-mem v17 新增 macOS 聊天观察器。Letta Code v0.34.71 新增当前会话的子代理列表。
Hindsight 合并了会话补写修复，OpenViking 和 Graphiti 分别调整了共享资源的派生更新与 Neo4j 全文检索。
启用聊天观察前先核对选择范围。依赖云端子代理历史或会话补写的团队，应确认后端与会话保留设置。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v17.0.0) | macOS Messages 增加按聊天选择的观察器 | v17.0.0 已发布 | 确认选中的聊天及其写入项目。使用 Photon 时另行核对专用线路和群成员范围。 |
| [Letta Code](https://github.com/letta-ai/letta-code/releases/tag/v0.34.71) | ListAgents 可查看当前会话的子代理状态 | v0.34.71 已发布 | 依赖重启后查询状态的团队，先确认当前会话走 Letta Cloud API。 |
| [Hindsight](https://github.com/vectorize-io/hindsight/commit/cd69d2553b5c2d24aae8899f8dcae57849ae2687) | Coding Agents 可在后续会话补写失败的会话记录 | 已合并，发行包含关系待核实 | 排查会话缺失时检查原 transcript、bank 的保留设置和 Stop hook 日志。 |
| [OpenViking](https://github.com/volcengine/OpenViking/commit/bac07e493fa9d717e64eac6bd408414fdecbe2c1) | 修正受信维护身份读写共享资源后的派生更新 | 已合并，发行包含关系待核实 | 维护任务若显示文件已写入，仍可检查向量与 L0/L1 任务是否完成。 |
| [Graphiti](https://github.com/getzep/graphiti/commit/c685bab084d9ce40bae52dac5f0531f10506f7d7) | Neo4j 全文查询统一多组过滤与文本条件 | 已合并，发行包含关系待核实 | 使用 Neo4j 多组检索时，可在采用含修复的版本后验证既有结果。 |

### 适用条件

**claude-mem**。本地 Messages 入口需要 macOS 完全磁盘访问权限。观察器从开始监听后的新消息取数，按选择的聊天交给 Claude-Mem worker。取消选择后，尚未提交的消息窗口会按原选择标识丢弃，即使随后迅速重新勾选。应用保存取消选择失败时暂停监听。Photon 路径使用另行授权的线路和群成员关系。

**Letta Code**。Letta Cloud API 分支为非默认会话写入子代理生命周期，按会话和状态分页读取。其他后端从进程内状态列出匹配父会话的子代理。写入创建或状态更新失败时客户端记录调试日志，子代理的执行仍可继续。发布标签指向的提交可沿父链追溯到这项变更。

**Hindsight**。启用会话保留且本次 Stop hook 有客户端时，它先处理当前会话，再尝试重放同一宿主中留下待补写游标的其他会话。候选须空闲至少 30 分钟且不超过 3 天，原 transcript 仍须存在，并受宿主时间预算及目标 bank 配置约束。补写再次失败会保留待办，等后续 Stop hook 处理。

**OpenViking**。写入队列会重建请求上下文，再按变更计划触发派生工作。该提交修改 GLOBAL 读取授权，只在受信维护已有 ACL 绕过能力且目标全部在共享资源范围时沿用原上下文。读取私有隐私规则时会恢复常规访问控制。派生任务的完成结果仍由队列单独汇报。

**Graphiti**。Neo4j 实现把备选分组作为一个整体与文本条件结合，搜索入口仍保留对应的 group_id 过滤。查询长度上限和无分组输入的处理仍各自保留。本轮只核对 Neo4j 与通用构造入口的源码。

## Star 变化

相邻净变化按每个项目两次实际观测计算。7 日和 30 日的基线采用目标时刻前后 6 小时内最近的实际观测。时间为 UTC。

| 项目 | 前次观测 | 本次观测 | 相隔小时 | 本次 Stars | 相邻净变化 | 7 日净变化 | 30 日净变化 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| claude-mem | 11-25 15:59:37 | 11-26 16:33:36 | 24.57 | 119923 | +220 | +1553 | — |
| Letta Code | 11-25 15:59:45 | 11-26 16:33:45 | 24.57 | 3919 | +4 | +43 | — |
| Hindsight | 11-25 15:59:48 | 11-26 16:33:48 | 24.57 | 63646 | +308 | +1642 | — |
| OpenViking | 11-25 16:00:07 | 11-26 16:34:07 | 24.57 | 42869 | +105 | +395 | — |
| Graphiti | 11-25 15:59:31 | 11-26 16:33:30 | 24.57 | 33113 | +28 | +170 | — |

## 新候选线索对比

机制来自搜索结果的项目描述，三条线索均待核对公开实现。

| 线索 | 描述中的记忆机制 | 待核实 |
| --- | --- | --- |
| [episodic-memory-demo](https://github.com/manishw7/episodic-memory-demo) | SQLite 来源记录、语义检索和生命周期管理。 | 检索入口、所称 51 个用例的测试内容。 |
| [kcp-memory](https://github.com/Cantara/kcp-memory) | 把 Claude Code 会话索引到 SQLite FTS5。 | 会话更新、删除与再索引策略。 |
| [yb-zhai/agent-memory](https://github.com/yb-zhai/agent-memory) | 本地多路召回，提供 MCP 入口。 | 存储格式与各召回通道的实现。 |

## 方法与覆盖边界

24 个登记项目的元数据、HEAD 与增量 Release 均取得完整结果。两个无 Star 门槛的查询各取首页，共返回 40 条。五个变更区间各选读一项实现，OpenViking 的比较列表达到 300 文件上限，所选提交另用前后两棵完整树定位文件。未新增正式跟踪项目。本轮证据来自公开发行和静态审读。

<details markdown="1"><summary>证据与时间</summary>

批次 `20261126T163301Z-local`，批次观测时刻 2026-11-26T16:34:42.580Z。

- claude-mem，变更或发行 UTC 2026-11-26T04:56:41Z，固定来源观测截至 2026-11-26T16:40:25.456Z。[变更记录](https://github.com/thedotmack/claude-mem/releases/tag/v17.0.0) · [监听入口](https://github.com/thedotmack/claude-mem/blob/94474143a3d5bb6f1f25d8049194d675d724310e/src/npx-cli/commands/imessage-mac.ts#L168-L232) · [排队前后核对选择](https://github.com/thedotmack/claude-mem/blob/94474143a3d5bb6f1f25d8049194d675d724310e/src/integrations/imessage-observer/observer.ts#L253-L299) · [保存取消选择失败](https://github.com/thedotmack/claude-mem/blob/94474143a3d5bb6f1f25d8049194d675d724310e/integrations/imessage-mac/Sources/ClaudeMemMessages/AppModel.swift#L236-L260)
- Letta Code，变更或发行 UTC 2026-11-26T06:53:25Z，固定来源观测截至 2026-11-26T16:37:54.020Z。[变更记录](https://github.com/letta-ai/letta-code/releases/tag/v0.34.71) · [生命周期写入条件](https://github.com/letta-ai/letta-code/blob/ed518ca012cc62dfc5841590f2f611ba8de0d209/src/tools/impl/subagent-persistence.ts#L13-L51) · [列表的云端与本地分支](https://github.com/letta-ai/letta-code/blob/ed518ca012cc62dfc5841590f2f611ba8de0d209/src/tools/impl/list-agents.ts#L25-L113) · [云端写入失败处理](https://github.com/letta-ai/letta-code/blob/ed518ca012cc62dfc5841590f2f611ba8de0d209/src/backend/api/subagents.ts#L97-L130)
- Hindsight，变更或发行 UTC 2026-11-26T11:31:35Z，固定来源观测截至 2026-11-26T16:37:57.747Z。[变更记录](https://github.com/vectorize-io/hindsight/commit/cd69d2553b5c2d24aae8899f8dcae57849ae2687) · [候选、配置和重放](https://github.com/vectorize-io/hindsight/blob/cd69d2553b5c2d24aae8899f8dcae57849ae2687/hindsight-integrations/coding-agents/src/core/retain-hook.ts#L187-L268) · [Stop hook 接入](https://github.com/vectorize-io/hindsight/blob/cd69d2553b5c2d24aae8899f8dcae57849ae2687/hindsight-integrations/coding-agents/src/core/retain-hook.ts#L319-L374) · [游标回退条件](https://github.com/vectorize-io/hindsight/blob/cd69d2553b5c2d24aae8899f8dcae57849ae2687/hindsight-integrations/coding-agents/src/core/retain-cursor.ts#L22-L87)
- OpenViking，变更或发行 UTC 2026-11-26T05:41:34Z，固定来源观测截至 2026-11-26T16:41:23.746Z。[变更记录](https://github.com/volcengine/OpenViking/commit/bac07e493fa9d717e64eac6bd408414fdecbe2c1) · [共享资源读取范围](https://github.com/volcengine/OpenViking/blob/bac07e493fa9d717e64eac6bd408414fdecbe2c1/openviking/storage/viking_fs/_access.py#L207-L237) · [隐私规则的读取上下文](https://github.com/volcengine/OpenViking/blob/bac07e493fa9d717e64eac6bd408414fdecbe2c1/openviking/privacy/sanitizer.py#L141-L168) · [派生任务队列入口](https://github.com/volcengine/OpenViking/blob/bac07e493fa9d717e64eac6bd408414fdecbe2c1/openviking/storage/queuefs/content_write_processor.py#L353-L386)
- Graphiti，变更或发行 UTC 2026-11-25T20:00:00Z，固定来源观测截至 2026-11-26T16:38:01.625Z。[变更记录](https://github.com/getzep/graphiti/commit/c685bab084d9ce40bae52dac5f0531f10506f7d7) · [Neo4j 全文条件与过滤入口](https://github.com/getzep/graphiti/blob/c685bab084d9ce40bae52dac5f0531f10506f7d7/graphiti_core/driver/neo4j/operations/search_ops.py#L54-L98) · [通用构造入口](https://github.com/getzep/graphiti/blob/c685bab084d9ce40bae52dac5f0531f10506f7d7/graphiti_core/search/search_utils.py#L85-L107)

| 项目 | 7 日基线 UTC | 实际小时 | 30 日基线 UTC | 实际小时 |
| --- | --- | ---: | --- | ---: |
| claude-mem | 2026-11-19T16:29:48.530Z | 168.06 | — | — |
| Letta Code | 2026-11-19T16:29:56.994Z | 168.06 | — | — |
| Hindsight | 2026-11-19T16:29:59.876Z | 168.06 | — | — |
| OpenViking | 2026-11-19T16:30:19.067Z | 168.06 | — | — |
| Graphiti | 2026-11-19T16:29:42.539Z | 168.06 | — | — |

</details>
