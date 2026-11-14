---
title: "Local Projections, Step by Step"
subtitle: "Theory, code, implementation and interpretation, with the Philippine fuel pass-through study as the worked example"
author: "Lian Cataytay"
date: "November 2026"
---

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Contents {.unnumbered}

QQL1QQAbout this bookletQQTABQQ3

QQL1QQPart I. TheoryQQTABQQ4

QQL2QQ1. The question: what an impulse response isQQTABQQ4

QQL2QQ2. Two ways to estimate an impulse responseQQTABQQ5

QQL2QQ3. The specification of the study, term by termQQTABQQ7

QQL2QQ4. Leads: the Teulings–Zubanov correctionQQTABQQ9

QQL2QQ5. From monthly effects to the price level: cumulative responsesQQTABQQ10

QQL2QQ6. How precise is the answer? Standard errors and bandsQQTABQQ11

QQL2QQ7. Panels: many regions in one regressionQQTABQQ12

QQL2QQ8. When is the response causal?QQTABQQ13

QQL1QQPart II. Implementation, step by stepQQTABQQ14

QQL2QQ9. Setting up and getting to know the dataQQTABQQ14

QQL2QQ10. Step 1: preparing the dataQQTABQQ15

QQL2QQ11. Step 2: one horizon by handQQTABQQ16

QQL2QQ12. Step 3: all horizons and the cumulative responseQQTABQQ17

QQL2QQ13. Step 4: bands and the figureQQTABQQ18

QQL2QQ14. Step 5: checking the estimator on simulated dataQQTABQQ20

QQL2QQ15. Step 6: the study's estimatorQQTABQQ22

QQL2QQ16. Step 7: the regional panelQQTABQQ23

QQL2QQ17. Step 8: robustness checks in codeQQTABQQ25

QQL2QQ18. Step 9: applying the responses to an episodeQQTABQQ26

QQL2QQ19. Step 10: the same in StataQQTABQQ27

QQL1QQPart III. InterpretationQQTABQQ29

QQL2QQ20. Reading a responseQQTABQQ29

QQL2QQ21. Interpreting the study's resultsQQTABQQ29

QQL2QQ22. The lead convention: what it changesQQTABQQ32

QQL2QQ23. Writing up the resultsQQTABQQ33

QQL2QQ24. Common mistakes and a checklistQQTABQQ34

QQL2QQ25. ExercisesQQTABQQ34

QQL2QQGlossaryQQTABQQ35

QQL1QQReferencesQQTABQQ36

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# About this booklet

This booklet teaches one econometric tool, the *local projection*, from the first idea to the last sentence of a results section. It uses a real study as its running example: the author's study of how retail fuel prices pass through to the inflation of poor households in the Philippines, which replicates the design of @kpodar_liu_2022 on Philippine data. Every number in the booklet comes from a script that runs on the study's own data, so you can reproduce each one yourself.

The booklet has three parts. Part I explains the theory: what question a local projection answers, why it works, what each term in the regression does, and how to judge how precise the answer is. Part II implements the method step by step in Python, first by hand and then with the study's own estimator, and shows the same steps in Stata. Part III explains how to read and report the results, using the study's three research questions as worked examples, and ends with a list of common mistakes, a checklist, exercises with answers and a glossary.

You need only basic regression: what ordinary least squares (OLS) does, what a coefficient and a standard error mean, and how to read a confidence interval. Every other term is defined the first time it is used, first in words, then as a formula, then with an example. A short glossary at the end collects the definitions.

To follow the code, open the study's repository and run, from its top folder,

```bash
.venv/bin/python tutorial/lp_tutorial.py
.venv/bin/python tutorial/build_booklet.py
```

The first command prints seven tables, one for each step in Part II, writes the figures to `tutorial/figures/` and saves every number to `tutorial/tutorial_numbers.json`. The second command reads those numbers and the study's results (`output/tables/paper_numbers.json`) and writes this booklet. The shorter, web version of the same material is `tutorial/README.md`.

Three conventions are used throughout. A *month* is indexed by *t*. A *log change* times 100, $100\,\Delta \ln X_t = 100(\ln X_t - \ln X_{t-1})$, is used as the monthly percentage change; for small changes the two are almost equal (a rise from 100 to 101 is a log change of 0.995). And all confidence bands are 90% bands, as in the reference study.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part I. Theory

## 1. The question: what an impulse response is

Suppose the price of gasoline and diesel at the pump rises by 1% this month. How much higher will consumer prices be next month? In three months? In a year? And how much higher compared with what? The answer is always *compared with what would have happened without the rise*. That comparison is the heart of the method, so it is worth stating carefully.

**The shock.** A *shock* is an unexpected change in one variable that we want to trace through the economy. In the study the shock is the monthly percentage change in the retail fuel price, measured by the Philippine Statistics Authority (PSA) consumer price sub-index 07.2.2, "fuels and lubricants for personal transport". If $F_t$ is that index in month *t*, the shock is

$$f_t = 100\,\Delta \ln F_t = 100\,(\ln F_t - \ln F_{t-1}). \qquad\qquad (1.1)$$

For example, in March 2026 the index rose from 120.5 to 165.6, so $f_t = 100 \ln(165.6/120.5) \approx 31.8$: a fuel shock of about 32%.

**The outcome.** The *outcome* is the variable whose reaction we want to measure. In the study it is monthly inflation of a consumer price index (CPI) $P_t$,

$$\pi_t = 100\,\Delta \ln P_t, \qquad\qquad (1.2)$$

for all households ("all income") and for the bottom 30% of households by income.

**The horizon.** The *horizon* *h* is the number of months after the shock: *h* = 0 is the month of the shock itself, *h* = 1 the next month, and so on up to *h* = 12 in the study.

**The impulse response.** The *impulse response* at horizon *h* is the expected difference in the outcome *h* months later between a world in which the shock happens and one in which it does not, everything else in the past being the same. In symbols, for a shock of size one,

$$\text{IR}_h = E\left[\pi_{t+h} \mid f_t = 1, \mathcal{H}_{t-1}\right] - E\left[\pi_{t+h} \mid f_t = 0, \mathcal{H}_{t-1}\right], \qquad\qquad (1.3)$$

where $E[\cdot]$ is an expected value and $\mathcal{H}_{t-1}$ ("the history") is everything known up to the month before the shock. The list $\text{IR}_0, \text{IR}_1, \dots, \text{IR}_{12}$ is called the impulse response *function*. It is the standard way economists describe how a shock, or "impulse", spreads over time.

**Example.** In the study, the impulse response of all-income prices to the fuel shock is about 0.044 in the month of the shock. This means that if pump prices rise by 1% this month, consumer prices are expected to be 0.044% higher this month than they would otherwise have been.

Why can we not read this off one simple regression of inflation on fuel prices? For two reasons. First, the effect *unfolds over time*: pump prices raise transport fares and the cost of moving food within weeks, but other prices adjust over months. Second, both series *depend on their own past*. Inflation is persistent, and fuel price rises tend to come in runs, so a same-month correlation mixes today's shock with older and later ones. A local projection handles both problems with nothing more than OLS.

## 2. Two ways to estimate an impulse response

### 2.1 The vector autoregression

The traditional tool is the *vector autoregression* (VAR) of @sims_1980. A VAR is a system of regressions in which each variable is explained by the past values of all the variables in the system. Once the system is estimated, the impulse response is obtained by *simulating* it forward: give it a shock in month *t*, compute what it implies for *t* + 1, feed that into the equations to get *t* + 2, and so on. Every horizon therefore depends on the whole system being correctly specified, and a small error in the equations is compounded at each step of the simulation.

### 2.2 The local projection

@jorda_2005 proposed a more direct route. To find the effect *h* months ahead, *regress the outcome h months ahead directly on today's shock*, holding the past constant. Do this separately for each horizon *h* = 0, 1, …, 12. Each regression is an ordinary OLS regression, and the coefficient on today's shock *is* the impulse response at that horizon. The word "local" means that each regression only has to describe one horizon well; the word "projection" is the statistical name for the best linear prediction that OLS delivers.

