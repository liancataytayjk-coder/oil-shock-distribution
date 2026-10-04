# Who Pays for Oil Shocks? — project brief

Fuel price pass-through to the inflation of poor households across Philippine
regions. Target journal: *Asian Economic Journal*. Replicates the local
projection design of Kpodar and Liu (2021), IMF WP/21/271
(*Energy Economics* 108, 2022), on Philippine national and regional data.

## Conventions

- `data/raw/` holds untouched downloads only; every file gets an entry in
  `data/raw/source_log.md` (URL, date pulled, base year, coverage).
- `data/processed/` and `output/` are written by scripts, never by hand.
- `replication/kpodar_liu_2021_targets.csv` holds the reference paper's
  coefficients; our replication is checked against it.
- No Philippine estimate is reported until the replication gate passes.
- Every specification choice goes in the decisions log below, with the evidence.

## Reference specification (read from WP/21/271)

- Equation (1): Δln CPI_{i,t+h} on 12 lags of Δln CPI and Δln RFP,
  Δln RFP_{i,t}, the Teulings–Zubanov terms Δln RFP_{i,t+h-l} for l = 1..h,
  a time trend, and country fixed effects. Estimated by OLS per horizon.
- RFP = average retail gasoline price (premium and regular), local currency.
- Sample: 122 countries (48 advanced, 74 developing; the Philippines is in the
  developing group), Jan 2000–Jun 2019, unbalanced.
- Tables report h = 0..6 for CPI; distribution figures run h = 0..12.
- Bands are 90%.
- Distribution metric: ratio of richest-quintile CPI to poorest-quintile CPI;
  positive response = progressive.
- Crude-versus-retail comparison is run on EU countries only, with before- and
  after-tax gasoline prices (before-tax regression controls for gasoline taxes).

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

## Estimation plan (pre-specified 2026-10-04)

Common: p = 12, h = 0..12, linear trend, 90% bands. Shock dates t from Jan 2001
(bottom-30% CPI starts Jan 2000, plus 12 lags) to the end of data (Aug 2026).
National models use Newey–West (h + 1 lags); the regional panel uses region
fixed effects and Driscoll–Kraay errors. Units: 100·Δln, so β is pp per 1 pp.
Every model is reported per horizon and cumulatively (running-sum outcome).

- **RQ1:** national Δln CPI_all on Δln fuel (07.2.2). Also Δln CPI_b30.
- **RQ2:** national ΔD = Δln(CPI_all/CPI_b30) on Δln fuel. Positive = progressive
  (H2a), negative = regressive (H2b). Judged on the cumulative response at
  h = 6 and h = 12.
- **RQ3:** national all-income Δln of each of the 13 COICOP divisions on Δln
  fuel. Gap decomposition: cumulative response at h = 12 of division k ×
  (w_all,k − w_b30,k)/100, national 2018 weights.
- **RQ4:** 17-region panel of ΔD on the regional Δln fuel. Baseline pooled β,
  then one interaction at a time with time-invariant group dummies:
  high poverty (2018 poverty incidence among population above the 17-region
  median); high food share (food weight in the region's 2018 all-income basket
  above median); Mindanao (IX, X, XI, XII, XIII, BARMM); island regions
  (MIMAROPA, VI, VII, VIII).
- **Robustness:** (a) shock = Dubai crude in pesos; (b) controls Δln PHP/USD,
  Δ policy rate, Δln FAO food index; (c) p = 6, 18; (d) excluding 2020 and
  excluding 2026; (e) dummies for Jan 2012, Jan 2018; (f) asymmetry
  (shock × 1[Δfuel > 0]); (g) paper's window, to Jun 2019; (h) shock =
  gasoline 07.2.2.2 (2019–); (i) shock = World Bank Manila pump price
  (2018–Mar 2025; the PH series starts Jan 2017); regional: (j) leave one region out, (k) drop flagged
  2026 observations (D6), (l) national instead of regional shock.

## Results (first full run, 2026-10-04; `output/tables/estimates.csv`, `output/figures/`)

Cumulative responses to a 1 pp fuel price rise, 90% bands, Jan 2001–Aug 2026.

- **RQ1:** CPI_all +0.044 on impact (SE 0.006), 0.087 at h = 6, 0.102 at h = 12;
  bottom-30% CPI similar (0.095, 0.102). Larger than the paper's
  developing-economy peak (0.018) and still rising at 12 months. Robust to all
  checks; Dubai crude in pesos gives about half (0.030, 0.041), consistent with
  the paper's crude-understates finding.
