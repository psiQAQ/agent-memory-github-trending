# vectorize-io/hindsight

以 retain、recall、reflect 接口组织 Agent 的记忆使用。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer / coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `4f1b06293453c966752102464442352769b756db` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；本轮对新增提交做了代码差异检查，未运行上游代码 |

## 记忆机制

retain 保存信息，recall 查询记忆，reflect 结合记忆生成回应；memory bank 用于组织命名空间。Coding Agent 集成还负责首轮上下文注入和 companion skill 的宿主适配。

## 部署和依赖

上游提供自托管、嵌入式与 Cloud 路线，并维护多种 Coding Agent 集成；文档列出 PostgreSQL 及本地/托管模型选项。

## 证据与核实范围

[当前代码版本](https://github.com/vectorize-io/hindsight/tree/4f1b06293453c966752102464442352769b756db)。本轮从 `be0e9399...` 到当前 HEAD 共检查 14 个提交的文件差异，核实到四项与 Agent Memory 直接相关的变化：

- [autoInject](https://github.com/vectorize-io/hindsight/commit/9ef0d901cbb5085e4fc4b54e3b1116a778eb2292)：首轮提示可在 `reflect`、`pages`、`recall` 或关闭注入之间选择，并统一 recall 配置。
- [plugin-manager skill delivery](https://github.com/vectorize-io/hindsight/commit/d73c517b42358e167eb20f797f1f084d288e5b52)：修复通过宿主自身插件管理器安装时 companion skill 未落地的问题，并为 OpenCode v2 提供内存注册路径。
- [bank transfer](https://github.com/vectorize-io/hindsight/commit/6e6098a03426b49446cd3a344242988e526f54aa)：统一 memory bank 的导出/导入 API，可选择数据、bank 配置和历史，并修复同实例复制时 directives/webhooks 静默丢失。
- [Anthropic reflect truncation](https://github.com/vectorize-io/hindsight/commit/4f1b06293453c966752102464442352769b756db)：将未显式限额时的默认输出上限从 4096 提高到 64000，并把 reflect 配置传入工具调用循环，避免长 `done` payload 被静默截断。

## 限制与本轮变化

以上为提交与 diff 级代码检查，不是运行时复现；没有执行上游服务、benchmark 或宿主集成测试。Release 水位仍为 v0.10.0，本轮变化来自默认分支提交而非新 Release。
