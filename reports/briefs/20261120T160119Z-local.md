# Agent Memory 简报｜2026-11-21

Letta Code v0.34.67 加入云端仓库技能加载，Hindsight 合并了按租户和记忆库轮转的 LLM 排队机制。
并行处理长短文档的 Hindsight 部署者、多节点 OpenViking 维护者和引用 LegalBench-RAG 结果的读者应重点核对适用版本和配置。
Hindsight v1.2.3 尚未包含上述排队改动。OpenViking 的 PostgreSQL Watch 后端需显式配置并预置表结构。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/pull/6338) | Chroma MCP 删除请求丢失回执或超时后，通过一次完整集合列表确认目标是否已消失。 | 已合并，未确认随包交付 | 遇到向量重建异常时，分别核对集合列表、失败日志和重建进度。 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/pull/5822) | 云端 Agent 可指定最多十个 GitHub 仓库及实例规格，并从克隆目录发现项目技能。 | 已发布 v0.34.67 | 使用云端 Agent 的团队可为技能仓库固定完整提交，并按子代理宿主核对技能发现。 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/pull/6742) | 同一 worker 满载时，LLM 槽位按租户、bank 轮转，bank 内优先队列较短的文档并定期服务最早等待者。 | 已合并，v1.2.3 未包含 | 混合长短文档的部署可在包含该提交的版本上检查排队时间和后台任务进度。 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking/pull/7568) | PostgreSQL 可保存共享 Watch 元数据、加密凭据和运行占用状态。 | 已合并，未确认随包交付 | 多节点 PostgreSQL 部署可先核对发行版本、预置表结构和各节点共用密钥。 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark/pull/83) | AMB 加入 LegalBench-RAG mini，按返回证据覆盖的标注字符计算 recall@5。 | 已合并，已见上游结果更新 | 引用结果时同时标注 Hindsight 提交、文件名设置和检索预算。 |

### 适用条件

**thedotmack/claude-mem**。该路径由同一集合的两个不同批次触发损坏确认，并合并同进程中的并发删除。MCP 管理器把删除回执丢失归为结果不明，重连后由调用方查询列表，支持多段文本、JSON 数组及空库标记。列表有效且目标缺席才记为已删除。目标仍存在、列表格式无效或查询失败会抛错，后续损坏批次可用至多三次的进程内失败预算。后台扫描仍会重启，预算耗尽后的进程内停止重试标记也不能作为数据库删除确认。

**letta-ai/letta-code**。cloud 参数仅用于 computer 为 cloud 的路径，仓库可用 owner/repo 或 owner/repo@完整 40 位提交，规格可选 regular、large、xlarge。省略 cloud 时沿用既有启动选项，非法参数在创建前返回错误。Letta 本身要求启用 project 技能源，Claude Code 以会话临时目录挂接 .claude/skills 和 .agents/skills，缺失目录可跳过，其他 staging 错误清理后上抛。Codex 在新线程前注册额外项目技能根。实际云端克隆和各宿主加载未运行。

**vectorize-io/hindsight**。全局槽位默认 32，由 HINDSIGHT_API_LLM_MAX_CONCURRENT 控制，并保留各操作的可选上限。waiter 按当前 schema、trace 或请求 bank、调用元数据 document_id 分组。bank 内每第四次出队选最早等待文档，其余选等待调用最少的文档。前台队列先于后台，持续高前台负载仍可让后台等待。取消请求会移除票据，已经取得槽位的取消请求会交还槽位。未测实际延迟。

**volcengine/OpenViking**。须显式设置 storage.watch_store.provider=postgres。file 仍为缺省，mysql 仍可选。PostgreSQL 路径需要 postgres 依赖和预置 Watch 表，源码校验缺表、列类型和主键并报告不兼容，缺少可用索引时告警。多节点共享该表时按发布文档配置同一 credential_encryption_key。Watch 后端独立于 Task、Account 和向量存储。未连接数据库验证迁移、锁争用或吞吐。

**vectorize-io/agent-memory-benchmark**。该 split 覆盖 714 份合同与 776 道问题，每组 194 题。评估只运行检索，最多取五个结果，配置检索文本预算为 4096 tokens。评分将命中文本定位回文档，合并重叠片段，再计算覆盖的标注字符比例。默认上传中性文件名，AMB_LEGALBENCH_NAMES=original 使用语料原名。上游 #90 声称以 Hindsight fdae5ed70 与默认知识库配置重跑两种文件名设置，#83 的初始结果对应更早实现。Vectorize 同时维护 AMB 和参评系统 Hindsight，本轮仅核对协议代码和上游结果说明。

