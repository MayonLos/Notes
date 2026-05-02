---
name: wiki-lint
description: 知识库全局健康度检查。扫描 wiki/ 目录，检测死链、孤儿页面、未同步索引、认知冲突和知识空白。当用户输入 /lint、/scan、/health，或要求"检查知识库状态/健康"时调用。
user-invocable: true
---

# wiki-lint — 知识图谱健康巡检技能

> **Vault 根目录**：`D:\Obsidian Vault\`
> **Schema**：先读 `D:\Obsidian Vault\CLAUDE.md` 了解完整约定

---

## 目录路径速查

| 作用 | 路径 |
|:---|:---|
| 全局索引 | `D:\Obsidian Vault\wiki\index.md` |
| 操作日志 | `D:\Obsidian Vault\wiki\log.md` |
| Wiki 根目录 | `D:\Obsidian Vault\wiki\` |
| 概念子目录 | `concepts\programming\`、`concepts\theory\`、`concepts\embedded\`、`concepts\digital\` |
| 实体 / 来源 / 对比 / 综合 | `entities\`、`sources\`、`comparisons\`、`syntheses\` |
| 原始资料（待处理） | `D:\Obsidian Vault\raw\` |

---

## 触发条件

- 用户输入 `/lint`、`/scan`、`/health`
- 用户询问「知识库健康状况如何」
- **建议**：每摄入 5-10 份资料后主动建议运行一次 lint

---

## 巡检流水线

### 第 1 步：读取全局视图

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
obsidian vault="Obsidian Vault" read path="wiki/log.md"
```

提取 index.md 中所有注册的 `[[页面名称]]`，建立「已注册页面集合」。

### 第 2 步：扫描 wiki/ 所有 .md 文件

列出 `wiki/` 下所有 `.md` 文件（排除 `index.md`、`log.md`、`synthesis.md`），建立「实际文件集合」。

```bash
obsidian vault="Obsidian Vault" search query="type:" limit=200
```

### 第 3 步：索引一致性检查

比对两个集合：
1. **未同步索引**：文件存在但未在 `index.md` 注册 → ⚠️ 黄灯
2. **幽灵条目**：`index.md` 中注册了但文件不存在 → ❌ 红灯（死链）

### 第 4 步：双向链接健康检查

读取所有 wiki `.md` 文件，提取所有 `[[双链]]`：

1. 链接指向不存在的页面 → **死链** ❌
2. 从未被任何其他页面引用的页面 → **孤儿页面** ⚠️

```bash
obsidian vault="Obsidian Vault" backlinks file="PageName"
```

### 第 5 步：认知冲突审查

```bash
obsidian vault="Obsidian Vault" search query="知识冲突" limit=50
obsidian vault="Obsidian Vault" search query="[!warning]" limit=50
```

提取冲突页面、冲突双方、是否已解决。

### 第 6 步：知识空白检查

```bash
obsidian vault="Obsidian Vault" search query="待补充" limit=50
obsidian vault="Obsidian Vault" search query="待验证" limit=50
```

### 第 7 步：收件箱积压检查（可选）

检查 `raw/` 下（排除 `09-archive/`）还有哪些未处理文件：

```bash
obsidian vault="Obsidian Vault" search query="path:raw" limit=50
```

---

## 报告输出规范

```markdown
## 🩺 知识库健康体检报告 — YYYY-MM-DD

### ✅ 绿灯项
- [运行良好的项目]

### ⚠️ 黄灯项（需关注）
- **孤儿页面 (N 个)**：
  - [[concepts/digital/组合逻辑电路]]：无任何入站链接 → 建议：添加关联
- **未同步索引 (N 个)**：
  - `wiki/concepts/theory/Laplace变换.md` → 建议：补充注册到 index.md
- **未处理收件箱 (N 个)**：
  - `raw/01-articles/article.md` → 建议：运行 `/ingest`

### ❌ 红灯项（需立即修复）
- **死链 (N 个)**：
  - [[来源页面]] → [[不存在的目标页面]] → 建议：创建目标页面 或 修正链接
- **未解决知识冲突 (N 个)**：
  - [[ConflictPage]]：<冲突描述>

### ⬜ 知识空白 (N 个)
- [[ConceptPage]] 中的 `> [!todo]`：<描述> → 建议：<搜索关键词>

### 🛠️ 下一步行动
1. 是否需要自动修复未同步索引？
2. 是否需要针对知识冲突重新推演？
3. 是否需要立即摄入未处理的收件箱文件？
```

---

## 执行修复

**修复未同步索引**：
```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/index.md" \
  content="\n- [[concepts/theory/Laplace变换]] — 拉普拉斯变换基础"
```

**修复孤儿页面（添加关联）**：
```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/concepts/digital/数字系统综合.md" \
  content="\n- [[concepts/digital/组合逻辑电路]] — 相关概念"
```

每次修复后追加日志：
```bash
obsidian vault="Obsidian Vault" append \
  path="wiki/log.md" \
  content="\n## [{今日日期}] lint | 修复了 N 个问题\n- **变更**: <修复内容>"
```

---

## 硬约束

- **仅读扫描**：报告前禁止修改任何文件
- **手动确认**：报告后等待用户确认再执行修复
- **不读 raw/09-archive/**

---

## 关联连接

- [[wiki/index.md]] — 全局索引
- [[wiki/log.md]] — 操作日志
- [[CLAUDE.md]] — Wiki 架构总规范
