# MemTensor/MemRL

研究 episodic memory 如何通过运行时强化学习持续更新，而不修改模型权重。

| 字段 | 当前记录 |
| --- | --- |
| 状态 | tracked / research |
| 分类 | episodic_memory / runtime_rl |
| 首次发现（UTC） | 2026-09-17T16:27:32Z |
| 本次 HEAD | `c1b322ca43de36ddf64c6712f89d0095bfc35ce0` |
| 许可证 | GitHub API 识别为 MIT；未作法律审查 |
| 证据等级 | upstream_statement；未复现实验 |

## 记忆机制

上游提出 Two-Phase Retrieval，用环境反馈筛选高效 episodic strategies，把稳定推理能力与可塑记忆分离。公开代码包含 HLE、BigCodeBench、ALFWorld 和 Lifelong Agent Bench 入口。

## 部署和依赖

提供 Python 本地安装与配置；部分 benchmark 需要 Docker、LLM 与 embedding endpoint。

## 证据边界

[当前代码版本](https://github.com/MemTensor/MemRL/tree/c1b322ca43de36ddf64c6712f89d0095bfc35ce0)。论文/README 的性能结论均视为作者声明，本仓库没有复现。
