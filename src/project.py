import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from .extensions import md_to_html, parse_frontmatter
from .toctree import resolve_toctree
from .renderer import render_page
from .snippets import extract_snippets
from .sidenotes import footnotes_to_sidenotes


def scan_project(src_dir: Path) -> tuple[dict, list]:
    pages = {}
    for md_path in sorted(src_dir.rglob("*.md")):
        rel = md_path.relative_to(src_dir)
        key = str(rel.with_suffix("")).replace("\\", "/")
        text = md_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        pages[key] = {
            "key": key,
            "title": meta.get("title") or _extract_h1(body) or key,
            "meta": meta,
            "body": body,
            "children": [],
        }

    for key, page in pages.items():
        if key == "index" or key.endswith("/index"):
            folder = str(Path(key).parent)
            if folder == ".":
                folder = ""
            for other in pages:
                if other == key:
                    continue
                other_folder = str(Path(other).parent)
                if other_folder == ".":
                    other_folder = ""
                if other_folder == folder and not other.endswith("/index"):
                    page["children"].append(other)
            page["children"].sort()

    ordered, visited = [], set()

    def dfs(key):
        if key in visited or key not in pages:
            return
        visited.add(key)
        ordered.append(key)
        for child in pages[key].get("children", []):
            dfs(child)

    dfs("index")
    for key in sorted(pages):
        dfs(key)

    return pages, ordered


def _extract_h1(text: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def build(src_dir: Path, out_dir: Path, conf: dict):
    project = conf.get("project", "Apuntes")
    author  = conf.get("author", "")
    lang    = conf.get("language", "es")
    year    = conf.get("year", datetime.now().year)

    print(f"fuente  : {src_dir}")
    print(f"salida  : {out_dir}")
    print(f"proyecto: {project}")

    pages, ordered = scan_project(src_dir)

    if not pages:
        print(f"Error: no se encontraron ficheros .md en {src_dir.resolve()}")
        sys.exit(1)

    print(f"paginas : {len(pages)}")

    out_dir.mkdir(parents=True, exist_ok=True)

    for asset_dir in ["_static", "assets", "img", "images"]:
        src_assets = src_dir / asset_dir
        if src_assets.exists():
            dst_assets = out_dir / asset_dir
            if dst_assets.exists():
                shutil.rmtree(dst_assets)
            shutil.copytree(src_assets, dst_assets)

    for key in ordered:
        page = pages[key]
        body_html, snippets = md_to_html(page["body"])
        body_html = resolve_toctree(body_html, pages, key)
        body_html = footnotes_to_sidenotes(body_html)
        body_html = extract_snippets(body_html, snippets, key, out_dir)

        page_title = page["title"]
        section_id = re.sub(r"[^a-z0-9]+", "-", page_title.lower()).strip("-")
        if not body_html.strip().startswith("<h1"):
            body_html = f'<section id="{section_id}">\n{body_html}\n</section>'

        html = render_page(body_html, page_title, project, lang, author, year)

        out_file = out_dir / (key + ".html")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")
        print(f"  {key}.html")

    print(f"\nlisto: {out_dir}/index.html")
