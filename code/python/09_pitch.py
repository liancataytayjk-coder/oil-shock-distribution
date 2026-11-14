"""Short research proposal (pitch), national version: paper/proposal_pitch.md, .docx, .pdf.

Reads the numbers written by 07_papers.py (output/tables/paper_numbers.json) and the national estimates in
output/tables/estimates.csv, draws output/figures/fig09_pitch_national (national pass-through and gap),
and renders paper/pitch_template.md in the house style (one-and-a-half spacing).
"""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

import jinja2  # noqa: E402
import pypandoc  # noqa: E402

from config import FIG, TAB  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PAPER, STYLE = ROOT / "paper", ROOT / "tools" / "lian_style"
OUT = "proposal_pitch"
BLACK, LIGHT = "0.0", "0.85"
plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "lines.linewidth": 1.4,
})


def national_figure():
    e = pd.read_csv(TAB / "estimates.csv")
    core = e[(e.core == 1) & e.cumulative & (e.term == "shock")]
    get = lambda rq, spec, y: core[(core.rq == rq) & (core.spec == spec) & (core.outcome == y)].sort_values("h")  # noqa: E731
    a, b, g = get("RQ1", "baseline", "d_cpi_all"), get("RQ1", "baseline", "d_cpi_b30"), get("RQ2", "national", "d_ratio")
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.9))
    ax[0].fill_between(a.h, a.lo, a.hi, color=LIGHT, linewidth=0)
    ax[0].plot(a.h, a.beta, color=BLACK, marker="o", markersize=3.5, label="All income")
    ax[0].plot(b.h, b.beta, color=BLACK, linestyle="--", marker="s", markersize=3.5, markerfacecolor="white",
               label="Bottom 30%")
    ax[0].set_ylabel("Cumulative response (% per 1% fuel)")
    ax[0].legend(loc="lower right")
    ax[0].set_title("(a) Price level of each group", loc="left", fontsize=9)
    ax[1].fill_between(g.h, g.lo, g.hi, color=LIGHT, linewidth=0)
    ax[1].plot(g.h, g.beta, color=BLACK, marker="o", markersize=3.5)
    ax[1].set_ylabel("Cumulative response (pp per 1% fuel)")
    ax[1].set_title("(b) Inflation gap, all income minus bottom 30%", loc="left", fontsize=9)
    for x in ax:
        x.axhline(0, color=BLACK, linewidth=0.6)
        x.set_xticks(range(0, 13, 2))
        x.set_xlabel("Months after the shock")
    fig.tight_layout()
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / "fig09_pitch_national.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / "fig09_pitch_national.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


def fix_bullets(docx):
    spec = importlib.util.spec_from_file_location("papers", Path(__file__).with_name("07_papers.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.fix_bullets(docx)


def main():
    national_figure()
    n = json.loads((TAB / "paper_numbers.json").read_text())
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(PAPER), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True, comment_start_string="<#--", comment_end_string="--#>")
    text = env.get_template("pitch_template.md").render(
        n=n, author="Lian Cataytay", date="November 2026",
        affiliation="Graduate School of Applied Economics, University of Southeastern Philippines, Davao City")
    md_path, docx = PAPER / f"{OUT}.md", PAPER / f"{OUT}.docx"
    md_path.write_text(text)
    pypandoc.convert_file(str(md_path), "docx", outputfile=str(docx), extra_args=[
        "--citeproc", f"--bibliography={PAPER / 'references.bib'}", f"--resource-path={PAPER}:{ROOT}",
        "--metadata=link-citations:true", f"--reference-doc={STYLE / 'assets' / 'lian-article-reference.docx'}"])
    py = sys.executable
    subprocess.run([py, str(STYLE / "scripts" / "docx_style.py"), "finish", str(docx), "--spacing", "onehalf"],
                   check=True, stdout=subprocess.DEVNULL)
    fix_bullets(docx)
    if shutil.which("soffice"):
        subprocess.run([py, str(STYLE / "scripts" / "render.py"), str(docx), "--outdir", str(PAPER)], check=True,
                       stdout=subprocess.DEVNULL)
    print(f"wrote paper/{OUT}.md, .docx" + (", .pdf" if shutil.which("soffice") else ""))


if __name__ == "__main__":
    main()
