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
cd ../..
$PY -m pytest -q tests
