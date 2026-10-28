# getzep/graphiti

面向 Agent 的动态知识图谱，关注事实关系及其随时间的变化。

## 记忆机制

以 episode 保存来源，将实体与事实关系组织为图，保留事实有效时间与失效历史。

## 部署和依赖

自托管图数据库和模型配置需由部署者提供；不要把 Zep 托管平台能力等同于 Graphiti。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | graph_temporal_memory |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `efc40d21b0afe28d6fc31d8c2c3e05752b02a9f1` |
| HEAD 观察（UTC） | 2026-10-28T03:34:44.026Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/getzep/graphiti/blob/main/README.md)；[该次记录的代码版本](https://github.com/getzep/graphiti/tree/c035afb7990b6077331a81e98b04efcfd9bf8184)。实现/评测资产线索：graphiti_core/ 与 tests/。README 阅读与 HEAD 采集并非同时完成；这部分证据属于上游说明，不等于代码审计。写入的具体触发条件、删除保证、隔离和存储后端，仍需结合对应实现进一步核实。

[元数据来源](https://api.github.com/repos/getzep/graphiti)；[HEAD 来源](https://api.github.com/repos/getzep/graphiti/git/ref/heads/main)。首次公开日期尚不明确，不能用仓库创建日期替代。

## 限制与本轮变化

本轮未执行索引、检索或性能实验；吞吐和延迟不作独立保证。

本轮仅建立基线。Release/PR 变化尚未逐项采集，不能据此认定没有发布。后续对比以真实时间戳、版本和来源为准。

## 最近检查的实现与发布状态

OpenAI 客户端的常规与 small 默认模型改为 gpt-6-luna，重排序默认模型改为 gpt-4.1-mini；客户端为 GPT-6 请求构造显式缓存选项，并按模型版本选择 reasoning 参数。这是调用兼容性和默认配置变化，未验证实际费用、延迟或检索质量。

状态：`released`；版本 `v0.31.0`。[PR #1999](https://github.com/getzep/graphiti/pull/1999)，合并 commit `82db2a4c57e2a9995f5e9526f51d76799db60740`；事件（UTC）2026-10-14T21:09:02Z，观察（UTC）2026-10-15T08:50:08Z。证据等级：`code_inspected`；未运行上游。

[实现 1](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/llm_client/openai_base_client.py) · [实现 2](https://github.com/getzep/graphiti/blob/aca369364226a666ca541b061ff2a1a54b80f2ff/graphiti_core/cross_encoder/openai_reranker_client.py)

Release 增量已覆盖到上次成功采集位置；这不代表全部历史发布已收集，也不代表已独立验证上游测试。

正式发布证据：[v0.31.0](https://github.com/getzep/graphiti/releases/tag/v0.31.0)；发布（UTC）：2026-10-14T23:58:36Z。

## 2026-10-19 部署边界：MCP 参考服务器

- 新 HEAD 将 MCP 配置默认 host 从 `0.0.0.0` 改为 `127.0.0.1`；示例 Docker Compose 端口绑定也由全接口调整为本机回环；SECURITY.md 提醒参考服务没有认证与授权。默认收紧监听地址并不等于已部署实例可免做鉴权。
- 状态：已进入默认分支，未核实进入正式 Release。固定实现：[配置](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/mcp_server/src/config/schema.py)、[Docker Compose](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/mcp_server/docker/docker-compose.yml)、[安全声明](https://github.com/getzep/graphiti/blob/417c3a125ae3ac53c19b8e53fffaccf3e665a88e/SECURITY.md)；证据等级 `code_inspected`，事件时间未核实。

## 2026-10-20 Neptune 搜索组隔离

- 本轮固定 HEAD `3cc723cd292eb5c2ac5ea2c5539270b8e1b6389f` 的 Neptune 搜索路径增加 group_id 过滤条件；新建的单元测试覆盖节点、事件和社群检索时的 `group_ids` 条件。
- 此变化与前一轮 MCP 服务器默认收紧监听地址是不同层面的风险：前者限制搜索分组，后者限制网络暴露，不代表提供了完整认证/租户隔离。
- 来源：[实现](https://github.com/getzep/graphiti/blob/3cc723cd292eb5c2ac5ea2c5539270b8e1b6389f/graphiti_core/driver/neptune/operations/search_ops.py)、[测试](https://github.com/getzep/graphiti/blob/3cc723cd292eb5c2ac5ea2c5539270b8e1b6389f/tests/test_neptune_search_isolation.py)；状态：`merged_unreleased`（默认分支已有代码，但未确认为正式 Release 内容）；证据等级 `code_inspected`，本仓库未运行测试，事件时间未核实。

## 2026-10-28：Gemini 不再重复拼入 JSON schema

Gemini 客户端移除提示词中重复的 schema 文本，保留原生 response_schema、JSON MIME 和响应模型解析。使用该适配器的部署可跟踪此修改；没有证据量化 Token 或质量收益。

状态：`merged_unreleased`；选定实现为 `code_inspected`，发布声明为 `upstream_statement`；未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/getzep/graphiti/commit/5f7cda913854ab932b91c02e6a50970598641ecd)；来源版本 `5f7cda913854ab932b91c02e6a50970598641ecd`。
- 事件 UTC 2026-10-27T18:02:32Z；观察 UTC 2026-10-28T03:44:33.759Z。
- 已读范围：[graphiti_core/llm_client/gemini_client.py](https://github.com/getzep/graphiti/blob/5f7cda913854ab932b91c02e6a50970598641ecd/graphiti_core/llm_client/gemini_client.py)。
- 默认分支记录为 `efc40d21b0afe28d6fc31d8c2c3e05752b02a9f1`，采样 UTC 2026-10-28T03:34:44.026Z；其余差异未全部审查，历史记录保留。

</details>
