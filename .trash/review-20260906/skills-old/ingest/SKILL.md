---
name: ingest
description: Compile raw source files into the wiki. Triggered by /ingest (scan all unarchived files) or /ingest <path> (specific file). Also triggers on natural language like "add this to the wiki", "ingest this article", "process this source". Never reads raw/09-archive/.
user-invocable: true
---

# ingest — Source Compilation Skill

## Quick Reference

| 角色 | 路径 |
|:---|:---|
| 网页文章 | `raw/01-articles/` |
| 论文文献 | `raw/02-papers/` |
| 转录文案 | `raw/03-transcripts/` |
| 手写笔记 | `raw/04-notes/` |
| 旧版 wiki 导出 | `raw/05-wiki-export/` |
| 已归档（禁止读取） | `raw/09-archive/` |
| 资料摘要页 | `wiki/sources/` |
| 概念页（自控/数学）| `wiki/concepts/control/` |
| 概念页（数字电路）| `wiki/concepts/digital/` |
| 概念页（C++）| `wiki/concepts/cpp/` |
| 全局索引 | `wiki/index.md` |
| 操作日志 | `wiki/log.md` |

## Trigger Logic

1. `/ingest` — scan all files in `raw/01-articles/`, `raw/02-papers/`, `raw/03-transcripts/`, `raw/04-notes/`, `raw/05-wiki-export/` that have not yet been archived. Process each in sequence.
2. `/ingest <path>` — process the single file at `<path>` directly.
3. Natural language — phrases like "add this to the wiki", "ingest this article", "process this source", "收录这篇文章", "摄入这个资料" all trigger this skill.

## Compilation Pipeline

### Step 1: Read Source File

Prefer Obsidian CLI:

```
obsidian vault="Vaults" read path="raw/01-articles/filename.md"
```

Fall back to the file-read tool if the CLI fails. For PDF files: extract text content. If text extraction fails, record metadata only (title, authors, date, abstract if visible) and note the limitation in the summary page.

### Step 2: Discuss with User ⚠️ REQUIRED — DO NOT SKIP

Extract 3–5 key insights from the source. Then open a Socratic dialogue with the user before writing anything to the wiki.

