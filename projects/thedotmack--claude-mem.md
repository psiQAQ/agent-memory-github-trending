# thedotmack/claude-mem

捕获 Agent 会话观察，压缩后在后续会话检索和注入上下文。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | coding_agent_memory, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 最近观测 HEAD | `abd9aaab61995c53060a6bd15ce41e236f7c53e3` |
| HEAD 观察（UTC） | 2026-10-25T16:13:22.939Z |
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

## 2026-10-25：长叙事与刷新失败汇总

主分支增加 story-input 的 narrativeLimit / previousNarrativeChars，超长拒绝带实际长度；runAgentTask 汇总所有已尝试 Agent 的失败，而非仅最后一次回退错误。适用于排查工作进展叙事无法更新与刷新失败；不是记忆算法或性能收益结论。

状态：已合入，未进入本轮观测最新 Release v15.0.2。来源：[固定叙事实现](https://github.com/thedotmack/claude-mem/blob/a4469fd4fc036461c05257184fe6445755f8e370/src/services/work-view/request-groups.mjs)、[失败汇总](https://github.com/thedotmack/claude-mem/blob/a4469fd4fc036461c05257184fe6445755f8e370/src/services/agent-runner/run.ts)、[Release 对照](https://github.com/thedotmack/claude-mem/compare/v15.0.2...a4469fd4fc036461c05257184fe6445755f8e370)。事件 UTC 2026-10-24T23:18:19Z。证据等级 code_inspected，只针对选定源补丁；未审计 bundle，未执行上游。

本轮观察 UTC：2026-10-25T06:03:01.212Z；本轮 Release 增量已覆盖旧成功水位，不表示穷尽历史。

## 2026-10-26：首次设置的云依赖与记忆写入来源防护

- [v15.2.0](https://github.com/thedotmack/claude-mem/releases/tag/v15.2.0)于UTC2026-10-25T11:52:08Z发布，真实tag指向1ce03615ca3df37683baf22b5ac0a7b12d3e9866。新安装扫描近30天历史，向CMEM Cloud发送筛选后用户提示词，随后选择存储位置。At Home不构成首次设置离线保证；持续刷新与首次设置不同，不笼统说全部功能都云端。
- [已读HostedIntent](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/work-view/hosted-intent.ts)将ownerPrompts/improveProduct一起gzip上传/api/pro/intent；improveProduct=false并不在该函数中禁止上传。云端与完整筛选链未审计。
- [PR5039](https://github.com/thedotmack/claude-mem/pull/5039)于UTC2026-10-25T12:09:56Z合并；MemoryRoutes在saveMemory前检查浏览器Origin。无Origin本地客户端及同端口loopback保留信任模型，并非新增完整认证。[MemoryRoutes](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/worker/http/routes/MemoryRoutes.ts)与[实际helper](https://github.com/thedotmack/claude-mem/blob/abd9aaab61995c53060a6bd15ce41e236f7c53e3/src/services/worker/http/routes/SettingsRoutes.ts)已读并与固定tree/blob比对；[版本对照](https://github.com/thedotmack/claude-mem/compare/1ce03615ca3df37683baf22b5ac0a7b12d3e9866...fa4e6e0fcc7cf16ca746940e92207d2159a6a2cf)确认防护尚不在v15.2.0。
- 上一节叙事预算/失败汇总已被本轮v15.1.0发布说明列入；保留上一轮当时观察，不改写成历史早已发布。
- code_inspected仅限选定文件；发布/托管效果为upstream_statement，未执行上游或复现实验。完整24提交范围未逐一审计，待办保留。观察UTC 2026-10-25T16:21:15.560Z。
