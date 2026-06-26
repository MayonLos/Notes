---
title: "Laplace变换"
type: concept
tags:
  - math
  - control
aliases:
  - 拉普拉斯变换
  - Laplace Transform
  - 复频域分析
sources: []
last_updated: 2026-06-22
---

> **一句话定义**：将时域函数转化为复频域的积分变换，把微分方程变成代数方程，是控制系统分析的数学基础。

> [!tip] 学习路径
> **前置**：[[算子]]（理解"把运算本身当符号操作"的思维）
> **本页**：Laplace 变换——将微积分算子代数化的核心工具
> **后续**：→ [[物理建模]]（用 Laplace 建立传递函数）

## 定义

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t)e^{-st}\,dt, \quad s = \sigma + j\omega$$

## 核心意义

| 用途 | 说明 |
|:-----|:-----|
| 化微分为代数 | 微分方程 → 代数方程，大幅简化求解 |
| 传递函数 | 直接得到 $G(s) = Y(s)/U(s)$ |
| 稳定性分析 | 通过极点位置判断系统稳定性 |
| 频率特性 | 令 $s = j\omega$ 即可分析频率响应 |

## 常用变换对

| 时域 $f(t)$ | 复频域 $F(s)$ | 说明 |
|:---|:---|:---|
| $\delta(t)$ | $1$ | 单位脉冲 |
| $u(t)$ | $\dfrac{1}{s}$ | 单位阶跃 |
| $t$ | $\dfrac{1}{s^2}$ | 单位斜坡 |
| $e^{-at}$ | $\dfrac{1}{s+a}$ | 指数衰减 |
| $t\,e^{-at}$ | $\dfrac{1}{(s+a)^2}$ | 重极点对应项 |
| $\sin(\omega t)$ | $\dfrac{\omega}{s^2+\omega^2}$ | 正弦 |
| $\cos(\omega t)$ | $\dfrac{s}{s^2+\omega^2}$ | 余弦 |
| $e^{-at}\sin(\omega t)$ | $\dfrac{\omega}{(s+a)^2+\omega^2}$ | 衰减正弦 |
| $e^{-at}\cos(\omega t)$ | $\dfrac{s+a}{(s+a)^2+\omega^2}$ | 衰减余弦 |

## 重要定理

### 微分定理

