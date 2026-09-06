#!/usr/bin/env python3
"""构建/刷新 Vault 索引缓存（只写 .claude/cache/vault-index/，不碰笔记）。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vault  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="构建 Vault 索引缓存")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--force", action="store_true", help="忽略新鲜度检查，强制重建")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = args.root.expanduser().resolve()
    if not (root / "wiki").is_dir():
        print("build_index: FAIL — 找不到 wiki/", file=sys.stderr)
        return 1
    stats, rebuilt = vault.ensure_index_ex(root, force=args.force)
    stats["rebuilt"] = rebuilt
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(f"build_index: OK（{'重建' if stats['rebuilt'] else '缓存命中'}）")
        print(f"pages: {stats['pages']}  links: {stats['links']}  "
              f"planned: {len(stats['planned_pages'])}")
        print(f"cache: {vault.cache_dir(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
