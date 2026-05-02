---
title: <% tp.file.title %>
aliases: []
category: 
tags: [模板, 说明]
status: ✅已完善
difficulty: 
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
modified: <% tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
---

# 笔记模板说明

本文件夹包含标准笔记模板。

## 可用模板

### concept.md
用于理论、定义和概念笔记。

结构：
- 定义（abstract 块）
- 核心概念
- 公式和定理
- 实际例子
- 常见错误
- 应用场景
- 相关笔记

### moc.md
用于领域导航和知识地图（MOC = Map of Content）。

结构：
- 概览
- 核心主题表
- 学习路径
- 前置要求
- 相关领域
- 进度跟踪
- 资源

## 命名约定

### 文件名
- 使用英文，kebab-case：`filename-here.md`
- 使用数字前缀排序：`01-first.md`、`02-second.md`
- 索引用下划线：`_index.md`

### 文件夹名
- 使用英文，hyphens 连接：`folder-name`
- 相关主题分组到子文件夹

### 元数据

所有文件必须有 YAML 前言：

```yaml
---
title: <% tp.file.title %>
aliases: [备选名称]
category: [自控原理|数字电路|CPP|Python|AI|数学建模]
tags: [标签1, 标签2]
status: 📝草稿 | 🔄迭代中 | ✅已完善
difficulty: 1-5
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
modified: <% tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
---
```

## Vault 结构

```
vault/
├── _nav/              导航和首页
├── theory/            理论和数学
├── systems/           工程系统
├── programming/       编程技术
├── embedded/          嵌入式系统
├── templates/         笔记模板
├── assets/            图片和资源
└── .obsidian/         Obsidian 配置
```

## 编写指南

1. **原子化笔记**：一个笔记聚焦一个主题
2. **双向链接**：使用 `[[]]` 链接相关笔记
3. **数学公式**：行内用 `$...$`，块级用 `$$...$$`
4. **代码高亮**：指定语言 ` ```cpp`
5. **Callouts**：
   - `> [!abstract]` - 定义
   - `> [!formula]` - 公式
   - `> [!code]` - 代码
   - `> [!warning]` - 易错点

6. **语言**：专业、严谨、无冗余
7. **避免**：不用"总之"、"综上所述"

---

更多信息见 [[_nav/Home|首页]]
