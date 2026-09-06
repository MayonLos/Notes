#!/usr/bin/env python3
"""只读体检：结构、frontmatter、链接、索引登记、孤儿页、学习标记。

学习笔记语义：指向尚未写的页面的 wikilink 是**待写页面**，不是错误；
只有「与现有页面高度相似」的缺失目标才按拼写错误上报为 ERROR。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
import vault  # noqa: E402


def _check_links(page, pages, lookup, root, inbound, result, errors, warnings, planned):
    """返回 (死链, 歧义, 缺标题) 计数；特殊页与内容页共用。"""
    dead = amb = frag = 0
    for embed, target in page.links:
        info = vault.resolve_link(target, lookup, root, page)
        status = info["status"]
        if status in {"resolved", "missing-fragment"}:
            # 缺小节的链接依然构成入链，否则会把目标页误报成孤儿页
            for match in info["matches"]:
                if match in inbound and match != page.rel:
                    inbound[match] += 1
            if status == "missing-fragment":
                frag += 1
                warnings.append(f"{page.rel}: [[{target}]] 目标存在但没有该标题/块")
        elif status == "ambiguous":
            amb += 1
            warnings.append(f"{page.rel}: 链接歧义 [[{target}]] → {info['matches']}")
        else:
            if embed:
                # 嵌入的图片/附件写错就是坏了，没有「待建」一说
                errors.append(f"{page.rel}: 嵌入资源缺失 ![[{target}]]")
                dead += 1
            else:
                planned.append(f"{target} ← {page.rel}")
                close = vault.nearest(target, pages, root)
                if close:
                    # 中文短名一字之差常常是另一个概念（一阶/二阶），只提示不判错
                    warnings.append(
                        f"{page.rel}: [[{target}]] 尚未建页，与已有页面相近 {close}"
                        "——确认是打错字还是另一页")
    return dead, amb, frag


def main() -> int:
    ap = argparse.ArgumentParser(description="Vault 只读健康检查")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--stale-days", type=int, default=180, help="last_updated 超过此天数记为过期")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    result: dict[str, object] = {
        "tool": "check_vault", "root": str(root), "status": "PASS",
        "checks": {}, "errors": [], "warnings": [], "planned": [], "notes": [],
    }
    errors: list[str] = result["errors"]        # type: ignore[assignment]
    warnings: list[str] = result["warnings"]    # type: ignore[assignment]
    planned: list[str] = result["planned"]      # type: ignore[assignment]

    if not (root / "wiki").is_dir():
        errors.append("找不到 wiki/ 目录")
        emit(result, args.json)
        return 1

    for required in sorted(vault.SPECIAL_PAGES):
        if not (root / required).is_file():
            errors.append(f"缺少 {required}")

    pages = vault.load_pages(root)
    lookup = vault.build_lookup(pages)
    # 按相对路径判定特殊页：wiki/concepts/cpp/index.md 这种普通页不应被跳过
    content = [p for p in pages if not p.is_special]
    index_page = next((p for p in pages if p.rel == "wiki/index.md"), None)
    index_keys = vault.registered_keys(index_page.body) if index_page else set()
    today = dt.date.today()

    inbound = {p.rel: 0 for p in content}
    dead = amb = frag = 0
    markers = {"conflict": 0, "unverified": 0, "todo": 0}
    seen_titles: dict[str, str] = {}

    for page in pages:
        rel = page.rel
        if page.is_special:
            # 特殊页不做 schema 检查，但链接必须查
            _check_links(page, pages, lookup, root, inbound, result, errors, warnings, planned)
            continue
        if page.fm is None:
            errors.append(f"{rel}: 缺少 YAML frontmatter")
        else:
            for field in ("title", "type", "tags", "last_updated"):
                if not page.fm.get(field):
                    warnings.append(f"{rel}: frontmatter 缺少 {field}")
            if page.type and page.type not in vault.PAGE_TYPES:
                errors.append(f"{rel}: type 非法 {page.type!r}（允许 {'|'.join(sorted(vault.PAGE_TYPES))}）")
            unknown = [t for t in page.tags if t not in vault.KNOWN_TAGS]
            if unknown:
                warnings.append(f"{rel}: 未登记标签 {unknown}；确认后请补进 CLAUDE.md 标签表")

        # 学科目录与标签是否一致
        if page.subject and page.subject in vault.SUBJECT_DIRS:
            expect = {"control": {"control", "math"}, "digital": {"digital"}, "cpp": {"cpp", "embedded"}}
            if page.tags and not (set(page.tags) & expect[page.subject]):
                warnings.append(f"{rel}: 位于 {page.subject}/ 但标签为 {page.tags}，目录与标签不一致")

        if "## 关联连接" not in page.body:
            warnings.append(f"{rel}: 缺少 ## 关联连接（会产生孤岛页面）")

        if page.last_updated:
            try:
                age = (today - dt.date.fromisoformat(page.last_updated)).days
                if age > args.stale_days:
                    warnings.append(f"{rel}: last_updated {page.last_updated} 已过去 {age} 天")
            except ValueError:
                warnings.append(f"{rel}: last_updated 不是 YYYY-MM-DD：{page.last_updated!r}")

        if page.title in seen_titles and seen_titles[page.title] != rel:
            warnings.append(f"{rel}: 标题与 {seen_titles[page.title]} 重复（{page.title}）")
        seen_titles.setdefault(page.title, rel)

        counts = page.markers()
        for key in markers:
            markers[key] += counts[key]

        counters = _check_links(page, pages, lookup, root, inbound, result,
                                errors, warnings, planned)
        dead += counters[0]
        amb += counters[1]
        frag += counters[2]

        if index_page and not vault.is_registered(index_keys, page):
            warnings.append(f"{rel}: 未登记到 wiki/index.md")

    orphans = [rel for rel, count in inbound.items() if count == 0]
    for rel in orphans:
        warnings.append(f"{rel}: 没有任何入链")

    raw_pending = sum(1 for d in ("01-articles", "02-papers", "03-transcripts",
                                  "04-notes", "05-wiki-export")
                      if (root / "raw" / d).is_dir()
                      for p in (root / "raw" / d).rglob("*") if p.is_file())

    result["checks"] = {
        "pages": len(content), "dead_links": dead, "ambiguous_links": amb,
        "missing_fragments": frag, "planned_pages": len(set(planned)),
        "orphans": len(orphans), "raw_pending": raw_pending, "markers": markers,
    }
    result["notes"] = [
        f"待写页面（wikilink 已指向、页面未建）{len(set(planned))} 个——学习路线的正常状态，用 /review 查看优先级",
        f"内容标记：冲突 {markers['conflict']} / 待验证 {markers['unverified']} / 待补充 {markers['todo']}",
    ]
    result["status"] = "FAIL" if errors else ("WARN" if warnings else "PASS")
    emit(result, args.json)
    return 1 if errors else 0


def emit(result: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    checks = result.get("checks") or {}
    print(f"check_vault: {result['status']}")
    if checks:
        print(f"pages: {checks['pages']}  errors: {len(result['errors'])}  "
              f"warnings: {len(result['warnings'])}  planned: {checks['planned_pages']}")
    for item in result["errors"]:                 # type: ignore[union-attr]
        print(f"ERROR: {item}")
    warns: list[str] = result["warnings"]         # type: ignore[assignment]
    for item in warns[:40]:
        print(f"WARN: {item}")
    if len(warns) > 40:
        print(f"WARN: ... 另有 {len(warns) - 40} 条")
    for item in result["notes"]:                  # type: ignore[union-attr]
        print(f"NOTE: {item}")


if __name__ == "__main__":
    raise SystemExit(main())
