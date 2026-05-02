---
title: "摘要-agent-skills-spec"
type: source
tags:
  - source
  - ai-tools
  - agent
sources:
  - raw/01-articles/Agent Skills (Claude Skills) 详细攻略，一期视频精通_哔哩哔哩_bilibili.md
  - https://agentskills.io/specification
last_updated: 2026-04-27
---

> **一句话摘要**：Agent Skills 是 Anthropic 发布的开放标准，用目录 + Markdown 文件定义可渐进式加载的 AI Agent 行为指南，2025 年 12 月 18 日发布，与 MCP 并列构成 Agent 工具生态的两大支柱。

## 核心观点

- **渐进式加载是核心设计**：技能元数据（~100 tokens）→ 完整指令（<5000 tokens）→ 按需资源（scripts/references/assets），三层逐级加载，避免上下文浪费
- **SKILL.md 是唯一必需文件**：YAML frontmatter（name、description 必需）+ Markdown 正文（任意格式），最小化 skill 只需一个文件
- **与 MCP 互补而非替代**：Skills 管"怎么做"（指令/知识层），MCP 管"能做什么"（能力/工具层），两者配合使用
- **生态快速扩大**：Codex、Cursor、OpenCode 等工具已陆续支持，Awesome Claude Skills 列表持续增长

## 关键资源

| 资源 | 链接 |
|:---|:---|
| 开放标准规范 | https://agentskills.io/specification |
| 官方 Skill 仓库 | https://github.com/anthropics/skills |
| Awesome 列表 | https://github.com/ComposioHQ/awesome-claude-skills |
| 参考验证工具 | https://github.com/agentskills/agentskills |
| 示例源码（技术爬爬虾） | https://github.com/tech-shrimp/agent-skills-examples |

## 目录结构

```
skill-name/
├── SKILL.md          # 必需：元数据 + 指令
├── scripts/          # 可选：可执行代码（Python/Bash/JS）
├── references/       # 可选：详细参考文档
├── assets/           # 可选：模板、资源文件
└── ...               # 任意额外文件
```

## 对现有知识的贡献

- 填补了 AI Agent 工具链中 **指令层标准化** 的知识空白
- Skills 与 MCP 的分工明确了 Agent 架构的两个独立维度
- 渐进式加载是一种通用设计模式，可应用于其他需要节省上下文的场景

## 关联连接

- [[concepts/programming/AgentSkills]] — Agent Skills 技术概念详解
- [[concepts/programming/渐进式加载]] — 渐进式加载设计模式
- [[entities/agentskills-io]] — Agent Skills 开放标准实体
- [[concepts/control/方框图]] — 类似的系统架构分层思维
