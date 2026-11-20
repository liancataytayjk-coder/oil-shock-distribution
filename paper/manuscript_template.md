---
title: "Who Pays for Oil Shocks? Evidence from Philippine Regional Price Indices"
{%- if not blind %}
author:
  - "{{ author }}[^aff]"
date: "{{ date }}"
{%- endif %}
abstract: |
  We estimate how retail fuel prices pass through to the consumer prices of poor and average households, using the official price indices for the bottom 30% of households and for all households in 17 Philippine regions, 2001–2026, and panel local projections. A 1% rise in fuel prices raises the price level by {{ pn.p_all_c12 }}% after a year. The prices of the bottom 30% rise about a quarter more, although their budget shares predict the opposite. The extra burden moves with food prices. Estimated on data to 2025, the model predicts the poor's excess inflation during the 2026 oil shock.

  **Keywords:** oil price shocks; inflation inequality; fuel prices; local projections; Philippines

  **JEL classification:** E31, Q41, I32, D31
bibliography: references.bib
link-citations: true
---

<#-- Manuscript for the Asian Economic Journal (decision D16). Rendered by code/python/11_manuscript.py:
     paper/manuscript.* (reading version) and paper/manuscript_submission.* (blind = True; every block between
     <!--F--> and <!--/F--> moves to the end), plus paper/manuscript_title_page.*. Numbers: pn = panel_numbers.json,
     n = paper_numbers.json, x = computed in 11_manuscript.py. --#>
{%- if not blind %}

[^aff]: {{ affiliation }}.
{%- endif %}

# 1. Introduction

When the price of oil rises, households pay more for fuel and, with a delay, for almost everything that fuel helps to produce and move. Whether poor households pay more than others is a question with direct policy consequences. Governments respond to oil shocks with fuel tax relief, fuel subsidies and cash transfers, and each response rests on an assumption about who bears the cost.

The most comprehensive evidence on this question comes from @kpodar_liu_2022. Using retail fuel prices for 122 countries and consumer price indices for income quintiles that they rebuild from household budget surveys, they find that fuel price increases are *progressive*: the price level of the richest households rises more than that of the poorest, because richer households spend more on vehicle fuel. Their indices, however, assign the same price change to every income group within each spending category and let only the budget shares differ. If poor households buy different items within a category, and those items respond differently to fuel prices, rebuilt indices cannot detect it [@jaravel_2021].

The Philippines offers a direct test. The Philippine Statistics Authority publishes an official consumer price index for the bottom 30% of households by income, monthly and for each of 17 regions, built from that group's own budget shares at a detailed item level. Poor Filipino households spend {{ n.w_food_b30 }}% of their budget on food, against {{ n.w_food_all }}% for all households, and {{ n.w_fuel_b30 }}% on fuel for their own vehicles, against {{ n.w_fuel_all }}%. The question also became pressing in 2026, when an oil shock raised the retail fuel price index {{ n.yoy_fuel_apr }}% above its level a year earlier and inflation for the bottom 30% reached {{ n.yoy_b30_apr }}% in April.

We make three contributions. First, we estimate the pass-through of retail fuel prices to the price level of all households and of the bottom 30% in a panel of 17 regions, with local projections [@jorda_2005] specified as in @kpodar_liu_2022. A 1% rise in fuel prices raises the all-household price level by {{ pn.p_all_c0 }}% in the month of the shock and by {{ pn.p_all_c12 }}% after a year. Second, we show that the effect is regressive, the opposite of the cross-country result. Six months after a shock, the price level of the bottom 30% has risen {{ pn.gap_rel_pct }}% more than that of all households, and the difference is significant at every horizon from {{ pn.gap_sig_from }} to {{ pn.gap_sig_to }} months. A budget-share calculation predicts a progressive effect, so the regressive gap must arise from faster price increases within the categories the poor buy; we show that it moves with food prices. Third, we test the estimates out of sample. Responses estimated on data ending in December 2025 predict a 2026 gap of {{ pn.e_gap_fd }} log points (90% bootstrap band {{ pn.e_gap_lo }} to {{ pn.e_gap_hi }}), against an actual {{ pn.e_gap_act }}, and put the fuel-driven cost to a family of five at the poverty line at PHP {{ pn.php_cost_b30 }} a month.

