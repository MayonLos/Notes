#!/usr/bin/env python3
"""共享库：Vault 页面模型、frontmatter 解析、wikilink 解析与索引缓存。

所有 skill 脚本都只读 Vault 内容；唯一写入是 `.claude/cache/vault-index/`
下的索引缓存（非笔记内容，不进入 Obsidian 图谱）。
标准库实现，无第三方依赖。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------- 约定常量

PAGE_TYPES = {"entity", "concept", "source", "synthesis", "comparison", "index", "meta"}
SUBJECT_DIRS = {"control": "自动控制原理", "digital": "数字电路", "cpp": "C++"}
# CLAUDE.md 标签表；新增标签时同步这里，lint 才不会误报
KNOWN_TAGS = {"control", "math", "digital", "cpp", "embedded", "ai", "cs", "meta",
              "todo", "synthesis", "source", "comparison"}
SPECIAL_PAGES = {"wiki/index.md", "wiki/log.md", "wiki/synthesis.md"}
MARKERS = {
    "conflict": re.compile(r"知识冲突|\[!warning\][^\n]*矛盾"),
    "unverified": re.compile(r"待验证|\[!question\]"),
    "todo": re.compile(r"待补充|\[!todo\]"),
}
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]\n]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$", re.M)
FENCE_RE = re.compile(r"^(?:```|~~~).*?^(?:```|~~~)\s*$", re.M | re.S)

CACHE_DIR = Path(".claude/cache/vault-index")
PAGES_TSV = "pages.tsv"
LIST_SEP = "\x1f"   # 列表分隔符：正文里不会出现，避免逗号/制表符破坏 TSV
LINKS_TSV = "links.tsv"
STATS_JSON = "stats.json"

# ---------------------------------------------------------------- 基础工具


def read_text(path: Path) -> str:
    """读文件并去掉 BOM（Vault 里有带 BOM 的页面，否则 frontmatter 会解析失败）。"""
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8")


def strip_code(text: str) -> str:
    """移除围栏代码块，避免把示例中的 [[页面名]] 当成真链接。"""
    return FENCE_RE.sub("", text)


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    """解析 YAML frontmatter 的常用子集：标量、块列表、行内列表。返回 (字段, 正文)。"""
    match = re.match(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", text, re.S)
    if not match:
        return None, text
    fields: dict[str, object] = {}
    key: str | None = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and key:
            bucket = fields.setdefault(key, [])
            if isinstance(bucket, list):
                bucket.append(_scalar(item.group(1)))
            continue
        pair = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if pair:
            key, value = pair.group(1), pair.group(2).strip()
            if value == "":
                fields[key] = []
            elif value.startswith("[") and value.endswith("]"):
                fields[key] = _inline_list(value[1:-1])
            else:
                fields[key] = _scalar(value)
    return fields, text[match.end():]


def _inline_list(inner: str) -> list[str]:
    """切分行内列表，引号内的逗号不算分隔符：["A, B"] 是一个元素。"""
    items, buf, quote = [], "", ""
    for ch in inner:
        if quote:
            if ch == quote:
                quote = ""
            else:
                buf += ch
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            items.append(buf)
            buf = ""
        else:
            buf += ch
    items.append(buf)
    return [v for v in (_scalar(i) for i in items) if v]


def _scalar(value: str) -> str:
    return value.strip().strip('"').strip("'").strip()


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    return [str(value)] if str(value).strip() else []


def norm_tag(tag: str) -> str:
    return tag.lstrip("#").strip()


# ---------------------------------------------------------------- 页面模型


@dataclass(eq=False)  # 按身份哈希，便于放进 dict/set
class Page:
    path: Path
    rel: str
    fm: dict[str, object] | None
    body: str
    title: str = ""
    type: str = ""
    tags: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    last_updated: str = ""
    headings: list[str] = field(default_factory=list)
    links: list[tuple[bool, str]] = field(default_factory=list)  # (是否 embed, 原始目标)
    summary: str = ""

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def subject(self) -> str:
        parts = self.rel.split("/")
        return parts[2] if len(parts) > 3 and parts[1] == "concepts" else ""

    @property
    def is_special(self) -> bool:
        return self.rel in SPECIAL_PAGES

    def markers(self) -> dict[str, int]:
        clean = strip_code(self.body)   # 代码示例里的 [!todo] 不算知识缺口
        return {name: len(rx.findall(clean)) for name, rx in MARKERS.items()}


def load_page(path: Path, root: Path) -> Page:
    text = read_text(path)
    fm, body = parse_frontmatter(text)
    fm = fm or {}
    clean = strip_code(body)
    page = Page(
        path=path,
        rel=path.relative_to(root).as_posix(),
        fm=fm if fm else None,
        body=body,
        title=str(fm.get("title") or path.stem),
        type=str(fm.get("type") or ""),
        tags=[norm_tag(t) for t in as_list(fm.get("tags"))],
        aliases=as_list(fm.get("aliases")),
        sources=as_list(fm.get("sources")),
        last_updated=str(fm.get("last_updated") or ""),
        headings=[m.group(2).strip() for m in HEADING_RE.finditer(clean)],
        links=[(bang == "!", target.strip()) for bang, target in WIKILINK_RE.findall(clean)],
    )
    page.summary = _summary(clean)
    return page


def _summary(body: str) -> str:
    """取首个引用块或首个正文段落作为一句话摘要。"""
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "---", "|", "!", "```")):
            continue
        text = re.sub(r"^>\s*", "", stripped)
        if text.startswith("[!"):
            continue
        text = re.sub(r"[*`$]|\[\[|\]\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 8:
            return text[:140]
    return ""


def wiki_pages(root: Path) -> list[Path]:
    wiki = root / "wiki"
    return sorted(p for p in wiki.rglob("*.md")) if wiki.is_dir() else []


def load_pages(root: Path) -> list[Page]:
    return [load_page(p, root) for p in wiki_pages(root)]


# ---------------------------------------------------------------- 链接解析


def link_key(value: str) -> str:
    value = value.replace("\\", "/").strip()
    if value.startswith("./"):
        value = value[2:]
    if value.lower().endswith(".md"):
        value = value[:-3]
    return value.casefold()


def build_lookup(pages: list[Page]) -> dict[str, list[Page]]:
    """页面名 / 相对路径 / 别名 → 页面，供 wikilink 解析。"""
    table: dict[str, list[Page]] = {}
    for page in pages:
        keys = {link_key(page.rel), link_key(page.stem), link_key(page.title)}
        if page.rel.startswith("wiki/"):
            keys.add(link_key(page.rel[5:]))
        for alias in page.aliases:
            keys.add(link_key(alias))
        for key in keys:
            if key:
                table.setdefault(key, []).append(page)
    return table


_FILE_INDEX: dict[str, dict[str, list[str]]] = {}
_NAME_INDEX: dict[str, dict[str, str]] = {}


def _rel_inside(path: Path, root: Path) -> str | None:
    """路径在 root 之内则返回相对路径，否则返回 None（库外路径不再抛异常）。"""
    try:
        return path.resolve().relative_to(root).as_posix()
    except (ValueError, OSError):
        return None


def file_index(root: Path) -> dict[str, list[str]]:
    """文件名 → 相对路径，整库只扫一次；避免每个缺失链接都 rglob 全库。"""
    key = str(root)
    if key not in _FILE_INDEX:
        table: dict[str, list[str]] = {}
        skip = {".git", ".trash", ".obsidian", ".claude", ".claudian", ".smart-env", ".team"}
        for path in root.rglob("*"):
            if not path.is_file() or skip & set(path.parts):
                continue
            table.setdefault(path.name.casefold(), []).append(
                path.relative_to(root).as_posix())
        _FILE_INDEX[key] = table
    return _FILE_INDEX[key]


def name_index(root: Path, pages: list[Page]) -> dict[str, str]:
    """页面名/别名 → 相对路径，供相近页面猜测复用，避免 O(N×M)。"""
    key = f"{root}:{len(pages)}"
    if key not in _NAME_INDEX:
        names: dict[str, str] = {}
        for page in pages:
            names[page.stem] = page.rel
            for alias in page.aliases:
                names.setdefault(alias, page.rel)
        _NAME_INDEX[key] = names
    return _NAME_INDEX[key]


def safe_page_path(root: Path, rel: str, scope: str = "wiki") -> tuple[Path | None, str]:
    """把用户给的路径限制在 root/scope 之内，挡掉 `wiki/../TODO.md` 这类穿越。"""
    candidate = (root / rel) if not Path(rel).is_absolute() else Path(rel)
    try:
        resolved = candidate.resolve()
    except OSError:
        return None, f"路径无法解析：{rel}"
    inside = _rel_inside(resolved, root)
    if inside is None:
        return None, f"路径在 Vault 之外：{rel}"
    if scope and not inside.startswith(f"{scope}/"):
        return None, f"路径不在 {scope}/ 之内：{inside}"
    if not resolved.is_file():
        return None, f"文件不存在：{inside}"
    return resolved, inside


def registered_keys(index_text: str) -> set[str]:
    """index.md 里所有 wikilink 目标的归一化键，整份只解析一次。"""
    return {link_key(split_link(raw[1])[0]) for raw in WIKILINK_RE.findall(index_text)}


def is_registered(index_text: str | set[str], page: Page) -> bool:
    """页面是否登记进 index.md——按 wikilink 匹配，不用子串（`逻辑` ≠ `逻辑函数化简`）。"""
    keys = index_text if isinstance(index_text, set) else registered_keys(index_text)
    rel_noext = page.rel[5:] if page.rel.startswith("wiki/") else page.rel
    targets = {page.stem, page.title, page.rel, rel_noext}
    return bool(keys & {link_key(t) for t in targets if t})


def split_link(target: str) -> tuple[str, str, str]:
    """`目标#标题|别名` → (目标, 片段, 别名)。"""
    body, _, alias = target.partition("|")
    path_part, marker, fragment = body.partition("#")
    return path_part.strip(), (fragment.strip() if marker else ""), alias.strip()


def resolve_link(target: str, lookup: dict[str, list[Page]], root: Path,
                 source: Page | None = None) -> dict[str, object]:
    path_part, fragment, alias = split_link(target)
    if not path_part and fragment and source is not None:
        matches = [source]
    else:
        matches = list(dict.fromkeys(lookup.get(link_key(path_part), [])))
    result: dict[str, object] = {
        "target": target, "path": path_part, "fragment": fragment, "alias": alias,
        "status": "missing", "matches": [p.rel for p in matches],
    }
    if not matches:
        # 非 wiki/ 内的根目录文档（README/TODO/CLAUDE）与 assets/ 里的图片
        for candidate in (root / path_part, root / f"{path_part}.md"):
            rel = _rel_inside(candidate, root)
            if rel and candidate.is_file():
                result.update(status="resolved", matches=[rel])
                return result
        hits = file_index(root).get(Path(path_part).name.casefold(), [])
        if len(hits) == 1:
            result.update(status="resolved", matches=[hits[0]])
        return result
    if len(matches) > 1:
        result["status"] = "ambiguous"
        return result
    page = matches[0]
    result["status"] = "resolved"
    if fragment:
        found = any(h.casefold() == fragment.casefold() for h in page.headings) or bool(
            re.search(r"\^" + re.escape(fragment) + r"\s*$", page.body, re.M))
        result["fragment_found"] = found
        if not found:
            result["status"] = "missing-fragment"
    return result


def nearest(target: str, pages: list[Page], root: Path | None = None,
            cutoff: float = 0.72) -> list[str]:
    """给缺失链接找相近的已有页面名——用于提示「可能打错字」，由人判断。"""
    import difflib
    names = name_index(root or Path("."), pages)
    hits = difflib.get_close_matches(split_link(target)[0], list(names), n=2, cutoff=cutoff)
    return [f"{h} ({names[h]})" for h in hits]


# ---------------------------------------------------------------- 索引缓存


def cache_dir(root: Path) -> Path:
    return root / CACHE_DIR


def source_signature(root: Path) -> str:
    """页面集合 + 各自 mtime 的指纹。改名或删除页面也会改变它，单看 mtime 会漏。"""
    import hashlib
    sources = wiki_pages(root) + [p for p in (root / "TODO.md", root / "CLAUDE.md") if p.is_file()]
    parts = [f"{p.relative_to(root).as_posix()}:{p.stat().st_mtime_ns}" for p in sorted(sources)]
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:32]


def index_stale(root: Path) -> bool:
    out = cache_dir(root)
    files = [out / PAGES_TSV, out / LINKS_TSV, out / STATS_JSON]
    if not all(f.is_file() for f in files):
        return True
    try:
        cached = json.loads((out / STATS_JSON).read_text(encoding="utf-8")).get("signature")
    except (OSError, ValueError):
        return True
    return cached != source_signature(root)


def build_index(root: Path) -> dict[str, object]:
    """生成紧凑索引：一行一页 + 一行一链接，供 skill 少量读取而非全库通读。"""
    pages = load_pages(root)
    lookup = build_lookup(pages)
    out = cache_dir(root)
    out.mkdir(parents=True, exist_ok=True)

    def cell(value: str) -> str:
        return re.sub(r"[\t\r\n\x1f]", " ", str(value)).strip()

    rows = ["path\ttype\ttags\ttitle\taliases\tupdated\tsummary\theadings"]
    for page in pages:
        rows.append("\t".join([
            page.rel, cell(page.type), LIST_SEP.join(cell(t) for t in page.tags),
            cell(page.title), LIST_SEP.join(cell(a) for a in page.aliases),
            cell(page.last_updated), cell(page.summary),
            LIST_SEP.join(cell(h) for h in page.headings[:24]),
        ]))
    (out / PAGES_TSV).write_text("\n".join(rows) + "\n", encoding="utf-8")

    link_rows = ["source\ttarget\tstatus\tresolved"]
    counts = {"resolved": 0, "missing": 0, "ambiguous": 0, "missing-fragment": 0}
    planned: dict[str, list[str]] = {}
    for page in pages:
        for embed, target in page.links:
            info = resolve_link(target, lookup, root, page)
            status = str(info["status"])
            counts[status] = counts.get(status, 0) + 1
            matches = info["matches"]
            link_rows.append("\t".join([
                page.rel, ("!" if embed else "") + target, status,
                ",".join(matches) if isinstance(matches, list) else "",
            ]))
            if status == "missing":
                planned.setdefault(split_link(target)[0], []).append(page.rel)
    (out / LINKS_TSV).write_text("\n".join(link_rows) + "\n", encoding="utf-8")

    stats = {
        "generated_from": str(root),
        "signature": source_signature(root),
        "pages": len(pages),
        "links": sum(counts.values()),
        "link_status": counts,
        "planned_pages": {k: sorted(set(v)) for k, v in sorted(planned.items())},
        "subjects": {s: sum(1 for p in pages if p.subject == s) for s in SUBJECT_DIRS},
    }
    (out / STATS_JSON).write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    return stats


def ensure_index(root: Path, force: bool = False) -> dict[str, object]:
    stats, _ = ensure_index_ex(root, force)
    return stats


def ensure_index_ex(root: Path, force: bool = False) -> tuple[dict[str, object], bool]:
    """返回 (stats, 是否重建)——CLI 要如实报告缓存命中还是重建。"""
    if force or index_stale(root):
        return build_index(root), True
    try:
        return json.loads((cache_dir(root) / STATS_JSON).read_text(encoding="utf-8")), False
    except (OSError, ValueError):
        return build_index(root), True


def load_index_rows(root: Path) -> list[dict[str, str]]:
    ensure_index(root)
    lines = (cache_dir(root) / PAGES_TSV).read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"))) for line in lines[1:] if line.strip()]


def add_lib_to_path(script_file: str) -> None:
    """给同仓库的 skill 脚本用：把 _lib 加进 sys.path。"""
    import sys
    lib = Path(script_file).resolve().parents[2] / "_lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
