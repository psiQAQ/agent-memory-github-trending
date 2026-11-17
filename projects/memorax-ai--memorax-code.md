# memorax-ai/memorax-code

面向 Coding Agent 的记忆插件，组合云端工程经验检索、本地仓库知识和用户习惯。

## 记忆机制

[宿主 Hook 接入](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/ts/memorax-code-backend/src/memory/service.ts)将 Codex、Claude Code 等宿主的会话事件交给本地 Backend。[自动回写路径](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/ts/memorax-code-backend/src/memory/automatic-writeback.ts)对会话内容做有界处理，按配置和仓库作用域决定是否发送。[MemoraX 适配器](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/ts/memorax-code-backend/src/provider/memorax/adapter.ts)调用远端 Add/Search 服务。[Repo Memory](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/ts/memorax-code-adapter-common/src/repo-memory/repo-memory-shared-bundle.mjs)依据本地远端跟踪分支管理共享仓库知识，供不同 worktree 复用。用户偏好及流程记忆的本地保存规则见[固定 README](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/README.md)。

## 部署和依赖

[npm 包](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/npm/memorax-code/package.json)提供 CLI 和宿主入口。云端 Coding Memory 需要 MemoraX 用户标识和 API 凭据，缺失时[配置解析](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/packages/ts/memorax-code-backend/src/provider/memorax/config.ts)返回失败。上游说明完成配置后会启用自动回写，支持的宿主默认保留本地 trace，具体记录内容随宿主和配置变化。MIT 范围对应客户端仓库，云端服务内部存储与模型未核实。

## 评测证据

由用户提供线索。[上游跨会话示例](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/README.md)用于说明预期操作。[Agent Memory Leaderboard 第一周期](https://agentmemoryleaderboard.ai/home)的 Coding 表登记的是 `MemoraX v0.5` 参评 API，其版本与本项目卡所审查的公开插件不同，榜单结果只对应参评 API。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 仓库 ID | 1318893208 |
| 创建时间（UTC） | 2026-08-01T02:13:37Z |
| 首次发现（UTC） | 2026-11-17T08:45:21.870Z |
| 首次公开 | 未核实 |
| 审读版本 | [固定提交](https://github.com/memorax-ai/memorax-code/tree/89c7c041dd56d713c7a968d27c5ac8c543c206bf)，证据观察至 2026-11-17T08:49:14.514Z |
| 观察到的 GitHub Release | [v0.1.23](https://github.com/memorax-ai/memorax-code/releases/tag/v0.1.23)，发布于 2026-11-12T01:35:56Z |
| 许可证 | [固定版本 LICENSE](https://github.com/memorax-ai/memorax-code/blob/89c7c041dd56d713c7a968d27c5ac8c543c206bf/LICENSE)，GitHub API 识别为 MIT |
| 证据等级 | code_inspected；尚无本仓库运行或评测结果 |

Release 记录用于建立跟踪基线。每日采集将分别记录元数据、默认分支 HEAD 和完整增量 Release。