## Star 变化

相邻两次实测相隔约 23.54 小时。以下对象均缺少距离目标时刻 ±6 小时内的 7 日和 30 日基线。

| 项目 | 前次 UTC | 本次 UTC | 本次 Stars | 净变化 |
| --- | --- | --- | ---: | ---: |
| mem0ai/mem0 | 2026-11-19T16:29:36.537Z | 2026-11-20T16:02:13.679Z | 69280 | +38 |
| thedotmack/claude-mem | 2026-11-19T16:29:48.530Z | 2026-11-20T16:02:26.176Z | 118572 | +202 |
| letta-ai/letta-code | 2026-11-19T16:29:56.994Z | 2026-11-20T16:02:34.623Z | 3883 | +7 |
| vectorize-io/hindsight | 2026-11-19T16:29:59.876Z | 2026-11-20T16:02:37.461Z | 62215 | +211 |
| volcengine/OpenViking | 2026-11-19T16:30:19.067Z | 2026-11-20T16:02:57.182Z | 42526 | +52 |
| vectorize-io/agent-memory-benchmark | 2026-11-19T16:30:22.491Z | 2026-11-20T16:03:00.672Z | 169 | +0 |

## 新候选线索对比

下列线索来自搜索结果的仓库描述，许可证和可运行资产尚未审读。观察池共 50 项，本轮无新增准入。