### 2.3 A small example that shows why it works

Consider a simple economy in which inflation depends on its own last value and on the shock:

$$y_t = \rho\, y_{t-1} + b\, x_t + e_t, \qquad\qquad (2.1)$$

where $x_t$ is a shock that is unrelated to everything in the past and $e_t$ is noise. If $x_t$ rises by one unit, $y_t$ rises by *b*. Next month, $y_{t+1} = \rho y_t + \dots$, so the effect is $\rho b$; the month after it is $\rho^2 b$, and in general

$$\text{IR}_h = \rho^h\, b. \qquad\qquad (2.2)$$

A VAR would estimate $\rho$ and *b* once and compute $\hat\rho^h \hat b$. A local projection instead substitutes equation (2.1) into itself *h* times, which gives

$$y_{t+h} = \rho^{h+1} y_{t-1} + \rho^h b\, x_t + \left(b\,x_{t+h} + \rho b\, x_{t+h-1} + \dots + \rho^{h-1} b\, x_{t+1}\right) + \text{noise}. \qquad\qquad (2.3)$$

The future shocks in brackets are unrelated to $x_t$, so a regression of $y_{t+h}$ on $x_t$ and $y_{t-1}$ gives a coefficient on $x_t$ that estimates $\rho^h b$ directly: the impulse response at horizon *h*. Nothing has to be simulated. This is the whole idea. In real applications the model is richer than (2.1), but the logic is the same: put the outcome at *t* + *h* on the left, today's shock and enough of the past on the right, and read the response off the shock's coefficient.

### 2.4 Which one to use

Table 1 compares the two tools. With enough lags, both estimate the same impulse response in large samples [@plagborg_wolf_2021]. In samples of realistic size they trade off differently: local projections tend to have less bias but more variance than VARs, especially at long horizons [@li_plagborg_wolf_2024]. Local projections are popular in applied work because they are easy to extend: controls, interactions, panels of regions and nonlinear terms enter as in any OLS regression [@jorda_2023].

Table: Table 1. Vector autoregression and local projection compared.

| | Vector autoregression | Local projection |
|---|---|---|
| How the response at horizon *h* is obtained | Simulate one estimated system forward *h* steps | Estimate a separate regression for horizon *h* |
| If the model is misspecified | Errors compound across horizons | Each horizon stands on its own |
| Precision at long horizons | Higher, if the model is right | Lower |
| Adding controls, interactions, panels | Harder | Easy, as in any OLS regression |
| Large-sample target | The same impulse response | The same impulse response |

Figure 1 shows the idea graphically, using the study's own data.

![Figure 1. How a local projection works: (a) what one regression uses; (b) one regression per horizon.](output/figures/fig02_local_projection.png){width=95%}

## 3. The specification of the study, term by term

### 3.1 The equation

For each horizon *h* = 0, …, 12, the study estimates the specification of @kpodar_liu_2022:

$$\pi_{t+h} = \alpha_h + \beta_h f_t + \sum_{q=1}^{12} \gamma_{q}\, \pi_{t-q} + \sum_{q=1}^{12} \lambda_{q}\, f_{t-q} + \sum_{l=1}^{h-1} \rho_{l}\, f_{t+l} + \delta_h\, t + \varepsilon_{t+h}. \qquad\qquad (3.1)$$

It looks long, but each term has one job. Table 2 lists them. Every coefficient carries an *h* subscript (left off the sums to keep the equation readable) because each horizon is a *separate* regression with its own coefficients.

Table: Table 2. The terms of equation (3.1).

| Term | What it is | Why it is there |
|---|---|---|
| $\pi_{t+h}$ | Inflation *h* months after the shock | The outcome whose reaction we trace |
| $\beta_h f_t$ | Today's fuel shock | $\beta_h$ is the impulse response at horizon *h* |
| $\sum \gamma_q \pi_{t-q}$ | Twelve past months of inflation | Holds the history of prices constant; the twelfth lag also absorbs seasonal patterns |
| $\sum \lambda_q f_{t-q}$ | Twelve past fuel shocks | Removes the delayed effects of *earlier* shocks |
| $\sum \rho_l f_{t+l}$ | Fuel shocks between *t* and *t* + *h* (the "leads") | Removes the effects of *later* shocks that tend to follow today's (Chapter 4) |
| $\alpha_h$, $\delta_h t$ | Constant and linear time trend | Absorb a constant level and slow drifts |
| $\varepsilon_{t+h}$ | Error | Everything else; correlated across neighbouring months (Chapter 6) |

### 3.2 Lags and leads

A *lag* is a past value of a variable: the first lag of $\pi_t$ is $\pi_{t-1}$, the twelfth is $\pi_{t-12}$. A *lead* is a future value: the first lead of $f_t$ is $f_{t+1}$. In a data set with one row per month, a lag is the same column shifted down by one row and a lead is the column shifted up. Part II shows how to build them.

### 3.3 Why twelve lags

The study uses the CPI as published, without seasonal adjustment. *Seasonal adjustment* removes regular calendar patterns, such as higher food prices every December. Without it, inflation in a given month is strongly related to inflation in the same month a year earlier. Twelve lags include that month ($\pi_{t-12}$), so the regression absorbs the seasonal pattern itself. The reference study's annex tables show a large coefficient (about 0.48) on the twelfth lag, which confirms that its data were also unadjusted (decision D2 in the study's decisions log).

### 3.4 Units: how to read a coefficient

Both $f_t$ and $\pi_t$ are log changes times 100, so both are in percent. A coefficient $\beta_h = 0.044$ therefore means: a 1% rise in fuel prices raises inflation in month *t* + *h* by 0.044 *percentage points*. A *percentage point* is the unit of a difference between two percentages: if inflation rises from 0.30% to 0.344% in a month, it has risen by 0.044 percentage points. To scale the response to a realistic shock, multiply: a 10% fuel price rise raises inflation by $10 \times 0.044 = 0.44$ percentage points in the same month.

### 3.5 The outcome for "who pays more": the inflation gap

The study's second research question asks whether the bottom 30% face larger price increases than all households. Its outcome is the change in the *inflation gap*. Let $P^A_t$ be the all-income CPI and $P^B_t$ the bottom-30% CPI. The gap is the log ratio of the two indices times 100, and its monthly change is the difference between the two inflation rates:

$$D_t = 100 \ln\left(P^A_t / P^B_t\right), \qquad \Delta D_t = \pi^A_t - \pi^B_t. \qquad\qquad (3.2)$$

If a fuel shock raises the prices of the poor by more than those of all households, $\Delta D$ falls, and the response of $\Delta D$ is negative. The study calls a negative response *regressive* (the poor pay relatively more) and a positive one *progressive* (the better-off pay relatively more). For example, if six months after a 1% fuel shock the all-income price level is 0.08% higher and the bottom-30% price level is 0.10% higher, the cumulative response of the gap is $0.08 - 0.10 = -0.02$: regressive.

## 4. Leads: the Teulings–Zubanov correction

### 4.1 The problem

Fuel price shocks are not one-off events. In the study's data (2001–2026) the monthly fuel shock has a first-order *autocorrelation*, the correlation between a variable and its own previous value, of 0.39. A rise this month therefore *predicts* a rise next month, and next month's rise has its own effect on prices. A regression of $\pi_{t+h}$ on $f_t$ alone gives today's shock the credit for the later shocks it predicts.

### 4.2 The fix

@teulings_zubanov_2014 proposed adding the shocks between *t* and *t* + *h* to the regression. Once they are held constant, $\beta_h$ measures the effect of a *one-time* shock. To see why, return to the small example of Section 2.3 but let the shock be persistent: $x_{t+1} = a\, x_t + u_{t+1}$, where $u$ is new noise. Equation (2.3) contains $b\, x_{t+1}$ when *h* = 1. Since $x_{t+1}$ is correlated with $x_t$, a regression without $x_{t+1}$ picks up part of its effect, and the estimated response at *h* = 1 becomes about $\rho b + a b$ instead of $\rho b$. Adding $x_{t+1}$ as a control removes the extra $ab$.

