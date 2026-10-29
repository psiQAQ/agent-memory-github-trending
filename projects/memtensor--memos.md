# MemTensor/MemOS

用于组织、检索、更新记忆，并在不同任务间复用经验的操作层。

## 记忆机制

关注记忆单元、图组织、调度和反馈修正，以及经验到可复用策略的转化。

## 部署和依赖

本地插件与云服务是不同组件；宿主支持和外部模型依赖应逐组件核对。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_management |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `176d4f676a93e0e34ca9fd50091eff5ad3236506` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；本轮检查了 HEAD 差异，未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/MemTensor/MemOS/blob/main/README.md)；[记录的代码版本](https://github.com/MemTensor/MemOS/tree/176d4f676a93e0e34ca9fd50091eff5ad3236506)。本轮从上一水位 `de806942...` 检查了 7 个提交的差异，主要新增按模型 QPS 的分布式 LLM 限流、Redis GCRA、配置与测试；它更偏基础设施可靠性，不当作新的记忆算法结论。

[元数据来源](https://api.github.com/repos/MemTensor/MemOS)；[HEAD 来源](https://api.github.com/repos/MemTensor/MemOS/git/ref/heads/main)。

## 限制与本轮变化

节省 token 等数字仍只属于作者报告。本轮没有运行服务，也没有独立验证限流在生产环境的行为。

## 2026-10-30：memos-local-plugin-v2.0.21 重点核对

本地插件的 Node engine 下限改为22，better-sqlite3 固定为13.0.3；附带自检会检查执行它的实际宿主 Node 版本，并尝试 SQLite 内存读写与 CPU ONNX 后端加载。 升级前核对加载插件的宿主进程是否使用 Node 22+；终端中的另一个 Node 版本不能替代宿主检查。本轮没有运行上游自检，尚未证明本机兼容性。

[合并 PR](https://github.com/MemTensor/MemOS/pull/2519)；[Release](https://github.com/MemTensor/MemOS/releases/tag/memos-local-plugin-v2.0.21)。合并 UTC 2026-10-29T08:33:08Z；发布 UTC 2026-10-29T09:15:46Z；观察 UTC 2026-10-29T19:18:28.621Z。证据等级 code_inspected，静态阅读 [apps/memos-local-plugin/package.json](https://github.com/MemTensor/MemOS/blob/e84eb655c6c63e79846b3ed98cc18272db0ace3d/apps/memos-local-plugin/package.json)、[apps/memos-local-plugin/scripts/verify-native-runtime.cjs](https://github.com/MemTensor/MemOS/blob/e84eb655c6c63e79846b3ed98cc18272db0ace3d/apps/memos-local-plugin/scripts/verify-native-runtime.cjs)；未独立复现。