| 线索 | 元数据描述 | 待核实 |
| --- | --- | --- |
| [linellazatin/nanomneme](https://github.com/linellazatin/nanomneme) | 编码代理使用 SQLite 保存跨会话上下文。 | 写入规则、检索接口和宿主集成。 |
| [tty-pt/pi-mm](https://github.com/tty-pt/pi-mm) | Pi 扩展，描述称支持持久化的多分辨率记忆。 | 多级记忆的生成、刷新和淘汰策略。 |
| [kaustubhsawant-it/meristem-bench](https://github.com/kaustubhsawant-it/meristem-bench) | 评测编码代理在代码事实过时后是否仍检索到旧事实。 | 任务生成器、协议固定版本和评分复现。 |

## 方法与覆盖边界

24 个登记对象均取得元数据、HEAD 和完整增量 Release。7 个变化区间选读上述 5 项，Hindsight 的 compare 达到 300 文件上限。两项无 Star 门槛搜索返回 37 条原始结果，其中一项仅取得首页。结论基于静态源码和发行关系，本轮未运行上游程序或评测。

<details markdown="1"><summary>证据与时间</summary>

批次 20261120T160119Z-local。固定基线 977d56b6d5b7d42199c353652438bc7bf7d768ee。批次观测结束于 2026-11-20T16:03:30.059Z。

### thedotmack/claude-mem #6338

合并时间 2026-11-19T18:36:00Z，观测时间 2026-11-20T16:05:10.338Z，合并提交 c0f37d60b2e4860851575e3cbb003f23fc340d4e。在 2026-11-20T16:05:11.451Z 取得全部 5 个 PR 文件条目，按相关入口做静态审读。

[PR 与完整文件列表](https://github.com/thedotmack/claude-mem/pull/6338) · [ChromaSync.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/src/services/sync/ChromaSync.ts) · [ChromaMcpManager.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/src/services/sync/ChromaMcpManager.ts) · [chroma-sync-corrupt-collection.test.ts](https://github.com/thedotmack/claude-mem/blob/c0f37d60b2e4860851575e3cbb003f23fc340d4e/tests/services/sync/chroma-sync-corrupt-collection.test.ts)

### letta-ai/letta-code #5822

合并时间 2026-11-20T00:12:49Z，观测时间 2026-11-20T16:05:15.992Z，合并提交 7900671f75e786c9fbfefe6dd620ec1c461997cd。在 2026-11-20T16:05:17.167Z 取得全部 34 个 PR 文件条目，按相关入口做静态审读。 v0.34.67 标签指向 758735789b96bd0a370de909308655840e4cd42b。采集的 compare 提交父链可达本项合并提交，证明标签源码包含该变更。

[PR 与完整文件列表](https://github.com/letta-ai/letta-code/pull/5822) · [task-cloud-options.ts](https://github.com/letta-ai/letta-code/blob/7900671f75e786c9fbfefe6dd620ec1c461997cd/src/tools/impl/task-cloud-options.ts) · [client-skills.ts](https://github.com/letta-ai/letta-code/blob/7900671f75e786c9fbfefe6dd620ec1c461997cd/src/agent/client-skills.ts) · [claude-repository-skills.ts](https://github.com/letta-ai/letta-code/blob/7900671f75e786c9fbfefe6dd620ec1c461997cd/src/tools/impl/claude-repository-skills.ts) · [cloud-repository-roots.ts](https://github.com/letta-ai/letta-code/blob/7900671f75e786c9fbfefe6dd620ec1c461997cd/src/utils/cloud-repository-roots.ts) · [补充来源 1](https://github.com/letta-ai/letta-code/releases/tag/v0.34.67)

### vectorize-io/hindsight #6742

合并时间 2026-11-20T14:43:46Z，观测时间 2026-11-20T16:05:24.561Z，合并提交 7f225b52134497fb02677f1950cd103ebc780226。在 2026-11-20T16:05:25.679Z 取得全部 6 个 PR 文件条目，按相关入口做静态审读。 v1.2.3 注释标签经对象 ccd998adf0541904e3d9575037000ebfd161d6df 解到 bd230e8bb40e768bf69f266f1dd3c9ae03e22fe3。该提交位于本项合并的父链上，标签源码早于此改动。

[PR 与完整文件列表](https://github.com/vectorize-io/hindsight/pull/6742) · [_cross_loop.py](https://github.com/vectorize-io/hindsight/blob/7f225b52134497fb02677f1950cd103ebc780226/hindsight-api-slim/hindsight_api/_cross_loop.py) · [llm_wrapper.py](https://github.com/vectorize-io/hindsight/blob/7f225b52134497fb02677f1950cd103ebc780226/hindsight-api-slim/hindsight_api/engine/llm_wrapper.py) · [config.py](https://github.com/vectorize-io/hindsight/blob/7f225b52134497fb02677f1950cd103ebc780226/hindsight-api-slim/hindsight_api/config.py) · [test_llm_per_op_concurrency.py](https://github.com/vectorize-io/hindsight/blob/7f225b52134497fb02677f1950cd103ebc780226/hindsight-api-slim/tests/test_llm_per_op_concurrency.py) · [补充来源 1](https://github.com/vectorize-io/hindsight/releases/tag/v1.2.3)

### volcengine/OpenViking #7568

合并时间 2026-11-20T06:17:36Z，观测时间 2026-11-20T16:05:32.628Z，合并提交 5c9f17603862ff18d13bae596bde92e2398bb1ea。在 2026-11-20T16:05:34.431Z 取得全部 30 个 PR 文件条目，按相关入口做静态审读。

[PR 与完整文件列表](https://github.com/volcengine/OpenViking/pull/7568) · [storage_config.py](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/openviking_cli/utils/config/storage_config.py) · [watch_store_postgres.py](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/openviking/resource/watch_store_postgres.py) · [watch_store_postgres_schema.py](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/openviking/resource/watch_store_postgres_schema.py) · [postgres_config.py](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/openviking/storage/postgres_config.py) · [001_watch_tasks_postgres.sql](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/openviking/service/sql/001_watch_tasks_postgres.sql) · [01-configuration.md](https://github.com/volcengine/OpenViking/blob/5c9f17603862ff18d13bae596bde92e2398bb1ea/docs/en/guides/01-configuration.md)

### vectorize-io/agent-memory-benchmark #83

合并时间 2026-11-19T22:33:10Z，观测时间 2026-11-20T16:05:40.689Z，合并提交 5d422bea3ae4d971c84121cad2b38e6f64779401。在 2026-11-20T16:05:41.831Z 取得全部 11 个 PR 文件条目，按相关入口做静态审读。

[PR 与完整文件列表](https://github.com/vectorize-io/agent-memory-benchmark/pull/83) · [knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/dataset/knowledge.py) · [knowledge_data.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/dataset/knowledge_data.py) · [test_knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/tests/test_knowledge.py) · [hindsight_knowledge.py](https://github.com/vectorize-io/agent-memory-benchmark/blob/5d422bea3ae4d971c84121cad2b38e6f64779401/src/memory_bench/memory/hindsight_knowledge.py) · [补充来源 1](https://github.com/vectorize-io/agent-memory-benchmark/pull/90) · [补充来源 2](https://github.com/vectorize-io/agent-memory-benchmark/blob/9738aa01da59cb73dae43ac0f05ea3b16a55aa99/src/memory_bench/dataset/knowledge.py)

</details>