### 4.3 Two conventions

The original correction includes the leads $f_{t+1}, \dots, f_{t+h}$. The reference study's annex tables instead use $f_{t+1}, \dots, f_{t+h-1}$: there is no lead at *h* = 0 or 1, and "lead 1" first appears at *h* = 2. The study follows the reference study (decision D4). The difference matters only at short horizons. With the reference convention, the lead set is empty at *h* = 1, so next month's shock is not held constant and the response at *h* = 1 is overstated when shocks are persistent. From *h* = 2 on, the lead $f_{t+1}$ is in the regression, and when the shock process is close to a first-order autoregression, as in the example above, holding $f_{t+1}$ constant is enough. Chapter 14 shows both effects in simulated data and Chapter 22 shows what this means for the study's results.

## 5. From monthly effects to the price level: cumulative responses

### 5.1 Definition

$\beta_h$ is the effect on inflation *in one month*, month *t* + *h*. Policy questions are usually about the *price level*: how much higher are prices a year after the shock? That is the *cumulative response*, the sum of the monthly effects up to *h*:

$$B_h = \beta_0 + \beta_1 + \dots + \beta_h. \qquad\qquad (5.1)$$

Because inflation is the change in the log price level, the sum of inflation from *t* to *t* + *h* is the change in the log price level over that period: $\sum_{j=0}^{h} \pi_{t+j} = 100\,(\ln P_{t+h} - \ln P_{t-1})$. So $B_h$ is the percentage effect of the shock on the price level *h* months later.

**Example.** For the all-income CPI, the study finds $B_{12} = 0.102$. A 10% rise in pump prices therefore makes consumer prices about $10 \times 0.102 \approx 1.0$% higher a year later than they would otherwise have been.

### 5.2 Estimating it directly

The running sum of the estimated $\hat\beta$'s gives $B_h$, but not its standard error, because the $\hat\beta$'s from different regressions are correlated. The simple solution is to estimate $B_h$ directly, by putting the *sum* of inflation on the left-hand side:

$$\sum_{j=0}^{h} \pi_{t+j} = \alpha_h + B_h f_t + (\text{the same lags, leads and trend}) + u_{t+h}. \qquad\qquad (5.2)$$

The coefficient on $f_t$ is $B_h$, and its standard error comes with the regression. In a finite sample the running sum and the direct estimate are not identical, because each horizon's regression uses a slightly different set of months; Chapter 12 shows the difference in the study's data. The study reports the direct estimates.

## 6. How precise is the answer? Standard errors and bands

### 6.1 Why ordinary standard errors are wrong here

The error $\varepsilon_{t+h}$ in equation (3.1) contains everything that happens between *t* and *t* + *h* that the regression does not hold constant. The error for month *t* and the error for month *t* + 1 share most of those events, so they are correlated. This is called *serial correlation*. It is present even when the model is right, and it is stronger for cumulative outcomes, which overlap by construction: the sum from *t* to *t* + 6 and the sum from *t* + 1 to *t* + 7 share six of their seven months. Ordinary OLS standard errors assume no serial correlation and are therefore too small.

### 6.2 Newey–West standard errors

A *heteroskedasticity- and autocorrelation-consistent* (HAC) standard error allows the errors to have different variances (heteroskedasticity) and to be correlated with nearby errors (autocorrelation). The most common one is that of @newey_west_1987. In words, it adds to the usual variance formula the covariances between each error and the errors up to *L* months away, with weights that fall linearly as the distance grows. In symbols, with regressors $x_t$ and residuals $\hat\varepsilon_t$,

$$\widehat{V}(\hat\beta) = (X'X)^{-1}\, \widehat{S}\, (X'X)^{-1}, \qquad \widehat{S} = \sum_t \hat\varepsilon_t^2\, x_t x_t' + \sum_{l=1}^{L} \left(1 - \frac{l}{L+1}\right) \sum_t \hat\varepsilon_t \hat\varepsilon_{t-l} \left(x_t x_{t-l}' + x_{t-l} x_t'\right). \qquad\qquad (6.1)$$

The study sets the number of lags to *L* = *h* + 1, because an outcome *h* months ahead overlaps with the outcomes of about *h* neighbouring months.

### 6.3 Driscoll–Kraay standard errors for panels

When the 17 regions are stacked into one regression (Chapter 7), a further problem appears. All regions are hit by the same national events in the same month: a typhoon, a rice import ban, a change in the exchange rate. Their errors are therefore correlated *across regions* within a month, as well as over time. @driscoll_kraay_1998 solve this in two steps: first add up each month's contributions across all regions into a single monthly series, then apply the Newey–West formula to that series. Correlation of any form across regions within a month is then allowed automatically. The study again uses *h* + 1 lags.

### 6.4 Bands and significance

The study reports 90% *confidence bands*: $\hat\beta_h \pm 1.645 \times \text{s.e.}(\hat\beta_h)$, where 1.645 is the value that leaves 5% in each tail of the normal distribution. If the band excludes zero, the response is *statistically significant* at the 10% level. For example, the national gap at *h* = 6 is $−0.0155$ with a standard error of 0.0103; the *t*-statistic is $−1.50$, smaller than 1.645 in absolute value, so the response is not significant at the 10% level.

@montiel_olea_plagborg_2021 show that when a local projection includes lags of the outcome and the shock, as equation (3.1) does, inference is more robust than had been thought, and even simple heteroskedasticity-robust errors often give correct bands. The study keeps the more conservative Newey–West and Driscoll–Kraay errors of the reference study.

### 6.5 Many tests

A response function has 13 horizons, and a study may test several outcomes and groups. With many tests, some will look significant by chance. With 13 independent tests at the 10% level, about one would be expected to be "significant" even if the true effect were zero. Two habits help. First, judge a response by its whole shape, not by isolated significant horizons. Second, when testing several groups, correct the significance level; the simplest correction, the *Bonferroni correction*, divides the level by the number of tests (four groups at 10% gives 2.5% each). The study does this for its four region-group interactions.

## 7. Panels: many regions in one regression

### 7.1 Stacking regions

The PSA publishes the CPIs for all 17 regions, so the same equation can be estimated with 17 times as many observations. A *panel* is a data set that follows many units (here regions, indexed by *r*) over time. The panel version of equation (3.1) for the inflation gap is

$$\Delta D_{r,t+h} = u_{r,h} + \beta_h f_{r,t} + \sum_{q=1}^{12} \gamma_{q} \Delta D_{r,t-q} + \sum_{q=1}^{12} \lambda_{q} f_{r,t-q} + \sum_{l=1}^{h-1} \rho_{l} f_{r,t+l} + \delta_h t + \varepsilon_{r,t+h}, \qquad\qquad (7.1)$$

where each region has its own outcome and its own fuel index, and $u_{r,h}$ is a region fixed effect.

### 7.2 Fixed effects