To the best of our knowledge, this is the first study to estimate the distributional pass-through of fuel prices with an official price index for low-income households. Section 2 reviews the related literature. Section 3 sets out a simple framework. Section 4 describes the data and the method. Section 5 presents the results, and Section 6 applies them to the 2026 oil shock. Section 7 concludes.

# 2. Related literature

The first strand of literature studies how oil price shocks reach consumer prices. @kilian_2009 separates oil supply shocks from shocks to global demand for commodities and to demand specific to oil, and shows that their effects on prices and activity differ. @blanchard_gali_2010 find that oil shocks had much smaller effects on inflation in the 2000s than in the 1970s, which they attribute to weaker wage responses, more credible monetary policy and a smaller oil share in production. @kanzig_2021 identifies oil supply news from futures price movements around OPEC announcements and finds that such news raises prices and inflation expectations immediately. These studies trace effects over time and distinguish the source of the shock; they do not ask who bears it.

The second strand measures pass-through to inflation. @kpodar_abdallah_2017 build a database of monthly retail fuel prices for 162 countries and find that changes in world crude prices reach pump prices within about six months, more fully for increases than for decreases. @choi_etal_2018 estimate for 72 countries that a 10% rise in world oil prices raises inflation by about 0.4 percentage points on impact. @gelos_ustyugova_2017 find larger and more persistent effects where food and fuel weigh more in the basket. In developing Asia during the 2007–2008 price spike, subsidies and price controls limited the pass-through [@jongwanich_park_2011]. For the Philippines, @allon_pineda_etal_2026 find with local projections that oil and food price shocks have persistent effects on national inflation, and @valera_etal_2025 find across provinces that energy and rice prices raise inflation more when inflation is already high. None of these studies distinguishes income groups. @kpodar_liu_2022 do, with the rebuilt indices described above, and find a progressive effect that persists beyond a year in developing economies.

The third strand asks who bears fuel price changes. Richer households capture most of the benefit of fuel subsidies [@coady_etal_2015], and energy price increases tend to be progressive in poorer countries because energy budget shares first rise and then fall with income [@dorband_etal_2019]. Both conclusions rest on budget shares. Studies of inflation inequality point to a channel that budget shares miss: households with different incomes face different price changes within the same categories [@jaravel_2021]. In the Philippines, the food price increases of 2006–2008 raised poverty, and the poorest households were affected most whether or not they farmed [@fujii_2013]. Rice, the largest single item in the poor's basket, also responds to trade policy: the 2019 rice tariffication law lowered rice prices, and the poorest quintiles gained most [@balie_etal_2021].

Our study joins these strands. We estimate pass-through as in the second strand, ask the distributional question of the third, and answer it with official prices that capture differences within categories.

# 3. Framework

Fuel is an input to almost every good. In the input–output price model [@miller_blair_2009], if margins and other costs are unchanged, a fuel price shock $f_t = 100\,\Delta \ln F_t$ raises the price of good *k* in proportion to its total fuel cost share $\phi_k$, so that $\pi_{k,t} \approx \phi_k f_t$. A group's consumer price index weights item prices by that group's budget shares $w^g_k$, so

$$\pi^g_t \approx \Phi^g f_t, \qquad \Phi^g = \sum_k w^g_k\, \phi_k. \qquad\qquad (1)$$

Intuitively, a group's pass-through equals the fuel intensity of its basket. We measure the difference between the two groups with the *inflation gap*, $D_t = 100 \ln(P^A_t / P^B_t)$, where *A* denotes all households and *B* the bottom 30%. Its monthly change is $\Delta D_t = \pi^A_t - \pi^B_t$, so a negative response of the gap means that the poor's prices rise more; we call such an effect *regressive*. The gap splits exactly into two terms:

$$\pi^A_t - \pi^B_t = \sum_k (w^A_k - w^B_k)\, \pi^A_{k,t} + \sum_k w^B_k\, (\pi^A_{k,t} - \pi^B_{k,t}). \qquad\qquad (2)$$

The first term is a *weights effect*: the gap that arises because the groups divide their budgets differently across categories. The second is a *within-category effect*: the gap that arises because the groups buy different items within a category, whose prices change differently. Indices rebuilt from budget shares with common category prices capture only the first term. Finally, following @deaton_1989, the rise in a group's price index approximates the extra spending the group needs to buy the same basket, which lets us express the burden of a shock in pesos.

# 4. Data and method

## 4.1 Data

