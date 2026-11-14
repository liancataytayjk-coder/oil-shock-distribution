---
title: "Who Pays for Oil Shocks? Project Handoff and Guide"
subtitle: "Fuel price pass-through to the inflation of poor households in the Philippines (version 2)"
author: "Lian Cataytay"
date: "November 2026"
---

# 1. What this project is

This study asks whether rising fuel prices hurt poor Filipino households more than the average household. It replicates the local projection design of Kpodar and Liu (2022, *Energy Economics* 108) on official Philippine data: the Philippine Statistics Authority (PSA) consumer price index (CPI) for all households, the CPI for the bottom 30% of households by income, and the PSA's pump price index (CPI sub-index 07.2.2), nationally and for 17 regions, monthly from 2001 to August 2026. The target journal is the *Asian Economic Journal*.

The study has three objectives and three research questions. Objective 1 describes the data (trends, fuel price episodes, the inflation gap). Objective 2 estimates how much fuel prices pass through to the prices of both groups (RQ1) and whether the poor pay more, and why (RQ2). Objective 3 applies the estimates to the 2026 oil shock, puts a peso value on its cost to a poor family and assesses the policy responses (RQ3).

**Status at handoff (14 November 2026).** All analyses are finished and every document is built. The whole pipeline was re-run from the raw data on the handoff date: all five automated tests pass, every document passes the house-style check, and no number or text changed from the committed version. All work is on the Git branch `claude/bold-hamilton-0ixcim`.

# 2. Start here: the documents

Table: Table 1. The finished documents (each in Word and PDF).

| Document | File | Pages | Use |
|------------------|------------------------------|-------:|----------------------------------------|
| Working paper (chapter form) | `paper/working_paper.pdf` / `.docx` | 54 | The full study: Chapters 1–5 and Appendices A (review matrix), B (supplementary results) and C (data) |
| Journal article (IMRAD) | `paper/article.pdf` / `.docx` | 27 | Draft for the *Asian Economic Journal*, with an online appendix |
| Research proposal, national pitch | `paper/proposal_pitch.pdf` / `.docx` | 11 | Short, national-only proposal that sells the idea: why it matters, how others answered it, how we answer it with Philippine data |
| Local projections booklet | `tutorial/lp_booklet.pdf` / `.docx` | 37 | Teaching booklet: theory, code step by step, interpretation, exercises with answers |
| Local projections tutorial (web) | `tutorial/README.md` | | Short GitHub version of the booklet |
| Codebook | `codebook/codebook.xlsx` | | Every variable, its source and its definition |

The figures are in `output/figures/` (PNG at 300 dpi, TIFF for journals, PDF), and the tables in `output/tables/`. The file `output/tables/estimates.csv` holds every estimate (column `core` = 1 marks the main-text results), and `output/tables/paper_numbers.json` holds the 230 numbers quoted in the papers.

# 3. Key results in brief

**RQ1, pass-through.** A 1% rise in pump prices raises the all-income price level by 0.044% within the month, 0.087% after six months and 0.102% after a year; the bottom-30% price level responds almost identically (0.044, 0.095 and 0.102). A 10% rise in pump prices makes prices about 1% higher a year later. World crude prices capture only about 40% of this.

**RQ2, who pays more.** The effect is not progressive, contrary to the cross-country finding. The inflation gap (all-income minus bottom-30% inflation) responds negatively: nationally −0.0155 after six months, significant only at 3, 4, 7 and 8 months; in the 17-region panel −0.0214 (standard error 0.0084), significant from 3 to 12 months. Budget shares alone would predict a progressive gap (+0.0101), so the regressive sign comes from larger price increases within the categories the poor buy (housing and household fuels, food). The gap shrinks with macroeconomic controls (−0.0046) and is concentrated in 2001–2012 (−0.0541 against −0.0091 since 2013); leaving out any one region changes little (−0.0227 to −0.0203).

