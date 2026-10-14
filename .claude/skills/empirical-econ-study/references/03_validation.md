# Phase 3 — Validation: prove the estimator works before trusting it

Two independent checks are needed. Both are cheap compared with publishing a wrong
number.

## 3.1 Simulation test

Copy `scripts/test_lp.py` into `tests/`. It simulates data with a known impulse
response and checks that the estimator recovers it, for:

- a single series with Newey–West standard errors;
- a panel with clustered and with Driscoll–Kraay standard errors;
- cumulative responses equal to the running sum;
- an interaction recovering a known group difference.

If you change the estimator, add a test for the change. Run `pytest` inside
`run_all.sh`.

## 3.2 Replication gate (pre-registered)

1. **Write the gate before running anything.** Put it in `CLAUDE.md` under
   "Replication gate", with the date. Each criterion needs a target and a
   pass range. For example:
   - G1: β₀ ∈ [0.035, 0.075], target 0.055, and β₂…β₆ each within ±0.01 of 0.
   - G2: an ordering, β₀(after tax) > β₀(before tax) and > β₀(crude).
   - G3: a shape on a second dataset.
2. **Use data you can actually get.** If the reference dataset is private,
   replicate a sub-result whose data are public. In the worked example, the
   reference paper's EU retail-versus-crude comparison was replicated with
   Eurostat HICP and the Weekly Oil Bulletin.
3. **Run `04_replicate.py`** and save `output/tables/replication_gate.csv` with
   columns target, estimate, pass/fail.
4. **Record the result** (PASS or FAIL, with the numbers) in `CLAUDE.md`.
5. **If the gate fails, stop.** Re-read the specification (Phase 1.2), fix the
   code, and say what changed. Do not loosen the pass range after seeing the
   result. If a range must change, log why, and label every later result as
   conditional on that change.

An *indicative* check is not part of the gate: run the new country on the
reference paper's sample window and compare it with the reference paper's
country-group profile.
