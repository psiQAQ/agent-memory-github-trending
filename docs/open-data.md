# 开放数据与导出

原始数据已由本仓库公开托管，不需要密钥；这些是版本化静态文件，不是实时上游 API。下载者应保留来源、时间戳、repository_id 和 snapshot SHA，不跨仓库迁移拼接 Star。

| 数据入口 | 包含内容 | 使用边界 |
| --- | --- | --- |
| [项目登记 JSON](../data/projects.json) | 分类、机制摘要、项目卡、稳定 ID | 正式项目与参照分开 |
| [候选 JSON](../data/candidates.json) | 未完成审查的线索及已有初审证据 | 不等于推荐名单 |
| [历史索引 JSON](../state/validation-index.json) | 快照路径、blob SHA、实际 Star 观测点 | 不是全量原始快照的替代品 |
| [运行状态 JSON](../state/status.json) | 最近数据提交、来源覆盖与最新指标 | 未知值不应当成零 |
| [当前观测](../reports/current.md) | 当期项目统计与范围 | 与技术简报更新时间可能不同 |

每份原始快照可根据索引的 path 直接下载；其数据在 `data/snapshots/YYYY/MM/` 下。使用 `state/status.json.latest_snapshot_path` 确认已完成批次，不只按文件名取最大值。

<button id="export-stars" type="button" hidden>导出全部已索引 Star 观测 CSV</button>

CSV 在浏览器中从项目登记和历史索引生成，不调用上游仓库。它包含 repository_id、项目名、UTC 观测时间、Stars、run_id、原始路径和 blob SHA；只保留真实点，不插值，不替未知项目推测名称。禁用 JavaScript 时仍可直接下载上面的 JSON。

CSV 是索引摘要的便捷导出，不会重新下载并校验每一个历史快照。正式研究应据 blob SHA 复核原始字节，并遵循[筛选与统计方法](methodology.md)。原始文件既可从本站下载，也可在 GitHub 选择固定 commit 获取不可变版本。