**RQ3, the 2026 shock.** A model estimated only on data to December 2025 explains 2.55 of the 4.81% rise in the all-income price level and 3.13 of the 5.98% rise for the bottom 30% between December 2025 and August 2026. The fuel-driven cost to a family of five at the poverty line is about PHP 467 a month (PHP 390–633 across regions); the total extra cost was about PHP 907. Rice and other cereals account for +1.67 points of the poor's +1.24-point excess price rise.

# 4. What is in the zip files

The handoff comes with two zip files in `handoff/zip/`. They are not stored in Git because of their size; rebuild them with `.venv/bin/python handoff/build_handoff.py`.

**`oil-shock_deliverables_2026-11.zip`** holds only the finished outputs, for reading and sharing: this guide (Word and PDF), the working paper, the article, the pitch proposal, the booklet and the tutorial, all figures and tables, and the codebook.

**`oil-shock_full-project_2026-11.zip`** holds the complete project, everything needed to rebuild every number: the code, the raw and clean data, all outputs and documents, the templates, the house-style tools, the tests, the tutorial and the version 1 archive. It leaves out only the Python environment (`.venv`), which is rebuilt from `requirements.txt`, and Git's internal files.

`handoff/MANIFEST.csv` lists every file in the full zip with its size and SHA-256 checksum, so you can confirm that nothing was lost or changed in transfer.

# 5. Folder map

Table: Table 2. Where everything is.

| Folder or file | Contents |
|---|---|
| `CLAUDE.md` | Project brief: structure, conventions, decisions log (D1–D12), key results, open questions |
| `README.md` | Short index of the repository |
| `run_all.sh` | Rebuilds everything from the raw data and runs the tests |
| `requirements.txt` | Python packages |
| `code/python/` | The pipeline, scripts `00`–`09`; `lp.py` is the estimator, `config.py` the settings, `catalog.py` the source and results map |
| `data/raw/` | Untouched downloads (PSA, World Bank, BSP, BIS, FAO), logged in `data/raw/source_log.md` |
| `data/clean/` | Analysis files: `national_monthly.csv`, `regional_panel.csv`, weights, region information, 2026 items |
| `output/tables/`, `output/figures/` | All results (written by scripts only) |
| `paper/` | Templates (`*_template.md`), the review matrix, the bibliography, and the built documents |
| `tutorial/` | The tutorial, the booklet, their sources and the script that prints every tutorial number |
| `codebook/` | `codebook.xlsx` |
| `tools/lian_style/` | House style: Word reference document, `docx_style.py`, `render.py`, `check_style.py` |
| `tests/` | Automated tests of the estimator (simulated data with known answers) |
| `handoff/` | This guide, the manifest and the handoff build script |
| `archive/v1_full/` | Version 1, unchanged: the 51-page working paper, the journal draft, the EU replication gate, all robustness checks, the FA2 proposal and SA3 submissions |

# 6. How to rebuild everything

