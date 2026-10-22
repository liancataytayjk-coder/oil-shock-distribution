# Source log

One entry per raw file. Never edit a raw file; download it again and log a new entry.
All files were downloaded on 2026-10-04 (see `archive/v1_full/data/raw/` for the original
compressed copies). PSA tables are stored here as plain CSV: the API responses, stacked one
geography at a time, decompressed but otherwise unchanged. Source IDs (S1-S11) match the
codebook (`codebook/codebook.xlsx`, sheet Sources) and the papers' data appendix.

| File | ID | Source / URL | Base / units | Coverage | Notes |
| --- | --- | --- | --- | --- | --- |
| `psa/cpi_all_2018old_backcast_1994_2017.csv` | S1 | PSA OpenSTAT API, `DB/2M/PI/CPI/2018/0012M4ACP15.px` | 2018=100 | Jan 1994–Dec 2017; PH and 17 regions (old code) | Gasoline (07.2.2.2) absent before 2018; 07.2.2 present. |
| `psa/cpi_all_2018old_2018_2025.csv` | S1 | `CPI/2018/0012M4ACP09.px` | 2018=100 | Jan 2018–Dec 2025 | Old geographic code. |
| `psa/cpi_all_2018old_weights.csv` | S1 | `CPI/2018/0012M4ACP12.px` | % of basket | 2018 | |
| `psa/cpi_all_2018new_2018_2026.csv` | S2 | `CPI/2018NEW/0012M4ACP22.px` | 2018=100 | Jan 2018–Aug 2026; PH, 17 regions, NIR | New geographic code. |
| `psa/cpi_all_2018new_weights.csv` | S2 | `CPI/2018NEW/0012M4ACP25.px` | % of basket | 2018 | |
| `psa/cpi_b30_2018old_backcast_allitems_2000_2011.csv` | S3 | `BIH/2018/0022M4ABOT5.px` | 2018=100 | Jan 2000–Dec 2011, all items only | Sets the start of the distributional sample. |
| `psa/cpi_b30_2018old_backcast_2012_2017.csv` | S3 | `BIH/2018/0022M4ABOT4.px` | 2018=100 | Jan 2012–Dec 2017, by commodity | |
| `psa/cpi_b30_2018old_2018_2025.csv` | S3 | `BIH/2018/0022M4ABOT1.px` | 2018=100 | Jan 2018–Dec 2025 | Region XII labelled "Reg12". |
| `psa/cpi_b30_2018old_weights.csv` | S3 | `BIH/2018/0022M4ABOT3.px` | % of basket | 2018 | |
| `psa/cpi_b30_2018new_2018_2026.csv` | S4 | `BIH/2018NEW/0022M4ABIR1.px` | 2018=100 | Jan 2018–Aug 2026 | New geographic code. |
| `psa/cpi_b30_2018new_weights.csv` | S4 | `BIH/2018NEW/0022M4ABIR3.px` | % of basket | 2018 | |
| `psa/poverty_population_2018_2023.csv` | S5 | PSA OpenSTAT API, `DB/1F/FY/0031F3DF020.px` | %, PHP | 2018, 2021, 2023; regions and provinces | Footnote markers in labels. |
| `wb/CMO-Historical-Data-Monthly.xlsx` | S6 | https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx | USD/bbl | Jan 1960–Sep 2026 | Pink Sheet, updated 2 Oct 2026. |
| `wb/Global_Fuel_Prices_Database.xlsx` (+ methodology PDF) | S7 | https://datacatalogfiles.worldbank.org/ddh-published/0066829/DR0095290/Global_Fuel_Prices_Database.xlsx | PHP/litre | PH: Jan 2017–Mar 2025 | Version April 2025. |
| `bsp/pesodollar.xlsx` | S8 | https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx | PHP per USD | 1945–Sep 2026 | Monthly averages. |
| `bis/bis_cbpol_ph_monthly.csv` | S9 | https://stats.bis.org/api/v1/data/WS_CBPOL/M.PH?format=csv | % end of period | 1986–Aug 2026 | |
| `fao/food_price_indices_data.csv` | S10 | https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/food_price_indices_data.csv | 2014–16=100 | 1990–Sep 2026 | |
| `extracts/*.csv` | S6–S8 | Written by `code/python/01_extract_excel.py` | as source | as source | The columns used from the three Excel files, copied without changing values (one row per month), so that Stata can read them. |

Not used in this version (kept in `archive/v1_full/data/raw/`): EU data for the replication
gate, and the PSA 2012-base and 2000-base tables.
