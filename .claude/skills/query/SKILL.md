---
name: query
description: 只读检索本 Vault 的 wiki 并基于页面证据回答问题；不以模型记忆替代笔记内容，也不默认写入新页面。
user-invocable: true
---

# query：知识检索

## 触发

- `/query <问题>`。
- “我的笔记里关于……”“知识库是否记录了……”等明确检索意图。

## 边界

- 只读 `/home/mayon/Vaults/wiki/`；不得修改笔记、索引、日志或配置。
- 回答必须来自 Vault 中实际读取的内容；没有证据时明确说“当前知识库没有足够内容”。
- 不读取 `raw/09-archive/`，不触碰 `.git/`、`.obsidian/`、`.claude/`、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- 只有用户明确要求“保存/沉淀/创建页面”时，才转交 `ingest` 或另行确认写入范围；本 skill 不自行写入。

## 检索流程

1. 先读 `/home/mayon/Vaults/wiki/index.md`，确定候选页面和目录。
2. 用精确关键词、别名和标签在 `wiki/` 内检索，再深读最相关页面；宽问题可补读 `wiki/synthesis.md`。
3. 沿关键 `[[wikilink]]` 最多追踪 3 跳；需要更多范围时说明原因，不扫描无关资料。
4. 区分来源原文、wiki 整理结论、推断和未决冲突；保留页面中的 `warning`、`question`、`todo` 等不确定性。
5. 综合答案，不把多个页面的不同定义强行合并；发现矛盾时并列呈现并指出页面路径。

## 可用命令

```bash
ROOT=/home/mayon/Vaults
sed -n '1,240p' "$ROOT/wiki/index.md"
rg -n -i --glob '*.md' '关键词|别名|#标签' "$ROOT/wiki"
```

对候选页使用 `sed` 或 Obsidian CLI 只读读取。路径、标题和链接都以实际文件为准，不凭文件名猜测。

## 输出格式

```markdown
## 结论
用简体中文直接回答；先给结论，再给范围和限制。

## 依据
- [[实际页面]]：支持了什么。
- [[另一实际页面#标题]]：补充或提出不同说法。

## 不确定性
- 明确指出缺失、冲突、过期或仅为推断的部分。
```

链接到页面而不是只写裸文件名；若没有相关页面，列出已检索范围和建议的下一步，而不是用常识补全。

## 可执行只读校验

解析页面中的 wikilink 或确认单个目标时使用标准库脚本；脚本只读：

```bash
ROOT=/home/mayon/Vaults
python3 "$ROOT/.claude/skills/query/scripts/resolve_wikilinks.py" \
  --root "$ROOT" '目标页面'
python3 "$ROOT/.claude/skills/query/scripts/resolve_wikilinks.py" \
  --root "$ROOT" --scan --from wiki/某页面.md --json
```

输出契约：单目标默认输出 `resolve_wikilinks: RESOLVED|MISSING|AMBIGUOUS|MISSING-FRAGMENT`、target 和 matches；扫描模式输出每个目标的状态。`--json` 输出含 `tool`、`root`、`status`、`target`/`source`、`matches` 或 `results` 的 JSON。退出码 `0` 表示目标（或扫描中的全部链接）已解析，`1` 表示缺失、歧义或缺失标题/块；脚本不会改写链接。
