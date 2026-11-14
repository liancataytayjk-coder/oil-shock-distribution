---
title: "Study Kit: Who Pays for Oil Shocks?"
subtitle: "A ten-day plan, likely defense questions with answers, and tools to redo the analysis on any data"
author: "Lian Cataytay"
date: "November 2026"
---



# 1. How to use this kit

This kit prepares you to present and defend the study. You will have about ten days. The first seven days follow a study plan, one topic a day, each ending with a short self-test. The last three days are for a mock defense, the weak spots it reveals, and rest. Section 3 puts the whole study on one page. Section 4 lists the questions a panel is likely to ask, each with a short answer you can say in under a minute. Section 5 shows how to redo the analysis on another data set, in Python or Stata, in case you are asked to.

Keep four documents open while you study: the article (`paper/article.pdf`) and its online appendix (`paper/article_online_appendix.pdf`), the local projections booklet (`tutorial/lp_booklet.pdf`), and this kit. Every number below comes from the study's own output, so it matches the papers.

# 2. The study plan

**Day 1. The question and why it matters.** Read the article's introduction and Section 2 (the 15 studies). Write, in your own words and without notes, three sentences: what Kpodar and Liu (2022) found, why it might not hold in the Philippines, and what the PSA bottom-30% CPI lets you do that they could not. *Self-test:* explain the difference between a progressive and a regressive effect, and say which sign of the gap means which.

**Day 2. Data.** Read Section 4.1 and the data appendix. Open `data/clean/national_monthly.csv` and find the four series that matter: `d_fuel`, `d_cpi_all`, `d_cpi_b30` and `d_ratio`. Learn why the PSA sub-index 07.2.2 stands in for pump prices (correlation 0.87 with the World Bank pump price), why the 17 old regions are kept, and what the 2012 and 2018 splices are. *Self-test:* compute by hand $100 \ln(F_t / F_{t-1})$ for March 2026 from the `fuel` column (about 31.8).

**Day 3. The method, part one: what a local projection is.** Read booklet Chapters 1–5. Run `.venv/bin/python tutorial/lp_tutorial.py` and look at Step 1: the estimator recovers a known answer. Be able to write equation (3) of the article from memory and say what each term does. *Self-test:* why twelve lags? Why a separate regression for each horizon? What is $B_h$ and how is it estimated?

**Day 4. The method, part two: inference, leads, panels, VAR.** Read booklet Chapters 6–7 and 14, and article Sections 4.2–4.3. Understand Newey–West and Driscoll–Kraay errors, the two lead conventions and why the VAR is a check. Run `python study_kit/lp_any.py --demo`. *Self-test:* why do overlapping outcomes need special standard errors? Why do leads 1 to *h* − 1 leave a bias at *h* = 1?

**Day 5. Results for RQ1 and RQ2.** Read article Section 5 with Tables 2–6 and Figures 3–5. Memorise the key numbers in Section 3 of this kit. Practise reading Figure 4 aloud: "below zero means the poor's prices rise more". *Self-test:* why is the panel more precise than the national estimate? What does the budget-share calculation show, and why does it matter that it is positive?

**Day 6. Robustness and the 2026 application.** Read Section 5.5, Section 6 and online appendix Tables A3–A6. Be ready to say which checks weaken the result (macro controls, the 2013–2026 period) and why you report them. Work through booklet Chapter 18 (the $\sum B f$ calculation). *Self-test:* how is the PHP 467 figure computed? Why is the contribution accounting called descriptive?

**Day 7. Policy, limitations and the code.** Read Section 6.4, the conclusion, and `code/stata/README.md`. Run the Stata files if you can (`do code/stata/00_master.do`) and check `07_compare.do`'s report. *Self-test:* give the three policy lessons and the three main limitations in under two minutes.

**Day 8. Mock defense.** Ask someone to pick twenty questions from Section 4 at random. Answer aloud, timed, without notes. Mark every question you could not answer in under a minute.

