---
name: query
description: 用户想知道自己的笔记里记了什么时触发——只读检索 wiki 并基于页面证据回答，索引优先、按需读片段。不写任何文件。纯讲解、做题、「别翻笔记直接讲」不要触发；问自己的学习状态用 review，要落盘用 note。
user-invocable: true
---

# query：查笔记（只读）

回答只能来自 Vault 里**真实读到**的内容；模型记忆可以用来组织语言，不能用来替代笔记里的结论。

## 触发

- `/query <问题>`。
- 「我的笔记里关于……」「知识库记过……吗」「之前是怎么推的」。

不触发：
- 「别翻笔记，直接给我讲一遍」「这道题怎么做」→ 直接正常回答，不用 skill、不必检索。
- 「二阶系统我还不会哪些 / 该复习什么」→ `review`（问的是学习状态，不是笔记内容）。
- 要写/补页 → `note`；要结构体检 → `lint`。

## 硬边界

- 只读 `/home/mayon/Vaults/wiki/` 与被其链接的根目录文档；不改任何笔记、索引、日志、配置。
- 不读 `raw/09-archive/`；不碰 `.git/`、`.obsidian/`、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- 用户明确说「保存/沉淀/建页」时，交给 `note`，本 skill 不写。
- 笔记里没有就说没有，并列出已检索范围；不要用常识补全后当成笔记内容。

## 检索顺序（token 纪律）

**先索引，后原文**。索引在 `.claude/cache/vault-index/`，由脚本按需自动刷新。

```bash
ROOT=/home/mayon/Vaults
Q="$ROOT/.claude/skills/query/scripts/lookup.py"

# 1. 定位：在标题/别名/标签/摘要/小标题里排序检索（最便宜）
python3 "$Q" --root "$ROOT" --search 触发器 特征方程

# 2. 定位到页后，先看骨架再决定读哪段
python3 "$Q" --root "$ROOT" --outline wiki/concepts/digital/锁存器和触发器.md

# 3. 只读需要的那几十行
sed -n '40,90p' "$ROOT/wiki/concepts/digital/锁存器和触发器.md"

# 4. 需要正文证据时才全文检索，只回上下文行
python3 "$Q" --root "$ROOT" --grep '特征方程|Q\^\{n\+1\}'

# 5. 需要顺链时看邻居，别整页读进来
python3 "$Q" --root "$ROOT" --neighbors 锁存器和触发器
```

规则：
- 除非问题确实覆盖全库，否则不要 `cat` 整个 `wiki/`，也不要为「保险」把 `index.md` 全文读进来——`--search` 已经覆盖索引。
- 顺 `[[wikilink]]` 最多 3 跳；再要扩大范围先说明理由。
- 单页超过 ~200 行时用 `--outline` + `sed` 读片段，不整页读。

## 回答要求

区分四层，别混在一起：**笔记原文结论** / **来源原文**（`sources/` 页）/ **你的推断** / **页面里已标的不确定性**（`[!warning]` `[!question]` `[!todo]` 原样保留）。多页说法不一致时并列呈现并给出路径，不要强行合并。

```markdown
## 结论
先给答案，再给适用范围。

## 依据
- [[锁存器和触发器#特征方程推导]] — 支持了什么（wiki/concepts/digital/锁存器和触发器.md:44）
- [[摘要-锁存器与触发器]] — 来源里的不同说法

## 不确定性
- 笔记缺 X；[[某页]] 标着待验证；结论 Y 是我的推断而非笔记内容。
```

结尾若发现明显知识缺口，一句话提示可以 `/note` 补页，但不要自己动手写。

## 输出契约

`lookup.py`：`lookup[mode]: ok|empty|resolved|missing|ambiguous`，`--json` 输出 `{tool, root, status, mode, ...}`。模式：`--search`（排序命中）、`--grep`（正文行）、`--outline`（小标题+行号）、`--neighbors`（出链/入链）、`--resolve`（单链接解析）、`--list`（清单，可加 `--subject control|digital|cpp`）。`--limit N` 控制返回条数（默认 8）。退出码 `0` 命中，`1` 未命中/未解析。
