---
title: <% tp.file.title %>
aliases: [导航, 索引]
category: 
tags: [模板, 导航笔记]
status: 📝草稿
difficulty: 
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
modified: <% tp.file.last_modified_date("YYYY-MM-DD HH:mm") %>
---

# MOC 导航模板

用于记录领域导航、知识地图、索引等。

## 概览

本领域的简要描述。

## 核心主题

| 笔记 | 难度 | 状态 | 说明 |
|------|------|------|------|
| [[笔记 1|主题 1]] | 2 | ✅完善 | 描述 |
| [[笔记 2|主题 2]] | 3 | 📝草稿 | 描述 |
| [[笔记 3|主题 3]] | 4 | 📝草稿 | 描述 |

## 学习路径

1. **阶段一** - 学习 [[笔记 1|主题 1]] 获取基础
2. **阶段二** - 学习 [[笔记 2|主题 2]] 加深理解
3. **阶段三** - 应用 [[笔记 3|主题 3]] 进行实践

## 前置要求

- [[前置要求 1|前置知识 1]]
- [[前置要求 2|前置知识 2]]

## 相关领域

- [[领域 1|相关领域 1]] - 连接说明
- [[领域 2|相关领域 2]] - 连接说明

## 进度跟踪

```dataview
TABLE category, status, difficulty
FROM "当前/文件夹"
WHERE file.name != "_index"
SORT difficulty ASC
```

## 推荐资源

- 资源 1
- 资源 2

---

返回 [[_nav/Home|首页]]
