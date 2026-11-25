# Agent Memory 简报｜2026-11-26

Letta Code 的本地后端可在模型请求前压缩接近上限的上下文。OpenViking 增加了只读会话历史查询。
使用 OpenRouter 的 claude-mem 部署可受益于临时错误分类修正。Hindsight 的 Coding Agents 集成会在默认云端地址缺少 token 时关闭记忆。
升级前先确认本地后端、会话捕获和云端凭据各自的配置。使用 Graphiti MCP 合并镜像时请核对镜像标签。

## 已确认合并/发布的变更

| 项目 | 变化 | 状态 | 影响与行动 |
| --- | --- | --- | --- |
| [Letta Code](https://github.com/letta-ai/letta-code/commit/c67a0d59263262a947b3dce3420b2c35b46bd829) | 本地后端在模型请求前检查上下文压力，必要时先压缩。 | 已合并，发行包含关系待核实 | 使用本地后端的团队可检查长会话在发出模型请求前的压缩记录。 |
| [OpenViking](https://github.com/volcengine/OpenViking/commit/035eae65139825d1c44e43ce50cde12cc2192f14) | 会话历史工具可按会话查找已保存的对话记录。 | 已合并，发行包含关系待核实 | 使用 Gateway 的团队可先检查会话捕获及工具策略。 |
| [claude-mem](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.3) | OpenRouter 的 HTTP 200 响应内若含临时上游错误，观察器会按实际错误分类。 | v16.1.3 发布，v16.1.5 源码仍包含 | 使用 OpenRouter 的部署可关注限流或上游故障后的队列暂停与恢复。 |
| [Hindsight](https://github.com/vectorize-io/hindsight/commit/e611e8b114576b33069e40ca665f50612eea91c2) | Coding Agents 集成在默认 Hindsight Cloud 地址缺少 API token 时关闭记忆。 | 已合并，发行包含关系待核实 | 使用默认云端地址时，先确认最终配置包含有效 token。 |
| [Graphiti MCP](https://github.com/getzep/graphiti/releases/tag/mcp-v1.1.5) | MCP 1.1.5 替换 1.1.4，调整 FalkorDB 与 MCP 的合并镜像构建。 | MCP 1.1.5 已发布 | 依赖合并镜像的部署应核对所用镜像标签与持久化卷。 |

### 适用条件

**Letta Code**。Pi 流式适配器在第一次调用模型前估算上下文占用。达到阈值且已配置回调时，先压缩，再用压缩后的消息发起请求。遇到模型返回的窗口溢出时，最多再进行三次溢出压缩。普通压缩没有返回新系统提示时，适配器沿用原提示。启用 MemFS 的分支仍能在压缩后刷新与记忆相关的提示。

**OpenViking**。服务端用调用方的会话上下文读取归档、尚未归档的尾部消息和工具输出，支持搜索、按位置读取和概览。Gateway 只在允许工具且会话捕获开启时提供该工具。省略会话 ID 时默认查询当前对话的已保存会话。尚无已保存会话时直接返回提示，窗口裁掉的消息若尚未保存，也有单独提示。历史工具预算按当前窗口计算，阈值为上下文窗口的 20% 与 8,000 token 中较大者。

**claude-mem**。从已剥离的 v16.1.5 标签看，OpenRouter 返回 2xx 时，响应体内 400–599 的数字错误码参与分类。429 进入限流路径，5xx 进入短暂上游故障路径。已知的上游输出解析失败保留原 HTTP 状态，避免把可能已计费的请求当临时故障重发。短暂故障超过内部重试且观察器暂停时，批次保留，存在可用后备提供商时可继续处理。v16.1.3 [发行说明](https://github.com/thedotmack/claude-mem/releases/tag/v16.1.3)登记了首发修复，v16.1.5 为本轮核对实现的版本。

**Hindsight**。配置先应用环境和文件层，再按路径及 bank 覆盖值解析。只有最终使用默认 Hindsight Cloud 地址且没有 token 时，才触发这条关闭规则。自托管地址不受该地址判断影响。Stop hook 在解析 bank 后读取关闭状态并提前退出，不进入远端写入路径。

**Graphiti MCP**。1.1.5 的发行说明说上一版发行作业未生成 Docker 镜像。新标签的 Dockerfile 在 FalkorDB 基础镜像中使用 uv 安装 CPython 3.13，无需 apt，启动脚本先等待 FalkorDB 就绪，再启动 MCP 服务。源码的默认构建参数与发布作业可传入的值不同。本轮核对了发行记录和标签源码，注册表镜像实际 digest 待核实。

## Star 变化

表中相邻观测相隔约 23.80 小时。7 日和 30 日采用目标时刻前后 6 小时内最接近的实际观测。

| 项目 | 前次 UTC | 本次 UTC | 本次 Stars | 相邻净变化 | 7 日净变化 | 30 日净变化 |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| letta-ai/letta-code | 11-24 16:11:52 | 11-25 15:59:45 | 3915 | +9 | +48 | +204 |
| volcengine/OpenViking | 11-24 16:12:14 | 11-25 16:00:07 | 42764 | +73 | +346 | +1887 |
| thedotmack/claude-mem | 11-24 16:11:43 | 11-25 15:59:37 | 119703 | +228 | +1533 | +16378 |
| vectorize-io/hindsight | 11-24 16:11:55 | 11-25 15:59:48 | 63338 | +238 | +1556 | +9292 |
| getzep/graphiti | 11-24 16:11:37 | 11-25 15:59:31 | 33085 | +28 | +161 | +843 |

## 新候选线索对比

以下为 GitHub 搜索中的项目描述，三条线索均待核对实现。

| 线索 | 描述中的记忆机制 | 待核实 |
| --- | --- | --- |
| [ClickHouse/loom](https://github.com/ClickHouse/loom) | 将记忆绑定到代码文件和符号，自托管于 ClickHouse。 | 代码变更后如何更新引用和索引。 |
| [omkarjainak/recall](https://github.com/omkarjainak/recall) | 使用 Relate 嵌入式图存储记录来源、替代与冲突。 | 冲突检测如何影响实际检索和旧记录。 |
| [CiMind](https://github.com/TinkeringDao/CiMind) | 声称提供本地、可审计的情景记忆与策略门控。 | 宿主集成、持久化层和门控实施位置。 |

## 方法与覆盖边界

24 个登记项目完成元数据、HEAD 和增量 Release 采集。两个无 Star 门槛的查询各取首页，共返回 40 条。六个 HEAD 区间中选读五项实现。OpenViking 对比列表达到 300 文件上限。候选池未新增准入。本轮依据公开发布和静态代码，未运行上游程序或评测。

<details markdown="1"><summary>证据与时间</summary>

本轮 `20261125T155843Z-local`，批次观察时刻 2026-11-25T16:00:41.981Z。


- Letta Code，变更或发行 UTC 2026-11-24T23:52:32Z，固定源码观测截至 2026-11-25T16:02:25.238Z。[请求前检查](https://github.com/letta-ai/letta-code/blob/c67a0d59263262a947b3dce3420b2c35b46bd829/src/backend/dev/pi-stream-adapter.ts#L385-L413) · [溢出恢复](https://github.com/letta-ai/letta-code/blob/c67a0d59263262a947b3dce3420b2c35b46bd829/src/backend/dev/pi-stream-adapter.ts#L620-L666) · [压缩后系统提示](https://github.com/letta-ai/letta-code/blob/c67a0d59263262a947b3dce3420b2c35b46bd829/src/backend/local/local-backend.ts#L606-L646)
- OpenViking，变更或发行 UTC 2026-11-25T12:44:58Z，固定源码观测截至 2026-11-25T16:04:58.019Z。[只读服务入口](https://github.com/volcengine/OpenViking/blob/af412110b367ec404560629dada718ba1172a1cf/openviking/server/routers/sessions.py#L356-L403) · [工具启用条件](https://github.com/volcengine/OpenViking/blob/af412110b367ec404560629dada718ba1172a1cf/openviking_gateway/tool_catalog.py#L70-L104) · [默认会话与窗口预算](https://github.com/volcengine/OpenViking/blob/af412110b367ec404560629dada718ba1172a1cf/openviking_gateway/tool_executor.py#L333-L385)
- claude-mem，变更或发行 UTC 2026-11-24T18:32:35Z，固定源码观测截至 2026-11-25T16:04:52.190Z。[响应体分类](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/OpenRouterProvider.ts#L185-L201) · [响应体调用入口](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/OpenRouterProvider.ts#L1252-L1264) · [暂停与队列处理](https://github.com/thedotmack/claude-mem/blob/11b47f9f4b8dc3614fab7452647f578886468849/src/services/worker/session/GeneratorRunner.ts#L322-L357)
- Hindsight，变更或发行 UTC 2026-11-25T10:27:39Z，固定源码观测截至 2026-11-25T16:06:05.027Z。[配置合并与关闭判定](https://github.com/vectorize-io/hindsight/blob/61c01ecbec8026858feac51caf5a818741cdbf42/hindsight-integrations/coding-agents/src/core/config.ts#L896-L932) · [Stop hook 写入门禁](https://github.com/vectorize-io/hindsight/blob/61c01ecbec8026858feac51caf5a818741cdbf42/hindsight-integrations/coding-agents/src/core/retain-hook.ts#L224-L235)
- Graphiti MCP，变更或发行 UTC 2026-11-24T17:09:14Z，固定源码观测截至 2026-11-25T16:04:50.288Z。[合并镜像构建](https://github.com/getzep/graphiti/blob/231ebdcf6409c7e9bcf57bea328108cd64297777/mcp_server/docker/Dockerfile#L5-L33) · [FalkorDB 启动顺序](https://github.com/getzep/graphiti/blob/231ebdcf6409c7e9bcf57bea328108cd64297777/mcp_server/docker/Dockerfile#L119-L152) · [镜像数据卷](https://github.com/getzep/graphiti/blob/231ebdcf6409c7e9bcf57bea328108cd64297777/mcp_server/docker/README-falkordb-combined.md#L97-L101)

| 项目 | 7 日基线 UTC | 实际小时 | 30 日基线 UTC | 实际小时 |
| --- | --- | ---: | --- | ---: |
| Letta Code | 2026-11-18T16:01:29.027Z | 167.97 | 2026-10-26T16:11:54.290Z | 719.80 |
| OpenViking | 2026-11-18T16:02:38.434Z | 167.96 | 2026-10-26T16:13:36.726Z | 719.78 |
| claude-mem | 2026-11-18T16:01:07.328Z | 167.97 | 2026-10-26T16:11:20.123Z | 719.80 |
| Hindsight | 2026-11-18T16:01:45.182Z | 167.97 | 2026-10-26T16:12:24.140Z | 719.79 |
| Graphiti MCP | 2026-11-18T16:00:49.711Z | 167.98 | 2026-10-26T16:10:20.016Z | 719.82 |

</details>