**Day 9. Fix the weak spots.** Reread the sections behind the questions you marked. Redo the self-tests you found hard. Rehearse a five-minute opening summary: question, data, method, three findings, policy.

**Day 10. Light review.** Reread Section 3 of this kit and the article's abstract and conclusion. Rest.

# 3. The study on one page

**Question.** When pump prices rise, do poor Filipino households face larger price increases than the average household? Three research questions: pass-through (RQ1), who pays more and why (RQ2), the 2026 shock and policy (RQ3).

**Data.** PSA consumer price indices, monthly, 2018 = 100: all-income CPI, bottom-30% CPI, and the fuel sub-index 07.2.2, nationally and for 17 regions, January 2001–August 2026 (shock dates); 308 national months and 5,219 region-months at *h* = 0.

**Method.** Local projections (Jordà 2005) as specified by Kpodar and Liu (2022): for *h* = 0, …, 12, the sum of inflation from *t* to *t + h* on the fuel shock, 12 lags of inflation and fuel, fuel leads 1 to *h* − 1, a trend and a constant; Newey–West errors nationally; region fixed effects and Driscoll–Kraay errors in the panel; 90% bands.

**RQ1.** A 1% fuel price rise raises the all-income price level by 0.044% on impact, 0.087% after six months and 0.102% after a year; bottom 30%: 0.044, 0.095, 0.102. A 10% rise → about 1.0% higher prices a year later. Crude oil captures only about 40% of this.

**RQ2.** Gap (all minus bottom 30%), six months: national −0.0155 (0.0103), significant only at *h* = 3, 4, 7, 8; panel −0.0214 (0.0084), significant from 3 to 12 months. Twelve months: national −0.0097, panel −0.0173. Regressive, not progressive.

**Why.** Budget shares alone give +0.0101 (progressive): food −0.0124, housing +0.0092, transport +0.0108. So the within-category part is regressive, about −0.0197 (national) to −0.0274 (panel). From 2013: housing 0.182 vs 0.142, food 0.067 vs 0.055, transport 0.196 vs 0.300 (bottom 30% vs all).

**Robustness (gap, six months).** Crude −0.0093; macro controls −0.0046; excluding 2020 −0.0186; leads 1 to *h* −0.0160 (panel −0.0216); VAR −0.0219; panel 2001–2012 −0.0541 vs 2013–2026 −0.0091; leaving out a region −0.0227 to −0.0203.

**RQ3.** Model to December 2025 explains 2.55 of 4.81 (all) and 3.13 of 5.98 (bottom 30%) log points of the rise to August 2026, about half. Fuel-driven cost for a poverty-line family of five: PHP 467 a month (PHP 390–633 by region); all prices: PHP 907. Cereals: +1.67 of the +1.24-point gap.

**Policy.** Gasoline and diesel tax relief is poorly targeted; LPG relief is neutral and small (about 8% of the fuel-driven cost); fares and rice matter most for the poor; size transfers with the bottom-30% CPI.

# 4. Likely defense questions, with answers

## 4.1 Motivation and contribution

**Q1. What is your research question, in one sentence?** When retail fuel prices rise, do poor Filipino households face larger price increases than the average household, and why?

**Q2. Why does it matter?** Every response to an oil shock, such as fuel tax relief, subsidies or transfers, assumes an answer. In 2026 the government suspended the excise on LPG and kerosene but not on gasoline and diesel; the Finance Secretary was reported as calling such relief not progressive. Whether the poor pay more decides which response helps them.

**Q3. What is new compared with Kpodar and Liu (2022)?** They rebuilt income-group price indices from survey budget shares, giving every group the same price for each category, and found a progressive effect. I use the PSA's official bottom-30% CPI, which reflects what the poor buy within categories. With it the sign reverses: the effect is regressive.

**Q4. Is this a replication or a new study?** Both. The specification replicates Kpodar and Liu exactly (same lags, leads, trend, cumulative responses, 90% bands). What is new is the data (official income-group indices, by region), the decomposition of why the result differs, and the out-of-sample application to 2026.

