---
title: LLM Wiki — 维护纲要
date: 2026-04-27
description: 本文件是整个 LLM Wiki 的宪法。它告诉 LLM 知识库的结构、约定和操作流程。用户和 LLM 共同演化此文件。
---

# LLM Wiki — 维护纲要

> **Vault 根目录**：`D:\Obsidian Vault\`

---

## 语言设定与核心角色

- **语言**：无论输入何种语言，始终使用**简体中文**思考、回复、编写 wiki。
- **角色**：你正在维护一个 **LLM Wiki**（基于 [Karpathy 的规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)）。你的任务是将碎片化信息编译成结构化、高度互联的 Obsidian 知识库。
- **协作模式**：用户负责来源筛选与方向引导；你负责所有簿记——摘要、交叉引用、归档、维护。

---

## 架构概览

```
├── raw\                        # 原始资料（只读，绝对不修改）
│   ├── 01-articles\            # 网页剪藏的 Markdown 文章
│   ├── 02-papers\              # 论文和 PDF 文献
│   ├── 03-transcripts\         # 视频/播客转录文案
│   ├── 04-notes\               # 用户手写笔记
│   └── 09-archive\             # 已处理文件的归档（禁止读取）
│
├── wiki\                       # LLM 维护的知识库（你完全拥有此层）
│   ├── concepts\               # 概念页（框架、方法论、理论、算法）
│   │   ├── programming\        # C++、Python 等编程语言概念
│   │   ├── theory\             # 数学、控制理论
│   │   ├── embedded\           # 嵌入式开发（STM32、ROS）
│   │   └── digital\            # 数字电路与系统
│   ├── entities\               # 实体页（人物、公司、工具、产品、事件）
│   ├── sources\                # 资料摘要页（从 raw/ 提炼）
│   ├── comparisons\            # 对比分析页
│   ├── syntheses\              # 综合论述页（查询的高价值回答）
│   ├── index.md                # 全局目录（每次 ingest 后必须更新）
│   ├── log.md                  # 操作日志（只追加，不修改历史）
│   └── synthesis.md            # 整体综合论述（持续演化的主论述）
│
├── assets\                     # 图片、图表、媒体文件
├── Excalidraw\                 # 画图文件
├── templates\                  # Obsidian 笔记模板
├── CLAUDE.md                   # 本文件：维护纲要
└── .claude\                    # AI 技能定义（Skills）
    └── skills\
        ├── wiki-ingest\        # 资料摄入技能
        ├── wiki-query\         # 知识库查询技能
        ├── wiki-lint\          # 健康检查技能
        ├── obsidian-cli\       # Obsidian CLI 操作
        └── obsidian-markdown\  # Obsidian Markdown 规范
```

**三层架构**：
1. **`raw/`（不可变层）**：用户精选的原始资料。LLM **只读**，绝不修改或删除。这是唯一的事实真相来源。
2. **`wiki/`（编译层）**：LLM 生成并维护的结构化知识库。你完全拥有此层。
3. **`CLAUDE.md`（纲要层）**：本文件。随协作深化而不断演化。

---

## 文件权限边界（不可逾越）

| 目录 | 权限 | 说明 |
|:---|:---|:---|
| `raw\01-articles\` | **只读** | 网页剪藏文章 |
| `raw\02-papers\` | **只读** | 论文和文献 |
| `raw\03-transcripts\` | **只读** | 转录文案 |
| `raw\04-notes\` | **只读** | 手写笔记 |
| `raw\09-archive\` | **禁止读取** | 已归档文件 |
| `wiki\` | **完全读写** | 你的工作区 |
| `CLAUDE.md` | **读写（谨慎）** | 和用户共同演化 |

---

## Wiki 内容分区说明

### `wiki/concepts/` 子目录规范

| 子目录 | 存放内容 |
|:---|:---|
| `wiki\concepts\programming\` | C++、Python、算法、设计模式等编程概念 |
| `wiki\concepts\theory\` | 数学（拉普拉斯变换等）、控制理论 |
| `wiki\concepts\embedded\` | STM32、ROS、嵌入式开发概念 |
| `wiki\concepts\digital\` | 数字电路、逻辑门、组合逻辑、时序逻辑 |

新 ingest 的资料若涉及上述领域，对应概念页更新到相应子目录。  
跨领域或通用概念直接放 `wiki\concepts\` 根目录。

---

## Wiki 页面规范

### 通用要求

- 每个 wiki 文件必须有 **YAML frontmatter**（至少含 `title`、`type`、`tags`、`last_updated`）
- 用 `[[wikilink]]` 链接到其他 wiki 页面（Obsidian 自动跟踪重命名）
- 用 `[text](url)` 链接到外部资源
- 用 `> [!type]` callout 标注重要信息（见标记系统）
- 每个页面必须含 `## 关联连接` 节，使用 `[[页面名]]` 链接相关内容——**绝不能产生孤岛页面**

### YAML Frontmatter 规范

```yaml
---
title: "页面标题"
type: entity | concept | source | synthesis | comparison
tags:
  - 主分类标签
  - 领域标签
aliases:
  - 英文名或别名
sources:
  - raw/01-articles/xxx.md
last_updated: YYYY-MM-DD
---
```

### 资料摘要页 `wiki/sources/`

文件命名：`摘要-{slug}.md`（kebab-case slug）

```markdown
---
title: "摘要-{slug}"
type: source
tags:
  - source
  - <主题领域>
sources:
  - raw/01-articles/xxx.md
last_updated: YYYY-MM-DD
---

> **一句话摘要**：<用一句话概括核心内容>

## 核心观点

- <要点 1>
- <要点 2>
- <要点 3>

## 对现有知识的贡献

- <新信息>
- <与现有认知的关系>

## 关联连接

- [[EntityName]] — <关联说明>
- [[ConceptName]] — <关联说明>
```

