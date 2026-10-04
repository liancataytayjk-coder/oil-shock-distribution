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

## Open questions

- [ ] Distribution outcome: monthly change in ln(CPI_rich/CPI_poor) (our
      default, consistent with D1) or its level? The paper says only that it
      "replaces the change in CPI with the ratio". Ask the adviser or authors.
- [ ] Standard errors: the text says clustered by country; the table notes say
      "robust". Replicate both and see which matches the brackets.
- [ ] Can we obtain the Global Monthly Retail Fuel Price Database (Kpodar and
      Abdallah) for 2000–2019? It is what the reference study used.
- [ ] How far back does PSA's bottom-30% CPI run? This sets our sample.
