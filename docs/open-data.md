# 开放数据与导出

你可以直接下载本仓库的公开 JSON，或在浏览器中导出 Star 观测 CSV，无需密钥。这里提供的是版本化静态文件，不是实时上游 API。

## 选择数据入口

| 数据入口 | 包含内容 | 使用边界 |
| --- | --- | --- |
| [项目登记 JSON](../data/projects.json) | 分类、机制摘要、项目卡、稳定 ID | 正式项目与参照分开 |
| [候选 JSON](../data/candidates.json) | 未完成审查的线索及已有初审证据 | 不等于推荐名单 |
| [历史索引 JSON](../state/validation-index.json) | 快照路径、blob SHA、实际 Star 观测点 | 不是全量原始快照的替代品 |
| [运行状态 JSON](../state/status.json) | 最近数据提交、来源覆盖与最新指标 | 未知值不应当成零 |
| [当前观测](../reports/current.md) | 当期项目统计与范围 | 与技术简报更新时间可能不同 |

## 确认批次与来源

先用 `state/status.json.latest_snapshot_path` 确认已完成批次，不能只按文件名取最大值。原始快照保存在 `data/snapshots/YYYY/MM/` 下，可按索引的 path 下载。

下载后请保留来源、时间戳、repository_id 和 snapshot SHA。仓库迁移前后的 ID 不同时，不能拼接 Star 历史。

## 导出 Star 观测 CSV

<button id="export-stars" type="button" hidden>导出全部已索引 Star 观测 CSV</button>

点击导出按钮后，浏览器根据项目登记和历史索引生成 CSV，不访问上游仓库。文件包含 repository_id、项目名、UTC 观测时间、Stars、run_id、原始路径和 blob SHA；只导出真实观测点，不插值，也不为未知项目推测名称。

导出需要 JavaScript；禁用 JavaScript 时仍可直接下载上表的 JSON。

CSV 便于使用索引摘要，但导出过程不会重新下载、校验每一个历史快照。用于正式研究时，应根据 blob SHA 复核原始字节，并遵循[筛选与统计方法](methodology.md)。原始文件可从本站下载；需要不可变版本时，可在 GitHub 选择固定 commit 获取。
