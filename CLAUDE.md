# Who Pays for Oil Shocks? — project brief (version 2)

Fuel price pass-through to the inflation of poor households across Philippine
regions. Author: Lian Cataytay (sole author), Graduate School of Applied
Economics, University of Southeastern Philippines. Target journal: *Asian
Economic Journal*. Replicates the local projection design of Kpodar and Liu
(2022, *Energy Economics* 108; IMF WP/21/271) on Philippine data.

Version 2 (from 2026-10-22) is the lean, core version at the top level of the
repository. The complete first version (51-page working paper, journal draft,
EU replication gate, all robustness checks, FA2 proposal, SA3 deck, master
document) is archived unchanged in `archive/v1_full/` and still runs on its own.

## Structure of the study (three objectives, three research questions)

- **Objective 1 (descriptive):** summary statistics, annual inflation, trends,
  fuel-shock episodes, regional summary, ADF tests.
- **Objective 2 (estimation):** RQ1 national pass-through, both groups; RQ2 the
  gap ΔD = π^A − π^B, national and 17-region pooled panel, plus the "why"
  (weights effect vs within-category effect: 13 divisions × weight differences;
  divisions in both baskets from 2013, exploratory).
- **Objective 3 (policy):** RQ3 the 2026 shock: out-of-sample test (model to
  Dec 2025), peso cost by region, household fuels/fares/cereals, item
  decomposition, policy-instrument assessment.
- **Core robustness (main text):** Dubai crude in pesos; macro controls; excluding
  2020; panel 2001–2012 vs 2013–2026; leave one region out.
- **Appendix:** 13 divisions, region-group interactions (not significant after
  Bonferroni), all other robustness checks, cross-correlations, regional figure.
- **Removed in v2:** the EU validation / replication gate (kept in the archive;
  the papers mention only the simulation test).

## Conventions

- `data/raw/` holds untouched downloads (PSA tables as plain CSV, decompressed
  but unchanged; Excel files as published) logged in `data/raw/source_log.md`;
  `data/raw/extracts/` holds CSV copies of the Excel columns used.
- `data/clean/`, `output/`, `paper/*.md|docx|pdf` and `codebook/codebook.xlsx`
  are written by scripts only. Edit templates (`paper/*_template.md`,
  `paper/review_matrix.csv`) and code, never outputs.
- Every specification choice goes in the decisions log, with its timing
  (pre-registered / supplementary / exploratory).
- House style for every document: `tools/lian_style/` (Times New Roman, black and
  white, three-line tables, 1-inch margins; `docx_style.py finish`, `render.py`).
- Writing: as simple as possible; define every term on first use (words →
  formula → example); paragraphs over bullets and tables; no AI-use disclosure in
  generated documents (the author adds it separately); date November 2026.
- Pronouns: refer to the author by name or as "the author", never he/she.

## Pipeline

`./run_all.sh` (Python 3.11, `.venv`, `requirements.txt`) runs
`code/python/01_extract_excel.py` → `02_build_clean.py` → `03_descriptive.py` →
`04_estimate.py` → `05_policy_2026.py` → `06_figures.py` → `07_papers.py` →
`08_codebook.py` → `09_pitch.py` (short national proposal, `paper/proposal_pitch.*`) → `10_panel_study.py`
→ `11_manuscript.py` (the AEJ manuscript, `paper/manuscript*.*`) → tutorial,
booklet (`tutorial/`) and study kit (`study_kit/`) → pytest; `handoff/build_handoff.py` builds the guide and zips. `00_download.py` refetches PSA tables. The Stata 17
version is `code/stata/` (to be run by the author; `00_master.do`). Estimator:
`code/python/lp.py`; settings: `code/python/config.py`; sources and results map:
`code/python/catalog.py` (S1–S12).

Outputs: `paper/working_paper.*` (chapter form, Ch. 1–5 + Appendices A review
matrix, B supplementary, C data appendix); `paper/article.*` (IMRAD, Asian Economic Journal,
reading version) with `article_online_appendix.*`, `article_submission.*` (blinded, tables and
figures at the end, author–date style `paper/asian-economic-journal.csl`) and `article_title_page.*`; `output/tables/estimates.csv` (column `core`); `output/figures/fig01–08`
(main) and `figA1–A4` (appendix); `codebook/codebook.xlsx`.

## Decisions log