A *fixed effect* is a separate constant for each unit. It absorbs everything about a region that does not change over time: its average inflation gap, its distance from Manila, its typical diet. The estimator subtracts each region's own average from every variable (the *within transformation*), so $\beta_h$ is estimated only from how each region's gap moves when its own fuel prices move. With lagged outcomes on the right, fixed effects cause a small bias of order 1/*T*, where *T* is the number of months [@nickell_1981]; with about 300 months per region it is negligible.

### 7.3 Interactions: do some regions respond differently?

To test whether a group of regions responds differently, add the product of the shock and a group indicator. Let $G_r = 1$ for regions in Mindanao and 0 otherwise. The regression then includes $\theta_h\, (f_{r,t} \times G_r)$. The response is $\beta_h$ outside Mindanao and $\beta_h + \theta_h$ in Mindanao, so $\theta_h$ is the *extra* response in the group, and its *t*-statistic tests whether the groups differ. The indicator itself is not needed, because it never changes over time and is absorbed by the fixed effects.

## 8. When is the response causal?

A local projection measures a *causal* effect only if the shock, given the controls, is unrelated to everything else that moves the outcome. This is called *identification*. In the study, $f_t$ is a domestic retail price, not a pure outside event. Three things could break identification. First, *common causes*: a depreciation of the peso raises both pump prices and the prices of imported food, so part of the estimated fuel effect could be an exchange-rate effect. Second, *reverse causality*: strong demand at home can push up both inflation and fuel margins. Third, *different kinds of oil shocks*: oil prices rise for different reasons, such as a supply cut or strong world demand, and their effects differ [@kilian_2009].

The study does not claim a perfect natural experiment. Instead, it checks how sensitive the results are, as the reference study does. It replaces the domestic fuel index with Dubai crude oil in pesos, a price set in world markets; it adds controls for the exchange rate, the policy interest rate and world food prices; and it drops 2020, the year of the pandemic. These are the core robustness checks; Chapter 17 shows how to run them and Chapter 21 how to read them. A good write-up states which threats remain and how the checks address them.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part II. Implementation, step by step

## 9. Setting up and getting to know the data

### 9.1 Software

The code uses Python 3.11 with four libraries: `pandas` for data tables, `numpy` for arithmetic, `statsmodels` for OLS with Newey–West errors and `linearmodels` for panels with Driscoll–Kraay errors (plus `matplotlib` for figures). In the study's repository they are already installed in the virtual environment `.venv`; elsewhere, run `pip install -r requirements.txt`. Chapter 19 gives the Stata equivalents.

### 9.2 The two data files

The study's cleaning script writes two files that contain everything needed here. `data/clean/national_monthly.csv` has one row per month from January 1994 to August 2026. `data/clean/regional_panel.csv` has one row per region and month, for 17 regions. Table 3 lists the columns used in this booklet.

Table: Table 3. Columns used in this booklet.

| Column | Meaning | Units |
|---|---|---|
| `date`, `date_str` | First day of the month; the same as text (for example 2026-03) | Date |
| `t` | Month counter, 0 in January 1994; used as the time trend | Integer |
| `region` | Region code (panel only) | Text |
| `fuel`, `cpi_all`, `cpi_b30` | Fuel index (07.2.2), all-income CPI and bottom-30% CPI | Index, 2018 = 100 |
| `d_fuel` | Fuel shock, $f_t = 100\,\Delta\ln$ `fuel` | Percent |
| `d_cpi_all`, `d_cpi_b30` | Monthly inflation, all income and bottom 30% | Percent |
| `d_ratio` | Change in the inflation gap, $\Delta D_t = \pi^A_t - \pi^B_t$ | Percentage points |
| `d_dubai_php` | Change in Dubai crude oil in pesos (robustness) | Percent |
| `d_php_usd`, `d_policy_rate`, `d_ffpi` | Peso–dollar rate, policy rate and world food prices (controls) | Percent or points |

### 9.3 Load and look

Always look at the data before estimating. The following lines load the national file, sort it by month and print a few rows and summary statistics.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

nat = pd.read_csv("data/clean/national_monthly.csv",
                  parse_dates=["date"])
nat = nat.sort_values("date").reset_index(drop=True)
print(nat[["date_str", "fuel", "d_fuel", "d_cpi_all"]].tail())
print(nat[["d_fuel", "d_cpi_all", "d_cpi_b30"]].describe())
```

The fuel shock is far more volatile than inflation: monthly fuel changes of 10% or more are common, while monthly inflation rarely exceeds 1%. That is why the coefficients in this study are small numbers such as 0.044: they are responses to a 1% fuel change.

## 10. Step 1: preparing the data

The data files already contain the shocks and outcomes, but it is worth knowing how to make them, and checking them.

### 10.1 Making the variables

The shock and the outcome are log changes times 100 of the index levels (equations 1.1 and 1.2). The gap is the difference between the two inflation rates (equation 3.2).

```python
nat["my_fuel"] = 100 * np.log(nat["fuel"]).diff()
nat["my_pi"] = 100 * np.log(nat["cpi_all"]).diff()
nat["my_gap"] = (100 * np.log(nat["cpi_all"]).diff()
                 - 100 * np.log(nat["cpi_b30"]).diff())
# they match the columns in the file
print((nat["my_fuel"] - nat["d_fuel"]).abs().max())
```

### 10.2 Checking the calendar

A lag must be exactly one month. If a month were missing and the rows simply stacked, "the previous row" would be two months back, and every lag would be wrong without any error message. Check that the months are consecutive, and if not, reindex the data to a complete monthly calendar so that missing months appear as empty rows.

```python
gaps = nat["date"].diff().dt.days.dropna()
assert gaps.between(28, 31).all(), "a month is missing"

# if the check fails, fill in the calendar:
full = pd.date_range(nat["date"].min(), nat["date"].max(),
                     freq="MS")
nat = nat.set_index("date").reindex(full).rename_axis("date")
nat = nat.reset_index()
```

In a panel, do the same check *within* each region.

## 11. Step 2: one horizon by hand

### 11.1 The function

The heart of the method fits in one short function. It builds the right-hand side of equation (3.1) for one horizon, builds the outcome *h* months ahead, drops incomplete rows and runs OLS with Newey–West errors.

```python
def one_horizon(df, y, x, h, p=12, start="2001-01-01"):
    X = pd.DataFrame({"x": df[x]})              # today's shock
    for q in range(1, p + 1):
        X[f"y_l{q}"] = df[y].shift(q)           # p lags of y
        X[f"x_l{q}"] = df[x].shift(q)           # p lags of x
    for lead in range(1, h):
        X[f"x_f{lead}"] = df[x].shift(-lead)    # leads 1..h-1
    X["trend"] = df["t"]
    dep = df[y].shift(-h)                       # y, h months ahead
    keep = df["date"] >= start
    d = X.assign(dep=dep)[keep].dropna()
    res = sm.OLS(d["dep"], sm.add_constant(d.drop(columns="dep")))
    res = res.fit(cov_type="HAC", cov_kwds={"maxlags": h + 1})
    return res.params["x"], res.bse["x"], int(res.nobs)
```

### 11.2 What each line does

`shift(q)` moves a column down by *q* rows, so row *t* receives the value of row *t* − *q*: a lag. `shift(-h)` moves it up, so row *t* receives the value of row *t* + *h*: the outcome *h* months ahead, or a lead. The loop `range(1, h)` runs from 1 to *h* − 1, so there are no leads at *h* = 0 and 1, as in the reference study. `sm.add_constant` adds the constant $\alpha_h$. Finally, `cov_type="HAC"` with `maxlags = h + 1` asks `statsmodels` for Newey–West standard errors with *h* + 1 lags.

### 11.3 Three rules hidden in the function

**Build lags and leads first, restrict the sample second.** The study's shocks start in January 2001, but the twelve lags of January 2001 come from 2000. The function builds every lag on the full data and only then keeps the rows from 2001 on. Restricting first would throw away those lags and lose a year of data.

**Drop incomplete rows last.** `dropna()` removes rows where any variable is missing: at the start (no lags yet) and at the end (no outcome *h* months ahead yet). This is why the number of observations falls as *h* grows: 308 months at *h* = 0 but 296 at *h* = 12, because the last twelve months have no outcome a year ahead.

**One horizon, one regression.** Nothing is carried from one horizon to the next.

### 11.4 Running it

```python
b, se, n = one_horizon(nat, "d_cpi_all", "d_fuel", h=0)
print(round(b, 4), round(se, 4), n)
```

This prints 0.0440, 0.0059 and 308: on impact, a 1% fuel price rise raises all-income inflation by 0.044 percentage points, with a standard error of 0.006, estimated on 308 months.

## 12. Step 3: all horizons and the cumulative response

### 12.1 The loop

To get the whole response function, call the function for *h* = 0, …, 12. To get the cumulative response (equation 5.2), change one line: the outcome becomes the sum of inflation from *t* to *t* + *h*.

```python
def one_horizon_cum(df, y, x, h, p=12, start="2001-01-01"):
    # identical to one_horizon except for the outcome:
    # dep = df[y].shift(-h)  becomes
    dep = sum(df[y].shift(-j) for j in range(h + 1))
    ...

per = [one_horizon(nat, "d_cpi_all", "d_fuel", h) for h in range(13)]
cum = [one_horizon_cum(nat, "d_cpi_all", "d_fuel", h)
       for h in range(13)]
```

### 12.2 The result

Table 4 shows the estimates. The second column is the one-month response $\beta_h$, the fourth its running sum and the fifth the directly estimated cumulative response $B_h$.

Table: Table 4. All-income CPI on the fuel shock, 2001–2026, estimated by hand.

| *h* | $\beta_h$ | s.e. | Running sum | $B_h$ (direct) | s.e. | Months |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.0440 | 0.0059 | 0.0440 | 0.0440 | 0.0059 | 308 |
| 1 | 0.0396 | 0.0099 | 0.0835 | 0.0836 | 0.0121 | 307 |
| 2 | −0.0190 | 0.0101 | 0.0645 | 0.0443 | 0.0103 | 306 |
| 3 | 0.0127 | 0.0073 | 0.0772 | 0.0772 | 0.0153 | 305 |
| 4 | −0.0025 | 0.0081 | 0.0747 | 0.0632 | 0.0090 | 304 |
| 5 | 0.0128 | 0.0072 | 0.0875 | 0.0758 | 0.0116 | 303 |
| 6 | 0.0127 | 0.0060 | 0.1001 | 0.0870 | 0.0150 | 302 |
| 7 | 0.0023 | 0.0059 | 0.1024 | 0.0885 | 0.0140 | 301 |
| 8 | 0.0109 | 0.0067 | 0.1133 | 0.0995 | 0.0153 | 300 |
| 9 | −0.0058 | 0.0074 | 0.1075 | 0.0928 | 0.0182 | 299 |
| 10 | 0.0098 | 0.0066 | 0.1173 | 0.1013 | 0.0185 | 298 |
| 11 | −0.0056 | 0.0067 | 0.1117 | 0.0947 | 0.0172 | 297 |
| 12 | 0.0059 | 0.0071 | 0.1176 | 0.1016 | 0.0174 | 296 |


::: {custom-style="Table Note"}
Note: Each row is a separate OLS regression with 12 lags of inflation and of the fuel shock, fuel leads 1 to *h* − 1, a trend and a constant. Standard errors are Newey–West with *h* + 1 lags. Source: `tutorial/lp_tutorial.py`, step 3.
:::

### 12.3 Reading the table

Three features are worth noticing. First, the one-month responses are large at *h* = 0 and 1 and small afterwards, sometimes negative: most of the pass-through happens within two months, and later months add small amounts. Second, the running sum and the direct estimate agree at *h* = 0, 1 and 3 but differ elsewhere (at *h* = 6, 0.100 against 0.087), because each regression uses a slightly different set of months and controls. The direct estimate is the one to report, because it comes with its own standard error. Third, the standard errors of $B_h$ grow with *h*, from 0.0059 at *h* = 0 to 0.0174 at *h* = 12: a long-horizon response is harder to pin down.

## 13. Step 4: bands and the figure

### 13.1 Bands

The 90% band at each horizon is the estimate plus and minus 1.645 standard errors.

```python
res = pd.DataFrame(cum, columns=["beta", "se", "nobs"])
res["h"] = range(13)
res["lo"] = res["beta"] - 1.645 * res["se"]
res["hi"] = res["beta"] + 1.645 * res["se"]
```

### 13.2 The figure

A response is best shown as a line over the horizons with its band shaded. The following code draws it in black and white, as journals print.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5.2, 3.2))
ax.fill_between(res["h"], res["lo"], res["hi"], color="0.85")
ax.plot(res["h"], res["beta"], "o-", color="k", markersize=3.5)
ax.axhline(0, color="k", linewidth=0.6)
ax.set_xlabel("Months after the shock (h)")
ax.set_ylabel("Cumulative response (pp per 1% fuel)")
fig.savefig("response.png", dpi=200, bbox_inches="tight")
```

Figure 2 shows the result for both price indices. The two lines are almost on top of each other: a 1% fuel price rise raises both price levels by about 0.04% within the month and by about 0.10% after a year.

![Figure 2. Cumulative responses of the all-income and bottom-30% price levels to a 1% fuel price shock, 2001–2026 (90% band for all income).](tutorial/figures/step3_national.png){width=75%}

## 14. Step 5: checking the estimator on simulated data

### 14.1 Why simulate

Before trusting an estimator on real data, check that it recovers a *known* answer. Make up data from a model whose impulse response you know, estimate the local projection on it and compare. If the estimator fails here, it will fail on real data too, and you will never know.

### 14.2 The simulation

The simulated model is a richer version of equation (2.1), in which the shock acts over three months:

$$y_t = 0.4\, y_{t-1} + 0.04\, x_t + 0.02\, x_{t-1} + 0.01\, x_{t-2} + e_t. \qquad\qquad (14.1)$$

Its true response to a one-time unit shock is 0.040 on impact, then $0.4 \times 0.040 + 0.02 = 0.036$, then $0.4 \times 0.036 + 0.01 = 0.0244$, and then it falls by 60% each month.

```python
rng = np.random.default_rng(0)
T = 3000
x, e = rng.normal(0, 3, T), rng.normal(0, 0.2, T)
y = np.zeros(T)
for s in range(T):
    y[s] = 0.4 * (y[s-1] if s else 0) + e[s] + sum(
        b * x[s-j] for j, b in enumerate((0.04, 0.02, 0.01))
        if s - j >= 0)
sim = pd.DataFrame({"t": np.arange(T), "y": y, "x": x})
```

Estimating `one_horizon` on `sim` (with no sample restriction) gives Table 5 and Figure 3. The estimates track the truth at every horizon; the largest error is 0.0043, within sampling noise.

Table: Table 5. True and estimated responses in simulated data (3,000 months).

| *h* | 0 | 1 | 2 | 3 | 4 | 6 | 9 | 12 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| True | 0.0400 | 0.0360 | 0.0244 | 0.0098 | 0.0039 | 0.0006 | 0.0000 | 0.0000 | 
| Estimate | 0.0404 | 0.0366 | 0.0243 | 0.0141 | 0.0061 | −0.0001 | −0.0006 | 0.0024 | 
| Standard error | 0.0012 | 0.0015 | 0.0015 | 0.0015 | 0.0014 | 0.0015 | 0.0015 | 0.0015 | 

![Figure 3. True response and local projection estimate in simulated data (90% band).](tutorial/figures/step1_simulation.png){width=75%}

### 14.3 Simulating persistent shocks: why the leads matter

Now make the shocks persistent, $x_t = 0.6\, x_{t-1} + u_t$, and estimate with and without the leads. Table 6 and Figure 4 show the result.

Table: Table 6. Persistent shocks: estimates with and without leads.

| *h* | 0 | 1 | 2 | 3 | 4 | 6 | 8 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| True response to a one-time shock | 0.040 | 0.036 | 0.024 | 0.010 | 0.004 | 0.001 | 0.000 | 
| With leads 1 to *h* − 1 | 0.041 | 0.061 | 0.022 | 0.009 | 0.005 | −0.002 | −0.001 | 
| Without leads | 0.041 | 0.061 | 0.058 | 0.043 | 0.031 | 0.008 | 0.003 | 

![Figure 4. With persistent shocks, leaving out the leads overstates the response.](tutorial/figures/step2_leads.png){width=75%}

Without leads, the response is overstated at every horizon, because today's shock gets the credit for the later shocks it predicts. With leads 1 to *h* − 1 it is right from *h* = 2 on, but not at *h* = 1, where the lead set is empty. The error at *h* = 1 is 0.025, close to the $a \times b = 0.6 \times 0.04 = 0.024$ predicted in Section 4.2. Including the lead at *t* + *h* as well (leads 1 to *h*) removes it; Exercise 7 asks you to check this.

The study's automated tests (`tests/test_lp.py`) run checks of this kind, including panel versions, every time the analysis is rebuilt.

## 15. Step 6: the study's estimator

### 15.1 One call for all horizons

Writing the loop by hand is the best way to learn, but a research project needs one tested function that handles every variant. The study's estimator is `local_projection` in `code/python/lp.py`:

```python
import sys
sys.path.insert(0, "code/python")
from lp import local_projection

res = local_projection(nat, y="d_cpi_all", x="d_fuel", time="t",
                       horizons=12, p=12, se="newey_west",
                       cumulative=True,
                       sample=nat["date"] >= "2001-01-01")
print(res[["h", "beta", "se", "lo", "hi", "nobs"]])
```

It returns one row per horizon with the estimate, its standard error, the 90% band, the number of observations and the R². Its estimates match the hand-made ones in Table 4 exactly: the largest difference is 0.

### 15.2 Options

Table 7 lists the options and where the study uses them.

Table: Table 7. Options of the study's estimator.

| Option | What it does | Use in the study |
|---|---|---|
| `cumulative=True` | Outcome is the sum from *t* to *t* + *h* | All reported responses |
| `unit="region"` | Panel with unit fixed effects; lags built within units | The 17-region panel |
| `se=...` | `"newey_west"`, `"driscoll_kraay"`, `"cluster"` or `"robust"` | National and panel |
| `p=12` | Number of lags of the outcome, shock and controls | 12; 6 and 18 in the appendix |
| `controls=(...)` | Extra variables, entered with *p* lags | Exchange rate, policy rate, world food prices |
| `exog=(...)` | Variables entered in the same month only | Dummies for the series' splice months |
| `interact=("G",)` | Adds shock × G and returns its coefficient | Region groups; asymmetry |
| `sample=mask` | Keeps shock dates where the mask is true, after lags are built | Sub-periods; dropping 2020 |
| `tz=False` | Drops the Teulings–Zubanov leads | Not used |

## 16. Step 7: the regional panel

### 16.1 The code

The panel needs the regional file sorted by region and month, and two more arguments: `unit` and Driscoll–Kraay errors.

```python
reg = pd.read_csv("data/clean/regional_panel.csv",
                  parse_dates=["date"])
reg = reg.sort_values(["region", "date"]).reset_index(drop=True)

pan = local_projection(reg, y="d_ratio", x="d_fuel", time="t",
                       unit="region", horizons=12, p=12,
                       se="driscoll_kraay", cumulative=True,
                       sample=reg["date"] >= "2001-01-01")
```

Two things happen inside. First, lags and leads are built *within* each region (the estimator groups the data by `unit` before shifting), so the first lag of Region II's first month is missing rather than borrowed from the last month of Region I. Second, the regression is run with the `linearmodels` package (`PanelOLS` with entity effects and a Driscoll–Kraay covariance with *h* + 1 lags).

### 16.2 The result

Table 8 compares the national and panel estimates of the inflation gap.

Table: Table 8. Cumulative response of the inflation gap: national and 17-region panel.

| *h* | National | s.e. | Panel | s.e. | Panel observations |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.0000 | 0.0040 | −0.0006 | 0.0032 | 5,219 |
| 1 | −0.0077 | 0.0073 | −0.0082 | 0.0057 | 5,202 |
| 2 | −0.0016 | 0.0078 | −0.0065 | 0.0046 | 5,185 |
| 3 | −0.0185 | 0.0110 | −0.0149 | 0.0075 | 5,168 |
| 4 | −0.0175 | 0.0086 | −0.0180 | 0.0071 | 5,151 |
| 6 | −0.0155 | 0.0103 | −0.0214 | 0.0084 | 5,117 |
| 8 | −0.0209 | 0.0102 | −0.0242 | 0.0084 | 5,083 |
| 10 | −0.0179 | 0.0114 | −0.0211 | 0.0085 | 5,049 |
| 12 | −0.0097 | 0.0113 | −0.0173 | 0.0085 | 5,015 |


::: {custom-style="Table Note"}
Note: The outcome is the cumulative change in the inflation gap, all-income minus bottom-30% inflation; a negative value means the poor's prices rise more. National: Newey–West errors. Panel: region fixed effects and Driscoll–Kraay errors. Source: `tutorial/lp_tutorial.py`, step 5.
:::

The panel uses 17 times as many observations, so its standard errors are smaller. Chapter 21 interprets the numbers.

### 16.3 Group interactions

To test whether a group of regions responds differently (Section 7.3), add a 0/1 column for the group and pass it to `interact`:

```python
mindanao = ["R09", "R10", "R11", "R12", "R13", "BARMM"]
reg["mindanao"] = reg["region"].isin(mindanao).astype(int)
grp = local_projection(reg, "d_ratio", "d_fuel", time="t",
                       unit="region", se="driscoll_kraay",
                       cumulative=True, interact=("mindanao",),
                       sample=reg["date"] >= "2001-01-01")
print(grp[grp["term"] == "shock_x_mindanao"])
```

The rows with `term == "shock_x_mindanao"` hold $\theta_h$, the extra response in Mindanao. The study reads its four groups from a region information table (`code/python/data_io.py`, `region_info()`); the list above is the same Mindanao group.

## 17. Step 8: robustness checks in code

A robustness check re-estimates the model with one change and asks whether the conclusion survives. With the estimator, each check is one argument. The study's five core checks are:

```python
base = dict(time="t", horizons=12, p=12, cumulative=True)
nw = dict(se="newey_west")
dk = dict(unit="region", se="driscoll_kraay")
s01 = nat["date"] >= "2001-01-01"

# 1. world crude oil in pesos instead of the domestic fuel index
crude = local_projection(nat, "d_ratio", "d_dubai_php",
                         sample=s01, **base, **nw)
# 2. macroeconomic controls (each with 12 lags)
macro = local_projection(nat, "d_ratio", "d_fuel", sample=s01,
                         controls=("d_php_usd", "d_policy_rate",
                                   "d_ffpi"), **base, **nw)
# 3. drop the shock dates in 2020
x20 = local_projection(nat, "d_ratio", "d_fuel",
                       sample=s01 & (nat["date"].dt.year != 2020),
                       **base, **nw)
# 4. the panel in two periods
r01 = reg["date"] >= "2001-01-01"
early = local_projection(reg, "d_ratio", "d_fuel",
                         sample=r01 & (reg["date"] <= "2012-12-01"),
                         **base, **dk)
late = local_projection(reg, "d_ratio", "d_fuel",
                        sample=reg["date"] >= "2013-01-01",
                        **base, **dk)
# 5. leave one region out
loo = {}
for r in reg["region"].unique():
    sub = reg[reg["region"] != r].reset_index(drop=True)
    loo[r] = local_projection(sub, "d_ratio", "d_fuel",
                              sample=sub["date"] >= "2001-01-01",
                              **base, **dk)
```

Note how check 3 works. Dropping 2020 through `sample` removes the months of 2020 as *shock dates*, but those months still supply lags and outcomes for the neighbouring months. That is the right way to drop a period in a local projection: deleting the rows instead would break the lags of 2021. The full set of checks is in `code/python/04_estimate.py`.

## 18. Step 9: applying the responses to an episode

### 18.1 The formula

Responses add up. If fuel prices change by $f_1$ in month 1, $f_2$ in month 2 and so on, the fuel-driven change in the log price level between month 0 and month *m* is

$$\text{fuel-driven change}_m = \sum_{s=1}^{m} B_{m-s}\, f_s. \qquad\qquad (18.1)$$

Each month's shock is multiplied by the cumulative response for the number of months that have passed since it happened. The study uses this to ask how much of the 2026 price surge was caused by fuel. To make it a fair test, the responses are estimated only on data up to December 2025, before the shock, and then applied to the fuel shocks of January to August 2026.

### 18.2 The code

```python
pre = nat[nat["date"] <= "2025-12-01"].reset_index(drop=True)
irf = local_projection(pre, "d_cpi_all", "d_fuel", time="t",
                       horizons=12, p=12, se="newey_west",
                       cumulative=True,
                       sample=pre["date"] >= "2001-01-01")
B = irf.set_index("h")["beta"]

ep = nat[(nat["date"] >= "2026-01-01")
         & (nat["date"] <= "2026-08-01")].reset_index(drop=True)
ep["months_to_aug"] = len(ep) - 1 - ep.index
ep["B"] = ep["months_to_aug"].map(B)
ep["contribution"] = ep["B"] * ep["d_fuel"]
print(ep["contribution"].sum())
```

### 18.3 The result

Table 9 shows the arithmetic. The March shock of 31.8% has had five months to work by August, so it is multiplied by $B_5 = 0.072$ and contributes 2.29 percentage points. The fuel price fall in May subtracts 0.94. In total, fuel explains 2.55 of the 4.81% rise in the all-income price level between December 2025 and August 2026, about 53%.

Table: Table 9. Fuel-driven rise in the all-income price level, December 2025 to August 2026.

| Month | Fuel shock $f_s$ (%) | Months to August | $B_{m-s}$ | Contribution (pp) |
|---|---:|---:|---:|---:|
| 2026-01 | −2.7 | 7 | 0.086 | −0.23 |
| 2026-02 | 1.2 | 6 | 0.086 | 0.10 |
| 2026-03 | 31.8 | 5 | 0.072 | 2.29 |
| 2026-04 | 23.5 | 4 | 0.061 | 1.44 |
| 2026-05 | −17.7 | 3 | 0.053 | −0.94 |
| 2026-06 | −7.9 | 2 | 0.032 | −0.25 |
| 2026-07 | −0.6 | 1 | 0.069 | −0.04 |
| 2026-08 | 4.9 | 0 | 0.040 | 0.19 |
| Total | | | | 2.55 |

::: {custom-style="Table Note"}
Note: $B_{m-s}$ is the cumulative response of the all-income price level estimated on shock dates from January 2001 to December 2025. The actual rise in 100 × ln CPI was 4.81. Source: `tutorial/lp_tutorial.py`, step 7; the study's version with bands is `code/python/05_policy_2026.py`.
:::

## 19. Step 10: the same in Stata

The study's full Stata 17 pipeline will be added in `code/stata/`, to be run by the author. The core of one horizon looks like this. Stata's time-series operators `L.` (lag) and `F.` (lead) respect the calendar declared by `tsset` or `xtset`, so gaps and region boundaries are handled automatically. Point estimates should match Python's; standard errors can differ slightly because packages use different small-sample corrections. This snippet has not yet been run in Stata.

```stata
import delimited "data/clean/national_monthly.csv", clear
gen mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate

local h = 6
* outcome: the sum of inflation from t to t+h
gen dep = d_cpi_all
forvalues j = 1/`h' {
    replace dep = dep + F`j'.d_cpi_all
}
* leads 1..h-1 (none when h < 2)
local leads ""
if `h' >= 2 local leads "F(1/`=`h'-1').d_fuel"

newey dep d_fuel L(1/12).d_cpi_all L(1/12).d_fuel `leads' t ///
    if mdate >= tm(2001m1), lag(`=`h'+1')
* the coefficient on d_fuel is B_h
```

For the regional panel, import `regional_panel.csv`, run `encode region, gen(rid)` and `xtset rid mdate`, install the Driscoll–Kraay command once with `ssc install xtscc`, and replace `newey` with

```stata
xtscc dep d_fuel L(1/12).d_ratio L(1/12).d_fuel `leads' t ///
    if mdate >= tm(2001m1), fe lag(`=`h'+1')
```

To loop over horizons, wrap everything from `local h` to the regression in `forvalues h = 0/12 { ... }`, drop `dep` at the end of each pass and store the coefficient with `post` or `estimates store`.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part III. Interpretation

## 20. Reading a response

### 20.1 A response is a "what if"

An impulse response answers a conditional question. $B_{12} = 0.102$ for the all-income CPI means: *if* fuel prices rise 1% this month and nothing else unusual happens, consumer prices will be 0.102% higher a year later than they would otherwise have been. It does not say that prices will rise by 0.102%, because other things will also happen in that year, and it does not say what caused the fuel price rise.

### 20.2 Four questions to ask of every response

**What are the units?** Check what a one-unit shock is and what the outcome measures. In the study the shock is a 1% fuel price change and the cumulative outcome is the percentage change in the price level, so $B_h$ is "percent per 1%", an *elasticity*: the percentage change in one variable for a 1% change in another.

**How big is it in a realistic case?** Scale the response to a shock that actually happens. Fuel prices rose by about 53.7 log points between December 2025 and April 2026; a typical month moves them by a few percent. A response of 0.102 per 1% is small for a 1% shock but large for a 50% one.

**Is it precise?** Look at the band, not only at the estimate. Ask whether the whole band lies on one side of zero, and at which horizons. A band that crosses zero at every horizon means the data cannot tell the sign; a band that excludes zero at most horizons, with a stable shape, is strong evidence.

**What is its shape?** Does the response build up, peak and fade, or keep growing? For a price level, a response that rises and stays up means the shock has a lasting effect on prices. A zig-zag between neighbouring horizons is usually noise or a feature of the specification (Chapter 22), not economics.

## 21. Interpreting the study's results

This chapter interprets the study's main estimates as a worked example. All numbers are cumulative responses to a 1% fuel price rise.

### 21.1 RQ1: how much and how fast do fuel prices pass through?

The all-income price level rises by 0.044% in the month of the shock (standard error 0.006), 0.077% after three months, 0.087% after six and 0.102% after twelve. The bottom-30% price level responds almost identically: 0.044, 0.097, 0.095 and 0.102. Every band excludes zero.

The interpretation has three parts. *Size:* a 10% rise in pump prices raises the price level by about 1.0% within a year. *Speed:* about 40% of the one-year effect happens in the first month, through the direct weight of fuel in the basket and fares that adjust quickly, and the rest builds up over the following months as transport and production costs are passed on. *Comparison:* the impact response equals the average that @kpodar_liu_2022 report for advanced economies (0.044) and is more than twice their developing-economy average (0.018). When world crude oil in pesos replaces the retail fuel index, the one-year response falls to 0.041, about 40% of the retail response: crude prices understate pass-through, because taxes and margins make pump prices move less than crude in percentage terms and the domestic index captures the price consumers actually pay.

### 21.2 RQ2: who pays more?

**National.** The cumulative response of the inflation gap is $−0.0185$ at *h* = 3, $−0.0155$ (standard error 0.0103) at *h* = 6 and $−0.0097$ (standard error 0.0113) at *h* = 12. The sign is negative throughout, which means the bottom 30%'s prices rise more: the effect is regressive. But the bands include zero at most horizons; the estimate is significant at the 10% level only at *h* = 3, 4, 7, 8. The honest reading is "regressive in sign, imprecise nationally".

**Panel.** With 17 regions, the response is $−0.0149$ at *h* = 3, $−0.0214$ (standard error 0.0084) at *h* = 6 and $−0.0173$ (standard error 0.0085) at *h* = 12, significant at every horizon from 3 to 12 months. The panel confirms the national sign with more precision. In magnitude, a 10% fuel price rise raises the poor's price level by about 0.2 percentage points more than the average household's after six months, on top of an average rise of about 0.9%.

**Why.** Let $w^g_k$ be the share of group *g*'s budget spent on category *k* (its *budget share*) and $\pi^g_k$ the inflation of category *k* in group *g*'s index. The gap splits exactly into two parts:

$$\pi^A - \pi^B = \sum_k (w^A_k - w^B_k)\, \pi^A_k + \sum_k w^B_k\, (\pi^A_k - \pi^B_k). \qquad\qquad (21.1)$$

The first sum is a *weights effect*: the gap that would arise if both groups faced the same price changes and differed only in what they spend their money on. The second is a *within-category effect*: the gap that arises because the groups buy different items inside each category and those items' prices change differently. Applying the 13 division responses to the two groups' budget shares gives the weights effect alone: +0.0101 at *h* = 12, a progressive number, because better-off households spend more on fuel and transport. Since the total is negative, the within-category effect must be regressive and larger: roughly $−0.0097 - (+0.0101) \approx −0.020$. The exploratory comparison of the two baskets from 2013 points to where it comes from: the housing and utilities division of the bottom 30%, which includes household fuels, responds more (0.182 against 0.142 after a year), and its food division also responds more (0.067 against 0.055), while its transport division responds less (0.196 against 0.300). The poor do not pay more because they buy more fuel; they pay more because the things they buy, such as cooking fuels and food, become relatively more expensive after a fuel shock.

### 21.3 Robustness: does the conclusion survive?

Read robustness checks as a group and report all of them, including those that weaken the result. Table 10 collects the study's core checks for the gap at *h* = 6.

Table: Table 10. Core robustness checks: cumulative response of the inflation gap at *h* = 6.

| Specification | Estimate | s.e. | Reading |
|---|---:|---:|---|
| National baseline | −0.0155 | 0.0103 | Regressive, imprecise |
| Dubai crude in pesos as the shock | −0.0093 | 0.0056 | Same sign with an outside price |
| Macroeconomic controls | −0.0046 | 0.0156 | Smaller, not significant |
| Excluding 2020 | −0.0186 | 0.0121 | Unchanged |
| Panel, 2001–2012 | −0.0541 | 0.0197 | Strong, significant |
| Panel, 2013–2026 | −0.0091 | 0.0064 | Small, not significant |
| Panel, leaving out one region | −0.0227 to −0.0203 | | No region drives the result |

::: {custom-style="Table Note"}
Note: Responses per 1% fuel price rise; a negative value means the bottom 30%'s prices rise more. Source: `output/tables/estimates.csv`.
:::

The sign is negative in every specification, which supports the direction of the result. Two checks qualify it. With macroeconomic controls the estimate shrinks to about a third and loses significance, so part of the gap may come from the exchange rate, interest rates or world food prices moving together with fuel prices. And the gap is concentrated in 2001–2012, a period that includes the 2008 rice crisis; since 2013 it has been small. A careful write-up states both, rather than reporting only the checks that agree.

### 21.4 RQ3: applying the responses to 2026

Chapter 18 showed how the responses, estimated only on data up to December 2025, explain the 2026 surge. Fuel accounts for 2.55 of the 4.81% rise in the all-income price level by August 2026 (about 53%) and 3.13 of the 5.98% rise for the bottom 30% (about 52%). The model predicts the right direction for the gap ($−0.65$ against an actual $−1.18$) but only about half its size.

Responses become more useful when expressed in money. If the bottom-30% price level is 3.13% higher because of fuel, a family of five living exactly at the poverty line, about PHP 14,714 a month at December 2025 prices, needs $14{,}714 \times (e^{3.13/100} - 1) \approx$ PHP 467 more a month to buy the same basket. Across regions this ranges from PHP 390 (XII SOCCSKSARGEN) to PHP 633 (National Capital Region). Including the part of the surge that the model does not attribute to fuel, the actual extra cost was about PHP 907.

How should the other half of the surge be read? A local projection gives the *average* response to a 1% shock in the estimation sample. If the 2026 shock was larger, or spread through rice and other food more than past shocks did, the model will under-predict. The study's descriptive decomposition finds exactly this: cereals alone account for +1.67 percentage points of the bottom 30%'s excess price rise of +1.24. An out-of-sample test like this is valuable precisely because it shows where the average response stops being a good guide.

## 22. The lead convention: what it changes

Chapter 4 explained that the study, following the reference paper, uses leads 1 to *h* − 1, while Teulings and Zubanov's own correction uses leads 1 to *h*. Table 11 compares the two on the study's national data.

Table: Table 11. Cumulative responses under two lead conventions (national, 2001–2026).

| *h* | 0 | 1 | 2 | 3 | 6 | 9 | 12 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| All-income CPI, leads 1 to *h* − 1 | 0.044 | 0.084 | 0.044 | 0.077 | 0.087 | 0.093 | 0.102 | 
| All-income CPI, leads 1 to *h* | 0.044 | 0.064 | 0.062 | 0.077 | 0.088 | 0.093 | 0.101 | 
| Inflation gap, leads 1 to *h* − 1 | 0.0000 | −0.0077 | −0.0016 | −0.0185 | −0.0155 | −0.0137 | −0.0097 | 
| Inflation gap, leads 1 to *h* | 0.0000 | −0.0021 | −0.0101 | −0.0183 | −0.0160 | −0.0126 | −0.0112 | 

::: {custom-style="Table Note"}
Note: The first row of each pair is the study's specification (decision D4). Source: `tutorial/lp_tutorial.py`, step 6.
:::

The two conventions differ at *h* = 1 and 2 and hardly at all from *h* = 3 on. With leads 1 to *h* − 1, the all-income response jumps to 0.084 at *h* = 1 and falls back to 0.044 at *h* = 2: a zig-zag. With leads 1 to *h*, it is a smooth 0.064 and 0.062. Chapters 4 and 14 explained why: at *h* = 1 the reference convention has no lead, so next month's shock, which is correlated 0.39 with this month's, is not held constant. The six- and twelve-month responses, on which the study's conclusions rest, are essentially the same under both conventions. The practical lesson is to read the responses at *h* = 1 and 2 with care, and to say in a footnote or robustness check which convention you use.

## 23. Writing up the results

### 23.1 What a results paragraph should contain

A good paragraph about an impulse response states, in order: the shock and its size; the outcome and its units; the estimate at one or two key horizons with its standard error or band; whether it is significant; what it means in a realistic case; and how it compares with earlier work. It avoids reading each horizon one by one.

### 23.2 Two examples

A weak paragraph: "Table 4 shows the results. The coefficient is 0.044 at h = 0, 0.084 at h = 1, 0.044 at h = 2, and so on. They are significant."

A better paragraph: "A 1% rise in retail fuel prices raises the all-income price level by 0.044% within the month (standard error 0.006) and by 0.102% after a year (standard error 0.017); the 90% bands exclude zero at every horizon. A 10% rise in pump prices thus makes consumer prices about 1.0% higher a year later. The impact effect equals the advanced-economy average in @kpodar_liu_2022."

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

1. Using $B_{12} = 0.102$, by how much would a 20% rise in pump prices raise the all-income price level after a year?
2. Why does the number of months in Table 4 fall from 308 at *h* = 0 to 296 at *h* = 12?
3. The national gap at *h* = 6 is $−0.0155$ with a standard error of 0.0103. Compute the 90% band. Is the response significant at the 10% level? Do the same for the panel estimate, $−0.0214$ with a standard error of 0.0084.
4. Fuel prices rise 10% in month 1 and fall 5% in month 2. Using $B_0 = 0.044$ and $B_1 = 0.084$, what is the fuel-driven change in the all-income price level by month 2?
5. A colleague drops the year 2020 by deleting its rows before building the lags. What goes wrong, and how should it be done?
6. Why can the region indicator $G_r$ be left out of the regression when the interaction $f_{r,t} \times G_r$ is included?
7. Change `range(1, h)` to `range(1, h + 1)` in `one_horizon` and re-run the persistent-shock simulation of Section 14.3. What happens at *h* = 1?
8. Re-estimate the national model with 6 lags instead of 12 (`p=6`). Which responses change most, and why might the twelfth lag matter for unadjusted data?

### Answers

1. $20 \times 0.102 = 2.04$: the price level would be about 2.0% higher than otherwise.
2. The outcome at *h* = 12 needs inflation twelve months after the shock date. For the last twelve shock dates in the data, that month has not happened yet, so those rows are dropped.
3. National: $−0.0155 \pm 1.645 \times 0.0103$ gives [−0.0324, 0.0014]; it includes zero, so the response is not significant at 10%. Panel: [−0.0352, −0.0077]; it excludes zero, so the response is significant.
4. By equation (18.1), $B_1 \times 10 + B_0 \times (-5) = 0.084 \times 10 - 0.044 \times 5 = 0.62$ percentage points.
5. The first months of 2021 would take their lags from 2019, so "lag 1" of January 2021 would be December 2019. Instead, keep the rows, build the lags, and exclude 2020 from the shock dates with the sample mask (Chapter 17).
6. $G_r$ does not change over time, so it is a constant for each region and is absorbed by the region fixed effect.
7. The estimate at *h* = 1 falls from about 0.061 to close to the true 0.036, because next month's shock is now held constant. The responses from *h* = 2 on hardly change.
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
