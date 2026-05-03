---
title: Wiki 索引
date: 2026-04-27
---

# Wiki 索引

> 知识库导航中枢。**每次 ingest 后自动更新**。查询前先读此文件定位相关页面。
>
> Vault：`D:\Obsidian Vault\wiki\`

---

## 🗺️ 推荐学习路线

> [!tip] 按领域顺序学习，领域间通过跨域链接贯通
>
> **C++ 编程**（顺序学习）
> [[concepts/cpp/基础语法|①基础语法]] → [[concepts/cpp/面向对象|②OOP]] → [[concepts/cpp/标准模板库|③STL]] → [[concepts/cpp/内存管理|④内存管理]]
>
> **数学 + 控制理论**（顺序学习）
> [[concepts/math/算子|①算子]] → [[concepts/math/Laplace变换|②Laplace变换]] → [[concepts/control/物理建模|③物理建模]] → [[concepts/control/方框图|④方框图]]
>
> **数字电路**（顺序学习）
> [[concepts/digital/原码反码补码|①原码反码补码]] → [[concepts/digital/组合逻辑电路|②组合逻辑电路]] → ③时序逻辑（待填充）
>
> **跨域桥梁**
> - C++ `int`/`char` 底层表示 ↔ [[concepts/digital/原码反码补码|补码]]
> - C++ 位运算符 (`&` `|` `^` `~`) ↔ [[concepts/digital/组合逻辑电路|逻辑门]]
> - 控制系统传递函数 ↔ [[concepts/math/算子|算子视角]] — 详见 [[syntheses/算子本质|算子本质（综合论述）]]

---

## 概念

### C++ 编程
<!-- wiki/concepts/cpp/ -->
- [[concepts/cpp/基础语法|C++ 基础语法]] — 数据类型、指针与引用、函数、控制流、模板入门
- [[concepts/cpp/面向对象|C++ 面向对象]] — 类、继承、多态、虚函数、抽象类、运算符重载
- [[concepts/cpp/标准模板库|C++ 标准模板库]] — vector / map / set 等容器、迭代器、sort / find 等算法
- [[concepts/cpp/内存管理|C++ 内存管理]] — 智能指针、RAII、Move 语义、Lambda、constexpr

### 数学工具
<!-- wiki/concepts/math/ -->
- [[concepts/math/Laplace变换|Laplace变换]] — 将微分方程化为代数方程，控制系统分析的数学基础（含定理推导）
- [[concepts/math/算子|算子]] — 函数→函数的映射规则，Laplace/微分/积分/传递函数都是算子的特例

### 控制理论
<!-- wiki/concepts/control/ -->
- [[concepts/control/物理建模|控制系统-物理建模]] — 机械/电路/流体/热力学系统的数学建模与传递函数推导
- [[concepts/control/方框图|控制系统-方框图]] — 框图元素、串并联反馈化简、误差传递函数

### 数字电路
<!-- wiki/concepts/digital/ -->
- [[concepts/digital/组合逻辑电路|组合逻辑电路]] — 逻辑门、加法器、MUX/DEMUX、编码器、译码器、比较器、竞争与冒险
- [[concepts/digital/原码反码补码|原码反码补码]] — 有符号整数的三种二进制编码，补码统一加减法的数学原理

### AI 工具与编程范式
<!-- wiki/concepts/programming/ -->
- [[concepts/programming/AgentSkills|AgentSkills]] — 用目录 + Markdown 定义 AI Agent 行为指南的开放标准，与 MCP 互补
- [[concepts/programming/渐进式加载|渐进式加载]] — 将信息按优先级分层、按需加载的设计模式，Agent Skills 的核心机制
- [[concepts/programming/API兼容性策略|API兼容性策略]] — LLM 服务商通过实现竞争 API 格式降低迁移成本，DeepSeek 双兼容（OpenAI + Anthropic）为典型案例

### 深度学习与 PyTorch
<!-- wiki/concepts/programming/ -->
- [[concepts/programming/PyTorch|PyTorch]] — Meta 开源的深度学习框架，动态计算图，学术界最常用，覆盖张量运算/自动求导/模型构建/训练部署全流程

### 嵌入式开发
<!-- wiki/concepts/embedded/ — 待填充 -->
*待填充。使用 `/ingest` 摄入 STM32、ROS 相关资料后自动填充。*

---

## 实体
<!-- wiki/entities/ -->

- [[entities/agentskills-io|Agent Skills 开放标准]] — Anthropic 于 2025-12-18 发布的 Agent 技能规范，生态包括 Claude Code / Codex / Cursor / OpenCode
- [[entities/DeepSeek|DeepSeek]] — 中国 LLM 服务商，API 双兼容（OpenAI + Anthropic），v4-flash/v4-pro，1M 上下文
- [[entities/DataWhale|DataWhale]] — AI 领域开源学习组织，"for the learner" 愿景，组队学习模式，维护深入浅出PyTorch 等教程

---

## 资料
<!-- wiki/sources/ -->

- [[sources/摘要-agent-skills-spec|摘要-agent-skills-spec]] — Agent Skills 开放标准规范的核心内容提炼：渐进式加载、SKILL.md 格式、与 MCP 的关系
- [[sources/摘要-deepseek-api|摘要-deepseek-api]] — DeepSeek API 双兼容配置指南、模型能力矩阵、Anthropic 兼容层能力缺口清单
- [[sources/摘要-thorough-pytorch|摘要-thorough-pytorch]] — DataWhale《深入浅出PyTorch》教程，从基础到实战覆盖 PyTorch 全流程，配套视频与练习

---

## 对比
<!-- wiki/comparisons/ -->

*暂无条目。*

---

## 综合
<!-- wiki/syntheses/ 和 wiki/synthesis.md -->

- [[syntheses/算子本质|算子本质]] — 算子的本质是「操作的代数化」，从维度跃升、Laplace 对应、算子链组合三个层次统一理解
- [[synthesis|整体综合论述]] — 对整个知识领域不断演化的综合理解（持续更新）
