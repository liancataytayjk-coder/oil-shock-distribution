# Teaching sequence: the panel study in Stata, step by step

A step-by-step tutorial for these files, from setup to the figures, is `study_kit/stata_tutorial.pdf`.

These do-files rebuild every result of the manuscript (`paper/manuscript.pdf`) in Stata 17, one step
at a time, so that you can run and read each part of the analysis yourself. Each file explains what it
does, prints the value Python obtained next to yours, and saves its results; step 8 checks them all.

Run them in order, in one Stata session, from the repository's top folder:

```stata
cd "C:/path/to/oil-shock-distribution"
do code/stata/teaching/00_setup.do
do code/stata/teaching/01_data.do
do code/stata/teaching/02_one_horizon.do
do code/stata/teaching/03_pass_through.do
do code/stata/teaching/04_gap.do
do code/stata/teaching/05_why.do
do code/stata/teaching/06_geography.do
do code/stata/teaching/07_robustness.do
do code/stata/teaching/08_check.do
do code/stata/teaching/09_figures.do
* optional, not in the manuscript:
do code/stata/teaching/extra_2026.do
```

| Step | What you do | Key result (Python) |
|---|---|---|
| 0 | Paths; installs `xtscc` | — |
| 1 | Read the 17-region panel, merge the national series, `xtset`, build lags and leads within regions | 17 regions, 2001–2026 |
| 2 | One local projection by hand (*h* = 6): `xtreg, fe`, then `xtscc, fe` | 0.0856 (0.0132) |
| 3 | Pass-through: all horizons, all households and low-income households; the loop, then the program `panel_lp` | 0.047, 0.086, 0.102 (all); 0.046, 0.105, 0.116 (low-income) |
| 4 | Who pays more: the gap | −0.0214 (0.0084) at 6 months, significant from 3 to 12 |
| 5 | By how much and why: the budget-share calculation | +0.0101 (progressive) |
| 6 | Geography: a response for every region; Wald test of equality; correlation with poverty and food share | gap from −0.053 to +0.009; equality rejected (p = 0.03); correlations weak |
| 7 | Robustness: world crude price as the shock; one region left out (plus the two estimates in the limitations) | crude: gap −0.0116 (0.0050); left-out range −0.0227 to −0.0203 |
| 8 | Check everything against Python | differences below 1e-6 |
| 9 | Draw the manuscript's figures: trends, pass-through, gap, regions | four PNG files |
| extra | The 2026 shock out of sample, peso cost, block bootstrap (not in the manuscript) | gap −0.77 [−1.45, −0.25] vs actual −1.18 |

Outputs go to `output/stata_teaching/`. Steps 6 and 7 take a few minutes each; the optional 2026 extra includes a
bootstrap (set `local REPS 0` there to skip it).

**Status:** written for Stata 17 but not yet run in Stata. If a step stops with an error, the message
and the line are usually enough to fix it; send them back if not.

**How it differs from `code/stata/00_master.do`:** that pipeline replicates every estimate of the
study at once with a general program (`lp_irf`); this sequence covers only the manuscript, writes each
loop out the first time it appears, and is meant to be read.
