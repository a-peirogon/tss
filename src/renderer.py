from .css import NATURE_CSS, PYGMENTS_CSS

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title} -- {project}</title>
  <style>
{nature_css}
  </style>
  <style>
{pygments_css}
  </style>
</head>
<body>
<div class="document">
  <div class="documentwrapper">
    <div class="body" role="main">
{body}
    </div>
  </div>
</div>
<div class="footer" role="contentinfo">
  &copy; {year}{author_str} --
  Generado con <a href="#">apuntes.py</a>.
</div>
</body>
</html>
"""


def render_page(
    body_html: str,
    page_title: str,
    project: str,
    lang: str,
    author: str,
    year: int,
) -> str:
    return PAGE_TEMPLATE.format(
        lang=lang,
        page_title=page_title,
        project=project,
        nature_css=NATURE_CSS,
        pygments_css=PYGMENTS_CSS,
        body=body_html,
        year=year,
        author_str=f", {author}" if author else "",
    )
