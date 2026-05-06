# LLM Wiki — Schema

> **Vault 根目录**：`/home/mayon/Vaults/`

---

## 角色与语言

- **语言**：无论输入何种语言，始终使用**简体中文**思考、回复、编写 wiki。
- **角色**：你正在维护一个 **LLM Wiki**（基于 [Karpathy 的规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)）。你的任务是将碎片化信息编译成结构化、高度互联的 Obsidian 知识库。
- **协作模式**：用户负责来源筛选与方向引导；你负责所有簿记——摘要、交叉引用、归档、维护。

---

## 架构概览

三层结构：

```
raw/                    # 不可变资料层（只读）
  01-articles/          # 网页剪藏 Markdown
  02-papers/            # 论文、PDF
  03-transcripts/       # 视频/播客转录
  04-notes/             # 手写笔记
  05-wiki-export/       # 历史 wiki 内容（待重摄入）
  09-archive/           # 已处理文件（禁止读取）

wiki/                   # 编译知识层（LLM 完全拥有）
  concepts/             # 概念页（扁平——用 tags 区分领域）
  entities/             # 实体页（人物、工具、公司、产品、事件）
  sources/              # 资料摘要页（从 raw/ 提炼）
  comparisons/          # 对比分析页
  syntheses/            # 综合论述页（高价值查询沉淀）
  index.md              # 全局目录（查询首先读这里）
  log.md                # 追加式操作日志
  synthesis.md          # 整体演化主论述

CLAUDE.md               # 本文件：schema 与约定
.claude/skills/         # 技能定义
  ingest/               # 资料摄入
  query/                # 知识查询
  lint/                 # 健康检查
```

---

## 文件权限边界

| 路径 | 权限 | 说明 |
|:-----|:-----|:-----|
| `raw/01-articles/` | 只读 | 网页剪藏 |
| `raw/02-papers/` | 只读 | 论文 |
| `raw/03-transcripts/` | 只读 | 转录 |
| `raw/04-notes/` | 只读 | 手写笔记 |
| `raw/05-wiki-export/` | 只读 | 历史 wiki 内容 |
| `raw/09-archive/` | **禁止读取** | 已归档文件 |
| `wiki/` | 完全读写 | 你的工作区 |
| `CLAUDE.md` | 读写（谨慎） | 与用户共同演化 |

---

## Wiki 页面规范

### YAML Frontmatter

每个 wiki 文件必须包含：

```yaml
---
title: "页面标题"
type: entity | concept | source | synthesis | comparison
tags:
  - 主领域标签
  - 次领域标签
aliases:
  - 英文名或别名
sources:
  - raw/01-articles/filename.md
last_updated: YYYY-MM-DD
---
```

### Tags 体系（动态扩展）

现有 tags 不够用时，自行创建新 tag 并**追加到此列表**：

| Tag | 覆盖领域 |
|:----|:---------|
| `#cpp` | C++ 编程语言 |
| `#math` | 数学工具（Laplace、算子等）|
| `#control` | 控制理论 |
| `#digital` | 数字电路与逻辑 |
| `#embedded` | 嵌入式开发（STM32、ROS）|
| `#ai` | 人工智能、机器学习、深度学习 |
| `#meta` | 方法论、工具、编程范式 |

### Wikilinks 与交叉引用

- 用 `[[页面名]]` 链接到其他 wiki 页面
- 用 `[文字](url)` 链接外部资源
- 每个页面**必须**包含 `## 关联连接` 区域——**绝不产生孤岛页面**

### Callout 标记系统

| 场景 | 标记 |
|:-----|:-----|
| 新发现（相比旧认识）| `> [!info] 新发现` |
| 与现有结论矛盾 | `> [!warning] 与 [[xxx]] 矛盾` |
| 待验证/不确定 | `> [!question] 待验证` |
| 知识空白 | `> [!todo] 待补充：<描述>` |
| 重要结论 | `> [!important]` |
| 已解决矛盾 | `> [!success] 矛盾已解决` |

### 命名约定

| 页面类型 | 命名规则 | 示例 |
|:---------|:---------|:-----|
| 资料摘要 | `摘要-{slug}.md`（kebab-case）| `摘要-attention-is-all-you-need.md` |
| 实体 | `EntityName.md`（TitleCase）| `AndrejKarpathy.md` |
| 概念 | `ConceptName.md`（中文或 TitleCase）| `Transformer架构.md` |
| 对比 | `{A}-vs-{B}.md` | `RAG-vs-LLM-Wiki.md` |
| 综合 | 主题描述 slug | `LLM-Wiki模式综合.md` |

优先中文命名；英文名/缩写作为 `aliases` 写入 frontmatter。

### 矛盾处理原则

1. **暂停**当前操作
2. **报告**：哪个页面、具体冲突点
3. **询问**：A) 保留双方建 `## 知识冲突` 区块 / B) 覆盖 / C) 放弃
4. **执行**：按用户选择，在 log.md 记录决策

> **绝对不要静默覆盖。**

---

## 操作速查

| 指令 | 技能 | 说明 |
|:-----|:-----|:-----|
| `/ingest` 或 `/ingest <路径>` | `ingest` | 将 raw/ 资料编译进 wiki |
| `/query <问题>` | `query` | 检索 wiki 并综合回答 |
| `/lint` | `lint` | 知识库健康检查 |
