# thedotmack/claude-mem

捕获 Agent 会话观察，压缩后在后续会话检索和注入上下文。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent_memory, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `75fc021a40655cbdd258f0e070f55a03ea9c8642` |
| HEAD 观察（UTC） | 2026-10-24T08:07:37.939Z |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 记忆机制

观察捕获→摘要/压缩→持久保存→按需检索与上下文回注；存储后端细节待代码核查。

## 部署和依赖

上游说明支持多种 Coding Agent；仅登记作者声明，不代表我们逐宿主安装验收。

## 证据与核实范围

阅读了[上游 README](https://github.com/thedotmack/claude-mem/blob/main/README.md)；[机制说明采用的固定版本](https://github.com/thedotmack/claude-mem/tree/dcfc44221deabc228b0698a0012f87ed2fe6bbe7)。实现/评测资产线索：src/ 与插件配置；以 README 的工作流说明为当前证据。README 阅读与 HEAD 采集不是原子操作；本条为上游说明，不冒充代码审计。具体写入触发、删除保证、隔离和存储后端需在对应实现中进一步核实。

[元数据来源](https://api.github.com/repos/thedotmack/claude-mem)；[HEAD 来源](https://api.github.com/repos/thedotmack/claude-mem/git/ref/heads/main)。首次公开日期未知，不以创建日期替代。

## 限制与本轮变化

部署路径可能涉及托管 observer 或外部模型；不能仅因插件在本地就认定数据不出网。

早期记录曾有 Release 增量缺口。本轮已取得与当前成功水位重叠的 Release 页；仅代表本轮增量范围完整，不对早期完整历史作追溯保证。

## 最近核实的发布

v13.39.0 修复 Codex 子代理在线程压缩后丢失记忆时间线：PostCompact 按 session_id/agent_id 标记线程，下一次 PostToolUse 恢复一次 timeline；SessionStart 清理标记以免根线程重复注入。

该结论来自正式 Release 说明；未检查本版本实现，也未验证各宿主实际行为。

[v13.39.0 官方 Release](https://github.com/thedotmack/claude-mem/releases/tag/v13.39.0)；发布（UTC）：2026-10-13T21:31:41Z；观察（UTC）：2026-10-15T04:56:26Z；此段证据等级：`upstream_statement`。

## 2026-10-19 版本追踪：v14

- v14.0.0 引入本地 My Work 查看 Agent 请求、状态和人工 Checked；v14.0.1 修复卡片的 Agent 归属。可选 TeamBrain 为独立商业团队服务，不将其收入开源功能范围。
- 状态：正式 Release；依据上游发布说明，未独立复现。
- 来源：[v14.0.0](https://github.com/thedotmack/claude-mem/releases/tag/v14.0.0)（2026-10-17T15:50:36Z）、[v14.0.1](https://github.com/thedotmack/claude-mem/releases/tag/v14.0.1)（2026-10-17T16:25:51Z）；证据等级 `upstream_statement`。

## 2026-10-24：v15.0.2 observer 输出预算修复

- 正式发布 UTC 2026-10-23T18:51:46Z；北京时间 2026-10-24。上游说明对 OpenRouter/cmem.ai/OpenAI-compatible observer 的推理预算与空回复重试作调整，防止输出预算用尽时零观测被当成正常结果。重试计入已有发送预算并累计用量；强制推理模型仍需按 provider 核对兼容性。
- [Release](https://github.com/thedotmack/claude-mem/releases/tag/v15.0.2)；[PR #5029](https://github.com/thedotmack/claude-mem/pull/5029) 已合并，合并 SHA `edc9880d7733a88b9f56f5ca006a998f22a54ae3`，UTC 2026-10-23T18:47:12Z。
- 等级 `upstream_statement`：阅读正式 Release 和 PR 全文，未执行作者测试、未验证实际提供方效果或费用。其他 103 个提交的完整变更范围尚未全部深读。
- 观察 UTC 2026-10-24T08:07:38.578Z；当前 HEAD 如上表，不能以其移动认定全部变更属于本 Release。
