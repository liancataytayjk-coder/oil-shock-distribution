---
title: "Who Pays for Oil Shocks? Fuel Price Pass-Through to the Inflation of Poor Households across Philippine Regions"
author:
  - "Lian Cataytay[^aff]"
date: "November 2026"
abstract: |
  Cross-country evidence finds that fuel price increases are progressive: they raise prices more for richer households. We test this within one country, using the Philippine Statistics Authority's official consumer price indices for the bottom 30% income households and for all households, nationally and for 17 regions, from 2001 to 2026. Following Kpodar and Liu (2022), we estimate local projections of each index on the CPI sub-index for retail motor fuels. A 1% rise in retail fuel prices raises the price level by 0.044 percentage points within the month and by 0.102 after a year; world crude prices capture only about 40% of this. The effect is not progressive: in the regional panel, the bottom 30%'s prices rise 0.0214 percentage points more than all households' after six months. Budget shares alone would predict the opposite sign, so the gap comes from larger price increases within the categories the poor buy. The effect is concentrated in 2001–2012 and weakens with macroeconomic controls. A model estimated on data to 2025 explains about half of the 2026 oil-shock price surge; the fuel-driven extra cost for a poverty-line family of five reached about PHP 467 a month, and rice accounted for most of the poor's excess inflation. Relief on gasoline and diesel taxes would mainly benefit better-off households; transfers sized with the bottom-30% CPI are better targeted.

  **Keywords:** oil price shocks; inflation inequality; fuel prices; local projections; Philippines

  **JEL classification:** E31, Q41, I32, D31, R12
bibliography: references.bib
link-citations: true
---

[^aff]: Graduate School of Applied Economics, University of Southeastern Philippines, Davao City.

# 1. Introduction

When oil prices rise, who pays? The question matters for every government that must decide whether to cut fuel taxes, subsidise fuel or transfer cash after an oil shock. The best cross-country evidence gives a clear answer. Using retail fuel prices for 122 countries and price indices for income quintiles rebuilt from household surveys, @kpodar_liu_2022 find that fuel price increases are *progressive*: the richest households' prices rise more, because they spend more on cars and fuel. If this holds generally, broad fuel tax relief mainly helps the better-off.

This paper tests that finding within one country, the Philippines, where it may not hold. Poor Filipino households spend more than half of their budget on food (54.9% in the 2018 basket, against 37.7% for all households) and travel by public transport, so they may feel oil shocks mostly through food and fares rather than through fuel. Moreover, the cross-country method gives every income group the same price for each spending category and lets only budget shares differ. Yet households with different incomes buy different items within categories and pay different prices for them [@kaplan_schulhofer_2017; @jaravel_2021]. The Philippine Statistics Authority (PSA) publishes an official consumer price index (CPI) for the bottom 30% income households, monthly and by region, built from their own budget shares at a detailed item level. This allows a direct test that captures both channels.

The question became urgent in 2026. An oil shock caused by the conflict in the Middle East raised the CPI sub-index for retail motor fuels 76% above its level a year earlier by April. Headline inflation rose from 2.4% in February to 7.2% in April, and inflation for the bottom 30% reached 8.5%. Republic Act 12316 gave the President standby authority to suspend petroleum excise taxes [@ra12316_2026]; the government used it for LPG and kerosene but not for gasoline and diesel, gave subsidies to transport drivers, and the central bank raised its policy rate three times.

We ask three questions. How much, and how fast, do retail fuel prices pass through to the price level of all households and of the bottom 30% (RQ1)? Do the bottom 30% face larger price increases than all households, nationally and across regions, and why (RQ2)? What did the 2026 shock cost poor families, and how well were the policy responses targeted (RQ3)?

We find that fuel prices pass through quickly and lastingly: a 10% rise in retail fuel prices makes the price level about 1.0% higher a year later, more than twice what crude oil prices imply. The effect is not progressive. In a panel of 17 regions, the bottom 30%'s price level rises 0.0214 percentage points more than all households' after six months per 1% fuel price rise, a significant regressive effect; nationally the sign is the same but the estimate is less precise. Budget shares alone would make the effect progressive, so the regressive gap comes from larger price increases within the categories the poor buy. The effect is strongest in 2001–2012 and shrinks with macroeconomic controls. Applied to 2026, a model estimated only on earlier data explains about half of the price surge and predicts the direction of the gap; most of the poor's excess inflation came through rice.

The paper contributes to three literatures. First, it adds a within-country test with official income-group price indices to the cross-country evidence on fuel price pass-through [@kpodar_abdallah_2017; @choi_etal_2018; @kpodar_liu_2022], and finds the opposite sign. Second, it connects that literature to work on inflation inequality [@hobijn_lagakos_2005; @kaplan_schulhofer_2017; @jaravel_2021], showing that differences within categories, which reconstructed indices cannot capture, decide who bears an oil shock. Third, it extends Philippine and Asian work on oil, food and inflation [@jongwanich_park_2011; @allon_pineda_etal_2026; @valera_etal_2025; @fujii_2013; @domingo_etal_2009] to income groups and regions, and to the 2026 shock.

# 2. Framework

Fuel enters almost every price. In the input–output price model [@miller_blair_2009], if margins and other costs are unchanged, a fuel price shock $f_t = 100\,\Delta\ln F_t$ raises the price of good *k* in proportion to its total (direct and indirect) fuel cost share $\phi_k$: $\pi_{k,t} \approx \phi_k f_t$. A group's CPI is a weighted average of item prices with that group's budget shares $w^g_k$, so its inflation is $\pi^g_t \approx \sum_k w^g_k \pi_{k,t}$, and

$$\pi^g_t \approx \Phi^g f_t, \qquad \Phi^g = \sum_k w^g_k \phi_k \qquad\qquad (1)$$

