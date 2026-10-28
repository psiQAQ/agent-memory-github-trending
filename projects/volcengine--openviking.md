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
