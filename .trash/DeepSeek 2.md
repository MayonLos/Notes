---
title: "DeepSeek"
type: entity
tags:
  - entity
  - llm-provider
  - company
aliases:
  - DeepSeek API
  - 深度求索
sources:
  - raw/01-articles/首次调用 API  DeepSeek API Docs.md
last_updated: 2026-05-07
---

> **一句话描述**：DeepSeek（深度求索）是中国 LLM 服务商，以 API 双兼容（OpenAI + Anthropic 格式）和 1M 超长上下文为差异化特征，当前旗舰模型为 deepseek-v4-pro。

## 关键属性

| 属性 | 值 |
|:---|:---|
| 类型 | 公司 / LLM 服务商 |
| API 兼容性 | OpenAI 格式 + Anthropic 格式（双兼容） |
| 官网 | https://api-docs.deepseek.com |
| 当前模型 | deepseek-v4-flash、deepseek-v4-pro |
| 上下文窗口 | 1M tokens |
| 最大输出 | 384K tokens |

## 模型演进

| 状态 | 模型名 | 说明 |
|:---|:---|:---|
| ✅ 当前 | `deepseek-v4-flash` | 快速模型，前身是 deepseek-chat（非思考）/ deepseek-reasoner（思考） |
| ✅ 当前 | `deepseek-v4-pro` | 旗舰模型 |
| ⏳ 弃用中 | `deepseek-chat` | 将于 **2026/07/24** 弃用 |
| ⏳ 弃用中 | `deepseek-reasoner` | 将于 **2026/07/24** 弃用 |

## 关键能力

- **思考模式**：支持，通过 `thinking: {"type": "enabled"}` 启用
- **工具调用**：支持标准 tool_use / tool_result
- **JSON 模式**：支持
- **FIM 补全**：Beta 阶段，仅非思考模式可用

## 不支持的能力（Anthropic 兼容层）

- 多模态输入（图片、文档）
- MCP 协议
- Prompt Cache
- 并行工具调用控制
- Redacted Thinking
- 代码执行 / 搜索工具

## API 接入

```bash
# OpenAI 格式
base_url: https://api.deepseek.com

# Anthropic 格式
base_url: https://api.deepseek.com/anthropic
```

## 关联连接

- [[摘要-deepseek-api]] — API 详细文档摘要
- [[API兼容性策略]] — 双兼容策略概念
- [[AgentSkills]] — 同属 AI 工具开放生态
