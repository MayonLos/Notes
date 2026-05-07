---
title: "PyTorch"
type: concept
tags:
  - concept
  - ai
  - 框架
aliases:
  - pytorch
  - torch
  - PyTorch框架
sources:
  - raw/01-articles/datawhalechinathorough-pytorch PyTorch入门教程，在线阅读地址：httpsdatawhalechina.github.iothorough-pytorch.md
last_updated: 2026-05-07
---

> **一句话定义**：PyTorch 是 Meta（原 Facebook）开源的深度学习框架，以动态计算图、Pythonic API 和灵活调试能力著称，是当前学术界实现深度学习算法最常用的工具。

## 详细说明

PyTorch 在**灵活性、可读性和性能**三方面具备显著优势，其核心设计理念是"定义即运行"（Define-by-Run），计算图随代码执行动态构建，这使得调试直观且易于理解。

### 核心组件

| 组件 | 说明 |
|:---|:---|
| **张量（Tensor）** | 多维数组，PyTorch 的基本数据结构，支持 GPU 加速运算 |
| **自动求导（Autograd）** | 自动计算梯度，反向传播的核心引擎 |
| **nn.Module** | 模型构建基类，支持模块化搭建复杂网络 |
| **损失函数（Loss）** | 衡量预测与真实值的差距（CrossEntropy、MSE 等） |
| **优化器（Optimizer）** | 参数更新策略（SGD、Adam 等） |
| **DataLoader** | 批量数据加载与预处理管道 |
| **CUDA / cuDNN** | GPU 并行计算加速 |

### 完整深度学习流程

```
数据读入 → 模型构建 → 前向传播 → 损失计算 → 反向传播 → 参数更新 → 评估与可视化
```

## 生态工具

| 工具 | 用途 |
|:---|:---|
| torchvision | 图像处理（数据集、预训练模型、图像变换） |
| torchtext | 文本处理 |
| torchaudio | 音频处理 |
| TensorBoard / WandB / SwanLab | 训练过程可视化 |
| ONNX | 模型导出与跨平台部署 |

## 进阶技巧

- **自定义损失函数**：当标准损失不满足需求时，继承 `nn.Module` 自行实现
- **动态学习率调整**：训练过程中根据 epoch 或指标调整学习率
- **模型微调（Fine-tuning）**：基于预训练模型进行迁移学习
- **半精度训练**：使用 FP16 加速训练、减少显存占用
- **数据扩充（Data Augmentation）**：通过变换增加训练数据多样性

## 与其他概念的关系

- [[API兼容性策略]] — PyTorch 和 TensorFlow/JAX 之间的框架选择本质上是 API 生态的选择
- CUDA — PyTorch 的 GPU 加速依赖 NVIDIA CUDA 平台

## 关联连接

- [[摘要-thorough-pytorch]] — 系统学习资料
- [[DataWhale]] — 维护该教程的开源组织
