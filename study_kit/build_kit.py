"""Build the study kit (study_kit/study_kit.md, .docx, .pdf) in the house style.

Run from the repository root after the main pipeline:  .venv/bin/python study_kit/build_kit.py
Text: study_kit/study_kit_template.md (Jinja); numbers: output/tables/paper_numbers.json.
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import jinja2
import pypandoc
from docx import Document
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "study_kit"
STYLE = ROOT / "tools" / "lian_style"


def build(template, out, ctx):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(KIT), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True, comment_start_string="<#--", comment_end_string="--#>")
    text = env.get_template(template).render(**ctx)
    md, docx = KIT / f"{out}.md", KIT / f"{out}.docx"
    md.write_text(text)
    pypandoc.convert_file(str(md), "docx", outputfile=str(docx), extra_args=[
        f"--resource-path={ROOT}", f"--reference-doc={STYLE / 'assets' / 'lian-article-reference.docx'}"])
    py = sys.executable
    subprocess.run([py, str(STYLE / "scripts" / "docx_style.py"), "finish", str(docx), "--spacing", "onehalf"],
                   check=True, stdout=subprocess.DEVNULL)
    spec = importlib.util.spec_from_file_location("papers", ROOT / "code" / "python" / "07_papers.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "code" / "python"))
    spec.loader.exec_module(mod)
    mod.fix_bullets(docx)
    doc = Document(docx)
    for p in doc.paragraphs:                                    # code blocks: no first-line indent
        if p.style is not None and p.style.name == "Source Code":
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Inches(0.1)
    doc.save(docx)
    if shutil.which("soffice"):
        subprocess.run([py, str(STYLE / "scripts" / "render.py"), str(docx), "--outdir", str(KIT)], check=True,
                       stdout=subprocess.DEVNULL)
    subprocess.run([py, str(STYLE / "scripts" / "check_style.py"), str(docx)], check=True)
    print(f"wrote study_kit/{out}.md, .docx" + (", .pdf" if shutil.which("soffice") else ""))


def main():
    n = json.loads((ROOT / "output" / "tables" / "paper_numbers.json").read_text())
    pn = json.loads((ROOT / "output" / "tables" / "panel_numbers.json").read_text())
    ctx = dict(n=n, pn=pn, author="Lian Cataytay", date="November 2026")
    build("study_kit_template.md", "study_kit", ctx)
    build("stata_tutorial_template.md", "stata_tutorial", ctx)


if __name__ == "__main__":
    main()
