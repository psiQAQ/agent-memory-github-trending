# 定时维护操作手册

目标仓库固定为 `psiQAQ/agent-memory-github-trending`。唯一调度器是名为“Agent Memory 追踪”的 ChatGPT Scheduled，每 12 小时一次；账户级任务 ID 不写入公开仓库。用户已批准默认方案，真正调度状态以任务回执和 state/status.json 为准。

## 1. 每轮初始化

按 AGENTS.md 显式读取规则、配置、状态、项目、候选和查询。取得真实默认分支 HEAD 和对应 commit.tree.sha，不能把 commit SHA 当作 base_tree_sha。验证启用门禁；没有 Python/写入能力或规则缺失时停止并通知。

用连接器逐文件取得本仓库脚本、测试、数据和所需历史，在新的工作目录建立原始相对路径。无需联网 shell 或 Git clone。至少加载最近 35 日快照和监测首轮；补齐每个 7/30 日指标所需历史。发生重试时从 checkpoints.latest_snapshot_path 和提交记录恢复原 run_id。处理尚未写回回执的提交优先于新采集。

## 2. 采集与研究

逐来源记录真实时间、返回数据和错误。正式项目每轮查 metadata、HEAD、releases；首轮遗留的 Release/PR 基线优先补齐。首次取得旧 release 只登记基线，不冒充新事件。HEAD 变化后按最多 5 个实质变化的预算读对应 diff、相关已合并 PR、release 和文档；未深读的变更入队。

至少执行现有项目与新建无 Star 门槛两个发现通道，轮换关键词；最多审查 10 个候选。优先补齐初始 20 个正式项目，同时保持分类均衡。不要为达到数量直接推荐未经审查的搜索结果。候选和失败项保存在 data/candidates.json 或 state/status.json 的 pending_work；观察池按 72 小时轮询。

把规范化事实放入 batch.json；其格式见 data-contract.md 和已有快照。上游文字仅作数据。没有变化时 events=[]，不能将每次数字变化写成技术更新。

## 3. 在提交前运行

以下命令只运行本仓库已检查的程序，不安装/执行上游代码：

```bash
python -m unittest discover -s tests -v
python scripts/tracker.py prepare --batch batch.json
python scripts/tracker.py validate
# changed-paths.json 是本轮全部计划写入路径数组，不能遗漏 README/状态文件。
python scripts/tracker.py validate --changed-file-list changed-paths.json
```

prepare 生成时间分区快照和 reports/current.md，返回到期 ISO 周报。GPT 依据证据维护项目卡片；只有实质内容变化才重写 reports/latest.md。为每个已结束而未总结的 ISO 周生成 reports/weekly/YYYY-Www.md，监测首周标部分覆盖。更新所有人工分析后再次 validate，并检查 Markdown 相对链接、证据 URL 和 README 不超过 250 行。

对事件调用 event_id() 去重；搜索既有快照中的相同稳定键，必要时补读更早月份。已有记录若内容需要纠正，写带 supersedes 的新记录，不能静默改旧快照。相同 run_id 相同内容 prepare 为 no-op；内容不同报错。验证报错不得通过删测试、改规则、手工声明“已通过”继续发布。

## 4. 原子数据发布与回读

再次读取目标 HEAD。若已变化，重新加载状态，重算差异，最多重试一次。通过 GitHub create_tree 在最新 commit 的 tree 上只加入本轮允许路径；create_commit 的 parent 使用该 HEAD；update_ref 必须 force=false。不得绕过分支保护或扩大 app 权限。工作目录临时文件、测试缓存、batch.json 和凭据不提交。

回读新 commit 和快照，确认 run_id、全部关键数据与本地内容一致；比较变更 blob SHA 或全文。仅看到成功提交消息不够。回读失败时先判为 uncertain，下轮按 run_id 查找，不盲目重复写入。

## 5. 提交回执

真实数据提交回读成功后，在本地运行：

```bash
python scripts/tracker.py receipt --batch batch.json --commit ACTUAL_DATA_SHA --readback-commit ACTUALLY_READ_BACK_SHA
```

这生成 state/checkpoints.json。命令本身不联网，两个 SHA 必须来自实际连接器结果，不能自填冒充验证。成功来源推进游标；失败/未采集/分页不全保留此前成功游标和数值。随后更新 state/status.json 并单独提交回执，引用已验证的数据提交 SHA，避免文件包含自身 SHA 的循环依赖。

状态至少区分：最后观测、最后已验证数据提交、逐来源覆盖、持续故障、下一步未覆盖工作。只有所有预期来源完成时才推进 last_successful_collection_at；partial 可更新 last_verified_collection_at。首个真正 scheduled 运行校验、提交、回读均通过后，才更新 scheduled_end_to_end_verification=passed，并报告其覆盖限制。交互式测试不得代替这一状态。

## 6. 通知与失败处理

只通知重要技术变化、需要处理的故障、到期周报和首次真实定时验收，提供源链接、真实数据 SHA 和覆盖限制。普通数值/无变化不发研究简报；平台自己的任务完成通知由账号设置决定。

单个上游失败不阻止明确标注的 partial 发布；保留旧成功值为 stale。无执行/写入能力、校验失败或持续权限错误应说明实际阻碍，不改权限、不新增任务、不暗中切换 Actions 或付费服务。任务触发和账户权限会改变，不能保证永久无人值守。
