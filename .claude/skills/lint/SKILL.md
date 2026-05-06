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
obsidian vault="Vaults" read path="wiki/index.md"
obsidian vault="Vaults" read path="wiki/log.md"
```

Extract all `[[page-name]]` references from index.md → build **registered pages set**.
Extract recent ingestion dates and topics from log.md → build **ingestion timeline**.

---

### Step 2: Scan All wiki/ Files

Enumerate all `.md` files under `wiki/` (excluding `index.md`, `log.md`, `synthesis.md`) → build **actual files set**.

The LLM should use the most reliable available method on the current platform. Obsidian CLI is preferred; platform-native directory listing is an acceptable fallback. The goal is a complete, accurate list of wiki page paths.

---

### Step 3: Index Consistency Check

Compare the two sets:

1. **Unsynced pages**: file exists but not registered in `index.md` → ⚠️ Yellow
2. **Ghost entries**: registered in `index.md` but file doesn't exist → ❌ Red (dead link in index)

---

### Step 4: Wikilink Health Check

Extract all `[[links]]` from every wiki `.md` file:

- Use Obsidian CLI backlinks for individual pages. For global wikilink extraction, use platform-native tools (e.g., `grep` on Unix, `Select-String` on Windows) to scan all `.md` files under `wiki/`.
- Alternatively, for each page in the actual files set, run Obsidian CLI backlinks to identify inbound references.

```bash
obsidian vault="Vaults" backlinks file="PageName"
```

1. Link target is not in the actual files set → **Dead link** ❌
2. Page is never referenced by any other page (no inbound backlinks) → **Orphan page** ⚠️

---

### Step 5: Cognitive Conflict Audit

```bash
obsidian vault="Vaults" search query="知识冲突" limit=50
obsidian vault="Vaults" search query="[!warning]" limit=50
```

For each result: identify the conflicting page, the parties in conflict, and whether it has been resolved.

---

### Step 6: Stale Knowledge Detection

Find pages where `last_updated` is more than **90 days ago** AND newer sources on the same topic appear in the log:

```bash
obsidian vault="Vaults" search query="last_updated" limit=200
```

Cross-reference with the ingestion timeline from Step 1. Flag pages where the `last_updated` date predates a log entry on the same topic — these may reflect superseded knowledge.

---

### Step 7: Knowledge Gap Scan

```bash
obsidian vault="Vaults" search query="待补充" limit=50
obsidian vault="Vaults" search query="待验证" limit=50
obsidian vault="Vaults" search query="[!todo]" limit=50
```

---

### Step 8: Inbox Backlog Check

Enumerate all unarchived files under `raw/` (exclude `09-archive/` entirely). Count how many source files are waiting to be ingested.

Use Obsidian CLI if available; fall back to platform-native file enumeration. The key metric is: how many files in `raw/01-04/` and `raw/05-wiki-export/` have not yet been ingested? Each file found is an item in the inbox backlog.

---

## Report Format

Generate this report after completing all 8 steps — do not modify any files before the report:

```
## 🩺 知识库健康体检报告 — YYYY-MM-DD

### ✅ 绿灯项
- [items running well, e.g. "索引与文件完全一致"]

### ⚠️ 黄灯项（需关注）
- **孤儿页面 (N 个)**：
  - [[ConceptName]]：无入站链接 → 建议：在相关页添加关联
- **未同步索引 (N 个)**：
  - `wiki/concepts/ConceptName.md` → 建议：注册到 index.md
- **知识过时 (N 个)**：
  - [[ConceptName]]：last_updated 2025-12-01，已有 2026-03 的相关摄入 → 建议：重新摄入更新来源
- **未处理收件箱 (N 个)**：
  - `raw/01-articles/article.md` → 建议：运行 `/ingest`

### ❌ 红灯项（立即修复）
- **死链 (N 个)**：
  - [[source-page]] 中 [[nonexistent-target]] → 建议：创建目标页面或修正链接
- **未解决认知冲突 (N 个)**：
  - [[ConflictPage]]：<description of conflict>

### ⬜ 知识空白 (N 个)
- [[ConceptPage]] 中 [!todo]：<description> → 建议：搜索关键词 "<term>"

### 📥 建议摄入清单
根据以上知识空白与过时页面，建议优先搜集：
1. <topic 1> — 填补 [[X]] 的空白
2. <topic 2> — 解决 [[Y]] 的过时问题

### 🛠️ 下一步行动
1. 是否自动修复未同步索引？（我可以执行）
2. 是否针对认知冲突重新推演？
3. 是否立即摄入收件箱积压文件？
```

---

## Executing Fixes (After User Confirmation)

**Fix unsynced index entry**:

```bash
obsidian vault="Vaults" append \
  path="wiki/index.md" \
  content="\n- [[ConceptName]] \`#tag\` — one-line definition"
```

**Fix orphan page** (add cross-reference from a related page):

```bash
obsidian vault="Vaults" append \
  path="wiki/concepts/RelatedConcept.md" \
  content="\n- [[OrphanConcept]] — <relationship>"
```

**Log each fix**:

```bash
obsidian vault="Vaults" append \
  path="wiki/log.md" \
  content="\n## [{today}] lint | Fixed N issues\n- **变更**: <specific fix description>"
```

---

## Hard Constraints

- **Read-only scan**: generate the report before modifying any files
- **Manual confirmation**: wait for user approval before executing any fixes
- **Never read `raw/09-archive/`**
