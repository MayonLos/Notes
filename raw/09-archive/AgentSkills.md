---
title: "AgentSkills"
type: concept
tags:
  - concept
  - ai-tools
  - agent
  - programming
aliases:
  - Agent Skills
  - Claude Skills
  - SKILL.md
sources:
  - wiki/sources/摘要-agent-skills-spec.md
  - https://agentskills.io/specification
last_updated: 2026-04-27
---

> **一句话定义**：Agent Skills 是一个开放标准，用目录结构 + Markdown 文件定义 AI Agent 的行为指南，通过渐进式加载机制让 Agent 在节省上下文的同时获取所需知识。

## 详细说明

### 什么是 Agent Skills？

Agent Skills 是 Anthropic 于 2025 年 12 月 18 日正式发布的开放标准。它规定了一种**以目录为单位的技能打包格式**，每个 skill 至少包含一个 `SKILL.md` 文件，其中用 YAML frontmatter 描述元数据，用 Markdown 正文描述操作指令。

与 MCP（Model Context Protocol）不同，Skills 侧重于**知识/流程层**而非**能力/工具层**：
- **Skills** = 告诉 Agent "怎么做"（步骤、流程、最佳实践）
- **MCP** = 给 Agent "能做什么"（API 调用、数据库访问、文件操作）

### 工作原理：渐进式加载

Agent Skills 的核心机制是 **渐进式加载（Progressive Disclosure）**，分三层：

```
第 1 层 — 元数据索引（~100 tokens/skill）
  └─ 启动时加载所有 skill 的 name + description
  └─ Agent 据此判断哪些 skill 与当前任务相关

第 2 层 — 完整指令（< 5000 tokens 推荐）
  └─ 匹配到任务后加载 SKILL.md 正文
  └─ 包含详细步骤、示例、边界情况

第 3 层 — 按需资源
  └─ 执行时按需读取 scripts/、references/、assets/
  └─ 避免一次性加载所有内容
```

**设计动机**：上下文窗口是有限资源。50 个 skill 若每个 5000 tokens，一次性加载需要 25 万 tokens。渐进式加载让 Agent 在启动时只需 ~5000 tokens 就能掌握所有 skill 的索引。

### SKILL.md 格式规范

```yaml
---
name: skill-name              # 必需：1-64 字符，小写+数字+连字符
description: |                # 必需：做什么 + 何时触发
  Describe what and when.
license: Apache-2.0           # 可选
compatibility:                # 可选：环境要求
  Requires git, docker
metadata:                     # 可选：自定义键值对
  author: example-org
allowed-tools:                # 可选（实验性）：预批准工具列表
  Bash(git:*) Read
---
# Markdown 正文 — 任意格式
```

`name` 字段必须与父目录名一致，且只能用小写字母、数字、连字符。

### 可选子目录

| 目录 | 用途 | 示例 |
|:---|:---|:---|
| `scripts/` | 可执行代码（Python/Bash/JS） | `scripts/extract.py` |
| `references/` | 按需加载的参考文档 | `references/REFERENCE.md` |
| `assets/` | 模板、图片、数据文件 | `assets/template.docx` |

推荐将 `SKILL.md` 控制在 500 行以内，详细资料移到 `references/` 中。

## 与其他概念的关系

- [[concepts/programming/渐进式加载]] — Agent Skills 的核心设计模式，决定了三层加载架构
- MCP（待补充） — 互补关系，Skills 提供流程知识，MCP 提供工具能力
- [[entities/agentskills-io]] — 开放标准本身，及生态概览

## 实例 / 应用

### 本 Vault 中的应用

本知识库的 `.claude/skills/` 目录即为 Skills 标准的实际应用：

```
.claude/skills/
├── wiki-ingest/     # 资料摄入流程
├── wiki-query/      # 知识库查询
├── wiki-lint/       # 健康检查
├── obsidian-cli/    # Obsidian 操作
└── obsidian-markdown/  # Markdown 规范
```

每次执行 `/ingest` 命令时，Agent 通过渐进式加载激活 `wiki-ingest` skill 的完整指令来执行摄入流水线。

### 其他已知应用

- **Claude Code**：内置 Skills 支持，`.claude/skills/` 目录
- **Codex by OpenAI**：已加入 Skills 支持
- **Cursor**：已加入 Skills 支持
- **OpenCode**：已加入 Skills 支持

## 关联连接

- [[sources/摘要-agent-skills-spec]] — 来源：规范摘要
- [[concepts/programming/渐进式加载]] — 核心设计模式
- [[entities/agentskills-io]] — 标准实体与生态
