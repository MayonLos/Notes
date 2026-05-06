# LLM Wiki — Personal Knowledge Base

基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的个人知识库，使用 Claude Code 维护。

---

## 这是什么

大多数人用 LLM 处理文档的方式类似于 RAG：上传文件，查询时检索片段，生成答案。这种方式有一个根本缺陷——**知识不会积累**。每次查询，LLM 都在从头重新发现知识。

这个知识库采用不同的范式：LLM **增量构建并维护一个持久化的 wiki**。当你添加新资料时，LLM 不只是索引它，而是读取、提炼，并将其整合到现有知识网络中——更新实体页面、修订概念摘要、标注与旧结论的矛盾、强化整体综合论述。

**关键差异**：wiki 是持久的、复利式的产出物。交叉引用已经建立好了。矛盾已经被标注了。综合论述已经反映了你读过的所有内容。每添加一份资料，知识库就更丰富一点。

你的工作：筛选资料、设定方向、提出好问题。
LLM 的工作：摘要、交叉引用、归档、维护——所有你不想做的簿记。

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
  concepts/        概念页（扁平，#tags 区分领域）
  entities/        实体页（人物、工具、公司）
  sources/         资料摘要页
  comparisons/     对比分析页
  syntheses/       综合论述页（高价值查询的沉淀）
  index.md         全局目录（导航中枢）
  log.md           追加式操作日志
  synthesis.md     整体演化主论述

CLAUDE.md       ← Schema 层（你和 LLM 共同演化）
```

---

## 快速上手

在 Claude Code 中打开此 Vault 目录，然后使用以下指令：

| 操作 | 指令 | 说明 |
|:-----|:-----|:-----|
| 摄入新资料 | `/ingest` | 扫描并处理所有 raw/ 中的待处理文件 |
| 摄入指定文件 | `/ingest raw/01-articles/filename.md` | 处理单个文件 |
| 查询知识库 | `/query 什么是 RAII？` | 检索并综合回答 |
| 健康检查 | `/lint` | 检测死链、孤儿页、知识冲突等 |

**工作流**：
1. 用 [Obsidian Web Clipper](https://obsidian.md/clipper) 将网页保存到 `raw/01-articles/`
2. 在 Claude Code 中运行 `/ingest`
3. 用 Obsidian 的 Graph View 浏览知识图谱
4. 用 `/query` 提问，好的回答自动沉淀为 `wiki/syntheses/` 页面
5. 每隔几次摄入运行 `/lint` 保持知识库健康

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
| [Claude Code](https://claude.ai/code) | Wiki 维护者（运行 `/ingest`、`/query`、`/lint`）|
| [Obsidian CLI](https://github.com/mscharley/obsidian-cli) | Claude Code 与 Vault 的交互桥梁 |
| [Obsidian Web Clipper](https://obsidian.md/clipper) | 浏览器扩展，网页转 Markdown 存入 raw/ |
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview)（可选）| 用 frontmatter tags 生成动态表格和视图 |
| [qmd](https://github.com/tobi/qmd)（可选）| Wiki 本地搜索引擎，BM25/向量混合检索，知识库扩大后使用 |

---

## 致谢

Pattern by [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — *"The wiki is a persistent, compounding artifact."*