**Principles:**
- **Socratic method**: Do not state conclusions directly. Ask questions that guide the user to derive insights themselves. The goal is active engagement, not passive consumption.
- **Rigorous language**: Carefully distinguish between 定义（definition）、定理（theorem）、推论（corollary）、猜想（conjecture）. Do not present speculation as established fact.
- **Cross-domain connections**: Actively look for links across the wiki's knowledge domains. Examples of productive entry points:
  - Digital circuit encoding ↔ C++ integer representation (two's complement, overflow behavior)
  - Control system transfer functions ↔ Laplace transform algebraic rules
  - Physical modeling ↔ block diagram simplification (same system, different representation)
  Use these connections as entry points for questions, not as assertions.
- **One question at a time**: Do not overwhelm. Ask one focused question, wait for the response, then proceed.

**Example framing:**

> 这篇资料的核心论点是 X。在我将它收录进 wiki 之前，我想先问你：你觉得这个观点和你已有的 [[ConceptName]] 认知有没有张力？

Ask what aspects of the source matter most to the user. Ask if there is any tension with prior knowledge already in the wiki. Let the discussion shape what gets emphasized in the compilation.

### Step 3: Extract Core Content

After the discussion, extract and classify:

- **核心论点**（1–2 sentences）: the source's central claim or contribution.
- **实体**（→ `wiki/entities/`）: named people, organizations, tools, products, events.
- **概念**（→ `wiki/concepts/`）: frameworks, methods, theories, algorithms.

**Tag assignment**: Check the Tags table in `CLAUDE.md` for existing tags. If no existing tag fits the new content, create a new tag and add it to the Tags table in `CLAUDE.md` before proceeding.

**Subfolder selection**: Determine the concept's domain subfolder from its primary tag — `#control` or `#math` → `wiki/concepts/control/`; `#digital` → `wiki/concepts/digital/`; `#cpp` → `wiki/concepts/cpp/`.

**Non-Chinese content**: translate key terms to Chinese, keeping the English original as an `aliases` entry in the frontmatter.

### Step 4: Create Source Summary Page

Create `wiki/sources/摘要-{slug}.md` using Obsidian CLI:

```
obsidian vault="Vaults" create path="wiki/sources/摘要-{slug}.md" content="..."
```

Template:

```markdown
---
title: "摘要-{slug}"
type: source
tags:
  - source
  - <主题领域>
sources:
  - raw/01-articles/filename.md
last_updated: YYYY-MM-DD
---

> [!important] 一句话摘要
> <用一句话概括核心内容>

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

### Step 5: Build Knowledge Network

For each entity and concept extracted in Step 3:

**If the page does not exist**, create it in the appropriate subfolder (determined by tag in Step 3):

```
obsidian vault="Vaults" create path="wiki/concepts/{domain}/ConceptName.md" content="..."
# domain = control | digital | cpp
```

**If the page exists**, read it first, then merge:

```
obsidian vault="Vaults" read path="wiki/concepts/{domain}/ConceptName.md"
obsidian vault="Vaults" append path="wiki/concepts/{domain}/ConceptName.md" content="..."
```

**If a conflict is detected** — immediately pause the pipeline. Do not proceed to Step 6. Go to the Conflict Resolution section below.

All pages must have a `## 关联连接` section with wikilinks to related pages. No orphan pages are permitted. Every new page must be linked from at least one existing page.

Concept page template:

```markdown
---
title: "ConceptName"
type: concept
tags:
  - concept
  - <领域>
aliases:
  - <英文名或别名>
sources:
  - raw/01-articles/filename.md
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

### Step 6: Update synthesis.md

If the new source meaningfully shifts the overall understanding of any topic in `wiki/synthesis.md`, append a callout using Obsidian CLI:

```
obsidian vault="Vaults" append path="wiki/synthesis.md" content="
> [!info] 新发现 — YYYY-MM-DD
> 来源：[[摘要-{slug}]]
> <一句话说明本次 ingest 如何改变或扩展了整体理解>
"
```

Only update if there is a genuine shift. Do not append boilerplate.

### Step 7: Update index.md

Read `wiki/index.md` first, then register all new pages created in this ingest run.

Format for concepts (include tag in backticks):

```
- [[ConceptName]] `#tag` — 一句话定义
```

Format for entities:

```
- [[EntityName]] — 一句话描述
```

Format for sources:

```
- [[摘要-{slug}]] — 该资料的核心主旨
```

### Step 8: Append to log.md

Append a single log entry:

```markdown
## [YYYY-MM-DD] ingest | {Source Title}
- **变更**: 新增 [[摘要-{slug}]]；新增/更新 [[ConceptName]]；更新 [[index.md]]
- **冲突**: 无（或：冲突 [[ConflictingPage]]，已标注）
```

To verify recent log entries:

```bash
grep "^## \[" wiki/log.md | tail -5
```

### Step 9: Archive Source File

Move the source file to `raw/09-archive/`:

```bash
mv raw/01-articles/filename.md raw/09-archive/filename.md
```

Move only. Never modify the file's content. Never delete it.

---

### Post-Ingest Prompt

After completing all 9 steps, ask the user:

> 这次收录涉及了 [[ConceptA]] 和 [[ConceptB]]。是否值得生成一个对比页（`comparisons/`）或综合论述页（`syntheses/`）？

## Conflict Resolution

If at any point in Step 5 a new claim contradicts an existing claim in the wiki:

1. **Pause** — stop the ingest pipeline immediately. Do not write any further files.
2. **Report** — tell the user exactly which page contains the conflict, quote both the existing claim and the new claim.
3. **Ask** — present three options:
   - **A**: Keep both claims, add a `## 知识冲突` block to the existing page with both versions labeled by source and date.
   - **B**: Overwrite with the new claim, removing the old one.
   - **C**: Abort this ingest run, leaving the wiki unchanged.
4. **Execute** — implement the user's chosen option. Append a conflict note to `wiki/log.md` regardless of which option is chosen.

> **绝对不要静默覆盖。** Silent overwriting is a hard prohibition.

## Core Constraints

- A single source may touch 10–15 wiki pages. This is expected and desirable — it means the source is well-integrated into the knowledge graph.
- Flagging contradictions is more valuable than hiding them. The wiki's reliability depends on visible conflict tracking.
- Never modify any file under `raw/`. The raw layer is immutable and is the sole ground truth.
- Never read `raw/09-archive/`. Archived files are considered processed and must not be re-ingested.
