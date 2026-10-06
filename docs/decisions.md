# 已批准决策

## 2026-09-16

仓库所有者明确确认采用全部默认方案。本页仅保存工程决策，不保存个人资料或聊天内容。

| 项目 | 已批准选择 |
| --- | --- |
| 研究范围 | 工具、论文代码、评测；无代码论文仅为背景；纯 SaaS 不进主榜 |
| 研究重点 | 各类均衡，增加 Coding Agent 与本地部署视图 |
| 发布权限 | 已批准规则内的数据/报告直写 main；后续规则和脚本变更另行提议 |
| 调度 | 初始方案为从启用起每 12 小时；后续已被同日的调度调整取代 |
| 通知 | 重要变化、需处理故障、周报、首次定时验收 |

本次初始化实现属于该批准范围。不会因为持续维护而自行扩大写入范围、访问私人资料、增加付费 API 或另设调度平台。初始目标 20 个正式项目不是降低审查标准的配额。第一轮只有 8 个正式项目和 1 个历史参照，其余候选继续审查。

## 2026-09-16 调度调整

仓库所有者明确将检查频率从“每 12 小时一次”调整为：**每天北京时间 00:00（Asia/Shanghai）执行一次**。

- 该决定仅覆盖原 A–E 默认方案中的调度项，其他研究范围、发布权限和通知策略保持不变。
- 原始数据仍以 UTC 保存，中文报告仍使用 Asia/Shanghai 展示。
- 下一次计划运行时间为 2026-09-17 00:00（北京时间），对应 2026-09-16 16:00 UTC。

## 2026-09-29 执行工作树调整

仓库所有者明确批准：完整 tree 索引与固定 HEAD 保留，工作树改为按实际执行依赖物化，每个使用文件仍须 size/mode/type/Git blob SHA 校验；未物化文件通过完整 base tree 保留。当前 validator 的全部历史快照与项目卡依赖不得省略。同步维护规则说明和现有定时任务描述，并执行一次交互式完整维护；不把交互验收替代真实定时验收。

批准加入 Agent Memory 排行榜的一手方法参考及经核实的参评仓库线索。研究范围、门禁、写入边界、每天北京时间零点的频率、唯一调度器及禁止上游执行/额外费用保持不变。后续日常轮次无权自行修改规则或停用定时任务。


## 2026-10-02 Manifest 校验与恢复自动维护

仓库所有者明确批准新增不依赖完整历史工作树物化的 `validate-batch` / `validate-manifest` 路径，并在实现、测试、提交与回读验证后重新启用现有“Agent Memory 追踪”任务。

- 完整默认分支 HEAD/tree 固定、完整 tree 索引、Git blob SHA 校验和非强制 ref 更新要求不变。
- 新增 `state/validation-index.json`，把已验证历史 snapshot 的 path/blob SHA 与必要语义摘要绑定；历史原始 snapshot 继续 append-only 保存，不被 index 替代。
- 每轮只需落盘执行/编辑所需的小型输入；历史 snapshot 与项目卡通过完整 tree + validation index 验证，不再强制逐文件物化。
- index 缺失或不一致时禁止降级校验；只能停止发布或显式使用完整工作树 fallback 重新验证。
- 调度仍为每天北京时间 00:00，唯一调度器仍是现有 ChatGPT Scheduled；不新增第二调度器、付费 API、MCP 或上游代码执行。


## 2026-10-07 API-native Scheduled 执行协议

仓库所有者明确要求解决连续 Scheduled 失败。已确认失败发生在任何 data commit 之前，GitHub 权限和调度本身正常，结构性阻塞是 connector 内容无法可靠物化到 Scheduled 的 Python/临时文件系统。

批准将 Scheduled runtime 改为纯 GitHub API：
- 不再要求 Python、本地落盘、shell、git clone 或完整/稀疏工作树；
- 完整 tree 使用 GitHub `create_tree` 服务器端重建并比对 root SHA；
- snapshot 历史由完整 tree + validation-index 的 path/blob 关系验证；
- snapshot/index/reports/cards 直接 create_blob，发布仍使用真实 base tree、非强制 update_ref 和逐 blob readback；
- checkpoints/status receipt 直接由已验证 data commit 和本轮 batch 生成并独立提交；
- scripts/tests 保留为交互式开发参考，不是 scheduled runtime gate；
- 为避免无 cryptographic helper 时伪造 legacy event_id，API-native scheduled 的新 snapshot 使用 `events=[]`，重要变化仍更新项目卡/报告并加入 pending_work，后续可交互式结构化回填。

调度仍保持每天北京时间 00:00，唯一调度器和研究/写入/费用边界均不变。