| # | Date | Decision | Evidence / reason |
| --- | --- | --- | --- |
| D1 | 2026-10-04 | Outcome at horizon h is the one-month change Δln CPI_{t+h}, not the cumulative change ln CPI_{t+h} − ln CPI_{t-1}. Report cumulative IRF as the running sum. | Annex Tables 1–2: the coefficient on CPI lag (12 − h) stays ≈ 0.47 (advanced) along the diagonal, i.e. the same calendar month a year earlier, which only happens if the outcome is a single month. TZ lead coefficients ≈ β_0. |
| D2 | 2026-10-04 | Use non-seasonally-adjusted CPI, as published; the 12 lags absorb seasonality. | Large lag-12 coefficient (0.48) in Annex Table 1 shows NSA data. |
| D3 | 2026-10-04 | Include a linear time trend and a constant alongside fixed effects. | Both appear in Annex Tables 1–2. |
| D4 | 2026-10-04 | Teulings–Zubanov terms are the shock leads 1..h−1 (none at h = 0, 1). | Annex Tables 1–2: "Lead 1" first appears in the h = 2 column; h = 6 has Leads 1–5. |
| D5 | 2026-10-04 | Shock = PSA CPI sub-index 07.2.2 "Fuels and lubricants for personal transport" (all-income, 2018=100), national and by region, Jan 1994–Aug 2026. Robustness: 07.2.2.2 gasoline (2018–), World Bank Manila RON91 pump price (Dec 2015–Apr 2025), Dubai crude in pesos. | The Kpodar–Abdallah fuel database is not public; the World Bank database stops Apr 2025 and has no regions. Monthly changes in 07.2.2 correlate 0.87 with the World Bank pump price and 0.99 with 07.2.2.2 over 2016–2025. |
| D6 | 2026-10-04 | Regions use the old geographic code (17 regions; Negros in VI/VII). Jan–Aug 2026 chains new-code monthly growth onto old-code levels; flagged `new_geo_ext` for VI, VII, XII, BARMM, whose boundaries changed. | Bottom-30% backcasts (2000–2017) exist only on the old code; old and new codes are identical for all other regions and nationally over 2018–2025. |
| D7 | 2026-10-04 | Bottom-30% all-items CPI spliced at Jan 2012 and Jan 2018 on PSA's own 2018=100 backcasts; robustness adds dummies for those two months. | Mean abs. monthly change in the CPI ratio is 0.71 pp (Jan 2012) and 0.50 pp (Jan 2018) vs 0.25 pp overall. Largest ratio moves are the 2008 rice crisis (genuine). |
| D8 | 2026-10-04 | Estimation plan for RQ1–RQ4, fixed before any Philippine estimate was run (see "Estimation plan" below). | Pre-specification. |
| D9 | 2026-10-04 | Exploratory, added after the first run: RQ3b compares bottom-30% and all-income responses of food, housing, transport and restaurants (2013–2026, the span of bottom-30% component indices). Also fixed a bug: "food share" is w(01)/w(all items) within each region, not the region's food weight in the national basket. | The weights decomposition (same component prices for both baskets) gave a progressive gap (+0.010) while the direct estimate is regressive (−0.010), suggesting the baskets face different price changes within divisions. Labelled exploratory in all output. |
| D10 | 2026-10-05 | 2026-episode and mechanism analyses, specified before estimation (after the main results were seen, so labelled "supplementary" not "pre-registered"): see "2026 episode plan" below. | Asked whether the study captures the 2026 shock; the main LPs use 2026 only at short horizons. |
| D11 | 2026-10-06 | Descriptive statistics and trend analysis (working paper Objective 1): summary statistics by sub-period, annual inflation, fuel-shock episodes (runs of ≥ 3 months with fuel ≥ +15% y/y), cross-correlations, regional summaries, ADF unit-root tests. Figures switched to black and white without in-image titles. | Requested for the working paper's three-objective structure; descriptive only, no inference beyond ADF. Journals print in greyscale and caption figures in the text. |

| D12 | 2026-10-22 | Version 2: keep only the core analyses in the main text (three RQs: pass-through; who pays more, national + pooled panel + why; 2026 and policy), five core robustness checks, everything else in appendices; drop the EU validation; region-group interactions moved to the appendix. All estimates unchanged from version 1 (verified to 1e-10). | Author's request for a one-semester scope; checks that weaken the result (macro controls, period split) kept in the main text to avoid cherry-picking. |

