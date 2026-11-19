# mem0ai/mem0

为 Agent 提供记忆写入与检索接口的独立记忆层。

## 记忆机制

记录语义、实体及时间相关的记忆；重点追踪提取和更新策略。

## 部署和依赖

上游同时提供 OSS SDK、自托管服务器和托管平台；自托管不自动等于离线运行。

## 登记信息

| 字段 | 登记记录 |
| --- | --- |
| 状态 | tracked / engineering |
| 分类 | memory_layer |
| 首次发现（UTC） | 2026-09-16T06:31:26Z |
| 记录的 HEAD | `0df3e4b87df20785f0741370c75e44428796193e` |
| 许可证 | GitHub API 识别为 Apache-2.0；未作法律审查 |
| 证据等级 | upstream_statement；本轮仅检查 HEAD 差异，未运行上游代码 |

## 证据与核实范围

阅读了[上游 README](https://github.com/mem0ai/mem0/blob/main/README.md)；[记录的代码版本](https://github.com/mem0ai/mem0/tree/0df3e4b87df20785f0741370c75e44428796193e)。本轮从上一水位 `b51f7692...` 对比到当前 HEAD，只发现文档变化，没有据此生成技术事件。未运行服务或复现评测。

[元数据来源](https://api.github.com/repos/mem0ai/mem0)；[HEAD 来源](https://api.github.com/repos/mem0ai/mem0/git/ref/heads/main)。

## 限制与本轮变化

README 的托管平台评测包含未进入 OSS SDK 的专有优化，不能直接作为开源版本性能。本轮没有新 Release，HEAD 的文档差异不计为核心技术变化。

## 2026-11-19：兼容性与可靠性修正

Mem0 调整名称识别：连字符 GPT-5 名称及 GPT-6 家族进入推理参数分支。 使用 OpenAILLM 的单模型 Chat Completions 路径时，先核对模型名与显式 is_reasoning_model 设置。

OpenAIConfig.is_reasoning_model 默认 None 时才按名称判断；显式 True/False 优先。gpt-5.4 等点号 GPT-5 名称仍不因本次前缀规则进入该分支。_get_supported_params 在推理分支不传 temperature/top_p，也不传旧 max_tokens；不能据此声称所有调用都会发送 max_completion_tokens。OpenRouter 多模型路由及实际服务端参数支持未实测。

已读固定 HEAD 的入口、参数 helper、配置和上游测试；未运行 API 或上游测试。

[PR](https://github.com/mem0ai/mem0/pull/7939) 合并UTC 2026-11-18T07:24:33Z；审读材料观察UTC 2026-11-19T06:24:55.194Z。固定观察 HEAD `fff8a6472512d1bc1a4bccab8c645b65a1df7fe5`，证据等级 code_inspected（上述有界范围），未独立运行；发行包含关系未确认。

阅读范围：[mem0/llms/base.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/llms/base.py)；[mem0/llms/openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/llms/openai.py)；[mem0/configs/llms/openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/mem0/configs/llms/openai.py)；[tests/llms/test_openai.py](https://github.com/mem0ai/mem0/blob/fff8a6472512d1bc1a4bccab8c645b65a1df7fe5/tests/llms/test_openai.py)。
