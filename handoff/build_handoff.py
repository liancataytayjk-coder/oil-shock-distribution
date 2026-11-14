"""Build the handoff package: the guide in Word and PDF, a manifest, and two zip files.

Run from the repository root after ./run_all.sh, tutorial/lp_tutorial.py and tutorial/build_booklet.py:
    .venv/bin/python handoff/build_handoff.py

Writes
  handoff/HANDOFF_GUIDE.docx, .pdf          the guide (from handoff/HANDOFF.md), house style
  handoff/MANIFEST.csv                      every file in the full zip, with size and SHA-256
  handoff/zip/oil-shock_deliverables_2026-11.zip   finished documents, figures, tables, codebook
  handoff/zip/oil-shock_full-project_2026-11.zip   the whole project except .venv, .git and caches
The zip folder is not tracked by Git (see .gitignore).
"""

import csv
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pypandoc
from docx import Document
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[1]
HAND = ROOT / "handoff"
ZIPS = HAND / "zip"
STYLE = ROOT / "tools" / "lian_style"
TAG = "2026-11"
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "deliverables", ".ipynb_checkpoints"}
DELIVERABLES = [
    "handoff/HANDOFF.md", "handoff/HANDOFF_GUIDE.pdf", "handoff/HANDOFF_GUIDE.docx", "README.md", "CLAUDE.md",
    "paper/working_paper.pdf", "paper/working_paper.docx", "paper/article.pdf", "paper/article.docx",
    "paper/proposal_pitch.pdf", "paper/proposal_pitch.docx", "paper/review_matrix.csv",
    "paper/policy_context_2026.md", "tutorial/lp_booklet.pdf", "tutorial/lp_booklet.docx", "tutorial/README.md",
    "codebook/codebook.xlsx", "data/raw/source_log.md",
]
DELIVERABLE_DIRS = ["output/figures", "output/tables", "tutorial/figures"]


def guide():
    md, docx = HAND / "HANDOFF.md", HAND / "HANDOFF_GUIDE.docx"
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
    doc = Document(docx)                                       # code blocks: no first-line indent
    for par in doc.paragraphs:
        if par.style is not None and par.style.name == "Source Code":
            par.paragraph_format.first_line_indent = Inches(0)
            par.paragraph_format.left_indent = Inches(0.25)
            par.paragraph_format.space_after = Inches(0.1)
    doc.save(docx)
    if shutil.which("soffice"):
        subprocess.run([py, str(STYLE / "scripts" / "render.py"), str(docx), "--outdir", str(HAND)], check=True,
                       stdout=subprocess.DEVNULL)
    subprocess.run([py, str(STYLE / "scripts" / "check_style.py"), str(docx)], check=True)


def project_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = Path(dirpath).relative_to(ROOT)
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and rel / d != Path("handoff/zip"))
        for name in sorted(filenames):
            if name.endswith((".pyc", ".tmp")) or name.startswith("~$"):
                continue
            out.append(rel / name)
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_zip(path, files, prefix):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in files:
            z.write(ROOT / rel, f"{prefix}/{rel.as_posix()}")
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise SystemExit(f"corrupt member in {path.name}: {bad}")
        n = len(z.namelist())
    print(f"wrote handoff/zip/{path.name}: {n} files, {path.stat().st_size / 1e6:.1f} MB")


def main():
    guide()
    files = project_files()
    with open(HAND / "MANIFEST.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["path", "bytes", "sha256"])
        for rel in files:
            if rel == Path("handoff/MANIFEST.csv"):
                continue
            w.writerow([rel.as_posix(), (ROOT / rel).stat().st_size, sha256(ROOT / rel)])
    print(f"wrote handoff/MANIFEST.csv: {len(files)} files")
    files = project_files()                                   # now includes the manifest itself
    deliv = [Path(p) for p in DELIVERABLES]
    for d in DELIVERABLE_DIRS:
        deliv += sorted(p.relative_to(ROOT) for p in (ROOT / d).iterdir() if p.is_file())
    missing = [p for p in deliv if not (ROOT / p).exists()]
    if missing:
        raise SystemExit(f"missing deliverables: {missing}")
    write_zip(ZIPS / f"oil-shock_deliverables_{TAG}.zip", deliv, f"oil-shock_deliverables_{TAG}")
    write_zip(ZIPS / f"oil-shock_full-project_{TAG}.zip", files, f"oil-shock-distribution_{TAG}")


if __name__ == "__main__":
    main()
