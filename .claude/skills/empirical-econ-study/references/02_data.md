# Phase 2 — Data collection and construction

Goal: a clean dataset built by scripts from untouched raw files, where every
choice about splicing, geography and proxies is logged and checked.

## 2.1 Where to look (official sources first)

Prefer official, documented and API-accessible sources. These are the ones used
before, and where they live:

| Need | Source | Access |
|---|---|---|
| Philippine CPI (all income, bottom 30%), sub-indices, weights, regional | PSA OpenSTAT | PxWeb API `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/` (CPI/ and BIH/ folders) |
| Poverty incidence by region | PSA OpenSTAT | `DB/1F/FY/0031F3DF020.px` |
| Crude oil (Dubai, Brent), commodity prices | World Bank Pink Sheet | `CMO-Historical-Data-Monthly.xlsx` |
| Retail pump prices across countries | World Bank Global Fuel Prices Database | xlsx; Manila only for PH, 2015/2017–Apr 2025 |
| Peso–dollar rate | BSP | `bsp.gov.ph/Statistics/External/pesodollar.xlsx` |
| Policy rates | BIS | `stats.bis.org/api/v1/data/WS_CBPOL/M.<CC>?format=csv` |
| World food prices | FAO Food Price Index | csv |
| EU consumer prices | Eurostat API | `prc_hicp_midx` |
| EU pump prices before and after tax | EC Weekly Oil Bulletin | history xlsx |

For other countries, look for the national statistics office's API (many run
PxWeb), then the central bank, then the international databases above. If the
network blocks a host, say so and ask the user to widen access. Do not substitute
a weaker source without telling them.

## 2.2 Download rules

- Write one download script per source family
  (`scripts/01_download_<source>.py`). Use `scripts/pxweb_download.py` for PxWeb.
- Save responses unchanged, gzipped, to `data/raw/<source>/<descriptive_name>.csv.gz`.
  Name each file with its base year and coverage, for example
  `cpi_b30_2018old_backcast_allitems_2000_2011`.
- Add a row to `data/raw/source_log.md` immediately: file, URL or API table id,
  base or units, coverage, notes (quirks such as "Region XII labelled Reg12").
- Problems seen before:
  - PxWeb cell limits: query one geography at a time.
  - Responses in Latin-1: fall back on decode errors.
  - Inconsistent region labels: use a broad regex and check that you get the
    full count of regions.
  - Dates not at month start: convert with `to_period("M")`.

## 2.3 Cleaning and construction

`02_clean_*.py` should produce long tables (geo × item × month). `03_build_panel.py`
should produce the analysis panel. Decisions that usually arise:

- **Base years and splicing.** Prefer the agency's own backcasts on the current
  base, such as PSA's 2018 = 100 back series. Where you must join series:
  - join on growth rates;
  - measure the jump at each join (mean absolute monthly change at the join
    month against overall);
  - log it as a decision;
  - add a robustness check with dummies for the join months (D7).
- **Geography that changes over time.** New regions, split provinces and renamed
  areas need care:
  1. Pick the coding for which the long history exists. In the worked example
     this was the old 17-region code.
  2. Check that the codings agree where they overlap.
  3. Chain the new-code growth onto old-code levels for the recent months.
  4. Flag the affected units and months, for example `new_geo_ext`.
  5. Add a robustness check that drops them (D6).
  6. Keep an open question for anything unconfirmed, such as the BARMM boundary
     history.
- **Proxies.** When the ideal variable does not exist (here, regional retail pump
  prices), choose the closest official series, here CPI sub-index 07.2.2. Then
  validate it against an independent series over their overlap; correlations of
  monthly changes were 0.87 with the World Bank pump price and 0.99 with the
  gasoline index. Plan robustness checks with each alternative proxy, plus a
  shock that is exogenous by construction, such as world crude in local currency.
- **Units.** Use 100·Δln for every rate, so coefficients read as "percentage
  points per 1% change".
- **Heterogeneity groups.** Define groups (high poverty, high food share, island,
  Mindanao, …) *before* estimation, from pre-period data such as 2018. Use simple
  rules such as "above the median of the units". Save membership to
  `output/tables/<groups>.csv`. These groups are the study's own constructions,
  not official categories; say so in the paper.

## 2.4 Gate

The gate for Phase 2 has four checks:

- every raw file is logged;
- the panel has the expected units and months;
- the proxies are validated;
- the processed data rebuild from raw with one command.
