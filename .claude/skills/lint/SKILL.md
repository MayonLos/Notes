---
name: lint
description: 只读检查本 Vault 的 wiki 结构、frontmatter、索引一致性、wikilink、孤儿页和来源待办，输出可复核的知识库健康报告。
user-invocable: true
---

# lint：知识库健康检查

## 触发

- `/lint`、`/scan`、`/health`。
- “检查知识库状态/死链/孤儿页/整理风险”等请求。

## 硬边界

- 这是只读审计：不得自动修复、移动、删除或改写任何文件。
- 只检查 `/home/mayon/Vaults/wiki/`，可统计 `raw/01-articles/` 至 `raw/05-wiki-export/` 的待办数量；绝不读取 `raw/09-archive/`。
- 不触碰 `.git/`、`.obsidian/`、`.claude/`、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- 输出问题的绝对路径、等级、证据和建议；修复必须另获用户确认，并交由对应流程执行。

## 检查项目

1. **入口与结构**：`wiki/index.md`、`wiki/log.md`、`wiki/synthesis.md` 是否存在；页面是否位于约定目录。
2. **Frontmatter**：每个 wiki Markdown 是否有 YAML frontmatter、`title`、`type`、`tags`、`last_updated`；`type` 是否属于 `entity|concept|source|synthesis|comparison`。
3. **索引一致性**：实际页面与 `index.md` 的注册项分别找出未登记页和幽灵链接。
4. **链接健康**：解析 `[[目标]]`、`[[目标#标题]]`、`[[目标|别名]]`；报告无法解析的目标、缺失标题和图片/文件 embed。
5. **孤儿与重复**：统计没有入链的页面；报告重复标题、重复来源或同名不同路径，避免合并猜测。
6. **内容风险**：标出 `知识冲突`、`待验证`、`待补充`、过期 `last_updated` 和缺少 `## 关联连接` 的页面。
7. **来源待办**：统计未归档目录中的文件数量和类型；不把数量误报为已完成摄入。

## 便携检查命令

```bash
ROOT=/home/mayon/Vaults

test -f "$ROOT/wiki/index.md" && test -f "$ROOT/wiki/log.md"
find "$ROOT/wiki" -type f -name '*.md' -print | sort
rg -n '^\[\[|\]\]|^sources:|^last_updated:|知识冲突|待验证|待补充|## 关联连接' "$ROOT/wiki" --glob '*.md'
find "$ROOT/raw" -path "$ROOT/raw/09-archive" -prune -o -type f -print | sort
```

命令只用于取证；不要把 `rg` 的高亮或退出码直接当结论。必要时用一个临时 Python 脚本解析 frontmatter 和 wikilink，并在报告中写出脚本版本/命令。

## 报告格式

```markdown
# 知识库健康报告 — YYYY-MM-DD

## ✅ 通过
- 检查项：证据和命令。

## ⚠️ 警告
- [绝对路径] 问题、证据、建议；不自动修复。

## ❌ 失败
- [绝对路径] 可复现的死链、缺字段或结构错误。

## 📥 待办
- raw 未处理文件数量及建议。

## 下一步
按风险排序列出动作，并注明需要用户确认的写入操作。
```

报告完成后再次确认：没有产生文件差异；若发现权限、运行中的 Obsidian 或解析器限制，明确标注为“未验证”，不要猜测结果。

## 可执行只读校验

用标准库脚本执行结构化健康检查；脚本只读，不自动修复：

```bash
ROOT=/home/mayon/Vaults
python3 "$ROOT/.claude/skills/lint/scripts/check_vault.py" --root "$ROOT"
python3 "$ROOT/.claude/skills/lint/scripts/check_vault.py" --root "$ROOT" --json
```

输出契约：默认输出 `check_vault: PASS|WARN|FAIL`、页面数、错误数、警告数和问题清单；`--json` 输出含 `tool`、`root`、`status`、`checks`、`errors`、`warnings` 的 JSON。`checks` 至少包含 `pages`、`frontmatter`、`dead_links`、`unindexed`、`orphans`、`raw_pending`。退出码 `0` 表示无错误（即使有 WARN），`1` 表示存在错误。