**Q5. Why only the bottom 30% and not quintiles?** The PSA publishes a CPI only for the bottom 30% and for all households. The comparison therefore understates the difference between the poorest and the richest, which I state as a limitation.

## 4.2 Data

**Q6. Why use a CPI sub-index as the fuel price instead of actual pump prices?** The Kpodar–Abdallah retail price database is not public, and the World Bank pump price series stops in April 2025 and has no regions. The PSA sub-index 07.2.2 covers 1994–2026 for every region, and its monthly changes correlate 0.87 with the World Bank pump price and 0.99 with the PSA gasoline index. Both alternatives are used as robustness checks.

**Q7. The bottom-30% CPI before 2018 is back-calculated. Is that a problem?** It is the PSA's own back-calculation, joined at January 2012 and January 2018. I checked the splice months (the monthly gap changes more there) and added dummies for them; the result does not change (appendix Table A3).

**Q8. Why 17 regions when there are now 18?** The Negros Island Region was created in 2024, and the bottom-30% history exists only on the old 17-region map. I keep the old map and chain the new-code monthly changes for January–August 2026; the four regions whose boundaries changed are flagged, and dropping those months does not change the result.

**Q9. Why use seasonally unadjusted data?** Because the reference study does; its twelfth lag coefficient (about 0.48) shows that its data were unadjusted. The twelve lags absorb seasonality.

## 4.3 Method

**Q10. What is a local projection?** A separate OLS regression for each horizon *h*: the outcome *h* months ahead on today's shock, holding the past constant. The coefficient on the shock is the impulse response at that horizon (Jordà 2005).

**Q11. Why not a VAR?** A VAR simulates one estimated system forward, so errors compound across horizons; a local projection estimates each horizon directly and is easy to extend to panels and interactions. Both estimate the same impulse response in large samples (Plagborg-Møller and Wolf 2021), and I report a VAR as a check: it gives the same sign.

**Q12. Explain each term of your equation.** Today's fuel shock (its coefficient is the response); twelve lags of inflation (persistence and seasonality); twelve lags of fuel (delayed effects of earlier shocks); leads of fuel between *t* and *t + h* (effects of later shocks that follow a first one); a trend and a constant (slow drifts).

**Q13. What are the Teulings–Zubanov leads for?** Fuel shocks come in runs: a rise this month predicts a rise next month (autocorrelation 0.39). Without leads, today's shock gets the credit for later shocks. Holding the future shocks constant makes the response that of a one-time shock.

**Q14. Why leads 1 to *h* − 1 and not 1 to *h*?** Because the reference study's annex tables use 1 to *h* − 1 and I replicate it. With 1 to *h* − 1 the lead set is empty at *h* = 1, which overstates the one-month response; that is the zig-zag at months 1 and 2. I report Teulings and Zubanov's own convention as a robustness check: it removes the zig-zag and changes the six-month results only in the third decimal (0.087 → 0.088; gap −0.0155 → −0.0160).

**Q15. What is the cumulative response and how is it estimated?** $B_h = \beta_0 + \dots + \beta_h$, the effect on the price level after *h* months. I estimate it directly by putting the sum of inflation from *t* to *t + h* on the left, so it comes with its own standard error.

**Q16. Why Newey–West standard errors with *h* + 1 lags?** The outcome *h* months ahead overlaps with the outcomes of neighbouring months, so the errors are serially correlated even if the model is right. Newey–West allows for that correlation up to *h* + 1 months.

**Q17. Why Driscoll–Kraay in the panel?** All regions are hit by the same national events in the same month, so errors are correlated across regions as well as over time. Driscoll–Kraay errors allow both.