All price data are monthly consumer price indices of the Philippine Statistics Authority on the 2018 = 100 base [@psa_openstat_2026], for 17 regions. The shock is the change in the sub-index 07.2.2, fuels and lubricants for personal transport, which measures retail gasoline and diesel prices. Its monthly changes correlate at 0.87 with the World Bank's Manila pump price over 2016–2025. The outcomes are the all-household index and the bottom-30% index of each region. The bottom-30% series join the statistics authority's own back-calculated series for 2000–2017 to the current series.[^splice] Because these back-calculations exist only for the 17 regions defined before the Negros Island Region was created in 2024, we keep the 17-region map and extend it to August 2026 with the monthly changes published on the new map.[^nir] The panel is balanced, and the shock dates run from January 2001 to August 2026, which gives {{ pn.obs_h0 }} region-months at the first horizon.

The robustness checks use Dubai crude oil in pesos [@worldbank_cmo_2026], the peso–dollar exchange rate and the policy interest rate of the central bank, and the FAO world food price index; these national series are the same for every region in a month. The budget-share calculation uses the 2018 weights of the two baskets and the national division indices. Poverty lines come from the statistics authority.

[^splice]: The back-calculated series are joined in January 2012 and January 2018. Monthly changes in the gap are larger in those two months than on average; dummies for them leave the national gap unchanged to three decimals.

[^nir]: The new map changes the boundaries of Regions VI, VII and XII and of the Bangsamoro region. Dropping their re-mapped 2026 months leaves the gap at six months unchanged to three decimals.

## 4.2 Panel local projections

For each horizon *h* = 0, 1, …, 12 months, we estimate by ordinary least squares the panel version of the specification of @kpodar_liu_2022:

$$\sum_{j=0}^{h} y_{r,t+j} = \mu_{r,h} + B_h f_{r,t} + \sum_{q=1}^{12} \gamma_{q,h}\, y_{r,t-q} + \sum_{q=1}^{12} \lambda_{q,h}\, f_{r,t-q} + \sum_{l=1}^{h-1} \rho_{l,h}\, f_{r,t+l} + \delta_h\, t + \varepsilon_{r,t+h}, \qquad\qquad (3)$$

where $y_{r,t}$ is monthly inflation (or the change in the gap) in region *r*, $f_{r,t}$ is the region's fuel shock, $\mu_{r,h}$ is a region fixed effect and *t* is a linear trend. The left-hand side is the change in the log price level from *t* − 1 to *t + h*, so $B_h$ is the *cumulative response*: the percentage change in the price level *h* months after a 1% rise in fuel prices. Intuitively, each horizon is a separate regression of the price level *h* months ahead on today's shock, holding the past constant [@jorda_2005]. The twelve lags absorb the persistence of inflation and the seasonality of the unadjusted indices. The leads $f_{r,t+1}, \dots, f_{r,t+h-1}$ hold constant the further fuel price changes that tend to follow a first one [@teulings_zubanov_2014], so that $B_h$ measures the effect of a single shock; we keep the lead set of the reference study. Lags and leads are built within regions before the sample is restricted, so the first shock dates keep their lags.

Two features of the panel matter for inference. The outcome at horizon *h* overlaps with the outcomes of neighbouring months, so the errors are serially correlated; and every region is hit by the same national events in the same month, so the errors are correlated across regions. We therefore report Driscoll–Kraay standard errors with *h* + 1 lags, which allow both forms of dependence [@driscoll_kraay_1998]. With about 300 months per region, the bias from combining fixed effects with lagged outcomes is negligible. Bands are 90%, as in the reference study. The estimator recovers known responses in simulated data.

## 4.3 The budget-share calculation

To ask whether budget shares can explain the sign of the gap, we apply the weights term of equation (2) to estimated responses. For each of the 13 divisions *k* of the national consumer price index, we estimate the twelve-month cumulative response $B^{(k)}_{12}$ with the national version of equation (3) and compute

$$G^{w} = \sum_{k=1}^{13} B^{(k)}_{12}\, \frac{w^A_k - w^B_k}{100}. \qquad\qquad (4)$$

$G^w$ is the gap that would arise if both groups faced the same price change within each division. A positive value is progressive. The difference between the estimated gap and $G^w$ is the within-category part. This calculation is an accounting exercise outside the regression model: it describes where the gap comes from and does not test a causal channel.

## 4.4 The 2026 out-of-sample test

To test the estimates on an episode they have not seen, we re-estimate equation (3) on data that end in December 2025 and apply the responses to the fuel price changes of 2026. Because responses add up, the fuel-driven change in the log price level between December 2025 and month *m* is

