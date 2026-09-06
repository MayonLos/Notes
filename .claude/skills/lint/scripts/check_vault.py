#!/usr/bin/env python3
"""Read-only structural health check for the Vault wiki."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
ALLOWED_TYPES = {"entity", "concept", "source", "synthesis", "comparison"}
EXEMPT = {"index.md", "log.md", "synthesis.md"}


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.S)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if item:
            fields[item.group(1)] = item.group(2).strip().strip("'\"")
    return fields


def resolve_target(target: str, pages: list[Path], root: Path, source: Path | None = None) -> list[Path]:
    value = target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if not value:
        return [source] if source else []
    if value.startswith("./"):
        value = value[2:]
    candidates: list[Path] = []
    direct = root / value
    if direct.is_file():
        candidates.append(direct)
    if not value.lower().endswith(".md") and (root / (value + ".md")).is_file():
        candidates.append(root / (value + ".md"))
    if not value.lower().endswith(".md") and (root / "wiki" / (value + ".md")).is_file():
        candidates.append(root / "wiki" / (value + ".md"))
    if (root / "wiki" / value).is_file():
        candidates.append(root / "wiki" / value)
    lowered = value.casefold()
    for page in pages:
        rel = page.relative_to(root).as_posix()
        choices = {rel.casefold(), page.stem.casefold(), page.name.casefold()}
        if not value.lower().endswith(".md"):
            choices.add(rel[:-3].casefold() if rel.lower().endswith(".md") else rel.casefold())
        if lowered in choices and page not in candidates:
            candidates.append(page)
    return candidates


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"check_vault: {result['status']}")
    print(f"pages: {result['checks']['pages']} errors: {len(result['errors'])} warnings: {len(result['warnings'])}")
    for item in result["errors"]:
        print(f"ERROR: {item}")
    for item in result["warnings"][:30]:
        print(f"WARNING: {item}")
    if len(result["warnings"]) > 30:
        print(f"WARNING: ... {len(result['warnings']) - 30} more")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Vault wiki health check")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Vault root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    wiki = root / "wiki"
    result: dict[str, Any] = {
        "tool": "check_vault",
        "root": str(root),
        "status": "PASS",
        "checks": {"pages": 0, "frontmatter": 0, "dead_links": 0, "unindexed": 0, "orphans": 0},
        "errors": [],
        "warnings": [],
    }
    if not root.is_dir() or not wiki.is_dir():
        result["status"] = "FAIL"
        result["errors"].append("root or wiki/ is missing")
        emit(result, args.json)
        return 1

    for required in ("index.md", "log.md", "synthesis.md"):
        if not (wiki / required).is_file():
            result["errors"].append(f"missing wiki/{required}")

    pages = sorted(wiki.rglob("*.md"))
    content_pages = [p for p in pages if p.name not in EXEMPT]
    result["checks"]["pages"] = len(content_pages)
    inbound: dict[Path, int] = {p: 0 for p in content_pages}
    index_text = (wiki / "index.md").read_text(encoding="utf-8") if (wiki / "index.md").is_file() else ""

    for page in content_pages:
        rel = page.relative_to(root).as_posix()
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            result["errors"].append(f"{rel}: not valid UTF-8")
            continue
        fm = parse_frontmatter(text)
        if fm is None:
            result["errors"].append(f"{rel}: missing YAML frontmatter")
        else:
            result["checks"]["frontmatter"] += 1
            for field in ("title", "type", "tags", "last_updated"):
                if field not in fm:
                    result["warnings"].append(f"{rel}: missing frontmatter field {field}")
            if fm.get("type") and fm["type"] not in ALLOWED_TYPES:
                result["errors"].append(f"{rel}: invalid type {fm['type']!r}")
        if "## 关联连接" not in text:
            result["warnings"].append(f"{rel}: missing ## 关联连接")
        for raw_target in WIKILINK_RE.findall(text):
            matches = resolve_target(raw_target, pages, root, page)
            if len(matches) == 1:
                if matches[0] in inbound:
                    inbound[matches[0]] += 1
            elif not matches:
                result["checks"]["dead_links"] += 1
                result["errors"].append(f"{rel}: unresolved wikilink [[{raw_target}]]")
            else:
                result["warnings"].append(f"{rel}: ambiguous wikilink [[{raw_target}]]")
        if not re.search(r"^last_updated:\s*\S+", text, re.M):
            result["warnings"].append(f"{rel}: last_updated is absent or empty")
        if rel not in index_text and page.stem not in index_text:
            result["checks"]["unindexed"] += 1
            result["warnings"].append(f"{rel}: not found in wiki/index.md")

    for page, count in inbound.items():
        if count == 0:
            result["checks"]["orphans"] += 1
            result["warnings"].append(f"{page.relative_to(root).as_posix()}: no inbound wikilink")

    raw_dirs = [root / f"raw/0{i}" for i in range(1, 6)]
    result["checks"]["raw_pending"] = sum(
        1 for directory in raw_dirs if directory.is_dir() for path in directory.rglob("*") if path.is_file()
    )
    if result["errors"]:
        result["status"] = "FAIL"
    elif result["warnings"]:
        result["status"] = "WARN"
    emit(result, args.json)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
