#!/usr/bin/env python3
"""只读复习看板：学科覆盖、复习队列、知识缺口、TODO 进度、自测考点抽取。

  （无参数）        输出整体学习状态
  --subject cpp     只看一个学科
  --points PAGE     抽取该页考点骨架（小标题/公式/加粗术语/表头），供出自测题
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
import vault  # noqa: E402

MARKER_LINE = re.compile(r"^.*(待补充|待验证|知识冲突|\[!todo\]|\[!question\]).*$", re.M)
BOLD = re.compile(r"\*\*([^*\n]{2,40})\*\*")
FORMULA = re.compile(r"\$\$(.+?)\$\$", re.S)
CHECK = re.compile(r"^\s*-\s\[( |x|/)\]\s+(.*)$", re.M)


def todo_progress(root: Path) -> dict[str, dict[str, int]]:
    path = root / "TODO.md"
    if not path.is_file():
        return {}
    text = vault.read_text(path)
    sections: dict[str, dict[str, int]] = {}
    current = "未分节"
    for line in text.splitlines():
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            current = head.group(1).strip()
            continue
        item = CHECK.match(line)
        if item:
            bucket = sections.setdefault(current, {"done": 0, "doing": 0, "todo": 0})
            bucket["done" if item.group(1) == "x" else
                   "doing" if item.group(1) == "/" else "todo"] += 1
    return sections


def points(root: Path, rel: str) -> dict[str, object]:
    path, reason = vault.safe_page_path(root, rel, scope="wiki")
    if path is None:
        return {"mode": "points", "page": rel, "error": reason}
    page = vault.load_page(path, root)
    body = vault.strip_code(page.body)
    terms: list[str] = []
    for term in BOLD.findall(body):
        clean = term.strip()
        if clean and clean not in terms:
            terms.append(clean)
    tables = [line.strip() for line in body.splitlines()
              if line.strip().startswith("|") and "---" not in line][:20]
    return {
        "mode": "points", "page": page.rel, "title": page.title,
        "summary": page.summary, "last_updated": page.last_updated,
        "headings": page.headings,
        "formulas": [f.strip().replace("\n", " ")[:120] for f in FORMULA.findall(body)][:20],
        "terms": terms[:40],
        "table_rows": tables,
        "links": sorted({vault.split_link(t)[0] for _, t in page.links}),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="只读学习状态看板")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--subject", choices=sorted(vault.SUBJECT_DIRS))
    ap.add_argument("--points", help="抽取某页考点骨架")
    ap.add_argument("--stale-days", type=int, default=60, help="超过多少天未更新进入复习队列")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    if not (root / "wiki").is_dir():
        print("study_status: FAIL — 找不到 wiki/", file=sys.stderr)
        return 1

    if args.points:
        data = points(root, args.points)
        if "error" in data:
            print(f"study_status[points]: FAIL — {data['error']}", file=sys.stderr)
            return 1
        payload = {"tool": "study_status", "root": str(root), "status": "ok", **data}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"study_status[points]: {payload['page']} — {payload['title']}")
            print(f"  摘要: {payload['summary']}")
            print(f"  小标题({len(payload['headings'])}): {' | '.join(payload['headings'][:20])}")
            print(f"  公式({len(payload['formulas'])}): " + " ;; ".join(payload["formulas"][:6]))
            print(f"  术语({len(payload['terms'])}): {'、'.join(payload['terms'][:25])}")
            print(f"  关联: {'、'.join(payload['links'])}")
        return 0

    stats = vault.ensure_index(root)
    pages_all = [p for p in vault.load_pages(root) if not p.is_special]
    pages = list(pages_all)
    if args.subject:
        pages = [p for p in pages if p.subject == args.subject]
    today = dt.date.today()

    queue = []
    gaps = []
    for page in pages:
        age = None
        if page.last_updated:
            try:
                age = (today - dt.date.fromisoformat(page.last_updated)).days
            except ValueError:
                age = None
        if age is not None and age >= args.stale_days:
            queue.append({"path": page.rel, "title": page.title, "days": age,
                          "subject": page.subject})
        for match in re.finditer(MARKER_LINE, vault.strip_code(page.body)):
            gaps.append({"path": page.rel, "marker": match.group(1),
                         "text": match.group(0).strip()[:110]})
    queue.sort(key=lambda x: -x["days"])

    planned = stats.get("planned_pages", {})
    if args.subject:
        planned = {k: v for k, v in planned.items()
                   if any(f"/concepts/{args.subject}/" in s for s in v)}
    planned_rank = sorted(planned.items(), key=lambda kv: -len(kv[1]))

    payload = {
        "tool": "study_status", "root": str(root), "status": "ok", "mode": "dashboard",
        "subject": args.subject or "全部",
        "coverage": {s: sum(1 for p in pages_all if p.subject == s)
                     for s in vault.SUBJECT_DIRS} if not args.subject
                    else {args.subject: len(pages)},
        "review_queue": queue[: args.limit],
        "planned_pages": [{"name": k, "awaited_by": v} for k, v in planned_rank[: args.limit]],
        "gaps": gaps[: args.limit * 2],
        "todo_progress": todo_progress(root),
        "totals": {"pages": len(pages), "stale": len(queue),
                   "planned": len(planned), "gaps": len(gaps)},
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    t = payload["totals"]
    print(f"study_status: {payload['subject']} — 页面 {t['pages']} / 待复习 {t['stale']} / "
          f"待写 {t['planned']} / 缺口标记 {t['gaps']}")
    print("\n[学科覆盖]")
    for key, value in payload["coverage"].items():
        print(f"  {vault.SUBJECT_DIRS.get(key, key)}: {value} 页")
    print(f"\n[复习队列 · 超过 {args.stale_days} 天未更新]")
    for item in payload["review_queue"]:
        print(f"  {item['days']:>4}天  {item['path']} — {item['title']}")
    print("\n[待写页面 · 按被引用次数]")
    for item in payload["planned_pages"]:
        print(f"  {item['name']}  ← {len(item['awaited_by'])} 处引用")
    print("\n[知识缺口标记]")
    for item in payload["gaps"]:
        print(f"  [{item['marker']}] {item['path']}: {item['text']}")
    print("\n[TODO 进度]")
    for section, counts in payload["todo_progress"].items():
        total = sum(counts.values())
        print(f"  {section}: {counts['done']}/{total} 完成，进行中 {counts['doing']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
