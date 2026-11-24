# Agent Memory 简报｜2026-11-24

claude-mem v16.1.1 修复了 Mem0 空生命周期字段导致的导入中断。Hindsight 合并了防止旧异步写入覆盖新文档的改动。
第一项影响从 Mem0 迁移的用户，第二项影响会重试单文档替换的自托管服务。OpenViking 的 PostgreSQL 队列后端已合并。
曾遇到 Mem0 导入中断的用户可以先在 v16.1.1 预览导入。OpenViking v0.5.6 尚未包含 PostgreSQL 队列后端。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/commit/42dd5db0be3fee9d70d26f83f202d56bacac3df7) | Mem0 导入接受生命周期字段为 null 的记录，继续按替换关系和到期时间筛选。 | 已发布 v16.1.1 | 曾因 null 值中断的导入可在 v16.1.1 先预览将写入和跳过的记录。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/commit/bae002db25cf4b2ce996b85a959c9a78376d9ab0) | 异步单文档替换重试时，若同一文档已有后提交且已完成的同类任务，会跳过旧写入。 | 已合并，未确认随包发布 | 依赖异步覆盖写入的自托管部署可关注含该提交的版本，并检查任务结果中的 superseded_by。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/commit/484347c192a1270b42ed500148e7511e653d96d0) | QueueFS 增加 PostgreSQL 后端，通过消费者租约恢复未确认消息。 | 已合并，v0.5.6 未包含 | 准备共享队列的部署先确认目标版本包含该提交，检查 schema 初始化和消费幂等。 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark/commit/01bd83f3fa5245d6be3986cfab81fdd828f26acd) | Hindsight 知识库检索评测显式请求重排。 | 已合并，未确认随包发布 | 对照两次结果时，记录 AMB 提交和服务端实际重排配置。 |

### 适用条件

**thedotmack/claude-mem**。变更位于 `import-memory` 的 Mem0 分支。`lifecycle_state` 缺失或为 `null` 时通过该字段校验。其他陌生状态仍报错，替换或已到期的记录仍可被跳过。计划会校验来源账号和记录身份，并把原始来源字段保存在 `importSource`。上游测试源码覆盖了 `null` 的导入和重复导入。

**vectorize-io/hindsight**。异步处理器在批量写入前检查 `operation_id`，且待处理内容不得含 `append`。检查限定在同一 memory bank、同一单文档 `serialization_key` 和同一操作类型，只考虑已完成任务，按创建时间和操作 ID 判断先后。命中时记录 `result_metadata.superseded_by` 并正常结束，旧内容不再写入。多文档任务缺少该序列键，其余写入继续走常规路径。

**volcengine/OpenViking**。OpenViking 的 AGFS 配置默认仍使用 SQLite。选用 PostgreSQL 需要显式设置 `storage.agfs.queuefs.backend`、初始化数据库结构，并让共享队列实例指向同一数据库和 `service_name`。Rust 构建需要相应 feature。消费采用至少一次投递，ACK 前的失败可能触发重投，已有本地消息不会自动迁移。

**vectorize-io/agent-memory-benchmark**。这条变化位于 AMB 的 `hindsight-knowledge` 检索路径。每次知识库搜索都会发送 `enable_reranking: true`，请求仍携带原有 token 预算并按 `top_k` 截取结果。实际效果依赖被测服务端版本和重排器配置。Vectorize 同时维护 AMB 和 Hindsight。

## Star 变化

两次观测间隔约 36.73 小时。7 日窗口没有符合 ±6 小时容差的基线。30 日列使用实际观测，起始时刻和经过时长见下方证据。

| 项目 | 前次 UTC | 本次 UTC | 本次 Stars | 相邻净变化 | 30 日净变化 |
| --- | --- | --- | ---: | ---: | ---: |
| mem0ai/mem0 | 2026-11-22T16:21:36.244Z | 2026-11-24T05:05:05.226Z | 69397 | +56 | +1637 |
| getzep/graphiti | 2026-11-22T16:21:41.820Z | 2026-11-24T05:05:11.302Z | 33041 | +44 | +852 |
| thedotmack/claude-mem | 2026-11-22T16:21:47.420Z | 2026-11-24T05:05:17.550Z | 119366 | +377 | +16485 |
| vectorize-io/hindsight | 2026-11-22T16:21:58.507Z | 2026-11-24T05:05:29.269Z | 62950 | +340 | +9454 |
| volcengine/OpenViking | 2026-11-22T16:22:16.065Z | 2026-11-24T05:05:48.195Z | 42669 | +64 | +1911 |
| vectorize-io/agent-memory-benchmark | 2026-11-22T16:22:19.334Z | 2026-11-24T05:05:51.635Z | 170 | +2 | +12 |

## 新候选线索对比

以下为搜索返回的项目自述。50 项观察池本轮未新增准入。

