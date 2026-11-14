```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part I. Theory

## 1. The question: what an impulse response is

Suppose the price of gasoline and diesel at the pump rises by 1% this month. How much higher will consumer prices be next month? In three months? In a year? And how much higher compared with what? The answer is always *compared with what would have happened without the rise*. That comparison is the heart of the method, so it is worth stating carefully.

**The shock.** A *shock* is an unexpected change in one variable that we want to trace through the economy. In the study the shock is the monthly percentage change in the retail fuel price, measured by the Philippine Statistics Authority (PSA) consumer price sub-index 07.2.2, "fuels and lubricants for personal transport". If $F_t$ is that index in month *t*, the shock is

$$f_t = 100\,\Delta \ln F_t = 100\,(\ln F_t - \ln F_{t-1}). \qquad\qquad (1.1)$$

For example, in March 2026 the index rose from {{ fuel_feb26 }} to {{ fuel_mar26 }}, so $f_t = 100 \ln({{ fuel_mar26 }}/{{ fuel_feb26 }}) \approx {{ f_mar26 }}$: a fuel shock of about {{ f_mar26_round }}%.

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

Fuel price shocks are not one-off events. In the study's data (2001–2026) the monthly fuel shock has a first-order *autocorrelation*, the correlation between a variable and its own previous value, of {{ f(t.fuel_ac1, 2) }}. A rise this month therefore *predicts* a rise next month, and next month's rise has its own effect on prices. A regression of $\pi_{t+h}$ on $f_t$ alone gives today's shock the credit for the later shocks it predicts.

### 4.2 The fix

@teulings_zubanov_2014 proposed adding the shocks between *t* and *t* + *h* to the regression. Once they are held constant, $\beta_h$ measures the effect of a *one-time* shock. To see why, return to the small example of Section 2.3 but let the shock be persistent: $x_{t+1} = a\, x_t + u_{t+1}$, where $u$ is new noise. Equation (2.3) contains $b\, x_{t+1}$ when *h* = 1. Since $x_{t+1}$ is correlated with $x_t$, a regression without $x_{t+1}$ picks up part of its effect, and the estimated response at *h* = 1 becomes about $\rho b + a b$ instead of $\rho b$. Adding $x_{t+1}$ as a control removes the extra $ab$.

### 4.3 Two conventions

The original correction includes the leads $f_{t+1}, \dots, f_{t+h}$. The reference study's annex tables instead use $f_{t+1}, \dots, f_{t+h-1}$: there is no lead at *h* = 0 or 1, and "lead 1" first appears at *h* = 2. The study follows the reference study (decision D4). The difference matters only at short horizons. With the reference convention, the lead set is empty at *h* = 1, so next month's shock is not held constant and the response at *h* = 1 is overstated when shocks are persistent. From *h* = 2 on, the lead $f_{t+1}$ is in the regression, and when the shock process is close to a first-order autoregression, as in the example above, holding $f_{t+1}$ constant is enough. Chapter 14 shows both effects in simulated data and Chapter 22 shows what this means for the study's results.

## 5. From monthly effects to the price level: cumulative responses

### 5.1 Definition

$\beta_h$ is the effect on inflation *in one month*, month *t* + *h*. Policy questions are usually about the *price level*: how much higher are prices a year after the shock? That is the *cumulative response*, the sum of the monthly effects up to *h*:

$$B_h = \beta_0 + \beta_1 + \dots + \beta_h. \qquad\qquad (5.1)$$

Because inflation is the change in the log price level, the sum of inflation from *t* to *t* + *h* is the change in the log price level over that period: $\sum_{j=0}^{h} \pi_{t+j} = 100\,(\ln P_{t+h} - \ln P_{t-1})$. So $B_h$ is the percentage effect of the shock on the price level *h* months later.

**Example.** For the all-income CPI, the study finds $B_{12} = {{ n.rq1_all_c12 }}$. A 10% rise in pump prices therefore makes consumer prices about $10 \times {{ n.rq1_all_c12 }} \approx {{ n.rq1_all_c12_10pct }}$% higher a year later than they would otherwise have been.

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

The study reports 90% *confidence bands*: $\hat\beta_h \pm 1.645 \times \text{s.e.}(\hat\beta_h)$, where 1.645 is the value that leaves 5% in each tail of the normal distribution. If the band excludes zero, the response is *statistically significant* at the 10% level. For example, the national gap at *h* = 6 is ${{ n.rq2_c6 }}$ with a standard error of {{ n.rq2_c6_se }}; the *t*-statistic is ${{ f(t_nat6, 2) }}$, smaller than 1.645 in absolute value, so the response is not significant at the 10% level.

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