$$\mathcal{L}\{f'(t)\} = sF(s) - f(0^-)$$

$$\mathcal{L}\{f^{(n)}(t)\} = s^nF(s) - s^{n-1}f(0^-) - \cdots - f^{(n-1)}(0^-)$$

> [!important] 关键用途
> 微分定理让微分项 $\dot{x}$ 变成 $sX(s)$，这是建立传递函数的核心操作。

### 积分定理

$$\mathcal{L}\left\{\int_0^t f(\tau)\,d\tau\right\} = \frac{F(s)}{s}$$

### 初值 / 终值定理

$$f(0^+) = \lim_{s \to \infty} sF(s) \qquad f(\infty) = \lim_{s \to 0} sF(s)$$

> [!warning] 易错点
> 终值定理要求极点**全在左半平面**，否则结果无效（如含振荡项时不可用）。

### 卷积定理

$$\mathcal{L}\{f_1(t) * f_2(t)\} = F_1(s) \cdot F_2(s)$$

### 算子视角总结

| 时域运算 | 复频域等价 |
|:---------|:----------|
| 微分 $\frac{d}{dt}$ | 乘以 $s$（减初始条件）|
| 积分 $\int_0^t$ | 除以 $s$ |
| 卷积 $f_1 * f_2$ | 乘积 $F_1(s)\cdot F_2(s)$ |
| 时移 $f(t-a)$ | 乘以 $e^{-as}$ |
| 频移 $e^{at}f(t)$ | 平移 $F(s-a)$ |

## 留数定理求逆变换

> [!important] 核心公式
> 逆变换本质是对所有极点求留数之和：
> $$f(t) = \sum_{i} \operatorname{Res}\!\left[F(s)\,e^{st},\; s_i\right], \quad t > 0$$

**留数的物理含义**：每个极点对应系统的一个"模态"，留数决定该模态的幅度。

### 情形一：单极点

$$\operatorname{Res}[F(s)e^{st},\; p_i] = \lim_{s \to p_i}(s - p_i)\,F(s)\,e^{st} = k_i\,e^{p_i t}$$

系数 $k_i$ 用"挖去法"：直接令 $s = p_i$ 代入去掉对应因子。

> **例**：$F(s) = \dfrac{2}{(s+1)(s+3)}$
>
> $$k_1 = \frac{2}{s+3}\bigg|_{s=-1} = 1, \qquad k_2 = \frac{2}{s+1}\bigg|_{s=-3} = -1$$
>
> $$\boxed{f(t) = e^{-t} - e^{-3t}}$$

### 情形二：重极点

$s = p$ 为 $m$ 阶重根，展开为：

$$F(s) = \frac{b_1}{s-p} + \frac{b_2}{(s-p)^2} + \cdots + \frac{b_m}{(s-p)^m} + \cdots$$

系数由**逐阶求导**确定（$k = 1, \ldots, m$）：

$$b_k = \frac{1}{(m-k)!}\lim_{s \to p}\frac{d^{m-k}}{ds^{m-k}}\!\left[(s-p)^m F(s)\right]$$

> **例**：$F(s) = \dfrac{1}{s\,(s+1)^2}$，极点 $s=0$（一阶），$s=-1$（二阶）
>
> $$A = \frac{1}{(s+1)^2}\bigg|_{s=0} = 1$$
>
> $$B_2 = \frac{1}{s}\bigg|_{s=-1} = -1, \qquad B_1 = \frac{d}{ds}\!\left[\frac{1}{s}\right]_{s=-1} = -\frac{1}{s^2}\bigg|_{s=-1} = -1$$
>
> $$F(s) = \frac{1}{s} - \frac{1}{s+1} - \frac{1}{(s+1)^2}$$
>
> $$\boxed{f(t) = 1 - e^{-t} - t\,e^{-t} = 1 - (1+t)\,e^{-t}}$$

> [!tip] 验证：$t=0$ 时 $f(0)=0$，与 $F(s)$ 分子次数低于分母一致 ✓

### 情形三：共轭复极点

极点 $s_{1,2} = -\alpha \pm j\beta$ 的贡献以共轭对形式出现，配凑为标准型：

$$\frac{Bs+C}{(s+\alpha)^2+\beta^2} = \underbrace{\frac{B(s+\alpha)}{(s+\alpha)^2+\beta^2}}_{\longleftrightarrow\; B\,e^{-\alpha t}\cos\beta t} + \underbrace{\frac{C-B\alpha}{\beta}\cdot\frac{\beta}{(s+\alpha)^2+\beta^2}}_{\longleftrightarrow\; \frac{C-B\alpha}{\beta}\,e^{-\alpha t}\sin\beta t}$$

> **例**：$F(s) = \dfrac{5}{s\,(s^2+4s+5)}$，共轭极点 $s_{1,2} = -2 \pm j$
>
> 单极点 $s=0$：$A = \dfrac{5}{5} = 1$
>
> 比较系数求共轭项：$F(s) = \dfrac{1}{s} + \dfrac{Bs+C}{s^2+4s+5}$，解得 $B=-1,\;C=-4$
>
> $$\frac{-s-4}{(s+2)^2+1} = -\frac{s+2}{(s+2)^2+1} - \frac{2}{(s+2)^2+1}$$
>
> $$\boxed{f(t) = 1 - e^{-2t}(\cos t + 2\sin t) = 1 - \sqrt{5}\,e^{-2t}\cos(t - \arctan 2)}$$

> [!tip] 极点位置速查
> | 极点位置 | 时域响应 |
> |:--------|:--------|
> | 负实轴 $s=-a$ | 单调衰减 $e^{-at}$ |
> | 负实轴二阶重根 | 先升后降 $t\,e^{-at}$ |
> | 左半平面共轭 $-\alpha\pm j\beta$ | 衰减振荡 $e^{-\alpha t}\cos(\beta t+\phi)$ |
> | 虚轴 $\pm j\beta$ | 等幅振荡（临界稳定）|
> | 右半平面 | 发散（不稳定）|

## 关联连接

- [[算子]] — 算子概念：Laplace 变换将微积分算子转化为代数运算
- [[算子本质]] — 算子视角下 Laplace 变换的深层意义
- [[物理建模]] — 物理系统建模需要拉普拉斯变换求传递函数
- [[方框图]] — 框图化简中广泛使用拉普拉斯变换
- [[自动控制原理]] — 自控课程学习中枢