A group's pass-through equals the fuel intensity of its basket. The shock is progressive if the average basket ($g = A$, all households) is more fuel-intensive than the poor's ($g = B$, bottom 30%), and regressive otherwise. We measure the difference with the inflation gap $D_t = 100 \ln(P^A_t / P^B_t)$, whose monthly change is $\Delta D_t = \pi^A_t - \pi^B_t$; a fall in $D$ means the poor's prices rose more. The gap splits exactly into two parts:

$$\pi^A_t - \pi^B_t = \sum_k (w^A_k - w^B_k)\, \pi^A_{k,t} + \sum_k w^B_k\, (\pi^A_{k,t} - \pi^B_{k,t}) \qquad\qquad (2)$$

The first term is a *weights effect*, which is all that cross-country indices built from survey budget shares can capture. The second is a *within-category effect*, which arises because the groups buy different items inside each category. Finally, following @deaton_1989, the rise in a group's CPI approximates the extra spending the group needs to buy the same basket, which lets us express the burden of a shock in pesos. Energy shocks also act through a slower indirect route and through wages and expectations [@kilian_2008; @blanchard_gali_2010], so we trace their effects over a year. Figure 1 summarises the framework.

![Figure 1. Conceptual framework: the retail fuel price shock (X) and the inflation of each household group and the gap between them (Y).](../output/figures/fig01_conceptual_framework.png){width=90%}

# 3. Data and method

## 3.1 Data

All price data are monthly PSA consumer price indices on the 2018 = 100 base [@psa_openstat_2026]: the all-income CPI and its 13 divisions (from January 1994), the bottom-30% CPI (from January 2000; divisions from 2012) and, as the fuel price, the CPI sub-index 07.2.2 for fuels and lubricants for personal transport, nationally and for 17 regions. The reference study's retail price database is not public; the PSA fuel index tracks pump prices closely, with monthly changes correlating at 0.87 with the World Bank's Manila pump price over 2016–2025 and at 0.99 with PSA's gasoline-only index. The bottom-30% series join PSA's own back-calculated series for 2000–2011 and 2012–2017 to the current series. Because the long history exists only for the 17 regions defined before the Negros Island Region was created in 2024, we keep those regions and apply the new-code monthly changes for January–August 2026; the panel is balanced. Robustness checks use Dubai crude oil (World Bank) converted to pesos, the peso–dollar rate (BSP), the BSP policy rate (BIS) and the FAO Food Price Index. Poverty lines and incidence come from PSA. The online appendix lists every source with its link.

## 3.2 Local projections

For each horizon *h* = 0, …, 12 months, we estimate by ordinary least squares the local projection [@jorda_2005] specified by @kpodar_liu_2022:

$$\pi_{t+h} = \alpha_h + \beta_h f_t + \sum_{q=1}^{12} \gamma_{q}\, \pi_{t-q} + \sum_{q=1}^{12} \lambda_{q}\, f_{t-q} + \sum_{l=1}^{h-1} \rho_{l}\, f_{t+l} + \delta_h\, t + \varepsilon_{t+h} \qquad\qquad (3)$$

where $\pi$ is the monthly log change (× 100) of a price index, $f$ the fuel price shock and *t* a linear trend. The twelve lags absorb dynamics and the seasonality of the unadjusted data. The fuel leads $f_{t+1}, \dots, f_{t+h-1}$ remove the effect of later shocks that tend to follow a first one [@teulings_zubanov_2014]. $\beta_h$ is the response of inflation *h* months after a 1% fuel price rise; we report the cumulative response $B_h = \beta_0 + \dots + \beta_h$, the effect on the price level, estimated directly by summing the outcome from *t* to *t + h*. National estimates use Newey–West standard errors with *h* + 1 lags [@newey_west_1987]. The regional version stacks the 17 regions with region fixed effects, each region's own fuel index, and Driscoll–Kraay standard errors, which allow for correlation over time and across regions [@driscoll_kraay_1998]. Bands are 90%. Shock dates run from January 2001 to August 2026. The estimator recovers known responses in simulated data.

RQ1 uses all-income and bottom-30% inflation as outcomes. RQ2 uses $\Delta D_t$; a negative cumulative response is regressive. To separate the two terms of equation (2), we estimate equation (3) for each of the 13 CPI divisions and compute the gap that budget shares alone would produce, $\sum_k B^{(k)}_{12} (w^A_k - w^B_k)/100$, and compare division responses in the two baskets from 2013. The estimation plan was fixed before the first estimate; analyses added afterwards are labelled.

## 3.3 The 2026 episode

