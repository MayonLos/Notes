# LLM Wiki Full Restructure — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 全量重构 LLM Wiki 仓库——迁移现有内容、重写三个 Skills（英文）、重写 CLAUDE.md、新增 README.md，对齐 Karpathy LLM Wiki 原始设计理念。

**Architecture:** 三层架构（raw 不可变层 / wiki 编译层 / CLAUDE.md schema 层）保持不变；concepts/ 改为扁平结构，用 tags 取代子目录；Skills 重命名并用英文重写；旧 wiki 内容迁移到 raw/05-wiki-export/ 待重摄入。

**Tech Stack:** Obsidian Markdown, YAML frontmatter, Obsidian CLI (`obsidian vault`), Claude Code Skills (SKILL.md), Git

---

## File Map

| Action | Path |
|:-------|:-----|
| Create dir | `raw/05-wiki-export/` |
| Move (archive→raw) | `raw/09-archive/* → raw/01-articles/ 或 raw/04-notes/` |
| Copy (wiki→export) | `wiki/**/*.md → raw/05-wiki-export/` |
| Clear & rewrite | `wiki/index.md`, `wiki/log.md`, `wiki/synthesis.md` |
| Delete dirs | `wiki/concepts/`, `wiki/entities/`, `wiki/sources/`, `wiki/comparisons/`, `wiki/syntheses/` |
| Rewrite | `CLAUDE.md` |
| Create | `.claude/skills/ingest/SKILL.md` |
| Create | `.claude/skills/query/SKILL.md` |
| Create | `.claude/skills/lint/SKILL.md` |
| Delete dirs | `.claude/skills/wiki-ingest/`, `.claude/skills/wiki-query/`, `.claude/skills/wiki-lint/` |
| Create | `README.md` |

---

## Task 1: Migrate — Unfreeze Archive & Export Wiki

**Files:**
- Create: `raw/05-wiki-export/` (directory)
- Move: `raw/09-archive/首次调用 API  DeepSeek API Docs.md → raw/01-articles/`
- Move: `raw/09-archive/Agent Skills ... .md → raw/01-articles/`
- Move: `raw/09-archive/2026-05-05-数字电路课堂笔记 → raw/04-notes/`
- Copy: all `wiki/**/*.md` (except index/log/synthesis) → `raw/05-wiki-export/`

- [ ] **Step 1.1: Create raw/05-wiki-export/ and copy wiki knowledge pages**

```bash
mkdir -p /home/mayon/Vaults/raw/05-wiki-export
# Copy all wiki knowledge pages (skip index.md, log.md, synthesis.md)
find /home/mayon/Vaults/wiki -name "*.md" \
  ! -name "index.md" ! -name "log.md" ! -name "synthesis.md" \
  -exec cp {} /home/mayon/Vaults/raw/05-wiki-export/ \;
ls /home/mayon/Vaults/raw/05-wiki-export/ | wc -l
```

Expected: 28 files

