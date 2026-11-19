# topoteretes/cognee

可自托管的 Agent Memory 平台，把文本、代码与会话经验组织为知识图谱、向量索引和可检索的长期上下文。

## 记忆机制

`remember` 写入永久或 session memory，`recall` 在图、向量和代码上下文间检索，`improve` 用反馈和会话经验丰富长期记忆。上游还提供 Claude Code、Codex、OpenClaw 与 MCP 接入。

## 部署和依赖

上游明确提供本地安装、自托管和 Docker 路线，也支持本地模型；完全离线行为未在本仓库验证。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_memory / coding_agent / session_memory |
| 首次发现（UTC） | 2026-09-16T07:36:37Z |
| 记录的 HEAD | `c0d18c80e24b7b78918e7642c03f6f128fdd2aee` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据边界

[记录的代码版本](https://github.com/topoteretes/cognee/tree/c0d18c80e24b7b78918e7642c03f6f128fdd2aee)。本轮只核对 README、metadata、HEAD 和 Release 水位，不复现检索质量。

## 2026-10-19 版本追踪：v1.6.5

- Release 声称优化 Trace backlog 和 cognify 批次、将 docstring 连接到代码图，并增加 memify API；自定义 graph_model 生成最低依赖 datamodel-code-generator >=0.56.0。
- 状态：已发布，效果/延迟没有本仓库实测；[v1.6.5](https://github.com/topoteretes/cognee/releases/tag/v1.6.5)，2026-10-16T20:10:50Z；证据等级 `upstream_statement`。
## 2026-10-24 新 Release：v1.6.6rc1（发布候选版标签）

- [官方 Release](https://github.com/topoteretes/cognee/releases/tag/v1.6.6rc1) 于 2026-10-23T01:46:26Z 发布，声明新增 `forget(clean_history=True)`、删除个人搜索历史的 API，并加强 Obsidian、Asana、OneNote 和 Drive 同步。发布标签含 rc1，**不宣称已稳定**。
- **升级兼容风险：** 删除 Dataset 现在清理搜索与会话历史；历史清理失败将导致删除/forget 失败；`run_info` 不再携带内嵌原始 data 字段。依赖审计记录或旧结构的调用方应先备份/修改适配。上游称同步性能改善，未由本仓库实测。
- 证据等级 `upstream_statement`，观测 UTC 2026-10-23T18:51:23.627Z；本轮 HEAD `37f788bd287750e10d7610173e5332b3843f6ebd`，HEAD 未变化不等于不存在新版本。

## 2026-10-31：v1.6.6 重点核对

新增冲突查询与选择事实的 REST/SDK 接口；实现检查数据集读写权限，记录用户选择，保留被替代事实，并在缓存清理失败时保留待完成标志。 需要人工裁决矛盾记忆的应用可评估接入。锁仅在进程内生效，多 API worker 须把同一数据集写入路由到一个 worker；旧无引用缓存和 append-only 缓存不在清理保证内。

[合并 PR](https://github.com/topoteretes/cognee/pull/6401)；[Release](https://github.com/topoteretes/cognee/releases/tag/v1.6.6)。合并 UTC 2026-10-29T20:50:54Z；发布 UTC 2026-10-29T21:33:43Z；观察 UTC 2026-10-30T16:09:30.647Z。静态源码版本 `df2b4facd7c1d73b59376fd251fb93674a9d60a3`，已确认包含该合并；证据等级 code_inspected，未独立复现。阅读范围：[cognee/api/v1/conflicts/routers/get_conflicts_router.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/api/v1/conflicts/routers/get_conflicts_router.py)、[cognee/modules/conflicts/methods.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/modules/conflicts/methods.py)、[cognee/modules/conflicts/models.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/modules/conflicts/models.py)、[docs/resolve-conflicts.md](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/docs/resolve-conflicts.md)。

## 2026-11-20｜PostgreSQL 每数据集连接池收窄并限制等待

图与按访问控制隔离的 PGVector 缺省池由2+20调为2+10；申请空闲连接的缺省等待统一为360秒。

状态：已发布 v1.6.10；tag 含合并提交。

### topoteretes/cognee #6787

PGVector 的 VECTOR_POOL_ARGS 优先于 POOL_ARGS，只有二者未显式提供且 backend access control 开启时，采用2+10的小池默认；非该路径仍可使用关系池5+35默认。二进制写池独立于 SQLAlchemy 池、按相同参数设上限，三处 acquire 均传入 pool_timeout；不是连接建立超时。图池显式 POOL_ARGS、NullPool 分支保留，关系池大小未变。多数据集并行仍会累加连接数，不构成全进程连接总量保证；未连接 PostgreSQL 做负载实验。

合并 UTC 2026-11-18T20:32:05Z；PR观察 UTC 2026-11-19T16:34:47.206Z；固定合并提交 `ebd8caba08799c719ec56c12939ec27ebdb5352d`。证据等级 `code_inspected`（有界静读）；未运行上游代码或测试。

[PR](https://github.com/topoteretes/cognee/pull/6787)；[cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/vector/pgvector/PGVectorAdapter.py)（blob `d13cb6fca18733cfb97ba1931887a878544e7989`）；[cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/relational/sqlalchemy/SqlAlchemyAdapter.py)（blob `5d2fde46eb9bc1617b65e4740860b01948d222b7`）；[cognee/infrastructure/databases/graph/postgres_demo/adapter.py](https://github.com/topoteretes/cognee/blob/ebd8caba08799c719ec56c12939ec27ebdb5352d/cognee/infrastructure/databases/graph/postgres_demo/adapter.py)（blob `bd1424f06c391ddf50e3eb7012fc48ec7220ccb8`）

[发行](https://github.com/topoteretes/cognee/releases/tag/v1.6.10)：tag 解至 `c8a094375821f2d8c7c4945d3b2202e2e5d6603e`，沿已返回 compare 的实际 parents 可达本项合并提交。此为源码包含关系，不证明构建资产或运行效果。

来源批次 `20261119T160540Z-local`；[本轮日期稿](../reports/briefs/20261119T160540Z-local.md)。
