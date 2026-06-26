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
| Concept pages (自控/数学) | `wiki/concepts/control/` |
| Concept pages (数字电路) | `wiki/concepts/digital/` |
| Concept pages (C++) | `wiki/concepts/cpp/` |
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
obsidian vault="Vaults" read path="wiki/index.md"
```

Identify all relevant concepts, entities, sources, and synthesis pages from the index.

---

### Step 2: Deep-Read Target Pages

```bash
obsidian vault="Vaults" read path="wiki/concepts/ConceptName.md"
obsidian vault="Vaults" read path="wiki/sources/摘要-slug.md"
```

Follow wikilinks up to **3 hops** to gather full context. Use backlinks to find pages that reference the topic:

```bash
obsidian vault="Vaults" backlinks file="ConceptName"
```

For broad questions, also read `wiki/synthesis.md` for the overall understanding framework.

---

### Step 3: Synthesize and Answer

Structure the answer with inline `[[wikilink]]` citations:

```
## 回答：<question>

<Synthesized answer referencing [[ConceptName]] and [[摘要-slug]]…>

### 依据

- [[ConceptName]] — <key point drawn from this page>
- [[摘要-source-slug]] — <what this source contributed>
```

**Language standards**:
- Use rigorous, precise language. Explicitly label epistemic status: 定义 (definition) / 定理 (theorem) / 推论 (corollary) / 猜想 (conjecture) / 经验规律 (empirical rule).
- Do not hedge unnecessarily — if the wiki content is clear, state it clearly.
- Do not summarize what the wiki says — synthesize it into a direct answer.

**End every answer with 延伸追问** — 1-2 follow-up questions pointing to deeper issues or cross-domain connections the user may not have considered:

```
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
obsidian vault="Vaults" create \
  path="wiki/syntheses/{topic-slug}.md" \
  content="---\ntitle: \"{title}\"\ntype: synthesis\ntags:\n  - synthesis\n  - <domain-tag>\nlast_updated: {today}\n---\n\n{answer content}\n\n## 关联连接\n\n- [[index]] — 全局索引\n- [[RelatedConcept]] — <relationship>\n" \
  silent
```

Register in `wiki/index.md` under the Syntheses section:

```bash
obsidian vault="Vaults" append \
  path="wiki/index.md" \
  content="\n- [[{slug}]] — <one-line description of what question this answers>"
```

Append to `wiki/log.md`:

```bash
obsidian vault="Vaults" append \
  path="wiki/log.md" \
  content="\n## [{today}] query | {question summary}\n- **输出**: saved [[{slug}]]"
```

If not saved, still log:

```bash
obsidian vault="Vaults" append \
  path="wiki/log.md" \
  content="\n## [{today}] query | {question summary}\n- **输出**: inline answer, not saved"
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

---
