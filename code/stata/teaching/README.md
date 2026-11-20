# Teaching sequence: the panel study in Stata, step by step

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
do code/stata/teaching/06_robustness.do
do code/stata/teaching/07_2026.do
do code/stata/teaching/08_check.do
```

| Step | What you do | Key result (Python) |
|---|---|---|
| 0 | Paths; installs `xtscc` | — |
| 1 | Read the 17-region panel, merge the national series, `xtset`, build lags and leads within regions | 17 regions, 2001–2026 |
| 2 | One local projection by hand (*h* = 6): `xtreg, fe`, then `xtscc, fe` | 0.0856 (0.0132) |
| 3 | RQ1: all horizons, both groups; the loop, then the program `panel_lp` | 0.047, 0.086, 0.102 (all); 0.046, 0.105, 0.116 (bottom 30%) |
| 4 | RQ2: the gap | −0.0214 (0.0084) at 6 months, significant from 3 to 12 |
| 5 | Why: the budget-share calculation | +0.0101 (progressive) |
| 6 | Five robustness checks | survives (i), (ii), (iv); concentrated in 2001–2012; not with food controls |
| 7 | RQ3: the 2026 shock out of sample; peso cost; block bootstrap | gap −0.77 [−1.45, −0.25] vs actual −1.18; PHP 499 and 109 |
| 8 | Check everything against Python | differences below 1e-6 |

Outputs go to `output/stata_teaching/`. Step 6 and the bootstrap in step 7 take a few minutes; set
`local REPS 0` in step 7 to skip the bootstrap.

**Status:** written for Stata 17 but not yet run in Stata. If a step stops with an error, the message
and the line are usually enough to fix it; send them back if not.

**How it differs from `code/stata/00_master.do`:** that pipeline replicates every estimate of the
study at once with a general program (`lp_irf`); this sequence covers only the manuscript, writes each
loop out the first time it appears, and is meant to be read.