You need Python 3.11, LibreOffice (Writer and Math, for the PDFs) and `pdftotext` (for the booklet's page numbers). From the project's top folder:

```bash
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
./run_all.sh
.venv/bin/python tutorial/lp_tutorial.py
.venv/bin/python tutorial/build_booklet.py
.venv/bin/python handoff/build_handoff.py
```

The first two lines create the Python environment. `run_all.sh` rebuilds the data, the results, the papers, the pitch proposal and the codebook and runs the tests (about four minutes). The last three lines rebuild the tutorial numbers and figures, the booklet, and this guide with its manifest and zip files.

`run_all.sh` runs, in order: `01_extract_excel.py` (copies the Excel columns used into CSV), `02_build_clean.py` (builds the clean data), `03_descriptive.py` (Objective 1), `04_estimate.py` (RQ1, RQ2, robustness and appendix), `05_policy_2026.py` (RQ3), `06_figures.py`, `07_papers.py` (working paper and article), `08_codebook.py`, `09_pitch.py` (the pitch proposal) and the tests. To download the PSA tables again first, run `./run_all.sh --download`.

# 7. How to change a document

Never edit a built document (`paper/*.md`, `.docx`, `.pdf`, or anything in `output/`, `data/clean/` or `codebook/`): the next rebuild overwrites it. Edit the source instead and rebuild (Table 3). The pipeline scripts are run from their own folder, for example `cd code/python && ../../.venv/bin/python 07_papers.py`; the tutorial and handoff scripts from the top folder, for example `.venv/bin/python tutorial/build_booklet.py`.

Table: Table 3. What to edit for each document.

| To change | Edit | Then run |
|--------------------|------------------------------------|----------------------------|
| Working paper | `paper/working_paper_template.md` | `07_papers.py` |
| Article | `paper/article_template.md` | `07_papers.py` |
| Review matrix | `paper/review_matrix.csv` | `07_papers.py` |
| Pitch proposal | `paper/pitch_template.md` | `09_pitch.py` |
| Booklet | `tutorial/booklet_src/*.md` | `tutorial/build_booklet.py` |
| References | `paper/references.bib`; booklet extras in `tutorial/booklet_src/extra.bib` | The document's build script |
| Any estimate | The code in `code/python/`, plus a decisions-log entry | `./run_all.sh` |

Numbers in the templates appear as `{{ n.name }}` and are filled in from `output/tables/paper_numbers.json`, so text and results cannot drift apart. The house style (Times New Roman, black and white, three-line tables, 1-inch margins) is applied automatically; `tools/lian_style/scripts/check_style.py file.docx` checks it.

# 8. Data sources

All data are public and free. The PSA series come from PSA OpenSTAT: the all-income CPI on the old and new geographic codes (S1, S2), the bottom-30% CPI on both codes (S3, S4) and official poverty statistics (S5). The supporting series are the World Bank's commodity prices, including Dubai crude oil (S6), and its global fuel price database (S7); the BSP peso–dollar rate (S8); the BIS policy rate series (S9); and the FAO Food Price Index (S10). The 2026 policy facts (S11) come from the law, executive orders and news reports, listed with their status in `paper/policy_context_2026.md`, and the reference study's published coefficients (S12) from Kpodar and Liu (2021). Every file, URL, download date and note is in `data/raw/source_log.md`; the codebook's Sources sheet uses the same IDs.

# 9. Open items and next steps

**Decisions for the adviser.** (1) Whether the distribution outcome should be in changes or levels; the reference paper is ambiguous. (2) The lead convention: the study follows the reference paper (fuel leads 1 to *h* − 1, decision D4); Teulings and Zubanov's own correction (leads 1 to *h*) removes the small zig-zag at months 1–2 and leaves the six- and twelve-month results unchanged. It could be reported as a footnote or robustness check (booklet Chapter 22 has the comparison).

**Work still to do.** (1) The Stata 17 version of the pipeline in `code/stata/` has not been written yet; the plan is for the author to run it and compare with Python's results (`run_all.sh` and the README already refer to `code/stata/00_master.do`). (2) Revise the FA2 proposal in the archive to the three-question structure, using the new pitch proposal as the base. (3) Slides, when needed. (4) The BARMM boundary before 2019 (ARMM versus BARMM, Cotabato City) is covered by the leave-one-region-out check but could be noted in the data appendix.

**Check before submitting.** (1) Several 2026 policy facts come from news or tax-firm reports rather than the official issuances, including the Finance Secretary's "not progressive" remark and the PHP 37 LPG saving per tank; `paper/policy_context_2026.md` marks each as verified or secondary. (2) Four references used only in the booklet (Sims 1980; Li, Plagborg-Møller and Wolf 2024; Jordà 2023; Nickell 1981) were entered from memory and should be checked. (3) The author adds the AI-use disclosure to each submission separately; the generated documents deliberately leave it out.

# 10. Version 1 archive

Version 1 of the study is kept unchanged in `archive/v1_full/` and still runs on its own. It contains the 51-page working paper, the journal manuscript, the EU replication gate (dropped from version 2), the full set of robustness checks, the submitted FA2 capstone proposal and the SA3 paper and presentation. Version 2 keeps every estimate of version 1 unchanged (verified to 10⁻¹⁰) and moves the non-core analyses to appendices (decision D12).
