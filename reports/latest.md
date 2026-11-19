# Agent Memory 简报｜2026-11-20

四个已发布版本包含认证隔离、回合竞态、记忆 scope 和连接池修正；OpenViking 另合并缺失向量 ID 的失败处理。
Windows 上使用 claude-mem Codex、重复 retain 的 Hindsight 用户，以及 PostgreSQL 多数据集部署者应重点核对适用条件。
升级时检查发行标签和现有配置；认证副本不同步回写，连接池默认值也不能替代全进程并发预算。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/6332) | 私有 Codex home 改为优先符号链接；Windows 遇 EPERM、EACCES 或 ENOTSUP 时复制独立文件。 | 已发布 v16.0.1；tag 含合并提交 | Windows 部署核对符号链接或副本模式；副本更新需重建私有运行时。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/5799) | 对已识别的 no-active-turn 或 turn-ID mismatch，最多等待三秒让本地回合结束，再启动一次新回合。 | 已发布 v0.34.66；tag 含合并提交 | 跟进消息遇回合结束竞态时核对三秒等待；queued 回执不代表可以重放。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6694) | 请求未指定 observation_scopes 时，四处保留事实的重标记调用改用 bank 默认值。 | 已发布 v1.2.2；tag 含合并提交 | 重复写入文档时检查保留事实的 scope；仅配置了 bank 默认值的部署受该回退影响。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7616) | TextEmbeddingHandler 在 upsert 返回空字符串或 None 时进入既有失败分支，不再返回成功但 vector_written=false。 | 已合并，未确认随包交付 | 检查空 ID 的向量写入是否报告失败；关闭期例外和最终任务状态仍需另验。 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee/pull/6787) | 图与按访问控制隔离的 PGVector 缺省池由2+20调为2+10；申请空闲连接的缺省等待统一为360秒。 | 已发布 v1.6.10；tag 含合并提交 | 按数据库连接预算配置每数据集池及并发数，显式参数仍优先。 |

### 适用条件

**thedotmack/claude-mem**。仅针对 claude-mem 的 Codex ChatGPT 登录路径，API key 不适用。其他符号链接错误继续抛出；复制使用 COPYFILE_EXCL，已有目标不会被覆盖。副本只是启动时快照，不向用户认证文件回写；recycle 后重新取当前登录。此处不建议更改系统权限或 Developer Mode。

**letta-ai/letta-code**。sendCodexMessage 在 session lock 内等待，每25ms检查状态；activeTurnId 仍未变化时抛回原错误。已返回 queued 回执的 steer 不重放；原回合的 waiter 保留结果。无关错误不进入新增三秒等待；已结束状态仍沿既有新回合分支处理。没有真实 Codex 运行验收。

**vectorize-io/hindsight**。仅当请求值是 None 才回退，显式空列表也会保留，不把它当缺省。全局默认 default_observation_scopes 为 None，可通过 HINDSIGHT_API_DEFAULT_OBSERVATION_SCOPES 或 bank 配置提供；没有默认值的 bank 不因此自动变 shared。已读 orchestrator、fact_storage 的委托与级联入口、配置和上游测试差异，未逐个检查存储后端。核对相同文本及部分改动文本再次写入时保留事实的 scope，不能把本次静读当成实际合并结果验收。

**volcengine/OpenViking**。仅限实际到达该 handler 的 embedding 写入；_embedding_failed 生成含 URI 的错误并返回 ProcessResult.failed。成功写入才报告 vector_written=true。is_closing 的数据库关闭期仍可返回 success，既有 no-op 路径不变。未追踪整个队列中间件或持久任务状态机，不能据此声称所有任务持久化故障已修复；React 或 SuperAgent 的单独发行不证明该核心修正随包交付。

