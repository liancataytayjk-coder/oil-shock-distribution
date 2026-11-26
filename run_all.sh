#!/usr/bin/env bash
# Rebuild everything from data/raw with Python. Add --download to fetch the PSA tables again first.
# The Stata version of the same pipeline is code/stata/00_master.do.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-$(pwd)/.venv/bin/python}
cd code/python
if [[ "${1:-}" == "--download" ]]; then $PY 00_download.py --force; fi
$PY 01_extract_excel.py      # Excel sheets -> data/raw/extracts/*.csv
$PY 02_build_clean.py        # raw -> data/clean/*.csv
$PY 03_descriptive.py        # Objective 1
$PY 04_estimate.py           # RQ1, RQ2, robustness (+ appendix)
$PY 05_policy_2026.py        # RQ3
$PY 06_figures.py            # output/figures
$PY 07_papers.py             # paper/: working paper and article (.md, .docx, .pdf)
$PY 08_codebook.py           # codebook/codebook.xlsx
$PY 09_pitch.py              # paper/proposal_pitch (short national proposal)
$PY 10_panel_study.py        # the panel study: estimates, 2026 block bootstrap, figures (about 9 minutes)
$PY 11_manuscript.py         # paper/manuscript (AEJ): reading version, blinded submission, title page
$PY 12_stata_data.py         # data for the Stata teaching sequence (code/stata/teaching/data/)
cd ../..
$PY tutorial/lp_tutorial.py > /dev/null      # tutorial numbers and figures
$PY tutorial/build_booklet.py                # tutorial/lp_booklet (.md, .docx, .pdf)
$PY study_kit/build_kit.py                   # study_kit/study_kit and stata_tutorial (.md, .docx, .pdf)
$PY code/python/12_stata_data.py zip         # study_kit/stata_pack.zip (do-files, data, tutorial)
$PY -m pytest -q tests
