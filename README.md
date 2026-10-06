# Who Pays for Oil Shocks?

Fuel price pass-through to the inflation of poor households across Philippine regions, 2001–2026.
Replication package: raw data, code, results, figures and documents.

## Documents

| File | Contents |
|---|---|
| `docs/master_document.docx` | **Start here.** The full record of data collection, analysis and interpretation, with every other document and all code as appendices |
| `docs/capstone_proposal_FA2.docx` | FA2 capstone proposal, built by `node scripts/12_capstone_proposal.js` |
| `docs/session_handoff.Rmd` | Context and must-upload list for starting a new Claude Code session |
| `docs/analysis_report.docx` | Every analysis and every estimate |
| `paper/working_paper.docx` | Working paper, Chapters 1–6 (three objectives) |
| `paper/manuscript.docx` | Journal manuscript, IMRAD (*Asian Economic Journal*) |
| `paper/SUBMISSION_CHECKLIST.md` | What remains to be done before submission |
| `CLAUDE.md` | Project brief, decision log D1–D11, estimation plans, results summary |
| `data/raw/source_log.md` | Every raw data file with URL, date, base year and coverage |

## Layout

```
data/raw/          untouched downloads (PSA, World Bank, BSP, BIS, FAO, Eurostat) + source_log.md
data/processed/    built by scripts (not committed)
ospd/              local projection estimator (lp.py) and region codes
scripts/           01 download → 02 clean → 03 panel → 04 replication gate → 05 estimates →
                   07 2026 episode → 09 descriptives → 06 figures → 08 papers → 10 report → 11 master
tests/             simulation tests of the estimator
output/tables/     all results as CSV (+ paper_numbers.json)
output/figures/    black-and-white figures (PNG and TIFF 300 dpi, PDF)
paper/             manuscript and working paper (templates, rendered .md/.docx), references.bib
docs/              analysis report, master document, concept note
```

## Reproduce

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh              # rebuild everything from data/raw
./run_all.sh --download   # first re-download the PSA tables
```

All data are public. Licences: PSA (open data), World Bank (CC BY 4.0 / ODbL for the fuel prices database),
Eurostat and European Commission (reuse with attribution), FAO, BIS and BSP (attribution).
