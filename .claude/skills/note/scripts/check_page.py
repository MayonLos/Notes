#!/usr/bin/env python3
"""写笔记的前置/后置校验（只读）。

用法三种：
  --new "二阶系统" --tag control   写之前查重并给出建议路径
  --page wiki/...md               写之后校验单页 schema、链接、登记
  --source raw/01-articles/x.md   摄入 raw 资料前的来源预检
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_lib"))
import vault  # noqa: E402

TAG_DIR = {"control": "wiki/concepts/control", "math": "wiki/concepts/control",
           "digital": "wiki/concepts/digital", "cpp": "wiki/concepts/cpp",
           "embedded": "wiki/concepts/cpp"}
REQUIRED_FM = ("title", "type", "tags", "last_updated")


def check_new(root: Path, name: str, tag: str | None, pages: list[vault.Page]) -> dict:
    names = {p.stem: p.rel for p in pages}
    for page in pages:
        for alias in page.aliases:
            names.setdefault(alias, page.rel)
    exact_names = [key for key in names if key.casefold() == name.casefold()]
    exact = [names[key] for key in exact_names]
    close = difflib.get_close_matches(name, list(names), n=4, cutoff=0.6)
    planned = []
    stats_file = vault.cache_dir(root) / vault.STATS_JSON
    vault.ensure_index(root)
    if stats_file.is_file():
        stats = json.loads(stats_file.read_text(encoding="utf-8"))
        for target, sources in stats.get("planned_pages", {}).items():
            # 待写链接可能写成 [[新页]] 也可能写成 [[concepts/cpp/新页]]
            leaf = target.rsplit("/", 1)[-1]
            if name.casefold() in {target.casefold(), leaf.casefold()}:
                planned = sources
    out = {"mode": "new", "name": name, "status": "ok", "existing": exact,
           "similar": [f"{c} → {names[c]}" for c in close if c not in exact_names],
           "awaited_by": planned,
           "suggested_path": f"{TAG_DIR.get(tag or '', 'wiki/concepts')}/{name}.md"}
    if exact:
        out["status"] = "duplicate"
    elif out["similar"]:
        out["status"] = "similar"
    return out


def check_page(root: Path, rel: str, pages: list[vault.Page],
               lookup: dict, index_keys: set, log_text: str) -> dict:
    out: dict = {"mode": "page", "page": rel, "status": "ok", "errors": [], "warnings": []}
    path, reason = vault.safe_page_path(root, rel, scope="wiki")
    if path is None:
        out["errors"].append(f"{reason}（本 skill 只写 wiki/）")
        out["status"] = "fail"
        return out
    out["page"] = reason          # 归一化后的相对路径
    page = vault.load_page(path, root)
    if page.fm is None:
        out["errors"].append("缺少 YAML frontmatter")
    else:
        for field in REQUIRED_FM:
            if not page.fm.get(field):
                out["errors"].append(f"frontmatter 缺少 {field}")
        if page.type and page.type not in vault.PAGE_TYPES:
            out["errors"].append(f"type 非法：{page.type}")
        if page.last_updated:
            try:
                dt.date.fromisoformat(page.last_updated)
            except ValueError:
                out["errors"].append(f"last_updated 非 YYYY-MM-DD：{page.last_updated}")
        if "sources" not in page.fm:
            out["warnings"].append("没有 sources 字段（自学笔记可留空列表，但字段要在）")
    if "## 关联连接" not in page.body:
        out["errors"].append("缺少 ## 关联连接 区域")
    else:
        tail = page.body.split("## 关联连接", 1)[1]
        if not vault.WIKILINK_RE.search(vault.strip_code(tail)):
            out["errors"].append("## 关联连接 里没有任何 [[wikilink]]")
    expect_dir = TAG_DIR.get(page.tags[0]) if page.tags else None
    if expect_dir and not page.rel.startswith(expect_dir) and page.type == "concept":
        out["warnings"].append(f"主标签 #{page.tags[0]} 建议放在 {expect_dir}/")
    for embed, target in page.links:
        info = vault.resolve_link(target, lookup, root, page)
        if info["status"] == "missing":
            close = vault.nearest(target, pages, root)
            if embed:
                out["errors"].append(f"嵌入资源缺失 ![[{target}]]")
            else:
                out.setdefault("planned", []).append(target)
                if close:
                    out["warnings"].append(
                        f"[[{target}]] 尚未建页，与已有页面相近 {close}——确认是打错字还是另一页")
        elif info["status"] != "resolved":
            out["warnings"].append(f"[[{target}]]：{info['status']} {info['matches']}")
    if not vault.is_registered(index_keys, page):
        out["errors"].append("未登记到 wiki/index.md")
    if page.stem not in log_text:
        out["warnings"].append("wiki/log.md 中没有提到本页（新建/大改后应追加一条）")
    out["status"] = "fail" if out["errors"] else ("warn" if out["warnings"] else "ok")
    return out


def check_source(root: Path, rel: str, pages: list[vault.Page]) -> dict:
    out: dict = {"mode": "source", "source": rel, "status": "ready",
                 "errors": [], "warnings": [], "referenced_by": []}
    path = (root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
    try:
        inside = path.relative_to(root).as_posix()
    except ValueError:
        out["errors"].append("来源在 Vault 之外")
        out["status"] = "invalid"
        return out
    if not inside.startswith("raw/"):
        out["errors"].append("来源不在 raw/ 下")
    elif inside == "raw/09-archive" or inside.startswith("raw/09-archive/"):
        out["errors"].append("raw/09-archive/ 已归档，禁止读取与摄入")
    elif not path.is_file():
        out["errors"].append("来源文件不存在")
    else:
        try:
            vault.read_text(path)
        except UnicodeDecodeError:
            out["warnings"].append("非 UTF-8 文本，需要先提取文本（PDF 等）")
        # 精确匹配，避免 raw/a.md 命中 raw/a.md.bak
        ref = re.compile(r"(?<![\w./-])" + re.escape(inside) + r"(?![\w.-])")
        out["referenced_by"] = [p.rel for p in pages
                                if ref.search(p.body) or any(ref.search(x) for x in p.sources)]
        if out["referenced_by"]:
            out["status"] = "duplicate"
            out["warnings"].append("该来源已被引用，确认是补充还是重复摄入")
    if out["errors"]:
        out["status"] = "invalid"
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="笔记页面写入前后的只读校验")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--page", action="append", default=[], help="要校验的 wiki 页面（可重复）")
    ap.add_argument("--new", help="拟新建的页面名，做查重")
    ap.add_argument("--tag", help="配合 --new，用主标签推荐落盘目录")
    ap.add_argument("--source", help="raw/ 下的来源文件预检")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    if not (root / "wiki").is_dir():
        print("check_page: FAIL — 找不到 wiki/", file=sys.stderr)
        return 1
    pages = vault.load_pages(root)
    lookup = vault.build_lookup(pages)
    index_keys = vault.registered_keys(
        vault.read_text(root / "wiki/index.md") if (root / "wiki/index.md").is_file() else "")
    log_text = vault.read_text(root / "wiki/log.md") if (root / "wiki/log.md").is_file() else ""

    results: list[dict] = []
    if args.new:
        results.append(check_new(root, args.new, args.tag, pages))
    if args.source:
        results.append(check_source(root, args.source, pages))
    for rel in args.page:
        results.append(check_page(root, rel, pages, lookup, index_keys, log_text))
    if not results:
        ap.error("至少提供 --new / --page / --source 之一")

    bad = [r for r in results if r["status"] in {"fail", "invalid"}]
    payload = {"tool": "check_page", "root": str(root),
               "status": "FAIL" if bad else "OK", "results": results}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"check_page: {payload['status']}")
        for item in results:
            head = item.get("page") or item.get("source") or item.get("name")
            print(f"\n[{item['mode']}] {head} → {item['status']}")
            for key in ("existing", "similar", "awaited_by", "referenced_by", "planned"):
                if item.get(key):
                    print(f"  {key}: {item[key]}")
            if item.get("suggested_path"):
                print(f"  suggested_path: {item['suggested_path']}")
            for err in item.get("errors", []):
                print(f"  ERROR: {err}")
            for warn in item.get("warnings", []):
                print(f"  WARN: {warn}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
