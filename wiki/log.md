# Wiki 操作日志

> Append-only。每条以 `## [YYYY-MM-DD] type | title` 开头，支持 grep：
> `grep "^## \[" wiki/log.md | tail -5`

## [2026-06-26] create | 方框图

- 新建 `wiki/concepts/control/方框图.md`
- 内容：基本图形元素、串联/并联/反馈三种连接、闭环传函推导、等效变换规则（相加点/分支点移动）、双回路化简例题、误差传递函数
- 更新 `wiki/index.md` 注册

## [2026-09-06] maintain | 文档结构整理

- 在 `README.md` 增加根目录文档与 Wiki 导航
- 在 `CLAUDE.md` 补充根目录文档、`index`/`meta` 类型与特殊页面说明
- 规范 `TODO.md`、`wiki/index.md`、`wiki/synthesis.md` 的内部导航链接

## [2026-09-06] maintain | Skills 重做为学习笔记工作流

- 技能集从 `ingest / query / lint` 改为 `note / query / review / lint`
  - `note`：唯一写入口，覆盖「把这次学的内容记下来」与 raw 资料摄入（原 `/ingest`）
  - `review`：新增，只读复习——自测题、复习队列、知识缺口、TODO 进度
  - `query` / `lint`：保持只读，改为索引优先检索、待写页面不再误报为死链
- 新增 `.claude/skills/_lib/`（共享库 + 索引构建）与 `.claude/cache/vault-index/` 索引缓存（已 gitignore）
- 旧 `ingest` 技能与 `resolve_wikilinks.py` 移至 `.trash/review-20260906/skills-v2/`，未删除
- 同步更新 `CLAUDE.md`、`README.md` 的技能表与操作速查；wiki 笔记内容未改，仅本日志与 `index.md` 顶部导航说明
- 经 codex（代码）与 grok（触发边界）两轮外部审查并修复：4 处崩溃、索引删除页面后不失效、代码块内标记误计、`index.md` 死链此前未被检查、四个 skill 的触发词互撞

## [2026-09-06] rewrite | 全部 16 页笔记按统一骨架重排

- 骨架：一句话定义 → 学习路径 → **直觉** → 原理与推导 → **例题** → **易错点** → 关联连接
  - 14 个 concept 页全部套用；`自动控制原理`（学习中枢）与 `摘要-锁存器与触发器`（source 类型）保留各自结构，仅对齐标题与补充易错点/待办
- **内容更正**：`逻辑函数化简` 课堂例题 $F=\bar ABC+AC+\bar AB\bar C+\bar AB+BC+AB+\bar ABC$ 的答案由 $A+B+C$ 更正为 $B+AC$
  - 原推导在「$AC+AB=A(C+B)$，再由吸收律化简为 $A$」处出错；已用完整真值表核实（$F=\Sigma m(2,3,5,6,7)$），并在页内保留错因说明
  - 该页原有的 `待验证` 标记随之解除
- `方框图`：4 段失效/占位的 TikZ 代码块替换为 `wiki/assets/bd-*.svg` 四张等效变换图（此前一直未被引用）
- C++ 四页：移除 UTF-8 BOM；标签由 `concept/编程/C++` 统一为 `cpp`；内部链接由路径式改为页面名式
- `摘要-锁存器与触发器`：补 aliases 与入链，去掉重复的 `逻辑门电路` 关联
- 每页新增「直觉」与「易错点」两节为本次编写，原有定义、公式、表格、例题、图片全部保留
- 同步更新 `wiki/index.md` 条目描述；`CLAUDE.md` 标签表登记 `#source`、`#comparison`
- 改写前快照保存在 `.trash/review-20260906/wiki-before-rewrite/`
