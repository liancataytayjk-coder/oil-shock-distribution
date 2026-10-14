# Project layout

```
project/
├── CLAUDE.md                     # brief, reference spec, decisions log, plans, results, open questions
├── README.md                     # what each document is, how to rebuild
├── run_all.sh                    # one-command rebuild (add --download to refresh data)
├── requirements.txt              # pandas statsmodels linearmodels matplotlib jinja2 pypandoc_binary requests openpyxl pyarrow pytest
├── <pkg>/                        # estimator and helpers (lp.py, regions.py)
├── tests/test_lp.py              # simulation tests
├── data/
│   ├── raw/<source>/...          # untouched downloads
│   ├── raw/source_log.md         # one row per raw file
│   └── processed/                # parquet, written by scripts (gitignored)
├── replication/<paper>_targets.csv
├── scripts/
│   ├── 01_download_*.py          # one per source family
│   ├── 02_clean_*.py             # long tables
│   ├── 03_build_panel.py         # analysis panel + flags
│   ├── 04_replicate.py           # replication gate
│   ├── 05_estimate.py            # RQs + robustness → output/tables/estimates.csv
│   ├── 06_figures.py             # all figures, B&W
│   ├── 07_episode_<year>.py      # current-episode / policy analysis
│   ├── 08_paper.py               # numbers dict n + tables → manuscript, working paper
│   ├── 09_descriptive.py         # Objective 1 tables
│   ├── 10_analysis_report.py     # visual report + statistical annex
│   ├── 11_master_document.py     # narrative + every document + all code
│   └── 12_<proposal>.js          # docx-js for Word-exact documents
├── output/{tables,figures}/      # written by scripts
├── paper/                        # *_template.md, references.bib, policy_context.md, SUBMISSION_CHECKLIST.md, rendered .md/.docx
├── docs/                         # concept note, report templates, rendered reports, session_handoff.Rmd
└── deliverables/                 # zips for the user (gitignored)
```

Python 3.11 in `.venv`; docx-js from npm for Word-exact documents; pandoc via
`pypandoc_binary`.
