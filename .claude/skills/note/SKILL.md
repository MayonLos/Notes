---
name: note
description: 用户要求把内容落盘成笔记时触发——「记下来 / 写成笔记 / 补进那一页 / 收录这份资料」。把课堂、教材、视频或刚讲明白的知识点编译成 wiki 页面，负责查重、建页、双向连线、登记索引与日志。这是唯一会写文件的 skill。只讲解不落盘时不要触发。
user-invocable: true
---

# note：记笔记（唯一写入口）

把「刚学会的东西」编译进知识库：查重 → 写页 → 连线 → 登记 → 校验。

## 触发

- `/note <主题或内容>`：把这次学的内容写成/补进笔记。
- `/note raw/01-articles/xxx.md`：把一份 raw 资料编译成笔记（旧 `/ingest` 的场景）。
- 「把这个记下来 / 补进笔记 / 建一页 / 收录这篇资料」。

**必须有明确的落盘意图才触发。** 边界上最容易搞错的几句：

| 用户原话 | 归属 | 理由 |
|:---|:---|:---|
| 「课上刚讲的阻尼比，帮我理一下」 | 先讲解，讲完问一句要不要记 | 没说要落盘 |
| 「这段记进笔记」「补到二阶系统那页」 | `note` | 明确落盘 |
| 「二阶系统有没有登记进索引」 | `lint` | 是检查不是写 |
| 「帮我复习触发器」「体检一下」 | `review` / `lint` | 本页正文提到它们只是转交说明，不是触发词 |

## 硬边界

- Vault 根：`/home/mayon/Vaults`（下文 `$ROOT`）。只写 `wiki/`、`wiki/index.md`、`wiki/log.md`、必要时 `wiki/synthesis.md`。
- `raw/` 只读：不改名、不删除、不移动、不归档。`raw/09-archive/` 禁止读取。
- 不碰 `.git/`、`.obsidian/`、`.claude/`（本 skill 自身除外）、`.claudian/`、`.smart-env/`、`.env`、`.team/`、`.trash/`。
- **绝不静默覆盖**：与现有页面结论冲突时暂停，报告冲突点，给出 A) 保留双方建 `## 知识冲突` B) 覆盖 C) 放弃，按用户选择执行并记入 `log.md`。
- 默认一次一个主题/一份资料。批量必须先列清单并获得确认。
- 用户没讲、来源没写的内容不要补：宁可留 `> [!todo] 待补充：<描述>`。

## 流程

1. **查重与定位**（写之前必做）
   ```bash
   ROOT=/home/mayon/Vaults
   python3 "$ROOT/.claude/skills/note/scripts/check_page.py" --root "$ROOT" --new "二阶系统" --tag control
   ```
   - `status=duplicate` → 改为**更新已有页**，不新建。
   - `status=similar` → 先读相似页，确认是补充还是另立新页。
   - `awaited_by` 非空 → 这页已被别处 `[[链接]]` 等着，建完自动补上入链。
   - 资料摄入先跑 `--source raw/01-articles/xxx.md`；`invalid` 停止，`duplicate` 先问。

2. **确定落盘位置**（按主标签，见 `CLAUDE.md`）

   | 主标签 | 目录 |
   |:---|:---|
   | `control` / `math` | `wiki/concepts/control/` |
   | `digital` | `wiki/concepts/digital/` |
   | `cpp` / `embedded` | `wiki/concepts/cpp/` |
   | 资料摘要 | `wiki/sources/摘要-{slug}.md` |
   | 对比 | `wiki/comparisons/{A}-vs-{B}.md` |
   | 综合 | `wiki/syntheses/{主题}.md` |

3. **写页**——学习笔记的页面骨架（比通用摘要多两段：为什么这样、容易错在哪）：
   ```markdown
   ---
   title: "页面标题"
   type: concept          # concept|source|comparison|synthesis|entity
   tags:
     - control            # 不带 #，第一个是主标签
   aliases:
     - English Name
   sources: []            # 自学笔记留空列表；来自 raw 的写相对路径
   last_updated: YYYY-MM-DD
   ---

   > **一句话定义**：……（一句说清是什么、解决什么问题）

   ## 直觉 / 为什么需要它
   ## 原理与推导        ← 关键步骤写出来，$$ 公式 $$ 单独成行
   ## 典型例题 / 用法
   ## 易错点            ← 学习笔记的核心价值，写自己踩过的坑
   ## 关联连接
   - [[前置概念]] — 前置：为什么必须先懂它
   - [[后续概念]] — 后续：它把这里的结论用在哪
   ```
   - 前置/后续关系写清楚，别只写「相关」。
   - 图片放 `assets/`，用 `![[文件名.png]]` 嵌入；没有图不要编造文件名。
   - 新发现 `> [!info]`、矛盾 `> [!warning]`、存疑 `> [!question] 待验证`、空白 `> [!todo] 待补充`、结论 `> [!important]`。

4. **连线**：给相关旧页补上指回新页的链接——`## 关联连接` 是双向的，只写单向会制造孤儿页。

5. **登记**
   - `wiki/index.md`：在对应学科小节加一行 `- [[页面名]] — 一句话说明`。
   - `wiki/log.md`：**追加**（绝不改写历史）
     ```markdown
     ## [YYYY-MM-DD] create|update|merge | 页面名

     - 新建/更新 `wiki/concepts/xxx/页面名.md`
     - 内容：……
     - 更新 `wiki/index.md` 注册
     ```

6. **写后校验**（必跑，贴出真实结果）
   ```bash
   python3 "$ROOT/.claude/skills/note/scripts/check_page.py" --root "$ROOT" \
     --page wiki/concepts/control/二阶系统.md
   python3 "$ROOT/.claude/skills/_lib/build_index.py" --root "$ROOT"   # 刷新检索索引
   ```
   `check_page` 退出码 `0` 通过、`1` 有 ERROR。ERROR 必须修完再报告；`planned` 列出的是尚未建的页面，属正常待办。

## 输出契约

`check_page.py`：默认打印 `check_page: OK|FAIL` 与每项的 `errors/warnings/planned`；`--json` 输出 `{tool, root, status, results[]}`。三种模式互斥可叠加：`--new`（查重，含 `suggested_path`、`awaited_by`）、`--source`（raw 预检：`ready|duplicate|invalid`）、`--page`（写后校验，可重复）。
