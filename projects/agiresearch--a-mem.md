# agiresearch/A-mem

研究 Agent 如何动态组织、链接和演化记忆，实现采用 Zettelkasten 思路。

## 记忆机制

新记忆会生成结构化属性、上下文与标签，检索历史记忆建立连接，并在新增或更新时触发记忆演化。向量索引使用 ChromaDB。

## 部署和依赖

上游包可本地安装，并列出 OpenAI 与 Ollama 后端；是否能完全离线取决于所选模型与 embedding，未实测。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / research |
| 分类 | agentic_memory / memory_evolution |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `ceffb860f0712bbae97b184d440df62bc910ca8d` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未运行上游代码 |

## 证据与核实范围

[上游 README](https://github.com/agiresearch/A-mem/blob/main/README.md)；[记录的代码版本](https://github.com/agiresearch/A-mem/tree/ceffb860f0712bbae97b184d440df62bc910ca8d)。README 明确指出论文结果复现使用另一个仓库，本卡不把该论文结果当成本仓库已复现结果。