**Q18. Why region fixed effects? Is there a Nickell bias?** Fixed effects absorb everything about a region that does not change, such as its average gap. With lagged outcomes they cause a bias of order 1/*T*; with about 300 months per region it is negligible.

**Q19. Is your estimate causal?** It is causal if, given the controls, the fuel shock is unrelated to other things that move prices. A domestic pump price could respond to the exchange rate or demand. I check with Dubai crude in pesos, a world price (same sign), and with macroeconomic controls (smaller and not significant). A pure oil supply shock (Kilian 2009; Känzig 2021) would strengthen the causal reading; that is an extension.

**Q20. How do you know your code is right?** The estimator recovers known responses in simulated data (automated tests); the hand-made regressions in the tutorial match the project's estimator exactly; and the Stata code re-estimates every result and compares it with Python.

## 4.4 Results

**Q21. Interpret 0.102.** If pump prices rise 1% this month and nothing else unusual happens, consumer prices are 0.102% higher a year later than they would otherwise be. A 10% rise means about 1.0% higher prices.

**Q22. Your national gap is not significant at six months. How can you claim a regressive effect?** Nationally the sign is negative at every horizon but the estimate is imprecise: significant only at 3, 4, 7, 8 months. The panel uses 17 times as many observations and each region's own fuel prices; it gives −0.0214 with standard error 0.0084, significant from 3 to 12 months. I claim the effect is regressive, clearly in the panel and in sign nationally, and that it is not progressive.

**Q23. How big is the gap in practice?** A 10% fuel price rise raises the poor's price level about 0.2 percentage points more than the average after six months, on top of a total rise of about 0.9%. Small per shock, but it accumulates over many shocks: the cumulative gap reached −13.3 log points by 2025.

**Q24. Why do the poor pay more if they buy less fuel?** Because of what happens within categories. If both groups paid the same price changes within each division, budget shares alone would make the effect progressive (+0.0101): food pushes it toward regressive (−0.0124), but housing (+0.0092) and transport (+0.0108) push the other way. The estimated gap is negative, so the items the poor buy within food and utilities must rise more; the bottom-30% division indices from 2013 confirm it.

**Q25. Is that decomposition causal?** No. It is an accounting exercise outside the model, and I label it descriptive. It shows that budget shares cannot produce the observed sign, which rules out one explanation; the 2013–2026 comparison of the two baskets is exploratory.

**Q26. Why can you not decompose the 2008 episode?** The bottom-30% item indices start only in 2013, so the largest gap in the data, during the 2008 rice crisis, cannot be broken down by item.

## 4.5 Robustness

**Q27. Which checks weaken your result, and why report them?** Two. With exchange-rate, policy-rate and world food price controls the six-month gap falls to −0.0046 and loses significance; and the effect is concentrated in 2001–2012 (−0.0541) rather than 2013–2026 (−0.0091). I report them in the main text because leaving them out would be cherry-picking.

**Q28. Does one region drive the panel result?** No. Leaving out each region in turn keeps the six-month gap between −0.0227 and −0.0203.

**Q29. Do regions differ?** I tested poorer, more food-dependent, Mindanao and island regions. No difference survives a Bonferroni correction for testing four groups, so I do not claim regional differences in the gap; the regional estimates matter for pricing the 2026 cost.

**Q30. Why does the VAR give a larger response?** The standard VAR response includes the further fuel price rises that tend to follow a first one, as does the local projection without leads; the two match (0.113 and 0.115 at six months). The baseline holds later shocks constant, so it is smaller. All versions give a negative gap.

**Q31. What else did you try?** 6 and 18 lags; gasoline and the World Bank pump price as shocks; dropping 2020, 2026, 2008 or the months after June 2019; splice dummies; separate effects of increases and decreases. Appendix Table A3 lists them all.

## 4.6 The 2026 application and policy

**Q32. How did you test the model on 2026?** I estimated the responses using data only to December 2025, then applied them to the actual fuel price changes of January–August 2026: the fuel-driven change in month *m* is $\sum_s B_{m-s} f_s$. It explains about half of the price rise and predicts that the poor pay more.

**Q33. Why only half?** The model gives the average response of past shocks. The 2026 surge also carried a large rice price increase (fertiliser, freight, import policy) and prices did not fall when fuel eased in May–June. Contribution accounting shows cereals contributed +1.67 points of the poor's +1.24-point excess inflation.

**Q34. How did you compute the peso cost?** The fuel-driven rise in the bottom-30% CPI (3.13 log points) times the poverty line for a family of five (about PHP 14,714 a month at December 2025 prices): $14{,}714 \times (e^{3.13/100} - 1) \approx$ PHP 467. Following Deaton (1989), the rise in a group's CPI approximates the extra spending needed to buy the same basket.

**Q35. Which policies do you recommend?** Do not use broad gasoline and diesel tax relief to protect the poor: motor fuel is 1.59% of their basket. LPG relief is neutral and small. Fares and rice matter most for the poor. Size transfers with the bottom-30% CPI, PHP 467–907 a month for a poverty-line family, and keep them for at least a year.

**Q36. What should the central bank take from this?** Retail fuel prices, not crude prices, measure the inflationary impulse, and it builds over at least a year. Monetary policy addresses the price level, not the gap between groups.

## 4.7 Limitations and extensions

**Q37. What are the main limitations?** The shock is a domestic price; the comparison is bottom 30% against all households, not poorest against richest; pre-2018 bottom-30% series are back-calculated; the effect is concentrated in 2001–2012 and weakens with controls; the decompositions are descriptive; the 2026 analysis covers eight months; price indices ignore substitution.

**Q38. What would you do next?** Identify a pure oil supply shock (Känzig-type surprises) and use it as an instrument; extend to provinces; add household survey data to separate net rice sellers from buyers; study fares and rice policy directly.

**Q39. If you had to redo the analysis on another country or another shock, how?** Put the outcome and the shock as monthly log changes in a CSV file and run `lp_any.py` (Section 5). It applies the same specification and the same safeguards.

**Q40. What did you learn about the method itself?** That details matter: building lags before restricting the sample, using cumulative outcomes for price levels, correcting standard errors for overlap, and checking the lead convention. Each changes the answer if done wrong.

# 5. Redoing the analysis on other data

## 5.1 In Python

`study_kit/lp_any.py` runs the study's specification on any CSV file. The outcome and shock should be monthly changes (100 × Δln of an index). It completes the calendar, builds lags and leads within units, restricts the sample after building them, and writes a table, a CSV file and a figure.

```bash
# one series
.venv/bin/python study_kit/lp_any.py data/clean/national_monthly.csv \
    --y d_cpi_all --x d_fuel --time date --start 2001-01-01 --out rq1
# a panel (unit fixed effects, Driscoll-Kraay errors)
.venv/bin/python study_kit/lp_any.py data/clean/regional_panel.csv \
    --y d_ratio --x d_fuel --time date --unit region --start 2001-01-01 --out gap
# simulated data with a known answer (prints the true response next to the estimate)
.venv/bin/python study_kit/lp_any.py --demo
```

Options: `--horizons 12`, `--lags 12`, `--leads paper|full|none`, `--controls a,b`, `--onemonth` (outcome at *t + h* only), `--start` and `--end` (shock dates), `--se newey_west|driscoll_kraay|cluster|robust`, `--noplot`. On the study's data it reproduces the published estimates exactly.

## 5.2 In Stata

`study_kit/lp_any.do` loads the study's estimator (`code/stata/02_lp_program.do`), then runs it on a data set you name in five marked lines: the file, the time variable, the outcome, the shock and the sample. It lists the responses with 90% bands, saves a CSV file and draws the figure.

## 5.3 A checklist for a new data set

Before you trust the result: make sure the time variable is regular and complete; express the outcome and shock as monthly changes; check that the estimator recovers a known answer on simulated data (`--demo`); use cumulative outcomes for questions about price levels; check that the number of observations falls by one for each horizon; and report the robustness checks that weaken the result as well as those that support it.
