# getzep/graphiti

面向 Agent 的动态、时间感知知识图谱。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_temporal_memory |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `aca369364226a666ca541b061ff2a1a54b80f2ff` |
| HEAD 观察（UTC） | 2026-10-15T08:46:16Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

以 episode 保存来源，将实体与事实关系组织为图，保留事实有效时间与失效历史。

## 部署和依赖

自托管图数据库和模型配置需由部署者提供；不要把 Zep 托管平台能力等同于 Graphiti。

## 证据与核实范围

阅读了[上游 README](https://github.com/getzep/graphiti/blob/main/README.md)；[本轮记录的代码版本](https://github.com/getzep/graphiti/tree/c035afb7990b6077331a81e98b04efcfd9bf8184)。实现/评测资产线索：graphiti_core/ 与 tests/。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/getzep/graphiti)；[HEAD 来源](https://api.github.com/repos/getzep/graphiti/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

本轮未执行索引、检索或性能实验；吞吐和延迟不作独立保证。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。

## 最近检查的实现与发布状态

OpenAI 客户端的常规与 small 默认模型改为 gpt-6-luna，重排序默认模型改为 gpt-4.1-mini；客户端为 GPT-6 请求构造显式缓存选项，并按模型版本选择 reasoning 参数。这是调用兼容性和默认配置变化，未验证实际费用、延迟或检索质量。

状态：`released`；版本 `v0.31.0`。[PR #1999](https://github.com/getzep/graphiti/pull/1999)，合并 commit `82db2a4c57e2a9995f5e9526f51d76799db60740`；事件（UTC）2026-10-14T21:09:02Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/llm_client/openai_base_client.py) · [实现 2](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/cross_encoder/openai_reranker_client.py)

Release 增量已覆盖到上次成功水位；不代表穷尽历史发布或独立验收上游测试。

正式发布证据：[v0.31.0](https://github.com/getzep/graphiti/releases/tag/v0.31.0)；发布（UTC）：2026-10-14T23:58:36Z。

## 2026-10-19 部署边界：MCP 参考服务器

- 新 HEAD 将 MCP 配置默认 host 从 `0.0.0.0` 改为 `127.0.0.1`；示例 Docker Compose 端口绑定也由全接口调整为本机回环；SECURITY.md 提醒参考服务没有认证与授权。默认收紧监听地址并不等于已部署实例可免做鉴权。
- 状态：已进入默认分支，未核实进入正式 Release。固定实现：[配置](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/mcp_server/src/config/schema.py)、[Docker Compose](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/mcp_server/docker/docker-compose.yml)、[安全声明](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/SECURITY.md)；证据等级 `code_inspected`，事件时间未核实。
