# _lib：skill 共享库

不是 skill，是 `note` / `query` / `review` / `lint` 四个 skill 的公共实现，避免四份脚本各自漂移。

| 文件 | 作用 |
|:---|:---|
| `vault.py` | 页面模型、BOM 安全的 frontmatter 解析、wikilink 解析、相近页面猜测、索引缓存读写 |
| `build_index.py` | CLI：构建/刷新 `.claude/cache/vault-index/` |

## 索引缓存

`.claude/cache/vault-index/`（已 gitignore，不是笔记，不进 Obsidian 图谱）：

| 文件 | 内容 |
|:---|:---|
| `pages.tsv` | 一页一行：路径、类型、标签、标题、别名、更新日期、一句话摘要、小标题 |
| `links.tsv` | 一链接一行：来源、目标、解析状态、命中路径 |
| `stats.json` | 页数、链接统计、待写页面（谁在等它）、学科页数 |

作用是**省 token**：先在索引里定位，再只读需要的页面片段，而不是把 `wiki/` 整个读进上下文。

任何脚本调用 `vault.ensure_index(root)` 时会比对 `wiki/**.md` 与 `TODO.md`、`CLAUDE.md` 的 mtime，过期自动重建；也可手动：

```bash
python3 /home/mayon/Vaults/.claude/skills/_lib/build_index.py --root /home/mayon/Vaults [--force] [--json]
```

新增标签、页面类型或学科目录时，同步改 `vault.py` 顶部的 `PAGE_TYPES` / `KNOWN_TAGS` / `SUBJECT_DIRS`，否则 `lint` 会误报。
