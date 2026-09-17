# letta-ai/letta-code

带身份和持久记忆的有状态 Agent harness。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | stateful_agent, coding_agent |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 本次 HEAD | `435e2cfbad64c2b5aa95482130b0c52fecf122f2` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | code_inspected；Release 说明与相关提交 diff 均已核对，未运行上游代码 |

## 记忆机制

上游介绍 memory blocks、消息搜索、MemFS 的 Git 跟踪及周期性整理，允许上下文与技能随运行变化。

## 本轮变化

- [v0.32.12](https://github.com/letta-ai/letta-code/releases/tag/v0.32.12) 于 2026-09-16T19:11:27Z 发布；Release 说明包含向 subagent 转发 Desktop credentials、Cloud deployment interruption 恢复、teleport/slack/CI 等修复。
- [`41f2e7a`](https://github.com/letta-ai/letta-code/commit/41f2e7abc7ca06be7413db5e6cbfe273ec2fcab3)：停止 subagent 时从“只杀 launcher”改为终止完整进程树；POSIX 使用独立进程组并支持强制升级，Windows 使用 `taskkill /t /f`，`task_stop` 等待实际清理完成后再结束状态。

## 部署和依赖

CLI 可配置自己的模型连接；Cloud 的状态存储和远程计算是另一个部署边界。子 Agent 生命周期管理属于 harness 可靠性而非新的记忆算法。

## 证据边界

[当前代码版本](https://github.com/letta-ai/letta-code/tree/435e2cfbad64c2b5aa95482130b0c52fecf122f2)。v0.32.12 为上游发布声明；进程树清理为 commit/diff 级代码检查。没有执行上游 Agent、Cloud 服务或宿主集成测试。
