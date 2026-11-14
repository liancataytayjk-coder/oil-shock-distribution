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

This prints {{ f(t.step3[0].beta_h, 4) }}, {{ f(t.step3[0].se, 4) }} and {{ t.step3[0].nobs }}: on impact, a 1% fuel price rise raises all-income inflation by {{ f(t.step3[0].beta_h, 3) }} percentage points, with a standard error of {{ f(t.step3[0].se, 3) }}, estimated on {{ t.step3[0].nobs }} months.

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
{% for r in t.step3 -%}
| {{ r.h }} | {{ f(r.beta_h, 4) }} | {{ f(r.se, 4) }} | {{ f(r.running_sum, 4) }} | {{ f(r.B_h, 4) }} | {{ f(r.se_B, 4) }} | {{ r.nobs }} |
{% endfor %}

::: {custom-style="Table Note"}
Note: Each row is a separate OLS regression with 12 lags of inflation and of the fuel shock, fuel leads 1 to *h* − 1, a trend and a constant. Standard errors are Newey–West with *h* + 1 lags. Source: `tutorial/lp_tutorial.py`, step 3.
:::

### 12.3 Reading the table

Three features are worth noticing. First, the one-month responses are large at *h* = 0 and 1 and small afterwards, sometimes negative: most of the pass-through happens within two months, and later months add small amounts. Second, the running sum and the direct estimate agree at *h* = 0, 1 and 3 but differ elsewhere (at *h* = 6, {{ f(t.step3[6].running_sum, 3) }} against {{ f(t.step3[6].B_h, 3) }}), because each regression uses a slightly different set of months and controls. The direct estimate is the one to report, because it comes with its own standard error. Third, the standard errors of $B_h$ grow with *h*, from {{ f(t.step3[0].se_B, 4) }} at *h* = 0 to {{ f(t.step3[12].se_B, 4) }} at *h* = 12: a long-horizon response is harder to pin down.

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

Estimating `one_horizon` on `sim` (with no sample restriction) gives Table 5 and Figure 3. The estimates track the truth at every horizon; the largest error is {{ f(t.step1_maxerr, 4) }}, within sampling noise.

Table: Table 5. True and estimated responses in simulated data (3,000 months).

| *h* | 0 | 1 | 2 | 3 | 4 | 6 | 9 | 12 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| True | {% for h in [0,1,2,3,4,6,9,12] %}{{ f(t.step1[h].true, 4) }} | {% endfor %}
| Estimate | {% for h in [0,1,2,3,4,6,9,12] %}{{ f(t.step1[h].est, 4) }} | {% endfor %}
| Standard error | {% for h in [0,1,2,3,4,6,9,12] %}{{ f(t.step1[h].se, 4) }} | {% endfor %}

![Figure 3. True response and local projection estimate in simulated data (90% band).](tutorial/figures/step1_simulation.png){width=75%}

### 14.3 Simulating persistent shocks: why the leads matter

Now make the shocks persistent, $x_t = 0.6\, x_{t-1} + u_t$, and estimate with and without the leads. Table 6 and Figure 4 show the result.

Table: Table 6. Persistent shocks: estimates with and without leads.

| *h* | 0 | 1 | 2 | 3 | 4 | 6 | 8 |
|----------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| True response to a one-time shock | {% for h in [0,1,2,3,4,6,8] %}{{ f(t.step2[h].true, 3) }} | {% endfor %}
| With leads 1 to *h* − 1 | {% for h in [0,1,2,3,4,6,8] %}{{ f(t.step2[h]["with"], 3) }} | {% endfor %}
| Without leads | {% for h in [0,1,2,3,4,6,8] %}{{ f(t.step2[h].without, 3) }} | {% endfor %}

![Figure 4. With persistent shocks, leaving out the leads overstates the response.](tutorial/figures/step2_leads.png){width=75%}

Without leads, the response is overstated at every horizon, because today's shock gets the credit for the later shocks it predicts. With leads 1 to *h* − 1 it is right from *h* = 2 on, but not at *h* = 1, where the lead set is empty. The error at *h* = 1 is {{ f(t.step2[1]["with"] - t.step2[1].true, 3) }}, close to the $a \times b = 0.6 \times 0.04 = 0.024$ predicted in Section 4.2. Including the lead at *t* + *h* as well (leads 1 to *h*) removes it; Exercise 7 asks you to check this.

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

It returns one row per horizon with the estimate, its standard error, the 90% band, the number of observations and the R². Its estimates match the hand-made ones in Table 4 exactly: the largest difference is {{ "%.0e"|format(t.step4_maxdiff) if t.step4_maxdiff else "0" }}.

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
{% for h in [0,1,2,3,4,6,8,10,12] -%}
| {{ h }} | {{ f(t.step5[h].nat, 4) }} | {{ f(t.step5[h].nat_se, 4) }} | {{ f(t.step5[h].pan, 4) }} | {{ f(t.step5[h].pan_se, 4) }} | {{ "{:,}".format(t.step5[h].pan_obs) }} |
{% endfor %}

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

Table 9 shows the arithmetic. The March shock of {{ f(t.step7[2].d_fuel, 1) }}% has had five months to work by August, so it is multiplied by $B_5 = {{ f(t.step7[2].B, 3) }}$ and contributes {{ f(t.step7[2].contribution, 2) }} percentage points. The fuel price fall in May subtracts {{ f(-t.step7[4].contribution, 2) }}. In total, fuel explains {{ f(t.step7_total, 2) }} of the {{ f(t.step7_actual, 2) }}% rise in the all-income price level between December 2025 and August 2026, about {{ (100 * t.step7_total / t.step7_actual)|round|int }}%.

Table: Table 9. Fuel-driven rise in the all-income price level, December 2025 to August 2026.

| Month | Fuel shock $f_s$ (%) | Months to August | $B_{m-s}$ | Contribution (pp) |
|---|---:|---:|---:|---:|
{% for r in t.step7 -%}
| {{ r.month }} | {{ f(r.d_fuel, 1) }} | {{ r.months_to_aug }} | {{ f(r.B, 3) }} | {{ f(r.contribution, 2) }} |
{% endfor -%}
| Total | | | | {{ f(t.step7_total, 2) }} |

::: {custom-style="Table Note"}
Note: $B_{m-s}$ is the cumulative response of the all-income price level estimated on shock dates from January 2001 to December 2025. The actual rise in 100 × ln CPI was {{ f(t.step7_actual, 2) }}. Source: `tutorial/lp_tutorial.py`, step 7; the study's version with bands is `code/python/05_policy_2026.py`.
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
