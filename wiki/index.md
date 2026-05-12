---
title: Wiki 索引
type: index
tags:
  - index
  - meta
last_updated: 2026-05-07
---

# Wiki 索引

> 知识库导航中枢。**每次 ingest 后自动更新**。查询前先读此文件定位相关页面。

---

## 概念
<!-- wiki/concepts/ — 扁平结构，tags 区分领域 -->

### AI / 工具链 `#ai` `#ai-tools`
- [[AgentSkills]] `#ai-tools` — AI Agent 行为标准，目录+Markdown 定义技能，渐进式加载
- [[渐进式加载]] `#meta` — 信息分层按需加载的设计模式，Agent Skills 的核心机制
- [[API兼容性策略]] `#ai` — LLM 服务商通过实现竞争对手 API 格式降低迁移成本的策略
- [[PyTorch]] `#ai` — Meta 开源深度学习框架，动态计算图，学术界主流

### 数字电路 `#digital`
- [[计数制与编码]] `#digital` — 二/十六进制计数制与 BCD/ASCII 编码体系
- [[逻辑代数]] `#digital` — 布尔代数基本定律与运算，数字电路理论基础
- [[逻辑函数化简]] `#digital` — 公式化简法与卡诺图化简，含无关项处理
- [[逻辑门电路]] `#digital` — DTL/TTL/CMOS 三代门电路工艺与参数
- [[组合逻辑电路]] `#digital` — 加法器、MUX、译码器、编码器、MSI 设计
- [[锁存器和触发器]] `#digital` — SR/JK/D/T 触发器，时序逻辑的记忆单元
- [[原码反码补码]] `#digital` `#cpp` — 有符号数的三种二进制编码，补码是现代计算机唯一实用方案

### C++ `#cpp`
- [[基础语法]] `#cpp` — 数据类型、指针与引用、函数、位运算
- [[面向对象]] `#cpp` — 封装/继承/多态，虚函数，抽象类
- [[标准模板库]] `#cpp` — vector/map/set 等容器，迭代器，算法
- [[内存管理]] `#cpp` — 智能指针、RAII、Move 语义，现代 C++ 内存安全

### 数学 / 控制理论 `#math` `#control`
- [[算子]] `#math` `#control` — 函数→函数的映射，把运算本身视为数学对象
- [[Laplace变换]] `#math` `#control` — 将微积分算子转化为复频域代数运算
- [[物理建模]] `#control` — 从物理系统到传递函数 G(s) 的建模步骤
- [[方框图]] `#control` — 传递函数的图形化组合与闭环化简

---

## 实体
<!-- wiki/entities/ -->

- [[agentskills-io]] — Agent Skills 开放标准（Anthropic，2025-12-18 发布）
- [[DeepSeek]] — 中国 LLM 服务商，双兼容（OpenAI + Anthropic）格式
- [[DataWhale]] — AI 领域开源学习组织，深入浅出 PyTorch 教程维护方

---

## 资料
<!-- wiki/sources/ -->

- [[摘要-agent-skills-spec]] — Agent Skills 开放标准：渐进式加载、SKILL.md 格式、与 MCP 关系
- [[摘要-deepseek-api]] — DeepSeek API 双兼容策略与 Anthropic 兼容层能力缺口
- [[摘要-thorough-pytorch]] — DataWhale《深入浅出PyTorch》三阶段教程结构
- [[摘要-数字电路课堂笔记]] — 江苏大学数字电子技术课程手写笔记（52张，2026-03~04）
- [[摘要-锁存器与触发器]] — 维持-阻塞D触发器原理及锁存器→触发器进化链手写笔记

---

## 对比
<!-- wiki/comparisons/ -->

- [[TTL-vs-CMOS]] — TTL 与 CMOS 逻辑器件选型对比（功耗/速度/噪声容限/集成度）

---

## 综合
<!-- wiki/syntheses/ 和 wiki/synthesis.md -->

- [[算子本质]] — 从"维度跃升/微积分代数化/算子链"三层理解算子的本质
