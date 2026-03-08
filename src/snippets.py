"""
Extraccion de snippets de codigo en dos fases:

1. SnippetCollector (preprocesador Markdown): recorre los bloques de codigo
   vallados, guarda (lang, codigo) en orden y pasa el texto sin cambios.

2. extract_snippets (post-procesador HTML): recorre los <div class="highlight">
   en el mismo orden, guarda los archivos y envuelve cada bloque con un enlace
   de descarga.
"""

import re
import html as html_lib
from pathlib import Path

from markdown.preprocessors import Preprocessor
from markdown import Extension

LANG_EXT: dict[str, str] = {
    "lean":       "lean",
    "python":     "py",
    "py":         "py",
    "bash":       "sh",
    "sh":         "sh",
    "haskell":    "hs",
    "rust":       "rs",
    "c":          "c",
    "cpp":        "cpp",
    "java":       "java",
    "javascript": "js",
    "js":         "js",
    "typescript": "ts",
    "ts":         "ts",
    "nix":        "nix",
    "ocaml":      "ml",
    "coq":        "v",
    "agda":       "agda",
    "sql":        "sql",
    "yaml":       "yaml",
    "toml":       "toml",
    "json":       "json",
}

_FENCE_RE = re.compile(
    r"^(?P<fence>```+|~~~+)[ \t]*(?P<lang>[a-zA-Z0-9_+\-]*)[ \t]*\n"
    r"(?P<code>.*?)"
    r"^(?P=fence)[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

SNIPPET_STYLE = """\
<style>
.snippet-wrap { position: relative; }
.snippet-dl {
    position: absolute;
    top: 5px; right: 8px;
    font-size: .75em;
    font-family: sans-serif;
    background: #eaecf0;
    border: 1px solid #a2a9b1;
    border-radius: 3px;
    padding: 1px 7px;
    color: #0645ad;
    text-decoration: none;
    opacity: .75;
    z-index: 10;
}
.snippet-dl:hover { opacity: 1; text-decoration: underline; }
</style>
"""


class SnippetCollector(Preprocessor):
    """Recorre los bloques vallados y acumula (lang, code) en self.md.snippets."""

    def run(self, lines: list[str]) -> list[str]:
        text = "\n".join(lines)
        self.md.snippets = []  # type: ignore[attr-defined]
        for m in _FENCE_RE.finditer(text):
            lang = m.group("lang").lower()
            code = m.group("code")
            if lang in LANG_EXT:
                self.md.snippets.append((lang, code))
        return lines  # sin modificar; fenced_code los procesara despues


class SnippetCollectorExtension(Extension):
    def extendMarkdown(self, md):
        # Prioridad 176: justo antes de ToctreePreprocessor (175) y
        # antes de FencedCodeExtension (que se registra en 25)
        md.preprocessors.register(SnippetCollector(md), "snippet_collector", 176)


# ── Post-procesador HTML ──────────────────────────────────────────────────────

_HIGHLIGHT_RE = re.compile(
    r'<div class="highlight"><pre>(?P<inner>.*?)</pre>\s*</div>',
    re.DOTALL,
)


def _flat(page_key: str) -> str:
    return page_key.replace("/", "_")


def extract_snippets(
    html: str,
    snippets: list[tuple[str, str]],
    page_key: str,
    out_dir: Path,
) -> str:
    """
    Para cada <div class="highlight"> en el HTML, si existe un snippet
    capturado en la misma posicion, guarda el archivo y añade el enlace.
    """
    if not snippets:
        return html

    snippets_dir = out_dir / "_snippets" / _flat(page_key)
    counters: dict[str, int] = {}
    snippet_iter = iter(snippets)
    style_injected = False

    def replace(m: re.Match) -> str:
        nonlocal style_injected

        entry = next(snippet_iter, None)
        if entry is None:
            return m.group(0)

        lang, code = entry
        counters[lang] = counters.get(lang, 0) + 1
        n = counters[lang]

        fname = f"{_flat(page_key)}-{lang}-{n}.{LANG_EXT[lang]}"
        snippets_dir.mkdir(parents=True, exist_ok=True)
        (snippets_dir / fname).write_text(code, encoding="utf-8")

        depth = len(Path(page_key).parts) - 1
        prefix = "../" * depth
        href = f"{prefix}_snippets/{_flat(page_key)}/{fname}"

        style = SNIPPET_STYLE if not style_injected else ""
        style_injected = True

        inner = m.group("inner")
        return (
            f"{style}"
            f'<div class="snippet-wrap">'
            f'<a class="snippet-dl" href="{href}" download="{fname}"'
            f' title="Descargar {fname}">{lang} \u2193</a>'
            f'<div class="highlight"><pre>{inner}</pre></div>'
            f'</div>'
        )

    return _HIGHLIGHT_RE.sub(replace, html)
