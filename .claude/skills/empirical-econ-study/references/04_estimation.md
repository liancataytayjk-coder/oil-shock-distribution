# Phase 4 — Estimation: pre-specified plan, main models, heterogeneity, robustness

## 4.1 Write the plan first

Before the first estimate on the new data, add an "Estimation plan" section to
`CLAUDE.md` and log it as a decision (D8 in the worked example). It should say:

- **common settings**, which in the worked example were:
  - lags p = 12;
  - horizons h = 0..12;
  - a linear trend;
  - 90% bands;
  - the sample window;
  - units 100·Δln;
  - Newey–West standard errors (national) and Driscoll–Kraay (panel);
- **for each RQ**, the outcome, the shock, the sample, and which horizons decide it
  (for example, judged on the cumulative response at h = 6 and h = 12);
- **the heterogeneity tests**: the group dummies, one interaction at a time, and
  how multiple testing is handled (Bonferroni across the group tests);
- **the robustness menu**, lettered (a), (b), ….

Anything added after the results are seen is labelled *exploratory* or
*supplementary*, in the log and in every document.

## 4.2 The local projection

For each h = 0..H, estimated by OLS:

π_{t+h} = α_h + β_h f_t + Σ_{q=1}^{p} γ_q π_{t−q} + Σ_{q=1}^{p} λ_q f_{t−q} + Σ_{l=1}^{h−1} ρ_l f_{t+l} + δ_h t + (u_i) + ε_{t+h}

- **β_h** is the pass-through at horizon h. The cumulative response is
  B_h = Σ_{j≤h} β_j; get it directly with `cumulative=True` (a running-sum
  outcome), which gives correct standard errors.
- **The leads f_{t+1..t+h−1}** are the Teulings–Zubanov correction. Match the lead
  set to the reference paper.
- **The lags** absorb dynamics and the seasonality of data that are not seasonally
  adjusted.
- **Panels** add unit fixed effects u_i. Interactions f × G_i give θ_h, the extra
  effect in group G.
- **Distributional outcome:** ΔD_t = π^A_t − π^B_t, where D = 100·ln(P^A/P^B).
  Negative means regressive (the poor face more inflation).

Use `scripts/lp.py`:

```python
from <pkg>.lp import local_projection
res = local_projection(df, y="dlp_all", x="dl_fuel", time="t", unit=None,
                       horizons=12, p=12, cumulative=True, se="newey_west")
panel = local_projection(df_reg, y="dD", x="dl_fuel_r", time="t", unit="region",
                         interact=("mindanao",), cumulative=True, se="driscoll_kraay")
```

Save every model to one long table, `output/tables/estimates.csv`, with columns
`rq, spec, outcome, cumulative, h, term, beta, se, lo, hi, nobs, n_units, r2`.
Figures and documents then read from one place.

## 4.3 Standard robustness menu (adapt it)

- (a) An exogenous shock, such as world crude in local currency.
- (b) Macro controls: exchange rate, policy rate, world food prices.
- (c) Lag length: p = 6 and 18.
- (d) Excluding crisis years, such as 2020 and the latest episode.
- (e) Dummies for splice months.
- (f) Asymmetry: shock × 1[shock > 0].
- (g) The reference paper's sample window.
- (h, i) Alternative proxies.
- Panels only: (j) leave one unit out, (k) drop flagged observations,
  (l) national instead of unit-level shock.

Report a robustness table of the decisive horizon(s) for every check. In the text,
name the checks under which the result weakens.

## 4.4 Mechanisms and decompositions

- **Weights-only decomposition.** Gap_h ≈ Σ_k B_{k,h}·(w^A_k − w^B_k), where B_k
  is the response of category k. If its sign differs from the direct estimate,
  the gap comes from price differences *within* categories. Test that with the
  group-specific category indices (RQ3b in the worked example, labelled
  exploratory).
- **Item mechanisms.** For each candidate item, contribution = cumulative response
  at h = 12 × basket weight, by group.

## 4.5 Applying the model to a current episode

This makes the study policy-relevant even when the latest shock is short in the
data.

1. **Out of sample.** Estimate on data that end before the episode. The predicted
   change from the episode start to month m is Σ_t B_{m−t}·f_t. Compare it with
   the actual change and report the share explained.
2. **By unit.** Do the same with the panel model and each unit's own shock path,
   and rank the units.
3. **Peso cost.** Multiply the poverty line for a reference family (annual
   per-capita threshold × family size / 12, carried forward with the group CPI)
   by the predicted rise.
4. **Descriptive decomposition** of the actual episode, as a fixed-base Laspeyres
   contribution by item. This covers whatever the model leaves unexplained.

Label these "supplementary": specified before running, but after the main results
were seen.

## 4.6 Descriptive analysis (Objective 1)

Script it in `09_descriptive.py`:

- summary statistics by sub-period;
- annual inflation by group;
- episodes: runs of at least 3 months with the shock ≥ +15% year on year;
- the direction of the gap in each episode;
- cross-correlations at leads and lags;
- regional summaries;
- ADF unit-root tests on levels and changes.

## 4.7 After the run

Record the headline numbers in the "Results" section of `CLAUDE.md`: point
estimates, standard errors, significance and fragility. That section is what a
new session reads first.
