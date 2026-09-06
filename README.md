# LLM Wiki — Personal Knowledge Base

基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的个人知识库，使用 Claude Code 维护。

---

## 这是什么

大多数人用 LLM 处理文档的方式类似于 RAG：上传文件，查询时检索片段，生成答案。这种方式有一个根本缺陷——**知识不会积累**。每次查询，LLM 都在从头重新发现知识。

这个知识库采用不同的范式：LLM **增量构建并维护一个持久化的 wiki**。当你添加新资料时，LLM 不只是索引它，而是读取、提炼，并将其整合到现有知识网络中——更新实体页面、修订概念摘要、标注与旧结论的矛盾、强化整体综合论述。

**关键差异**：wiki 是持久的、复利式的产出物。交叉引用已经建立好了。矛盾已经被标注了。综合论述已经反映了你读过的所有内容。每添加一份资料，知识库就更丰富一点。

你的工作：筛选资料、设定方向、提出好问题。
LLM 的工作：摘要、交叉引用、维护——所有你不想做的簿记。

---

## 架构

```
raw/            ← 不可变资料层（只读）
  01-articles/     网页剪藏（Obsidian Web Clipper）
  02-papers/       论文、PDF
  03-transcripts/  视频/播客转录
  04-notes/        手写笔记
  05-wiki-export/  历史 wiki 内容（待重摄入）
  09-archive/      已处理文件（归档）

wiki/           ← 编译知识层（LLM 完全拥有）
  concepts/        概念页（按学科分子目录，#tags 区分领域）
  entities/        实体页（人物、工具、公司）
  sources/         资料摘要页
  comparisons/     对比分析页
  syntheses/       综合论述页（经明确要求保存的高价值查询沉淀）
  index.md         全局目录（导航中枢）
  log.md           追加式操作日志
  synthesis.md     整体演化主论述

CLAUDE.md       ← Schema 层（你和 LLM 共同演化）
```

---

## 文档导航

- [[wiki/index|Wiki 索引]] — 知识页面、资料摘要与综合论述的入口
- [[wiki/synthesis|整体综合论述]] — 知识库的跨领域演化总结
- [[wiki/log|操作日志]] — Wiki 维护操作的追加式记录
- [[TODO|学习路线 & 待办]] — 学习主题与待办事项
- [[CLAUDE|Schema 与维护约定]] — 页面规范、目录约定与操作规则

---

## 快速上手

在 Claude Code 中打开此 Vault 目录，然后使用以下指令：

| 操作 | 指令 | 说明 |
|:-----|:-----|:-----|
| 记笔记 | `/note 二阶系统的超调量怎么来的` | 把刚学会的内容写成/补进笔记页 |
| 摄入资料 | `/note raw/01-articles/filename.md` | 把一份 raw 资料编译进 wiki |
| 查笔记 | `/query 什么是 RAII？` | 只读检索并给出带出处的回答 |
| 复习 | `/review` | 看板：该复习什么、缺什么、TODO 到哪了 |
| 自测 | `/review 锁存器和触发器` | 基于该页出题并批改 |
| 默写提纲 | `/review 锁存器和触发器 --提纲` | 把该章压成填空式背诵材料 |
| 体检 | `/lint` | 只读检测死链、孤儿页、结构问题，不自动修复 |

**学习闭环**：

1. **学** — 上课、看书、看视频，或直接在 Claude Code 里把某个知识点问明白
2. **记** — `/note <主题>` 落盘：查重 → 建页 → 双向连线 → 登记 `index.md` 与 `log.md` → 自动校验
3. **查** — 复习或做题时 `/query`，回答只来自笔记且给出页面锚点
4. **复习** — 每周 `/review` 看该复习哪几页、哪些前置概念还空着；`/review <页面>` 做自测
5. **体检** — 每隔几次记录跑 `/lint`，保持链接与索引干净

资料也可以走 [Obsidian Web Clipper](https://obsidian.md/clipper) 存进 `raw/01-articles/`，再用 `/note <路径>` 摄入；`raw/` 始终只读，不会被移动或删除。

> **不需要用 skill 的场景**：做题（「帮我画 Bode 图估相角裕度」）、纯答疑（「别翻笔记，用弹簧直觉讲讲欠阻尼」）——直接问就行。讲完觉得值得留下来，再说一句「记进笔记」走 `/note`。

### 知识库 Skills

职责互斥，**只有 `note` 会写文件**：

| Skill | 语义 |
|:------|:-----|
| `note` | 唯一写入口：写/更新 `wiki/` 页面，含 raw 资料摄入。冲突先问，绝不静默覆盖。|
| `query` | 只读检索 `wiki/`；索引优先、按需读片段；要落盘转交 `note`。|
| `review` | 只读复习：自测题、复习队列、知识缺口、TODO 进度；不写 Vault。|
| `lint` | 只读结构体检；只报告不修复。指向未建页面的链接算「待写」，不算错误。|

> **省 token 的做法**：`.claude/cache/vault-index/` 里有一份自动刷新的索引（页面摘要 + 小标题 + 链接图）。skill 先在索引里定位，再只读需要的几十行，而不是把整个 `wiki/` 读进上下文。删掉也没关系，下次运行会自动重建。

---

## 当前知识领域

通过 frontmatter tags 区分，可用 Obsidian Dataview 查询。**动态扩展**——摄入新领域资料时自动添加新 tag：

| Tag | 领域 |
|:----|:-----|
| `#cpp` | C++ 编程语言 |
| `#math` | 数学工具（Laplace 变换、算子等）|
| `#control` | 控制理论 |
| `#digital` | 数字电路与逻辑 |
| `#embedded` | 嵌入式开发（STM32、ROS）|
| `#ai` | 人工智能、机器学习、深度学习 |
| `#meta` | 方法论、工具、编程范式 |

---

## 工具链

| 工具 | 用途 |
|:-----|:-----|
| [Obsidian](https://obsidian.md) | Wiki 浏览器，Graph View 可视化知识图谱 |
| [Claude Code](https://claude.ai/code) | Wiki 工作流入口（运行 `/note`、`/query`、`/review`、`/lint`）|
| [Obsidian CLI](https://github.com/mscharley/obsidian-cli) | Claude Code 与 Vault 的交互桥梁 |
| [Obsidian Web Clipper](https://obsidian.md/clipper) | 浏览器扩展，网页转 Markdown 存入 raw/ |
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview)（可选）| 用 frontmatter tags 生成动态表格和视图 |
| [qmd](https://github.com/tobi/qmd)（可选）| Wiki 本地搜索引擎，BM25/向量混合检索，知识库扩大后使用 |

---

## 致谢

Pattern by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — *"The wiki is a persistent, compounding artifact."*