**topoteretes/cognee**。PGVector 的 VECTOR_POOL_ARGS 优先于 POOL_ARGS，只有二者未显式提供且 backend access control 开启时，采用2+10的小池默认；非该路径仍可使用关系池5+35默认。二进制写池独立于 SQLAlchemy 池、按相同参数设上限，三处 acquire 均传入 pool_timeout；不是连接建立超时。图池显式 POOL_ARGS、NullPool 分支保留，关系池大小未变。多数据集并行仍会累加连接数，不构成全进程连接总量保证；未连接 PostgreSQL 做负载实验。

## Star 变化：相邻实测区间与合格长期窗口

按登记对象展示关注度，不作跨类别质量排名。相邻区间按各项目真实 metadata 时刻计算；7/30日窗口使用±6小时容差。

| 项目 | 本次 Stars | 相邻净变化 | 实际时长 | 7日净变化 | 30日净变化 |
| --- | ---: | ---: | ---: | ---: | ---: |
| mem0ai/mem0 | 69242 | +55 | 24.48小时 | 无合格基线 | 无合格基线 |
| thedotmack/claude-mem | 118370 | +200 | 24.48小时 | 无合格基线 | 无合格基线 |
| letta-ai/letta-code | 3876 | +9 | 24.47小时 | 无合格基线 | 无合格基线 |
| vectorize-io/hindsight | 62004 | +222 | 24.47小时 | 无合格基线 | 无合格基线 |
| volcengine/OpenViking | 42474 | +56 | 24.46小时 | 无合格基线 | 无合格基线 |
| topoteretes/cognee | 33410 | +22 | 24.46小时 | 无合格基线 | 无合格基线 |

## 新候选线索对比

本轮没有完成新候选实现审查，不新增或晋升：23个跟踪项目、1个历史参照、26个候选已占满50个位置。以下仅是实际搜索元数据宣称，README、实现、依赖与许可证正文均未核实。

