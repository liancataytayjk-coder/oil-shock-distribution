```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part III. Interpretation

## 20. Reading a response

### 20.1 A response is a "what if"

An impulse response answers a conditional question. $B_{12} = {{ n.rq1_all_c12 }}$ for the all-income CPI means: *if* fuel prices rise 1% this month and nothing else unusual happens, consumer prices will be {{ n.rq1_all_c12 }}% higher a year later than they would otherwise have been. It does not say that prices will rise by {{ n.rq1_all_c12 }}%, because other things will also happen in that year, and it does not say what caused the fuel price rise.

### 20.2 Four questions to ask of every response

**What are the units?** Check what a one-unit shock is and what the outcome measures. In the study the shock is a 1% fuel price change and the cumulative outcome is the percentage change in the price level, so $B_h$ is "percent per 1%", an *elasticity*: the percentage change in one variable for a 1% change in another.

**How big is it in a realistic case?** Scale the response to a shock that actually happens. Fuel prices rose by about {{ n.fuel_cum_apr }} log points between December 2025 and April 2026; a typical month moves them by a few percent. A response of {{ n.rq1_all_c12 }} per 1% is small for a 1% shock but large for a 50% one.

**Is it precise?** Look at the band, not only at the estimate. Ask whether the whole band lies on one side of zero, and at which horizons. A band that crosses zero at every horizon means the data cannot tell the sign; a band that excludes zero at most horizons, with a stable shape, is strong evidence.

**What is its shape?** Does the response build up, peak and fade, or keep growing? For a price level, a response that rises and stays up means the shock has a lasting effect on prices. A zig-zag between neighbouring horizons is usually noise or a feature of the specification (Chapter 22), not economics.

## 21. Interpreting the study's results

This chapter interprets the study's main estimates as a worked example. All numbers are cumulative responses to a 1% fuel price rise.

### 21.1 RQ1: how much and how fast do fuel prices pass through?

The all-income price level rises by {{ n.rq1_all_c0 }}% in the month of the shock (standard error {{ n.rq1_all_c0_se }}), {{ n.rq1_all_c3 }}% after three months, {{ n.rq1_all_c6 }}% after six and {{ n.rq1_all_c12 }}% after twelve. The bottom-30% price level responds almost identically: {{ n.rq1_b30_c0 }}, {{ n.rq1_b30_c3 }}, {{ n.rq1_b30_c6 }} and {{ n.rq1_b30_c12 }}. Every band excludes zero.

The interpretation has three parts. *Size:* a 10% rise in pump prices raises the price level by about {{ n.rq1_all_c12_10pct }}% within a year. *Speed:* about 40% of the one-year effect happens in the first month, through the direct weight of fuel in the basket and fares that adjust quickly, and the rest builds up over the following months as transport and production costs are passed on. *Comparison:* the impact response equals the average that @kpodar_liu_2022 report for advanced economies ({{ n.kl_adv_b0 }}) and is more than twice their developing-economy average ({{ n.kl_dev_b0 }}). When world crude oil in pesos replaces the retail fuel index, the one-year response falls to {{ n.crude_c12 }}, about {{ n.crude_share }}% of the retail response: crude prices understate pass-through, because taxes and margins make pump prices move less than crude in percentage terms and the domestic index captures the price consumers actually pay.

### 21.2 RQ2: who pays more?

**National.** The cumulative response of the inflation gap is ${{ n.rq2_c3 }}$ at *h* = 3, ${{ n.rq2_c6 }}$ (standard error {{ n.rq2_c6_se }}) at *h* = 6 and ${{ n.rq2_c12 }}$ (standard error {{ n.rq2_c12_se }}) at *h* = 12. The sign is negative throughout, which means the bottom 30%'s prices rise more: the effect is regressive. But the bands include zero at most horizons; the estimate is significant at the 10% level only at *h* = {{ n.rq2_sig_h }}. The honest reading is "regressive in sign, imprecise nationally".

**Panel.** With 17 regions, the response is ${{ n.pan_c3 }}$ at *h* = 3, ${{ n.pan_c6 }}$ (standard error {{ n.pan_c6_se }}) at *h* = 6 and ${{ n.pan_c12 }}$ (standard error {{ n.pan_c12_se }}) at *h* = 12, significant at every horizon from {{ n.pan_sig_from }} to 12 months. The panel confirms the national sign with more precision. In magnitude, a 10% fuel price rise raises the poor's price level by about {{ n.gap6_10pct }} percentage points more than the average household's after six months, on top of an average rise of about {{ n.all6_10pct }}%.

**Why.** Let $w^g_k$ be the share of group *g*'s budget spent on category *k* (its *budget share*) and $\pi^g_k$ the inflation of category *k* in group *g*'s index. The gap splits exactly into two parts:

$$\pi^A - \pi^B = \sum_k (w^A_k - w^B_k)\, \pi^A_k + \sum_k w^B_k\, (\pi^A_k - \pi^B_k). \qquad\qquad (21.1)$$

The first sum is a *weights effect*: the gap that would arise if both groups faced the same price changes and differed only in what they spend their money on. The second is a *within-category effect*: the gap that arises because the groups buy different items inside each category and those items' prices change differently. Applying the 13 division responses to the two groups' budget shares gives the weights effect alone: {{ n.gap_weights_only }} at *h* = 12, a progressive number, because better-off households spend more on fuel and transport. Since the total is negative, the within-category effect must be regressive and larger: roughly ${{ n.rq2_c12 }} - ({{ n.gap_weights_only }}) \approx {{ within12 }}$. The exploratory comparison of the two baskets from 2013 points to where it comes from: the housing and utilities division of the bottom 30%, which includes household fuels, responds more ({{ n.why_c04_b30 }} against {{ n.why_c04_all }} after a year), and its food division also responds more ({{ n.why_c01_b30 }} against {{ n.why_c01_all }}), while its transport division responds less ({{ n.why_c07_b30 }} against {{ n.why_c07_all }}). The poor do not pay more because they buy more fuel; they pay more because the things they buy, such as cooking fuels and food, become relatively more expensive after a fuel shock.

### 21.3 Robustness: does the conclusion survive?

Read robustness checks as a group and report all of them, including those that weaken the result. Table 10 collects the study's core checks for the gap at *h* = 6.

Table: Table 10. Core robustness checks: cumulative response of the inflation gap at *h* = 6.

| Specification | Estimate | s.e. | Reading |
|---|---:|---:|---|
| National baseline | {{ n.rq2_c6 }} | {{ n.rq2_c6_se }} | Regressive, imprecise |
| Dubai crude in pesos as the shock | {{ n.rob_crude }} | {{ n.rob_crude_se }} | Same sign with an outside price |
| Macroeconomic controls | {{ n.rob_macro }} | {{ n.rob_macro_se }} | Smaller, not significant |
| Excluding 2020 | {{ n.rob_x20 }} | {{ n.rob_x20_se }} | Unchanged |
| Panel, 2001–2012 | {{ n.split_p1 }} | {{ n.split_p1_se }} | Strong, significant |
| Panel, 2013–2026 | {{ n.split_p2 }} | {{ n.split_p2_se }} | Small, not significant |
| Panel, leaving out one region | {{ n.loo_min }} to {{ n.loo_max }} | | No region drives the result |

::: {custom-style="Table Note"}
Note: Responses per 1% fuel price rise; a negative value means the bottom 30%'s prices rise more. Source: `output/tables/estimates.csv`.
:::

The sign is negative in every specification, which supports the direction of the result. Two checks qualify it. With macroeconomic controls the estimate shrinks to about a third and loses significance, so part of the gap may come from the exchange rate, interest rates or world food prices moving together with fuel prices. And the gap is concentrated in 2001–2012, a period that includes the 2008 rice crisis; since 2013 it has been small. A careful write-up states both, rather than reporting only the checks that agree.

### 21.4 RQ3: applying the responses to 2026

Chapter 18 showed how the responses, estimated only on data up to December 2025, explain the 2026 surge. Fuel accounts for {{ n.e1_all_fd }} of the {{ n.e1_all_act }}% rise in the all-income price level by August 2026 (about {{ n.e1_all_share }}%) and {{ n.e1_b30_fd }} of the {{ n.e1_b30_act }}% rise for the bottom 30% (about {{ n.e1_b30_share }}%). The model predicts the right direction for the gap (${{ n.e1_gap_fd }}$ against an actual ${{ n.e1_gap_act }}$) but only about half its size.

Responses become more useful when expressed in money. If the bottom-30% price level is {{ n.e1_b30_fd }}% higher because of fuel, a family of five living exactly at the poverty line, about PHP {{ n.e3_ph_line }} a month at December 2025 prices, needs ${{ n.e3_ph_line|replace(',', '{,}') }} \times (e^{ {{- n.e1_b30_fd -}} /100} - 1) \approx$ PHP {{ n.e3_ph_cost }} more a month to buy the same basket. Across regions this ranges from PHP {{ n.e3_min }} ({{ n.e3_min_reg }}) to PHP {{ n.e3_max }} ({{ n.e3_max_reg }}). Including the part of the surge that the model does not attribute to fuel, the actual extra cost was about PHP {{ n.e3_ph_actual_cost }}.

How should the other half of the surge be read? A local projection gives the *average* response to a 1% shock in the estimation sample. If the 2026 shock was larger, or spread through rice and other food more than past shocks did, the model will under-predict. The study's descriptive decomposition finds exactly this: cereals alone account for {{ n.e5_cereals_gap }} percentage points of the bottom 30%'s excess price rise of {{ n.e5_total_gap }}. An out-of-sample test like this is valuable precisely because it shows where the average response stops being a good guide.

## 22. The lead convention: what it changes

Chapter 4 explained that the study, following the reference paper, uses leads 1 to *h* − 1, while Teulings and Zubanov's own correction uses leads 1 to *h*. Table 11 compares the two on the study's national data.

Table: Table 11. Cumulative responses under two lead conventions (national, 2001–2026).

| *h* | 0 | 1 | 2 | 3 | 6 | 9 | 12 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| All-income CPI, leads 1 to *h* − 1 | {% for h in [0,1,2,3,6,9,12] %}{{ f(t.step6[h].all_paper, 3) }} | {% endfor %}
| All-income CPI, leads 1 to *h* | {% for h in [0,1,2,3,6,9,12] %}{{ f(t.step6[h].all_full, 3) }} | {% endfor %}
| Inflation gap, leads 1 to *h* − 1 | {% for h in [0,1,2,3,6,9,12] %}{{ f(t.step6[h].gap_paper, 4) }} | {% endfor %}
| Inflation gap, leads 1 to *h* | {% for h in [0,1,2,3,6,9,12] %}{{ f(t.step6[h].gap_full, 4) }} | {% endfor %}

::: {custom-style="Table Note"}
Note: The first row of each pair is the study's specification (decision D4). Source: `tutorial/lp_tutorial.py`, step 6.
:::

The two conventions differ at *h* = 1 and 2 and hardly at all from *h* = 3 on. With leads 1 to *h* − 1, the all-income response jumps to {{ f(t.step6[1].all_paper, 3) }} at *h* = 1 and falls back to {{ f(t.step6[2].all_paper, 3) }} at *h* = 2: a zig-zag. With leads 1 to *h*, it is a smooth {{ f(t.step6[1].all_full, 3) }} and {{ f(t.step6[2].all_full, 3) }}. Chapters 4 and 14 explained why: at *h* = 1 the reference convention has no lead, so next month's shock, which is correlated {{ f(t.fuel_ac1, 2) }} with this month's, is not held constant. The six- and twelve-month responses, on which the study's conclusions rest, are essentially the same under both conventions. The practical lesson is to read the responses at *h* = 1 and 2 with care, and to say in a footnote or robustness check which convention you use.

## 23. Writing up the results

### 23.1 What a results paragraph should contain

A good paragraph about an impulse response states, in order: the shock and its size; the outcome and its units; the estimate at one or two key horizons with its standard error or band; whether it is significant; what it means in a realistic case; and how it compares with earlier work. It avoids reading each horizon one by one.

### 23.2 Two examples

A weak paragraph: "Table 4 shows the results. The coefficient is 0.044 at h = 0, 0.084 at h = 1, 0.044 at h = 2, and so on. They are significant."

A better paragraph: "A 1% rise in retail fuel prices raises the all-income price level by {{ n.rq1_all_c0 }}% within the month (standard error {{ n.rq1_all_c0_se }}) and by {{ n.rq1_all_c12 }}% after a year (standard error {{ n.rq1_all_c12_se }}); the 90% bands exclude zero at every horizon. A 10% rise in pump prices thus makes consumer prices about {{ n.rq1_all_c12_10pct }}% higher a year later. The impact effect equals the advanced-economy average in @kpodar_liu_2022."

For a result that is mixed, say so plainly: "In the national data the gap is negative at every horizon but significant only at three, four, seven and eight months; in the regional panel it is significant from three months on. The effect shrinks and loses significance when macroeconomic controls are added."

### 23.3 Figures and tables

Show cumulative responses with their bands over all horizons in a figure, and give the estimates and standard errors at a few key horizons (for example 0, 3, 6 and 12) in a table. State the units on the axis ("percent per 1% fuel price rise"), the band level and the standard errors in the caption or note, and the sample period.

## 24. Common mistakes and a checklist

Table 12 lists the mistakes that come up most often, what goes wrong and how to avoid them.

Table: Table 12. Common mistakes with local projections.

| Mistake | What goes wrong | Fix |
|---|---|---|
| Missing months stacked together | "Lag 1" becomes a two-month lag | Reindex to a complete monthly calendar |
| Restricting the sample before building lags | The first months lose their lags | Build lags and leads first, then restrict |
| Lagging across units in a panel | Region A's lag is Region B's last month | Shift within units (`groupby`, `xtset`) |
| Too few lags with unadjusted data | Seasonality stays in the errors | 12 lags for monthly unadjusted data |
| No leads when shocks are persistent | Response overstated (Chapter 14) | Include the Teulings–Zubanov leads |
| Reading $\beta_h$ as the effect on the price level | A monthly rate is confused with a level | Report the cumulative $B_h$ |
| Plain OLS standard errors | Bands far too narrow | Newey–West; Driscoll–Kraay for panels |
| Dropping a period by deleting rows | Lags of the following months break | Exclude it through the sample mask |
| Testing many groups or horizons | Some results "significant" by chance | Report all tests; correct (Bonferroni) |
| Treating a domestic price as a pure shock | Common causes, reverse causality | Check with an outside shock and controls |

Before reporting, check that:

- the estimator recovers a known response in simulated data;
- the calendar is complete and lags are built within units;
- the sample is restricted after the lags and leads are built;
- the outcome is cumulative when the question is about the price level;
- standard errors allow for serial (and, in panels, cross-sectional) correlation;
- the number of observations falls with *h* as expected;
- all robustness checks are reported, including those that weaken the result;
- every specification choice is written down, with whether it was planned before or after seeing the results.

## 25. Exercises

Answers follow the exercises. Use the numbers in this booklet; exercises 7 and 8 need the code.

1. Using $B_{12} = {{ n.rq1_all_c12 }}$, by how much would a 20% rise in pump prices raise the all-income price level after a year?
2. Why does the number of months in Table 4 fall from {{ t.step3[0].nobs }} at *h* = 0 to {{ t.step3[12].nobs }} at *h* = 12?
3. The national gap at *h* = 6 is ${{ n.rq2_c6 }}$ with a standard error of {{ n.rq2_c6_se }}. Compute the 90% band. Is the response significant at the 10% level? Do the same for the panel estimate, ${{ n.pan_c6 }}$ with a standard error of {{ n.pan_c6_se }}.
4. Fuel prices rise 10% in month 1 and fall 5% in month 2. Using $B_0 = {{ f(t.step3[0].B_h, 3) }}$ and $B_1 = {{ f(t.step3[1].B_h, 3) }}$, what is the fuel-driven change in the all-income price level by month 2?
5. A colleague drops the year 2020 by deleting its rows before building the lags. What goes wrong, and how should it be done?
6. Why can the region indicator $G_r$ be left out of the regression when the interaction $f_{r,t} \times G_r$ is included?
7. Change `range(1, h)` to `range(1, h + 1)` in `one_horizon` and re-run the persistent-shock simulation of Section 14.3. What happens at *h* = 1?
8. Re-estimate the national model with 6 lags instead of 12 (`p=6`). Which responses change most, and why might the twelfth lag matter for unadjusted data?

### Answers

1. $20 \times {{ n.rq1_all_c12 }} = {{ f(20 * (n.rq1_all_c12|float), 2) }}$: the price level would be about {{ f(20 * (n.rq1_all_c12|float), 1) }}% higher than otherwise.
2. The outcome at *h* = 12 needs inflation twelve months after the shock date. For the last twelve shock dates in the data, that month has not happened yet, so those rows are dropped.
3. National: ${{ n.rq2_c6 }} \pm 1.645 \times {{ n.rq2_c6_se }}$ gives [{{ f(t.step5[6].nat - 1.645 * t.step5[6].nat_se, 4) }}, {{ f(t.step5[6].nat + 1.645 * t.step5[6].nat_se, 4) }}]; it includes zero, so the response is not significant at 10%. Panel: [{{ f(t.step5[6].pan - 1.645 * t.step5[6].pan_se, 4) }}, {{ f(t.step5[6].pan + 1.645 * t.step5[6].pan_se, 4) }}]; it excludes zero, so the response is significant.
4. By equation (18.1), $B_1 \times 10 + B_0 \times (-5) = {{ f(t.step3[1].B_h, 3) }} \times 10 - {{ f(t.step3[0].B_h, 3) }} \times 5 = {{ f(10 * t.step3[1].B_h - 5 * t.step3[0].B_h, 2) }}$ percentage points.
5. The first months of 2021 would take their lags from 2019, so "lag 1" of January 2021 would be December 2019. Instead, keep the rows, build the lags, and exclude 2020 from the shock dates with the sample mask (Chapter 17).
6. $G_r$ does not change over time, so it is a constant for each region and is absorbed by the region fixed effect.
7. The estimate at *h* = 1 falls from about {{ f(t.step2[1]["with"], 3) }} to close to the true {{ f(t.step2[1].true, 3) }}, because next month's shock is now held constant. The responses from *h* = 2 on hardly change.
8. With unadjusted monthly data, inflation in a month is related to the same month a year earlier; with only six lags, that seasonal pattern is left in the error, which makes the estimates noisier and can bias them if fuel shocks are also seasonal. Compare your results with the appendix row "p=6" in `output/tables/estimates.csv`.

## Glossary

Table: Table 13. Glossary.

| Term | Meaning |
|---|---|
| Autocorrelation | The correlation of a variable with its own past values |
| Band (90%) | The estimate ± 1.645 standard errors; if it excludes zero, the estimate is significant at 10% |
| Bonferroni correction | Dividing the significance level by the number of tests |
| Cumulative response ($B_h$) | The effect of a shock on the level of a variable *h* periods later; the sum of the one-period responses |
| Driscoll–Kraay standard errors | Standard errors for panels that allow correlation over time and across units |
| Elasticity | The percentage change in one variable for a 1% change in another |
| Fixed effect | A separate constant for each unit in a panel |
| Horizon (*h*) | The number of periods after the shock |
| Identification | The conditions under which an estimate measures a causal effect |
| Impulse response | The expected difference in an outcome *h* periods after a shock, compared with no shock |
| Inflation gap ($\Delta D$) | All-income inflation minus bottom-30% inflation; negative values are regressive |
| Interaction | The product of the shock and a group indicator; its coefficient is the group's extra response |
| Lag, lead | A past value (lag) or future value (lead) of a variable |
| Local projection | A regression of an outcome *h* periods ahead on today's shock and controls, run separately for each *h* |
| Log change × 100 | $100(\ln X_t - \ln X_{t-1})$, approximately the percentage change |
| Newey–West standard errors | Standard errors that allow for heteroskedasticity and serial correlation in a time series |
| Panel | Data that follow many units over time |
| Pass-through | How much of a cost change is passed on to consumer prices |
| Percentage point | The unit of a difference between two percentages |
| Progressive, regressive | A shock that raises prices more for richer (progressive) or poorer (regressive) households |
| Serial correlation | Correlation between errors in nearby periods |
| Shock | An unexpected change in a variable whose effects are traced |
| Teulings–Zubanov leads | Future shocks added as controls so that the response is to a one-time shock |
| Vector autoregression (VAR) | A system in which each variable depends on the past of all variables; responses are simulated |

# References

::: {#refs}
:::