$$\widehat{\Delta \ln P}_{m} = \sum_{s=1}^{m} \widehat{B}_{m-s}\, f_s, \qquad\qquad (5)$$

where $f_s$ is the fuel shock in month *s* of 2026. We apply the panel responses to the national fuel path and compare the prediction with the actual change in the national indices. The prediction combines thirteen estimated coefficients whose sampling errors are correlated across horizons. We therefore compute its uncertainty with a moving-block bootstrap: we resample blocks of 12 consecutive months, with all regions of a month kept together, re-estimate all horizons and recompute equation (5), {{ pn.b_reps }} times. The 90% band is the 5th to 95th percentile of the bootstrap distribution.

# 5. Results

## 5.1 The record

The inflation of the bottom 30% exceeded that of all households in {{ n.d_years_b30_higher }} of the {{ n.d_years_total }} years from 2001 to 2025 (Fig. 1). The largest difference occurred in 2008, when the oil price spike coincided with a rice price crisis and annual inflation reached {{ n.d_2008_b30 }}% for the bottom 30% against {{ n.d_2008_all }}% for all households. In {{ x.n_episodes_b30 }} of the {{ x.n_episodes }} episodes in which retail fuel prices stayed at least 15% above their level a year earlier, the poor's inflation was the higher of the two (Table 1). This descriptive record already points away from a progressive effect; the regressions below ask whether it is caused by fuel prices.

<!--F-->
![Figure 1. Year-on-year inflation of all households and of the bottom 30% (a), the gap between them (b), and the retail fuel price index (c), Philippines, 2001–2026.](../output/figures/fig03_trends.png){width=88%}
<!--/F-->

<!--F-->
Table: Table 1. Fuel price episodes: at least three months with retail fuel prices 15% or more above their level a year earlier

{{ t.episodes }}

::: {custom-style="Table Note"}
*Notes:* National series. Inflation is the average year-on-year rate during the episode.
:::
<!--/F-->

## 5.2 Pass-through to the price level

Retail fuel prices pass through quickly and lastingly (Table 2, Fig. 2). A 1% rise raises the all-household price level by {{ pn.p_all_c0 }}% in the month of the shock, by {{ pn.p_all_c6 }}% after six months and by {{ pn.p_all_c12 }}% after a year, so that a 10% rise in pump prices leaves consumer prices about {{ pn.p_all_c12_10pct }}% higher a year later. The bottom-30% price level responds by {{ pn.p_b30_c0 }}%, {{ pn.p_b30_c6 }}% and {{ pn.p_b30_c12 }}%. The impact response is of the same size as the advanced-economy estimate of @kpodar_liu_2022 ({{ n.kl_adv_b0 }}) and more than twice their developing-economy estimate ({{ n.kl_dev_b0 }}). When Dubai crude oil in pesos replaces the retail price as the shock, the twelve-month response falls to {{ pn.p_crude_c12 }}, about {{ pn.p_crude_share }}% of the retail estimate; studies that measure oil shocks with crude prices therefore understate the pass-through to consumers.

<!--F-->
Table: Table 2. Cumulative response of the price level to a 1% rise in retail fuel prices, 17-region panel

{{ t.responses }}

::: {custom-style="Table Note"}
*Notes:* Percentage change in the price level (gap: percentage points) *h* months after the shock; equation (3), shock dates January 2001–August 2026, region fixed effects; Driscoll–Kraay standard errors in parentheses. \* *p* < 0.10, \*\* *p* < 0.05, \*\*\* *p* < 0.01.
:::
<!--/F-->

<!--F-->
![Figure 2. Cumulative response of the price level of all households and of the bottom 30% to a 1% rise in retail fuel prices, with 90% bands (17-region panel).](../output/figures/figP1_passthrough.png){width=72%}
<!--/F-->

## 5.3 Who pays more?

The gap responds negatively at every horizon (Table 2, Fig. 3). Six months after a 1% fuel price rise, the price level of the bottom 30% has risen {{ pn.gap_c6|replace("−", "") }} percentage points more than that of all households (standard error {{ pn.gap_c6_se }}, *t* = {{ pn.gap_c6_t }}); after a year the difference is {{ pn.gap_c12|replace("−", "") }} points ({{ pn.gap_c12_se }}). The 90% band excludes zero at every horizon from {{ pn.gap_sig_from }} to {{ pn.gap_sig_to }} months. In relative terms, the poor's price level rises about {{ pn.gap_rel_pct }}% more than the average household's: a 10% rise in pump prices raises average prices by {{ pn.all6_10pct }}% after six months and the prices of the bottom 30% by about {{ pn.gap6_10pct }} percentage points more.[^sep] The progressive effect found across countries does not hold in the Philippines; the effect is regressive.

