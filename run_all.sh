#!/usr/bin/env bash
# Rebuild every dataset and table from data/raw. Add --download to refresh PSA tables first.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
if [[ "${1:-}" == "--download" ]]; then $PY scripts/01_download_psa.py --force; $PY scripts/01b_download_poverty.py; fi
$PY scripts/02_clean_psa.py
$PY scripts/03_build_panel.py
$PY scripts/04_replicate.py
$PY scripts/05_estimate.py
$PY scripts/07_episode_2026.py
$PY scripts/09_descriptive.py
$PY scripts/06_figures.py
$PY scripts/08_paper.py
$PY scripts/10_analysis_report.py
$PY -m pytest -q tests
$PY scripts/11_master_document.py
