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
