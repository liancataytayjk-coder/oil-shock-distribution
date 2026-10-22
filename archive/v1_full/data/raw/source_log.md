# Source log

One entry per raw file. Never edit a raw file; re-download and log a new entry.
All files below were pulled on 2026-10-04.

| File | Source / URL | Base / units | Coverage | Notes |
| --- | --- | --- | --- | --- |
| `psa/cpi_all_2018new_2018_2026.csv.gz` | PSA OpenSTAT API, `DB/2M/PI/CPI/2018NEW/0012M4ACP22.px` | 2018=100 | Jan 2018–Aug 2026; PH, NCR, AONCR, 17 regions + NIR; full COICOP 2018 detail | New geographic code (Negros Island Region separate). Pulled by `scripts/01_download_psa.py`. |
| `psa/cpi_all_2018new_backcast_1994_2017.csv.gz` | `CPI/2018NEW/0012M4ACP28.px` | 2018=100 (backcast) | Jan 1994–Dec 2017 | Gasoline (07.2.2.2) and diesel absent before 2018; 07.2.2 present. |
| `psa/cpi_all_2018new_weights.csv.gz` | `CPI/2018NEW/0012M4ACP25.px` | weights | 2018 basket | |
| `psa/cpi_all_2018old_*.csv.gz` (3 files) | `CPI/2018/0012M4ACP09/15/12.px` | 2018=100 | 1994–Dec 2025 | Old geographic code; used for the main panel. |
| `psa/cpi_all_2012_*.csv.gz` (3 files) | `CPI/2012/0012M4ACPI1/4/3.px` | 2012=100 | 1994–Dec 2021 | Robustness only. |
| `psa/cpi_b30_2018new_*.csv.gz` (2 files) | `BIH/2018NEW/0022M4ABIR1/3.px` | 2018=100 | Jan 2018–Aug 2026 | Bottom-30% income households. |
| `psa/cpi_b30_2018old_2018_2025.csv.gz`, `..._weights` | `BIH/2018/0022M4ABOT1/3.px` | 2018=100 | Jan 2018–Dec 2025 | Region XII labelled "Reg12" in the source. |
| `psa/cpi_b30_2018old_backcast_2012_2017.csv.gz` | `BIH/2018/0022M4ABOT4.px` | 2018=100 (backcast) | Jan 2012–Dec 2017, by commodity | |
| `psa/cpi_b30_2018old_backcast_allitems_2000_2011.csv.gz` | `BIH/2018/0022M4ABOT5.px` | 2018=100 (backcast) | Jan 2000–Dec 2011, all items only | Sets the start of the distributional sample. |
| `psa/cpi_b30_2012_*.csv.gz`, `psa/cpi_b30_2000_*.csv.gz` | `BIH/2012/0022M4AB301/303/305/311.px` | 2012=100, 2000=100 | 2000–2022 | Robustness; 2000-base has 38 old-classification groups. |
| `psa/poverty_population_2018_2023.csv` | PSA OpenSTAT API, `DB/1F/FY/0031F3DF020.px` | % of population | 2018, 2021, 2023; region and province | Official poverty incidence among population. Pulled by `scripts/01b_download_poverty.py`. Footnote markers in labels. |
| `wb/CMO-Historical-Data-Monthly.xlsx` | https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx | USD/bbl | 1960–Sep 2026 | World Bank Pink Sheet, updated 2 Oct 2026. Dubai, Brent. |
| `wb/Global_Fuel_Prices_Database.xlsx` (+ methodology PDF) | https://datacatalogfiles.worldbank.org/ddh-published/0066829/DR0095290/Global_Fuel_Prices_Database.xlsx | LCU/litre | Dec 2015–Apr 2025 | Version April 2025. PH row: Manila RON 91. |
| `bsp/pesodollar.xlsx` | https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx | PHP per USD, monthly average | 1945–Sep 2026 | |
| `bis/bis_cbpol_ph_monthly.csv` | https://stats.bis.org/api/v1/data/WS_CBPOL/M.PH?format=csv | % end of period | 1986–Aug 2026 | BSP policy rate as compiled by the BIS. |
| `fao/food_price_indices_data.csv` | https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/food_price_indices_data.csv | 2014–16=100 | 1990–Sep 2026 | FAO Food Price Index, nominal. |
| `eurostat/prc_hicp_midx_cp00_cp0722.tsv.gz` | Eurostat API `prc_hicp_midx/M.I15.CP00+CP0722.` | 2015=100 | 1996–2026 | Replication gate (G3). |
| `eurostat/Weekly_Oil_Bulletin_Prices_History.xlsx` | https://energy.ec.europa.eu/document/download/906e60ca-8b6a-44e7-8589-652854d2fd3f_en?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx | EUR/1000 l | weekly 2005–Sep 2026 | Prices with and without taxes; gate G1–G2. |
| `eurostat/ert_bil_eur_m_usd.tsv.gz` | Eurostat API `ert_bil_eur_m/M.AVG.NAC.USD` | USD per EUR | 1971–2026 | Converts Brent to euro (G2). |
| (reference paper, not committed) | https://www.imf.org/en/publications/wp/issues/2021/11/12/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation-506822 | — | — | Kpodar and Liu (2021), WP/21/271. Coefficients in `replication/kpodar_liu_2021_targets.csv`. |

Not obtainable: the Kpodar–Abdallah Global Monthly Retail Fuel Price Database used
by the reference study is not publicly downloadable (2026-10-04 search).