- **RQ2:** national gap negative (regressive, H2b): −0.0155 (SE 0.010) at h = 6,
  −0.0097 (0.011) at h = 12; significant at 10% only at h = 3, 4, 7, 8.
  Regional panel: −0.021 (0.008) at h = 6, −0.017 (0.009) at h = 12, both
  significant; leave-one-region-out range −0.020 to −0.023 at h = 6.
- **Fragility:** sign holds in nearly all checks, but macro controls, gasoline
  index (2019–) and World Bank pump price (2018–25) give ≈ 0. Exploratory split
  (D9): regional −0.054 (0.020) in 2001–2012 vs −0.009 (0.006) in 2013–2026.
- **RQ3:** largest pass-through in transport (0.37), housing/utilities (0.16),
  food (0.07), restaurants (0.06); 10 of 13 divisions significantly positive at 10% (paper: 10 of 12 in developing economies). Weight-only
  decomposition predicts a progressive gap (+0.010), opposite to the direct
  estimate. RQ3b (exploratory, 2013–): bottom-30% housing/utilities responds more
  (0.18 vs 0.14) and transport less (0.20 vs 0.30) than all-income.
- **RQ4 (h = 12, extra effect vs other regions):** Mindanao −0.017 (0.009),
  island −0.012 (0.009), high poverty −0.010 (0.008), high food share +0.010
  (0.005). None survives a Bonferroni correction for four tests.

## Replication gate (pre-registered 2026-10-04, before any estimate was run)

The Philippine analysis starts only if all three pass. Data: EU countries.

- **G1, retail after tax (Figure 7, blue):** HICP all-items on Weekly Oil Bulletin
  Euro-super 95 after-tax price, EU, 2005–Jun 2019. Pass if β₀ ∈ [0.035, 0.075]
  (target 0.055) and β₂…β₆ are each within ±0.01 of zero.
- **G2, ordering (Figure 7):** β₀(after tax) > β₀(before tax, with tax control)
  and β₀(after tax) > β₀(Brent in euro). Targets 0.055 > 0.020 ≈ 0.015.
- **G3, advanced-economy shape (Annex Table 1):** HICP all-items on HICP CP0722
  (fuels and lubricants), EU, 2000–Jun 2019. Pass if β₀ > 0 is significant at
  10% and β₁ < β₀, with β₂…β₆ each within ±0.01 of zero. (Level not required: the
  fuel index differs from the gasoline price.)
- Indicative only (not part of the gate): Philippines alone, 2000–Jun 2019,
  against the developing-economy profile in Annex Table 2.

**Result (2026-10-04): PASS.** `output/tables/replication_eu_ph.csv`. β₀ = 0.057
after tax, 0.024 before tax, 0.014 Brent (paper: 0.055, 0.020, 0.015); all
responses ≈ 0 from h = 2. G3: β₀ = 0.065, β₁ = 0.026, then ≈ 0.

## Pipeline

`./run_all.sh` rebuilds everything from `data/raw/` (add `--download` to refresh
PSA). Python 3.11, packages in `requirements.txt`, estimator in `ospd/lp.py`,
tests in `tests/`.

## Open questions

- [ ] Distribution outcome: monthly change in ln(CPI_all/CPI_b30) (our
      default, consistent with D1) or its level? The paper says only that it
      "replaces the change in CPI with the ratio". Ask the adviser or authors.
- [ ] Standard errors: the text says clustered by country; the table notes say
      "robust". In the EU replication the two give similar errors (0.004 vs 0.002
      at h = 0); report clustered (Driscoll–Kraay for PH regions).
- [x] Kpodar–Abdallah fuel database: not public. Replaced by D5 (PH) and the
      Weekly Oil Bulletin (EU gate).
- [x] Bottom-30% CPI coverage: all items Jan 2000–Aug 2026, by commodity from
      Jan 2012, all 17 regions, on one 2018=100 basis (PSA backcasts).
- [x] Regional fuel sub-index: 07.2.2 for all regions 1994–2026; 07.2.2.2
      gasoline from 2018.
- [ ] BARMM: PSA publishes one unbroken series from 1994 (all-income) and 2000
      (bottom 30%), labelled BARMM in the backcasts. Not yet confirmed whether
      pre-2019 values use ARMM or BARMM boundaries (Cotabato City); check the
      PSA backcasting technical note. Leave-one-region-out covers it meanwhile.
