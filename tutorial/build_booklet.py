"""Build the local projections booklet (tutorial/lp_booklet.md, .docx, .pdf) in the house style.

Run from the repository root, after tutorial/lp_tutorial.py and the main pipeline:
    .venv/bin/python tutorial/lp_tutorial.py
    .venv/bin/python tutorial/build_booklet.py

Text: tutorial/booklet_src/*.md (Jinja templates). Numbers: tutorial/tutorial_numbers.json (written by
lp_tutorial.py) and output/tables/paper_numbers.json (written by code/python/07_papers.py). The contents
page gets its page numbers from a first rendering of the PDF (two passes).
"""

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import jinja2
import numpy as np
import pandas as pd
import pypandoc
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tutorial" / "booklet_src"
OUT = ROOT / "tutorial"
NAME = "lp_booklet"
STYLE = ROOT / "tools" / "lian_style"
PARTS = ["00_front.md", "01_theory.md", "02_implementation.md", "03_interpretation.md"]
TAB, LVL = "QQTABQQ", "QQL{}QQ"


def f(x, d=3):
    """Format a number with d decimals and a true minus sign."""
    s = f"{float(x):.{d}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace("-", "−")


def context():
    n = json.loads((ROOT / "output" / "tables" / "paper_numbers.json").read_text())
    t = json.loads((OUT / "tutorial_numbers.json").read_text())
    num = lambda s: float(str(s).replace("−", "-").replace("+", ""))  # noqa: E731
    nat = pd.read_csv(ROOT / "data" / "clean" / "national_monthly.csv").set_index("date_str")
    feb, mar = nat.loc["2026-02", "fuel"], nat.loc["2026-03", "fuel"]
    f_mar = 100 * np.log(mar / feb)
    return dict(
        n=n, t=t, f=f, author="Lian Cataytay", date="November 2026",
        fuel_feb26=f"{feb:.1f}", fuel_mar26=f"{mar:.1f}", f_mar26=f(f_mar, 1), f_mar26_round=f"{f_mar:.0f}",
        t_nat6=num(n["rq2_c6"]) / num(n["rq2_c6_se"]),
        within12=f(num(n["rq2_c12"]) - num(n["gap_weights_only"]), 3),
    )


def render_markdown(ctx):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(SRC), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True, comment_start_string="<#--", comment_end_string="--#>")
    return "\n".join(env.get_template(p).render(**ctx) for p in PARTS)


def headings(md):
    """Part (level 1) and chapter (level 2) headings after the contents page, in order."""
    out, in_code = [], False
    for line in md.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = re.match(r"^(#{1,2}) (.+?)\s*(\{.*\})?$", line)
        if m and m.group(2) != "Contents":
            out.append((len(m.group(1)), m.group(2)))
    return out


def contents_block(heads, pages=None):
    lines = []
    for i, (lvl, text) in enumerate(heads):
        plain = re.sub(r"[*_`]", "", text)
        pg = pages[i] if pages else "00"
        lines.append(f"{LVL.format(lvl)}{plain}{TAB}{pg}")
    return "\n\n".join(lines)


def fix_bullets(docx):
    spec = importlib.util.spec_from_file_location("papers", ROOT / "code" / "python" / "07_papers.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "code" / "python"))
    spec.loader.exec_module(mod)
    mod.fix_bullets(docx)


def format_contents(docx):
    """Contents lines get a dotted right tab and the page number; code blocks lose the first-line indent."""
    doc = Document(docx)
    for p in doc.paragraphs:
        if p.style is not None and p.style.name == "Source Code":      # code: no indent, a little air
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_before = Inches(0.06)
            p.paragraph_format.space_after = Inches(0.1)
            continue
        if TAB not in p.text:
            continue
        lvl = 1 if LVL.format(1) in p.text else 2
        title, page = p.text.replace(LVL.format(1), "").replace(LVL.format(2), "").split(TAB)
        for r in p.runs[1:]:
            r._element.getparent().remove(r._element)
        run = p.runs[0]
        run.text = f"{title}\t{page}"
        run.bold = lvl == 1
        pf = p.paragraph_format
        pf.first_line_indent = Inches(0)
        pf.left_indent = Inches(0 if lvl == 1 else 0.3)
        pf.space_before = Inches(0.08 if lvl == 1 else 0)
        pf.space_after = Inches(0)
        pf.line_spacing = 1.15
        pf.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    doc.save(docx)


def build(md):
    md_path, docx = OUT / f"{NAME}.md", OUT / f"{NAME}.docx"
    md_path.write_text(md)
    pypandoc.convert_file(str(md_path), "docx", outputfile=str(docx), extra_args=[
        "--citeproc", f"--bibliography={ROOT / 'paper' / 'references.bib'}", f"--bibliography={SRC / 'extra.bib'}",
        f"--resource-path={ROOT}", "--metadata=link-citations:true",
        f"--reference-doc={STYLE / 'assets' / 'lian-article-reference.docx'}"])
    py = sys.executable
    subprocess.run([py, str(STYLE / "scripts" / "docx_style.py"), "finish", str(docx), "--spacing", "onehalf"],
                   check=True, stdout=subprocess.DEVNULL)
    fix_bullets(docx)
    format_contents(docx)
    subprocess.run([py, str(STYLE / "scripts" / "render.py"), str(docx), "--outdir", str(OUT)], check=True,
                   stdout=subprocess.DEVNULL)
    return OUT / f"{NAME}.pdf"


def page_numbers(pdf, heads):
    """Page of each heading in the body: the first page, after the previous heading's, with a line that starts
    with the heading text and has no dot leader (which marks the contents page)."""
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')).strip()  # noqa: E731
    pages = [[norm(ln) for ln in pg.splitlines()] for pg in txt.split("\f")]
    out, start = [], 0
    for _, text in heads:
        key = norm(re.sub(r"[*_`$\\]", "", text))[:40]
        for i in range(start, len(pages)):
            if any(ln.startswith(key) and "...." not in ln for ln in pages[i]):
                out.append(str(i + 1))
                start = i
                break
        else:
            raise SystemExit(f"heading not found in the PDF: {text}")
    return out


def main():
    if not shutil.which("soffice") or not shutil.which("pdftotext"):
        raise SystemExit("needs LibreOffice (soffice) and pdftotext")
    md = render_markdown(context())
    heads = headings(md.split("<!--CONTENTS-->", 1)[1])
    pdf = build(md.replace("<!--CONTENTS-->", contents_block(heads)))
    pages = page_numbers(pdf, heads)
    pdf = build(md.replace("<!--CONTENTS-->", contents_block(heads, pages)))
    if page_numbers(pdf, heads) != pages:
        print("warning: page numbers moved in the second pass")
    print(f"wrote tutorial/{NAME}.md, .docx, .pdf")


if __name__ == "__main__":
    main()
