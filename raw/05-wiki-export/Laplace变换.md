---
title: "Laplace变换"
type: concept
tags:
  - concept
  - 数学
  - 控制理论
aliases:
  - 拉普拉斯变换
  - Laplace Transform
  - 复频域分析
sources: []
last_updated: 2026-04-27
---

> **一句话定义**：将时域函数转化为复频域的积分变换，把微分方程变成代数方程，是控制系统分析的数学基础。

> [!tip] 学习路径
> **前置**：[[concepts/math/算子|算子]]（理解"把运算本身当符号操作"的思维）
> **本页**：Laplace 变换——将微积分算子代数化的核心工具
> **后续**：→ [[concepts/control/物理建模|物理建模]]（用 Laplace 建立传递函数）→ [[concepts/control/方框图|方框图]]（传递函数的图形化组合）

## 定义

对于函数 $f(t)$（$t \geq 0$），拉普拉斯变换定义为：

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t)e^{-st}\,dt$$

其中 $s = \sigma + j\omega$ 为复变量。

## 核心意义

- **化微分为代数**：将微分方程转化为代数方程，大幅简化求解
- **传递函数**：直接得到系统的 $G(s) = \frac{Y(s)}{U(s)}$
- **稳定性分析**：通过极点位置判断系统稳定性
- **频率特性**：令 $s = j\omega$ 即可分析频率响应

## 常用变换对

| 时域 $f(t)$ | 复频域 $F(s)$ | 说明 |
|:---|:---|:---|
| $\delta(t)$ | $1$ | 单位脉冲 |
| $u(t)$ | $\dfrac{1}{s}$ | 单位阶跃 |
| $t$ | $\dfrac{1}{s^2}$ | 单位斜坡 |
| $e^{-at}$ | $\dfrac{1}{s+a}$ | 指数衰减 |
| $\sin(\omega t)$ | $\dfrac{\omega}{s^2+\omega^2}$ | 正弦 |
| $\cos(\omega t)$ | $\dfrac{s}{s^2+\omega^2}$ | 余弦 |

## 重要定理

### 微分定理

$$\mathcal{L}\{f'(t)\} = sF(s) - f(0^-)$$

$$\mathcal{L}\{f''(t)\} = s^2F(s) - sf(0^-) - f'(0^-)$$

> [!important] 关键用途
> 微分定理让微分项 $\dot{x}$ 变成 $sX(s)$，这是建立传递函数的核心操作。

### 积分定理

$$\mathcal{L}\left\{\int_0^t f(\tau)\,d\tau\right\} = \frac{F(s)}{s}$$

### 初值 / 终值定理

$$f(0^+) = \lim_{s \to \infty} sF(s) \qquad f(\infty) = \lim_{s \to 0} sF(s)$$

> [!warning] 易错点
> 初值取 $t \to 0^-$ 的极限，而非简单的 $f(0)$。终值定理要求极点全在左半平面，否则结果无效。

### 卷积定理

$$\mathcal{L}\{f_1(t) * f_2(t)\} = F_1(s) \cdot F_2(s)$$

## 定理推导与统一原理

> 所有定理都从同一个**定义**出发，**核心工具只有一个：分部积分法**。

### 微分定理的推导

$$\mathcal{L}\{f'(t)\} = \int_0^{\infty} f'(t)\,e^{-st}\,dt$$

设 $u = e^{-st}$，$dv = f'(t)\,dt$，则 $du = -s e^{-st}dt$，$v = f(t)$：

$$\begin{aligned} \mathcal{L}\{f'(t)\} &= \left[ f(t)e^{-st} \right]_0^{\infty} - \int_0^{\infty} f(t)(-s e^{-st})\,dt \\ &= (0 - f(0^-)) + s\int_0^{\infty} f(t)e^{-st}\,dt \\ &= sF(s) - f(0^-) \end{aligned}$$

**高阶推广**（重复应用分部积分）：

$$\mathcal{L}\{f^{(n)}(t)\} = s^nF(s) - s^{n-1}f(0^-) - s^{n-2}f'(0^-) - \cdots - f^{(n-1)}(0^-)$$

### 积分定理的推导

设 $g(t) = \int_0^t f(\tau)\,d\tau$，则 $g'(t) = f(t)$ 且 $g(0) = 0$。直接用微分定理反向：

$$\mathcal{L}\{f(t)\} = \mathcal{L}\{g'(t)\} = sG(s) - g(0) = sG(s)$$

$$\therefore \boxed{\mathcal{L}\left\{\int_0^t f(\tau)d\tau\right\} = \frac{F(s)}{s}}$$

### 卷积定理的推导

$$\mathcal{L}\{f(t) * g(t)\} = \int_0^\infty \left[\int_0^t f(\tau)g(t-\tau)\,d\tau\right] e^{-st}\,dt$$

交换积分次序（Fubini 定理），令 $u = t-\tau$：

$$= \int_0^\infty f(\tau) \left[\int_\tau^\infty g(t-\tau)e^{-st}\,dt\right] d\tau = \int_0^\infty f(\tau)e^{-s\tau} \left[\int_0^\infty g(u)e^{-su}\,du\right] d\tau = F(s) \cdot G(s)$$

### 🔑 统一原理：算子视角

从 [[concepts/math/算子|算子]] 的视角看，Laplace 变换的核心价值是**它将时域的微积分算子转化为复频域的代数运算**：

$$
\frac{d}{dt} \xrightarrow{\mathcal{L}} s \qquad\qquad \int_0^t \xrightarrow{\mathcal{L}} \frac{1}{s}
$$

| 时域（算子运算） | 复频域（代数运算） |
|:---|:---|
| 微分 $\dfrac{d}{dt}$ | **乘以 $s$**（减初始条件） |
| 积分 $\int_0^t$ | **除以 $s$** |
| 卷积 $f * g$ | **乘积** $F(s) \cdot G(s)$ |
| 时移 $f(t-a)$ | **乘以** $e^{-as}$ |
| 频移 $e^{at}f(t)$ | **平移** $F(s-a)$ |

本质原因：$e^{-st}$ 对 $t$ 的导数为 $-s e^{-st}$，所以每次分部积分都会"提取"出一个 $s$ 因子。

> [!important] 核心洞察
> **微分定理是最根本的一条**——积分定理是它的反向，卷积定理通过积分次序交换证明，初值/终值定理是 $s \to \infty$ 或 $s \to 0$ 时的极限推论。整个 Laplace 定理体系可以看作微分定理在不同方向上的展开。

## 拉普拉斯逆变换

实际应用中常用**部分分式展开法**：

将 $F(s) = \dfrac{B(s)}{A(s)} = \sum_i \dfrac{k_i}{s - p_i}$ 分解，其中 $p_i$ 为极点，再逐项查变换对表。

## 关联连接

- [[concepts/math/算子|算子]] — 算子概念：Laplace 变换将微积分算子转化为代数运算
- [[concepts/control/物理建模|控制系统-物理建模]] — 物理系统建模需要拉普拉斯变换求传递函数
- [[concepts/control/方框图|控制系统-方框图]] — 框图化简中广泛使用拉普拉斯变换
- [[syntheses/算子本质|算子本质（综合论述）]] — 算子视角下 Laplace 变换的深层意义
