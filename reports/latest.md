# Agent Memory 简报｜2026-10-31

Letta Code 发布 Windows 外部 worker 启动修复；Cognee 发布可持久保存人工选择的事实冲突解决接口。
受影响的是在 Windows 调用 npm 安装的外部 CLI，或需要人工裁决矛盾记忆的应用。
前者升级后仍需本机复测；后者接入前需核对写入路由与缓存边界。本轮结论来自静态源码，未运行上游程序。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code/releases/tag/v0.34.32) | Windows 外部 worker 和 Codex app-server 改经 cross-spawn 启动，可解析 npm 的 .cmd 包装；模型发现保留启动错误，避免只暴露后续 EPIPE。 | 已发布 v0.34.32 | 遇到命令可在 PowerShell 运行、worker 却报找不到或 EPIPE 的用户，可在升级后复测启动和进程退出。上游明确未在真实 Windows 机器验证，本轮也未运行。 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee/releases/tag/v1.6.6) | 新增冲突查询与选择事实的 REST/SDK 接口；实现检查数据集读写权限，记录用户选择，保留被替代事实，并在缓存清理失败时保留待完成标志。 | 已发布 v1.6.6 | 需要人工裁决矛盾记忆的应用可评估接入。锁仅在进程内生效，多 API worker 须把同一数据集写入路由到一个 worker；旧无引用缓存和 append-only 缓存不在清理保证内。 |

## Star 变化：真实间隔约 20.87–23.48 小时

下表比较逐项目上一轮与本轮真实观测，按类别与登记顺序排列。7日/30日合格基线分别为 21/21、0/21，容差为 ±6 小时；实际起止时刻见折叠区。此处不外推24小时或周增量，关注度不代表质量。

