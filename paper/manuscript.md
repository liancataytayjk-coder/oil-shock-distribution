---
title: "Who Pays for Oil Shocks? Fuel Prices, Rice, and the Inflation of Poor Households across Philippine Regions, 2001–2026"
author:
  - "[Author name], Graduate School of Applied Economics, University of Southeastern Philippines, Davao City, Philippines. Corresponding author: [email]"
date: "Manuscript draft, October 2026"
abstract: |
  We estimate how retail fuel price shocks pass through to the consumer prices faced by the poorest 30% of Philippine households and by all households, nationally and in 17 regions, from 2001 to August 2026. We replicate the local projection design of Kpodar and Liu (2022), first reproducing their EU benchmark (impact pass-through 0.057 against their 0.055), and then apply it to the Philippine Statistics Authority's official bottom-30% and all-income consumer price indices. A 1% rise in retail fuel prices raises the price level by 0.044 percentage points (pp) within the month and by 0.102 pp after a year; world crude prices capture only about 40% of this. Unlike the cross-country evidence, the shock is not progressive in the Philippines: in the regional panel, prices for the bottom 30% rise 0.0214 pp more per 1% fuel increase after six months, although the gap is concentrated in 2001–2012 and is not robust to all controls. A model estimated only on data up to 2025 predicts about half of the 2026 price surge. In accounting terms, most of the poor's excess inflation in 2026 came from rice, whose link to the oil shock (through fertilizer and freight) the data cannot isolate. Fuel excise relief is a weak instrument for protecting the poor; income transfers sized to their price index are better targeted.
keywords: "oil price shocks; inflation inequality; fuel prices; local projections; Philippines; rice"
bibliography: references.bib
link-citations: true
---

**Keywords:** oil price shocks; inflation inequality; fuel price pass-through; local projections; regional inflation; rice; Philippines

**JEL classification:** E31, Q41, I32, D31, R12

# 1. Introduction

## 1.1 Motivation

