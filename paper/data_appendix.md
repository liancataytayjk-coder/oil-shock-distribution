# Appendix A. Data appendix

This appendix gives everything needed to reproduce each figure and table in this paper. Section A.1 explains how to rebuild the results. Section A.2 lists every data source with its link. Section A.3 maps each figure and table to its sources, the script that computes it and the output file it is drawn from.

## A.1 How to reproduce the results

All data are public, and all processing is done by scripts. Nothing is copied or typed by hand. The replication package contains the raw files exactly as downloaded, with a source log; the code; the decision log; and the output tables and figures. The repository is <https://github.com/liancataytayjk-coder/oil-shock-distribution>, branch `claude/bold-hamilton-0ixcim`, also supplied as a zip file with this paper.

The package needs Python 3.11 and the packages listed in `requirements.txt`. With these installed, the command `./run_all.sh` rebuilds everything from the stored raw files. In order, it cleans the data, builds the national and regional panel, runs the EU replication test, estimates the models, runs the 2026 analysis and the descriptive statistics, draws the figures, writes the documents and runs the automated tests.
To download fresh copies of the PSA tables first, run `./run_all.sh --download`.

Each raw file is listed in `data/raw/source_log.md` with its URL, download date, base year and coverage. All files were downloaded on 4 October 2026.

PSA OpenSTAT tables are read through the PxWeb interface, using the table addresses below. Opening an address in a browser returns the table's description. The script `scripts/01_download_psa.py` sends the query that returns the data, one geography at a time. The same tables can be viewed by hand on the OpenSTAT website (<https://openstat.psa.gov.ph>), under *Economic Indices → Prices → Consumer Price Index*.

## A.2 Data sources

**S1. PSA, CPI for all income households, 2018 = 100, old geographic code (17 regions).** We use this source for all items and all commodity groups, national and regional; the fuel price index, sub-index 07.2.2 (fuels and lubricants for personal transport equipment); and the basket weights.
The tables are listed below.

*Backcast, Jan 1994–Dec 2017:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP15.px>

*Jan 2018–Dec 2025:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP09.px>

*2018 weights:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP12.px>

**S2. PSA, CPI for all income households, 2018 = 100, new geographic code (Negros Island Region separate).** We use this source for the January–August 2026 months, chained onto S1 (decision D6); the gasoline sub-index 07.2.2.2; and the 2018 weights used in the 2026 decomposition.
The tables are listed below.

*Jan 2018–Aug 2026:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018NEW/0012M4ACP22.px>

*Backcast, 1994–2017:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018NEW/0012M4ACP28.px>

*Weights:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018NEW/0012M4ACP25.px>

**S3. PSA, CPI for the bottom 30% income households, 2018 = 100, old geographic code.** The tables are listed below.

*All-items backcast, Jan 2000–Dec 2011:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT5.px>

*Commodity-group backcast, Jan 2012–Dec 2017:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT4.px>

*Jan 2018–Dec 2025:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT1.px>

*2018 weights:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT3.px>

**S4. PSA, CPI for the bottom 30% income households, 2018 = 100, new geographic code.** We use this source for the January–August 2026 months, chained onto S3, and for the weights used in the 2026 decomposition. The tables are listed below.

*Jan 2018–Aug 2026:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018NEW/0022M4ABIR1.px>

*Weights:* <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018NEW/0022M4ABIR3.px>

**S5. PSA, official poverty statistics by region, 2018, 2021 and 2023.** We use poverty incidence among the population and the annual per-capita poverty threshold. Table: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1F/FY/0031F3DF020.px>.

**S6. World Bank, Commodity Price Data (Pink Sheet), monthly.** We use Dubai and Brent crude oil prices in US dollars per barrel. File: <https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx>.

**S7. World Bank, Global Fuel Prices Database (April 2025 version).** We use the Philippine row, the Manila regular gasoline (RON 91) pump price in pesos per litre. File: <https://datacatalogfiles.worldbank.org/ddh-published/0066829/DR0095290/Global_Fuel_Prices_Database.xlsx>.

**S8. Bangko Sentral ng Pilipinas, peso–dollar exchange rate, monthly average.** File: <https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx>.

**S9. Bank for International Settlements, central bank policy rates, Philippines.** Data: <https://stats.bis.org/api/v1/data/WS_CBPOL/M.PH?format=csv>.

**S10. FAO Food Price Index, nominal, 2014–2016 = 100.** File: <https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/food_price_indices_data.csv>.

**S11. Eurostat, harmonised index of consumer prices (HICP), all items and fuels and lubricants (CP0722), 2015 = 100.** Data: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/prc_hicp_midx/M.I15.CP00+CP0722.?format=TSV>.

