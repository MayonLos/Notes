---
title: 操作日志
date: 2026-04-27
---

# 操作日志

> 按时间顺序记录所有 wiki 操作。**只追加，不修改历史记录。**
>
> 快速查看最近 5 条：`grep "^## \[" log.md | tail -5`

---

## [2026-04-27] init | Vault 完整重建

- **变更**：
  - 废弃旧结构（`theory/`、`programming/`、`embedded/`、`systems/`、`_nav/`、`llm-wiki/`）
  - 新建根目录结构：`raw/`（01-articles / 02-papers / 03-transcripts / 04-notes / 09-archive）+ `wiki/`（concepts / entities / sources / comparisons / syntheses）
  - `CLAUDE.md` 移至 Vault 根目录，路径全部更新
  - 迁移现有笔记为初始 wiki 概念页：
    - `programming/cpp/*.md` → `wiki/concepts/programming/`（4 个文件）
    - `theory/math/01-Laplace-Transform.md` → `wiki/concepts/theory/Laplace变换.md`
    - `theory/control/*.md` → `wiki/concepts/theory/`（2 个文件）
    - `theory/digital_circuits/*.md` → `wiki/concepts/digital/`（2 个文件）
    - 图片资产迁移至 `assets/`
  - 重写三个核心技能（wiki-ingest / wiki-query / wiki-lint），全部使用新根目录路径
  - `wiki/index.md` 重建，注册所有迁移内容
- **冲突**：无

## [2026-04-27] query | Laplace 定理推导通式 + 算子概念
- **输出**：基于 [[concepts/math/Laplace变换]] + 通用数学知识，综合回答了微分定理、积分定理的推导过程及其统一原理（$s$ 为微分算子、$1/s$ 为积分算子）
- **后续操作**：
  - 补充 [[concepts/math/Laplace变换]] — 新增「定理推导与统一原理」章节（分部积分推导 + 算子对照表）
  - 新建 [[concepts/math/算子]] — 算子概念页（定义、类型、线性性质、时频域对应关系）
  - 更新 [[index|Wiki 索引]] — 注册算子页面

## [2026-04-27] query | Laplace 定理推导通式
- **输出**：基于 [[concepts/math/Laplace变换]] + 通用数学知识，综合回答了微分定理、积分定理的推导过程及其统一原理（$s$ 为微分算子、$1/s$ 为积分算子）
- **缺口**：Laplace 页面缺少推导过程，已向用户提议补充

## [2026-04-27] ingest | DeepSeek API 首次调用 + Anthropic 兼容指南 + 模型能力
- **变更**：
  - 新增 [[sources/摘要-deepseek-api]] — 三份资料合并摘要（首次调用 / Anthropic 兼容层 / 模型定价）
  - 新增 [[concepts/programming/API兼容性策略]] — LLM API 双兼容模式与格式兼容层次
  - 新增 [[entities/DeepSeek]] — 公司实体（模型矩阵、兼容层能力缺口、定价）
  - 更新 [[index|Wiki 索引]] — 新增概念、实体、资料条目
  - 更新 [[synthesis|综合论述]] — 新增 API 兼容性论点、DeepSeek 实体、开放问题
- **冲突**：无
- **来源**：DeepSeek API 官方文档（首次调用 / Anthropic API 指南 / 定价页）

## [2026-04-27] ingest | Agent Skills (Claude Skills) 详细攻略 + 开放标准规范

- **变更**：
  - 新增 [[sources/摘要-agent-skills-spec]] — Agent Skills 开放标准规范摘要
  - 新增 [[concepts/programming/AgentSkills]] — 技术概念详解（SKILL.md 格式、渐进式加载、与 MCP 关系）
  - 新增 [[concepts/programming/渐进式加载]] — 渐进式加载设计模式概念页
  - 新增 [[entities/agentskills-io]] — Agent Skills 开放标准实体页
  - 更新 [[index|Wiki 索引]] — 新增 AI 工具与编程范式分区、实体条目、资料条目
  - 重写 [[synthesis|综合论述]] — 首批内容填充，确立 Agent Skills 和渐进式加载为核心论点
- **冲突**：无
- **来源**：Bilibili 视频剪藏（元数据）+ agentskills.io/specification（完整规范）

