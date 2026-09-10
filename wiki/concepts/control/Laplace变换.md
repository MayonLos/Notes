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
last_updated: 2026-09-10
---

> **一句话定义**：把时域函数搬到复频域的积分变换，让微分方程变成代数方程，是整门控制理论的数学地基。

> [!tip] 学习路径
> **前置**：微积分（积分、求导）、复数
> **本页**：Laplace 变换——把微积分算子代数化
> **后续**：→ [[物理建模]]（用它求传递函数）→ [[方框图]]（传函的图形化连接）

---

## 直觉

微分方程难解，代数方程好解。Laplace 变换做的就是这一件事：

$$\text{微分方程} \xrightarrow{\ \mathcal{L}\ } \text{代数方程} \xrightarrow{\ \text{解}\ } F(s) \xrightarrow{\ \mathcal{L}^{-1}\ } f(t)$$

关键在**微分定理** $\mathcal{L}\{f'\}=sF(s)-f(0^-)$：求导这个「算子」变成了乘 $s$ 这个「数」。于是 $m\ddot x+b\dot x+kx=F$ 直接变成 $(ms^2+bs+k)X=F$，一步得到传递函数。

$s=\sigma+j\omega$ 的两部分各有含义：$\sigma$ 管衰减快慢，$\omega$ 管振荡频率。所以**极点在 $s$ 平面的位置，直接就是系统的行为**——这条对应关系是后面稳定性分析、根轨迹、频域法的共同出发点。

---

## 原理与推导

### 定义

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t)e^{-st}\,dt, \quad s = \sigma + j\omega$$

### 常用变换对

| 时域 $f(t)$               | 复频域 $F(s)$                         | 说明     |
| :---------------------- | :--------------------------------- | :----- |
| $\delta(t)$             | $1$                                | 单位脉冲   |
| $u(t)$                  | $\dfrac{1}{s}$                     | 单位阶跃   |
| $t$                     | $\dfrac{1}{s^2}$                   | 单位斜坡   |
| $e^{-at}$               | $\dfrac{1}{s+a}$                   | 指数衰减   |
| $t\,e^{-at}$            | $\dfrac{1}{(s+a)^2}$               | 重极点对应项 |
| $\sin(\omega t)$        | $\dfrac{\omega}{s^2+\omega^2}$     | 正弦     |
| $\cos(\omega t)$        | $\dfrac{s}{s^2+\omega^2}$          | 余弦     |
| $e^{-at}\sin(\omega t)$ | $\dfrac{\omega}{(s+a)^2+\omega^2}$ | 衰减正弦   |
| $e^{-at}\cos(\omega t)$ | $\dfrac{s+a}{(s+a)^2+\omega^2}$    | 衰减余弦   |

### 微分定理

