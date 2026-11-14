# volcengine/OpenViking

以 `viking://` 虚拟文件系统组织资源、用户记忆与技能，在会话提交后抽取和演化长期记忆。

## 机制

上游将 `resources`、`memories`、`skills` 等统一到虚拟文件系统；L0/L1/L2 分层用于先读摘要再按需加载细节。Session commit 后可进行记忆抽取和演化。

## Coding Agent / 部署

上游明确维护 Claude Code、Codex、Cursor、OpenClaw、Hermes、OpenCode、Pi 等集成，并提供 Python 包、服务端、CLI、SDK 与本地/云模型配置路线。这里未验证完整离线运行。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | context_database / coding_agent / memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `54d4c0fac91fae976325ebed618d7278ff9b5c77` |
| HEAD 观察（UTC） | 2026-10-28T03:36:54.304Z |
| 许可证 | GitHub API 识别为 AGPL-3.0；未作法律审查 |
| 证据等级 | 固定版本 Experience Memory 实现为 code_inspected；最近 Release 为 upstream_statement；未运行上游代码 |

## 已检查的实现证据

- [`ov-experience-memory`](https://github.com/volcengine/OpenViking/blob/4bccb1294c013e1485c72377afcbba5ffc435cc7/agent-plugins/skills/ov-experience-memory/SKILL.md)：新增面向可执行任务的 Experience Memory skill。它要求在 coding、文件/数据修改、配置、部署、工作流执行或失败恢复前按需搜索当前用户的 Experience root，再读取少量高相关经验；经验只作为 advisory guidance，当前用户请求、当前环境和真实工具结果仍具有更高优先级。
- 该 skill 对 Codex、Claude Code、OpenCode、OpenClaw 等运行时映射不同 search/read 工具名，并限制一次初始检索和至多一次基于新失败证据的补充检索，避免无限扩张记忆搜索。
- 对应固定版本与其前次记录相比共有 25 个新增提交；diff 还包含 skill package retrieval、memory template、semantic queue/DAG、Hermes plugin 与可靠性测试等工程变化。

## Release 水位

此前已记录的 SDK Release 为 [`python-sdk@0.1.12`](https://github.com/volcengine/OpenViking/releases/tag/python-sdk@0.1.12)，发布时间 2026-09-18T10:17:32Z。该 SDK Release 未提供单独的机制结论；Experience Memory 的实现证据绑定到上面的固定版本。

## 证据边界

[已检查实现版本](https://github.com/volcengine/OpenViking/tree/4bccb1294c013e1485c72377afcbba5ffc435cc7)。未执行上游代码，也未复现任何 benchmark 数值。

## 最近核实的发布

v0.5.0 发布 Gateway Beta，通过模型协议代理检索并注入记忆，保存对话以供后续抽取；Working Memory 默认关闭，仍保留原始消息归档与长期记忆抽取。宿主插件需要单独升级，显式开启旧策略的部署也需核对升级后的实际配置。

Gateway、服务端与宿主插件是不同部署环节；本仓库未安装或运行。该版本的 Working Memory 默认值及兼容性说明来自正式 Release。

[v0.5.0 官方 Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.0)；发布（UTC）：2026-10-09T15:46:55Z；观察（UTC）：2026-10-15T04:56:27Z；此段证据等级：`upstream_statement`。

## 最近检查的实现与发布状态

新增 Redis expiry 调度与会话适配器，按到期时间处理空闲 session，并复用既有提交路径；默认仍为 legacy backend。该能力已合并、尚未发布，未验证多进程故障恢复、吞吐或 Windows 运行。

状态：`merged_unreleased`。[PR #6046](https://github.com/volcengine/OpenViking/pull/6046)，合并 commit `89fbcb96822c6aaab2828395b9f65e91846de001`；事件（UTC）2026-10-15T03:42:40Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/service/session_expiry.py) · [实现 2](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/scheduling/expiry/config.py)

StoreEngineProxy 的 write/delete/clear/两个 batch 入口开始检查原生返回状态，非零状态抛出 RuntimeError；这防止底层未持久化时上层仍返回成功 ID。该修复已合并、尚未发布；PR 中的测试和真实 I/O 复现属于上游声明，本仓库没有重复运行。

状态：`merged_unreleased`。[PR #5803](https://github.com/volcengine/OpenViking/pull/5803)，合并 commit `f75b6141dc477d7f35049fb1782c937bfc29a60c`；事件（UTC）2026-10-15T08:12:47Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/volcengine/OpenViking/blob/ec56b9443750c2f11418d0301aa8343daeb999d3/openviking/storage/vectordb/store/local_store.py)

Release 增量已覆盖到上次成功采集位置；这不代表全部历史发布已收集，也不代表已独立验证上游测试。

## 2026-10-20 升级警告：v0.5.1

- 正式 Release 包含集成 Gateway、隐私字段引用与显式解引用、多图检索、Session 后台任务修复、可选分布式/多写存储等。
- **兼容性要求：** `write(mode="create")` 不再保护已有正文，而是 replace 兼容别名；移除独立 Session extract 和服务端/SDK 等待专用 timeout；Gateway 路径、管理密钥与加密迁移存在破坏性变化，多写存储 V2 不保证旧版本直接回滚。升级前需备份存储并检查调用方防覆盖假设。
- 来源：[v0.5.1 Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.1)，2026-10-19T13:37:45Z；[迁移说明](https://github.com/volcengine/OpenViking/blob/v0.5.1/docs/zh/guides/22-gateway-operations.md)。状态：`released`；证据等级 `upstream_statement`，未独立运行数据迁移验证。
## 2026-10-24 新 Release：v0.5.2

- v0.5.2（2026-10-23T12:43:54Z）发布：Session 隐私树、记忆抽取重试、增量 compile 与 durable content write task；迁移要求涉及 LangChain 独立包、Working Memory 默认关闭、Watch 重导入语义、Pi 插件 MCP 工具名与凭据、external peer ID。升级前备份且核对调用方兼容性，未独立运行迁移测试。
- 证据：[官方 Release](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2)；事件时间按 Release UTC，观测时间 2026-10-23T18:50:30.961Z；等级 `upstream_statement`，未独立复现。
- 本轮默认分支 HEAD：`4ab22a4923452362b60aef2826c2083ce36168d2`（2026-10-23T18:50:30.961Z）；仅为最新采样，不表示全部 HEAD 变更已逐项审查。

## 2026-10-27：Python SDK 0.1.17 发布与主分支依赖下限

python-sdk@0.1.17 已发布但无 Release 正文；主分支 pyproject.toml 把 openviking-sdk 下限0.1.15改为0.1.17，锁文件同步。相关 commit 将其描述为 Compile API 兼容要求；不能据此宣称服务端已发布新版本，观测服务端 Release 仍为 v0.5.2。

状态：`sdk_released_server_dependency_merged`；证据等级 `code_inspected`。这是选定实现和一手发布材料的检查，未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/volcengine/OpenViking/commit/009c483f20806d63979cec0f3a7fb1304fd600df)；来源版本 `009c483f20806d63979cec0f3a7fb1304fd600df`。
- 事件 UTC 2026-10-26T03:40:46Z；观察 UTC 2026-10-26T16:15:43.546Z。
- 已读范围：`pyproject.toml`、`uv.lock`、`python-sdk@0.1.17 release metadata`。
- 记录的默认分支 HEAD：`5c066d97094d713238c483c10691d7b4e1cfbf6e`，采样 UTC 2026-10-26T16:13:48.989Z；不是实时最新版本，也不表示其他提交已经逐项审查。

</details>

## 2026-10-28：v0.5.2.1 暂停新敏感值自动识别

为减少误报造成的内容替换与无效隐私记录，新敏感值的规则探测及敏感字段捕获在代码中禁用，没有运行时开关；已登记值的替换与历史引用还原保留。未登记的新敏感内容可能原样持久化，升级者需核对已有登记范围；本次不清理旧记录。Release 同时列入 SDK 最低依赖0.1.17。

状态：`released`；选定实现为 `code_inspected`，发布声明为 `upstream_statement`；未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/volcengine/OpenViking/releases/tag/v0.5.2.1)；[相关 PR](https://github.com/volcengine/OpenViking/pull/6680)；来源版本 `3f85145b71a8e011df4deba1eced057b0409f147`。
- 事件 UTC 2026-10-27T13:44:25Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 已读范围：[openviking/privacy/session_extractor.py](https://github.com/volcengine/OpenViking/blob/3f85145b71a8e011df4deba1eced057b0409f147/openviking/privacy/session_extractor.py)；[docs/zh/concepts/13-privacy.md](https://github.com/volcengine/OpenViking/blob/3f85145b71a8e011df4deba1eced057b0409f147/docs/zh/concepts/13-privacy.md)。
- 默认分支记录为 `54d4c0fac91fae976325ebed618d7278ff9b5c77`，采样 UTC 2026-10-28T03:36:54.304Z；其余差异未全部审查，历史记录保留。

</details>

## 2026-11-07：重点变更核对

LangGraph Store 以单个 URI 段编码含分隔符的 key；index=[] 保留 JSON 值并移除语义索引投影；写入与列举只忽略对应的明确缺失/已存在情形，其他后端错误向上抛出。归档文本搜索同时保留 Unicode 查询词约束。 受影响者是该 LangChain/LangGraph 集成包的使用者。可评估集成包 0.2.0，核对路径型 key 的往返读写、index=[] 的语义检索行为，并让上层区分“空结果”和权限/可用性错误。

这是 langchain-openviking 集成包发布，不是 OpenViking 主包新版本。Unicode 修正没有增加规范化或更宽的大小写等价，原有短 ASCII 词过滤仍保留；上述错误传播结论限于已审的 Store 路径。

[PR](https://github.com/volcengine/OpenViking/pull/7038) 合并 UTC 2026-11-06T10:05:35Z；[正式版本 langchain-openviking@0.2.0](https://github.com/volcengine/OpenViking/releases/tag/langchain-openviking%400.2.0) 发布 UTC 2026-11-06T11:06:58Z；实际 tag commit `b8e88959f3ab437b4d08514eceaa7221cca470dc` 已确认包含该合并。审读观察 UTC 2026-11-06T16:39:37.116Z；证据等级 code_inspected，未独立复现。实际轻量 tag 指向 b8e8895；分别从 PR7038、PR7040 合并 commit 到该 tag 的 compare 均确认包含关系。

阅读范围：[integrations/frameworks/langchain/src/langchain_openviking/store.py](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/src/langchain_openviking/store.py)、[integrations/frameworks/langchain/src/langchain_openviking/tools.py](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/src/langchain_openviking/tools.py)、[integrations/frameworks/langchain/pyproject.toml](https://github.com/volcengine/OpenViking/blob/b8e88959f3ab437b4d08514eceaa7221cca470dc/integrations/frameworks/langchain/pyproject.toml)。

[Unicode 查询 PR](https://github.com/volcengine/OpenViking/pull/7040) 同属该集成包版本，已核对合并与 tag 包含关系。

## 2026-11-08：重点变更核对

FileTree 从空壳变成渲染行与状态的可复用前端组件；操作等待成功后才发通知，重复未完成操作被抑制，拒绝不发成功通知。 面向使用前端组件包构建目录浏览器的接入者，可评审固定commit。树数据、展开和分页状态仍由宿主维护；尚无本轮Release覆盖该合并的证据。

这是前端目录交互组件变化，不代表后端记忆检索、持久化或召回质量改进。合并commit等于本轮观察HEAD；仅核对组件、body与操作hook源码，未在浏览器运行，也未验证上游宣称的测试结果。

[PR](https://github.com/volcengine/OpenViking/pull/7201) 合并UTC 2026-11-07T14:00:58Z；状态 merged-unreleased；发布UTC 未确认。审读版本 `9ac008f9b86c91b79d6e93eb8df8ea7f4d48cecb`，观察UTC 2026-11-07T16:44:09.211Z，证据等级code_inspected，未独立复现。PR7201实际合并SHA与本轮观察HEAD一致。增量Release仍以此前集成包发布为最新记录，不能把它当作此次前端组件已发布的证明。

阅读范围：[frontend/packages/react/src/components/file-tree/file-tree.tsx](https://github.com/volcengine/OpenViking/blob/9ac008f9b86c91b79d6e93eb8df8ea7f4d48cecb/frontend/packages/react/src/components/file-tree/file-tree.tsx)；[frontend/packages/react/src/components/file-tree/file-tree-body.tsx](https://github.com/volcengine/OpenViking/blob/9ac008f9b86c91b79d6e93eb8df8ea7f4d48cecb/frontend/packages/react/src/components/file-tree/file-tree-body.tsx)；[frontend/packages/react/src/components/file-tree/use-file-tree-actions.ts](https://github.com/volcengine/OpenViking/blob/9ac008f9b86c91b79d6e93eb8df8ea7f4d48cecb/frontend/packages/react/src/components/file-tree/use-file-tree-actions.ts)。

## 2026-11-09：重点变更核对

合并 FilePreview 多格式预览与编辑实现，保存失败保留草稿，成功后退出编辑。 面向自行接入前端组件的开发者；核对宿主提供的读取、保存和渲染依赖，等待发布确认。

状态仅为已合并，未确认发布；组件 README 仍称占位，但固定源码已导出实现。未运行 UI 或格式兼容测试，不推断记忆后端质量提升。

[PR](https://github.com/volcengine/OpenViking/pull/7225) 合并UTC 2026-11-08T10:00:32Z；状态 merged-unreleased；发布UTC 未确认。审读版本 `14ce455d90c178746508633440d9085220e187bc`，观察UTC 2026-11-08T16:33:53.438Z，证据等级code_inspected，未独立复现。PR7225 的合并SHA属于已采集 HEAD 的完整两提交 compare 范围；增量 Release 未发现覆盖此变更的新发布。

阅读范围：[frontend/packages/react/src/components/file-preview/file-preview-body.tsx](https://github.com/volcengine/OpenViking/blob/14ce455d90c178746508633440d9085220e187bc/frontend/packages/react/src/components/file-preview/file-preview-body.tsx)；[frontend/packages/react/src/components/file-preview/use-file-preview-editing.ts](https://github.com/volcengine/OpenViking/blob/14ce455d90c178746508633440d9085220e187bc/frontend/packages/react/src/components/file-preview/use-file-preview-editing.ts)；[frontend/packages/react/src/components/file-preview/index.ts](https://github.com/volcengine/OpenViking/blob/14ce455d90c178746508633440d9085220e187bc/frontend/packages/react/src/components/file-preview/index.ts)；[frontend/packages/react/src/components/file-preview/README.md](https://github.com/volcengine/OpenViking/blob/14ce455d90c178746508633440d9085220e187bc/frontend/packages/react/src/components/file-preview/README.md)。

## 2026-11-10：重点变更核对

资源文件写入仍等待自身摘要与向量，直接父目录 L0/L1 和目录向量改为独立刷新任务。 调用方应区分文件写入完成与目录语义刷新完成；依赖即时目录概览的流程需核对该边界。

代码只在 resource、非递归 content_write 等条件下分离父目录刷新；独立目录消息不继承原任务和正文锁凭证，复用已生成文件摘要。删除检查在写回及加锁前 best-effort 执行，检查后删除仍有 TOCTOU 窗口；未实测延迟、吞吐、持久性或站内部署效果。

[PR](https://github.com/volcengine/OpenViking/pull/7268) 合并UTC 2026-11-09T09:56:46Z；状态 released；发布UTC 2026-11-09T10:08:45Z。审读版本 `9dfa9017a8c61abefcd239fe98fdba094a2de7f3`，观察UTC 2026-11-10T06:41:57.412Z，证据等级code_inspected，未独立复现。版本标签直接指向 PR #7268 的合并提交，Release 明确列出该变化；主库 v0.5.4 与独立 SDK/CLI 标签分别记录，不混作同一包版本。

阅读范围：[openviking/storage/queuefs/semantic_processor.py](https://github.com/volcengine/OpenViking/blob/9dfa9017a8c61abefcd239fe98fdba094a2de7f3/openviking/storage/queuefs/semantic_processor.py)；[openviking/storage/queuefs/semantic_executor.py](https://github.com/volcengine/OpenViking/blob/9dfa9017a8c61abefcd239fe98fdba094a2de7f3/openviking/storage/queuefs/semantic_executor.py)；[openviking/storage/queuefs/semantic_work.py](https://github.com/volcengine/OpenViking/blob/9dfa9017a8c61abefcd239fe98fdba094a2de7f3/openviking/storage/queuefs/semantic_work.py)；[tests/storage/test_semantic_processor_target_preexisting.py](https://github.com/volcengine/OpenViking/blob/9dfa9017a8c61abefcd239fe98fdba094a2de7f3/tests/storage/test_semantic_processor_target_preexisting.py)。

## 2026-11-14：重点变更核对

新增可选 PostgreSQL pgvector 后端，用于持久化向量与相关索引数据，支持精确检索与 HNSW。 选用 PostgreSQL 的部署应核对 pgvector 版本及向量维度。4096 维使用精确检索，HNSW 上限为 2000 维。

源码要求 pgvector 0.8.0 或更新版本，嵌入仍由配置的提供方生成。本文未验证性能、召回率或迁移。

[PR](https://github.com/volcengine/OpenViking/pull/7516) 合并UTC 2026-11-13T08:06:42Z；状态 released；发布UTC 2026-11-13T13:13:11Z。审读版本 `4f4b09c8b81cc52cc0361ec7d9f189ce0ccda35b`，观察UTC 2026-11-14T02:56:05.518Z，证据等级code_inspected，未独立复现。发行标签包含合并提交：领先 5 个提交，落后 0。

阅读范围：[openviking/storage/vectordb_adapters/pgvector_adapter.py](https://github.com/volcengine/OpenViking/blob/4f4b09c8b81cc52cc0361ec7d9f189ce0ccda35b/openviking/storage/vectordb_adapters/pgvector_adapter.py)；[openviking/storage/vectordb_adapters/factory.py](https://github.com/volcengine/OpenViking/blob/4f4b09c8b81cc52cc0361ec7d9f189ce0ccda35b/openviking/storage/vectordb_adapters/factory.py)；[docs/en/guides/25-pgvector.md](https://github.com/volcengine/OpenViking/blob/4f4b09c8b81cc52cc0361ec7d9f189ce0ccda35b/docs/en/guides/25-pgvector.md)。