For RQ3 we re-estimate the cumulative responses on data ending in December 2025 and apply them to the actual 2026 fuel path: the fuel-driven change in the price level between December 2025 and month *m* is $\sum_{s} B_{m-s} f_s$. We compare this with the actual change, nationally and by region (using the panel estimates and each region's fuel path). The fuel-driven rise in the bottom-30% CPI, multiplied by the official monthly poverty line for a family of five (the 2023 regional threshold carried to December 2025), gives the peso cost. We also estimate the responses of household fuels, fares and cereals in both baskets (2013–2026), and decompose the actual December 2025–August 2026 change in each index by item using the 2018 weights.

# 4. Results

## 4.1 The descriptive record

Over 2001–2026, bottom-30% prices rose by 4.33% a year on average and all-income prices by 3.77% (Table 2, Figure 2). The poor's inflation was higher in 18 of 25 years and in 6 of 9 episodes in which fuel prices stayed at least 15% above their level a year earlier; the cumulative gap reached −13.3 log points by 2025 and was negative in every region. The gap was largest in 2008, when the oil spike coincided with the rice crisis (13.9% against 8.2%), and second largest in 2026. Price levels are non-stationary and monthly changes stationary (online appendix), supporting the model in changes.

Table: Table 2. Summary statistics of monthly changes (100 × Δln), national, January 2001–August 2026

| Variable | N | Mean (pp/month) | Annualised mean | SD | Min | Max |
|---|---|---|---|---|---|---|
| Fuel index (07.2.2) | 308 | 0.449 | 5.39 | 4.367 | −18.10 | 31.79 |
| CPI, all income | 308 | 0.314 | 3.77 | 0.386 | −0.59 | 2.60 |
| CPI, bottom 30% | 308 | 0.361 | 4.33 | 0.565 | −0.88 | 3.89 |
| Gap: ln(CPI all/CPI b30) | 308 | −0.047 | −0.56 | 0.303 | −2.27 | 0.71 |

![Figure 2. Inflation of all income and bottom-30% households, the gap between them, and the retail fuel index, 2001–2026 (year on year).](../output/figures/fig03_trends.png){width=95%}

## 4.2 Pass-through to the price level (RQ1)

A 1% rise in the retail fuel index raises the all-income price level by 0.044 percentage points within the month, 0.087 after six months and 0.102 after a year (Table 3, Figure 3); the bottom-30% level responds similarly (0.044, 0.095 and 0.102). The impact response equals the reference study's advanced-economy estimate (0.044) and is more than twice its developing-economy estimate (0.018); the six-month response is close to the developing-economy total (0.091). Motor fuel is 2.39% of the all-income basket, so the direct effect accounts for about 54% of the impact response; for the bottom 30% (fuel weight 1.59%) only about 36%. With Dubai crude in pesos as the shock, the twelve-month response is 0.041, about 40% of the retail estimate.

Table: Table 3. Cumulative responses to a 1% fuel price increase

| Horizon (months) | CPI, all income | CPI, bottom 30% | Gap, national | Gap, 17-region panel |
|---|---|---|---|---|
| 0 | 0.044*** (0.006) | 0.044*** (0.009) | −0.0000 (0.0040) | −0.0006 (0.0032) |
| 3 | 0.077*** (0.015) | 0.097*** (0.026) | −0.0185* (0.0110) | −0.0149** (0.0075) |
| 6 | 0.087*** (0.015) | 0.095*** (0.023) | −0.0155 (0.0103) | −0.0214** (0.0084) |
| 9 | 0.093*** (0.018) | 0.103*** (0.026) | −0.0137 (0.0101) | −0.0187** (0.0086) |
| 12 | 0.102*** (0.017) | 0.102*** (0.026) | −0.0097 (0.0113) | −0.0173** (0.0085) |

::: {custom-style="Table Note"}
*Notes:* Cumulative response (percentage points) of 100 × ln of each index. Gap = 100 × ln(CPI all/CPI bottom 30%); negative values mean bottom-30% prices rise more. National: Newey–West standard errors; panel: region fixed effects, Driscoll–Kraay standard errors; in parentheses. \* *p* < 0.10, \*\* *p* < 0.05, \*\*\* *p* < 0.01.
:::

![Figure 3. Cumulative pass-through of a 1% fuel price increase to the price level of each group (90% bands).](../output/figures/fig04_rq1_passthrough.png){width=80%}

## 4.3 Who pays more? (RQ2)

The cumulative response of the gap is negative at every horizon after the first month (Table 3, Figure 4). Nationally it is −0.0155 (standard error 0.0103) after six months and −0.0097 after twelve, significant at the 10% level at horizons 3, 4, 7, 8. In the regional panel it is −0.0214 (0.0084) after six months and −0.0173 (0.0085) after twelve, both significant. A 10% fuel price rise thus raises the poor's price level about 0.2 percentage points more than the average after six months, against a total rise of about 0.9%. The progressive hypothesis is rejected.

![Figure 4. Cumulative response of the gap 100 × ln(CPI all/CPI bottom 30%) to a 1% fuel price increase: (a) national; (b) 17-region panel (90% bands).](../output/figures/fig05_rq2_gap.png){width=95%}

Budget shares cannot explain this sign. Transport, whose prices respond most (0.370 after a year), is 9.0% of the all-income basket but 6.1% of the poor's. If both groups faced the same price changes within divisions, the twelve-month gap would be progressive (+0.0101; online appendix Table A1). The regressive gap must therefore come from the second term of equation (2). The bottom-30% division indices confirm it (Table 4): the poor's housing and utilities index rises 0.182 per 1% fuel price rise against 0.142 for all households, and their food index 0.067 against 0.055, while their transport index, mostly fares, rises less (0.196 against 0.300).

Table: Table 4. Response after 12 months of the same divisions in the two baskets, 2013–2026

| Division | All-income index | Bottom-30% index |
|---|---|---|
| 01 Food and non-alcoholic beverages | 0.055* (0.033) | 0.067* (0.037) |
| 04 Housing, water, electricity, gas | 0.142*** (0.017) | 0.182*** (0.038) |
| 07 Transport | 0.300*** (0.051) | 0.196** (0.078) |
| 11 Restaurants and accommodation | 0.044*** (0.016) | 0.040* (0.021) |

::: {custom-style="Table Note"}
*Notes:* Cumulative response per 1% fuel price increase; national; Newey–West standard errors in parentheses. Exploratory analysis added after the first results.
:::

## 4.4 Robustness

The sign survives the core checks (Table 5, Figure 5). With Dubai crude in pesos as the shock the six-month gap is −0.0093; excluding 2020 it is −0.0186; leaving out one region at a time keeps it between −0.0227 and −0.0203. Two results qualify it. With controls for the exchange rate, the policy rate and world food prices it falls to −0.0046, and splitting the panel gives −0.0541 (0.0197) over 2001–2012 but −0.0091 (0.0064) over 2013–2026. The regressive effect is robust in sign but concentrated in the 2000s, the decade of the 2008 rice crisis. Twelve further checks, and tests of whether the gap differs in poorer, more food-dependent, Mindanao or island regions (no difference survives a correction for multiple tests), are in the online appendix.

Table: Table 5. Robustness of the gap

| Specification | Gap, h = 6 | Gap, h = 12 |
|---|---|---|
| Baseline, national | −0.0155 (0.0103) | −0.0097 (0.0113) |
| Shock: Dubai crude in pesos (national) | −0.0093 (0.0056) | −0.0075 (0.0063) |
| Controls: exchange rate, policy rate, world food prices (national) | −0.0046 (0.0156) | 0.0086 (0.0160) |
| Excluding 2020 (national) | −0.0186 (0.0121) | −0.0142 (0.0129) |
| Baseline, 17-region panel | −0.0214** (0.0084) | −0.0173** (0.0085) |
| Panel, 2001–2012 | −0.0541*** (0.0197) | −0.0369** (0.0147) |
| Panel, 2013–2026 | −0.0091 (0.0064) | −0.0063 (0.0075) |
| Panel, leaving out one region at a time (range) | −0.0227 to −0.0203 | −0.0189 to −0.0156 |

![Figure 5. Robustness of the six-month gap (90% CI). Open squares: split of the panel sample, specified after the first results.](../output/figures/fig06_robustness.png){width=85%}

## 4.5 The 2026 oil shock (RQ3)

Estimated only on data to December 2025, the model attributes 2.55 log points (range 1.94 to 3.17) of the 4.81-point rise in the all-income CPI between December 2025 and August 2026 to fuel, and 3.13 (2.16 to 4.10) of the 5.98-point rise in the bottom-30% CPI: about half (Figure 6). It also predicts that the poor would pay more (−0.65 of the −1.18-point actual gap). Prices did not fall back when fuel eased in May–June, as the model predicted.

![Figure 6. Actual price changes in 2026 against the fuel-driven changes predicted by a model estimated on 2001–2025 data.](../output/figures/fig07_rq3_2026.png){width=95%}

For a family of five at the poverty line (about PHP 14,714 a month), the fuel-driven cost increase by August 2026 was about PHP 467 a month nationally, from PHP 390 in XII SOCCSKSARGEN to PHP 633 in the National Capital Region (Table 6); counting all price increases it was about PHP 907. Actual bottom-30% inflation was highest in XI Davao, BARMM, VI Western Visayas, XIII Caraga and IX Zamboanga Peninsula; fuel explains about 72% of the rise in Luzon's core regions but only 44% in Mindanao.

Table: Table 6. The 2026 shock by region, December 2025 to August 2026

| Region | Poverty 2018 (%) | Fuel price rise (%) | Fuel-driven rise, bottom-30% CPI | Actual rise, bottom-30% CPI | Fuel-driven extra cost (PHP/month) |
|---|---|---|---|---|---|
| National Capital Region | 2.2 | 34.5 | 3.68 [2.66, 4.70] | 3.47 | 633 |
| Cordillera (CAR) | 12.0 | 30.7 | 3.30 [2.41, 4.18] | 6.36 | 470 |
| I Ilocos | 9.9 | 36.3 | 3.68 [2.69, 4.68] | 3.82 | 571 |
| II Cagayan Valley | 16.3 | 34.1 | 3.47 [2.53, 4.42] | 4.64 | 503 |
| III Central Luzon | 7.0 | 33.9 | 3.50 [2.56, 4.45] | 6.00 | 605 |
| IV-A CALABARZON | 7.1 | 34.6 | 3.52 [2.57, 4.48] | 4.96 | 596 |
| MIMAROPA | 15.1 | 30.9 | 3.13 [2.26, 4.00] | 6.44 | 425 |
| V Bicol | 27.0 | 33.9 | 3.30 [2.37, 4.22] | 6.21 | 503 |
| VI Western Visayas† | 14.2 | 31.6 | 3.20 [2.31, 4.08] | 7.48 | 478 |
| VII Central Visayas† | 16.1 | 25.9 | 2.65 [1.94, 3.36] | 5.90 | 419 |
| VIII Eastern Visayas | 30.7 | 27.4 | 2.85 [2.07, 3.62] | 6.80 | 410 |
| IX Zamboanga Peninsula | 32.7 | 29.4 | 3.07 [2.23, 3.91] | 7.07 | 457 |
| X Northern Mindanao | 23.1 | 31.7 | 3.17 [2.28, 4.06] | 5.30 | 474 |
| XI Davao | 19.1 | 29.3 | 2.97 [2.14, 3.79] | 8.52 | 417 |
| XII SOCCSKSARGEN† | 27.3 | 29.6 | 3.00 [2.16, 3.84] | 6.10 | 390 |
| XIII Caraga | 30.5 | 31.1 | 3.11 [2.25, 3.96] | 7.10 | 409 |
| BARMM† | 60.4 | 33.5 | 3.30 [2.38, 4.21] | 7.88 | 444 |
| Philippines | 16.7 | 32.5 | 3.13 [2.16, 4.10] | 5.98 | 467 |

::: {custom-style="Table Note"}
*Notes:* 100 × log points. Fuel-driven rise from panel responses estimated to December 2025 (national model for the Philippines); indicative range in brackets. Extra cost for a family of five at the official poverty line. †Boundary changed in 2024.
:::

Between December 2025 and August 2026 the bottom-30% CPI rose 6.16% and the all-income CPI 4.92%, a gap of +1.24 points (Figure 7). Rice and other cereals contributed +1.67: their prices rose 18.3% in the poor's basket, where they weigh 19.6%, against 15.7% and 9.4% in the average basket. Fares added +0.15 and household fuels +0.13; private vehicle fuel (−0.38) and rent (−0.23) worked the other way. Historically, cereal prices barely respond to pump prices within a year (Table 7), so the 2026 rice increase likely reflects fertilizer and freight costs and import policy [@usda_fas_2026] as much as fuel; the data cannot separate these. LPG responds equally in both baskets and has equal budget shares (1.27% and 1.33%); kerosene responds strongly but is 0.27% of the poor's basket; charcoal and wood (4.02% of the poor's basket) do not respond.

![Figure 7. Contribution of each item group to the difference between bottom-30% and all-income price changes, December 2025–August 2026.](../output/figures/fig08_rq3_decomposition.png){width=85%}

Table: Table 7. Household fuels, fares and cereals: budget shares and responses after 12 months, 2013–2026

| Item | Weight, all (%) | Weight, bottom 30% (%) | Response, all-income index | Response, bottom-30% index |
|---|---|---|---|---|
| 04.5.2 Gas (LPG) | 1.27 | 1.33 | 0.730*** (0.152) | 0.722*** (0.148) |
| 04.5.3 Liquid fuels (kerosene) | 0.04 | 0.27 | 1.152*** (0.114) | 1.111*** (0.107) |
| 04.5.4 Solid fuels (charcoal, wood) | 0.87 | 4.02 | 0.013 (0.026) | 0.038 (0.024) |
| 07.3 Passenger transport (fares) | 4.54 | 3.72 | 0.071 (0.079) | 0.010 (0.101) |
| 01.1.1 Cereals and cereal products | 12.32 | 23.64 | 0.019 (0.084) | 0.012 (0.101) |

::: {custom-style="Table Note"}
*Notes:* Cumulative response per 1% fuel price increase, national, Newey–West standard errors in parentheses. \* *p* < 0.10, \*\* *p* < 0.05, \*\*\* *p* < 0.01.
:::

# 5. Discussion and policy implications

The cross-country finding that fuel shocks are progressive does not carry over to the Philippines. The reason is instructive: the poor's budget shares would make the shock progressive, but the prices they pay within food, utilities and fares rise more. Studies that rebuild income-group indices from survey budget shares with common prices cannot see this channel, so they may overstate how progressive fuel shocks are wherever the poor buy different items within categories.

For policy, three implications follow. First, fuel tax relief is poorly targeted, but not because the poor are spared. Relief on gasoline and diesel, which RA 12316 allows but the government did not use in 2026, would mainly benefit households that own vehicles; motor fuel is 2.39% of the average basket and 1.59% of the poor's. Relief on LPG is neutral between groups, and kerosene relief, though well aimed, is small: about PHP 37 per 11-kg LPG tank is roughly 8% of the fuel-driven monthly cost for a poverty-line family. Second, the channels that matter for the poor, food, especially rice, and fares, are reached by rice supply measures and fare policy, and by transport subsidies only if they are tied to fare restraint. Third, transfers can be sized and allocated by region with the bottom-30% CPI: on the 2026 evidence, PHP 467–907 a month for a poverty-line family of five, kept for at least a year because prices do not fall when fuel eases. For monetary policy, retail fuel prices, not crude prices, measure the inflationary impulse, which builds over at least a year.

The study has limitations. Retail fuel prices may partly respond to domestic conditions; crude oil gives the same sign, but a pure oil supply shock [@kilian_2009; @baumeister_hamilton_2019; @kanzig_2021] would strengthen the causal reading. The comparison is between the bottom 30% and all households, which understates rich–poor differences. Pre-2018 bottom-30% series are back-calculated. The regressive effect is concentrated in 2001–2012 and sensitive to macroeconomic controls. The 2026 analysis covers eight months, and its decomposition is descriptive. Price indices ignore substitution and income effects.

# 6. Conclusion

Fuel price shocks pass through quickly and lastingly to Philippine consumer prices, and their burden falls at least as heavily on poor households as on others, contrary to the cross-country evidence. The 2026 shock confirmed this pattern and added a large rice-price channel. Protecting the poor from oil shocks therefore calls for transfers sized to their own price index, attention to rice and fares, and restraint in broad fuel tax relief.

# Declarations {-}

**Data and code availability.** All data are public. The replication package (raw files with a source log, cleaned data in CSV, full code in Python and Stata 17, and a codebook) reproduces every number, table and figure; the online appendix lists every source with its link.

**Funding.** [To be completed.] **Conflict of interest.** [To be completed.] **Acknowledgements.** [To be completed.]

# References {-}

::: {#refs}
:::

# Online Appendix {-}

## A.1 Supplementary results

Table: Table A1. Response after 12 months by CPI division and the gap implied by budget shares alone

| COICOP division | Weight, all income (%) | Weight, bottom 30% (%) | Response after 12 months | Contribution to the gap if prices were the same |
|---|---|---|---|---|
| 07 Transport | 9.0 | 6.1 | 0.370*** (0.044) | +0.0108 |
| 12 Financial services | 0.0 | 0.0 | 0.358** (0.158) | +0.0001 |
| 04 Housing, water, electricity, gas | 21.4 | 15.5 | 0.158*** (0.015) | +0.0092 |
| 01 Food and non-alcoholic beverages | 37.7 | 54.9 | 0.072** (0.033) | −0.0124 |
| 11 Restaurants and accommodation | 9.6 | 7.5 | 0.063*** (0.018) | +0.0013 |
| 03 Clothing and footwear | 3.1 | 2.5 | 0.032*** (0.009) | +0.0002 |
| 05 Furnishings and household equipment | 3.2 | 2.4 | 0.031*** (0.010) | +0.0003 |
| 06 Health | 2.9 | 1.4 | 0.027** (0.013) | +0.0004 |
| 13 Personal care and miscellaneous | 4.5 | 4.8 | 0.025*** (0.009) | −0.0001 |
| 09 Recreation, sport and culture | 1.0 | 0.7 | 0.024 (0.025) | +0.0001 |
| 08 Information and communication | 3.4 | 1.0 | 0.019*** (0.007) | +0.0005 |
| 02 Alcoholic beverages and tobacco | 2.2 | 2.6 | 0.018 (0.055) | −0.0001 |
| 10 Education services | 2.0 | 0.4 | −0.009 (0.022) | −0.0001 |
| Total | 100.0 | 100.0 |  | +0.0101 |

::: {custom-style="Table Note"}
*Notes:* National; Newey–West standard errors in parentheses. Last column: response × (all-income share − bottom-30% share) ÷ 100; positive values push toward a progressive gap.
:::

Table: Table A2. The gap in groups of regions (17-region panel, Driscoll–Kraay standard errors)

| Group G | Other regions, h = 12 | Extra effect in G, h = 12 |
|---|---|---|
| High poverty (2018 incidence above the median) | −0.0131 (0.0100) | −0.0095 (0.0078) |
| High food share (above the median) | −0.0216** (0.0094) | 0.0100* (0.0052) |
| Mindanao | −0.0118 (0.0096) | −0.0166* (0.0092) |
| Island regions (MIMAROPA, VI, VII, VIII) | −0.0147* (0.0079) | −0.0123 (0.0086) |

![Figure A1. Extra effect on the gap after 12 months in groups of regions (90% CI). None survives a correction for testing four groups.](../output/figures/figA2_region_groups.png){width=80%}

Table: Table A3. Further robustness checks

| Specification | Gap, h = 6 | Gap, h = 12 | CPI all, h = 12 |
|---|---|---|---|
| 6 lags | −0.0160* (0.0093) | −0.0157 (0.0121) | 0.107*** (0.020) |
| 18 lags | −0.0191* (0.0106) | −0.0109 (0.0115) | 0.109*** (0.018) |
| Shock dates to Dec 2025 only | −0.0158 (0.0097) | −0.0097 (0.0113) | 0.102*** (0.017) |
| Dummies for the base-change months (Jan 2012, Jan 2018) | −0.0155 (0.0102) | −0.0100 (0.0114) | 0.102*** (0.018) |
| Reference study's window (to Jun 2019) | −0.0315 (0.0202) | −0.0215 (0.0191) | 0.093*** (0.016) |
| Shock: gasoline index, 2019–2026 | −0.0016 (0.0122) | −0.0051 (0.0125) | 0.096*** (0.027) |
| Shock: World Bank pump price, 2018–2025 | −0.0063 (0.0096) | −0.0005 (0.0054) | 0.072*** (0.019) |
| National, excluding 2008 | −0.0131 (0.0088) | −0.0079 (0.0115) | — |
| National, 2013–2026 | −0.0046 (0.0095) | 0.0031 (0.0092) | — |
| Panel, excluding 2008 | −0.0177** (0.0073) | −0.0135 (0.0092) | — |
| Panel, dropping the re-mapped 2026 months | −0.0215*** (0.0083) | −0.0173** (0.0085) | — |
| Panel, national instead of regional fuel index | −0.0225** (0.0095) | −0.0188** (0.0095) | — |
| Asymmetry: extra effect of fuel increases (CPI all, h = 12) |  |  | 0.079 (0.079) |

![Figure A2. Further robustness checks of the six-month gap (90% CI).](../output/figures/figA3_robustness_other.png){width=85%}

Table: Table A4. Annual inflation by group and fuel price change, 2001–2026

| Year | Inflation, all income (%) | Inflation, bottom 30% (%) | Gap, b30 − all (pp) | Fuel index (% y/y) |
|---|---|---|---|---|
| 2001 | 5.41 | 5.39 | −0.02 | 11.8 |
| 2002 | 2.73 | 2.98 | +0.25 | 0.1 |
| 2003 | 2.25 | 2.40 | +0.15 | 10.9 |
| 2004 | 4.80 | 5.93 | +1.13 | 15.8 |
| 2005 | 6.61 | 7.91 | +1.30 | 23.4 |
| 2006 | 5.48 | 6.62 | +1.14 | 19.0 |
| 2007 | 2.94 | 3.26 | +0.32 | 1.4 |
| 2008 | 8.17 | 13.91 | +5.74 | 20.9 |
| 2009 | 4.26 | 5.38 | +1.12 | −15.9 |
| 2010 | 3.79 | 3.61 | −0.17 | 12.9 |
| 2011 | 4.72 | 5.13 | +0.41 | 11.9 |
| 2012 | 3.17 | 2.82 | −0.36 | 2.1 |
| 2013 | 2.58 | 3.05 | +0.46 | −1.4 |
| 2014 | 3.60 | 4.68 | +1.08 | −0.4 |
| 2015 | 0.68 | 1.32 | +0.64 | −24.3 |
| 2016 | 1.25 | 1.11 | −0.14 | −7.3 |
| 2017 | 2.85 | 2.30 | −0.55 | 14.0 |
| 2018 | 5.23 | 5.99 | +0.76 | 23.2 |
| 2019 | 2.41 | 1.91 | −0.50 | −1.0 |
| 2020 | 2.39 | 2.59 | +0.20 | −11.2 |
| 2021 | 3.93 | 4.22 | +0.29 | 20.8 |
| 2022 | 5.81 | 6.56 | +0.75 | 39.7 |
| 2023 | 6.01 | 6.77 | +0.76 | −9.1 |
| 2024 | 3.22 | 4.18 | +0.97 | −3.0 |
| 2025 | 1.66 | 0.29 | −1.37 | −4.3 |
| 2026* | 5.16 | 6.20 | +1.04 | 33.8 |

Table: Table A5. Fuel-shock episodes

| Episode | Months | Peak fuel rise (% y/y) | Inflation, all (%) | Inflation, b30 (%) | Gap (pp) |
|---|---|---|---|---|---|
| 2001-01 to 2001-03 | 3 | 22.8 | 5.83 | 5.90 | +0.07 |
| 2004-06 to 2006-09 | 28 | 28.3 | 6.21 | 7.53 | +1.32 |
| 2008-02 to 2008-10 | 9 | 40.3 | 8.50 | 14.68 | +6.17 |
| 2010-01 to 2010-05 | 5 | 23.5 | 3.92 | 3.88 | −0.04 |
| 2017-01 to 2017-03 | 3 | 24.6 | 2.88 | 2.12 | −0.76 |
| 2017-09 to 2017-11 | 3 | 15.9 | 3.06 | 2.61 | −0.44 |
| 2018-02 to 2018-11 | 10 | 33.5 | 5.42 | 6.22 | +0.81 |
| 2021-04 to 2022-12 | 21 | 62.7 | 4.99 | 5.52 | +0.53 |
| 2026-03 to 2026-08 | 6 | 76.3 | 6.14 | 7.58 | +1.44 |

Table: Table A6. Augmented Dickey–Fuller tests, 2001–2026

| Series | Form | ADF statistic | p-value | Lags | N |
|---|---|---|---|---|---|
| ln fuel index | level | −2.22 | 0.480 | 2 | 305 |
| ln fuel index | first difference | −13.47 | 0.000 | 1 | 305 |
| ln CPI all | level | −1.62 | 0.786 | 1 | 306 |
| ln CPI all | first difference | −12.12 | 0.000 | 0 | 306 |
| ln CPI b30 | level | −1.91 | 0.649 | 1 | 306 |
| ln CPI b30 | first difference | −9.59 | 0.000 | 0 | 306 |
| ln(CPI all/CPI b30) | level | −1.66 | 0.770 | 4 | 303 |
| ln(CPI all/CPI b30) | first difference | −9.08 | 0.000 | 3 | 303 |

## A.2 Data appendix

The replication package is the repository <https://github.com/liancataytayjk-coder/oil-shock-distribution>. The command `./run_all.sh` (Python 3.11) or `code/stata/00_master.do` (Stata 17) rebuilds everything from the raw files; `codebook/codebook.xlsx` documents every raw and cleaned variable. All files were downloaded on 4 October 2026.

**S1. CPI for All Income Households, 2018 = 100, old geographic code (17 regions).** Philippine Statistics Authority (PSA), OpenSTAT. Used for: All-income CPI, its divisions and sub-indices, and the fuel index 07.2.2 (Jan 1994-Dec 2025); 2018 basket weights. Coverage: Jan 1994-Dec 2025; Philippines and 17 regions. Files: `psa/cpi_all_2018old_backcast_1994_2017.csv`, `psa/cpi_all_2018old_2018_2025.csv`, `psa/cpi_all_2018old_weights.csv`. Link: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP15.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP09.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018/0012M4ACP12.px>

**S2. CPI for All Income Households, 2018 = 100, new geographic code (Negros Island Region separate).** PSA, OpenSTAT. Used for: Jan-Aug 2026 months (chained onto S1); gasoline index 07.2.2.2; 2018 weights for the 2026 decomposition. Coverage: Jan 2018-Aug 2026; Philippines, 17 regions and NIR. Files: `psa/cpi_all_2018new_2018_2026.csv`, `psa/cpi_all_2018new_weights.csv`. Link: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018NEW/0012M4ACP22.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/CPI/2018NEW/0012M4ACP25.px>

**S3. CPI for the Bottom 30% Income Households, 2018 = 100, old geographic code.** PSA, OpenSTAT. Used for: Bottom-30% CPI (all items from 2000; divisions and sub-indices from 2012); 2018 basket weights. Coverage: Jan 2000-Dec 2025; Philippines and 17 regions. Files: `psa/cpi_b30_2018old_backcast_allitems_2000_2011.csv`, `psa/cpi_b30_2018old_backcast_2012_2017.csv`, `psa/cpi_b30_2018old_2018_2025.csv`, `psa/cpi_b30_2018old_weights.csv`. Link: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT5.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT4.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT1.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018/0022M4ABOT3.px>

**S4. CPI for the Bottom 30% Income Households, 2018 = 100, new geographic code.** PSA, OpenSTAT. Used for: Jan-Aug 2026 months (chained onto S3); 2018 weights for the 2026 decomposition. Coverage: Jan 2018-Aug 2026; Philippines, 17 regions and NIR. Files: `psa/cpi_b30_2018new_2018_2026.csv`, `psa/cpi_b30_2018new_weights.csv`. Link: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018NEW/0022M4ABIR1.px>; <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/BIH/2018NEW/0022M4ABIR3.px>

**S5. Official poverty statistics by region: poverty incidence among population and annual per-capita poverty threshold.** PSA, OpenSTAT. Used for: Region groups (poverty 2018); poverty line for the peso cost (threshold 2023). Coverage: 2018, 2021, 2023; Philippines, regions and provinces. Files: `psa/poverty_population_2018_2023.csv`. Link: <https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/1F/FY/0031F3DF020.px>

**S6. Commodity Price Data (Pink Sheet), monthly.** World Bank. Used for: Dubai crude oil price, USD/barrel (robustness shock, with S8). Coverage: Jan 1960-Sep 2026. Files: `wb/CMO-Historical-Data-Monthly.xlsx`, `extracts/wb_cmo_crude_monthly.csv`. Link: <https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx>

**S7. Global Fuel Prices Database (April 2025 version).** World Bank. Used for: Manila regular gasoline (RON 91) pump price, PHP/litre: check of the fuel index; appendix robustness. Coverage: Philippines: Jan 2017-Mar 2025. Files: `wb/Global_Fuel_Prices_Database.xlsx`, `wb/Global_Fuel_Prices_Database_methodology.pdf`, `extracts/wb_gfpd_phl_gasoline.csv`. Link: <https://datacatalogfiles.worldbank.org/ddh-published/0066829/DR0095290/Global_Fuel_Prices_Database.xlsx>

**S8. Peso per US dollar exchange rate, monthly average.** Bangko Sentral ng Pilipinas (BSP). Used for: Converts Dubai crude to pesos; control variable (robustness). Coverage: Jan 1945-Sep 2026. Files: `bsp/pesodollar.xlsx`, `extracts/bsp_php_usd_monthly.csv`. Link: <https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx>

**S9. Central bank policy rates, Philippines.** Bank for International Settlements (BIS). Used for: BSP policy rate, end of month (control variable, robustness). Coverage: Jan 1986-Aug 2026. Files: `bis/bis_cbpol_ph_monthly.csv`. Link: <https://stats.bis.org/api/v1/data/WS_CBPOL/M.PH?format=csv>

**S10. FAO Food Price Index, nominal, 2014-2016 = 100.** Food and Agriculture Organization (FAO). Used for: World food prices (control variable, robustness). Coverage: Jan 1990-Sep 2026. Files: `fao/food_price_indices_data.csv`. Link: <https://www.fao.org/media/docs/worldfoodsituationlibraries/wfs-library/food_price_indices_data.csv>

**S11. 2026 policy facts (RA 12316, executive orders, subsidies, fares, policy rate).** Republic of the Philippines; news and official releases. Used for: Policy assessment (RQ3); each fact listed with its link and verification status. Coverage: Mar-Sep 2026. Files: `paper/policy_context_2026.md`. Link: <https://lawphil.net/statutes/repacts/ra2026/ra_12316_2026.html>

**S12. Published coefficients of the reference study (Annex Tables 1-2, Figure 7).** Kpodar and Liu (2021), IMF Working Paper WP/21/271. Used for: Comparison of the Philippine pass-through with the reference study's estimates. Coverage: Advanced and developing economies, 2000-2019. Files: `reference/kpodar_liu_2021_targets.csv`. Link: <https://www.imf.org/en/publications/wp/issues/2021/11/12/the-distributional-implications-of-the-impact-of-fuel-price-increases-on-inflation-506822>

Table: Table A7. Sources, scripts and output files

| Item | Content | Sources | Python script | Stata do-file |
|---|---|---|---|---|
| Figure 1 | Conceptual framework (X to Y) | - | 06_figures.py | - |
| Table 2 | Summary statistics of monthly changes by period | S1-S4 | 03_descriptive.py | 03_descriptive.do |
| Table A4 | Annual inflation of both groups, the gap and fuel | S1-S4 | 03_descriptive.py | 03_descriptive.do |
| Figure 2 | Year-on-year inflation, gap and fuel, 2001-2026 | S1-S4 | 03_descriptive.py, 06_figures.py | 03_descriptive.do |
| Table A5 | Fuel-shock episodes | S1-S4 | 03_descriptive.py | 03_descriptive.do |
| Table A6 | Unit-root tests | S1-S4 | 03_descriptive.py | 03_descriptive.do |
| Table 3 | Pass-through to the price level, both groups | S1-S4 | 04_estimate.py | 04_estimate.do |
| Figure 3 | RQ1 cumulative responses | S1-S4 | 04_estimate.py, 06_figures.py | 04_estimate.do |
| Table 3 | Gap response, national and 17-region panel | S1-S4 | 04_estimate.py | 04_estimate.do |
| Figure 4 | RQ2 cumulative responses | S1-S4 | 04_estimate.py, 06_figures.py | 04_estimate.do |
| Table A1 | RQ2 why: division responses x weight differences | S1, S3 | 04_estimate.py | 04_estimate.do |
| Table 4 | Divisions in both baskets, 2013-2026 (exploratory) | S1, S3 | 04_estimate.py | 04_estimate.do |
| Table 5 | Core robustness checks | S1-S10 | 04_estimate.py | 04_estimate.do |
| Figure 5 | Core robustness of the six-month gap | S1-S10 | 04_estimate.py, 06_figures.py | 04_estimate.do |
| Figure 6 | 2026: actual vs fuel-driven change | S1-S4 | 05_policy_2026.py, 06_figures.py | 05_policy_2026.do |
| Table 6 | 2026 by region; peso cost for a poverty-line family | S1-S5 | 05_policy_2026.py | 05_policy_2026.do |
| Table 7 | LPG, kerosene, solid fuels, fares, cereals: both baskets | S1, S3 | 05_policy_2026.py | 05_policy_2026.do |
| Figure 7 | Item contributions to the 2026 gap | S2, S4 | 05_policy_2026.py, 06_figures.py | 05_policy_2026.do |
| Tables A2–A3 | Region-group interactions; other robustness checks | S1-S10 | 04_estimate.py | 04_estimate.do |
| Figure A1 | Region-group interactions | S1-S5 | 04_estimate.py, 06_figures.py | 04_estimate.do |
| Figure A2 | Other robustness checks | S1-S10 | 04_estimate.py, 06_figures.py | 04_estimate.do |
