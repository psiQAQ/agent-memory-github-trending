# 2026-10-27：Receipt 证据写入中断

## 最先中断的环节与已知事实

run_id为 `20261026T160515Z-interactive`。日期按北京时间2026-10-27；该历史 interactive 是保守执行标签，触发来源未独立核验，不能据此认定人工运行。

Data [4017c12a255160429f7110845ac9d57f2fcd117a](https://github.com/psiQAQ/agent-memory-github-trending/commit/4017c12a255160429f7110845ac9d57f2fcd117a) 已发布且10/10路径回读通过后，首次导致整轮停止的中断位于 Receipt evidence 的 `create_blob`（`a153`，外部 `seg-050-pre`）。可见外层结果原文为：

```text
functions.exec aborted by user after 4784.5s
```

该文本来自包装器，不是 GitHub HTTP/权限响应。实际 GitHub 子调用开始、返回和服务端执行均未能确认；outcome=uncertain，denied=null。宿主为何产生该中断不可进一步证明，不根据“by user”文字猜测用户意图或内部机制。

待写 UTF-8 字节数765058、预计算 Git blob SHA `70fb7a5c379768e328f858a67be30edffcced060` 是内容身份，未被观察为成功返回 SHA。后续只读对账 `a155` 在 UTC 2026-10-26T17:50:43.113Z—17:50:43.586Z 返回404/NOT_FOUND。404是后续查询结果，不是首次中断原因；不证明载荷上限、权限问题或平台安全拒绝。此前内存处理可恢复的异常不等于此次首次整轮中断；不将阶段名或推测当作底层证据。

## 实际恢复与证据

恢复先核对原 Data、全部变更路径、20份 Snapshot/index 和原成功创建的 Receipt 对象，复用已校验 checkpoint/metrics，生成新 status 与紧凑证据，只发布独立 Receipt [4648d87b1e0c23e41e5603214f8505462ddaf81a](https://github.com/psiQAQ/agent-memory-github-trending/commit/4648d87b1e0c23e41e5603214f8505462ddaf81a)。四份 checkpoints/status/metrics/evidence 与 commit/tree/ref 的真实回读已通过；没有重采或重复发布 Data，也未修改任务设置。

一手留存：
- [恢复证据（固定版本）](https://github.com/psiQAQ/agent-memory-github-trending/blob/4648d87b1e0c23e41e5603214f8505462ddaf81a/state/run-evidence/2026/10/20261026T160515Z-interactive/20261026T181147Z-recovery-001.json)：first_uncertain_attempt_id=a153、first_failure_attempt_id=a155，records含实际可取得的原始错误及恢复调用。
- [原冻结 metrics](https://github.com/psiQAQ/agent-memory-github-trending/blob/4648d87b1e0c23e41e5603214f8505462ddaf81a/state/run-metrics/2026/10/20261026T160515Z-interactive.json)：三类来源各21/21，预选深读5/5，Data回读10/10；API三数null，instrumentation_complete=false。
- [恢复 status](https://github.com/psiQAQ/agent-memory-github-trending/blob/4648d87b1e0c23e41e5603214f8505462ddaf81a/state/status.json)：保存诊断与提交前 pending。Receipt不能预先证明自身回读，该文字不否定提交后已完成的真实回读。

原完整内存账本在中断后不可取得，只保留有明确来源的可得记录，没有追造时间、完整 pre/post 或来源认证。后续收尾只读核查出现过一次 RemoteProtocolError，同参只读GET重试成功；它发生在恢复完成之后，不能替代此次首次中断原因。

## 后续规则与验收边界

按[触发来源与恢复规范](../run-provenance.md)在入口立即取证、未知不猜、写不确定先对账、Data已发布只补Receipt。通过源文本单份保存、可靠身份引用和必要结果减少重复正文；这降低重复/恢复成本，但紧凑写入成功只证明那次调用成功，不证明765058字节导致此前中断。

历史来源仍为unknown/unverified。新规范不能补造历史平台运行记录；API埋点、触发来源、Data/Receipt发布分别验收，未来自然Scheduled仍待真实入口证据。