| 线索 | 公开描述 | 待核实 |
| --- | --- | --- |
| [synuns/flint](https://github.com/synuns/flint) | 描述称使用 Doltgres 管理有版本的记忆，并提供 MCP 接口。 | 持久化和版本恢复是否覆盖代理写入。 |
| [yb-zhai/agent-memory](https://github.com/yb-zhai/agent-memory) | 描述称面向本机使用，提供四路召回与 MCP。 | 各路召回如何合并、实际运行依赖。 |
| [cstksniper/hippo-mcp](https://github.com/cstksniper/hippo-mcp) | 描述称提供用户与项目范围的本地长期记忆。 | 作用域在读写及删除流程中如何约束。 |

## 方法与覆盖边界

24 个登记对象均取得元数据、HEAD 和完整增量 Release。9 个变化区间中，预选 5 项，完成 4 项静态审读。Graphiti 的对应公开 PR 未取得，继续待核实。两条无 Star 门槛的搜索均只读第一页，共返回 40 条。未运行上游代码或重跑评测。

<details markdown="1"><summary>证据与时间</summary>

批次 20261124T050333Z-local。基线 `e0d0ff2734eb34502ba8427a1a3f34b8a065027a`。采集观测结束于 2026-11-24T05:06:21.350Z。

### thedotmack/claude-mem

固定提交 `42dd5db0be3fee9d70d26f83f202d56bacac3df7`，提交记录时间 2026-11-23T17:28:22Z，提交读取于 2026-11-24T09:40:10.884Z。v16.1.1 注释标签剥离为 `ecfc1c0bde70efc16839e3ffcdf02efce736512f`，留存的默认分支父链包含该变更。 证据等级 `code_inspected`。

[固定提交](https://github.com/thedotmack/claude-mem/commit/42dd5db0be3fee9d70d26f83f202d56bacac3df7) · [导入校验与计划](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/src/npx-cli/commands/import-memory.ts#L262-L277) · [保存确认](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/src/npx-cli/commands/import-memory.ts#L327-L343) · [测试源码](https://github.com/thedotmack/claude-mem/blob/42dd5db0be3fee9d70d26f83f202d56bacac3df7/tests/fixtures/import-provider-smoke.py#L80-L91) · [v16.1.1](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.1)

### vectorize-io/hindsight

固定提交 `bae002db25cf4b2ce996b85a959c9a78376d9ab0`，提交记录时间 2026-11-23T12:49:13Z，提交读取于 2026-11-24T09:40:15.821Z。按固定 Contents 返回的 blob SHA 取得完整实现，并用实际字节核对；原观测的 Release 未确认包含关系。 证据等级 `code_inspected`。

[固定提交](https://github.com/vectorize-io/hindsight/commit/bae002db25cf4b2ce996b85a959c9a78376d9ab0) · [处理器入口](https://github.com/vectorize-io/hindsight/blob/bae002db25cf4b2ce996b85a959c9a78376d9ab0/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L4563-L4595) · [任务先后判定](https://github.com/vectorize-io/hindsight/blob/bae002db25cf4b2ce996b85a959c9a78376d9ab0/hindsight-api-slim/hindsight_api/engine/memory_engine.py#L23671-L23703) · [测试源码](https://github.com/vectorize-io/hindsight/blob/bae002db25cf4b2ce996b85a959c9a78376d9ab0/hindsight-api-slim/tests/test_retain_stale_replace_retry.py#L49-L90)

### volcengine/OpenViking

固定提交 `484347c192a1270b42ed500148e7511e653d96d0`，提交记录时间 2026-11-23T13:33:26Z，提交读取于 2026-11-24T09:40:21.255Z。v0.5.6 标签指向 `831ad81f5838d3502812a48bbec2e1d2930ed13c`，留存父链显示该标签提交早于此变更。 证据等级 `code_inspected`。

[固定提交](https://github.com/volcengine/OpenViking/commit/484347c192a1270b42ed500148e7511e653d96d0) · [PostgreSQL 后端](https://github.com/volcengine/OpenViking/blob/484347c192a1270b42ed500148e7511e653d96d0/crates/ragfs/src/plugins/queuefs/postgres_backend.rs#L354-L401) · [QueueFS 配置](https://github.com/volcengine/OpenViking/blob/484347c192a1270b42ed500148e7511e653d96d0/crates/ragfs/src/plugins/queuefs/mod.rs#L828-L856) · [上游部署指南](https://github.com/volcengine/OpenViking/blob/484347c192a1270b42ed500148e7511e653d96d0/docs/zh/guides/15-postgres-queuefs.md) · [v0.5.6](https://github.com/volcengine/OpenViking/releases/tag/v0.5.6)

### vectorize-io/agent-memory-benchmark

固定提交 `01bd83f3fa5245d6be3986cfab81fdd828f26acd`，提交记录时间 2026-11-23T09:01:32Z，提交读取于 2026-11-24T09:40:27.736Z。本轮核对请求实现及固定默认分支提交，未测量检索分数或延迟。 证据等级 `code_inspected`。

[固定提交](https://github.com/vectorize-io/agent-memory-benchmark/commit/01bd83f3fa5245d6be3986cfab81fdd828f26acd) · [请求参数](https://github.com/vectorize-io/agent-memory-benchmark/blob/01bd83f3fa5245d6be3986cfab81fdd828f26acd/src/memory_bench/memory/hindsight_knowledge.py#L157-L170) · [检索调用方](https://github.com/vectorize-io/agent-memory-benchmark/blob/01bd83f3fa5245d6be3986cfab81fdd828f26acd/src/memory_bench/memory/hindsight_knowledge.py#L281-L293)

### 30 日 Star 基线

| 项目 | 基线 UTC | 实际经过小时 |
| --- | --- | ---: |
| mem0ai/mem0 | 2026-10-25T05:58:55.917Z | 719.10 |
| getzep/graphiti | 2026-10-25T05:59:27.932Z | 719.10 |
| thedotmack/claude-mem | 2026-10-25T05:59:38.068Z | 719.09 |
| vectorize-io/hindsight | 2026-10-25T06:01:17.332Z | 719.07 |
| volcengine/OpenViking | 2026-10-25T06:01:46.411Z | 719.07 |
| vectorize-io/agent-memory-benchmark | 2026-10-25T06:01:57.958Z | 719.06 |

</details>
