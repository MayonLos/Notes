#!/usr/bin/env python3
"""Read-only preflight for ingest sources."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

RAW_DIRS = (
    "raw/01-articles",
    "raw/02-papers",
    "raw/03-transcripts",
    "raw/04-notes",
    "raw/05-wiki-export",
)
ARCHIVE = "raw/09-archive"


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def candidates(root: Path) -> list[str]:
    result: list[str] = []
    for rel_dir in RAW_DIRS:
        directory = root / rel_dir
        if directory.is_dir():
            result.extend(
                p.relative_to(root).as_posix()
                for p in directory.rglob("*")
                if p.is_file()
            )
    return sorted(result)


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"validate_ingest: {result['status'].upper()}")
    print(f"root: {result['root']}")
    if result.get("source"):
        print(f"source: {result['source']}")
    if "candidates" in result:
        print(f"eligible_sources: {len(result['candidates'])}")
    for message in result.get("errors", []):
        print(f"ERROR: {message}")
    for message in result.get("warnings", []):
        print(f"WARNING: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only ingest source preflight")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Vault root")
    parser.add_argument("--source", help="Vault-relative or absolute source path")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    result: dict[str, Any] = {
        "tool": "validate_ingest",
        "root": str(root),
        "status": "invalid",
        "source": None,
        "checks": {},
        "errors": [],
        "warnings": [],
    }
    if not root.is_dir():
        result["errors"].append("root is not a directory")
        emit(result, args.json)
        return 1

    if args.source is None:
        missing = [d for d in RAW_DIRS if not (root / d).is_dir()]
        result["checks"]["raw_dirs"] = {d: d not in missing for d in RAW_DIRS}
        result["candidates"] = candidates(root)
        if missing:
            result["errors"].append("missing source directories: " + ", ".join(missing))
        result["status"] = "inventory" if not result["errors"] else "invalid"
        emit(result, args.json)
        return 1 if result["errors"] else 0

    supplied = Path(args.source).expanduser()
    source = (supplied if supplied.is_absolute() else root / supplied).resolve()
    result["source"] = source.relative_to(root).as_posix() if inside(source, root) else str(source)
    raw_root = (root / "raw").resolve()
    archive_root = (root / ARCHIVE).resolve()

    if not inside(source, root):
        result["errors"].append("source is outside the vault root")
    elif not inside(source, raw_root):
        result["errors"].append("source is not under raw/")
    elif inside(source, archive_root):
        result["errors"].append("archived sources under raw/09-archive/ are not ingestible")
    elif not source.is_file():
        result["errors"].append("source file does not exist")
    else:
        result["checks"]["readable"] = True
        try:
            source.read_text(encoding="utf-8")
            result["checks"]["utf8"] = True
        except UnicodeDecodeError:
            result["checks"]["utf8"] = False
            result["warnings"].append("source is not UTF-8; use a text extractor before compilation")
        source_rel = source.relative_to(root).as_posix()
        occurrences: list[str] = []
        wiki = root / "wiki"
        if wiki.is_dir():
            for page in wiki.rglob("*.md"):
                try:
                    text = page.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if source_rel in text:
                    occurrences.append(page.relative_to(root).as_posix())
        if occurrences:
            result["checks"]["existing_source_references"] = occurrences
            result["warnings"].append("source path already appears in: " + ", ".join(occurrences[:10]))
            result["status"] = "duplicate"
        else:
            result["checks"]["existing_source_references"] = []
            result["status"] = "ready"

    if result["errors"]:
        result["status"] = "invalid"
    emit(result, args.json)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