| 原始线索 | 描述中的载体与机制 | 主要待核实项 |
| --- | --- | --- |
| [vshulcz/coding-agent-memory-benchmark](https://github.com/vshulcz/coding-agent-memory-benchmark) | 描述声称提供 Day-Zero、LongMemEval-S、LoCoMo 与 MCP schema token 评测 | 协议版本、评分实现、运行资产和各协议可比性；不转用其成绩 |
| [drly77/mem-agents](https://github.com/drly77/mem-agents) | 描述声称用 SQLite FTS5、bge-m3 和本地 reranker 搜索编码代理记忆 | 本地运行与模型依赖、写入维护机制、许可和公开复现实验 |

## 方法与覆盖边界

24个对象的 metadata、HEAD 与所需增量 Release 来源完整。8个变化区间中深读上述5项，未审范围继续保留；Hindsight、OpenViking 两份 compare 达300文件，不代表全量变化已覆盖。两条无 Star 门槛搜索仅读第一页，共39条原始结果，生态覆盖有界。Tencent v2.0.4、OpenViking React 0.2.0 / SuperAgent 0.5.5-preview 及 AMB 外部结果更新留待后续判读，未据此宣称新的性能收益。所有技术结论来自静态源码、完整选定 PR 差异和发行身份；未运行上游代码、测试或付费评测。

<details markdown="1"><summary>证据与时间</summary>

批次 `20261119T160540Z-local`；基线 `227ec54e3ef9006325dae42c9ca39b194f37b1b4`；来源批次最大观察 UTC 2026-11-19T16:30:51.727Z。补充来源按实际返回时间独立记录，不改变原采集时刻。

### thedotmack/claude-mem #6332

仅针对 claude-mem 的 Codex ChatGPT 登录路径，API key 不适用。其他符号链接错误继续抛出；复制使用 COPYFILE_EXCL，已有目标不会被覆盖。副本只是启动时快照，不向用户认证文件回写；recycle 后重新取当前登录。此处不建议更改系统权限或 Developer Mode。

合并 UTC 2026-11-19T11:01:27Z；PR观察 UTC 2026-11-19T16:34:38.887Z；固定合并提交 `833a0a834c8c91e6b4843cdba5c8bbe9035fb6d9`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/thedotmack/claude-mem/pull/6332)；[src/services/worker/CodexAppServerClient.ts](https://github.com/thedotmack/claude-mem/blob/833a0a834c8c91e6b4843cdba5c8bbe9035fb6d9/src/services/worker/CodexAppServerClient.ts)（blob `c2700c146041ef88d6f3828a10be91cb4ab62479`）

[发行](https://github.com/thedotmack/claude-mem/releases/tag/v16.0.1)：tag 解至 `e22c58353b950b15e6e16d98719801224840f046`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

### letta-ai/letta-code #5799

sendCodexMessage 在 session lock 内等待，每25ms检查状态；activeTurnId 仍未变化时抛回原错误。已返回 queued 回执的 steer 不重放；原回合的 waiter 保留结果。无关错误不进入新增三秒等待；已结束状态仍沿既有新回合分支处理。没有真实 Codex 运行验收。

合并 UTC 2026-11-18T20:33:33Z；PR观察 UTC 2026-11-19T16:34:40.907Z；固定合并提交 `e564536b66d97f6053f83cf3a1705144784f354d`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/letta-ai/letta-code/pull/5799)；[src/tools/impl/codex-app-server.ts](https://github.com/letta-ai/letta-code/blob/e564536b66d97f6053f83cf3a1705144784f354d/src/tools/impl/codex-app-server.ts)（blob `d991894ce5eb9d9c8a5e0083ad2ddba55f65f871`）；[src/tools/impl/codex-steer-receipt.ts](https://github.com/letta-ai/letta-code/blob/e564536b66d97f6053f83cf3a1705144784f354d/src/tools/impl/codex-steer-receipt.ts)（blob `3f1e8cca2782cc08900d9c2816e2dbc1c7c0cccd`）

[发行](https://github.com/letta-ai/letta-code/releases/tag/v0.34.66)：tag 解至 `1af182c9bd8d228f6941970ab5f9f8ba8363f2c5`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

### vectorize-io/hindsight #6694

仅当请求值是 None 才回退，显式空列表也会保留，不把它当缺省。全局默认 default_observation_scopes 为 None，可通过 HINDSIGHT_API_DEFAULT_OBSERVATION_SCOPES 或 bank 配置提供；没有默认值的 bank 不因此自动变 shared。已读 orchestrator、fact_storage 的委托与级联入口、配置和上游测试差异，未逐个检查存储后端。核对相同文本及部分改动文本再次写入时保留事实的 scope，不能把本次静读当成实际合并结果验收。

合并 UTC 2026-11-19T14:09:03Z；PR观察 UTC 2026-11-19T16:34:43.041Z；固定合并提交 `79f7e56d6f9c5e86bafec00f98f031ce19316672`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/vectorize-io/hindsight/pull/6694)；[hindsight-api-slim/hindsight_api/engine/retain/orchestrator.py](https://github.com/vectorize-io/hindsight/blob/79f7e56d6f9c5e86bafec00f98f031ce19316672/hindsight-api-slim/hindsight_api/engine/retain/orchestrator.py)（blob `eac5fefcc5861e4c48fbb98cb86a4c6f07af1240`）；[hindsight-api-slim/hindsight_api/engine/retain/fact_storage.py](https://github.com/vectorize-io/hindsight/blob/79f7e56d6f9c5e86bafec00f98f031ce19316672/hindsight-api-slim/hindsight_api/engine/retain/fact_storage.py)（blob `43271c311fbb64b79fc4c95832787f92aa8888af`）；[hindsight-api-slim/hindsight_api/config.py](https://github.com/vectorize-io/hindsight/blob/79f7e56d6f9c5e86bafec00f98f031ce19316672/hindsight-api-slim/hindsight_api/config.py)（blob `5f8549b1856ebe9c3783c33c347f5ab07c463b42`）

[发行](https://github.com/vectorize-io/hindsight/releases/tag/v1.2.2)：tag 解至 `b4b4652949d5a8c3ac3fe9fa572c99c74ecb2b9c`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

### volcengine/OpenViking #7616

仅限实际到达该 handler 的 embedding 写入；_embedding_failed 生成含 URI 的错误并返回 ProcessResult.failed。成功写入才报告 vector_written=true。is_closing 的数据库关闭期仍可返回 success，既有 no-op 路径不变。未追踪整个队列中间件或持久任务状态机，不能据此声称所有任务持久化故障已修复；React 或 SuperAgent 的单独发行不证明该核心修正随包交付。

合并 UTC 2026-11-19T08:13:40Z；PR观察 UTC 2026-11-19T16:34:45.135Z；固定合并提交 `5f50e2d0bfb0f6fbc6c6044ca195ef30314c370e`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/volcengine/OpenViking/pull/7616)；[openviking/storage/collection_schemas.py](https://github.com/volcengine/OpenViking/blob/5f50e2d0bfb0f6fbc6c6044ca195ef30314c370e/openviking/storage/collection_schemas.py)（blob `e3c176bfaea91d71c829845fb2b1e557ef2d04da`）；[openviking/storage/queuefs/process_result.py](https://github.com/volcengine/OpenViking/blob/5f50e2d0bfb0f6fbc6c6044ca195ef30314c370e/openviking/storage/queuefs/process_result.py)（blob `2b54dee6b00562021433f785673aea0ef108a401`）

### topoteretes/cognee #6787

PGVector 的 VECTOR_POOL_ARGS 优先于 POOL_ARGS，只有二者未显式提供且 backend access control 开启时，采用2+10的小池默认；非该路径仍可使用关系池5+35默认。二进制写池独立于 SQLAlchemy 池、按相同参数设上限，三处 acquire 均传入 pool_timeout；不是连接建立超时。图池显式 POOL_ARGS、NullPool 分支保留，关系池大小未变。多数据集并行仍会累加连接数，不构成全进程连接总量保证；未连接 PostgreSQL 做负载实验。

合并 UTC 2026-11-18T20:32:05Z；PR观察 UTC 2026-11-19T16:34:47.206Z；固定合并提交 `ebd8caba08799c719ec56c12939ec27ebdb5352d`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/topoteretes/cognee/pull/6787)；[cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py)（blob `d13cb6fca18733cfb97ba1931887a878544e7989`）；[cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py)（blob `5d2fde46eb9bc1617b65e4740860b01948d222b7`）；[cognee/infrastructure/databases/graph/postgres_demo/adapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/graph/postgres_demo/adapter.py)（blob `bd1424f06c391ddf50e3eb7012fc48ec7220ccb8`）

[发行](https://github.com/topoteretes/cognee/releases/tag/v1.6.10)：tag 解至 `c8a094375821f2d8c7c4945d3b2202e2e5d6603e`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

### Star 实际窗口

| 项目 ID | 相邻起始 UTC | 相邻结束 UTC | 7日实际天数 | 30日实际天数 |
| --- | --- | --- | ---: | ---: |
| 656099147 | 2026-11-18T16:00:32.311Z | 2026-11-19T16:29:36.537Z | 无合格基线 | 无合格基线 |
| 1048065319 | 2026-11-18T16:01:07.328Z | 2026-11-19T16:29:48.530Z | 无合格基线 | 无合格基线 |
| 1082960574 | 2026-11-18T16:01:29.027Z | 2026-11-19T16:29:56.994Z | 无合格基线 | 无合格基线 |
| 1086419061 | 2026-11-18T16:01:45.182Z | 2026-11-19T16:29:59.876Z | 无合格基线 | 无合格基线 |
| 1128123594 | 2026-11-18T16:02:38.434Z | 2026-11-19T16:30:19.067Z | 无合格基线 | 无合格基线 |
| 679343504 | 2026-11-18T16:02:58.828Z | 2026-11-19T16:30:28.360Z | 无合格基线 | 无合格基线 |

7/30日基线来自只追加索引中的实际观测；关注度不证明实现质量或操纵。

</details>
