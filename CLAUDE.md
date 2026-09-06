# 个人学习 Wiki — Schema

> **Vault 根目录**：`/home/mayon/Vaults/`

---

## 角色与语言

- **语言**：无论输入何种语言，始终使用**简体中文**思考、回复、编写 wiki。
- **角色**：你正在维护一个**个人学习知识库**，涵盖自动控制原理、数字电路、C++ 等课程。你的任务是将碎片化信息编译成结构化、高度互联的 Obsidian 知识库。
- **协作模式**：用户负责来源筛选与方向引导；你负责所有簿记——摘要、交叉引用、维护。

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
  concepts/             # 概念页（按学科分子文件夹）
    control/            # 自动控制原理
    digital/            # 数字电路
    cpp/                # C++
  sources/              # 资料摘要页（从 raw/ 提炼）
  comparisons/          # 对比分析页
  syntheses/            # 综合论述页（经明确要求保存的高价值查询沉淀）
  index.md              # 全局目录（查询首先读这里）
  log.md                # 追加式操作日志
  synthesis.md          # 整体演化主论述

CLAUDE.md               # 本文件：schema 与约定
README.md               # 知识库说明与导航入口
TODO.md                 # 学习路线与待办事项
.claude/skills/         # 技能定义
  _lib/                 # 四个 skill 的共享库 + 索引构建
  note/                 # 记笔记（唯一写入口）
  query/                # 查笔记（只读）
  review/               # 复习自测（只读）
  lint/                 # 结构体检（只读）
.claude/cache/          # 索引缓存（自动生成，已 gitignore，非笔记）
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
| `README.md` | 读写（谨慎） | 知识库说明与导航 |
| `TODO.md` | 读写 | 学习路线与待办 |

---

## Wiki 页面规范

### YAML Frontmatter

每个 wiki 文件必须包含：

```yaml
---
title: "页面标题"
type: entity | concept | source | synthesis | comparison | index | meta
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

| Tag | 覆盖领域 | 对应子文件夹 |
|:----|:---------|:------------|
| `#control` | 自动控制原理 | `concepts/control/` |
| `#math` | 数学工具（Laplace、算子等）| `concepts/control/` |
| `#digital` | 数字电路与逻辑 | `concepts/digital/` |
| `#cpp` | C++ 编程语言 | `concepts/cpp/` |
| `#embedded` | 嵌入式开发（STM32、ROS）| `concepts/cpp/`（待定）|
| `#meta` | 方法论、工具、编程范式 | 视情况 |
| `#source` | 资料摘要页的类型标签 | `sources/` |
| `#comparison` | 对比分析页的类型标签 | `comparisons/` |

### Wikilinks 与交叉引用

- 用 `[[页面名]]` 链接到其他 wiki 页面
- 用 `[文字](url)` 链接外部资源
- 每个知识页面**必须**包含 `## 关联连接` 区域——**绝不产生孤岛页面**。`wiki/index.md` 是导航中枢，`wiki/log.md` 是追加式操作日志，分别遵循各自的导航与日志格式。

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

| 页面类型 | 路径 | 命名规则 | 示例 |
|:---------|:-----|:---------|:-----|
| 概念（自控）| `wiki/concepts/control/` | 中文或 TitleCase | `二阶系统.md` |
| 概念（数电）| `wiki/concepts/digital/` | 中文或 TitleCase | `组合逻辑电路.md` |
| 概念（C++）| `wiki/concepts/cpp/` | 中文或 TitleCase | `内存管理.md` |
| 资料摘要 | `wiki/sources/` | `摘要-{slug}.md` | `摘要-ogata-modern-control.md` |
| 对比 | `wiki/comparisons/` | `{A}-vs-{B}.md` | `PID-vs-超前校正.md` |
| 综合 | `wiki/syntheses/` | 主题描述 slug | `频域分析综合.md` |

优先中文命名；英文名/缩写作为 `aliases` 写入 frontmatter。

**概念子文件夹选择规则**：根据页面的主 tag 确定放置位置——`#control`/`#math` → `control/`，`#digital` → `digital/`，`#cpp` → `cpp/`。

### 矛盾处理原则

1. **暂停**当前操作
2. **报告**：哪个页面、具体冲突点
3. **询问**：A) 保留双方建 `## 知识冲突` 区块 / B) 覆盖 / C) 放弃
4. **执行**：按用户选择，在 log.md 记录决策

> **绝对不要静默覆盖。**

### 知识库 Skills

四个 skill 职责互斥，只有 `note` 能写：

| Skill | 用途 | 边界 |
|:------|:-----|:-----|
| `note` | 把学到的内容写成/更新笔记页，含 raw 资料摄入 | **唯一写入口**：可写 `wiki/`（含 `index.md`、`log.md`）；`raw/` 只读；冲突必须先问，绝不静默覆盖；默认一次一个主题 |
| `query` | 基于笔记证据回答问题 | 只读；索引优先、按需读片段；要落盘转交 `note` |
| `review` | 出自测题、排复习队列、找知识缺口、核对 TODO | 只读；看板与题目不写进 Vault |
| `lint` | 结构体检：frontmatter、链接、索引、孤儿页 | 只读；只报告不修复；待写页面按待办计，不算错误 |

分界线：**`note` 问「要不要落盘」，`query` 问「笔记里记了什么」，`review` 问「学得怎么样」，`lint` 问「文件写得合不合规」。** 做题与纯答疑不走 skill，直接回答即可。

**索引缓存**：`.claude/cache/vault-index/`（`pages.tsv` / `links.tsv` / `stats.json`）由 `.claude/skills/_lib/build_index.py` 生成，供 skill 先定位后精读，减少 token 消耗。它是派生数据，可随时删除重建；**新增标签、页面类型或学科目录时，同步更新 `.claude/skills/_lib/vault.py` 顶部常量**，否则 `lint` 会误报。

---

## 操作速查

| 指令 | 技能 | 说明 |
|:-----|:-----|:-----|
| `/note <主题或内容>` | `note` | 把这次学的内容写成/补进笔记页 |
| `/note raw/01-articles/x.md` | `note` | 把一份 raw 资料编译进 wiki（原 `/ingest`） |
| `/query <问题>` | `query` | 只读检索笔记并给出带出处的回答 |
| `/review` | `review` | 学习状态看板：该复习什么、缺什么 |
| `/review <页面>` | `review` | 基于该页出自测题并批改 |
| `/review <页面> --提纲` | `review` | 把该页压成默写/背诵提纲 |
| `/lint` | `lint` | 只读结构体检，不自动修复 |