[^sep]: The difference between the separate responses in Table 2 is {{ pn.diff_sep_c6 }} at six months, close to the direct estimate of the gap. The two need not coincide, because the separate regressions control for each group's own past inflation while the gap regression controls for the past gap.

<!--F-->
![Figure 3. Cumulative response of the gap 100 × ln(CPI all households / CPI bottom 30%) to a 1% rise in retail fuel prices, with 90% band (17-region panel). Values below zero mean that the prices of the bottom 30% rise more.](../output/figures/figP2_gap.png){width=72%}
<!--/F-->

## 5.4 Why the poor pay more

Budget shares predict the opposite sign (Table 3). If both groups faced the same price change within each division, the twelve-month gap would be {{ n.gap_weights_only }}, a progressive effect. Food pushes the gap toward regressive ({{ n.dec_food }}), because the poor spend more on it. Housing and utilities ({{ n.dec_housing }}) and transport ({{ n.dec_transport }}) push it the other way, because the average household spends more on them and transport prices respond most to fuel ({{ n.div_transport }} after a year). Since the estimated gap is {{ pn.gap_c12 }}, the within-category part is about {{ n.within12_pan }}: prices rise faster within the categories the poor buy, by more than enough to reverse the sign implied by their budget shares.

<!--F-->
Table: Table 3. The gap implied by budget shares alone, twelve months after a 1% rise in retail fuel prices

{{ t.decomp }}

::: {custom-style="Table Note"}
*Notes:* Descriptive calculation, equation (4). Response: cumulative twelve-month response of the national all-household division index (Newey–West standard errors in parentheses). Contribution = response × (weight, all − weight, bottom 30%) ÷ 100; positive values push toward a progressive gap. Weights: 2018 baskets.
:::
<!--/F-->

The bottom-30% division indices, which the statistics authority publishes nationally from 2013, point to the same channel. Over 2013–2026, the twelve-month response of the poor's housing and utilities index, which includes cooking fuels, is {{ n.why_c04_b30 }} against {{ n.why_c04_all }} for all households, and that of their food index is {{ n.why_c01_b30 }} against {{ n.why_c01_all }}. Their transport index, mostly fares, responds less ({{ n.why_c07_b30 }} against {{ n.why_c07_all }}).[^why] The poor pay more because the goods they buy within food and utilities become relatively more expensive, not because they buy more fuel.

[^why]: These comparisons are exploratory: they were added after the first results and cover only the period for which bottom-30% division indices exist. Because item-level indices for the bottom 30% start in 2013, the 2008 episode cannot be decomposed by item.

## 5.5 Robustness

Table 4 and Fig. 4 report five checks on the gap. The result does not depend on any single region: leaving out each region in turn keeps the six-month gap between {{ pn.loo_min }} and {{ pn.loo_max }}. It does not depend on 2008: excluding the shock dates of that year gives {{ pn.rob_x08_c6 }} ({{ pn.rob_x08_c6_se }}). It survives a shock measured by a price set in world markets: with Dubai crude oil in pesos, the gap is {{ pn.rob_crude_c6 }} ({{ pn.rob_crude_c6_se }}) after six months and {{ pn.rob_crude_c12 }} ({{ pn.rob_crude_c12_se }}) after a year. The effect is, however, concentrated in the first half of the sample: {{ pn.rob_p1_c6 }} ({{ pn.rob_p1_c6_se }}) for shock dates in 2001–2012, against {{ pn.rob_p2_c6 }} ({{ pn.rob_p2_c6_se }}) in 2013–2026.

<!--F-->
Table: Table 4. Robustness of the gap

{{ t.robust }}

::: {custom-style="Table Note"}
*Notes:* Cumulative response of the gap per 1% shock, 17-region panel; Driscoll–Kraay standard errors in parentheses. Controls enter with their current value and twelve lags. \* *p* < 0.10, \*\* *p* < 0.05, \*\*\* *p* < 0.01.
:::
<!--/F-->

