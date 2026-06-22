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
> **后续**：→ [[物理建模]]（用 Laplace 建立传递函数）→ [[方框图]]（传递函数的图形化组合）

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

### 统一原理：算子视角

从 [[算子]] 的视角看，Laplace 变换的核心价值是**它将时域的微积分算子转化为复频域的代数运算**：

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

---

## 留数定理求逆变换

> [!important] 核心公式
> 逆变换本质是对所有极点求留数之和：
> $$f(t) = \sum_{i} \operatorname{Res}\!\left[F(s)\,e^{st},\; s_i\right], \quad t > 0$$

**留数的物理含义**：每个极点 $s_i$ 对应系统的一个"模态"，留数决定该模态的幅度。

---

### 情形一：单极点（互不相同的实极点）

若极点 $s = p_i$ 为一阶，则：

$$\operatorname{Res}[F(s)e^{st},\; p_i] = \lim_{s \to p_i}(s - p_i)\,F(s)\,e^{st} = k_i\,e^{p_i t}$$

其中 $k_i = \lim_{s \to p_i}(s-p_i)F(s)$ 即部分分式系数（可直接"挖去"极点代入）。

> **例**：求 $F(s) = \dfrac{2}{(s+1)(s+3)}$ 的逆变换
>
> 极点：$p_1 = -1$，$p_2 = -3$
>
> $$k_1 = (s+1)\cdot\frac{2}{(s+1)(s+3)}\bigg|_{s=-1} = \frac{2}{-1+3} = 1$$
>
> $$k_2 = (s+3)\cdot\frac{2}{(s+1)(s+3)}\bigg|_{s=-3} = \frac{2}{-3+1} = -1$$
>
> $$\boxed{f(t) = e^{-t} - e^{-3t}}$$

---

### 情形二：重极点

若极点 $s = p$ 为 $m$ 阶重根，部分分式展开为：

$$F(s) = \frac{b_1}{s-p} + \frac{b_2}{(s-p)^2} + \cdots + \frac{b_m}{(s-p)^m} + \cdots$$

各系数由**逐阶求导**确定：

$$b_k = \frac{1}{(m-k)!}\lim_{s \to p}\frac{d^{m-k}}{ds^{m-k}}\!\left[(s-p)^m F(s)\right], \quad k = 1,2,\ldots,m$$

对应时域项（查变换对表）：

$$\frac{1}{(s-p)^k} \;\longleftrightarrow\; \frac{t^{k-1}}{(k-1)!}\,e^{pt}$$

> **例**：求 $F(s) = \dfrac{1}{s\,(s+1)^2}$ 的逆变换
>
> 极点：$s=0$（一阶），$s=-1$（二阶）
>
> 展开为：$\dfrac{A}{s} + \dfrac{B_1}{s+1} + \dfrac{B_2}{(s+1)^2}$
>
> $$A = \left.\frac{1}{(s+1)^2}\right|_{s=0} = 1$$
>
> $$B_2 = \left.\frac{1}{s}\right|_{s=-1} = -1$$
>
> $$B_1 = \frac{d}{ds}\!\left[\frac{1}{s}\right]_{s=-1} = \left.\left(-\frac{1}{s^2}\right)\right|_{s=-1} = -1$$
>
> 所以：
> $$F(s) = \frac{1}{s} - \frac{1}{s+1} - \frac{1}{(s+1)^2}$$
>
> $$\boxed{f(t) = 1 - e^{-t} - t\,e^{-t} = 1 - (1+t)\,e^{-t}}$$

> [!tip] 验证技巧
> $t=0$ 时 $f(0) = 1-(1+0) = 0$，而 $F(s)$ 分子次数低于分母，故 $f(0^+)=0$ ✓

---

### 情形三：共轭复数极点

若极点为 $s_{1,2} = -\alpha \pm j\beta$（$\alpha,\beta > 0$），留数必以共轭对出现。

**方法A（配凑标准型）**：将二阶因子拆成 $\cos$ 和 $\sin$ 两项：

$$\frac{Bs+C}{(s+\alpha)^2+\beta^2} = \frac{B(s+\alpha)}{(s+\alpha)^2+\beta^2} + \frac{C - B\alpha}{\beta}\cdot\frac{\beta}{(s+\alpha)^2+\beta^2}$$

$$\longleftrightarrow\; B\,e^{-\alpha t}\cos\beta t + \frac{C-B\alpha}{\beta}\,e^{-\alpha t}\sin\beta t$$

**方法B（留数公式）**：只算 $s = -\alpha + j\beta$ 处的留数 $A_1$，然后取实部：

$$\text{共轭对的时域贡献} = 2\,\operatorname{Re}\!\left[A_1\,e^{(-\alpha+j\beta)t}\right]$$

> **例**：求 $F(s) = \dfrac{5}{s\,(s^2+4s+5)}$ 的逆变换
>
> 分母因式：$s^2+4s+5 = (s+2)^2 + 1^2$，共轭极点 $s_{1,2} = -2 \pm j$
>
> **单极点** $s=0$：
> $$A = \frac{5}{0+0+5} = 1$$
>
> **共轭项**（配凑法）：
> $$F(s) = \frac{1}{s} + \frac{Bs+C}{s^2+4s+5}$$
>
> 恒等比较系数（两边乘以 $s(s^2+4s+5)$）：
> $$5 = (s^2+4s+5) + s(Bs+C) \implies B=-1,\; C=-4$$
>
> $$\frac{-s-4}{(s+2)^2+1} = -\frac{(s+2)}{(s+2)^2+1} - \frac{2 \cdot 1}{(s+2)^2+1}$$
>
> 逐项查表：
>
> $$\boxed{f(t) = 1 - e^{-2t}\cos t - 2\,e^{-2t}\sin t = 1 - e^{-2t}(\cos t + 2\sin t)}$$
>
> 也可合并为单一余弦：$f(t) = 1 - \sqrt{5}\,e^{-2t}\cos(t - \arctan 2)$

> [!tip] 极点位置与响应形状
> | 极点位置 | 时域响应 |
> |:--------|:--------|
> | 负实轴 $s = -a$ | 单调衰减 $e^{-at}$ |
> | 负实轴重根 $s = -a$（二阶）| $t\,e^{-at}$，先升后降 |
> | 左半平面共轭 $s = -\alpha \pm j\beta$ | 衰减振荡 $e^{-\alpha t}\cos(\beta t+\phi)$ |
> | 虚轴 $s = \pm j\beta$ | 等幅振荡（临界稳定）|
> | 右半平面 | 发散（不稳定）|

---

## 关联连接

- [[算子]] — 算子概念：Laplace 变换将微积分算子转化为代数运算
- [[物理建模]] — 物理系统建模需要拉普拉斯变换求传递函数
- [[方框图]] — 框图化简中广泛使用拉普拉斯变换
- [[算子本质]] — 算子视角下 Laplace 变换的深层意义
