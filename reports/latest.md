# Agent Memory 简报｜2026-11-28

Cognee v1.6.11 更换本地默认嵌入模型，部分既有数据集会重新嵌入。
claude-mem v17.0.2 可跳过超长工具字段压缩。Hindsight 合并了会话启动上下文配置，OpenViking 合并了 pgvector 检索模式选择。
升级 Cognee 前先确认旧数据集的嵌入模型。使用 OpenViking pgvector 的团队可提前核对旧配置项。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [Cognee](https://github.com/topoteretes/cognee/releases/tag/v1.6.11) | 本地默认嵌入改用 pplx-embed-v1-0.6b | v1.6.11 已发布 | 依赖本地默认模型的部署，升级前先查现有数据集的嵌入模型记录。 |
| [claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v17.0.2) | 允许跳过超长工具字段的模型压缩 | v17.0.2 已发布 | 关闭压缩前，先确认能否接受工具输入或输出的中段被裁掉。 |
| [Hindsight](https://github.com/vectorize-io/hindsight/commit/2ae5fbe2ab0e1771db23c3bb04155cdb7471484e) | Coding Agents 会话启动可载入指定记忆页 | 已合并，发行包含关系待核实 | 使用启动上下文时，核对配置中的页面或 mental model ID。 |
| [OpenViking](https://github.com/volcengine/OpenViking/commit/1f19e59b8c07fd9ed98c3780f08af0b2ab3ffe74) | pgvector 检索支持显式选择 native 或 enhanced | 已合并，发行包含关系待核实 | 沿用老 pgvector 配置的部署，升级前检查旧开关和增强模式前置条件。 |

### 适用条件

**Cognee**。未显式配置嵌入、没有可用 LLM API key 且启用本地默认路径时，FastEmbed 默认用 `perplexity-ai/pplx-embed-v1-0.6b`。自动迁移默认开启，只重新嵌入明确记录由旧默认 `BAAI/bge-small-en-v1.5` 构建的独立数据集。只记录了维数而没有模型名的旧数据集会留在原状态，需确认来源后再决定沿用旧模型或手动重嵌。迁移中断后，已部分处理的数据集可从迁移入口续跑。

**claude-mem**。`CLAUDE_MEM_FIELD_CONDENSE_ENABLED` 默认开启。对配置了压缩器的观察路径，超过字符预算的字段才进入压缩分支。设为 `false` 时跳过这一次模型调用，由观察提示词按首尾裁剪。启用时，过长、超时或无可用压缩结果也可能走裁剪。观察请求仍按原流程生成。

**Hindsight**。`sessionContext` 默认为空，配置后按列出的顺序插入页面正文或 mental model 内容。会话启动钩子在客户端支持读取、且当前步骤可以附加上下文时执行，OpenCode 共用的持久运行入口在第一轮注入。单条读取带 5 秒超时参数，失败或为空会记录警告并略过该条。

**OpenViking**。`pgvector.search_implementation` 默认 `native`。`enhanced` 需要 PostgreSQL 17、增强扩展的 `ov_filtered_knn` envelope v1 能力和适用的 HNSW 索引。能力缺失或索引不支持时直接报错。旧 `filtered_knn` 和 `unfiltered_use_native` 设置会被配置校验拒绝，切换实现后需要重新初始化适配器。

## Star 变化

时间为 UTC。相邻观测相隔约 23.44 小时。7 日增量采用前后 6 小时容差内最接近目标时刻的观测。四个项目都没有合格的 30 日基线。

| 项目 | 前次观测 | 本次观测 | 本次 Stars | 相邻净变化 | 7 日基线（实际间隔） | 7 日净变化 | 30 日净变化 |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: |
| Cognee | 11-26 16:34:17 | 11-27 16:00:49 | 33672 | +25 | 11-20 16:03:06（6.998 日） | +241 | — |
| claude-mem | 11-26 16:33:36 | 11-27 16:00:09 | 120142 | +219 | 11-20 16:02:26（6.998 日） | +1570 | — |
| Hindsight | 11-26 16:33:48 | 11-27 16:00:21 | 63809 | +163 | 11-20 16:02:37（6.998 日） | +1594 | — |
| OpenViking | 11-26 16:34:07 | 11-27 16:00:40 | 42928 | +59 | 11-20 16:02:57（6.998 日） | +402 | — |

## 新候选线索对比

以下线索来自仓库搜索描述，公开实现与评测资产待核实。

| 线索 | 描述中的记忆机制 | 许可证（搜索元数据） | 待核实 |
| --- | --- | --- | --- |
| [RE-call](https://github.com/GiulioDER/RE-call) | SQLite 或自托管 PostgreSQL，带来源与拒答阈值的记忆检索 | AGPL-3.0 | 阈值如何校准，拒答如何传回宿主 |
| [mem-agents](https://github.com/drly77/mem-agents) | Claude Code 会话检索，组合 SQLite FTS5、本地向量与重排 | MIT | 会话刷新方式及模型是否全程本地 |
| [stale-recall-bench](https://github.com/alchimestre/stale-recall-bench) | 用固定 SWE-bench 任务测编码 Agent 是否召回过期记忆 | MIT | 任务版本、过期标注及评分实现 |

本轮覆盖 24 个登记项目的元数据、HEAD 和完整增量 Release，深读四项变化。发现范围为两条无 Star 门槛查询的首页，共 35 条原始结果。结论来自固定版本的静态源码，未运行上游实现或基准。

<details markdown="1"><summary>证据与时间</summary>

批次 `20261127T155901Z-local`。采集结束于 2026-11-27T16:01:12.217Z。四项证据等级均为 `code_inspected`。

- **Cognee**。发行 2026-11-26T17:05:51Z，本项最后一条源码或标签回执 2026-11-27T16:03:37.386Z。[发行说明](https://github.com/topoteretes/cognee/releases/tag/v1.6.11) · [配置](https://github.com/topoteretes/cognee/blob/c78a56ff4a705a6f46090a1fe6a3a9737f45e17b/cognee/infrastructure/databases/vector/embeddings/config.py#L229-L242) · [迁移条件与失败处理](https://github.com/topoteretes/cognee/blob/c78a56ff4a705a6f46090a1fe6a3a9737f45e17b/cognee/modules/migrations/versions/reembed_local_default_embedding_model.py) · [自动迁移入口](https://github.com/topoteretes/cognee/blob/c78a56ff4a705a6f46090a1fe6a3a9737f45e17b/cognee/modules/migrations/startup.py#L400-L456)
- **claude-mem**。发行 2026-11-26T20:45:45Z，本项最后一条源码或标签回执 2026-11-27T16:03:32.739Z。[发行说明](https://github.com/thedotmack/claude-mem/releases/tag/v17.0.2) · [Claude 观察入口](https://github.com/thedotmack/claude-mem/blob/019a36df177c9e952a125d9be4a32e23dd59cbf9/src/services/worker/ClaudeProvider.ts#L1389-L1415) · [字段压缩判定](https://github.com/thedotmack/claude-mem/blob/019a36df177c9e952a125d9be4a32e23dd59cbf9/src/services/worker/field-optimizer.ts#L151-L224) · [配置默认值](https://github.com/thedotmack/claude-mem/blob/019a36df177c9e952a125d9be4a32e23dd59cbf9/src/shared/SettingsDefaultsManager.ts#L776)
- **Hindsight**。提交 2026-11-27T13:56:37Z，本项最后一条源码或标签回执 2026-11-27T16:02:49.415Z。[合并记录](https://github.com/vectorize-io/hindsight/commit/2ae5fbe2ab0e1771db23c3bb04155cdb7471484e) · [引用解析和读取](https://github.com/vectorize-io/hindsight/blob/2ae5fbe2ab0e1771db23c3bb04155cdb7471484e/hindsight-integrations/coding-agents/src/core/session-context.ts#L15-L80) · [启动钩子](https://github.com/vectorize-io/hindsight/blob/2ae5fbe2ab0e1771db23c3bb04155cdb7471484e/hindsight-integrations/coding-agents/src/core/session-start.ts#L438-L445) · [持久运行入口](https://github.com/vectorize-io/hindsight/blob/2ae5fbe2ab0e1771db23c3bb04155cdb7471484e/hindsight-integrations/coding-agents/src/core/runtime.ts#L243-L249)
- **OpenViking**。提交 2026-11-27T08:53:41Z，本项最后一条源码或标签回执 2026-11-27T16:02:51.239Z。[合并记录](https://github.com/volcengine/OpenViking/commit/1f19e59b8c07fd9ed98c3780f08af0b2ab3ffe74) · [pgvector 配置指南](https://github.com/volcengine/OpenViking/blob/1f19e59b8c07fd9ed98c3780f08af0b2ab3ffe74/docs/en/guides/25-pgvector.md#L123-L159) · [索引与模式判定](https://github.com/volcengine/OpenViking/blob/1f19e59b8c07fd9ed98c3780f08af0b2ab3ffe74/openviking/storage/vectordb_adapters/pgvector_adapter.py#L52-L78) · [初始化能力检查](https://github.com/volcengine/OpenViking/blob/1f19e59b8c07fd9ed98c3780f08af0b2ab3ffe74/openviking/storage/vectordb_adapters/pgvector_adapter.py#L445-L516)

- claude-mem v17.0.2 注释标签剥离到 `019a36df177c9e952a125d9be4a32e23dd59cbf9`。Cognee v1.6.11 标签直接指向 `c78a56ff4a705a6f46090a1fe6a3a9737f45e17b`。
- Hindsight 与 OpenViking 的完整增量 Release 未出现包含复核提交的新发行证据。Cognee 的 HEAD 对比达到 300 个文件的返回上限，本轮只深读标签内的嵌入迁移。
- 分页覆盖：宽查询第一页返回 20 条且还有后续页。新建项目查询第一页返回 15 条，响应无下一页。

</details>