<!--F-->
![Figure 4. Robustness of the six-month gap, with 90% confidence intervals. The bar at the bottom spans the estimates obtained when each region is left out in turn.](../output/figures/figP3_robustness.png){width=82%}
<!--/F-->

The fifth check qualifies the result. When the regression controls for the exchange rate, the policy rate and world food prices, the six-month gap falls to {{ pn.rob_ctl_c6 }} ({{ pn.rob_ctl_c6_se }}); world food prices alone have the same effect ({{ pn.rob_food_c6 }}, {{ pn.rob_food_c6_se }}). The poor's extra burden therefore moves with world food prices, and the data admit two readings. In the first, food is the channel through which fuel prices reach the poor: fuel is an input to growing, processing and moving food, and twelve-month changes in world food prices correlate at {{ x.corr_fuel_food }} with retail fuel prices and at {{ x.corr_crude_food }} with crude oil in pesos over 2001–2026. Conditioning on a variable that the shock itself moves removes part of the effect being measured [@angrist_pischke_2009]. In the second reading, a common commodity cycle, such as a rise in global demand [@kilian_2009], raises oil and food prices together, and part of the gap reflects that cycle rather than fuel. Our data cannot separate the two readings. We therefore state the result as follows: fuel price shocks in the Philippines are not progressive, and the additional burden on the poor arrives together with, and plausibly through, food prices.

# 6. The 2026 oil shock

## 6.1 An out-of-sample test

Between December 2025 and April 2026 retail fuel prices rose {{ pn.e_fuel_cum_apr }} log points. The responses estimated on data to December 2025 predict {{ pn.e_all_fd }} of the {{ pn.e_all_act }}-point rise in the all-household price level by August 2026 and {{ pn.e_b30_fd }} of the {{ pn.e_b30_act }}-point rise in the bottom-30% level, a little more than half in both cases (Table 5, Fig. 5). They also predict the direction and most of the size of the gap: {{ pn.e_gap_fd }} log points, with a 90% bootstrap band from {{ pn.e_gap_lo }} to {{ pn.e_gap_hi }} that excludes zero, against an actual {{ pn.e_gap_act }}. A model that never saw 2026 thus anticipated that the poor would pay more. The unexplained part of the surge is consistent with the observation that prices did not fall back when fuel prices eased in May and June.

<!--F-->
Table: Table 5. The 2026 shock: predicted and actual change in the price level, December 2025 to August 2026 (100 × log points)

{{ t.e2026 }}

::: {custom-style="Table Note"}
*Notes:* Prediction from equation (5) with panel responses estimated on shock dates January 2001–December 2025, applied to the national fuel path; actual change in the national indices. Bands: moving-block bootstrap, {{ pn.b_reps }} replications, blocks of {{ pn.block }} months.
:::
<!--/F-->

<!--F-->
![Figure 5. Actual change since December 2025 and the change predicted from fuel prices by responses estimated on data to December 2025, with 90% bootstrap bands: (a) all households; (b) bottom 30%; (c) the gap.](../output/figures/figP4_2026.png){width=95%}
<!--/F-->

## 6.2 The cost to poor families

For a family of five living at the poverty line, about PHP {{ pn.php_line }} a month at December 2025 prices, the fuel-driven rise in the bottom-30% price level implies an extra cost of PHP {{ pn.php_cost_b30 }} a month by August 2026 (90% band PHP {{ pn.php_cost_b30_lo }} to {{ pn.php_cost_b30_hi }}). About PHP {{ pn.php_extra }} of it (band PHP {{ pn.php_extra_lo }} to {{ pn.php_extra_hi }}) is the excess over what the same family would pay at the average household's inflation. Counting every price increase, not only the fuel-driven part, the extra cost was PHP {{ pn.php_actual_cost_b30 }}. Across regions, applying the same responses to each region's fuel path, the fuel-driven cost ranges from PHP {{ pn.php_reg_min }} in {{ pn.php_reg_min_name }} to PHP {{ pn.php_reg_max }} in the {{ pn.php_reg_max_name }} (Table 6). The burden is thus large for everyone, and about a quarter larger for the poor.

<!--F-->
Table: Table 6. The 2026 shock by region, December 2025 to August 2026

{{ t.regions }}

::: {custom-style="Table Note"}
*Notes:* Predicted: change in 100 × ln of the region's bottom-30% index implied by equation (5) and the region's fuel path. Cost: extra monthly spending of a family of five at the region's official poverty line. †Boundary changed in 2024; 2026 months extended with the new map.
:::
<!--/F-->

