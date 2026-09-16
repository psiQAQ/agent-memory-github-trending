# 数据契约 1.0

契约的可执行定义是 `scripts/tracker.py` 中 validate_registry/validate_batch/validate_repo；不依赖外部 JSON Schema 包。所有 JSON 使用 UTF-8，UTC 时间以 Z 结尾；未知值用 null，不能用 0 或空列表伪装成功。

## 项目登记

`data/projects.json` 包含 schema_version 和 projects。正式条目包含 repository_id（稳定整数）、full_name、status、kind、tags、first_discovered_at、created_at、first_public_at、summary、source_url、source_version_or_sha、evidence_level、implementation_evidence、card。status 可为 tracked/reference/watchlist/candidate/retired；kind 为 engineering/research/benchmark/reference。未审查线索另在 candidates.json，不从名称推断实现质量。

## 观测批次

每轮先在工作目录生成 batch.json，参考仓库已有快照的实际结构。顶层必填：

```text
schema_version = "1.0"
run_id = YYYYMMDDTHHMMSSZ-scheduled（同一轮重试复用，不重新造 ID）
run_type = scheduled | interactive | interactive_baseline
observed_at = 批次完成 UTC 时间
base_commit_sha = 本轮读取的目标仓库 HEAD
expected_repository_ids = 本轮预定覆盖的 ID 数组
observations = 每个预定 ID 恰好一个对象
discovery = 实际查询日志（无搜索时空数组，同时解释原因）
events = 已核实实质变化（无变化时空数组）
```

每个 observation 包含 repository_id、full_name，以及 metadata/head/releases 三个 source 对象。source 对象统一包含 status（ok/error/not_collected）、observed_at、source_url、value。失败或未采集必须 value=null 并给 reason，不遗漏对象。source_url 必须是对应上游仓库的实际 GitHub API URL。

metadata.value：stars、forks 为非负整数；archived 为布尔；default_branch；created_at；pushed_at（未知可 null）；license_spdx（未知可 null）。head.value 是完整 40 位 commit SHA。releases.value 为列表，每项含 id、tag、published_at、url；releases.status=ok 时必须给 complete 布尔，表示是否完成本轮所需分页范围。成功取得空列表与根本未采集不同。

初期读 `GET /repos/{owner}/{repo}`、`GET /repos/{owner}/{repo}/git/ref/heads/{default_branch}` 和 `GET /repos/{owner}/{repo}/releases?per_page=30&page=1`，按需要继续分页。记录 GitHub 连接器实际返回，不用 get_repo 的精简包装冒充完整计数。通过 README/代码差异/相关 PR 做技术解读；不在快照里保存个人 profile、权限或完整长 README。

## 事件与发现

事件必填 repository_id、type、claim、source_url、source_version_or_sha、event_at、observed_at、evidence_level、event_id。用脚本 event_id(event) 计算稳定键。第一次看到过去事件不等于刚发生；同源同版本的多次报道不重复。改写旧结论需新 source_version_or_sha 并附 supersedes。事件保存在不可变快照内，不另外复制一份相同原始内容。

每条 discovery 包含 query、page、returned、sort、observed_at、incomplete_results、pagination_complete。连接器未给 total_count/incomplete_results 时保留未知，不能猜测。候选队列记录来源、稳定 ID 和审查状态。

## 执行输出

prepare 输出本轮待提交路径和到期周报列表；不会调用 GitHub。render 输出当前 Markdown。receipt 只在真实 GitHub 提交完成并回读比对后运行，用于生成逐来源成功游标；不能凭自己填两个相同 SHA 就声称已验证。

`reports/current.md` 的“fresh”只表示本轮得到新元数据，不代表其余来源全量覆盖。缺失增长显示“—”；具体区间由 growth() 返回。每轮应在简报或状态说明释放/PR/深读的实际覆盖范围。
