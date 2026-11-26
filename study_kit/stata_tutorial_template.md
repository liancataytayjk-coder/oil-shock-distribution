---
title: "Stata Tutorial: The Panel Study from Setup to Figures"
subtitle: "Every command of the teaching do-files, explained, with the result you should see"
author: "{{ author }}"
date: "{{ date }}"
---

<#-- Rendered by study_kit/build_kit.py; numbers from output/tables/panel_numbers.json. The commands are the
     ones in code/stata/teaching/*.do; keep the two in step. --#>

# 1. What you need and how to use this tutorial

This tutorial takes you through the whole analysis of the manuscript in Stata 17, from opening Stata to exporting the figures. Each section explains one do-file of the folder `code/stata/teaching/`: what each command does, why it is there, and the number you should see when it runs. Type the commands yourself the first time, or run the do-file and read along.

You need three things. First, Stata 17 (any edition). Second, the folder of do-files and data described in Section 2; it is ready to use, so nothing has to be built first. Third, an internet connection the first time, to install one user-written command, `xtscc`, which computes Driscoll–Kraay standard errors.

Three Stata conventions recur. A *do-file* is a text file of commands that Stata runs in order with `do filename`. A *local macro*, written `` `name' `` with a backquote and a straight quote, is a short piece of text that Stata substitutes before running a command; `local h = 6` followed by `` display `h' `` prints 6. A *global macro*, written `$NAME`, does the same across do-files. Three slashes, `///`, at the end of a line continue a command on the next line.

Table: Table 1. The teaching do-files.

| Step | File | What it does |
|---|---|---|
| 0 | `00_setup.do` | Sets the folders, installs `xtscc` |
| 1 | `01_data.do` | Reads the panel, declares it, builds lags and leads |
| 2 | `02_one_horizon.do` | One local projection by hand |
| 3 | `03_pass_through.do` | Pass-through for both groups, all horizons; the program `panel_lp` |
| 4 | `04_gap.do` | Who pays more: the gap |
| 5 | `05_why.do` | By how much and why: the budget-share calculation |
| 6 | `06_geography.do` | A response for every region; test of equality |
| 7 | `07_robustness.do` | World crude price; one region left out |
| 8 | `08_check.do` | Compares every result with Python's |
| 9 | `09_figures.do` | The four figures |

# 2. Get the data and the files

## 2.1 Two ways to get them

**The pack (easiest).** Download `stata_pack.zip` (in the `study_kit/` folder of the project) and unzip it anywhere, for example in `Documents`. You get one folder, `stata_pack`, that holds everything:

```text
stata_pack/
  00_setup.do ... 09_figures.do    the ten steps
  extra_2026.do                    optional, not in the manuscript
  expected_*.csv                   Python's results, for the check in step 8
  README.md, stata_tutorial.pdf    instructions and this tutorial
  data/
    regional_panel.csv             the panel: 17 regions x 392 months
    national_monthly.csv           national series, one row per month
    weights_2018.csv               2018 budget shares
    region_info.csv                poverty and food share by region
    rq2_weights_decomposition.csv  Python's step 5, for the check
    stata_data.xlsx                the same five tables in Excel, with a data dictionary
```

Results are written to a new subfolder, `stata_pack/output/`.

**The repository.** If you have the whole project folder, `oil-shock-distribution`, the same files are in `code/stata/teaching/`, with the data in `code/stata/teaching/data/`. Results go to `output/stata_teaching/`. The do-files work the same way from either place; only the `cd` and `do` lines differ (Section 3).

Do not open and re-save the CSV files in Excel. Excel may change the dates ("2001-01" becomes "Jan-01") and drop the leading zero of codes such as "01", and Stata would then read them wrongly. To look at the data, open `stata_data.xlsx` instead; it is a copy.

## 2.2 What is in the data

Table: Table 2. The data files.

| File | One row is | Rows | Used in |
|--------------------------------|----------------------------------------|--------|--------------------|
| `regional_panel.csv` | one region in one month, January 1994 to August 2026 | {{ "{:,}".format(17 * 392) }} | steps 1–4, 6, 7 |
| `national_monthly.csv` | one month, the Philippines | 392 | steps 1, 5, 9 |
| `weights_2018.csv` | one spending category in one region's basket, for each group | 532 | step 5 |
| `region_info.csv` | one region (and the Philippines) | 18 | steps 6, 9 |
| `rq2_weights_decomposition.csv` | one spending category | 13 | step 8 |

All index series come from the Philippine Statistics Authority (PSA) consumer price index, with 2018 = 100. The *headline index* is the price index of all households; the *low-income index* is the price index of the bottom 30% of households by income per person, which the PSA publishes from 2000 for every region. The *retail fuel price index* is the PSA sub-index 07.2.2, fuels and lubricants for personal transport, which tracks pump prices of gasoline and diesel. The national file adds the world crude price (Dubai crude, World Bank), the exchange rate (Bangko Sentral ng Pilipinas), the policy rate (Bank for International Settlements) and the FAO Food Price Index.

Table: Table 3. The variables of the regional panel.

| Variable | Meaning | Unit |
|----------------------------------|----------------------------------------------|--------------------|
| `region`, `region_name` | Region code (NCR, CAR, R01 … R13, R04A, R04B, BARMM) and name | text |
| `date_str` | Month, as text "YYYY-MM" | text |
| `year`, `month`, `t` | Year, month, and months since January 1994 (the trend) | number |
| `cpi_all`, `cpi_b30`, `fuel` | Headline index, low-income index, retail fuel price index | 2018 = 100 |
| `d_cpi_all`, `d_cpi_b30` | Inflation of all households and of low-income households | 100 × Δln |
| `d_fuel` | The fuel shock: change in the retail fuel price index | 100 × Δln |
| `d_ratio` | The gap: `d_cpi_all` − `d_cpi_b30`; negative when low-income prices rose more | pp |
| `ratio` | Relative price level, 100 × ln(`cpi_all` / `cpi_b30`) | log points |
| `new_geo_ext`, `d_fuel_nat` | Flag for 2026 months of four regions whose boundaries changed; the national fuel shock | 0/1; 100 × Δln |

"100 × Δln" means 100 times the change in the natural logarithm from the previous month, which is close to the percentage change: a value of 2.0 means the index rose by about 2% that month. Empty cells are missing values; Stata shows them as a dot. The low-income index starts in 2000, so `d_cpi_b30` is missing before February 2000. The sheet `dictionary` of `stata_data.xlsx` describes every variable of all five files.

## 2.3 A first look in Stata

Before the steps, you can open the panel and look at it:

```stata
cd "C:/Users/yourname/Documents/stata_pack"
import delimited "data/regional_panel.csv", clear varnames(1) case(preserve)
browse
summarize d_fuel d_cpi_all d_cpi_b30 d_ratio
tabulate region
```

`browse` opens the data in a spreadsheet window. `summarize` gives the number of observations, mean, standard deviation, minimum and maximum. `tabulate region` should show 17 regions with 392 months each. The Excel copy can be read too, one sheet at a time, with `import excel "data/stata_data.xlsx", sheet("regional_panel") firstrow clear`; the do-files use the CSV files because they read faster and keep the text columns exactly.

# 3. Step 0: setup

Open Stata and change the working directory with `cd`. If you use the pack:

```stata
cd "C:/Users/yourname/Documents/stata_pack"
do 00_setup.do
```

If you use the repository (on a Mac the path looks like `"/Users/yourname/oil-shock-distribution"`):

```stata
cd "C:/Users/yourname/oil-shock-distribution"
do code/stata/teaching/00_setup.do
```

In the rest of this tutorial the steps are written as `do 01_data.do`; from the repository, put `code/stata/teaching/` in front. The setup file runs these commands:

```stata
version 17
clear all
set more off
global ROOT "`c(pwd)'"
if fileexists("$ROOT/code/stata/teaching/00_setup.do") {
    global TEACH "$ROOT/code/stata/teaching"
    global TOUT  "$ROOT/output/stata_teaching"
}
else if fileexists("$ROOT/00_setup.do") {
    global TEACH "$ROOT"
    global TOUT  "$ROOT/output"
}
global DATA "$TEACH/data"
foreach f in regional_panel national_monthly weights_2018 region_info rq2_weights_decomposition {
    capture confirm file "$DATA/`f'.csv"
    if _rc display as error "Missing data file: $DATA/`f'.csv"
}
capture mkdir "$TOUT"
capture which xtscc
if _rc ssc install xtscc, replace
```

`version 17` makes the code behave the same in later Stata versions. `clear all` empties memory, and `set more off` stops Stata pausing after each screen of output. `` `c(pwd)' `` is the current folder. `fileexists()` returns 1 if a file exists, so the `if` blocks work out whether you started in the repository or in the pack, and set three globals: `$TEACH` (the do-files), `$DATA` (the data) and `$TOUT` (the results). The `foreach` loop stops with a clear message if a data file is missing. `capture` runs a command and ignores its error: `capture mkdir` creates the output folder only if it does not exist. `which xtscc` looks for the command; if it is missing, the return code `_rc` is non-zero and `ssc install` downloads it from the Statistical Software Components archive.

**Check:** Stata prints the data and results folders, then "Set up. Next: do 01_data.do" (with `code/stata/teaching/` in front if you started in the repository).

# 4. Step 1: the data

## 4.1 Read and inspect

```stata
import delimited "$DATA/regional_panel.csv", clear varnames(1) ///
    case(preserve) stringcols(1 2 3 4) bindquote(strict)
describe, short
list region date_str cpi_all cpi_b30 fuel d_fuel d_ratio in 1/3
```

`import delimited` reads a CSV file. `varnames(1)` takes variable names from the first row, `case(preserve)` keeps their lower-case spelling, and `stringcols(1 2 3 4)` reads the first four columns (region code, region name, date as text, date) as text. One row is one region in one month: 17 regions × 392 months. The four variables of the study are 100 times the monthly change in the natural log of an index: `d_fuel` (the fuel shock, from the retail fuel price index 07.2.2), `d_cpi_all` (inflation of all households), `d_cpi_b30` (inflation of low-income households, the poorest 30% by income) and `d_ratio` (the gap, `d_cpi_all` minus `d_cpi_b30`).

## 4.2 Add the national series

```stata
preserve
import delimited "$DATA/national_monthly.csv", clear varnames(1) ///
    case(preserve) stringcols(1 2) bindquote(strict)
keep date_str d_dubai_php d_php_usd d_policy_rate d_ffpi
tempfile nat
save `nat'
restore
merge m:1 date_str using `nat', keep(master match) nogenerate
```

The robustness checks need the world crude price in pesos (`d_dubai_php`) and three other national series. `preserve` saves the panel in memory, so another file can be opened; `restore` brings the panel back. A `tempfile` is a temporary file that disappears when the do-file ends. `merge m:1` attaches the national value of each month to every region in that month: *many* panel rows match *one* national row.

## 4.3 Declare the panel

```stata
generate mdate = monthly(date_str, "YM")
format mdate %tm
encode region, generate(rid)
xtset rid mdate, monthly
xtdescribe
```

`monthly()` turns the text "2001-01" into a Stata monthly date, and `format %tm` displays it as 2001m1. `encode` turns the region code (text) into numbers 1 to 17 with the codes as labels, in alphabetical order. `xtset` declares the panel: unit `rid`, time `mdate`. From now on, `L.` (lag) and `F.` (lead) look back and forward within each region. **Check:** `xtdescribe` reports 17 regions and a balanced panel.

## 4.4 Check the variables, build lags and leads

```stata
generate double chk1 = 100 * (ln(fuel) - ln(L.fuel)) - d_fuel
assert abs(chk1) < 1e-6 if !missing(chk1)
drop chk1
foreach v in cpi_all cpi_b30 ratio fuel dubai_php php_usd policy_rate ffpi {
    forvalues q = 1/12 {
        quietly generate double l`q'_`v' = L`q'.d_`v'
    }
}
foreach v in fuel dubai_php {
    forvalues q = 1/12 {
        quietly generate double f`q'_`v' = F`q'.d_`v'
    }
}
generate byte s01 = mdate >= tm(2001m1)
save "$TOUT/panel.dta", replace
```

The first three lines rebuild the fuel shock from the index level and stop the do-file (`assert`) if it differs from the stored variable. The loops create twelve lags, `l1_cpi_all` to `l12_cpi_all`, and twelve leads, `f1_fuel` to `f12_fuel`, of each variable. `foreach` loops over a list of words and `forvalues` over numbers; `` `q' `` and `` `v' `` take each value in turn. Building the lags once, on the full data, matters for two reasons. Because the panel is declared, the first lag of Region II's first month is missing instead of borrowing Region I's last month. And the first shock month, January 2001, still gets its twelve lags from 2000. The indicator `s01` marks the shock dates the study uses, January 2001 onward.

# 5. Step 2: one local projection by hand

The question at horizon *h* = 6: if fuel prices in a region rise 1% this month, how much higher is that region's price level six months later? Equation (12) of the manuscript answers it with one regression.

```stata
use "$TOUT/panel.dta", clear
xtset rid mdate
generate double cum6 = d_cpi_all
forvalues j = 1/6 {
    replace cum6 = cum6 + F`j'.d_cpi_all
}
local lags  "l1_cpi_all-l12_cpi_all l1_fuel-l12_fuel"
local leads "f1_fuel f2_fuel f3_fuel f4_fuel f5_fuel"
xtreg cum6 d_fuel `lags' `leads' t if s01, fe
xtscc cum6 d_fuel `lags' `leads' t if s01, fe lag(7)
```

`cum6` adds inflation from this month to six months ahead: the percentage change in the price level. The hyphen in `l1_cpi_all-l12_cpi_all` means "every variable from the first to the last in dataset order". The leads 1 to 5 (that is, 1 to *h* − 1) hold constant the fuel price changes that follow the first one. `t` is the time trend. `xtreg ..., fe` estimates with region fixed effects; `xtscc ..., fe lag(7)` gives the same coefficient with Driscoll–Kraay standard errors, which allow errors to be correlated over time and across regions, with *h* + 1 = 7 lags. The `if s01` condition selects the shock dates only: the lags and future outcomes may still come from outside it.

**Check:** the coefficient on `d_fuel` is {{ pn.p_all_c6 }}, standard error {{ pn.p_all_c6_se }}, on 5,117 observations. *Read it:* a 1% fuel price rise raises the price level of all households by about {{ pn.p_all_c6 }}% six months later.

# 6. Step 3: pass-through at every horizon

A local projection repeats step 2 for *h* = 0, 1, …, 12. The do-file first writes the loop out, then wraps it in a program, `panel_lp`, that later steps reuse:

```stata
capture program drop panel_lp
program define panel_lp
    syntax namelist(min=2 max=2) [if], SPEC(string) POST(string) ///
        [CONTROLS(namelist)]
    tokenize `namelist'
    local y `1'
    local x `2'
    forvalues h = 0/12 {
        capture drop cum
        quietly generate double cum = d_`y'
        forvalues j = 1/`h' {
            quietly replace cum = cum + F`j'.d_`y'
        }
        local leads ""
        forvalues l = 1/`=`h'-1' {
            local leads "`leads' f`l'_`x'"
        }
        quietly xtscc cum d_`x' l1_`y'-l12_`y' l1_`x'-l12_`x' ///
            `leads' t `if', fe lag(`=`h'+1')
        post `post' ("`spec'") ("d_`y'") ("d_`x'") (`h') ///
            (_b[d_`x']) (_se[d_`x']) (e(N))
    }
end
```

`program define` creates a new command; `syntax` reads its arguments: two names (the outcome and the shock, without the `d_` prefix), an optional `if` condition, and options. `` `=`h'-1' `` computes *h* − 1 inside a macro; when the upper bound is below 1, `forvalues` runs zero times, so there are no leads at *h* = 0 and 1. After each regression, `_b[d_fuel]` is the coefficient, `_se[d_fuel]` its standard error and `e(N)` the number of observations. `post` writes them as one row of a results file opened with `postfile`:

```stata
tempname R
postfile `R' str40 spec str16 outcome str16 shock int h ///
    double beta se long nobs using "$TOUT/step03.dta", replace
panel_lp cpi_all fuel if s01, spec(baseline) post(`R')
panel_lp cpi_b30 fuel if s01, spec(baseline) post(`R')
postclose `R'
```

**Check:** all households {{ pn.p_all_c0 }}, {{ pn.p_all_c6 }} and {{ pn.p_all_c12 }} at *h* = 0, 6 and 12; low-income households {{ pn.p_b30_c0 }}, {{ pn.p_b30_c6 }} and {{ pn.p_b30_c12 }}. *Read it:* a 10% rise in pump prices leaves the price level about 1% higher a year later, and the low-income price level rises more from the third month.

# 7. Step 4: who pays more?

```stata
postfile `R' str40 spec str16 outcome str16 shock int h ///
    double beta se long nobs using "$TOUT/step04.dta", replace
panel_lp ratio fuel if s01, spec(baseline) post(`R')
postclose `R'
use "$TOUT/step04.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
generate byte significant = (hi < 0) | (lo > 0)
list h beta se lo hi significant, noobs clean
```

The outcome is now the gap. Its cumulative response is negative when low-income households' prices rise more. `lo` and `hi` are the 90% confidence band (1.645 standard errors either side); a band that excludes zero is significant at the 10% level.

**Check:** {{ pn.gap_c6 }} ({{ pn.gap_c6_se }}) at six months and {{ pn.gap_c12 }} ({{ pn.gap_c12_se }}) at twelve; `significant` equals 1 from *h* = {{ pn.gap_sig_from }} to {{ pn.gap_sig_to }}. *Read it:* low-income households' price level rises about {{ pn.gap_rel_pct }}% more ({{ pn.gap_c6|replace("−", "") }} ÷ {{ pn.p_all_c6 }}).

# 8. Step 5: by how much and why

The budget-share calculation (equation 15) asks what the gap would be if both groups faced the same price change within each spending category. It needs the twelve-month response of each of the 13 categories of the national index, and the 2018 budget shares.

```stata
import delimited "$DATA/national_monthly.csv", clear varnames(1) ///
    case(preserve) stringcols(1 2) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate
forvalues c = 1/13 {
    local cc : display %02.0f `c'
    capture drop cum12
    generate double cum12 = d_c`cc'
    forvalues j = 1/12 {
        quietly replace cum12 = cum12 + F`j'.d_c`cc'
    }
    quietly newey cum12 d_fuel L(1/12).d_c`cc' L(1/12).d_fuel ///
        F(1/11).d_fuel t if mdate >= tm(2001m1), lag(13) force
    post `D' ("`cc'") (_b[d_fuel]) (_se[d_fuel])
}
```

This is a single national series, so `tsset` replaces `xtset` and `newey` gives Newey–West standard errors (13 lags for *h* = 12). `L(1/12).d_c01` is Stata's short form for twelve lags; `F(1/11).d_fuel` for eleven leads. `%02.0f` writes 1 as "01", to match the variable names `d_c01` to `d_c13`. The do-file then reads the budget shares, puts the two groups side by side with `reshape wide`, and computes each category's contribution, response × (share of all households − share of low-income households) ÷ 100.

**Check:** food {{ n.dec_food }}, housing and utilities {{ n.dec_housing }}, transport {{ n.dec_transport }}; total {{ n.gap_weights_only }}. *Read it:* on spending shares alone, the effect would be progressive. The estimated gap is regressive, so prices must rise faster within the categories low-income households buy.

# 9. Step 6: does geography matter?

```stata
* (cum and the leads are built for h = 6 as in step 3)
quietly levelsof rid, local(ids)
local sx ""
foreach s of local ids {
    quietly generate double sx_`s' = d_fuel * (rid == `s')
    local sx "`sx' sx_`s'"
}
quietly xtscc cum `sx' l1_ratio-l12_ratio l1_fuel-l12_fuel ///
    `leads' t if s01, fe lag(7)
test sx_1 = sx_2 = sx_3 = sx_4 = sx_5 = sx_6 = sx_7 = sx_8 = ///
     sx_9 = sx_10 = sx_11 = sx_12 = sx_13 = sx_14 = sx_15 = sx_16 = sx_17
```

`levelsof` lists the region numbers. `` (rid == `s') `` equals 1 for region *s* and 0 otherwise, so `sx_s` is the fuel shock of region *s* and zero elsewhere: one shock variable per region. The coefficient on `sx_s` is region *s*'s own response, while the lags, leads, trend and fixed effects stay common. `test` checks whether all 17 coefficients are equal, using the Driscoll–Kraay covariance. Stata reports an *F* statistic; multiplied by its 16 degrees of freedom it is close to the chi-squared statistic in the manuscript. The do-file builds the long `test` line automatically and repeats everything for *h* = 6 and 12 and for both outcomes, then correlates the regional responses with the 2018 poverty rate and food share (`correlate`).

**Check:** six-month pass-through from {{ pn.geo_all_c6_min }} to {{ pn.geo_all_c6_max }}, chi-squared {{ pn.geo_all_c6_wald }}; gap from {{ pn.geo_gap_c6_min }} to {{ pn.geo_gap_c6_max }}, chi-squared {{ pn.geo_gap_c6_wald }} (*p* = {{ pn.geo_gap_c6_p }}); correlation of the gap with poverty {{ pn.geo_gap_c6_corr_pov }}. *Read it:* regions differ significantly, but not along poverty or food spending.

# 10. Step 7: robustness

```stata
panel_lp cpi_all dubai_php if s01, spec(crude in pesos) post(`R')
panel_lp cpi_b30 dubai_php if s01, spec(crude in pesos) post(`R')
panel_lp ratio   dubai_php if s01, spec(crude in pesos) post(`R')
quietly levelsof region, local(regions)
foreach r of local regions {
    panel_lp ratio fuel if s01 & region != "`r'", spec(drop `r') post(`R')
}
```

The first three lines replace the retail fuel price with the world crude price in pesos, which is set in world markets and cannot respond to Philippine conditions. The loop re-estimates the gap 17 times, each time leaving out one region through the `if` condition. The do-file ends with the two estimates reported in the manuscript's limitations: the period split and the world food price control.

**Check:** with crude oil, the six-month gap is {{ pn.rob_crude_c6 }} ({{ pn.rob_crude_c6_se }}); leaving out one region, it stays between {{ pn.loo_min }} and {{ pn.loo_max }}.

# 11. Step 8: did Stata reproduce Python?

`08_check.do` appends the results of steps 3, 4 and 7, merges them with the values the Python pipeline saved (`expected_panel.csv`, `expected_regions.csv`), and reports the largest absolute difference. Point estimates should agree to about 10⁻⁸. Standard errors can differ slightly because `xtscc` and Python's `linearmodels` apply different small-sample corrections; the file reports their ratio. If a difference is large, compare the number of observations first: a different sample is the most common cause.

# 12. Step 9: the figures

`09_figures.do` draws the manuscript's four figures from the saved results, in black and white.

```stata
set scheme s1mono
use "$TOUT/step03.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
twoway (rarea lo hi h if outcome == "d_cpi_all", color(gs13))      ///
       (rline lo hi h if outcome == "d_cpi_b30", lpattern(dot))     ///
       (connected beta h if outcome == "d_cpi_all", msize(small))   ///
       (connected beta h if outcome == "d_cpi_b30", lpattern(dash)  ///
            msymbol(Sh) msize(small)),                              ///
       yline(0) xlabel(0(2)12) xtitle("Months after the shock")     ///
       ytitle("Cumulative response (% per 1% fuel)")                ///
       legend(order(3 "All households" 4 "Low-income households")   ///
              ring(0) position(5) cols(1))
graph export "$TOUT/fig2_passthrough.png", replace width(2000)
```

A `twoway` graph overlays several plots, each in parentheses. `rarea lo hi h` shades the area between the band's limits; `rline` draws the limits as lines; `connected` draws the estimates as points joined by lines. `if` selects the rows of one outcome. `yline(0)` adds the zero line, `xlabel(0(2)12)` labels every second month, and `legend(order(3 4 ...))` keeps only the two estimate lines in the legend. `graph export` saves the picture; `width(2000)` gives a sharp image.

The regional figure uses two further commands. `rcap lo hi pos, horizontal` draws a horizontal confidence interval for each region at height `pos`, and `scatter pos beta` adds the estimate. Region names appear on the vertical axis through a *value label*: the do-file defines a label `posl` that maps 1 to 17 to the region names, ordered by the gap, and attaches it with `label values pos posl`. `graph combine` places the two panels side by side. The trends figure uses `line` and `area` on the national series and `graph combine ..., cols(1)` to stack the three panels.

**Check:** the results folder (`stata_pack/output/` or `output/stata_teaching/`) contains `fig1_trends.png`, `fig2_passthrough.png`, `fig3_gap.png` and `fig4_regions.png`. They should look like Figures 1 to 4 of the manuscript.

# 13. When something goes wrong

Table: Table 4. Common errors and their fixes.

| Message | Cause | Fix |
|---|---|---|
| `command xtscc is unrecognized` | `xtscc` not installed | `ssc install xtscc` (needs internet) |
| `file ... not found` or `Start Stata in ...` | Stata is not in the right folder | `cd` to `stata_pack` (or the repository's top folder); `pwd` shows where Stata is |
| `Missing data file` | The `data/` folder was moved or renamed | Keep `data/` next to the do-files, with the file names unchanged |
| Dates or codes read as numbers | A CSV file was re-saved in Excel | Unzip the pack again; look at the data in `stata_data.xlsx` instead |
| `repeated time values within panel` | Panel declared on the wrong variables | `xtset rid mdate` (region number, monthly date) |
| `variable l1_cpi_all not found` | Step 1 was skipped | Run `01_data.do` first |
| `panel_lp is unrecognized` | Program not defined in this session | Run `03_pass_through.do` first, in the same session |
| `postfile handle already in use` | A previous run stopped half-way | `postclose _all`, then rerun the step |
| `time-series operators not allowed` | Data not declared | `xtset` (panel) or `tsset` (single series) |
| Results differ from Python in the 3rd decimal | Different sample | Compare `e(N)` with the number of observations in the check file |

# 14. The commands at a glance

Table: Table 5. Stata commands used in this tutorial.

| Command | What it does |
|---|---|
| `cd`, `pwd` | Change and show Stata's working folder |
| `import delimited` | Read a CSV file |
| `import excel ..., sheet() firstrow` | Read one sheet of an Excel workbook |
| `browse` | Look at the data in a spreadsheet window |
| `describe`, `list`, `summarize`, `tabulate`, `tabstat` | Inspect variables and values |
| `fileexists()`, `confirm file` | Check that a file is there |
| `merge m:1` | Attach one row of another file to many rows |
| `encode` | Turn text categories into labelled numbers |
| `xtset`, `tsset` | Declare a panel or a time series |
| `L.`, `F.`, `L(1/12).` | Lags and leads |
| `generate`, `replace` | Create and change variables |
| `foreach`, `forvalues` | Loops over words or numbers |
| `local`, `global` | Macros: text that Stata substitutes |
| `xtreg, fe` | Fixed-effects regression |
| `xtscc, fe lag()` | Fixed effects with Driscoll–Kraay standard errors |
| `newey, lag()` | Single series with Newey–West standard errors |
| `test` | Wald test of restrictions on coefficients |
| `postfile`, `post`, `postclose` | Collect results into a new dataset |
| `program define`, `syntax` | Write your own command |
| `twoway`, `rarea`, `rline`, `connected`, `rcap`, `scatter`, `line`, `area` | Graphs |
| `graph combine`, `graph export` | Combine panels; save a figure |
