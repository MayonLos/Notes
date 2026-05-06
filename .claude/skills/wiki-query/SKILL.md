---
name: wiki-query
description: 在 wiki/ 知识库中检索并综合回答用户问题。当用户输入 /query、或用自然语言询问"我的笔记里关于X"、"查询Y"、"知识库里有没有Z"时调用。必须先读 wiki/index.md 定位相关页面，再深度阅读，最后以双链引用格式回答。禁止凭模型记忆回答。知识库无相关内容时必须声明。
user-invocable: true
---

# wiki-query — 知识库查询技能

> **Schema**：先读 `CLAUDE.md` 了解完整约定

---

## 目录路径速查

| 作用 | 路径 |
|:---|:---|
| 全局索引（查询入口） | `wiki/index.md` |
| 操作日志 | `wiki/log.md` |
| 概念页（编程） | `wiki/concepts/programming/` |
| 概念页（理论） | `wiki/concepts/theory/` |
| 概念页（嵌入式） | `wiki/concepts/embedded/` |
| 概念页（数字电路） | `wiki/concepts/digital/` |
| 实体页 | `wiki/entities/` |
| 资料摘要 | `wiki/sources/` |
| 对比页 | `wiki/comparisons/` |
| 综合论述 | `wiki/syntheses/` |
| 整体综合 | `wiki/synthesis.md` |

---

## 触发场景

- 用户输入 `/query <问题>`
- 用户询问：「我的笔记里关于 X 是怎么说的」、「查询 Y 相关知识」
- 用户提及 wiki、知识库、笔记、记录等关键词

**降级策略**：wiki 中无相关内容时：
> 本地知识库中未找到相关内容，以下为通用知识回答：[直接回答]

---

## 检索与综合流水线

### 步骤 1：读取全局索引（永远的第一步）

```bash
obsidian vault="Obsidian Vault" read path="wiki/index.md"
```

在 index.md 中定位与问题相关的概念、实体、资料、综合页面。

### 步骤 2：深度阅读目标页面

```bash
obsidian vault="Obsidian Vault" read path="wiki/concepts/programming/CppBasics.md"
obsidian vault="Obsidian Vault" read path="wiki/concepts/digital/组合逻辑电路.md"
obsidian vault="Obsidian Vault" read path="wiki/sources/摘要-slug.md"
```

必要时追溯：
- `[[sources/xxx]]` → 查看资料摘要
- `[[entities/xxx]]`、`[[concepts/xxx]]` → 扩展上下文
- `[[synthesis.md]]` → 获取整体理解框架

也可通过反向链接查找相关页面：

```bash
obsidian vault="Obsidian Vault" backlinks file="ConceptName"
```

### 步骤 3：综合与回答

以结构化方式回答，使用双链引用：

```markdown
## 回答：<问题>

<综合回答正文，引用 [[concepts/digital/组合逻辑电路]] 中的…>

### 依据

- [[concepts/programming/CppBasics]] — <相关观点摘要>
- [[sources/摘要-source-slug]] — <资料来源说明>
```

**双链引用规范**：引用某页面信息时，在文本中标注 `[[页面名称]]`。

### 步骤 4：高价值内容固化（可选）

回答超过 2 段且具有总结性时，主动询问：
> 这是一个有价值的综合，是否保存到 `wiki/syntheses/`？

用户同意后：

```bash
obsidian vault="Obsidian Vault" create /
  path="wiki/syntheses/{主题描述}.md" /
  content="---/ntitle: /"{标题}/"/ntype: synthesis/ntags:/n  - synthesis/nlast_updated: {今日日期}/n---/n/n{回答内容}/n/n## 关联连接/n/n- [[wiki/index.md]] — 全局索引/n" /
  silent
```

在 `wiki/index.md` 的 Syntheses 分类下注册。

### 步骤 5：记录操作日志

```bash
obsidian vault="Obsidian Vault" append /
  path="wiki/log.md" /
  content="/n## [{今日日期}] query | {问题简述}/n- **输出**: {引用页面列表，或/"即时回答未保存/"}"
```

---

## 强制约束

- **禁止凭记忆回答**：必须先检索知识库
- **禁止静默回答**：知识库无内容时必须声明
- **探索可以归档**：好的探索值得留在 wiki 里

---

## 关联连接

- [[wiki/index.md]] — 全局索引
- [[wiki/log.md]] — 操作日志
- [[CLAUDE.md]] — Wiki 架构总规范
