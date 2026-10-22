# Who Pays for Oil Shocks? Concept Note

Oct 4, 2026 · @Lee

## Summary

**Working title:** Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households across Philippine Regions

**Target journal:** *Asian Economic Journal* (Wiley, East Asian Economic Association)

**Author:** Master's student, Graduate School of Applied Economics, University of Southeastern Philippines (macroeconomics)

This paper asks whether poor Filipino households pay more than everyone else when fuel prices spike, and whether that burden depends on where they live. It replicates the local projection design of Kpodar and Liu (2021, 2022) on Philippine data. It uses PSA's published CPI for the bottom 30% income households, available for all 17 regions, against the all-income CPI. The 2026 Middle East oil shock gives the question immediate policy weight.

## Motivation

The 2026 Middle East conflict produced the sharpest Philippine oil shock since 2008, and its cost was not shared equally. Headline inflation jumped to 4.1% in March 2026 from 2.4% in February, above the BSP's 2–4% target ([Inquirer/ANN](https://asianews.network/?p=266841)). The government declared a national energy emergency with about 45 days of fuel supply as of March 20 ([Trading Economics](https://tradingeconomics.com/philippines/currency/news/531646)).

- **Exposure.** The Philippines imports about 95% of its petroleum needs, and most of it comes from the Gulf ([IBON](https://www.ibon.org/?p=17890)).
- **Speed.** ING expected the Philippines to see the fastest pass-through among regional peers ([ANN](https://asianews.network/oil-price-surge-to-deal-heavy-blow-on-philippines/)).
- **The open question.** Cross-country evidence says fuel price increases are progressive: richer households lose more purchasing power because they spend more on transport (Kpodar and Liu, 2021). Poor Filipino households spend a larger share on food and public transport, so the second-round effect through food may dominate. Whether the global finding holds in the Philippines is unknown.

Answering it tells policymakers whether fuel subsidies, transport fare relief or targeted cash transfers protect the poor best.

## Research questions and hypotheses

The central question: **when fuel prices rise, do poor Filipino households pay more than everyone else, and does it depend on where they live?**

| # | Question | Hypothesis | Test |
| --- | --- | --- | --- |
| RQ1 | How much, and for how long, does a fuel price increase raise Philippine inflation? | Positive, persistent pass-through, peaking within 6 months, as Kpodar and Liu find for developing economies | National LP of headline CPI on retail fuel price changes |
| RQ2 | Is the burden larger for the bottom 30% than for all households? | H2a (global finding): progressive, all-income CPI rises more. H2b (Philippine alternative): regressive, bottom-30% CPI rises more through food | LP of the ratio of all-income CPI to bottom-30% CPI |
| RQ3 | Through which goods does the shock reach households? | Transport and food carry most of the pass-through; food matters more for the poor | LP by CPI component |
| RQ4 | Is the gap wider in some regions? | Wider where food shares and poverty are high and fuel must be shipped further (Mindanao, island regions) | Regional panel LP split by region characteristics |

## Reference study

We replicate [Kpodar and Liu (2021), IMF Working Paper 2021/271](https://www.imf.org/en/publications/wp/issues/2021/11/12/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation-506822), published in *Energy Economics* 108 (2022). The working paper is free and documents the full specification.

| Element | Kpodar and Liu |
| --- | --- |
| Sample | 122 countries (48 advanced, 74 developing), monthly, Jan 2000–Jun 2019; Philippines is in the developing sample |
| Shock | Monthly % change in the retail gasoline price, local currency |
| Outcomes | Headline CPI, 12 COICOP components, and quintile CPIs built from household survey shares |
| Method | Panel local projections (Jordà 2005) with the Teulings–Zubanov (2014) correction, horizons 0–11 months |
| Controls | 12 lags of CPI and fuel price changes, a time trend, country fixed effects; robustness adds the policy rate, exchange rate, world food prices |
| Inference | Standard errors clustered by country, 90% bands |
| Distribution metric | Ratio of richest-quintile CPI to poorest-quintile CPI: positive response = progressive |

**Key findings to replicate:**

- A 1 pp rise in gasoline prices raises developing-economy inflation by about 0.02 pp at peak, lasting 5–6 months.
- Transport, housing and utilities, and food carry most of the effect; 10 of 12 CPI components respond in developing economies.
- Using crude oil prices instead of retail prices understates pass-through, mostly because fuel taxes are ignored.
- The impact is progressive, and in developing economies the progressivity lasts beyond a year. It is stronger in Asia and Latin America than in Sub-Saharan Africa.

The paper reports no code package. Its regression tables (Annex Tables 1–2) give coefficients to check our implementation against.

## Contribution and AEJ positioning

AEJ has a long line of work on who bears the cost of shocks and policies in Asia, but almost all of it is microeconomic; we bring a global macroeconomic shock into that conversation. A review of AEJ's 2006–2026 contents ([IDEAS/RePEc](https://ideas.repec.org/s/bla/asiaec.html)) found no macroeconomic oil-shock paper.

| AEJ thread | Papers we engage | What we add |
| --- | --- | --- |
| Distribution of price shocks and policies | Satriawan and Shrestha (2018), Indonesian rice subsidy mistargeting; Timmer and Dawe (2007), food price instability in Asia | Evidence on who bears a fuel price shock, estimated from price data rather than simulated |
| Poverty and inequality in Southeast Asia | Warr, Rasphone and Menon (2018), Laos; Wihardja and Pradana (2024), Indonesia; Zagdbazar (2026), Mongolia | A price channel through which inequality in living standards moves month to month |
| Subnational heterogeneity | Kurita and Kurosaki (2011), regional data for Thailand and the Philippines; Pagaduan (2022), Philippine subnational GDP; Kataoka (2022), Indonesian districts; Hofer et al. (2025), poverty granularity | Regional pass-through using all 17 Philippine regions |
| Price transmission and inflation targeting | Taguchi and Sohn (2014), pass-through in East Asia; Armas (2021), Philippine bank lending channel | Pass-through of an energy price, split by income group |

**Contributions beyond the reference study:**

1. A single-country, within-country test of a cross-country finding, using official income-group CPIs rather than reconstructed ones.
2. Regional heterogeneity, which cross-country panels cannot see.
3. Coverage of the 2022 and 2026 shocks, both outside Kpodar and Liu's sample.

**Related Philippine work to cite and distinguish:** BSP's local projection study of second-round oil and food effects ([2025](https://www.sciencedirect.com/science/article/pii/S2666143825000183)) is national and not distributional. [Valera, Holmes and Delloro (2025)](https://econpapers.repec.org/RePEc:bhd:dpaper:202502) use provincial data but study inflation states, not income groups.

## Empirical strategy

We keep Kpodar and Liu's estimator unchanged and change only the unit of observation, from countries to Philippine regions and income groups.

**Step 1: Replication equation (Kpodar and Liu, eq. 1).** For country i and horizon h = 0, …, 11:

```latex
\Delta \ln CPI_{i,t+h} = \sum_{q=1}^{p} \gamma_{1q}\,\Delta \ln CPI_{i,t-q} + \sum_{q=1}^{p} \gamma_{2q}\,\Delta \ln RFP_{i,t-q} + \beta_h\,\Delta \ln RFP_{i,t} + \sum_{l=1}^{h} \gamma_{3l}\,\Delta \ln RFP_{i,t+h-l} + \gamma_4\,\tau + u_i + \varepsilon_{i,t+h}
```

RFP is the retail gasoline price in local currency, p = 12, τ a time trend, and u\_i country fixed effects. The third sum is the Teulings–Zubanov correction. β\_h is the pass-through at horizon h.

**Step 2: National Philippine model (RQ1, RQ3).** Same equation for one series (no u\_i), with Newey–West standard errors. The outcome is headline CPI, then each CPI component in turn.

**Step 3: Distributional model (RQ2).** The outcome becomes the log ratio of the all-income CPI to the bottom-30% CPI:

```latex
D_{t} = \ln\left( \frac{CPI^{\,all}_{t}}{CPI^{\,b30}_{t}} \right)
```

A positive β\_h means fuel shocks raise prices for the average household more than for the poor (progressive). A negative β\_h means the poor pay more (regressive). Our contrast is milder than Kpodar and Liu's richest-versus-poorest ratio, because the all-income CPI includes the poor. An extension backs out a "non-poor" CPI from FIES expenditure weights.

**Step 4: Regional panel (RQ4).** For region r = 1, …, 17, with region fixed effects and Driscoll–Kraay standard errors, since all regions face the same national shocks:

```latex
D_{r,t+h} = \sum_{q=1}^{12} \gamma_{1q} D_{r,t-q} + \sum_{q=1}^{12} \gamma_{2q}\,\Delta \ln RFP_{r,t-q} + \beta_h\,\Delta \ln RFP_{r,t} + \theta_h\,(\Delta \ln RFP_{r,t} \times G_r) + \sum_{l=1}^{h} \gamma_{3l}\,\Delta \ln RFP_{r,t+h-l} + u_r + \varepsilon_{r,t+h}
```

G\_r marks a group of regions (high poverty, high food share, Mindanao or island). θ\_h measures the extra pass-through in that group.

**Step 5: Crude versus retail.** Re-run Steps 2 and 3 with Dubai crude in pesos as the shock. This replicates the paper's finding that crude oil understates pass-through, now for a country with deregulated prices and fuel excise taxes.

## Data inventory

Every core series is public and monthly; the main work is splicing CPI base years and confirming how far back the bottom-30% series runs.

| Variable | Source | Frequency, level | Notes and checks |
| --- | --- | --- | --- |
| All-income CPI, headline and COICOP components | PSA OpenSTAT | Monthly, national and 17 regions | 2018=100 from 2022; splice to 2012 and 2006 bases |
| Bottom-30% income households CPI | PSA OpenSTAT; regional releases (e.g. [RSSO VII](https://rsso07.psa.gov.ph/node/1684058199), [RSSO XI Davao](https://rsso11.psa.gov.ph/cpi-all-infographics)) | Monthly, national and 17 regions | Confirm start year and component detail before committing to the sample |
| Retail fuel price (shock) | [World Bank Global Fuel Prices Database](https://datacatalog.worldbank.org/search/dataset/0066829/global-fuel-prices-database); DOE Oil Monitor | Monthly national (WB, from Dec 2015); weekly NCR and regional (DOE) | Regional proxy: CPI sub-index for fuels and lubricants for personal transport, by region |
| Crude oil price | Dubai and Brent, World Bank Pink Sheet | Monthly | Convert to pesos with BSP exchange rate |
| Exchange rate, policy rate | BSP | Monthly | Robustness controls, as in the reference study |
| World food prices | FAO Food Price Index | Monthly | Robustness control |
| Expenditure shares by income group | PSA FIES (2015, 2018, 2021, 2023) | Triennial, by region | For the "non-poor" CPI extension and G\_r grouping |
| Poverty incidence | PSA official poverty statistics | Triennial, by region | Defines high- versus low-poverty regions |

**Open questions to settle first:**

- [ ] How many years of bottom-30% CPI exist across base years? This sets the sample.
- [ ] Is the regional fuels-and-lubricants CPI sub-index published on OpenSTAT for all 17 regions?
- [ ] Does BARMM (formerly ARMM) have a consistent series across the regional reorganisations?

## Robustness and threats to identification

The main threat is that domestic fuel prices respond to Philippine conditions; we answer it by also using world crude prices, which no Philippine region can move.

| Threat | Why it matters | Response |
| --- | --- | --- |
| Fuel price endogeneity | Pump prices include the peso and local margins that move with domestic demand | Re-estimate with peso Dubai crude (Step 5) and with an identified oil supply shock (Baumeister–Hamilton or Känzig) as an instrument |
| Peso depreciation confounds the shock | 2026 combined an oil shock and a record-weak peso | Control for the exchange rate, as in the reference study's robustness check |
| Monetary policy response | BSP tightening dampens later inflation | Control for the policy rate |
| Policy interventions | Excise suspensions, fuel subsidies, fare increases with lags | Event dummies for major interventions; report with and without 2020 and 2026 |
| Spliced CPI base years | Weight changes create breaks | Splice on overlap months; re-estimate on the 2018-base window only |
| Common shocks across regions | Biases standard errors in the panel | Driscoll–Kraay errors; leave-one-region-out estimates |
| Lag length | LP results can be sensitive to p | p = 6, 12, 18 |
| Asymmetry | Increases may pass through more than decreases | Split positive and negative price changes, a simple extension used by Kpodar and Abdallah (2020) |

## Implementation roadmap in Claude Code

The whole project runs as one scripted repository, so every number and figure in the paper can be regenerated with a single command. Claude Code writes and runs the code, drafts text, and keeps a decisions log; you supply judgment, adviser feedback, and any downloads that need a browser login.

&#91;embedded content: project roadmap · 6 phases, 5 gates\]

The replication phase is the hinge: nothing Philippine is estimated until our code reproduces the reference study's results.

**Repository layout:**

```
oil-shock-distribution/
├── CLAUDE.md          project brief, conventions, decisions log
├── data/raw/          untouched downloads + source_log.md
├── data/processed/    cleaned national and regional panels
├── R/                 01_download, 02_clean, 03_replicate,
│                      04_estimate, 05_robustness, 06_figures
├── output/            tables/ and figures/ written by scripts
├── paper/             Quarto manuscript + references.bib
├── submission/        cover letter, highlights, replication package
└── renv.lock          pinned package versions
```

**Tool stack:** R for estimation (`fixest` for the panel local projections and Driscoll–Kraay errors, `sandwich` for Newey–West, `data.table` for cleaning, `ggplot2` and `sf` for figures and the regional map, `modelsummary` for tables). Quarto turns the manuscript into Word or PDF for AEJ. Python stays available for scraping the DOE price bulletins if needed. Git records every change for the replication package.

## Next actions

The first two weeks decide feasibility: if the bottom-30% CPI runs back far enough, everything else follows.

- [ ] Share this note with the adviser and confirm the reference study and the AEJ target
- [ ] Pull the bottom-30% and all-income CPI series from PSA OpenSTAT and record each base year's start and end
- [ ] Check the regional fuels-and-lubricants CPI sub-index and the DOE regional pump price data
- [ ] Download the World Bank Global Fuel Prices Database and the Pink Sheet crude series
- [ ] Set up the project repository in Claude Code (structure below) and commit the raw data with a source log
- [ ] Replicate the reference study's developing-economy result on its own data or a subsample, as an implementation check
- [ ] Request the *Energy Economics* version through the USeP library to confirm any changes from the working paper

## Sources

- [Kpodar and Liu (2021), IMF Working Paper 2021/271](https://www.imf.org/en/publications/wp/issues/2021/11/12/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation-506822); [full text](https://imf.org/-/media/Files/Publications/WP/2021/English/wpiea2021271-print-pdf.ashx)
- [Kpodar and Liu (2022), *Energy Economics* 108](https://ferdi.fr/publications/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation)
- [Asian Economic Journal contents, 2016–2026](https://ideas.repec.org/s/bla/asiaec.html) and [2006–2016](https://ideas.repec.org/s/bla/asiaec2.html)
- [BSP study on second-round effects of oil and food shocks (2025)](https://www.sciencedirect.com/science/article/pii/S2666143825000183)
- [Valera, Holmes and Delloro (2025), BSP DP 2025-02](https://econpapers.repec.org/RePEc:bhd:dpaper:202502)
- [World Bank Global Fuel Prices Database](https://datacatalog.worldbank.org/search/dataset/0066829/global-fuel-prices-database)
- [PSA RSSO VII, bottom-30% CPI release](https://rsso07.psa.gov.ph/node/1684058199); [PSA RSSO XI CPI infographics](https://rsso11.psa.gov.ph/cpi-all-infographics)
- [Inquirer/ANN, March 2026 inflation](https://asianews.network/?p=266841); [Trading Economics, peso and energy emergency](https://tradingeconomics.com/philippines/currency/news/531646); [ANN, ING on pass-through](https://asianews.network/oil-price-surge-to-deal-heavy-blow-on-philippines/); [IBON on import dependence](https://www.ibon.org/?p=17890)

Other methodological references (Jordà 2005; Teulings and Zubanov 2014; Choi et al. 2018; Kpodar and Abdallah 2020; Driscoll and Kraay 1998) are cited from Kpodar and Liu's reference list and standard practice; full entries go in the manuscript bibliography.
