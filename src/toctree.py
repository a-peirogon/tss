import json
import os
import re
from pathlib import Path


def resolve_toctree(html: str, pages: dict, current_file: str) -> str:
    def replace_node(m):
        try:
            entries = json.loads(m.group(1))
        except json.JSONDecodeError:
            return m.group(0)

        items = []
        for entry in entries:
            if ":" in entry and not entry.startswith("http"):
                path, label = [s.strip() for s in entry.split(":", 1)]
            else:
                path, label = entry.strip(), None

            key = _normalize_key(path, current_file)
            if key in pages:
                label = label or pages[key].get("title", path)
                href = rel_href(current_file, key)
                children = "".join(
                    f'<li class="toctree-l2"><a href="{rel_href(current_file, ck)}">'
                    f'{pages[ck].get("title", ck)}</a></li>'
                    for ck in pages[key].get("children", []) if ck in pages
                )
                items.append(
                    f'<li class="toctree-l1"><a href="{href}">{label}</a>'
                    + (f"<ul>{children}</ul>" if children else "")
                    + "</li>"
                )
            else:
                items.append(
                    f'<li class="toctree-l1"><span style="color:#999">{label or path}</span></li>'
                )

        return f'<div class="toctree-wrapper compound"><ul>{"".join(items)}</ul></div>'

    return re.sub(
        r"<div class='__toctree__' data-entries='([^']*)'>\s*</div>",
        replace_node,
        html,
    )


def _normalize_key(path: str, current: str) -> str:
    path = path.rstrip("/")
    if "/" not in path:
        folder = str(Path(current).parent)
        if folder and folder != ".":
            path = f"{folder}/{path}"
    return path.replace(".md", "") if path.endswith(".md") else path


def rel_href(from_file: str, to_key: str) -> str:
    try:
        rel = os.path.relpath(Path(to_key + ".html"), Path(from_file).parent)
    except ValueError:
        rel = to_key + ".html"
    return rel.replace("\\", "/")
