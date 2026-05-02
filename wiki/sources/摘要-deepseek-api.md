---
title: "摘要-deepseek-api"
type: source
tags:
  - source
  - llm-api
  - deepseek
sources:
  - raw/01-articles/首次调用 API  DeepSeek API Docs.md
  - https://api-docs.deepseek.com/zh-cn/
  - https://api-docs.deepseek.com/zh-cn/guides/anthropic_api
  - https://api-docs.deepseek.com/zh-cn/quick_start/pricing
last_updated: 2026-04-27
---

> **一句话摘要**：DeepSeek API 同时兼容 OpenAI 和 Anthropic 两种 API 格式，通过简单切换 base_url 即可用现有 SDK 调用 DeepSeek 模型；但 Anthropic 兼容层存在显著能力缺口（无多模态、无 MCP、无 prompt cache）。

## 核心观点

- **双兼容策略是差异化优势**：大多数国产模型只兼容 OpenAI 格式，DeepSeek 额外提供 Anthropic 格式兼容，可直接接入 Claude Code 和 Anthropic SDK
- **兼容 ≠ 等价**：Anthropic 兼容层不支持图片/文档输入、MCP、prompt cache、thinking budget_tokens 控制、并行工具调用控制、redacted thinking 等
- **模型矩阵简单清晰**：v4-flash（快速）+ v4-pro（旗舰），均为 1M 上下文 / 384K 最大输出，均支持思考模式和工具调用
- **旧模型名即将弃用**：`deepseek-chat` 和 `deepseek-reasoner` 将于 2026/07/24 弃用，分别对应 v4-flash 的非思考/思考模式

## API 快速配置

| 参数 | OpenAI 格式 | Anthropic 格式 |
|:---|:---|:---|
| base_url | `https://api.deepseek.com` | `https://api.deepseek.com/anthropic` |
| api_key | 从 [platform.deepseek.com](https://platform.deepseek.com/api_keys) 申请 | 同左 |
| 认证方式 | `Authorization: Bearer <key>` | `x-api-key: <key>` |

```bash
# OpenAI 格式调用示例
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "thinking": {"type": "enabled"},
    "reasoning_effort": "high",
    "stream": false
  }'
```

## 模型能力矩阵

| 特性 | v4-flash | v4-pro |
|:---|:---|:---|
| 定位 | 快速 | 旗舰 |
| 上下文窗口 | 1M tokens | 1M tokens |
| 最大输出 | 384K tokens | 384K tokens |
| 思考模式 | ✅ 支持 | ✅ 支持 |
| JSON 输出 | ✅ | ✅ |
| 工具调用 | ✅ | ✅ |
| FIM 补全（Beta） | ✅（仅非思考模式） | ✅（仅非思考模式） |
| 输入价格（缓存命中） | ¥0.02/M | ¥0.025/M（限时2.5折） |
| 输入价格（缓存未命中） | ¥1/M | ¥3/M（限时2.5折） |
| 输出价格 | ¥2/M | ¥6/M（限时2.5折） |

> [!warning] v4-pro 限时 2.5 折促销截至 **2026/05/05 23:59**，之后恢复原价（输入 ¥12/M、输出 ¥24/M）

## Anthropic 兼容层能力缺口

| 功能 | 支持状态 |
|:---|:---|
| 文本消息（string / text block） | ✅ 完全支持 |
| 系统提示（system） | ✅ 完全支持 |
| 工具调用（tools / tool_use / tool_result） | ✅ 基本支持 |
| 思考模式（thinking） | ⚠️ 支持，但 `budget_tokens` 被忽略 |
| 流式输出（stream） | ✅ 完全支持 |
| 温度（temperature） | ✅ 支持，范围 [0.0, 2.0] |
| 图片输入（image） | ❌ 不支持 |
| 文档输入（document） | ❌ 不支持 |
| MCP（mcp_servers / mcp_tool_use） | ❌ 不支持 |
| Prompt Cache（cache_control） | ❌ 全部忽略 |
| 并行工具调用控制（disable_parallel_tool_use） | ❌ 忽略 |
| Redacted Thinking | ❌ 不支持 |
| 代码执行工具 | ❌ 不支持 |
| 搜索工具 | ❌ 不支持 |
| anthropic-version / anthropic-beta 头 | ❌ 忽略 |
| top_k | ❌ 忽略 |

## 对现有知识的贡献

- DeepSeek 的双兼容策略是一种 API 设计模式：通过实现多个事实标准来降低接入门槛
- Anthropic 兼容层的缺口清单可指导实际开发中的功能选择：哪些功能不能用 DeepSeek 替代 Claude

## 关联连接

- [[entities/DeepSeek]] — 公司实体
- [[concepts/programming/API兼容性策略]] — 双兼容策略概念详解
- [[concepts/programming/AgentSkills]] — Skills 与 API 格式同为 Anthropic 推动的开放标准
