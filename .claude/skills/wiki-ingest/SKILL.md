---
name: wiki-ingest
description: 将 raw/ 下的原始资料编译到 wiki/ 中。支持 /ingest（扫描所有未归档文件）或 /ingest <路径>（处理指定文件）。当用户提到"摄入"、"导入"、"收录"某资料，或要求将文章加入知识库时，也应触发此技能。绝对忽略 raw/09-archive/ 目录。
user-invocable: true
---

# wiki-ingest — 资料摄入技能

> **Vault 根目录**：`D:\Obsidian Vault\`
> **Schema**：先读 `D:\Obsidian Vault\CLAUDE.md` 了解完整约定

---

## 目录路径速查

| 作用 | 路径 |
|:---|:---|
| 网页剪藏文章 | `D:\Obsidian Vault\raw\01-articles\` |
| 论文/PDF | `D:\Obsidian Vault\raw\02-papers\` |
| 视频/播客转录 | `D:\Obsidian Vault\raw\03-transcripts\` |
| 手写笔记 | `D:\Obsidian Vault\raw\04-notes\` |
| 已归档（禁止读取） | `D:\Obsidian Vault\raw\09-archive\` |
| 资料摘要 | `D:\Obsidian Vault\wiki\sources\` |
| 实体页 | `D:\Obsidian Vault\wiki\entities\` |
| 概念页（编程） | `D:\Obsidian Vault\wiki\concepts\programming\` |
| 概念页（理论） | `D:\Obsidian Vault\wiki\concepts\theory\` |
| 概念页（嵌入式） | `D:\Obsidian Vault\wiki\concepts\embedded\` |
| 概念页（数字电路） | `D:\Obsidian Vault\wiki\concepts\digital\` |
| 全局索引 | `D:\Obsidian Vault\wiki\index.md` |
| 操作日志 | `D:\Obsidian Vault\wiki\log.md` |

---

## 触发逻辑

1. **`/ingest`**：扫描 `raw/` 所有子目录（排除 `09-archive/`），列出待处理文件，逐一处理。
2. **`/ingest <路径>`**：仅处理指定文件。
3. **隐式触发**：用户说"把这个摄入知识库"、"导入这篇文章"、"收录这个资料"时自动执行。

---

## 编译流水线

### 步骤 1：使用 Obsidian CLI 读取源文件

```bash
# Vault 名为 "Obsidian Vault"
obsidian vault="Obsidian Vault" read path="raw/01-articles/文件名.md"
```

若 CLI 不可用，直接用文件读取工具。

- `.md` 文件：完整读取文本
- `.pdf` 文件：尝试提取文本；无法提取时记录文件元信息

### 步骤 2：与用户讨论（不得跳过）

读取完成后，提炼 3-5 条关键收获，向用户确认：
- 哪些点最重要？侧重什么方向？
- 有没有特别想深挖的角度？
- 与现有认知有无冲突？

> **禁止跳过此步骤**。

### 步骤 3：提炼核心内容

从源文件中提取：
- **核心主旨**：1-2 句话概括
- **实体**：人物、公司、工具、产品 → 将写入 `wiki/entities/`
- **概念**：框架、方法论、理论 → 将写入 `wiki/concepts/<领域>/`

判断概念归属：
- 编程相关 → `wiki/concepts/programming/`
- 数学/控制理论 → `wiki/concepts/theory/`
- 嵌入式/硬件 → `wiki/concepts/embedded/`
- 数字电路 → `wiki/concepts/digital/`
- 其他/跨领域 → `wiki/concepts/`

非中文内容翻译成中文再处理。

### 步骤 4：创建资料摘要页

```bash
obsidian vault="Obsidian Vault" create \
  path="wiki/sources/摘要-{slug}.md" \
  content="..." silent
```

文件内容（参见 CLAUDE.md 资料摘要页规范）：

```markdown
---
title: "摘要-{slug}"
type: source
tags:
  - source
  - <主题领域>
sources:
  - raw/01-articles/<文件名>.md
last_updated: <今日日期>
---

> **一句话摘要**：<核心内容>

## 核心观点

- <要点 1>
- <要点 2>
- <要点 3>

## 对现有知识的贡献

- <新信息、矛盾、补充>

## 关联连接

- [[entities/EntityName]] — <关联说明>
- [[concepts/<领域>/ConceptName]] — <关联说明>
```

### 步骤 5：知识网络化（实体 / 概念页面）

对每个提取的实体和概念：

1. **页面不存在** → 按 CLAUDE.md 规范创建
2. **页面已存在** → 读取后增量合并
3. **发现冲突** → **立即暂停**，向用户报告，询问处理方式

```bash
# 创建新概念页
obsidian vault="Obsidian Vault" create \
  path="wiki/concepts/<领域>/ConceptName.md" \
  content="..." silent

# 向已有页面追加内容
obsidian vault="Obsidian Vault" append \
  path="wiki/concepts/<领域>/ConceptName.md" \
  content="\n## 补充信息（来自 [[sources/摘要-{slug}]]）\n..."
```

所有页面必须包含 `## 关联连接` 区域，使用 `[[双链]]`，**不能产生孤岛页面**。

### 步骤 6：更新 synthesis.md

如果新资料影响整体理解框架：

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/synthesis.md" \
  content="\n> [!info] 新发现（来自 [[sources/摘要-{slug}]]）\n> <影响说明>"
```

### 步骤 7：更新全局索引

读取 `wiki/index.md`，在对应分类下添加新页面条目：

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
```

然后追加：
- Concepts: `- [[concepts/<领域>/ConceptName]] — 一句话定义`
- Entities: `- [[entities/EntityName]] — 一句话描述`
- Sources: `- [[sources/摘要-{slug}]] — 该资料的核心主旨`

### 步骤 8：追加操作日志（Append-only）

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [<今日日期>] ingest | <资料标题>\n- **变更**: 新增 [[sources/摘要-{slug}]]，更新 [[wiki/index.md]]\n- **冲突**: 无"
```

### 步骤 9：归档源文件

确认以上全部完成后，将源文件移动到 `raw/09-archive/`。**只移动文件，绝不修改文件内容。**

---

## 冲突处理流程

1. **暂停**：停止当前 ingest 流程
2. **报告**：说明冲突所在页面和具体冲突点
3. **询问**：A) 保留双方，建 `## 知识冲突` 区块 / B) 覆盖 / C) 放弃
4. **执行**：按用户选择，在 log.md 记录决策

---

## 核心原则

- **一份资料可能触及 10-15 个 wiki 页面**
- **标注矛盾比掩盖矛盾更有价值**
- **禁止修改 raw/ 下任何文件**
- **禁止读取 raw/09-archive/**

---

## 关联技能

- Schema：`D:\Obsidian Vault\CLAUDE.md`
- Obsidian 操作：`obsidian-cli` skill
- Markdown 规范：`obsidian-markdown` skill