| D13 | 2026-11-14 | Supplementary robustness: Teulings–Zubanov's own lead set (leads 1..h, `lp.py tz="full"`), national (CPI all, gap) and panel (gap). Main specification keeps D4. | Found while writing the tutorial: with leads 1..h−1 the h = 1 estimate is biased when shocks are serially correlated. Changes almost nothing from h = 3: CPI all 0.087→0.088 (h = 6); gap −0.0155→−0.0160; panel −0.0214→−0.0216. |
| D14 | 2026-11-14 | Supplementary check: VAR(12) in (fuel, outcome) with constant and trend, fuel ordered first (Cholesky), shock scaled to 1% fuel on impact; 90% Monte Carlo bands; also the VAR response to a one-time fuel change (later fuel held at zero) and the LP without leads. | Plagborg-Møller and Wolf (2021): LP and VAR estimate the same impulse response; the VAR matches the LP without leads (CPI all 0.113 vs 0.115 at h = 6). The gap stays negative (−0.0219 at h = 6). |
| D15 | 2026-11-14 | Article version 3 for the *Asian Economic Journal*: IMRAD; descriptives → RQ1 → RQ2 (national and panel side by side; budget-share decomposition and 2026 contribution accounting labelled descriptive) → 2026 application and policy; review limited to 15 studies (column `article` in `paper/review_matrix.csv`); separate online appendix with every robustness check; blinded submission file and title page; author–date references. | Author's scope for the defense and submission. Item-level bottom-30% indices start in 2013, so the 2008 episode cannot be decomposed by item. |

| D16 | 2026-11-20 | Manuscript for the AEJ is the panel study (`paper/manuscript.*`, `10_panel_study.py`, `11_manuscript.py`): one method (panel LP, region FE, Driscoll–Kraay), the 17-region panel, RQ1 (both groups), RQ2 (gap + budget-share calculation, descriptive), five robustness checks (leave one region out, excl. 2008, period split, Dubai crude in pesos, exchange-rate/policy-rate/world-food controls; food-only added), RQ3 (responses to Dec 2025 applied to the 2026 national fuel path; moving-block bootstrap, 12-month blocks, 999 replications; peso cost). New panel estimates are supplementary (after the main results). Stata teaching sequence `code/stata/teaching/`. | Author's lean scope for the defense. Panel CPI responses: all 0.047/0.086/0.102, b30 0.046/0.105/0.116. Crude in pesos: gap −0.0116 (0.0050) at h = 6. With world food prices controlled the gap is −0.0036 (0.0133): reported openly as food channel vs common commodity cycle. 2026 gap predicted −0.77 [−1.45, −0.25] vs actual −1.18; PHP 499/month, PHP 109 above average inflation. |

| D17 | 2026-11-25 | Manuscript narrowed further: (1) pass-through, all vs low-income households; (2) who pays more and by how much (gap; budget-share calculation, descriptive); (3) geography: region-specific responses (shock × region indicators, common lags, FE, Driscoll–Kraay), Wald test of equality (χ²(16)), correlation with poverty and food share; (4) robustness: world crude price in pesos (all, low-income, gap) and leave one region out. Period split and the world-food-price control reported in the limitations, not dropped. 2026 application removed from the manuscript (kept in the pipeline and as `extra_2026.do`). Terms: "low-income households" (bottom 30% by income per person, PSA) and "all households"; "headline index" and "low-income index". Method section rebuilt step by step from the ARDL model; a "where" list after every equation. | Author's request. Geography: pass-through h = 6 ranges 0.058–0.110, equality rejected (χ² = 55.3, p < 0.001); gap −0.053 to +0.009, rejected (p = 0.034; h = 12 p = 0.038); correlation with poverty 0.23, food share 0.30 at h = 6, ≈ 0 at h = 12 (exploratory, after the main results). |

## Key results (unchanged from version 1)

RQ1: CPI_all +0.044 on impact, 0.087 at h = 6, 0.102 at h = 12; b30 0.044, 0.095, 0.102; crude ≈ 40% of retail.
RQ2: national −0.0155 (0.0103) at h = 6, −0.0097 at h = 12 (significant at h = 3, 4, 7, 8);
panel −0.0214 (0.0084), −0.0173 (0.0085); weights-only gap +0.0101 (progressive);
2013– b30 vs all: housing 0.182 vs 0.142, transport 0.196 vs 0.300.
Robustness: crude −0.0093; macro −0.0046; panel 2001–12 −0.0541 vs 2013–26 −0.0091; LOO −0.0227 to −0.0203.
RQ3: fuel-driven 2.55 of 4.81 (all), 3.13 of 5.98 (b30); PHP 467/month (390–633), total PHP 907; cereals +1.67 of +1.24 gap.

## Open questions

- [ ] Distribution outcome in changes vs levels (reference paper ambiguous); ask the adviser.
- [ ] BARMM pre-2019 boundary (ARMM vs BARMM, Cotabato City); leave-one-region-out covers it.
- [ ] Stata code: written (`code/stata/`, D13–D14 included); to be run by the author in Stata 17; `07_compare.do` compares with `code/stata/expected_results.csv`.
- [ ] AEJ submission rules taken from 2023–2024 issue notices (Wiley page not reachable): ~100-word abstract, author–date references, blinded main file, separate title page, 8,000 words + 20%; confirm on the live page before submitting.
- [x] Lead convention: reported as a robustness row (D13); the main specification keeps D4.
- [ ] FA2 proposal to be revised to the three-RQ structure after the papers are final.