In March 2026 the conflict in the Middle East produced one of the sharpest oil shocks the Philippines has experienced. Retail prices of motor fuels in the consumer price index (CPI) rose 36% year on year in March and 76% in April. Headline inflation, which had been 2.4% in February, reached 4.1% in March and 7.2% in April 2026, and was still 6.2% in August. Inflation measured with the official CPI for the bottom 30% income households rose further, to 8.5% in April and 8.2% in August, 1.2 and 2.1 percentage points above the all-income rate (PSA OpenSTAT, authors' calculations). The country imports almost all of its petroleum, and the government responded on several fronts: a new law allowing the President to suspend fuel excise taxes when Dubai crude averages USD 80 per barrel or more [@ra12316_2026]; the suspension of excise taxes on liquefied petroleum gas (LPG) and kerosene from April 2026, renewed in September; fuel subsidies for public utility vehicle drivers; and three increases in the policy rate between March and August 2026, from 4.25% to 5.00%.

Each of these responses rests on an implicit answer to a question this paper addresses directly: when fuel prices rise, who pays? A large cross-country literature finds that fuel price increases raise inflation, more persistently in developing than in advanced economies [@choi_etal_2018; @gelos_ustyugova_2017; @kpodar_abdallah_2017]. The closest study, @kpodar_liu_2022, combines retail fuel prices for 122 countries with quintile-specific CPIs built from household surveys, and concludes that fuel price shocks are *progressive*: prices for the richest quintile rise more than for the poorest, because richer households spend more on transport. If that holds in the Philippines, broad fuel tax cuts would mainly benefit better-off households, and the case for targeted relief would rest on the level of the poor's losses rather than on their relative burden. If it does not, the design of relief changes.

## 1.2 This paper

We test the cross-country finding within one country, using official price indices rather than reconstructed ones, and we ask whether the answer depends on where households live. The Philippine Statistics Authority (PSA) publishes a CPI for the bottom 30% income households alongside the all-income CPI, monthly, for the country and every region, with commodity detail on a common 2018 base. Together with a regional retail fuel index from the same source, these data allow a direct estimate of the gap between the price changes faced by the poor and by the average household after a fuel shock, over 2001–2026 and across 17 regions.

We ask four questions. How much, and for how long, does a fuel price increase raise Philippine consumer prices (RQ1)? Is the burden larger for the bottom 30% than for all households (RQ2)? Through which goods does it travel (RQ3)? Is the gap wider in poorer, more food-dependent, Mindanao or island regions (RQ4)? We then use the 2026 episode as an out-of-sample test: a model estimated only on data up to December 2025 is asked to predict the 2026 price surge, nationally and by region, and the remaining gap is decomposed by item.

We keep the estimator of @kpodar_liu_2022 unchanged — panel local projections [@jorda_2005] with the correction of @teulings_zubanov_2014 — and validate our implementation before using it: on EU data, our estimates reproduce their benchmark that retail fuel prices pass through to inflation about three times as strongly as crude oil prices.

## 1.3 Related literature and contribution

The paper sits between two literatures. The first measures the pass-through of oil and fuel prices to inflation, mostly with crude oil prices [@blanchard_gali_2010; @choi_etal_2018; @gelos_ustyugova_2017] and more recently with retail prices [@kpodar_abdallah_2017; @kpodar_imam_2021]. For the Philippines, @allon_pineda_etal_2026 estimate second-round and asymmetric effects of oil and food price shocks on national inflation, and @valera_etal_2025 document the changing effects of energy and rice prices on overall inflation. Neither distinguishes income groups or regions. The second literature studies who bears the cost of fuel price changes, mostly through partial or general equilibrium simulations of subsidy reform [@coady_etal_2015; @dorband_etal_2019; @siddig_etal_2014; @soile_mu_2015], and, more broadly, how inflation differs across households [@easterly_fischer_2001; @kaplan_schulhofer_2017; @jaravel_2021].

In the *Asian Economic Journal*, a long line of work examines who bears the cost of shocks and policies in Asia — rice subsidies and their targeting [@satriawan_shrestha_2018], food price instability [@timmer_dawe_2007], and the evolution of poverty and inequality [@warr_etal_2018; @wihardja_pradana_2024] — and a growing body uses subnational data [@kurita_kurosaki_2011; @pagaduan_2022; @kataoka_2022]. Work on price transmission in the region has focused on the exchange rate and monetary policy [@taguchi_sohn_2014; @armas_2021].

We contribute in three ways. First, we provide a within-country test of the cross-country progressivity result, using the statistical agency's own income-group CPIs, and find that it does not hold in the Philippines: the sign of the distributional effect is reversed. Second, we show that the reason is not the expenditure weights the cross-country approach relies on — those predict a progressive effect here too — but differences in the price changes the two groups face *within* the same categories. Third, we bring the 2026 shock into the analysis: we test the historical model out of sample, quantify the fuel-driven cost for a poverty-line family by region, and show that rice, not fuel, accounted for most of the poor's excess inflation in 2026.

# 2. Methods

## 2.1 Data

Table 1 lists the series. Prices come from PSA OpenSTAT [@psa_openstat_2026]. The CPI for all income households and the CPI for the bottom 30% income households are published monthly, 2018 = 100, for the Philippines and each region. The bottom-30% index prices the basket of households in the lowest 30% of the income distribution, with weights from the 2018 Family Income and Expenditure Survey. PSA publishes backcasts of both indices on the 2018 base: all-income from January 1994 with full commodity detail, and bottom-30% from January 2000 for all items and from January 2012 by commodity. We splice the backcasts to the current series without re-basing; the joins in January 2012 and January 2018 are examined below.

Regions follow the geographic code used in PSA's backcasts: 17 regions, with Negros Occidental and Negros Oriental in Regions VI and VII. The Negros Island Region, created in 2024, is published separately only on the new geographic code. For January–August 2026, which PSA publishes only on the new code, we chain each region's new-code monthly changes onto the old-code level; for the four regions whose boundaries changed (VI, VII, XII and BARMM) these months are flagged and dropped in a robustness check. The sample for estimation runs from January 2001 to August 2026 (308 months).

*The fuel price shock.* The reference study uses retail gasoline prices from the Global Monthly Retail Fuel Price Database, which is not publicly available. We use the PSA sub-index 07.2.2, "fuels and lubricants for personal transport equipment" (mainly gasoline and diesel at the pump), available for every region from 1994. Its monthly changes correlate at 0.87 with the World Bank's Manila RON 91 pump price over 2016–2025 [@worldbank_gfpd_2025] and at 0.99 with PSA's gasoline-only index, available from 2018. Both serve as alternative shocks, as does the Dubai crude price in pesos [@worldbank_cmo_2026].

*Other data.* The peso–dollar rate (BSP), the BSP policy rate (as compiled by the BIS) and the FAO Food Price Index enter as controls. Official 2018 poverty incidence by region and the 2023 poverty thresholds come from PSA. For the validation exercise we use Eurostat's harmonised CPI and the European Commission's Weekly Oil Bulletin, which reports pump prices with and without taxes [@ec_wob_2026].

## 2.2 Specification

We estimate the reference study's equation, for horizon *h* = 0, …, 12:

$$
\Delta \ln y_{t+h} = \alpha_h + \sum_{q=1}^{12} \gamma_{1q}\, \Delta \ln y_{t-q} + \sum_{q=1}^{12} \gamma_{2q}\, \Delta \ln F_{t-q} + \beta_h\, \Delta \ln F_{t} + \sum_{l=1}^{h-1} \gamma_{3l}\, \Delta \ln F_{t+l} + \delta_h\, t + \varepsilon_{t+h}
$$

where *F* is the retail fuel index, *y* is the outcome and *t* is a linear trend. The third sum is the Teulings–Zubanov correction, which conditions on fuel price changes between *t* and *t + h*; following the reference study's Annex Tables, it includes leads 1 to *h* − 1. Both variables are 100 × log changes, so β_h is the percentage-point change in month *t + h* inflation per 1% change in fuel prices. The outcome is the one-month change at *t + h*, as in the reference study; we report the cumulative response, the effect on the price level after *h* months, by replacing the outcome with Σ_{j=0}^{h} Δ ln y_{t+j}. Data are not seasonally adjusted; the twelve lags absorb seasonality.

National models use Newey–West standard errors with *h* + 1 lags [@newey_west_1987]. The regional panel adds region fixed effects and uses Driscoll–Kraay errors [@driscoll_kraay_1998], which allow for the cross-regional correlation created by common national shocks. Bands are 90%, as in the reference study.

*Outcomes.* RQ1 uses ln CPI for all households and for the bottom 30%. RQ2 uses the log ratio D_t = ln(CPI^all_t / CPI^b30_t). A positive cumulative response means the average household's prices rise more (progressive, the cross-country finding); a negative response means the poor's prices rise more (regressive). Because the all-income index includes the bottom 30%, this contrast is milder than the richest-to-poorest quintile ratio in @kpodar_liu_2022. RQ3 uses the 13 COICOP divisions of the all-income CPI and, from 2013, the matching bottom-30% divisions. RQ4 estimates the regional panel for D_{r,t} on each region's own fuel index, and then adds an interaction of the shock with a time-invariant group dummy *G_r*, one group at a time: high poverty (2018 poverty incidence above the median; range 2.2–60.4%), high food share (food share of the regional basket above the median; range 29.5–59.4%), Mindanao, and island regions.

## 2.3 The 2026 episode

To test the model out of sample, we re-estimate the cumulative responses on data ending in December 2025 and combine them with the observed 2026 fuel path. The fuel-driven change in the price level between December 2025 and month *m* is

$$
\widehat{\Delta P}_m = \sum_{s=\text{Jan 2026}}^{m} \hat{\beta}^{\,cum}_{m-s}\, \Delta \ln F_s ,
$$

which we compare with the actual change. Regionally, we apply the pooled panel responses to each region's own fuel path. The fuel-driven rise in the bottom-30% CPI is converted into pesos for a family of five living at the official poverty line: PSA's 2023 regional per-capita poverty threshold × 5 / 12, carried to December 2025 with the regional bottom-30% CPI. Finally, we decompose the actual December 2025–August 2026 change in each index into item contributions, using the fixed 2018 weights of each basket. This decomposition is descriptive and involves no model.

## 2.4 Validation and pre-specification

Before estimating anything for the Philippines, we required our implementation to reproduce the reference study on comparable data, under criteria written down in advance. Using EU countries, monthly harmonised CPIs and Weekly Oil Bulletin pump prices for 2005–June 2019, our impact response of inflation to after-tax gasoline prices is 0.057, against 0.055 in @kpodar_liu_2022 (their Figure 7); to before-tax prices with a tax control, 0.024 (theirs 0.020); and to Brent crude in euro, 0.014 (theirs 0.015). As in the reference study, responses are close to zero from the second month. Using the EU fuels-and-lubricants index instead, the impact response is 0.065 and falls to 0.026 in the next month. The estimator also recovers known impulse responses from simulated panels in unit tests.

The national, regional and robustness specifications in Section 3 were recorded in the project's decision log before any Philippine estimate was produced. Analyses added after the first results — the comparison of bottom-30% and all-income components, the sub-period splits and the 2026 episode — are labelled as supplementary throughout. All data, code and the log are available in the replication package.

# 3. Results

## 3.1 Pass-through to the price level (RQ1)

Fuel prices pass through quickly and lastingly to Philippine consumer prices (Figure 1, Table 2). A 1% rise in the retail fuel index raises the all-income CPI by 0.044 pp within the month (s.e. 0.006), 0.087 pp after six months and 0.102 pp (s.e. 0.017) after a year. A 10% fuel price increase therefore adds about 0.44 pp to the price level on impact and about 1.0 pp within twelve months, and the cumulative response is still rising at the end of the window.

The profile combines features of the two groups in @kpodar_liu_2022. The impact response matches their advanced-economy estimate (0.044) rather than their developing-economy estimate (0.018), while the cumulative response over six months, 0.087, is close to the sum of their developing-economy responses (0.091) and well above the advanced-economy sum (0.060). Motor fuel has a weight of 2.39% in the all-income basket, so the direct effect accounts for roughly 54% of the impact response; the remainder reflects indirect effects within the month. For the bottom 30%, whose basket gives motor fuel a weight of only 1.59%, the direct effect explains only about 36% of an impact response of the same size (0.044).

World crude prices understate the pass-through, as the reference study found for the EU. With Dubai crude in pesos as the shock, the cumulative response after a year is 0.041, about 40% of the retail estimate. Retail fuel prices embed taxes, margins and the exchange rate, all of which move with the shock and reach consumers.

## 3.2 Who pays more? (RQ2)

The cross-country finding of progressivity does not carry over. In the national series the cumulative response of D = ln(CPI^all/CPI^b30) is negative at every horizon after the impact month: −0.0185 after three months, −0.0155 (s.e. 0.0103) after six and −0.0097 after twelve (Figure 2, Table 2). It is significant at the 10% level at horizons 3, 4, 7, 8. The regional panel, which uses 17 regions' own fuel prices, gives a sharper estimate: −0.0214 (s.e. 0.0084) after six months and −0.0173 (s.e. 0.0085) after twelve, both significant. Dropping any one region leaves the six-month estimate between −0.0227 and −0.0203.

The magnitude is modest. After six months, a 10% fuel price increase raises the bottom-30% price level about 0.2 pp more than the all-income level (panel estimate), against a total increase of about 0.9 pp. The two groups' cumulative responses are close (0.095 and 0.087 after six months; both 0.102 after a year), but the bottom-30% response builds faster.

## 3.3 Channels (RQ3)

Ten of the thirteen all-income CPI divisions rise significantly after a fuel shock (Table 4, Figure 3), the same breadth as the reference study found in developing economies (10 of 12). The largest cumulative responses after a year are in transport (0.370), housing, water, electricity and gas (0.158), food (0.072) and restaurants (0.063); education does not respond.

These responses, combined with the two baskets' weights, do not explain the regressive gap. The bottom-30% basket gives food a weight of 54.9% against 37.7%, but transport, which responds most, a weight of 6.1% against 9.0%. If both groups faced the same price change within each division, the weights would predict a *progressive* cumulative gap of +0.0101 after a year — the cross-country result. The direct estimate has the opposite sign, so the poor must face larger increases within divisions.

The bottom-30% component indices, available from 2013, show where (supplementary analysis). After a year, the bottom-30% housing, water, electricity and gas index rises 0.182 per 1% fuel increase against 0.142 for all households, and its food index 0.067 against 0.055, while its transport index rises less (0.196 against 0.300), because it is dominated by fares rather than motor fuel. At the item level (Table 7), LPG prices respond almost identically in the two baskets (0.730 and 0.722), and the two groups give LPG almost the same budget share (1.27% and 1.33%). Kerosene responds strongly (1.111), but has a weight of only 0.27% even for the poor. Solid fuels — charcoal and wood — take 4.02% of the poor's budget against 0.87% of the average, but barely respond to fuel prices (0.038). Passenger fares in the bottom-30% basket have historically responded little (0.010, against 0.071 for all households), consistent with regulated jeepney fares that adjust infrequently.

## 3.4 Regional differences (RQ4)

The regional estimates point in the direction of the hypotheses but are imprecise (Table 5, Figure 4). After a year, per 1% fuel increase, the gap is 0.0166 pp larger in Mindanao (s.e. 0.0092), 0.0123 pp larger in the island regions (s.e. 0.0086) and 0.0095 pp larger in high-poverty regions (s.e. 0.0078). Regions where food takes a larger share of the basket show a *smaller* gap (0.0100, s.e. 0.0052), opposite to the hypothesis. The Mindanao and food-share interactions are significant at the 10% level, but with four groups tested none survives a Bonferroni correction. We read the regional evidence as suggestive, not conclusive.

## 3.5 Robustness and stability

Table 3 and Figure 5 report the pre-specified checks for the six-month gap. The negative sign holds in all of them, and most estimates are within one standard error of the baseline: Dubai crude as the shock, 6 or 18 lags, excluding 2020 or 2026, dummies for the January 2012 and January 2018 base changes, the reference study's sample window, and, in the panel, dropping the re-mapped 2026 observations or replacing regional fuel prices with the national index. Three checks shrink the gap toward zero: adding the exchange rate, policy rate and world food prices as controls (−0.0046, s.e. 0.0156), and the two alternative fuel series available only from 2018–2019, the gasoline index (−0.0016) and the World Bank pump price (−0.0063).

The short-sample checks reflect a genuine change over time. In the regional panel, the six-month gap is −0.0541 (s.e. 0.0197) over 2001–2012 and −0.0091 (s.e. 0.0064) over 2013–2026 (supplementary analysis). Excluding 2008, the year of the global rice price crisis, leaves a significant panel estimate of −0.0177 (s.e. 0.0073). The regressive effect of fuel shocks was therefore strongest in the 2000s and has weakened, though not reversed, since. For the price level, pass-through is somewhat larger for fuel price increases than decreases (an additional 0.079 after a year, s.e. 0.079), but the difference is not significant.

## 3.6 The 2026 shock

The fuel index rose 53.7% (log points) between December 2025 and April 2026 and was still 32.5% higher in August. Figure 6 compares the actual change in each price index with the fuel-driven change implied by a model estimated only on data up to December 2025.

The historical relationships hold, but explain about half of the surge. By August 2026, the model attributes 2.55 log points (indicative range 1.94 to 3.17) of the 4.81-point rise in the all-income CPI to fuel, about 53%. For the bottom-30% CPI the fuel-driven rise is 3.13 (2.16 to 4.10) out of an actual 5.98, about 52%. The model also predicts the sign of the distributional gap: it attributes −0.65 pp of the −1.18 pp actual gap to fuel. Prices did not fall back when fuel prices eased in May and June, as the model predicts they would; this is consistent with the asymmetry noted above and with the other shocks of 2026, including a 5.1% depreciation of the peso between February and August.

Item contributions show where the rest of the poor's excess inflation came from (Figure 7). Between December 2025 and August 2026, the bottom-30% CPI rose 6.16% and the all-income CPI 4.92%, a gap of +1.24 pp. Rice and other cereals contributed +1.67 pp of it: cereal prices rose 18.3% in the bottom-30% basket and 15.7% in the all-income basket, and cereals weigh 19.6% in the first against 9.4% in the second. Passenger fares added +0.15 pp — passenger transport services in the bottom-30% basket rose 9.1%, against 4.7% for all households — and household fuels +0.13 pp. Motor fuel for private vehicles worked the other way (−0.38 pp), as did rents (−0.23 pp): better-off households bore more of the direct fuel increase. The historical model offers little explanation for the rice increase: over 2013–2026, cereal prices respond to retail fuel prices by only 0.012–0.019 after a year. The 2026 rice increase coincided with higher fertilizer and freight costs linked to the conflict and with changes in rice import policy [@usda_fas_2026], and our data cannot separate these causes.

Regionally (Table 6), the fuel-driven rise in the bottom-30% CPI by August ranges narrowly, because the pooled responses are applied to regional fuel paths that moved together. For a family of five at the poverty line, it amounts to about PHP 467 a month nationally (PHP 390 in XII SOCCSKSARGEN to PHP 633 in the National Capital Region), out of a total price-driven increase in the cost of the poverty-line basket of about PHP 907 a month. Actual bottom-30% inflation, however, differed widely: it was highest in XI Davao (8.5), BARMM (7.9), VI Western Visayas (7.5), XIII Caraga (7.1), IX Zamboanga Peninsula (7.1), against 3.5 in the National Capital Region (log points). Fuel explains on average about 72% of the rise in NCR, CAR and Regions I to IV-A, and only 44% in the six Mindanao regions.

# 4. Discussion

## 4.1 Main findings

Three findings stand out. First, fuel price shocks pass through to Philippine consumer prices quickly and lastingly: a 10% increase in pump prices raises the price level by about 1.0% within a year, as in the average developing economy, but the effect arrives as fast as in advanced economies. Second, the cross-country result that fuel shocks are progressive [@kpodar_liu_2022] does not hold within the Philippines. The poor's prices rise as much as, and in the regional panel more than, the average household's. The expenditure weights alone would predict progressivity; the reversal comes from larger increases within the categories the poor buy — their food, their utilities and, in 2026, their fares. Third, the regressive gap was largest in the 2000s and has narrowed since 2013. In 2026 it widened again: the historical model attributes about half of the 2026 gap to fuel, while in accounting terms the gap came mostly from rice. The two readings are compatible if rice is one of the routes through which oil reaches the poor — through fertilizer and freight — a route that the post-2013 data, in which cereal prices barely respond to pump prices, do not capture.

These results are consistent with the view that a single-country test with official income-group indices can overturn conclusions drawn from reconstructed indices. Quintile CPIs built from survey shares apply national component prices to each group's weights. That method rules out, by construction, the within-category differences that drive our result. Our weight-only decomposition, which mimics it, reproduces the progressive sign of the cross-country literature; the official bottom-30% index does not.

## 4.2 Policy implications

The evidence supports five implications for the response to fuel shocks.

*Untargeted cuts in gasoline and diesel taxes would mainly help better-off households.* Motor fuel takes 2.39% of the all-income basket but 1.59% of the bottom-30% basket, and in 2026 private vehicle fuel lowered the poor's relative inflation by 0.38 pp. The government's decision not to suspend excise taxes on gasoline and diesel, on the grounds that doing so would not be progressive, is consistent with our estimates.

*Excise relief on LPG is distribution-neutral, and its scale is small.* LPG prices respond equally in both baskets and both groups give LPG the same budget share, so the LPG excise suspension under RA 12316 helps the poor and the non-poor in proportion. At about PHP 37 per 11-kg tank, it would offset roughly 8% of the fuel-driven monthly cost increase of a poverty-line family even if the family bought one tank a month. Kerosene relief is better targeted but small, given kerosene's weight. The household fuel the poor use most — charcoal and wood — does not respond to oil prices at all.

*Cash transfers, sized with the bottom-30% CPI, are the better-targeted instrument.* Our estimates translate the shock into a monthly amount: about PHP 467 for the fuel-driven component and about PHP 907 for the full price increase faced by a poverty-line family of five by August 2026. Existing registries of poor households would allow such transfers to be targeted. Because the poor's prices respond faster and stay higher, relief should not be withdrawn as soon as fuel prices ease: in 2026 the price level did not fall back when pump prices did.

*Fare policy and food policy matter as much as fuel policy.* The poor's historical insulation from fuel shocks through regulated fares broke down in 2026, when their passenger fares rose 9.1% against 4.7% for all households. Fuel subsidies to public transport operators that delay fare increases are therefore a way of protecting the poor, not only the operators; the jeepney fare increase that took effect at the end of September 2026 will add to the poor's inflation from October. Above all, rice accounted for most of the poor's excess inflation in 2026. Whatever its exact cause, monitoring and relief that focus on pump prices miss the longer route from oil to fertilizer, freight and rice.

*Regional relief should follow regional prices, not regional fuel prices.* Fuel price increases were similar across regions, but the poor's inflation was much higher in XI Davao, BARMM, VI Western Visayas, XIII Caraga and IX Zamboanga Peninsula than in the National Capital Region, and fuel explains less than half of it in Mindanao. Regional bottom-30% CPIs, which PSA already publishes monthly, are a better basis for allocating relief than pump prices.

For monetary policy, the results suggest that the second-round effects of a fuel shock build over at least a year, and that analyses based on crude oil prices understate them by more than half. Since the burden falls slightly harder on the poor, policy rate increases aimed at second-round effects need to be accompanied by targeted fiscal support rather than broad fuel tax cuts.

## 4.3 Limitations

Several limitations qualify these results. First, retail fuel prices may respond to domestic conditions. Results with Dubai crude in pesos have the same sign, but an identified oil supply shock [@kilian_2009; @baumeister_hamilton_2019; @kanzig_2021] used as an instrument would strengthen the causal interpretation. Second, our contrast compares the bottom 30% with all households, not the poorest with the richest, and so understates differences between groups. Third, the bottom-30% series before 2018 are PSA backcasts, and the gap is somewhat larger in months when the base changes, although dummies for those months leave the results unchanged. Fourth, the distributional effect is concentrated in 2001–2012 and is sensitive to macro controls and to the short alternative fuel series; we regard it as robust in sign but uncertain in size. Fifth, the 2026 analysis covers only eight months, and the decomposition of the 2026 gap is descriptive: we cannot separate the oil-related part of the rice increase from trade-policy and supply factors. The ranges reported for the 2026 fuel-driven changes are indicative, combining the per-horizon bands without their covariance. Sixth, regional tests involve four groups and 17 units, and none survives a multiple-testing correction. Finally, price indices measure the cost of a fixed basket; they ignore substitution and the income effects of oil shocks on the poor, such as lower earnings for drivers and farmers.

## 4.4 Conclusion

The 2026 oil shock raised prices for poor Filipino households faster than for the average household. Our estimates show that this is not an accident of 2026. Over twenty-five years, fuel price shocks have been at best neutral and often regressive in the Philippines, contrary to the cross-country evidence, because the poor's food, utilities and fares absorb more of the shock than their small spending on motor fuel would suggest. The policy lesson is to protect the poor with transfers sized to their own price index and with attention to rice and fares, rather than with broad cuts in fuel taxes.

# Declarations

**Data and code availability.** All data are public. The replication package (download scripts, raw files with a source log, estimation code, tests and a decision log recording when each specification was fixed) reproduces every number, table and figure with one command.

**Use of AI tools.** [To be completed by the author in line with the journal's policy: describe how AI tools were used in data processing, coding and drafting, and confirm that the author reviewed and takes responsibility for all content.]

**Funding.** [To be completed.] **Conflict of interest.** [To be completed.] **Acknowledgements.** [To be completed.]

# References

::: {#refs}
:::

# Tables

**Table 1. Data sources**

| Series | Source | Frequency and coverage | Use |
|---|---|---|---|
| CPI, all income households, 13 COICOP divisions and sub-indices (2018 = 100) | PSA OpenSTAT | Monthly, Jan 1994–Aug 2026; national and 17 regions | Outcomes (RQ1, RQ3) |
| CPI, bottom 30% income households (2018 = 100) | PSA OpenSTAT | Monthly, all items Jan 2000–Aug 2026; by commodity from Jan 2012; national and 17 regions | Outcomes (RQ1, RQ2, RQ4) |
| CPI sub-index 07.2.2, fuels and lubricants for personal transport | PSA OpenSTAT | Monthly, Jan 1994–Aug 2026; national and 17 regions | Fuel price shock |
| CPI sub-index 07.2.2.2, gasoline | PSA OpenSTAT | Monthly, Jan 2018–Aug 2026 | Alternative shock |
| Regular gasoline pump price, Manila (RON 91) | World Bank Global Fuel Prices Database | Monthly, Jan 2017–Mar 2025 | Alternative shock; validation of the fuel index |
| Dubai and Brent crude oil prices | World Bank Pink Sheet | Monthly, 1960–Sep 2026 | Alternative shock |
| Peso–dollar rate; policy rate | BSP; BIS | Monthly | Controls |
| FAO Food Price Index | FAO | Monthly, 1990–Sep 2026 | Control |
| CPI weights, both baskets | PSA OpenSTAT | 2018 | Decompositions |
| Poverty incidence and thresholds by region | PSA | 2018, 2021, 2023 | Region groups; peso costs |
| HICP all items and CP0722; pump prices with and without taxes | Eurostat; European Commission Weekly Oil Bulletin | Monthly, 2000–2019 | Validation (EU) |

**Table 2. Cumulative response to a 1% increase in retail fuel prices**

| Horizon (months) | CPI, all income | CPI, bottom 30% | Gap ln(CPI all/CPI b30), national | Gap, 17-region panel |
|---|---|---|---|---|
| 0 | 0.044*** (0.006) | 0.044*** (0.009) | −0.0000 (0.0040) | −0.0006 (0.0032) |
| 3 | 0.077*** (0.015) | 0.097*** (0.026) | −0.0185* (0.0110) | −0.0149** (0.0075) |
| 6 | 0.087*** (0.015) | 0.095*** (0.023) | −0.0155 (0.0103) | −0.0214** (0.0084) |
| 9 | 0.093*** (0.018) | 0.103*** (0.026) | −0.0137 (0.0101) | −0.0187** (0.0086) |
| 12 | 0.102*** (0.017) | 0.102*** (0.026) | −0.0097 (0.0113) | −0.0173** (0.0085) |

*Notes:* Cumulative response of 100 × ln of each index (pp) to a 1% increase in the fuel index, Jan 2001–Aug 2026. Gap = ln(CPI all / CPI bottom 30%); negative values mean the bottom-30% CPI rises more. National: Newey–West standard errors; panel: region fixed effects, Driscoll–Kraay standard errors. Standard errors in parentheses. \*, \*\*, \*\*\*: significant at 10%, 5%, 1%.

**Table 3. Robustness of the distributional gap**

| Specification | Gap, h = 6 | Gap, h = 12 | CPI all, h = 12 |
|---|---|---|---|
| Baseline, national | −0.0155 (0.0103) | −0.0097 (0.0113) | 0.102*** (0.017) |
| Baseline, 17-region panel | −0.0214** (0.0084) | −0.0173** (0.0085) | — |
| (a) Shock: Dubai crude in pesos | −0.0093 (0.0056) | −0.0075 (0.0063) | 0.041*** (0.009) |
| (b) + PHP/USD, policy rate, FAO food index | −0.0046 (0.0156) | 0.0086 (0.0160) | 0.072*** (0.020) |
| (c) 6 lags | −0.0160* (0.0093) | −0.0157 (0.0121) | 0.107*** (0.020) |
| (c) 18 lags | −0.0191* (0.0106) | −0.0109 (0.0115) | 0.109*** (0.018) |
| (d) Excluding 2020 | −0.0186 (0.0121) | −0.0142 (0.0129) | 0.111*** (0.017) |
| (d) Shock dates to Dec 2025 only | −0.0158 (0.0097) | −0.0097 (0.0113) | 0.102*** (0.017) |
| (e) Base-change dummies (Jan 2012, Jan 2018) | −0.0155 (0.0102) | −0.0100 (0.0114) | 0.102*** (0.018) |
| (g) Reference study's window (to Jun 2019) | −0.0315 (0.0202) | −0.0215 (0.0191) | 0.093*** (0.016) |
| (h) Shock: gasoline index, 2019–2026 | −0.0016 (0.0122) | −0.0051 (0.0125) | 0.096*** (0.027) |
| (i) Shock: World Bank pump price, 2018–2025 | −0.0063 (0.0096) | −0.0005 (0.0054) | 0.072*** (0.019) |
| (k) Panel, drop re-mapped 2026 observations | −0.0215*** (0.0083) | −0.0173** (0.0085) | — |
| (l) Panel, national instead of regional shock | −0.0225** (0.0095) | −0.0188** (0.0095) | — |
| Supplementary: national, excluding 2008 | −0.0131 (0.0088) | −0.0079 (0.0115) | — |
| Supplementary: panel, excluding 2008 | −0.0177** (0.0073) | −0.0135 (0.0092) | — |
| Supplementary: panel, 2001–2012 | −0.0541*** (0.0197) | −0.0369** (0.0147) | — |
| Supplementary: panel, 2013–2026 | −0.0091 (0.0064) | −0.0063 (0.0075) | — |

*Notes:* Cumulative responses as in Table 2. Rows labelled "Supplementary" were specified after the first results. "—": not estimated for this specification.

**Table 4. Pass-through by CPI division, all income households**

| COICOP division | Weight, all income (%) | Weight, bottom 30% (%) | Cumulative response, h = 12 |
|---|---|---|---|
| 07 Transport | 9.0 | 6.1 | 0.370*** (0.044) |
| 12 Financial services | 0.0 | 0.0 | 0.358** (0.158) |
| 04 Housing, water, electricity, gas | 21.4 | 15.5 | 0.158*** (0.015) |
| 01 Food and non-alcoholic beverages | 37.7 | 54.9 | 0.072** (0.033) |
| 11 Restaurants and accommodation | 9.6 | 7.5 | 0.063*** (0.018) |
| 03 Clothing and footwear | 3.1 | 2.5 | 0.032*** (0.009) |
| 05 Furnishings and household equipment | 3.2 | 2.4 | 0.031*** (0.010) |
| 06 Health | 2.9 | 1.4 | 0.027** (0.013) |
| 13 Personal care and miscellaneous | 4.5 | 4.8 | 0.025*** (0.009) |
| 09 Recreation, sport and culture | 1.0 | 0.7 | 0.024 (0.025) |
| 08 Information and communication | 3.4 | 1.0 | 0.019*** (0.007) |
| 02 Alcoholic beverages and tobacco | 2.2 | 2.6 | 0.018 (0.055) |
| 10 Education services | 2.0 | 0.4 | −0.009 (0.022) |

*Notes:* Cumulative response after 12 months; 2018 basket weights. National, Newey–West standard errors.

**Table 5. Regional heterogeneity in the distributional gap**

| Group G | Base effect, h = 6 | Extra effect θ, h = 6 | Base effect, h = 12 | Extra effect θ, h = 12 |
|---|---|---|---|---|
| High poverty (2018 incidence above median) | −0.0271** (0.0108) | 0.0128 (0.0119) | −0.0131 (0.0100) | −0.0095 (0.0078) |
| High food share of the regional basket (above median) | −0.0240*** (0.0085) | 0.0060 (0.0044) | −0.0216** (0.0094) | 0.0100* (0.0052) |
| Mindanao | −0.0263** (0.0108) | 0.0146 (0.0151) | −0.0118 (0.0096) | −0.0166* (0.0092) |
| Island regions (MIMAROPA, VI, VII, VIII) | −0.0201*** (0.0078) | −0.0061 (0.0096) | −0.0147* (0.0079) | −0.0123 (0.0086) |

*Notes:* 17-region panel; each row adds the interaction of the regional fuel shock with the group dummy G. Base effect: regions outside G; θ: additional effect in G. Driscoll–Kraay standard errors.

**Table 6. The 2026 shock by region, December 2025 to August 2026**

| Region | Poverty 2018 (%) | Fuel price rise, Dec 2025–Aug 2026 (%) | Fuel-driven rise, bottom-30% CPI | Actual rise, bottom-30% CPI | Fuel-driven extra cost, poverty-line family of five (PHP/month) |
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

*Notes:* Changes in 100 × log points. Fuel-driven rise: pooled panel responses estimated on data to Dec 2025, applied to each region's fuel path (national model for the Philippines); indicative range in brackets. Cost: 2023 poverty threshold for a family of five, carried to Dec 2025 with the regional bottom-30% CPI. †: boundaries changed in 2024; 2026 months chained from the new geographic code.

**Table 7. Household fuels, fares and cereals: weights and responses, 2013–2026**

| Item | Weight, all (%) | Weight, b30 (%) | Response, all-income index | Response, bottom-30% index |
|---|---|---|---|---|
| 04.5 Electricity, gas and other fuels | 6.74 | 10.11 | 0.424*** (0.038) | 0.294*** (0.050) |
| 04.5.2 Gas (LPG) | 1.27 | 1.33 | 0.730*** (0.152) | 0.722*** (0.148) |
| 04.5.3 Liquid fuels (kerosene) | 0.04 | 0.27 | 1.152*** (0.114) | 1.111*** (0.107) |
| 04.5.4 Solid fuels (charcoal, wood) | 0.87 | 4.02 | 0.013 (0.026) | 0.038 (0.024) |
| 07.3 Passenger transport services (fares) | 4.54 | 3.72 | 0.071 (0.079) | 0.010 (0.101) |
| 01.1.1 Cereals and cereal products | 12.32 | 23.64 | 0.019 (0.084) | 0.012 (0.101) |

*Notes:* Cumulative response after 12 months of each sub-index in each basket; national, Newey–West standard errors. Supplementary analysis.

# Figures

![Figure 1. Cumulative pass-through of a 1% fuel price increase to the price level, all income and bottom 30% households, with 90% bands.](../output/figures/fig1_rq1_passthrough.png){width=85%}

![Figure 2. Cumulative response of ln(CPI all/CPI bottom 30%) to a 1% fuel price increase, national and 17-region panel. Negative values mean the bottom 30% face larger price increases.](../output/figures/fig2_rq2_rq4_ratio.png){width=100%}

![Figure 3. Cumulative pass-through after 12 months by CPI division, with 90% confidence intervals.](../output/figures/fig3_rq3_components.png){width=90%}

![Figure 4. Additional distributional effect in groups of regions after 12 months, with 90% confidence intervals.](../output/figures/fig4_rq4_groups.png){width=85%}

![Figure 5. Robustness of the six-month distributional effect, with 90% confidence intervals.](../output/figures/fig5_robustness.png){width=90%}

![Figure 6. Actual price changes in 2026 against the fuel-driven changes predicted by a model estimated on 2001–2025 data.](../output/figures/fig6_2026_out_of_sample.png){width=100%}

![Figure 7. Item contributions to the difference between bottom-30% and all-income price changes, December 2025 to August 2026.](../output/figures/fig7_2026_gap_decomposition.png){width=90%}
