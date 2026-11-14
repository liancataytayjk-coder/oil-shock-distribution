# Stata 17 replication

This folder re-estimates every result of the study in Stata 17, for practice, replication and a check
that the Python results do not depend on the software. The Python pipeline (`run_all.sh`) remains the
main analysis; Stata starts from the cleaned files it writes (`data/clean/*.csv`) and checks the
derived variables against the index levels before estimating anything.

**Status:** written for Stata 17 but not yet run (Stata was not available where the code was written).
Run it, read the log, and send any error messages back so the code can be fixed.

## How to run

```stata
cd "C:/path/to/oil-shock-distribution"     // the repository's top folder
do code/stata/00_master.do
```

It installs `xtscc` (Driscoll–Kraay standard errors) from SSC if needed, writes everything to
`output/stata/` and keeps a log in `output/stata/stata_log.smcl`. The panel regressions make
`04_estimate.do` the slow step (roughly 15–30 minutes).

## Files

| File | What it does | Python counterpart |
|---|---|---|
| `00_master.do` | Sets paths, installs `xtscc`, runs everything, keeps the log | `run_all.sh` |
| `01_import.do` | Imports `national_monthly.csv`, `regional_panel.csv`, `region_info.csv`; checks every derived variable | `02_build_clean.py` (output only) |
| `02_lp_program.do` | Defines `lp_irf`, the local projection estimator | `lp.py` |
| `03_descriptive.do` | Summary statistics, annual inflation, ADF tests | `03_descriptive.py` |
| `04_estimate.do` | RQ1, RQ2 (national and panel), the 13 divisions, both baskets from 2013, every robustness check, region groups, leave one region out | `04_estimate.py` |
| `05_policy_2026.do` | Responses estimated to December 2025, the fuel-driven 2026 rise, peso cost by region | `05_policy_2026.py` |
| `06_var.do` | VAR with fuel ordered first; one-time fuel change | `var_irf()` in `04_estimate.py` |
| `07_compare.do` | Compares every Stata estimate with Python's | — |
| `expected_results.csv` | Python's cumulative estimates (written by `04_estimate.py`) | — |

## The estimator in one line

For each horizon *h* = 0, …, 12, `lp_irf` regresses the sum of the outcome from *t* to *t + h* on the
shock, 12 lags of the outcome and the shock, the leads of the shock (1 to *h* − 1 by default), a
trend and a constant, with `newey, lag(h+1) force` nationally and `xtscc, fe lag(h+1)` for the panel.
The `if` condition selects the shock dates only; lags, leads and future outcomes still come from
outside it, exactly as in Python. Example:

```stata
use output/stata/national.dta, clear
tsset mdate
lp_results_init
lp_irf d_cpi_all if mdate >= tm(2001m1), shock(d_fuel) rq(RQ1) spec(baseline)
lp_show, spec(baseline) outcome(d_cpi_all)
```

Options: `horizons(12)`, `lags(12)`, `leads(paper|full|none)`, `noncumulative`, `panel`,
`controls(varlist)` (current value and *p* lags), `exog(varlist)` (current value only),
`interact(varlist)` (adds shock × variable and reports its coefficient).

## What "consistent" means

`07_compare.do` reports, for every matched estimate, the absolute difference in the point estimate
(expected: below 1e-6), the ratio of standard errors (expected: close to 1; small differences come
from different small-sample corrections in `newey`/`xtscc` and `statsmodels`/`linearmodels`), and
whether the number of observations is the same. It also compares the 2026 fuel-driven rise and peso
cost, the VAR responses and the summary statistics. The ADF tests use the lag length that Python
chose by AIC, so their statistics should be close but need not be identical.
