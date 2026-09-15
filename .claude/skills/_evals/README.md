# 四个 skill 的触发边界评测

`note` / `query` / `review` / `lint` 职责互斥，边界靠 `description` 区分。
这里放的是验证边界是否真的分得开的评测集与脚本。

## 为什么不用 skill-creator 的 run_eval.py

那个脚本把待测 skill 注册成 `.claude/commands/` 下的**临时 slash command** 来检测触发。
在本仓库这种 **skill 已经装好**的项目里，模型会直接走真正的 skill，临时 command 永远抢不到，
于是**恒为零触发**——而它的记分方式会让"全不触发"在 negative 占多数的评测集上得到一个很高的
假分数（实测 19/24 "passed"，实际触发次数合计为 0）。

它还会在项目里留下 `.claude/commands/*-skill-*.md`，中断时不清理。

## 这里的做法

直接测真实触发：在一个只软链 `.claude/` 与 `CLAUDE.md` 的临时目录里跑 `claude -p`，
看它第一个选中的是哪个 skill。这样一次就能测出**四个 skill 相互竞争**的结果，
而不是四次单独的二元判断。

```bash
T=/tmp/skilltest && rm -rf $T && mkdir -p $T
ln -s /home/mayon/Vaults/.claude $T/.claude
ln -s /home/mayon/Vaults/CLAUDE.md $T/CLAUDE.md
cd $T && python3 /home/mayon/Vaults/.claude/skills/_evals/probe_triggers.py
```

`--disallowedTools Write,Edit,NotebookEdit,Bash,Task` 是必须的：
`note` 真触发起来会写文件，测触发不该产生副作用。

## 文件

| 文件 | 说明 |
|:---|:---|
| `queries.json` | 24 条查询，每条标注 `owner`（应归哪个 skill，`none` = 四个都不该触发）|
| `probe_triggers.py` | 批量探测脚本 |
| `real-trigger.json` | 最近一次结果 |

查询是按**边界模糊**来设计的，不是清晰样本——例如「我到底记过换相重叠没有」（像 review 实为 query）、
「TODO 上数电标了 17 条完成，跟实际笔记对得上吗」（像 lint 实为 review）、
「我怀疑几页 frontmatter 漏了字段」（像 query 实为 lint）。清晰样本测不出边界问题。

## 2026-09-13 结果：24/24

四类各 5 条全部命中，4 条纯答疑/做题（`none`）全部正确地没有触发任何 skill。
**结论：description 边界已经足够清晰，不需要跑优化循环。**

> 批量并发跑时有一条会因判定逻辑失真显示 `(直接用工具)`，单独复测 3/3 正确。
> 脚本按「同一条 assistant 消息里 Skill 之前出现过别的工具」判负，模型偶尔先 Glob 一下就会误伤。
