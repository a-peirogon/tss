import json
import re

import yaml
import markdown
from markdown.preprocessors import Preprocessor
from markdown import Extension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.meta import MetaExtension
from markdown.extensions.attr_list import AttrListExtension


class ToctreePreprocessor(Preprocessor):
    PATTERN = re.compile(r"^:::\s*toctree\s*\n(.*?)^:::\s*$", re.MULTILINE | re.DOTALL)

    def run(self, lines):
        text = "\n".join(lines)
        def replace(m):
            entries = [l.strip() for l in m.group(1).splitlines() if l.strip()]
            return f"<div class='__toctree__' data-entries='{json.dumps(entries)}'></div>"
        return self.PATTERN.sub(replace, text).splitlines()


class ToctreeExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(ToctreePreprocessor(md), "toctree", 175)


class VersionPreprocessor(Preprocessor):
    PATTERN = re.compile(r"^::version:\s*(.+)$", re.MULTILINE)

    def run(self, lines):
        text = "\n".join(lines)
        text = self.PATTERN.sub(
            lambda m: f"<p class='release'>Version: {m.group(1).strip()}</p><hr>", text
        )
        return text.splitlines()


class VersionExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(VersionPreprocessor(md), "version_tag", 174)


MD_EXTENSIONS = [
    FencedCodeExtension(),
    CodeHiliteExtension(guess_lang=False, css_class="highlight"),
    TableExtension(),
    TocExtension(permalink=True, toc_depth="2-4"),
    AdmonitionExtension(),
    MetaExtension(),
    AttrListExtension(),
    ToctreeExtension(),
    VersionExtension(),
    "markdown.extensions.def_list",
    "markdown.extensions.footnotes",
    "markdown.extensions.abbr",
]


def md_to_html(text: str) -> str:
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    return md.convert(text)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    try:
        meta = yaml.safe_load(text[3:end].strip()) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[end + 4:].lstrip("\n")
