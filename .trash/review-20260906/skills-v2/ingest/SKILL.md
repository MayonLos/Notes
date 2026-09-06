---
name: ingest
description: 将 raw 中的一份资料安全编译为 wiki 页面，维护来源、链接、索引和日志。仅在用户要求摄入资料时使用，不负责泛化文件整理。
user-invocable: true
---

# ingest：资料摄入

## 触发

- `/ingest <Vault 相对路径>`：处理指定资料。
- `/ingest`：仅在用户明确要求批量处理时，扫描待处理资料。
- “收录/摄入/整理这篇资料到知识库”等明确意图。

## 边界与安全

- Vault 根目录固定为 `/home/mayon/Vaults`；所有文件操作使用绝对路径或先设置 `ROOT`。
- 允许写入：`wiki/`；必要时写入 `wiki/index.md`、`wiki/log.md`、`wiki/synthesis.md`。
- `raw/` 是来源层：只读，不改名、不删除、不覆盖、不自动移动到 `raw/09-archive/`。
- 不读取 `raw/09-archive/`；不触碰 `.git/`、`.obsidian/`、`.claude/`、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- 发现已有页面或结论冲突时暂停，报告冲突并请求选择；绝不静默覆盖。
- 默认一次处理一份资料；批处理必须先列出清单并获得用户确认。

## 流程

1. **确认来源**：解析为 `/home/mayon/Vaults/raw/...`，确认存在且不在 `raw/09-archive/`。先检查是否已有相同 `sources`、标题或文件名，避免重复摄入。
2. **读取与分层**：读取全文或可获得的文本；记录读取限制。区分来源明确写出的事实、作者观点、推断和待验证内容。
3. **提炼**：确定 1–2 句核心论点、3–5 个关键点、实体和概念；只创建能复用且有交叉连接的页面。
4. **写来源摘要**：优先创建 `wiki/sources/摘要-{slug}.md`，包含标准 frontmatter、来源路径、摘要、关键点、局限和 `## 关联连接`。
5. **更新知识页**：仅在新内容确实扩展或纠正现有知识时创建/更新 `wiki/concepts/`、`wiki/entities/`、`wiki/comparisons/` 或 `wiki/syntheses/`。遵守 `CLAUDE.md` 的类型、标签、目录和命名约定。
6. **连线与登记**：使用 `[[页面名]]` 建立双向有意义的关联；更新 `wiki/index.md`；在 `wiki/log.md` 追加本次动作。不要为制造连接而添加无意义链接。
7. **冲突处理**：把未决冲突标为待验证并停止相关覆盖，向用户说明涉及页面、双方说法和可选处理方式。
8. **验证**：写入后重新读取改动文件，运行下方检查，修复失败项后再报告。

## 页面最低结构

```markdown
---
title: "页面标题"
type: source | concept | entity | comparison | synthesis
tags:
  - 现有标签
aliases:
  - English alias
sources:
  - raw/相对路径
last_updated: YYYY-MM-DD
---

正文

## 关联连接

- [[相关页面]] — 关系说明
```

除非来源确实支持，不补写作者、日期、结论或引用。非中文资料保留英文术语作为 `aliases`，关键内容用简体中文表达。

## 写入前后检查

```bash
ROOT=/home/mayon/Vaults
find "$ROOT/raw" -path "$ROOT/raw/09-archive" -prune -o -type f -print | grep -F -- '指定路径'
test -f "$ROOT/wiki/index.md" && test -f "$ROOT/wiki/log.md"
rg -n '^sources:|^last_updated:|^## 关联连接' "$ROOT/wiki" --glob '*.md'
```

再运行 `lint` skill 的只读健康检查；报告实际命令、通过/失败项和未解决风险。不要把验证输出写入 Vault 笔记，除非用户明确要求。

## 可执行只读校验

写入 wiki 前先运行来源预检；脚本只读，不创建、移动或修改文件：

```bash
ROOT=/home/mayon/Vaults
python3 "$ROOT/.claude/skills/ingest/scripts/validate_ingest.py" \
  --root "$ROOT" --source "raw/01-articles/<文件名>"
# 仅盘点可摄入来源：
python3 "$ROOT/.claude/skills/ingest/scripts/validate_ingest.py" --root "$ROOT"
```

输出契约：默认输出 `validate_ingest: READY|DUPLICATE|INVENTORY|INVALID`、root/source、错误和警告；加 `--json` 输出含 `tool`、`root`、`status`、`source`、`checks`、`errors`、`warnings` 的 JSON。退出码 `0` 表示可继续或盘点成功，`1` 表示来源无效；`DUPLICATE` 仍需人工决定是否跳过。