## 6.3 Which prices drove the gap

A descriptive accounting of the 2026 episode identifies the items behind the gap. For a fixed-weight index, the contribution of item *k* to the change in group *g*'s index between December 2025 and August 2026 is $w^g_k (I^g_{k,m} - I^g_{k,0}) / I^g_0$, and the contributions add up to the change in the index. By this accounting, the bottom-30% index rose {{ n.e5_b30_total }}% and the all-household index {{ n.e5_all_total }}%, a difference of {{ n.e5_total_gap }} points (Fig. 6). Rice and other cereals contributed {{ n.e5_cereals_gap }} points: cereal prices rose {{ n.e5_cereal_pct_b30 }}% in the poor's basket, where cereals weigh {{ n.e5_cereal_w_b30 }}%, against {{ n.e5_cereal_pct_all }}% and {{ n.e5_cereal_w_all }}% in the average basket. Fares added {{ n.e5_fares_gap }} and household fuels {{ n.e5_hhfuel_gap }}, while fuel for private vehicles ({{ n.e5_ownfuel_gap }}) and rent ({{ n.e5_rent_gap }}) narrowed the gap. The 2026 rice increase also reflects fertiliser and freight costs and import policy [@usda_fas_2026]; the accounting describes the gap and does not attribute it to fuel.

<!--F-->
![Figure 6. Contribution of each item group to the difference between the bottom-30% and all-household price changes, December 2025 to August 2026 (percentage points).](../output/figures/fig08_rq3_decomposition.png){width=80%}
<!--/F-->

## 6.4 Implications for policy

The results bear on the policy responses of 2026. Republic Act 12316 allows the President to suspend fuel excise taxes when world oil prices are high [@ra12316_2026]; the government suspended the excise on liquefied petroleum gas and kerosene but not on gasoline and diesel, subsidised transport drivers, and raised the policy rate {{ n.n_hikes_word }} times. Relief on gasoline and diesel would mainly benefit households that own vehicles, since motor fuel is {{ n.w_fuel_all }}% of the average basket and {{ n.w_fuel_b30 }}% of the poor's. The suspension on liquefied petroleum gas saves a family about PHP 37 per 11-kg tank, roughly {{ x.lpg_share }}% of the fuel-driven monthly cost estimated above. Because the poor's extra burden arrives through food and fares, measures on rice supply and fares reach it more directly than fuel tax relief. Transfers can be sized with the bottom-30% index and the estimates of Section 6.2, and kept for at least a year, because prices did not fall when fuel prices eased.

# 7. Conclusion

We estimated the pass-through of retail fuel prices to the price level of poor and average households in a panel of 17 Philippine regions. Three findings stand out. First, pass-through is fast and lasting: a 10% rise in pump prices leaves consumer prices about {{ pn.p_all_c12_10pct }}% higher a year later, more than twice what crude prices imply. Second, the effect is regressive, contrary to cross-country evidence built on budget shares: the price level of the bottom 30% rises about a quarter more, and budget shares alone would predict the opposite sign. Third, responses estimated before 2026 predicted most of the poor's excess inflation during the 2026 shock.

The study has limitations. The regressive gap moves with world food prices, and our data cannot separate a food channel from a common commodity cycle; an exogenous measure of oil supply shocks [@kilian_2009; @kanzig_2021] would sharpen the causal reading. The gap is concentrated in 2001–2012 and is small and imprecise after 2013. The comparison is between the bottom 30% and all households, which understates the difference between the poorest and the richest. The bottom-30% series before 2018 are back-calculated, and the decompositions are descriptive. Future work could use household survey data to separate net buyers from net sellers of rice, whose exposure to an oil shock differs.

{% if blind -%}
# Declarations {-}

**Data and code availability.** All data are public. A replication package with the raw data, a source log, the cleaned data, Python and Stata 17 code and a codebook reproduces every number, table and figure; its location is given on the title page.
{%- else -%}
# Declarations {-}

**Data and code availability.** All data are public. A replication package with the raw data, a source log, the cleaned data, Python and Stata 17 code and a codebook reproduces every number, table and figure: <https://github.com/liancataytayjk-coder/oil-shock-distribution>.

**Funding.** [To be completed.] **Conflict of interest.** [To be completed.] **Acknowledgements.** [To be completed.]
{%- endif %}

# References {-}

::: {#refs}
:::
