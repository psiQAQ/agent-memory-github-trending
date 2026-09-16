# 初步方案与决策入口

状态：待确认；调研日期：2026-09-16。本文记录初步设计，不代表采集器、CI、历史数据或定时更新已经验收。

## 定位

建立“Agent Memory 技术观察站”，而不是复制一个按总 Star 排序的 Awesome List。持续回答：出现了哪些新实现、已有项目改了什么、哪些变化涉及新的记忆机制、哪些项目值得进一步验证。关注热度、工程变化和研究证据分别呈现。

默认由 ChatGPT Scheduled 每 12 小时启动一轮，GitHub 是跨会话状态和可审计输出的持久存储。GPT 负责发现、阅读、归类、解释和发布；确定性脚本负责数据校验、增量计算、去重与渲染。脚本将在方案确认后实现并测试，不能假设定时运行一定具有终端；无终端时必须采用经批准的等价校验路径或停止发布，不得跳过校验。

## 同类项目的组织方式

| 参考仓库 | 已观察到的结构/机制 | 本项目借鉴与取舍 |
| --- | --- | --- |
| [best-of-lists/best-of](https://github.com/best-of-lists/best-of) 与 [best-of-generator](https://github.com/best-of-lists/best-of-generator) | projects.yaml、config、history、latest-changes.md；生成器从结构化项目表产生 Markdown 和历史变化 | 采用单一数据源与生成视图分离；不照搬其经验性 project-quality 分数 |
| [trackawesomelist](https://github.com/trackawesomelist/trackawesomelist) 与 [source](https://github.com/trackawesomelist/trackawesomelist-source) | 内容仓库与生成器分离；配置源、parser、templates；按来源和时间生成内容，网站提供日/周更新 | 采用来源登记、增量变化、时间分区；初期保留单仓库，不先搭网站或数据库服务 |
| [bonfy/github-trending](https://github.com/bonfy/github-trending) | 日期 Markdown、历年目录、采集脚本与 workflow | 保留可回溯快照；避免在根目录堆每日文件或全文复制上游 |
| [vitalets/github-trending-repos](https://github.com/vitalets/github-trending-repos) | 每种语言对应一个 Issue，定时脚本用评论发送每日/每周变化 | 借鉴“通知与数据分离”；默认不建立不断增长的单一订阅 Issue |
| [Agent-Memory-Paper-List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List) | 按记忆形式、功能、动态过程组织文献 | 用作研究分类和新代码发现源，不把文献清单当作实时热度榜 |

以上是组织方式参考，不构成对这些仓库运行可靠性或项目质量的评测。综述的形式/功能/动态过程分类也不是本仓库唯一或强制的标准。

## 文档与数据组织

已建立的草案入口：README、AGENTS、本文、methodology、maintenance、config/tracker.json、data/projects.json、state/status.json。

确认后按实际需要增加以下产物，不提前创建无内容目录：

```text
README.md                         # 当前摘要、最近成功时间、覆盖率、入口
AGENTS.md                         # 稳定执行边界和阅读顺序
config/tracker.json               # 已批准的范围、阈值、频率、发布策略
config/queries.json               # 有版本的搜索查询与关键词组
config/schema.json                # 数据校验契约
state/status.json                 # 当前健康状态与已验证数据提交
state/checkpoints.json            # 每个来源的游标、重试与候选队列
 data/projects.json               # 项目登记表；含候选/正式/背景/归档状态
 data/snapshots/YYYY/MM/*.json     # 每轮数值快照，保留实际观测时间
 data/events/YYYY-MM.jsonl        # 已核实实质变化与证据
projects/<slug>.md                # 当前实现、适用场景、限制和证据
reports/latest.md                # 最新有实质内容的简报；覆盖写入
reports/weekly/YYYY-Www.md         # 周度跨项目趋势，完成后固定
scripts/validate.py               # 确定性校验，待实现
scripts/render.py                 # 由数据生成当前视图，待实现
 tests/                          # 边界与回归测试，待实现
```

目录示意中 data 与 tests 的前导空格仅为排版；实际路径无前导空格。仅在确认后、确有必要时添加 `.github/workflows/validate.yml`；不默认部署第二个采集调度器。

README 不超过 250 行，项目卡片以当前状态为主。原始快照保留；月度分区减少单文件增长，周报不重复堆砌每次执行过程。Git 历史本身仍会增长，分目录并不消除存储增长；确需压缩/迁移时另行设计可恢复归档，不擅自清理。

## 建议的运行策略

- 初始正式跟踪目标为 20 个，正式跟踪与观察池总上限暂设 50 个；现有 seed 只是候选，不是已完成基线。
- 重点项目每 12 小时检查；观察池最长 72 小时轮询一遍，每轮新候选深读不超过 10 个，技术差异深读不超过 5 个。超出预算进入持久队列并报告覆盖率，不能声称已检查所有项目。
- 技术变化简报仅在有重要变化时更新；每轮仍可保存计数快照和检查状态。
- 每个已结束的 ISO 周在下一次成功检查中生成一次周报；不增加独立任务，不承诺精确的单独周报时点。
- 普通数据与报告默认直推 main；代码、流程和统计口径变更单独提议，经明确批准后实施。授权、费用、写入范围不会因“全权维护”而自行扩大。
- 初期不要求本地常驻机器，不配置付费 API。ChatGPT 自身的任务/使用额度限制仍适用；未测量前不估算额度节省。

## 待确认的五项选择

| 编号 | 问题 | 建议默认 |
| --- | --- | --- |
| A | 研究范围：只有可用工具，还是工具 + 论文代码 + 评测？ | 工具 + 论文代码 + 评测；无代码论文仅作为背景线索；纯 SaaS 不进主榜 |
| B | 对 Coding Agent 记忆插件重点倾斜，还是各类 Agent Memory 均衡？ | 各类均衡，额外提供 Coding Agent / 本地部署标签与视图 |
| C | 正常数据和报告直接更新 main，还是每次创建 PR？ | 已批准规则内直推 main；规则/脚本变更单独提议；不要求每轮人工审批 |
| D | 每 12 小时从启用起滚动，还是固定北京时间 09:00 / 21:00？ | 从启用起每 12 小时；UTC 存储，中文报告按 Asia/Shanghai 展示 |
| E | 每轮都通知，还是只通知重要变化/故障并给周报？ | 重要变化、需处理故障、周报和首轮定时验收；普通计数变化不打扰 |

所有建议均未视为用户批准。初步调度任务已创建后暂停；不能仅在 UI 点恢复就绕过配置与实现就绪门禁。

## 启用前验收

1. 将用户明确选择写入配置与本页决策结果，不依赖聊天记忆。
2. 实现并运行校验/渲染与数据契约测试；基线数据必须实采，7/30 日无基线时保持 null。
3. 在当前交互式会话完成一次真实采集、提交与回读；同一批输入重跑不得重复事件或重复技术简报。
4. 验证失败/缺失数据、分页不全、低基数增长、重命名、并发冲突、恶意 README、无变化与跨周场景。
5. 经确认启用后，首个真实定时运行须证明 GitHub 读写与必要校验路径可用，再标记定时端到端通过。创建任务本身不是此项证据。

## 平台能力来源与限制

[Scheduled tasks in ChatGPT](https://help.openai.com/en/articles/10291617-tasks-in-chatgpt) 当前说明任务可以使用受支持的 GitHub 等应用，但改变外部数据可能需要审批；项目内任务不能依赖上传文件。因此仓库必须是显式读取的状态源。

[Connecting GitHub to ChatGPT](https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt) 的 FAQ 仍将常规 GitHub app 描述为只读。这与当前会话暴露的写入工具并不完全一致。因此本项目以本账号的实际操作验证为准：初始化 README 已成功写入；这仅证明当前会话可写，尚不证明未来定时执行稳定可写。没有改动用户原有权限设置。

若正式定时运行缺少写入/校验能力，停止发布并报告阻碍。可以另行选择 GitHub Actions 确定性采集 + ChatGPT 分析的双层方案，但不能静默切换执行平台或增加付费 API。
