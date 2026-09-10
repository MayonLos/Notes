---
name: lint
description: 只读检查笔记的结构与格式是否合规：frontmatter 字段、type/标签合法性、目录与标签一致性、wikilink 能否解析、index.md 登记、孤儿页、重复标题、公式里丢反斜杠。只报告不修复。问「该复习什么、还缺什么知识」是学习视角，属于 review，不是这里。
user-invocable: true
---

# lint：知识库体检（只读）

学习笔记的体检口径与通用 wiki 不同：**指向还没写的页面的链接是「待写页面」，不是错误**——只有嵌入资源（`![[图片]]`）缺失才算 ERROR。与已有页面相近的缺失链接降为 WARN 由人判断：中文短名里一字之差往往是另一个概念（`一阶系统` / `二阶系统`），不是拼写错误。已有页名整个被包住的（`状态空间` → `离散状态空间`）是「限定词 + 基词」构词，直接豁免不提示。

另一类肉眼极难发现的问题也在这里查：**数学公式里丢掉的反斜杠**。`\right` 经一次字符串转义会塌成 `ight`、`\frac` 塌成 `rac`，Obsidian 不报错、只静默渲染成乱码，通读十遍也未必看得见。

## 触发

- `/lint`、「体检 / 检查知识库 / 有没有死链孤儿页」。

不触发：
- 「哪些笔记很久没更新了 / 该复习什么 / 知识库还缺什么」→ `review`。**分界线**：lint 问「文件写得合不合规」，review 问「学得怎么样」。`last_updated` 在这里只查格式合法性与是否明显过期，排复习优先级是 review 的事。
- 修问题 → `note`（本 skill 不写文件）。

## 硬边界

- 纯只读审计：**不自动修复、移动、删除、改写任何文件**（脚本只写 `.claude/cache/vault-index/` 索引缓存）。
- 只检查 `/home/mayon/Vaults/wiki/` 与其链接到的根目录文档，另统计 `raw/01~05` 待处理文件数；不读 `raw/09-archive/`。
- 不碰 `.git/`、`.obsidian/`、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- 报告给路径 + 证据 + 建议；任何修复都要另行确认并由 `note` 执行。

## 运行

```bash
ROOT=/home/mayon/Vaults
python3 "$ROOT/.claude/skills/lint/scripts/check_vault.py" --root "$ROOT"
python3 "$ROOT/.claude/skills/lint/scripts/check_vault.py" --root "$ROOT" --json
python3 "$ROOT/.claude/skills/lint/scripts/check_vault.py" --root "$ROOT" --stale-days 90
```

检查项：入口三件套（`index/log/synthesis`）存在性 · frontmatter 必填与 `type` 合法性 · 标签是否已在 `CLAUDE.md` 登记 · 目录与主标签是否一致（口径来自 `_lib/vault.py` 的 `SUBJECTS`） · `## 关联连接` 是否存在 · 链接解析（resolved / 待写 / 歧义 / 缺标题 / 疑似打错） · **公式里丢反斜杠与 `$` 未闭合** · `index.md` 登记 · 入链为 0 的孤儿页 · `last_updated` 格式与过期 · 重复标题 · 内容标记计数 · `raw/` 待处理数。

不要把 `rg` 的退出码或高亮当结论；脚本没覆盖到的判断，写清楚是人工核对还是「未验证」。

## 报告格式

```markdown
# 知识库体检 — YYYY-MM-DD

## ❌ 失败（必须修）
- `wiki/xxx.md`：嵌入资源缺失 `![[kmap.png]]`

## ⚠️ 警告（建议修）
- `wiki/xxx.md`：`[[稳定裕度]]` 尚未建页且与 `稳定裕量` 相近——确认是打错字还是另一页
- `wiki/concepts/cpp/基础语法.md`：标签 `['concept','编程','C++']` 与目录 `cpp/` 不一致，建议改为 `cpp`
- `wiki/concepts/micro/汇编语言.md:91`：公式里疑似丢了反斜杠 `['sum']` — `sum_{i=0}^{4}BUF[i]`

## 📝 待写页面（正常待办，不是错误）
- `稳态误差` ← 2 处引用在等

## 📊 统计
16 页 · 0 错误 · 10 警告 · 18 待写 · 标记：冲突 0 / 待验证 2 / 待补充 9

## 下一步
按风险排序；标明哪些需要用户确认后交给 `/note` 修。
```

跑完确认没有产生文件差异（`git status --short -- wiki/` 应无新增改动）。

## 输出契约

`check_vault.py`：默认打印 `check_vault: PASS|WARN|FAIL` + `pages/errors/warnings/planned` + 逐条 `ERROR:`/`WARN:`/`NOTE:`；`--json` 输出 `{tool, root, status, checks, errors, warnings, planned, notes}`，`checks` 含 `pages, dead_links, ambiguous_links, missing_fragments, latex_issues, planned_pages, orphans, raw_pending, markers`。退出码 `0` 无 ERROR（含 WARN），`1` 有 ERROR。
