---
title: "摘要-thorough-pytorch"
type: source
tags:
  - source
  - deep-learning
  - pytorch
  - 教程
sources:
  - raw/01-articles/datawhalechinathorough-pytorch PyTorch入门教程，在线阅读地址：httpsdatawhalechina.github.iothorough-pytorch.md
last_updated: 2026-05-07
---

> [!important] 一句话摘要
> DataWhale 开源组织推出的《深入浅出PyTorch》系列教程，从基础到实战覆盖 PyTorch 深度学习全流程，配套 B 站视频与 Jupyter Notebook 练习。

## 核心观点

- PyTorch 是学术界最常用的深度学习框架，兼具灵活性、可读性和性能
- 学习 PyTorch 需要理论储备和动手训练并重——"两手都要抓两手都要硬"
- 课程分三阶段：基础知识（Ch1-4）、进阶操作（Ch5-8）、案例分析（Ch9+，持续更新）
- 组队学习模式：Part 1 周期 10 天，Part 2 周期 11 天
- 课程内容以 Markdown + Jupyter Notebook 形式开源在 GitHub，使用 Forking 工作流协作

## 内容架构

| 阶段 | 章节 | 内容 |
|:---|:---|:---|
| 前置 | Ch0 | AI 简史、评价指标、常用包、Jupyter |
| 基础 | Ch1-4 | 安装、张量运算、自动求导、数据读入、模型构建、损失函数、优化器、训练评估、Fashion-MNIST 实战 |
| 进阶 | Ch5-8 | 模型定义方式、模型块搭建、进阶训练技巧（自定义损失/动态学习率/微调/半精度/数据扩充）、可视化（TensorBoard/WandB/SwanLab）、生态（torchvision/torchtext/torchaudio） |
| 实战 | Ch9+ | ONNX 部署、ResNet/Swin Transformer/ViT/YOLO/LSTM 源码解读 |

## 关键实体

- [[DataWhale]] — 发起该教程的 AI 领域开源学习组织
- 核心贡献者：牛志康（西电）、李嘉骐（清华）、刘洋（中科院数学所）、陈安东（哈工大）

## 对现有知识的贡献

- **新领域**：这是 Wiki 中首个深度学习/PyTorch 相关资料，为 AI 编程工具链知识库开辟了全新分支
- **学习方法论**：教程强调"理论 + 动手"的组队学习模式，区别于纯文档型教程
- **生态全景**：覆盖了 PyTorch 从训练到部署的完整工具链（ONNX、TensorBoard、torchvision 等）

## 关联连接

- [[PyTorch]] — 核心概念页
- [[DataWhale]] — 开源组织实体
- [[摘要-agent-skills-spec]] — 同为开源社区驱动的技术标准
