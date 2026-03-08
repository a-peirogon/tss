from pygments.formatters import HtmlFormatter

NATURE_CSS = """
/* ============================================================
   TUFTE LAYOUT — lambdanotes
   Text column: ~620px left-aligned
   Sidenote margin: ~340px right, outside the text column
   ============================================================ */

/* ── Web fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Code+Pro:wght@400;600&display=swap');

/* ── Reset / base ───────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html { font-size: 16px; }

body {
    background: #fffff8;
    color: #111;
    font-family: 'Libre Baskerville', Palatino, 'Book Antiqua', Georgia, serif;
    font-size: 1rem;
    line-height: 1.7;
    margin: 0;
    padding: 0;
}

/* ── Page skeleton ──────────────────────────────────────────── */
/*
   .document
     .documentwrapper          (overflow:visible, position:relative)
       .body                   (max-width 620px, left-aligned, overflow:visible)
         <content>
         .sidenote / .marginnote  (float:right, negative margin-right → right gutter)
*/

div.document {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

div.documentwrapper {
    position: relative;
    overflow: visible;
}

div.body {
    max-width: 620px;
    margin-left: 6%;        /* small left indent — sidenotes live in the remaining ~58% */
    margin-right: 0;
    overflow: visible;      /* critical: allows sidenotes to escape to the right */
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* ── Sidenotes & margin notes ───────────────────────────────── */
/*  Placed *inside* a paragraph or element; float:right + negative
    margin-right pulls them out of the text column into the gutter.  */

.sidenote,
.marginnote {
    float: right;
    clear: right;
    margin-right: -58%;     /* escape the body column */
    width: 50%;             /* relative to .body — lands in the right gutter */
    margin-top: 0.1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    line-height: 1.55;
    font-style: normal;
    color: #444;
    vertical-align: baseline;
    position: relative;
}

/* Numbered sidenote label (the superscript in running text) */
label.sidenote-number {
    counter-increment: sidenote-counter;
}
label.sidenote-number::after,
span.sidenote-number::after {
    content: counter(sidenote-counter);
    font-size: 0.7rem;
    top: -0.5em;
    position: relative;
    vertical-align: baseline;
    color: #666;
    font-variant-numeric: lining-nums;
}

/* Number inside the sidenote itself */
.sidenote::before {
    content: counter(sidenote-counter) " ";
    font-size: 0.7rem;
    top: -0.5em;
    position: relative;
    vertical-align: baseline;
    color: #666;
}

/* Checkbox toggle for narrow screens */
input.margin-toggle { display: none; }
label.margin-toggle:not(.sidenote-number) { display: none; }

@media (max-width: 900px) {
    label.margin-toggle:not(.sidenote-number) {
        display: inline;
        color: #60A5FA;
        cursor: pointer;
    }
    .sidenote, .marginnote {
        display: none;
        float: left;
        clear: both;
        width: 95%;
        margin: 0.8rem 2.5%;
        font-size: 0.88rem;
        background: #f5f5ee;
        border-left: 3px solid #ccc;
        padding: 0.4rem 0.6rem;
    }
    input.margin-toggle:checked + .sidenote,
    input.margin-toggle:checked + .marginnote {
        display: block;
    }
}

/* ── Typography ─────────────────────────────────────────────── */

div.body h1,
div.body h2,
div.body h3,
div.body h4,
div.body h5,
div.body h6 {
    font-weight: 700;
    line-height: 1.25;
    margin-top: 2.2rem;
    margin-bottom: 0.6rem;
    color: #1a1a1a;
}

div.body h1 { font-size: 2rem; margin-top: 0; border-bottom: 2px solid #e5e5e5; padding-bottom: 0.3rem; }
div.body h2 { font-size: 1.45rem; border-bottom: 1px solid #e5e5e5; padding-bottom: 0.2rem; }
div.body h3 { font-size: 1.15rem; }
div.body h4 { font-size: 1rem; font-style: italic; }

div.body p  { margin: 0.9rem 0; }

div.body a {
    color: #1a56a0;
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 2px;
}
div.body a:hover { color: #0d3d7a; }

/* Permalink anchors from TocExtension */
div.body a.headerlink {
    color: #bbb;
    font-size: 0.75em;
    margin-left: 0.4em;
    text-decoration: none;
}
div.body a.headerlink:hover { color: #666; }

/* ── Lists ──────────────────────────────────────────────────── */
div.body ul,
div.body ol {
    padding-left: 1.8em;
    margin: 0.6rem 0 0.9rem;
}
div.body li { line-height: 1.65; margin-bottom: 0.2rem; }

/* ── Blockquote ─────────────────────────────────────────────── */
div.body blockquote {
    border-left: 3px solid #bbb;
    margin: 1rem 0 1rem 1.5rem;
    padding: 0.1rem 0.8rem;
    color: #555;
    font-style: italic;
}

/* ── Inline code ─────────────────────────────────────────────── */
code {
    background: #f0f0ea;
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 1px 5px;
    font-size: 0.87em;
    font-family: 'Source Code Pro', 'Droid Sans Mono', 'Liberation Mono', Courier, monospace;
}

/* ── Code blocks ─────────────────────────────────────────────── */
div.body pre {
    background: #f7f7f2;
    border: 1px solid #e0e0d8;
    border-left: 4px solid #c0b890;
    border-radius: 3px;
    padding: 0.8rem 1rem;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.5;
    font-family: 'Source Code Pro', 'Droid Sans Mono', monospace;
}
div.body pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: 1em;
}

/* ── Tables ──────────────────────────────────────────────────── */
div.body table {
    border-collapse: collapse;
    margin: 1.2rem 0;
    width: 100%;
    font-size: 0.92em;
}
div.body table th {
    background: #e8e8e0;
    padding: 5px 10px;
    border: 1px solid #ccc;
    text-align: left;
    font-weight: 700;
}
div.body table td {
    padding: 4px 10px;
    border: 1px solid #ddd;
}
div.body table tr:nth-child(even) { background: #f5f5ee; }
div.body table tr:nth-child(odd)  { background: #fffff8; }

/* ── Horizontal rule ─────────────────────────────────────────── */
hr { border: none; border-top: 1px solid #ddd; margin: 1.8rem 0; }

/* ── Version tag ─────────────────────────────────────────────── */
p.release {
    font-size: 0.82rem;
    color: #888;
    font-style: italic;
}

/* ── Admonitions ─────────────────────────────────────────────── */
div.admonition {
    border-radius: 4px;
    padding: 0.6rem 0.9rem;
    margin: 1.2rem 0;
    border-left: 4px solid #aaa;
    background: #f9f9f2;
    font-size: 0.93em;
}
p.admonition-title {
    font-weight: bold;
    margin: 0 0 0.3rem;
    text-transform: uppercase;
    font-size: 0.78em;
    letter-spacing: 0.05em;
}
p.admonition-title::after { content: ""; }

div.note     { border-color: #7ba7bc; background: #eef4f8; }
div.tip      { border-color: #6aab6a; background: #eef7ee; }
div.warning  { border-color: #d4a843; background: #fdf6e3; }
div.important{ border-color: #c0534a; background: #fdf0ef; }
div.caution  { border-color: #d4a843; background: #fdf6e3; }
div.danger   { border-color: #c0534a; background: #fdf0ef; }
div.hint     { border-color: #6aab6a; background: #eef7ee; }

/* ── Toctree ─────────────────────────────────────────────────── */
div.toctree-wrapper {
    background: #f9f9f2;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.8rem 1rem;
    margin: 1.2rem 0;
    display: inline-block;
    min-width: 240px;
}
div.toctree-wrapper ul { margin: 0; padding: 0; }

li.toctree-l1 {
    list-style: none;
    font-size: 1rem;
    font-weight: 700;
    padding: 0.3rem 0;
    border-bottom: 1px solid #eee;
}
li.toctree-l1:last-child { border-bottom: none; }
li.toctree-l1 > a { color: #1a56a0; text-decoration: none; }
li.toctree-l1 > a:hover { text-decoration: underline; }

li.toctree-l1 ul { padding-left: 1rem; margin-top: 0.3rem; }
li.toctree-l2 {
    list-style: square;
    font-size: 0.88rem;
    font-weight: 400;
    padding: 0.15rem 0;
}
li.toctree-l2 > a { color: #1a56a0; text-decoration: none; }
li.toctree-l2 > a:hover { text-decoration: underline; }

/* ── Footer ──────────────────────────────────────────────────── */
div.footer {
    max-width: 1200px;
    margin: 2rem auto 0;
    padding: 1rem 1.5rem 1rem calc(6% + 1.5rem);
    border-top: 1px solid #ddd;
    font-size: 0.8rem;
    color: #999;
}
div.footer a { color: #888; text-decoration: none; }
div.footer a:hover { text-decoration: underline; }

/* ── Images ──────────────────────────────────────────────────── */
div.body img {
    max-width: 100%;
    height: auto;
    border-radius: 3px;
    display: block;
    margin: 1rem auto;
}

/* ── TOC (inline, from TocExtension) ────────────────────────── */
div.toc {
    background: #f5f5ee;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.6rem 1rem;
    display: inline-block;
    font-size: 0.88em;
    margin: 1rem 0;
}
div.toc ul { padding-left: 1.4em; margin: 0.2rem 0; }
div.toc li { list-style: none; padding: 0.1rem 0; }
div.toc a  { color: #1a56a0; text-decoration: none; }
div.toc a:hover { text-decoration: underline; }

/* ── Definition lists ────────────────────────────────────────── */
div.body dt { font-weight: bold; margin-top: 0.6rem; }
div.body dd { margin-left: 1.6rem; margin-bottom: 0.4rem; }
"""

PYGMENTS_CSS = HtmlFormatter(style="friendly").get_style_defs(".highlight")