| 项目 | 类型 | 起点 Stars | 本次 Stars | 实际区间净变化 |
| --- | --- | ---: | ---: | ---: |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | engineering | 68056 | 68107 | +51 |
| [getzep/graphiti](https://github.com/getzep/graphiti) | engineering | 32335 | 32367 | +32 |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | engineering | 12178 | 12199 | +21 |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | engineering | 104424 | 105687 | +1263 |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | engineering | 3736 | 3741 | +5 |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | engineering | 56088 | 56456 | +368 |
| [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory) | engineering | 30098 | 30255 | +157 |
| [memodb-io/memobase](https://github.com/memodb-io/memobase) | engineering | 2941 | 2942 | +1 |
| [neo4j-labs/agent-memory](https://github.com/neo4j-labs/agent-memory) | engineering | 596 | 596 | +0 |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | engineering | 41136 | 41193 | +57 |
| [redis/agent-memory-server](https://github.com/redis/agent-memory-server) | engineering | 323 | 323 | +0 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | engineering | 32898 | 32927 | +29 |
| [obra/episodic-memory](https://github.com/obra/episodic-memory) | engineering | 494 | 494 | +0 |
| [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | engineering | 4375 | 4379 | +4 |
| [VectorSpaceLab/general-agentic-memory](https://github.com/VectorSpaceLab/general-agentic-memory) | research | 864 | 864 | +0 |
| [agiresearch/A-mem](https://github.com/agiresearch/A-mem) | research | 1211 | 1212 | +1 |
| [MemTensor/MemRL](https://github.com/MemTensor/MemRL) | research | 193 | 193 | +0 |
| [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | benchmark | 1182 | 1184 | +2 |
| [xiaowu0162/LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2) | benchmark | 199 | 199 | +0 |
| [vectorize-io/agent-memory-benchmark](https://github.com/vectorize-io/agent-memory-benchmark) | benchmark | 159 | 159 | +0 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | reference | 25289 | 25292 | +3 |

## 新候选对比

两条发现查询各取第一页，共返回 40 条原始线索。本轮完成候选初审0项、正式晋升0项，登记池保持 47/50；线索留在原始发现记录中等待核对稳定 ID。下表仅转述公开描述，未确认实现、依赖或成熟度。

| 搜索线索 | 上游描述的机制或资产 | 依赖、宿主、成熟度 | API 许可证线索 | 处理 |
| --- | --- | --- | --- | --- |
| [RyanW124/RegMem](https://github.com/RyanW124/RegMem) | 回归引导的记忆整合，保留决策相关信息 | 未核实 | MIT，适用文件未核实 | 待初审 |
| [zensation-ai/zenbrain](https://github.com/zensation-ai/zenbrain) | 分层记忆、间隔重复与整合；描述提及 TypeScript/MCP 接入 | 未核实 | Apache-2.0，适用文件未核实 | 待初审 |
| [dmzhou95/ReMem](https://github.com/dmzhou95/ReMem) | 可逆情景记忆路由，用于长上下文推理 | 未核实 | Apache-2.0，适用文件未核实 | 待初审 |

## 方法与边界

21个登记项目的 metadata、HEAD、Release 增量范围均已取得；两项预选变化已完成源码、合并与发布关系核对，其他变化仍待审。搜索仅覆盖两条查询的第一页，不代表生态普查。未执行上游程序、实验或付费评测，不能据此确认运行兼容性、持久性或性能收益。

<details markdown="1">
<summary>证据与时间</summary>

批次 `20261030T155835Z-local`；完成时间 UTC 2026-10-30T16:09:30.647Z。[原始快照](../data/snapshots/2026/10/20261030T155835Z-local.json)；[索引](../state/validation-index.json)；[状态](../state/status.json)。触发来源 unknown/unverified，legacy interactive 标签不证明人工或自然定时触发。

### letta-ai/letta-code

- [合并 PR](https://github.com/letta-ai/letta-code/pull/5365)，合并 UTC 2026-10-29T16:30:30Z；[Release](https://github.com/letta-ai/letta-code/releases/tag/v0.34.32)，发布 UTC 2026-10-30T02:20:03Z。
- 已确认合并 `981f9fbbd2bdbdb9c584fdac6e3288b8e600e38b` 是发布提交 `0cd08ecf0585dfd5851826ad38b3f1440af51627` 的祖先；代码观察 UTC 2026-10-30T16:09:30.647Z，证据等级 code_inspected。
- 已静态阅读：[src/utils/package-manager-spawn.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/utils/package-manager-spawn.ts)；[src/agent/subagents/subagent-process.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/agent/subagents/subagent-process.ts)；[src/tools/impl/codex-app-server.ts](https://github.com/letta-ai/letta-code/blob/0cd08ecf0585dfd5851826ad38b3f1440af51627/src/tools/impl/codex-app-server.ts)。

### topoteretes/cognee

- [合并 PR](https://github.com/topoteretes/cognee/pull/6401)，合并 UTC 2026-10-29T20:50:54Z；[Release](https://github.com/topoteretes/cognee/releases/tag/v1.6.6)，发布 UTC 2026-10-29T21:33:43Z。
- 已确认合并 `94ca27397c81943ddcf8e36f0625d843995c8ff5` 是发布提交 `df2b4facd7c1d73b59376fd251fb93674a9d60a3` 的祖先；代码观察 UTC 2026-10-30T16:09:30.647Z，证据等级 code_inspected。
- 已静态阅读：[cognee/api/v1/conflicts/routers/get_conflicts_router.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/api/v1/conflicts/routers/get_conflicts_router.py)；[cognee/modules/conflicts/methods.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/modules/conflicts/methods.py)；[cognee/modules/conflicts/models.py](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/cognee/modules/conflicts/models.py)；[docs/resolve-conflicts.md](https://github.com/topoteretes/cognee/blob/df2b4facd7c1d73b59376fd251fb93674a9d60a3/docs/resolve-conflicts.md)。

### 逐项目观测时刻

| 项目 | 起点 UTC | 终点 UTC | 小时 |
| --- | --- | --- | ---: |
| mem0ai/mem0 | 2026-10-29T16:31:47.227Z | 2026-10-30T16:00:41.086Z | 23.4816 |
| letta-ai/letta | 2026-10-29T16:31:48.178Z | 2026-10-30T16:00:42.539Z | 23.4818 |
| getzep/graphiti | 2026-10-29T16:32:25.921Z | 2026-10-30T16:01:09.257Z | 23.4787 |
| MemTensor/MemOS | 2026-10-29T16:32:26.855Z | 2026-10-30T16:01:10.251Z | 23.4787 |
| thedotmack/claude-mem | 2026-10-29T16:32:54.752Z | 2026-10-30T16:01:41.876Z | 23.4798 |
| xiaowu0162/LongMemEval | 2026-10-29T16:32:55.799Z | 2026-10-30T16:01:42.723Z | 23.4797 |
| xiaowu0162/LongMemEval-V2 | 2026-10-29T16:33:31.061Z | 2026-10-30T16:02:07.260Z | 23.4767 |
| letta-ai/letta-code | 2026-10-29T16:33:31.971Z | 2026-10-30T16:02:08.149Z | 23.4767 |
| vectorize-io/hindsight | 2026-10-29T16:33:54.987Z | 2026-10-30T16:02:33.957Z | 23.4775 |
| TencentCloud/TencentDB-Agent-Memory | 2026-10-29T16:33:55.893Z | 2026-10-30T16:02:34.859Z | 23.4775 |
| VectorSpaceLab/general-agentic-memory | 2026-10-29T16:34:23.161Z | 2026-10-30T16:03:04.725Z | 23.4782 |
| agiresearch/A-mem | 2026-10-29T16:34:24.062Z | 2026-10-30T16:03:05.641Z | 23.4782 |
| memodb-io/memobase | 2026-10-29T19:11:25.592Z | 2026-10-30T16:03:29.150Z | 20.8677 |
| neo4j-labs/agent-memory | 2026-10-29T19:11:26.533Z | 2026-10-30T16:03:30.143Z | 20.8677 |
| volcengine/OpenViking | 2026-10-29T19:11:50.747Z | 2026-10-30T16:03:54.266Z | 20.8676 |
| vectorize-io/agent-memory-benchmark | 2026-10-29T19:11:51.734Z | 2026-10-30T16:03:55.204Z | 20.8676 |
| redis/agent-memory-server | 2026-10-29T19:12:22.641Z | 2026-10-30T16:04:19.608Z | 20.8658 |
| topoteretes/cognee | 2026-10-29T19:12:23.590Z | 2026-10-30T16:04:20.648Z | 20.8658 |
| MemTensor/MemRL | 2026-10-29T19:12:50.319Z | 2026-10-30T16:04:44.805Z | 20.8651 |
| obra/episodic-memory | 2026-10-29T19:12:51.186Z | 2026-10-30T16:04:45.671Z | 20.8651 |
| tigerless-labs/agent-memory | 2026-10-29T19:13:13.861Z | 2026-10-30T16:05:12.440Z | 20.8663 |

### 发现与参考覆盖

- `"memory consolidation" in:name,description archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；returned=20，total_count=315，incomplete_results=false，pagination_complete=false；观察 UTC 2026-10-30T16:06:00.466Z。
- `"episodic memory" in:name,description created:>=2026-09-30 archived:false fork:false`：sort=updated、order=desc、page=1、per_page=20；returned=20，total_count=60，incomplete_results=false，pagination_complete=false；观察 UTC 2026-10-30T16:06:02.031Z。
- 本轮读取的 [Verging Labs JSON](https://verginglabs.com/index/memory.json) 与[变更记录](https://verginglabs.com/changelog)仍列 v0.2、2026-09-16、datasetId=6b0dd2681430eca3。网页工具注明内容分别抓取于3天和2天前，未证明源站即时状态；不作为本轮新技术事件，也不转用其分数证明开源库性能。

</details>
