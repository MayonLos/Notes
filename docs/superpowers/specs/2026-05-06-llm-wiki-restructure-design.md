# LLM Wiki 全量重构设计文档

**日期**：2026-05-06  
**状态**：已批准，待实施  
**参考**：[Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

## 背景与目标

当前仓库基于 Karpathy LLM Wiki 模式，但存在以下问题：

1. Skills 路径与 CLAUDE.md 不一致（`concepts/theory/` vs `concepts/math/` + `concepts/control/`）
2. Skills 用中文书写，与行业惯例不符
3. `wiki-` 前缀冗余（文件夹已在 `.claude/skills/` 下，上下文已明确）
4. `concepts/` 按学科分子目录，跨领域概念归属模糊
5. 无 README，仓库对新访客不透明
6. `raw/09-archive/` 中的文件已无法重摄入

**目标**：对齐 Karpathy 原始设计理念，全量重建 wiki 基础设施。

---

## 决策记录

| 决策点 | 选择 | 理由 |
|:---|:---|:---|
| 重构范围 | 全层（meta + wiki 内容） | 彻底清零，消除历史债务 |
| 现有 wiki 内容 | 迁移到 `raw/05-wiki-export/` | 作为待重摄入资料，不直接保留 |
| archive 处理 | 解冻，移回对应 raw/ 目录 | 恢复可摄入状态 |
| concepts 分类 | 扁平化，靠 tags 区分领域 | 对齐 Karpathy"类型优先"原则 |
| Skills 语言 | 英文 | 行业惯例，与 Claude Code 生态一致 |
| Skills 命名 | 去掉 `wiki-` 前缀 | 路径已提供上下文 |
| Tags 体系 | 动态扩展（无匹配时新建） | 领域边界会随知识增长变化 |

---

## 新目录结构

```
Vaults/
├── raw/
│   ├── 01-articles/          # 网页剪藏（Obsidian Web Clipper）
│   ├── 02-papers/            # 论文、PDF
│   ├── 03-transcripts/       # 视频/播客转录
│   ├── 04-notes/             # 手写笔记
│   ├── 05-wiki-export/       # 旧 wiki 内容（待重摄入）★ 新增
│   └── 09-archive/           # 已处理文件归档
│
├── wiki/
│   ├── concepts/             # 所有概念页（扁平，tags 区分领域）
│   ├── entities/             # 人物、工具、公司、产品
│   ├── sources/              # 原始资料摘要页
│   ├── comparisons/          # A vs B 对比分析
│   ├── syntheses/            # 综合论述（高价值查询沉淀）
│   ├── index.md              # 全局目录（查询首先读这里）
│   ├── log.md                # 追加式操作日志
│   └── synthesis.md          # 整体演化主论述
│
├── assets/                   # 图片、附件
├── docs/                     # 项目文档（设计文档等）
├── README.md                 # 项目说明 ★ 新增
├── CLAUDE.md                 # Schema 文档（重写）
└── .claude/skills/
    ├── ingest/               # 摄入技能（原 wiki-ingest，重写）
    │   └── SKILL.md
    ├── query/                # 查询技能（原 wiki-query，重写）
    │   └── SKILL.md
    └── lint/                 # 健康检查（原 wiki-lint，重写）
        └── SKILL.md
```

---

## Tags 体系

初始 tags，可动态扩展：

| Tag | 覆盖领域 |
|:----|:--------|
| `#cpp` | C++ 编程语言 |
| `#math` | 数学工具（Laplace、算子等）|
| `#control` | 控制理论 |
| `#digital` | 数字电路与逻辑 |
| `#embedded` | 嵌入式开发（STM32、ROS）|
| `#ai` | 人工智能、机器学习、深度学习 |
| `#meta` | 方法论、工具、编程范式 |

**规则**：ingest 时若现有 tags 无法准确描述内容，自行创建新 tag 并追加到 CLAUDE.md 的 tags 列表。

---

## CLAUDE.md 重写规范

精简为 5 个板块（删除 Skills 内部已覆盖的冗余信息）：

1. **角色与语言** — 简体中文，LLM 维护者角色
2. **架构概览** — 三层架构图（raw / wiki / schema）
3. **文件权限边界** — 仅列各目录读写权限
4. **Wiki 页面规范** — frontmatter 格式、wikilink 规范、标记系统
5. **操作速查** — `/ingest` `/query` `/lint` 三条指令映射

---

## Skills 设计

### `ingest/SKILL.md`（英文）

**Pipeline（9步）**：

1. **Read source** — Obsidian CLI 优先（`obsidian vault read`），不可用时降级到文件读取工具
2. **Discuss with user** — 提炼 3-5 条收获，确认方向；**禁止跳过**
3. **Extract content** — 识别实体、概念、主旨；按 tags 分类（动态扩展）
4. **Create source summary** — `wiki/sources/摘要-{slug}.md`
5. **Network knowledge** — 更新/创建 entities、concepts 页（扁平路径）；冲突立即暂停报告
6. **Update synthesis.md** — 整体理解有变化时追加
7. **Update index.md** — 注册所有新页面，含 tags 列
8. **Append log.md** — 格式：`## [YYYY-MM-DD] ingest | Title`（支持 grep）
9. **Archive source** — 移入 `raw/09-archive/`

**摄入后提示**：询问是否为此资料生成对比页或综合页。

### `query/SKILL.md`（英文）

**输出格式**（自动选择或用户指定）：

| 格式 | 场景 | 触发 |
|:---|:---|:---|
| Markdown page | 通用问题 | 默认 |
| Comparison table | 两个概念对比 | 自动检测 / `--table` |
| Marp slide deck | 演示性综合 | `--marp` |
| Timeline | 事件序列 | `--timeline` |

**Pipeline（4步）**：

1. 读 `wiki/index.md` 定位相关页面
2. 深度阅读目标页 + 追溯双链上下文（最多 3 跳）
3. 综合回答，内联 `[[wikilink]]` 引用
4. **主动提问是否保存**——凡回答超过 3 句，询问是否沉淀为 `wiki/syntheses/`

**降级策略**：wiki 无内容时声明后仍作答，标注"通用知识，未摄入相关资料"。

### `lint/SKILL.md`（英文）

**七项检查**：

| # | 检查项 | 级别 |
|:--|:---|:---|
| 1 | 索引一致性（index.md vs 实际文件）| ❌/⚠️ |
| 2 | 死链（`[[链接]]` 指向不存在页面）| ❌ |
| 3 | 孤儿页（无任何入站链接）| ⚠️ |
| 4 | 认知冲突（未解决的 `[!warning]`）| ❌ |
| 5 | 知识过时（`last_updated` 超 90 天 + 有更新来源）| ⚠️ |
| 6 | 知识空白（含 `[!todo]`、`待补充`）| ⬜ |
| 7 | 收件箱积压（`raw/` 未归档文件数）| ⚠️ |

**报告末尾**：生成"建议摄入清单"，根据知识空白推荐应搜集的资料方向。

---

## README.md 框架

```
# LLM Wiki — Personal Knowledge Base
## 这是什么（引用 Karpathy 核心理念）
## 架构（三层图）
## 快速上手（/ingest /query /lint 表格）
## 目录结构（简洁树形图）
## 当前知识领域（tags 动态列表）
## 工具链（Obsidian + Claude Code + Obsidian CLI + qmd）
## 致谢（Andrej Karpathy）
```

---

## 迁移步骤（实施顺序）

1. 解冻 `raw/09-archive/` — 文件移回原分类目录
2. 导出旧 wiki — `wiki/**/*.md` 复制到 `raw/05-wiki-export/`
3. 清空 `wiki/` — 只保留三个空框架文件
4. 删除旧 skills 文件夹（`wiki-ingest/`、`wiki-query/`、`wiki-lint/`）
5. 重写 `CLAUDE.md`
6. 创建新 skills（`ingest/`、`query/`、`lint/`）
7. 写 `README.md`
8. Git commit