**S12. European Commission, Weekly Oil Bulletin, price history with and without taxes.** File: <https://energy.ec.europa.eu/document/download/906e60ca-8b6a-44e7-8589-652854d2fd3f_en?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx>.

**S13. Eurostat, euro–dollar exchange rate, monthly average.** We use it to convert Brent crude to euros. Data: <https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/ert_bil_eur_m/M.AVG.NAC.USD?format=TSV>.

**S14. Reference coefficients.** These are the published estimates of Kpodar and Liu (2021, IMF Working Paper WP/21/271), typed from the paper's figures and annex tables into `replication/kpodar_liu_2021_targets.csv`. Paper: <https://www.imf.org/en/publications/wp/issues/2021/11/12/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation-506822>.

**S15. 2026 policy facts.** These are the laws, executive orders and agency issuances cited in Chapter 5. Each one is listed with its source link and verification status in `paper/policy_context_2026.md`.

## A.3 Sources, scripts and output files for each figure and table

Scripts are in `scripts/`, output tables in `output/tables/` and figures in `output/figures/`. Every script after the first two reads the processed files written by `02_clean_psa.py` and `03_build_panel.py`. The figures are written by `06_figures.py`, and the tables are inserted into this document by `08_paper.py`.

**Table A1. Sources, scripts and output files**

| Item | Content | Sources | Computed by | Output file |
|---|---|---|---|---|
| Figure 1 | Conceptual framework | — | 06_figures.py | figw0_framework.png |
| Table 1 | Data sources and variables | S1–S13 | — | — |
| Table 2 | Summary statistics | S1–S4 | 09_descriptive.py | desc_summary.csv |
| Figure 2 | Inflation trends and the gap | S1–S4 | 09_descriptive.py | desc_yoy_national.csv; figd1_trends.png |
| Table 3 | Annual inflation | S1–S4 | 09_descriptive.py | desc_annual.csv |
| Table 4 | Fuel-shock episodes | S1–S4 | 09_descriptive.py | desc_episodes.csv |
| Table 5 | Cross-correlations | S1–S4 | 09_descriptive.py | desc_crosscorr.csv |
| Figure 3 | Regional inflation and gap | S1–S5 | 09_descriptive.py | desc_regional.csv; figd2_regional.png |
| Table 6 | Regional summary | S1–S5 | 09_descriptive.py | desc_regional.csv |
| Table 7 | Unit-root tests | S1–S4 | 09_descriptive.py | desc_adf.csv |
| Table 8 | Validation against the reference study | S1, S3, S6, S11–S14 | 04_replicate.py | replication_eu_ph.csv; replication_gate.csv |
| Figure 4, Table 9 | Pass-through to the price level and the gap | S1–S4 | 05_estimate.py | estimates.csv; fig1_rq1_passthrough.png |
| Figure 5 | Response of the gap, national and panel | S1–S4 | 05_estimate.py | estimates.csv; fig2_rq2_rq4_ratio.png |
| Figure 6, Table 10 | Pass-through by CPI division | S1, S3 | 05_estimate.py | estimates.csv; rq3_gap_decomposition.csv; fig3_rq3_components.png |
| Figure 7, Table 11 | Regional groups | S1–S5 | 05_estimate.py | estimates.csv; region_groups.csv; fig4_rq4_groups.png |
| Figure 8, Table 12 | Robustness | S1–S10 | 05_estimate.py | estimates.csv; fig5_robustness.png |
| Figure 9 | 2026: actual and predicted | S1–S4 | 07_episode_2026.py | e1_national_2026.csv; fig6_2026_out_of_sample.png |
| Table 13 | 2026 by region; peso cost | S1–S5 | 07_episode_2026.py | e2_regional_2026.csv |
| Figure 10 | 2026 gap by item | S2, S4 | 07_episode_2026.py | e5_decomposition_2026.csv; fig7_2026_gap_decomposition.png |
| Table 14 | Household fuels, fares, cereals | S1, S3 | 07_episode_2026.py | e4_mechanism.csv |
| Table 15 | Policy instruments | S15; Tables 9–14 | — | — |

*Notes:* S1–S4 enter as the national and regional all-income CPI, the bottom-30% CPI and the fuel index (07.2.2), spliced and chained by `03_build_panel.py` (decisions D6 and D7). Robustness (Table 12) also uses S6 and S8 (Dubai crude in pesos), S7 (pump price), S9 (policy rate) and S10 (world food prices). Every number in the text comes from `output/tables/paper_numbers.json`, which `08_paper.py` writes from the files above.