## [2026-04-27] sync | wiki/concepts/ 文件夹重构与笔记规范重写
- **变更**：
  - programming/ → cpp/，文件名中文化（基础语法 / 面向对象 / 标准模板库 / 内存管理）
  - theory/ 拆分 → math/（Laplace变换）+ control/（物理建模 / 方框图）
  - digital/ 保留，新增 embedded/stm32/ 和 embedded/ros/ 占位目录
  - 重写 组合逻辑电路.md，补充完整 wiki frontmatter 和关联连接
  - 所有9个概念页内部链接更新到新路径
  - wiki/index.md 重建，按新结构注册所有页面
  - 模板体系扩充：新增 source.md、entity.md、comparison.md
- **冲突**：无

## [2026-04-28] ingest | DataWhale 深入浅出PyTorch 教程

- **变更**：
  - 新增 [[sources/摘要-thorough-pytorch]] — DataWhale《深入浅出PyTorch》教程摘要（课程架构、核心观点、贡献者信息）
  - 新增 [[entities/DataWhale|DataWhale]] — AI 开源学习组织实体页（愿景、代表性项目、协作方式）
  - 新增 [[concepts/programming/PyTorch|PyTorch]] — PyTorch 深度学习框架概念页（核心组件、生态工具、进阶技巧）
  - 更新 [[index|Wiki 索引]] — 新增深度学习与 PyTorch 分区、DataWhale 实体条目、摘要条目
  - 更新 [[synthesis|综合论述]] — 新增开源 AI 教育模式核心论点、新实体与概念、开放问题
- **冲突**：无
- **来源**：`raw/01-articles/datawhalechinathorough-pytorch PyTorch入门教程，在线阅读地址：httpsdatawhalechina.github.iothorough-pytorch.md`（GitHub README）

## [2026-04-28] query | 算子本质是什么
- **输出**：基于 [[算子]] + [[Laplace变换]] 综合回答，从三个层次（维度跃升、微积分→代数、算子链组合）统一阐述算子本质为「操作的代数化」
- **后续操作**：
  - 新建 [[syntheses/算子本质]] — 综合论述页，固化回答
  - 更新 [[index|Wiki 索引]] — 注册综合条目

## [2026-05-03] lint | 知识库全量健康巡检
- **结果**：22 个页面均已注册，无幽灵条目，无文件缺失，图片资源完整
- **修复（红灯）**：
  - [[entities/agentskills-io]] — 修复 `[[Anthropic]]` 死链（改为纯文本，无实体页）
- **修复（黄灯）**：
  - [[synthesis|综合论述]] — 新增「专项综合论述」区块，补充 [[syntheses/算子本质]] 引用
  - [[CLAUDE.md]] — 更新 `concepts/` 子目录规范（`cpp/`、`math/`、`control/` 取代旧 `programming/`、`theory/`）
- **冲突**：无

## [2026-05-03] sync | concepts 全面整理（学习路径 + 跨域链接）
- **变更**：
  - 所有 10 个 concepts 内容页新增 `> [!tip] 学习路径` callout（前置知识 / 本页定位 / 后续方向）
  - [[concepts/math/算子]] — 修复 `sources` 字段（错误引用了 wiki 文件，已清空）；新增 [[syntheses/算子本质]] 关联
  - [[concepts/math/Laplace变换]] — 新增 [[syntheses/算子本质]] 关联
  - [[concepts/control/物理建模]] — 新增 [[concepts/math/算子]] + [[syntheses/算子本质]] 关联
  - **跨域链接（数字电路 ↔ C++）**：
    - [[concepts/cpp/基础语法]] → 新增 [[concepts/digital/原码反码补码]]（整型底层表示）
    - [[concepts/digital/原码反码补码]] → 新增 [[concepts/cpp/基础语法]]（整数溢出原理）
    - [[concepts/digital/组合逻辑电路]] → 新增 [[concepts/cpp/基础语法]]（位运算符 ↔ 逻辑门）
  - [[index|Wiki 索引]] — 新增「🗺️ 推荐学习路线」区块（三条学习路径 + 跨域桥梁导航）
- **冲突**：无
