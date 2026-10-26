# TencentCloud/TencentDB-Agent-Memory

面向多 Agent 团队的记忆资产中枢，把会话、文档和代码整理为可复用资产。

## 记忆机制

上游把 Chat Memory、Skill、Wiki、CodeGraph 作为四类可治理资产，并支持团队共享、Agent 绑定、版本与权限管理。Proxy 路线面向多种 Coding Agent 复用同一 Memory Hub。

## 部署和依赖

上游提供本地多服务一键启动和面板，支持自托管；MongoDB 后端标记为实验性。自托管不代表不需要外部 LLM，离线运行未核实。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | team_memory / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `084bed45cad6bb7f877455082cee82835d65671a` |
| HEAD 观察（UTC） | 2026-10-26T16:12:34.326Z |
| 默认分支 | `feat/server_team` |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

[上游 README](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/README.md)；[机制说明采用的固定版本](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/8f2dc830317934e54548472bf62c5999f9bb1202)。本仓库没有执行安装脚本、Proxy 或 Memory Hub。

## 最近核实的发布

v2.0.3-beta.1 新增可替换的决策服务，集中处理 Skill 选择与 Memory L3 更新判定，并加入按需加载 Skill 和 Proxy 会话轨迹记录；这些新能力默认关闭。

按 beta 标签记录该版本，不据 GitHub 的 prerelease=false 推断稳定性；未运行 Proxy、决策服务或 MemoryCore。

[v2.0.3-beta.1 官方 Release](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.3-beta.1)；发布（UTC）：2026-10-13T10:43:52Z；观察（UTC）：2026-10-15T04:56:27Z；此段证据等级：`upstream_statement`。

## 2026-10-27：v2.0.3 会话默认配置与代理转发

正式发布说明新增用户 Team/Agent/Task 默认组合、文档导入和默认转发超时60分钟（显式配置不变）。选定源码显示转发重试共享总截止时间，设置成功日志放到 upsert 之后；发布声明的全部功能未逐项审计或运行。

状态：`released`；证据等级 `code_inspected`。这是选定实现和一手发布材料的检查，未运行上游或独立验证效果。

<details markdown="1">
<summary>本次证据与时间</summary>

- [一手来源](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases/tag/v2.0.3)；来源版本 `084bed45cad6bb7f877455082cee82835d65671a`。
- 事件 UTC 2026-10-26T14:09:03Z；观察 UTC 2026-10-26T16:15:42.090Z。
- 已读范围：`v2.0.3 upstream release statement`、`MemoryCore/src/metadata/service/user-session-default-service.ts`、`MemoryProxy/src/pipeline/stages/forward-with-retry.ts`。
- 记录的默认分支 HEAD：`084bed45cad6bb7f877455082cee82835d65671a`，采样 UTC 2026-10-26T16:12:34.326Z；不是实时最新版本，也不表示其他提交已经逐项审查。

</details>
