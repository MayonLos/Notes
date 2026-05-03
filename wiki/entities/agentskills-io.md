---
title: "agentskills-io"
type: entity
tags:
  - entity
  - open-standard
  - ai-tools
  - anthropic
aliases:
  - Agent Skills 开放标准
  - agentskills.io
sources:
  - https://agentskills.io/specification
  - raw/01-articles/Agent Skills (Claude Skills) 详细攻略，一期视频精通_哔哩哔哩_bilibili.md
last_updated: 2026-04-27
---

> **一句话描述**：Agent Skills 是 Anthropic 于 2025 年 12 月 18 日发布的开放标准，用于定义 AI Agent 技能的打包、分发和加载格式。

## 关键属性

| 属性 | 值 |
|:---|:---|
| 类型 | 开放标准 |
| 发布方 | Anthropic |
| 发布日期 | 2025-12-18 |
| 规范地址 | https://agentskills.io/specification |
| 许可证 | 开放标准（Apache 2.0 兼容生态） |
| 状态 | 活跃发展中 |

## 相关知识

### 生态组成

| 组件 | 说明 | 地址 |
|:---|:---|:---|
| 规范网站 | 完整格式规范 + 文档 | https://agentskills.io |
| 官方 Skill 仓库 | Anthropic 维护的示例 Skills | https://github.com/anthropics/skills |
| 参考验证工具 | Skills 格式校验 CLI | https://github.com/agentskills/agentskills |
| Awesome 列表 | 社区 Skills 汇总 | https://github.com/ComposioHQ/awesome-claude-skills |

### 支持工具

- **Claude Code** — 原生支持，`.claude/skills/` 目录
- **Codex** — 已加入支持
- **Cursor** — 已加入支持
- **OpenCode** — 已加入支持

### 与 MCP 的关系

Skills 与 MCP 同为 Anthropic 推动的 Agent 开放标准，但定位不同：
- **Skills**：定义 Agent **行为知识**（流程、最佳实践）
- **MCP**：定义 Agent **工具能力**（API、数据库、文件系统）
- 两者互补，共同构成 Agent 的完整工具生态

## 关联连接

- [[sources/摘要-agent-skills-spec]] — 规范摘要
- [[concepts/programming/AgentSkills]] — 技术概念详解
- [[concepts/programming/渐进式加载]] — 核心设计模式
