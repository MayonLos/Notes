#!/usr/bin/env python3
"""只读检索：先查索引再读页面，避免整库通读。

  --search 关键词         在标题/别名/标签/摘要/小标题里排序检索（默认，最省 token）
  --grep 正则             需要正文证据时再做全文检索，只回上下文行
  --outline PAGE          只列小标题与行号，用来决定读哪一段
  --neighbors PAGE        列出出链/入链，供有节制地跳转
  --resolve 目标          解析单个 [[wikilink]]
  --list [--subject cpp]  页面清单
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
import vault  # noqa: E402


def show(value: str) -> str:
    """索引里的列表用 US 分隔存储，给人看时换回逗号。"""
    return value.replace(vault.LIST_SEP, ",")


def score(row: dict[str, str], terms: list[str]) -> int:
    total = 0
    for term in terms:
        t = term.casefold()
        if t in row["title"].casefold():
            total += 10
        if any(t in a.casefold() for a in row["aliases"].split(vault.LIST_SEP) if a):
            total += 8
        if any(t == tag.casefold() for tag in row["tags"].split(vault.LIST_SEP) if tag):
            total += 6
        if t in row["headings"].casefold():
            total += 4
        if t in row["summary"].casefold():
            total += 3
        if t in row["path"].casefold():
            total += 2
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="Vault 只读检索（索引优先）")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--search", nargs="+", help="关键词（可多个）")
    ap.add_argument("--grep", help="正文正则检索")
    ap.add_argument("--outline", help="列出该页小标题")
    ap.add_argument("--neighbors", help="列出该页出链与入链")
    ap.add_argument("--resolve", help="解析单个 wikilink 目标")
    ap.add_argument("--list", action="store_true", help="页面清单")
    ap.add_argument("--subject", choices=sorted(vault.SUBJECT_DIRS), help="限定学科")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    if not (root / "wiki").is_dir():
        print("lookup: FAIL — 找不到 wiki/", file=sys.stderr)
        return 1
    rows = vault.load_index_rows(root)
    if args.subject:
        rows = [r for r in rows if f"/concepts/{args.subject}/" in r["path"]]
    payload: dict[str, object] = {"tool": "lookup", "root": str(root), "status": "ok"}

    if args.search:
        ranked = sorted(((score(r, args.search), r) for r in rows), key=lambda x: -x[0])
        hits = [r for s, r in ranked if s > 0][: args.limit]
        payload["mode"], payload["query"] = "search", args.search
        payload["hits"] = [{"path": r["path"], "title": r["title"], "tags": show(r["tags"]),
                            "updated": r["updated"], "summary": r["summary"]} for r in hits]
        if not hits:
            payload["status"] = "empty"
    elif args.grep:
        pattern = re.compile(args.grep, re.I)
        hits = []
        for r in rows:
            path = root / r["path"]
            for i, line in enumerate(vault.read_text(path).splitlines(), 1):
                if pattern.search(line):
                    hits.append({"path": r["path"], "line": i, "text": line.strip()[:200]})
                    if len(hits) >= args.limit * 4:
                        break
        payload["mode"], payload["hits"] = "grep", hits
        payload["status"] = "ok" if hits else "empty"
    elif args.outline:
        path, reason = vault.safe_page_path(root, args.outline, scope="wiki")
        if path is None:
            payload.update(mode="outline", status="missing", detail=reason)
            print(f"lookup[outline]: missing — {reason}")
            return 1
        page = vault.load_page(path, root)
        heads, fenced = [], False
        for i, line in enumerate(vault.read_text(path).splitlines(), 1):
            if re.match(r"^\s*(```|~~~)", line):
                fenced = not fenced          # 代码块里的 ## 不是小标题
                continue
            if not fenced and re.match(r"^#{1,6}\s+.+", line):
                heads.append({"line": i, "heading": line.strip()})
        payload.update(mode="outline", page=page.rel, title=page.title,
                       summary=page.summary, headings=heads)
    elif args.neighbors:
        pages = vault.load_pages(root)
        lookup = vault.build_lookup(pages)
        target = vault.resolve_link(args.neighbors, lookup, root)
        if target["status"] != "resolved":
            payload.update(mode="neighbors", status=target["status"], target=args.neighbors)
        else:
            rel = target["matches"][0]              # type: ignore[index]
            page = next((p for p in pages if p.rel == rel), None)
            if page is None:
                payload.update(mode="neighbors", status="not-a-wiki-page",
                               target=args.neighbors, resolved=rel)
                print(f"lookup[neighbors]: {rel} 不是 wiki/ 里的笔记页，没有链接图")
                return 1
            out = []
            for _, t in page.links:
                info = vault.resolve_link(t, lookup, root, page)
                out.append({"target": t, "status": info["status"], "matches": info["matches"]})
            inbound = []
            for other in pages:
                if other.rel == rel:
                    continue
                for _, t in other.links:
                    if rel in vault.resolve_link(t, lookup, root, other)["matches"]:  # type: ignore[operator]
                        inbound.append(other.rel)
                        break
            payload.update(mode="neighbors", page=rel, outbound=out, inbound=sorted(set(inbound)))
    elif args.resolve:
        pages = vault.load_pages(root)
        info = vault.resolve_link(args.resolve, vault.build_lookup(pages), root)
        payload.update(mode="resolve", **info)
        payload["status"] = info["status"]
    elif args.list:
        payload["mode"] = "list"
        payload["pages"] = [{"path": r["path"], "title": r["title"], "type": r["type"],
                             "tags": show(r["tags"]), "updated": r["updated"]} for r in rows]
    else:
        ap.error("需要 --search / --grep / --outline / --neighbors / --resolve / --list 之一")

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"lookup[{payload['mode']}]: {payload['status']}")
        for item in payload.get("hits", []):            # type: ignore[union-attr]
            if "line" in item:
                print(f"  {item['path']}:{item['line']}  {item['text']}")
            else:
                print(f"  {item['path']}  [{item['tags']}] {item['title']} — {item['summary'][:80]}")
        for item in payload.get("headings", []):        # type: ignore[union-attr]
            print(f"  L{item['line']}: {item['heading']}")
        for item in payload.get("outbound", []):        # type: ignore[union-attr]
            print(f"  → {item['target']} [{item['status']}]")
        for item in payload.get("inbound", []):         # type: ignore[union-attr]
            print(f"  ← {item}")
        for item in payload.get("pages", []):           # type: ignore[union-attr]
            print(f"  {item['path']}  [{item['tags']}] {item['title']}")
        if payload["mode"] == "resolve":
            print(f"  matches: {payload.get('matches')}")
    return 0 if payload["status"] in {"ok", "resolved"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