### 实体页 `wiki/entities/`

文件命名：`EntityName.md`（TitleCase）

```markdown
---
title: "EntityName"
type: entity
tags:
  - entity
  - <分类>
aliases:
  - <别名>
sources:
  - <来源路径>
last_updated: YYYY-MM-DD
---

> **一句话描述**：<定义>

## 关键属性

| 属性 | 值 |
|:---|:---|
| 类型 | 人物 / 组织 / 工具 / 产品 / 事件 |

## 相关知识

<从资料中提炼的核心认知>

## 关联连接

- [[摘要-source-slug]] — 来源
- [[RelatedConcept]] — <关联说明>
```

### 概念页 `wiki/concepts/`

文件命名：`ConceptName.md`（TitleCase 或中文）

```markdown
---
title: "ConceptName"
type: concept
tags:
  - concept
  - <领域>
aliases:
  - <别名>
sources:
  - <来源路径>
last_updated: YYYY-MM-DD
---

> **一句话定义**：<定义>

## 详细说明

<深入解释>

## 与其他概念的关系

- [[RelatedConcept]] — <关系描述>

## 实例 / 应用

<具体例子>

## 关联连接

- [[摘要-source-slug]] — 来源
```

---

## index.md 规范

`wiki/index.md` 是整个知识库的导航中枢。格式：

```markdown
# Wiki 索引

> 本索引是 LLM Wiki 的内容目录。每次资料摄入后自动更新。查询时首先读此文件。

---

## 概念
### 编程
- [[concepts/programming/xxx]] — 一句话定义

### 理论与数学
- [[concepts/theory/xxx]] — 一句话定义

### 嵌入式开发
- [[concepts/embedded/xxx]] — 一句话定义

### 数字电路
- [[concepts/digital/xxx]] — 一句话定义

## 实体
- [[entities/EntityName]] — 一句话描述

## 资料
- [[sources/摘要-source-slug]] — 该资料的核心主旨

## 对比
- [[comparisons/A-vs-B]] — 对比说明

## 综合
- [[syntheses/slug]] — 该页面回答的核心问题
```

**每次 ingest 后必须更新**。查询前先读 index.md。

---

## log.md 规范

`wiki/log.md` 是追加式操作日志（Append-only）。每条格式：

```markdown
## [YYYY-MM-DD] <操作类型> | <操作简述>
- **变更**: 新增 [[PageName]]；更新 [[index.md]]
- **冲突**: 无（或：冲突 [[ConflictingPage]]，已标注）
```

操作类型：`ingest` | `query` | `lint` | `sync` | `init`

---

## 操作流程（技能快捷指令）

| 指令 | 触发技能 | 说明 |
|:---|:---|:---|
| `/ingest` 或 `/ingest <路径>` | `wiki-ingest` | 摄入 raw/ 中的新资料 |
| `/query <问题>` | `wiki-query` | 查询 wiki 并综合回答 |
| `/lint` | `wiki-lint` | 知识库健康检查 |

---

## 标记系统

| 场景 | 标记方式 |
|:---|:---|
| 新发现（相比旧认识） | `> [!info] 新发现` |
| 与现有结论矛盾 | `> [!warning] 与 [[xxx]] 矛盾` |
| 待验证 / 不确定 | `> [!question] 待验证` |
| 知识空白 | `> [!todo] 待补充：<描述>` |
| 重要结论 | `> [!important]` |
| 已解决的矛盾 | `> [!success] 矛盾已解决` |

---

## 命名约定

| 页面类型 | 命名规则 | 示例 |
|:---|:---|:---|
| 资料摘要 | `摘要-{slug}.md`（kebab-case） | `摘要-attention-is-all-you-need.md` |
| 实体 | `{EntityName}.md`（TitleCase） | `AndrejKarpathy.md` |
| 概念 | `{概念名}.md`（中文或 TitleCase） | `Transformer架构.md` |
| 对比 | `{A}-vs-{B}.md` | `RAG-vs-LLM-Wiki.md` |
| 综合 | `{主题描述}.md` | `LLM-Wiki模式综合.md` |

- **优先中文命名**（与 Obsidian 阅读体验一致）
- 英文名 / 缩写作为 `aliases` 写入 frontmatter

---

## 矛盾处理原则

如果新摄入的知识与旧知识冲突：
1. **暂停** ingest 流程
2. **报告**：告诉用户冲突在哪个页面、具体冲突点
3. **询问**：A) 保留双方并标注冲突 / B) 用新知识覆盖 / C) 放弃本次 ingest
4. **执行**：按用户选择，在页面中建 `## 知识冲突` 区块保留两种说法

> **绝对不要静默覆盖**。

---

## 与 Obsidian 的配合

- **浏览**：用 Obsidian Graph View 查看 wiki 图谱（哪些页面是枢纽，哪些是孤岛）
- **操作**：用 Antigravity / Claude Code 维护 wiki，在 Obsidian 中实时预览
- **剪藏**：用 [Obsidian Web Clipper](https://obsidian.md/clipper) 将网页转为 Markdown 存入 `raw/01-articles/`
- **图片**：附件目录设为 `assets/`，使用 `![[文件名.png]]` 引用
- **Dataview**：用 frontmatter 中的 `type` 和 `tags` 字段生成动态视图
- **Obsidian CLI**：通过 `obsidian` 命令行工具直接操作 vault（见 `obsidian-cli` skill）

---

## 本文件演化说明

本文件是**活文件**。随协作演化随时更新。每次重大修改在 `wiki/log.md` 追加 `sync` 类型记录。
