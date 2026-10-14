# <Short title> — project brief

<One paragraph: question, country/units, target journal or course output, reference paper.>

## Conventions

- `data/raw/` holds untouched downloads only; every file gets an entry in
  `data/raw/source_log.md` (URL, date pulled, base year, coverage).
- `data/processed/` and `output/` are written by scripts, never by hand.
- `replication/<paper>_targets.csv` holds the reference paper's coefficients.
- No new-data estimate is reported until the replication gate passes.
- Every specification choice goes in the decisions log below, with the evidence,
  labelled pre-registered / supplementary / exploratory.
- Documents are rendered from templates; never edit rendered .md/.docx by hand.
- User style: as simple as possible, define every term on first use (words →
  formula → example), paragraphs over bullets/tables.

## Reference specification (read from <paper>)

- Equation: <outcome> on <lags>, <shock>, <correction terms>, <trend/FE>. Estimator: <OLS per horizon>.
- Shock variable and units:
- Sample:
- Horizons reported; band width; standard errors:
- Distribution metric (if any):

## Decisions log

| # | Date | Decision | Evidence / reason |
| --- | --- | --- | --- |
| D1 | | | |

## Replication gate (pre-registered <date>, before any estimate)

- **G1:** <estimate> ∈ [<lo>, <hi>] (target <x>); <shape criterion>.
- **G2:** <ordering criterion>.
- **G3:** <second dataset / shape>.

**Result:** <PASS/FAIL, numbers, file>.

## Estimation plan (pre-specified <date>)

Common: <p, h, trend, bands, sample, SEs, units>.

- **RQ1:** ...
- **RQ2:** ... judged on <horizons>.
- **Heterogeneity:** <groups, rules, multiple-testing correction>.
- **Robustness:** (a) ... (b) ...

## Results (<date>; `output/tables/estimates.csv`)

- **RQ1:** ...

## Documents

- <template> → <script> → <output>

## Pipeline

`./run_all.sh` rebuilds everything from `data/raw/` (`--download` to refresh).

## Open questions

- [ ] ...