- [ ] **Step 1.2: Unfreeze archive — move files back to raw/**

```bash
# DeepSeek API doc → articles
mv "/home/mayon/Vaults/raw/09-archive/首次调用 API  DeepSeek API Docs.md" \
   /home/mayon/Vaults/raw/01-articles/

# AgentSkills bilibili article → articles
mv "/home/mayon/Vaults/raw/09-archive/Agent Skills (Claude Skills) 详细攻略，一期视频精通_哔哩哔哩_bilibili.md" \
   /home/mayon/Vaults/raw/01-articles/

# Digital circuits notebook (directory) → notes
mv /home/mayon/Vaults/raw/09-archive/2026-05-05-数字电路课堂笔记 \
   /home/mayon/Vaults/raw/04-notes/

ls /home/mayon/Vaults/raw/09-archive/
```

Expected: empty directory

- [ ] **Step 1.3: Clear wiki knowledge subdirectories**

```bash
rm -rf /home/mayon/Vaults/wiki/concepts
rm -rf /home/mayon/Vaults/wiki/entities
rm -rf /home/mayon/Vaults/wiki/sources
rm -rf /home/mayon/Vaults/wiki/comparisons
rm -rf /home/mayon/Vaults/wiki/syntheses
mkdir -p /home/mayon/Vaults/wiki/concepts
mkdir -p /home/mayon/Vaults/wiki/entities
mkdir -p /home/mayon/Vaults/wiki/sources
mkdir -p /home/mayon/Vaults/wiki/comparisons
mkdir -p /home/mayon/Vaults/wiki/syntheses
ls /home/mayon/Vaults/wiki/
```

Expected: concepts/ entities/ sources/ comparisons/ syntheses/ index.md log.md synthesis.md

- [ ] **Step 1.4: Reset wiki framework files**

Write `wiki/index.md`:

```bash
cat > /home/mayon/Vaults/wiki/index.md << 'EOF'
---
title: Wiki 索引
date: 2026-05-06
---

# Wiki 索引

> 知识库导航中枢。**每次 ingest 后自动更新**。查询前先读此文件定位相关页面。

---

## 概念
<!-- wiki/concepts/ — 扁平结构，tags 区分领域 -->

*暂无内容。运行 `/ingest` 摄入资料后自动填充。*

---

## 实体
<!-- wiki/entities/ -->

*暂无内容。*

---

## 资料
<!-- wiki/sources/ -->

*暂无内容。*

---

## 对比
<!-- wiki/comparisons/ -->

*暂无内容。*

---

## 综合
<!-- wiki/syntheses/ 和 wiki/synthesis.md -->

*暂无内容。*
EOF
```

Write `wiki/log.md`:

```bash
cat > /home/mayon/Vaults/wiki/log.md << 'EOF'
# Wiki 操作日志

> Append-only。每条以 `## [YYYY-MM-DD] type | title` 开头，支持 grep：
> `grep "^## \[" wiki/log.md | tail -5`

---

## [2026-05-06] init | 知识库全量重构

- **变更**: 清空 wiki/，重建框架文件；旧内容迁移至 raw/05-wiki-export/；archive 解冻至 raw/
- **冲突**: 无
EOF
```

Write `wiki/synthesis.md`:

```bash
cat > /home/mayon/Vaults/wiki/synthesis.md << 'EOF'
---
title: 整体综合论述
type: synthesis
tags:
  - synthesis
  - meta
last_updated: 2026-05-06
---

> 本页是对整个知识领域持续演化的综合理解。每次摄入对整体认知框架有影响的资料时追加更新。

*知识库刚刚重建。摄入资料后此页将持续演化。*

## 关联连接

- [[index]] — 全局索引
EOF
```

- [ ] **Step 1.5: Verify migration**

```bash
echo "=== raw/05-wiki-export ===" && ls /home/mayon/Vaults/raw/05-wiki-export/ | wc -l
echo "=== raw/01-articles ===" && ls /home/mayon/Vaults/raw/01-articles/
echo "=== raw/09-archive ===" && ls /home/mayon/Vaults/raw/09-archive/
echo "=== wiki/ (should be empty dirs + 3 files) ===" && find /home/mayon/Vaults/wiki -name "*.md" | sort
```

Expected:
- `raw/05-wiki-export/`: 28 files
- `raw/01-articles/`: contains DeepSeek doc + AgentSkills doc
- `raw/09-archive/`: empty
- `wiki/`: only index.md, log.md, synthesis.md

- [ ] **Step 1.6: Commit migration**

```bash
cd /home/mayon/Vaults
git add -A
git commit -m "$(cat <<'EOF'
migrate: export wiki to raw/05-wiki-export, unfreeze archive

- Copied 28 wiki knowledge pages to raw/05-wiki-export/ for re-ingestion
- Moved 3 archived files back to raw/01-articles/ and raw/04-notes/
- Cleared wiki subdirectories and reset framework files (index/log/synthesis)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Rewrite CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 2.1: Write new CLAUDE.md**

```bash
cat > /home/mayon/Vaults/CLAUDE.md << 'CLAUDEEOF'
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
CLAUDEEOF
```

- [ ] **Step 2.2: Verify CLAUDE.md**

```bash
wc -l /home/mayon/Vaults/CLAUDE.md
head -5 /home/mayon/Vaults/CLAUDE.md
```

Expected: ~120 lines, starts with `# LLM Wiki — Schema`

- [ ] **Step 2.3: Commit**

```bash
cd /home/mayon/Vaults
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
refactor(schema): rewrite CLAUDE.md — flat concepts, dynamic tags, 5-section structure

Removed redundant skill-internal content. Fixed path inconsistencies
(theory/ → concepts/ flat). Added dynamic tags table with extension rule.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Create ingest/SKILL.md

**Files:**
- Create: `.claude/skills/ingest/SKILL.md`

- [ ] **Step 3.1: Create directory and write SKILL.md**

```bash
mkdir -p /home/mayon/Vaults/.claude/skills/ingest
cat > /home/mayon/Vaults/.claude/skills/ingest/SKILL.md << 'EOF'
---
name: ingest
description: Compile raw source files into the wiki. Triggered by /ingest (scan all unarchived files) or /ingest <path> (specific file). Also triggers on natural language like "add this to the wiki", "ingest this article", "process this source". Never reads raw/09-archive/.
user-invocable: true
---

# ingest — Source Compilation Skill

## Quick Reference

| Role | Path |
|:-----|:-----|
| Web articles | `raw/01-articles/` |
| Papers / PDFs | `raw/02-papers/` |
| Transcripts | `raw/03-transcripts/` |
| Notes | `raw/04-notes/` |
| Legacy wiki export | `raw/05-wiki-export/` |
| Archived (do not read) | `raw/09-archive/` |
| Source summaries | `wiki/sources/` |
| Entity pages | `wiki/entities/` |
| Concept pages | `wiki/concepts/` |
| Global index | `wiki/index.md` |
| Operation log | `wiki/log.md` |

---

## Trigger Logic

1. `/ingest` — scan all `raw/` subdirectories (exclude `09-archive/`), list pending files, process each.
2. `/ingest <path>` — process the specified file only.
3. Natural language — "摄入这篇"、"导入这个"、"收录" → auto-trigger.

---

## Compilation Pipeline

### Step 1: Read Source File

**Priority**: Obsidian CLI first; fall back to file-read tool if CLI unavailable.

```bash
obsidian vault="Obsidian Vault" read path="raw/01-articles/filename.md"
```

For `.pdf` files: extract text. If extraction fails, record file metadata only.

---

### Step 2: Discuss with User ⚠️ REQUIRED — DO NOT SKIP

Extract 3-5 key insights from the source. Present them to the user and ask questions following these principles:

- **Socratic method**: do not state conclusions directly. Ask questions that guide the user to derive them independently.
- **Rigorous language**: distinguish clearly between 定义 (definition), 定理 (theorem), 推论 (corollary), and 猜想 (conjecture).
- **Cross-domain connections**: actively look for links to existing wiki content across domains (e.g., digital circuit encoding ↔ C++ integer representation; control system optimization ↔ AI gradient descent; Laplace transforms ↔ frequency-domain ML). Use these as entry points for questions.
- **One question at a time**: do not overwhelm with multiple questions simultaneously.

Example framing: instead of "This article explains that X is Y", ask "Given what the wiki already says about Z, what do you think the relationship between X and Y might be here?"

Ask: what aspects matter most? Any angles to emphasize? Any tension with prior knowledge?

---

### Step 3: Extract Core Content

From the source, identify:
- **Core thesis**: 1-2 sentence summary
- **Entities**: people, companies, tools, products → will go to `wiki/entities/`
- **Concepts**: frameworks, methods, theories → will go to `wiki/concepts/`

**Tag assignment** (flat structure — no subdirectories in concepts/):
Check existing tags in CLAUDE.md. If none fit the content accurately, create a new tag and **add it to the Tags table in CLAUDE.md**.

Non-Chinese content: translate key terms to Chinese before processing.

---

### Step 4: Create Source Summary Page

```bash
obsidian vault="Obsidian Vault" create \
  path="wiki/sources/摘要-{slug}.md" \
  content="..." silent
```

Template:

```markdown
---
title: "摘要-{slug}"
type: source
tags:
  - source
  - <domain-tag>
sources:
  - raw/01-articles/<filename>.md
last_updated: <today YYYY-MM-DD>
---

> **一句话摘要**：<core content in one sentence>

## 核心观点

- <point 1>
- <point 2>
- <point 3>

## 对现有知识的贡献

- <new information, contradictions, or supplements vs. existing wiki>

## 关联连接

- [[entities/EntityName]] — <relationship>
- [[concepts/ConceptName]] — <relationship>
```

---

### Step 5: Build Knowledge Network

For each extracted entity and concept:

1. **Page does not exist** → create per CLAUDE.md standards
2. **Page exists** → read it with Obsidian CLI, then incrementally merge

```bash
# Read existing page first
obsidian vault="Obsidian Vault" read path="wiki/concepts/ConceptName.md"

# Create new page
obsidian vault="Obsidian Vault" create \
  path="wiki/concepts/ConceptName.md" \
  content="..." silent

# Append to existing page
obsidian vault="Obsidian Vault" append \
  path="wiki/concepts/ConceptName.md" \
  content="\n## 补充信息（来自 [[sources/摘要-{slug}]]）\n..."
```

3. **Conflict detected** → **immediately pause**, report to user, await decision before continuing.

All pages must include `## 关联连接` with `[[wikilinks]]`. **No orphan pages.**

Concept page template:

```markdown
---
title: "ConceptName"
type: concept
tags:
  - concept
  - <domain-tag>
aliases:
  - <English name>
sources:
  - raw/01-articles/<filename>.md
last_updated: <today>
---

> **一句话定义**：<definition>

## 详细说明

<in-depth explanation>

## 与其他概念的关系

- [[concepts/RelatedConcept]] — <relationship>

## 实例 / 应用

<concrete examples>

## 关联连接

- [[sources/摘要-{slug}]] — 来源
```

---

### Step 6: Update synthesis.md

If the new source meaningfully shifts the overall understanding of the knowledge domain:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/synthesis.md" \
  content="\n> [!info] 新发现（来自 [[sources/摘要-{slug}]]）\n> <impact on overall understanding>"
```

---

### Step 7: Update index.md

Read `wiki/index.md`, then register all new pages under the appropriate section:

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
```

Add entries (include tags in brackets):
- Concepts: `- [[concepts/ConceptName]] \`#tag\` — one-line definition`
- Entities: `- [[entities/EntityName]] — one-line description`
- Sources: `- [[sources/摘要-{slug}]] — core thesis of the source`

---

### Step 8: Append to log.md

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [<today>] ingest | <source title>\n- **Changes**: added [[sources/摘要-{slug}]]; updated [[wiki/index.md]]\n- **Conflicts**: none"
```

Format `## [YYYY-MM-DD] ingest | Title` keeps the log grep-parseable:

```bash
grep "^## \[" wiki/log.md | tail -5
```

---

### Step 9: Archive Source File

After confirming all steps above are complete, move the source to `raw/09-archive/`. **Move only — never modify file content.**

---

### Post-Ingest Prompt

After completing the pipeline, ask:

> 这份资料是否值得生成 **对比页**（与现有某个概念的系统对比）或 **综合页**（作为高价值查询沉淀保存到 wiki/syntheses/）？

---

## Conflict Resolution

1. **Pause** the current ingest pipeline immediately
2. **Report**: which page, what exactly conflicts
3. **Ask**: A) keep both with `## 知识冲突` block / B) overwrite with new / C) abort this ingest
4. **Execute** per user choice; record decision in `wiki/log.md`

---

## Core Constraints

- A single source may touch 10-15 wiki pages
- Flagging contradictions is more valuable than hiding them
- Never modify any file under `raw/`
- Never read `raw/09-archive/`
EOF
```

- [ ] **Step 3.2: Verify**

```bash
wc -l /home/mayon/Vaults/.claude/skills/ingest/SKILL.md
head -5 /home/mayon/Vaults/.claude/skills/ingest/SKILL.md
```

Expected: ~160 lines, starts with frontmatter `---`

- [ ] **Step 3.3: Commit**

```bash
cd /home/mayon/Vaults
git add .claude/skills/ingest/
git commit -m "$(cat <<'EOF'
feat(skill): add ingest/SKILL.md — English rewrite with Socratic discussion

9-step pipeline: Obsidian CLI priority, Socratic questioning, cross-domain
connection prompts, dynamic tag extension, grep-parseable log format.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Create query/SKILL.md

**Files:**
- Create: `.claude/skills/query/SKILL.md`

- [ ] **Step 4.1: Create directory and write SKILL.md**

```bash
mkdir -p /home/mayon/Vaults/.claude/skills/query
cat > /home/mayon/Vaults/.claude/skills/query/SKILL.md << 'EOF'
---
name: query
description: Search the wiki and synthesize answers to user questions. Triggered by /query, or natural language like "what does my wiki say about X", "look up Y in my notes", "is there anything on Z". Must read wiki/index.md first. Never answers from model memory alone. Declares when wiki has no relevant content.
user-invocable: true
---

# query — Knowledge Retrieval Skill

## Quick Reference

| Role | Path |
|:-----|:-----|
| Global index (always start here) | `wiki/index.md` |
| Operation log | `wiki/log.md` |
| Concept pages | `wiki/concepts/` |
| Entity pages | `wiki/entities/` |
| Source summaries | `wiki/sources/` |
| Comparisons | `wiki/comparisons/` |
| Syntheses | `wiki/syntheses/` |
| Master synthesis | `wiki/synthesis.md` |

---

## Trigger Scenarios

- User types `/query <question>`
- User asks: "我的笔记里关于 X 是怎么说的"、"查询 Y"、"知识库里有没有 Z"
- User mentions: wiki、知识库、笔记、记录

---

## Output Formats

Selected automatically based on question type, or specified by the user:

| Format | Best for | Trigger |
|:-------|:---------|:--------|
| Markdown page | General questions | Default |
| Comparison table | Two-concept comparisons | Auto-detected / `--table` |
| Marp slide deck | Presentation-worthy syntheses | `--marp` |
| Timeline | Event sequences | `--timeline` |

---

## Retrieval & Synthesis Pipeline

### Step 1: Read Global Index

Always the first action, no exceptions.

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
```

Identify all relevant concepts, entities, sources, and synthesis pages from the index.

---

### Step 2: Deep-Read Target Pages

```bash
obsidian vault="Obsidian Vault" read path="wiki/concepts/ConceptName.md"
obsidian vault="Obsidian Vault" read path="wiki/sources/摘要-slug.md"
```

Follow wikilinks up to **3 hops** to gather full context. Use backlinks to find pages that reference the topic:

```bash
obsidian vault="Obsidian Vault" backlinks file="ConceptName"
```

For broad questions, also read `wiki/synthesis.md` for the overall understanding framework.

---

### Step 3: Synthesize and Answer

Structure the answer with inline `[[wikilink]]` citations:

```markdown
## 回答：<question>

<Synthesized answer referencing [[concepts/ConceptName]] and [[sources/摘要-slug]]…>

### 依据

- [[concepts/ConceptName]] — <key point drawn from this page>
- [[sources/摘要-source-slug]] — <what this source contributed>
```

**Language standards**:
- Use rigorous, precise language. Explicitly label epistemic status: 定义 (definition) / 定理 (theorem) / 推论 (corollary) / 猜想 (conjecture) / 经验规律 (empirical rule).
- Do not hedge unnecessarily — if the wiki content is clear, state it clearly.
- Do not summarize what the wiki says — synthesize it into a direct answer.

**End every answer with延伸追问** — 1-2 follow-up questions pointing to deeper issues or cross-domain connections the user may not have considered:

```markdown
---

**延伸追问**：
1. <A question that challenges an implicit assumption or points to a related wiki concept>
2. <A cross-domain question — connect this topic to a different domain already in the wiki>
```

These questions should not be rhetorical. They should be genuinely answerable and point toward productive next steps.

---

### Step 4: Offer to Save

If the answer is more than 3 sentences, always ask:

> 这是一个有价值的综合。是否保存到 `wiki/syntheses/` 作为永久页面？

If yes, create the synthesis page:

```bash
obsidian vault="Obsidian Vault" create \
  path="wiki/syntheses/{topic-slug}.md" \
  content="---\ntitle: \"{title}\"\ntype: synthesis\ntags:\n  - synthesis\n  - <domain-tag>\nlast_updated: {today}\n---\n\n{answer content}\n\n## 关联连接\n\n- [[index]] — 全局索引\n- [[concepts/RelatedConcept]] — <relationship>\n" \
  silent
```

Register in `wiki/index.md` under the Syntheses section:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/index.md" \
  content="\n- [[syntheses/{slug}]] — <one-line description of what question this answers>"
```

Append to `wiki/log.md`:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [{today}] query | {question summary}\n- **Output**: saved [[syntheses/{slug}]]"
```

If not saved, still log:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [{today}] query | {question summary}\n- **Output**: inline answer, not saved"
```

---

## Fallback (No Wiki Content)

When the wiki has no relevant content, declare it explicitly before answering:

> 本地知识库中未找到相关内容。以下为通用知识回答（准确性依赖模型训练数据，未经知识库验证）：

Then answer, and end with:

> 建议摄入以下类型资料以提升此领域的知识库覆盖：<specific suggestion>

---

## Hard Constraints

- **Never answer from model memory alone** — always read the wiki first
- **Never silently skip** — always declare when wiki has no relevant content
- **Good explorations belong in the wiki** — offer to save every synthesis that took more than 3 sentences
EOF
```

- [ ] **Step 4.2: Verify**

```bash
wc -l /home/mayon/Vaults/.claude/skills/query/SKILL.md
grep "name:" /home/mayon/Vaults/.claude/skills/query/SKILL.md | head -1
```

Expected: ~130 lines, `name: query`

- [ ] **Step 4.3: Commit**

```bash
cd /home/mayon/Vaults
git add .claude/skills/query/
git commit -m "$(cat <<'EOF'
feat(skill): add query/SKILL.md — output formats, Socratic follow-ups, save-by-default

4-step pipeline: index-first retrieval, 3-hop traversal, rigorous epistemic
labeling, 延伸追问 cross-domain follow-ups, always offer to save syntheses.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Create lint/SKILL.md

**Files:**
- Create: `.claude/skills/lint/SKILL.md`

- [ ] **Step 5.1: Create directory and write SKILL.md**

```bash
mkdir -p /home/mayon/Vaults/.claude/skills/lint
cat > /home/mayon/Vaults/.claude/skills/lint/SKILL.md << 'EOF'
---
name: lint
description: Global knowledge base health check. Scans wiki/ for dead links, orphan pages, unsynced index, cognitive conflicts, stale knowledge, and knowledge gaps. Triggered by /lint, /scan, /health, or "检查知识库状态/健康". Recommended after every 5-10 ingestions.
user-invocable: true
---

# lint — Knowledge Graph Health Check Skill

## Quick Reference

| Role | Path |
|:-----|:-----|
| Global index | `wiki/index.md` |
| Operation log | `wiki/log.md` |
| All wiki pages | `wiki/` |
| Raw inbox | `raw/` (excluding `09-archive/`) |

---

## Trigger Conditions

- User types `/lint`, `/scan`, `/health`
- User asks "知识库健康状况如何"、"检查一下知识库"
- **Recommended**: after every 5-10 ingestions

---

## Inspection Pipeline (8 Steps)

### Step 1: Read Global View

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
obsidian vault="Obsidian Vault" read path="wiki/log.md"
```

Extract all `[[page-name]]` references from index.md → build **registered pages set**.
Extract recent ingestion dates and topics from log.md → build **ingestion timeline**.

---

### Step 2: Scan All wiki/ Files

List all `.md` files under `wiki/` (excluding `index.md`, `log.md`, `synthesis.md`) → build **actual files set**.

```bash
obsidian vault="Obsidian Vault" search query="type:" limit=200
```

---

### Step 3: Index Consistency Check

Compare the two sets:

1. **Unsynced pages**: file exists but not registered in `index.md` → ⚠️ Yellow
2. **Ghost entries**: registered in `index.md` but file doesn't exist → ❌ Red (dead link in index)

---

### Step 4: Wikilink Health Check

Read all wiki `.md` files, extract all `[[links]]`:

1. Link points to a non-existent page → **Dead link** ❌
2. Page is never referenced by any other page → **Orphan page** ⚠️

```bash
obsidian vault="Obsidian Vault" backlinks file="PageName"
```

---

### Step 5: Cognitive Conflict Audit

```bash
obsidian vault="Obsidian Vault" search query="知识冲突" limit=50
obsidian vault="Obsidian Vault" search query="[!warning]" limit=50
```

For each result: identify the conflicting page, the parties in conflict, and whether it has been resolved.

---

### Step 6: Stale Knowledge Detection

Find pages where `last_updated` is more than **90 days ago** AND newer sources on the same topic appear in the log:

```bash
obsidian vault="Obsidian Vault" search query="last_updated" limit=200
```

Cross-reference with the ingestion timeline from Step 1. Flag pages where the `last_updated` date predates a log entry on the same topic — these may reflect superseded knowledge.

---

### Step 7: Knowledge Gap Scan

```bash
obsidian vault="Obsidian Vault" search query="待补充" limit=50
obsidian vault="Obsidian Vault" search query="待验证" limit=50
obsidian vault="Obsidian Vault" search query="[!todo]" limit=50
```

---

### Step 8: Inbox Backlog Check

Count unarchived files in `raw/` (excluding `09-archive/`):

```bash
obsidian vault="Obsidian Vault" search query="path:raw" limit=100
```

---

## Report Format

Generate this report after completing all 8 steps — do not modify any files before the report:

```markdown
## 🩺 知识库健康体检报告 — YYYY-MM-DD

### ✅ 绿灯项
- [items running well, e.g. "索引与文件完全一致"]

### ⚠️ 黄灯项（需关注）
- **孤儿页面 (N 个)**：
  - [[concepts/ConceptName]]：无入站链接 → 建议：在相关页添加关联
- **未同步索引 (N 个)**：
  - `wiki/concepts/ConceptName.md` → 建议：注册到 index.md
- **知识过时 (N 个)**：
  - [[concepts/ConceptName]]：last_updated 2025-12-01，已有 2026-03 的相关摄入 → 建议：重新摄入更新来源
- **未处理收件箱 (N 个)**：
  - `raw/01-articles/article.md` → 建议：运行 `/ingest`

### ❌ 红灯项（立即修复）
- **死链 (N 个)**：
  - [[source-page]] 中 `[[nonexistent-target]]` → 建议：创建目标页面或修正链接
- **未解决认知冲突 (N 个)**：
  - [[ConflictPage]]：<description of conflict>

### ⬜ 知识空白 (N 个)
- [[concepts/ConceptPage]] 中 `[!todo]`：<description> → 建议：搜索关键词 "<term>"

### 📥 建议摄入清单
根据以上知识空白与过时页面，建议优先搜集：
1. <topic 1> — 填补 [[concepts/X]] 的空白
2. <topic 2> — 解决 [[concepts/Y]] 的过时问题

### 🛠️ 下一步行动
1. 是否自动修复未同步索引？（我可以执行）
2. 是否针对认知冲突重新推演？
3. 是否立即摄入收件箱积压文件？
```

---

## Executing Fixes (After User Confirmation)

**Fix unsynced index entry**:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/index.md" \
  content="\n- [[concepts/ConceptName]] \`#tag\` — one-line definition"
```

**Fix orphan page** (add cross-reference from a related page):

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/concepts/RelatedConcept.md" \
  content="\n- [[concepts/OrphanConcept]] — <relationship>"
```

**Log each fix**:

```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [{today}] lint | Fixed N issues\n- **Changes**: <specific fix description>"
```

---

## Hard Constraints

- **Read-only scan**: generate the report before modifying any files
- **Manual confirmation**: wait for user approval before executing any fixes
- **Never read `raw/09-archive/`**
EOF
```

- [ ] **Step 5.2: Verify**

```bash
wc -l /home/mayon/Vaults/.claude/skills/lint/SKILL.md
grep "name:" /home/mayon/Vaults/.claude/skills/lint/SKILL.md | head -1
```

Expected: ~155 lines, `name: lint`

- [ ] **Step 5.3: Commit**

```bash
cd /home/mayon/Vaults
git add .claude/skills/lint/
git commit -m "$(cat <<'EOF'
feat(skill): add lint/SKILL.md — 8-step health check with stale knowledge detection

Added Step 6 (stale knowledge: last_updated vs log timeline cross-check) and
📥 recommended ingestion list at end of report.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Remove Old Skill Folders

**Files:**
- Delete: `.claude/skills/wiki-ingest/`
- Delete: `.claude/skills/wiki-query/`
- Delete: `.claude/skills/wiki-lint/`

- [ ] **Step 6.1: Remove old skill directories**

```bash
rm -rf /home/mayon/Vaults/.claude/skills/wiki-ingest
rm -rf /home/mayon/Vaults/.claude/skills/wiki-query
rm -rf /home/mayon/Vaults/.claude/skills/wiki-lint
ls /home/mayon/Vaults/.claude/skills/
```

Expected: `defuddle  ingest  json-canvas  lint  notebooklm  obsidian-bases  obsidian-cli  obsidian-markdown  query`

- [ ] **Step 6.2: Commit**

```bash
cd /home/mayon/Vaults
git add -A
git commit -m "$(cat <<'EOF'
chore: remove deprecated wiki-ingest, wiki-query, wiki-lint skill folders

Replaced by ingest/, query/, lint/ (English rewrites).

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Create README.md

**Files:**
- Create: `README.md`

- [ ] **Step 7.1: Write README.md**

```bash
cat > /home/mayon/Vaults/README.md << 'EOF'
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
EOF
```

- [ ] **Step 7.2: Verify**

```bash
wc -l /home/mayon/Vaults/README.md
head -3 /home/mayon/Vaults/README.md
```

Expected: ~100 lines, starts with `# LLM Wiki — Personal Knowledge Base`

- [ ] **Step 7.3: Commit**

```bash
cd /home/mayon/Vaults
git add README.md
git commit -m "$(cat <<'EOF'
docs: add README.md — LLM Wiki pattern intro, quickstart, toolchain

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Final Verification

- [ ] **Step 8.1: Verify complete structure**

```bash
echo "=== Skills ===" && ls /home/mayon/Vaults/.claude/skills/
echo "=== Wiki framework ===" && ls /home/mayon/Vaults/wiki/
echo "=== Wiki subdirs (should be empty) ===" && find /home/mayon/Vaults/wiki -name "*.md" | sort
echo "=== raw/05-wiki-export ===" && ls /home/mayon/Vaults/raw/05-wiki-export/ | wc -l
echo "=== raw/01-articles ===" && ls /home/mayon/Vaults/raw/01-articles/
echo "=== README ===" && head -1 /home/mayon/Vaults/README.md
echo "=== CLAUDE.md sections ===" && grep "^## " /home/mayon/Vaults/CLAUDE.md
```

Expected:
- Skills: `defuddle ingest json-canvas lint notebooklm obsidian-bases obsidian-cli obsidian-markdown query`
- Wiki subdirs: only `index.md log.md synthesis.md` (concepts/ entities/ etc. are empty dirs)
- raw/05-wiki-export/: 28 files
- raw/01-articles/: includes DeepSeek + AgentSkills docs
- README.md: starts with `# LLM Wiki — Personal Knowledge Base`
- CLAUDE.md sections: 角色与语言, 架构概览, 文件权限边界, Wiki 页面规范, 操作速查

- [ ] **Step 8.2: Verify skill frontmatter names**

```bash
grep "^name:" /home/mayon/Vaults/.claude/skills/ingest/SKILL.md
grep "^name:" /home/mayon/Vaults/.claude/skills/query/SKILL.md
grep "^name:" /home/mayon/Vaults/.claude/skills/lint/SKILL.md
```

Expected:
```
name: ingest
name: query
name: lint
```

- [ ] **Step 8.3: Final commit**

```bash
cd /home/mayon/Vaults
git status
git log --oneline -8
```

Expected: clean working tree, 7-8 commits ahead of the design spec commit.
