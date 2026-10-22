"""Make the course submission files in the house style, with PDFs.

FA2: docs/capstone_proposal_FA2.docx (scripts/12_capstone_proposal.js), single-spaced
     to stay within the 10-page limit.
SA3: paper/capstone_paper.docx (scripts/08_paper.py), double-spaced, with the data
     appendix; docs/presentation_SA3.pptx (scripts/13_presentation.py).

Each Word file is copied to submissions/, passed through the house-style finisher
(tools/lian_style), converted to PDF with LibreOffice and audited with check_style.
Needs LibreOffice Writer and Impress (apt-get install libreoffice-writer
libreoffice-impress libreoffice-math).
"""

import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools" / "lian_style" / "scripts"
OUT = ROOT / "submissions"

JOBS = [  # source, submission name, spacing (None for decks)
    (ROOT / "docs" / "capstone_proposal_FA2.docx", "FA2_Capstone_Proposal.docx", "single"),
    (ROOT / "paper" / "capstone_paper.docx", "SA3_Capstone_Paper.docx", "double"),
    (ROOT / "docs" / "presentation_SA3.pptx", "SA3_Presentation.pptx", None),
]


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True)


def fix_bullets(docx):
    """Give pandoc's bullet lists a visible Times New Roman bullet (the symbol-font glyph is lost)."""
    tmp = docx.with_suffix(".tmp")
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/numbering.xml":
                xml = data.decode("utf-8")

                def lvl(m):
                    block = m.group(0)
                    if 'w:numFmt w:val="bullet"' not in block:
                        return block
                    glyph = "•" if m.group(1) in ("0", "2", "4", "6", "8") else "–"
                    block = re.sub(r'<w:lvlText w:val="[^"]*"/>', f'<w:lvlText w:val="{glyph}"/>', block)
                    return re.sub(r'<w:rFonts [^>]*/>', '<w:rFonts w:ascii="Times New Roman" '
                                  'w:hAnsi="Times New Roman" w:cs="Times New Roman"/>', block)

                xml = re.sub(r'<w:lvl w:ilvl="(\d)".*?</w:lvl>', lvl, xml, flags=re.S)
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(docx)


def main():
    OUT.mkdir(exist_ok=True)
    for src, name, spacing in JOBS:
        dst = OUT / name
        shutil.copyfile(src, dst)
        if spacing:
            run(TOOLS / "docx_style.py", "finish", dst, "--spacing", spacing)
            fix_bullets(dst)
        run(TOOLS / "render.py", dst, "--outdir", OUT)
        run(TOOLS / "check_style.py", dst)


if __name__ == "__main__":
    main()
