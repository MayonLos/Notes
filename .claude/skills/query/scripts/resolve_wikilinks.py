#!/usr/bin/env python3
"""Read-only Obsidian wikilink resolver for query workflows."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def files(root: Path) -> list[Path]:
    # Query is deliberately scoped to the compiled knowledge layer.  Indexing
    # root metadata or collaboration briefs would let operational text become
    # an accidental source of knowledge answers.
    wiki = root / "wiki"
    return sorted(wiki.rglob("*.md")) if wiki.is_dir() else []


def key(value: str) -> str:
    value = value.replace("\\", "/").lstrip("./")
    if value.lower().endswith(".md"):
        value = value[:-3]
    return value.casefold()


def index_files(root: Path) -> tuple[dict[str, list[Path]], list[Path]]:
    all_files = files(root)
    index: dict[str, list[Path]] = {}
    for path in all_files:
        rel = path.relative_to(root).as_posix()
        rel_no_ext = rel[:-3] if rel.lower().endswith(".md") else rel
        values = {key(rel), key(rel_no_ext), key(path.name), key(path.stem)}
        if rel.startswith("wiki/"):
            values.update({key(rel[5:]), key(rel_no_ext[5:])})
        for value in values:
            index.setdefault(value, []).append(path)
    return index, all_files


def resolve_target(
    target: str,
    index: dict[str, list[Path]],
    root: Path,
    source: Path | None = None,
) -> dict[str, Any]:
    raw = target.strip()
    embedded = raw.startswith("!")
    if embedded:
        raw = raw[1:]
    target_part, _, alias = raw.partition("|")
    target_part, marker, fragment = target_part.partition("#")
    target_part = target_part.strip()
    candidates = [source] if marker and not target_part and source else []
    candidates.extend(index.get(key(target_part), []))
    candidates = list(dict.fromkeys(candidates))
    if not candidates and (root / target_part).is_file():
        candidates = [root / target_part]
    result: dict[str, Any] = {
        "target": target,
        "path": target_part,
        "alias": alias or None,
        "fragment": fragment if marker else None,
        "embedded": embedded,
        "status": "missing",
        "matches": [p.relative_to(root).as_posix() for p in candidates],
    }
    if len(candidates) == 1:
        result["status"] = "resolved"
        if marker and fragment:
            try:
                text = candidates[0].read_text(encoding="utf-8")
            except UnicodeDecodeError:
                result["fragment_found"] = False
            else:
                heading = re.compile(r"^#{1,6}\s+" + re.escape(fragment) + r"\s*$", re.I | re.M)
                block = re.compile(r"\^" + re.escape(fragment) + r"\s*$", re.M)
                result["fragment_found"] = bool(heading.search(text) or block.search(text))
                if not result["fragment_found"]:
                    result["status"] = "missing-fragment"
    elif len(candidates) > 1:
        result["status"] = "ambiguous"
    return result


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if "results" in result:
        print(f"resolve_wikilinks: {result['status'].upper()} ({len(result['results'])} links)")
        for item in result["results"]:
            print(f"{item['status']}: {item['target']} -> {', '.join(item['matches']) or '-'}")
    else:
        print(f"resolve_wikilinks: {result['status'].upper()}")
        print(f"target: {result['target']}")
        print(f"matches: {', '.join(result['matches']) or '-'}")
        if result.get("fragment"):
            print(f"fragment_found: {result.get('fragment_found', False)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Obsidian wikilink resolver")
    parser.add_argument("target", nargs="?", help="Wikilink target, without [[ ]]")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Vault root")
    parser.add_argument("--from", dest="source", type=Path, help="Page to scan with --scan")
    parser.add_argument("--scan", action="store_true", help="Resolve every wikilink in --from")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error("--root is not a directory")
    index, _ = index_files(root)

    if args.scan:
        if args.source is None:
            parser.error("--scan requires --from")
        source = (args.source if args.source.is_absolute() else root / args.source).resolve()
        if not inside(source, root) or not source.is_file():
            parser.error("--from must be an existing file under --root")
        text = source.read_text(encoding="utf-8")
        results = [resolve_target(match, index, root, source) for match in LINK_RE.findall(text)]
        bad = [item for item in results if item["status"] != "resolved"]
        result: dict[str, Any] = {
            "tool": "resolve_wikilinks",
            "root": str(root),
            "source": source.relative_to(root).as_posix(),
            "status": "ok" if not bad else "issues",
            "results": results,
        }
        emit(result, args.json)
        return 1 if bad else 0

    if not args.target:
        parser.error("provide TARGET or use --scan --from FILE")
    result = resolve_target(args.target, index, root)
    result = {"tool": "resolve_wikilinks", "root": str(root), **result}
    emit(result, args.json)
    return 0 if result["status"] == "resolved" else 1


if __name__ == "__main__":
    sys.exit(main())
