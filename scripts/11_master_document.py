"""Assemble the Master Document: process narrative plus every project document and all code.

Renders docs/master_narrative_template.md with the paper numbers, then appends each
document (front matter removed, headings demoted, reference lists merged) and the
complete source code. Writes docs/master_document.md and docs/master_document.docx.
"""

import json
import re
import subprocess
from pathlib import Path

import jinja2
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

APPENDICES = [
    ("A", "Concept note", "docs/concept_note.md"),
    ("B", "Project brief and decision log (CLAUDE.md)", "CLAUDE.md"),
    ("C", "Data source log", "data/raw/source_log.md"),
    ("D", "2026 policy context with sources", "paper/policy_context_2026.md"),
    ("E", "Analysis and results report", "docs/analysis_report.md"),
    ("F", "Working paper", "paper/working_paper.md"),
    ("G", "Journal manuscript (IMRAD)", "paper/manuscript.md"),
    ("H", "Submission checklist", "paper/SUBMISSION_CHECKLIST.md"),
]
CODE = ["run_all.sh", "requirements.txt", "ospd/lp.py", "ospd/regions.py", "scripts/01_download_psa.py",
        "scripts/01b_download_poverty.py", "scripts/02_clean_psa.py", "scripts/03_build_panel.py",
        "scripts/04_replicate.py", "scripts/05_estimate.py", "scripts/06_figures.py", "scripts/07_episode_2026.py",
        "scripts/08_paper.py", "scripts/09_descriptive.py", "scripts/10_analysis_report.py",
        "scripts/11_master_document.py", "tests/test_lp.py"]


def prepare(text, levels=1):
    """Drop YAML front matter (keep title/subtitle as a line), demote headings, remove reference divs."""
    title = ""
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if m:
        meta = m.group(1)
        t = re.search(r'^title:\s*"?(.*?)"?\s*$', meta, flags=re.M)
        st = re.search(r'^subtitle:\s*"?(.*?)"?\s*$', meta, flags=re.M)
        ab = re.search(r"^abstract:\s*\|\n((?:  .*\n?)+)", meta, flags=re.M)
        title = "".join([f"**{t.group(1)}**" if t else "", f" — {st.group(1)}" if st else "", "\n\n"])
        if ab:
            title += "**Abstract.** " + " ".join(line.strip() for line in ab.group(1).splitlines()) + "\n\n"
        text = text[m.end():]
    text = re.sub(r"::: \{#refs\}\n:::\n?", "", text)
    out, in_code = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{1,5} ", line):
            line = "#" * levels + line
        out.append(line)
    return title + "\n".join(out)


def main():
    n = json.loads((ROOT / "output" / "tables" / "paper_numbers.json").read_text())
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(DOCS), undefined=jinja2.StrictUndefined,
                             comment_start_string="<#--", comment_end_string="--#>")
    parts = [env.get_template("master_narrative_template.md").render(n=n)]
    for letter, title, path in APPENDICES:
        body = (ROOT / path).read_text()
        if letter not in ("F", "G"):  # only the papers contain citations; elsewhere "@" is literal
            body = re.sub(r"(?<![\\\w])@", r"\\@", body)
        parts.append(f"\n\n# Appendix {letter}. {title}\n\n*Source file: `{path}`*\n\n" + prepare(body, levels=1))
    bib = (ROOT / "paper" / "references.bib").read_text()
    parts.append("\n\n# Appendix I. Bibliography file\n\n*Source file: `paper/references.bib`*\n\n```bibtex\n"
                 + bib + "\n```\n")
    parts.append("\n\n# Appendix J. Complete source code\n\nThe files below are the complete code of the study, "
                 "in the order they run.\n")
    for path in CODE:
        lang = {"py": "python", "sh": "bash", "txt": "text"}[path.rsplit(".", 1)[-1]]
        parts.append(f"\n## {path}\n\n```{lang}\n{(ROOT / path).read_text()}\n```\n")
    try:
        log = subprocess.run(["git", "log", "--format=%h %ad %s", "--date=short"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except Exception:  # noqa: BLE001
        log = "(git history not available)"
    parts.append("\n\n# Appendix K. Version history (git log)\n\n```text\n" + log + "\n```\n")
    parts.append("\n\n# References\n\n::: {#refs}\n:::\n")
    text = "".join(parts)
    (DOCS / "master_document.md").write_text(text)
    pypandoc.convert_text(text, "docx", format="markdown", outputfile=str(DOCS / "master_document.docx"),
                          extra_args=["--citeproc", f"--bibliography={ROOT / 'paper' / 'references.bib'}",
                                      f"--resource-path={DOCS}:{ROOT / 'paper'}:{ROOT}", "--toc", "--toc-depth=2",
                                      "--metadata=title:Master Document — Who Pays for Oil Shocks?"])
    print("wrote docs/master_document.md and .docx;", len(text.split()), "words")


if __name__ == "__main__":
    main()
