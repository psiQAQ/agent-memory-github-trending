# API-native 定时维护协议

本协议用于 ChatGPT Scheduled。目标是完全消除 Scheduled 对 connector→filesystem、Python、shell、git clone 和持久工作树的依赖。

## 运行时必须具备

- GitHub 只读：repo metadata、refs、commits、trees、files/blobs、releases/search 等。
- GitHub 已授权写入：create_blob、create_tree、create_commit、update_ref。
- 运行上下文可保存本轮结构化数据直到当前轮结束。

不要求 Python、本地文件、Code Interpreter、Work/Codex、Actions 或第二调度器。

## 完整性证明

1. 固定默认分支 HEAD 与其真实 tree SHA。
2. 优先读取 recursive tree，必须明确 `truncated=false`。
3. 用完整 tree 中所有 blob 的 path/mode/type/sha 调用 `create_tree`，不传 base tree。
4. 返回 SHA 必须等于 pinned root tree SHA。
5. validation-index 中历史 snapshot 集合必须与 tree 的 `data/snapshots/YYYY/MM/*.json` 集合完全相同，逐项 blob SHA 相同。
6. data/projects.json 中 tracked/reference card 必须全部存在。
7. 所有必读文件 fetch 返回的 blob SHA 必须与 pinned tree 一致。

任一步失败都停止发布。

## 新批次

- 对正式项目采集 metadata、default-branch HEAD、releases；按 maintenance.md 做 bounded discovery/deep review。
- 逐字段按 data-contract 校验。
- Scheduled 新 batch 使用 `events=[]`；实质技术变化写项目卡/报告并进入 pending_work。
- 生成 snapshot JSON 后调用 `create_blob`，记录返回 blob SHA。
- 基于旧 validation-index 仅追加该 snapshot 的 path/blob/run/time、Stars 摘要和 source coverage，调用 `create_blob`。
- 其他计划变更文件也分别 create_blob。

## 发布

发布前重读 HEAD；若移动则基于新 HEAD/tree 重做受影响校验，最多一次。

使用真实最新 tree SHA 作为 `base_tree_sha`，只替换 allowlist 路径；create_commit 的 parent 是同一个最新 HEAD；update_ref 必须 force=false。

发布后：
- fetch data commit；
- 重新读取完整 tree；
- 回读全部 changed paths；
- 每个实际 blob SHA 必须等于 create_blob 返回值；
- 新 snapshot/index 对账必须通过。

## Receipt

基于 data commit 的 tree 直接生成新的 checkpoints/status blob，只推进真正成功且分页完整的 source。单独 create_tree/create_commit/update_ref(force=false)，再回读 receipt commit 与 state blob。

## 恢复

写入结果不确定时先按 run_id 和 snapshot path 检查 main；已存在且内容/SHA一致则继续 receipt，不重复发布。存在同 run_id 不同 blob 时停止并报告冲突。