$$\mathcal{L}\{f'(t)\} = sF(s) - f(0^-)$$

$$\mathcal{L}\{f^{(n)}(t)\} = s^nF(s) - s^{n-1}f(0^-) - \cdots - f^{(n-1)}(0^-)$$

> [!important] 关键用途
> 微分定理让 $\dot{x}$ 变成 $sX(s)$，这是建立传递函数的核心操作。求传函时默认**零初始条件**，初值项全部消掉。

### 积分定理

$$\mathcal{L}\left\{\int_0^t f(\tau)\,d\tau\right\} = \frac{F(s)}{s}$$

### 初值 / 终值定理

$$f(0^+) = \lim_{s \to \infty} sF(s) \qquad f(\infty) = \lim_{s \to 0} sF(s)$$

> [!warning] 两个定理都有前提，不能拿来就用
> **终值定理**要求 $sF(s)$ 的极点**全部位于开左半平面**（虚轴上、右半平面都不行）；**初值定理**要求 $F(s)$ 严格真、原点处不含冲激项。详见下方「易错点」一节。

### 卷积定理

$$\mathcal{L}\{f_1(t) * f_2(t)\} = F_1(s) \cdot F_2(s)$$

时域卷积 ↔ 复频域相乘。串联环节传函直接相乘，根就在这里。

### 时移定理（延迟定理）

$$\mathcal{L}\{f(t-a)\,u(t-a)\} = e^{-as}F(s), \quad a \geq 0$$

时域延迟 $a$ 秒 ↔ 复频域乘 $e^{-as}$（纯相位因子，幅值不变）。含纯延迟的系统（传输延迟、采样延迟）传函里的 $e^{-\tau s}$ 就是它。

### 频移定理（s 域平移）

$$\mathcal{L}\{e^{at}f(t)\} = F(s-a)$$

时域乘 $e^{at}$ ↔ $s$ 域整体平移，极点右移 $a$。配合正余弦变换对，直接得到衰减正弦/余弦：

$$e^{-at}\sin\omega t \;\longleftrightarrow\; \frac{\omega}{(s+a)^2+\omega^2}$$

### 逆变换：留数法

> [!important] 核心公式
> 逆变换本质是对所有极点求留数之和：
> $$f(t) = \sum_{i} \operatorname{Res}\!\left[F(s)\,e^{st},\; s_i\right], \quad t > 0$$

**物理含义**：每个极点对应系统的一个「模态」，留数决定该模态的幅度。

**情形一 · 单极点**

$$\operatorname{Res}[F(s)e^{st},\; p_i] = \lim_{s \to p_i}(s - p_i)\,F(s)\,e^{st} = k_i\,e^{p_i t}$$

系数 $k_i$ 用「挖去法」：令 $s = p_i$ 代入，去掉对应因子。

**情形二 · 重极点**（$s = p$ 为 $m$ 阶重根）

$$F(s) = \frac{b_1}{s-p} + \frac{b_2}{(s-p)^2} + \cdots + \frac{b_m}{(s-p)^m} + \cdots$$

系数由逐阶求导确定（$k = 1, \ldots, m$）：

$$b_k = \frac{1}{(m-k)!}\lim_{s \to p}\frac{d^{m-k}}{ds^{m-k}}\!\left[(s-p)^m F(s)\right]$$

**情形三 · 共轭复极点**（$s_{1,2} = -\alpha \pm j\beta$）

配凑成标准型再查表：

$$\frac{Bs+C}{(s+\alpha)^2+\beta^2} = \underbrace{\frac{B(s+\alpha)}{(s+\alpha)^2+\beta^2}}_{\longleftrightarrow\; B\,e^{-\alpha t}\cos\beta t} + \underbrace{\frac{C-B\alpha}{\beta}\cdot\frac{\beta}{(s+\alpha)^2+\beta^2}}_{\longleftrightarrow\; \frac{C-B\alpha}{\beta}\,e^{-\alpha t}\sin\beta t}$$

### 极点位置 → 时域行为速查

| 极点位置 | 时域响应 |
|:--------|:--------|
| 负实轴 $s=-a$ | 单调衰减 $e^{-at}$ |
| 负实轴二阶重根 | 先升后降 $t\,e^{-at}$ |
| 左半平面共轭 $-\alpha\pm j\beta$ | 衰减振荡 $e^{-\alpha t}\cos(\beta t+\phi)$ |
| 虚轴 $\pm j\beta$ | 等幅振荡（临界稳定）|
| 右半平面 | 发散（不稳定）|

---

## 例题

### 例 1 · 单极点

$$F(s) = \dfrac{2}{(s+1)(s+3)}$$

$$k_1 = \frac{2}{s+3}\bigg|_{s=-1} = 1, \qquad k_2 = \frac{2}{s+1}\bigg|_{s=-3} = -1$$

$$\boxed{f(t) = e^{-t} - e^{-3t}}$$

### 例 2 · 重极点

$$F(s) = \dfrac{1}{s\,(s+1)^2}, \quad \text{极点 } s=0\ (\text{一阶}),\ s=-1\ (\text{二阶})$$

$$A = \frac{1}{(s+1)^2}\bigg|_{s=0} = 1$$

$$B_2 = \frac{1}{s}\bigg|_{s=-1} = -1, \qquad B_1 = \frac{d}{ds}\!\left[\frac{1}{s}\right]_{s=-1} = -\frac{1}{s^2}\bigg|_{s=-1} = -1$$

$$F(s) = \frac{1}{s} - \frac{1}{s+1} - \frac{1}{(s+1)^2}$$

$$\boxed{f(t) = 1 - e^{-t} - t\,e^{-t} = 1 - (1+t)\,e^{-t}}$$

> [!tip] 自检
> $t=0$ 时 $f(0)=0$，与 $F(s)$ 分子次数低于分母一致 ✓

### 例 3 · 共轭复极点

$$F(s) = \dfrac{5}{s\,(s^2+4s+5)}, \quad \text{共轭极点 } s_{1,2} = -2 \pm j$$

单极点 $s=0$：$A = \dfrac{5}{5} = 1$

比较系数：$F(s) = \dfrac{1}{s} + \dfrac{Bs+C}{s^2+4s+5}$，解得 $B=-1,\;C=-4$

$$\frac{-s-4}{(s+2)^2+1} = -\frac{s+2}{(s+2)^2+1} - \frac{2}{(s+2)^2+1}$$

$$\boxed{f(t) = 1 - e^{-2t}(\cos t + 2\sin t) = 1 - \sqrt{5}\,e^{-2t}\cos(t - \arctan 2)}$$

---

## 易错点

> [!warning] 终值定理的适用条件
> $f(\infty)=\lim_{s\to0}sF(s)$ 只在 $sF(s)$ 的极点**全在左半平面**时成立。含虚轴极点（等幅振荡）或右半平面极点时，公式会算出一个数，但这个数没有意义。做题前先看极点，别直接代。

> [!warning] 时移 vs 频移，方向相反
> - 时移：**时域**平移 → **复频域**乘 $e^{-as}$
> - 频移：**时域**乘 $e^{at}$ → **复频域**平移 $F(s-a)$
>
> 记「谁平移，另一边就乘指数」，两个定理不会混。

> [!warning] 微分定理漏初值
> $\mathcal{L}\{f'\}=sF(s)-f(0^-)$ 的初值项只有在**零初始条件**下才能丢。求传递函数可以丢；解带初值的微分方程时丢了就错。

> [!warning] 重极点求导阶数搞反
> $b_k=\frac{1}{(m-k)!}\frac{d^{m-k}}{ds^{m-k}}[\cdot]$：**最高阶系数 $b_m$ 不用求导**（$k=m$ 时导数阶为 0），越往低阶求导次数越多。写反了整题作废。

> [!warning] 共轭极点配方后漏掉 $\cos$ 项的偏移
> $\frac{Bs+C}{(s+\alpha)^2+\beta^2}$ 必须先把分子凑成 $B(s+\alpha)$ 再补差额，不能直接把 $Bs$ 当作 $\cos$ 项的系数——差的那 $B\alpha$ 要并进 $\sin$ 项。

---

## 关联连接

- [[物理建模]] — 后续：用微分定理把物理方程变成传递函数
- [[方框图]] — 后续：卷积定理是串联环节传函相乘的依据
- [[自动控制原理]] — 上级：自控课程学习中枢
