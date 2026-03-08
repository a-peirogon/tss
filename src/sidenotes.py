"""
Convierte las notas al pie generadas por python-markdown en sidenotes
al estilo Tufte, que aparecen en el margen derecho fuera de la columna
de texto principal.

Sintaxis en Markdown (igual que notas al pie estándar):

    Texto normal con una nota[^1] al margen.

    [^1]: Esto aparecerá en el margen derecho, no al pie de página.

El HTML resultante usa el patrón label/checkbox/span de Tufte CSS,
que en pantallas anchas flota en el margen y en móvil es colapsable.
"""

import re


# ── Patrones del HTML generado por python-markdown footnotes ──────────────

# Referencia inline: <sup id="fnref:label"><a class="footnote-ref" href="#fn:label">N</a></sup>
_FNREF_RE = re.compile(
    r'<sup\s+id="fnref:(?P<key>[^"]+)">'
    r'<a\s[^>]*class="footnote-ref"[^>]*>\d+</a>'
    r'</sup>',
    re.DOTALL,
)

# Bloque al pie: <div class="footnote"> ... </div>
_FNBLOCK_RE = re.compile(
    r'<div\s+class="footnote">.*?</div>',
    re.DOTALL,
)

# Cada <li> dentro del bloque: <li id="fn:key"><p>...texto...<a ...>↩</a></p></li>
_FNITEM_RE = re.compile(
    r'<li\s+id="fn:(?P<key>[^"]+)">\s*<p>(?P<body>.*?)'
    r'<a\s[^>]*class="footnote-backref"[^>]*>[^<]*</a>\s*</p>\s*</li>',
    re.DOTALL,
)


def _extract_footnotes(html: str) -> dict[str, str]:
    """Devuelve {key: contenido_html} de todas las notas al pie."""
    block_m = _FNBLOCK_RE.search(html)
    if not block_m:
        return {}
    footnotes: dict[str, str] = {}
    for m in _FNITEM_RE.finditer(block_m.group(0)):
        footnotes[m.group("key")] = m.group("body").strip()
    return footnotes


def footnotes_to_sidenotes(html: str) -> str:
    """
    Reemplaza las referencias a notas al pie por sidenotes Tufte inline y
    elimina el bloque <div class="footnote"> del final de la página.
    """
    footnotes = _extract_footnotes(html)
    if not footnotes:
        return html

    counter = [0]

    def _replace_ref(m: re.Match) -> str:
        key = m.group("key")
        content = footnotes.get(key)
        if content is None:
            return m.group(0)          # referencia huérfana: dejar tal cual

        counter[0] += 1
        n = counter[0]

        # Tufte sidenote: label (número visible) + checkbox (toggle móvil) + span
        return (
            f'<label for="sn-{n}" class="margin-toggle sidenote-number"></label>'
            f'<input type="checkbox" id="sn-{n}" class="margin-toggle"/>'
            f'<span class="sidenote">{content}</span>'
        )

    html = _FNREF_RE.sub(_replace_ref, html)

    # Quitar el bloque de notas al pie del final
    html = _FNBLOCK_RE.sub("", html)

    return html
