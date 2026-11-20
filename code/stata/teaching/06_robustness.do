* =============================================================================
* STEP 6. Does the gap survive? Five checks
* -----------------------------------------------------------------------------
* Each check changes ONE thing and re-estimates the gap (step 4).
*   (i)   leave one region out at a time        Python, h=6: -0.0227 to -0.0203
*   (ii)  exclude the shock dates of 2008       Python, h=6: -0.0177 (0.0073)
*   (iii) split the period                      2001-2012: -0.0541 (0.0197); 2013-2026: -0.0091 (0.0064)
*   (iv)  shock = Dubai crude oil in pesos      Python, h=6: -0.0116 (0.0050)
*   (v)   controls: exchange rate, policy rate, world food prices
*                                               Python, h=6: -0.0051 (0.0117); food only: -0.0036 (0.0133)
* Excluding a period through the -if- condition removes those months as SHOCK DATES only;
* they still supply lags and future outcomes to the months around them. Deleting the
* rows instead would break the lags of the following year.
* Requires panel_lp from step 3. Running time: several minutes (17 + 7 specifications).
* =============================================================================

use "$TOUT/panel.dta", clear
xtset rid mdate
capture program list panel_lp
if _rc {
    display as error "Run 03_pass_through.do first (it defines panel_lp)."
    exit 199
}

tempname R
postfile `R' str40 spec str16 outcome str16 shock int h double beta se long nobs ///
    using "$TOUT/step06.dta", replace

* (i) leave one region out
quietly levelsof region, local(regions)
foreach r of local regions {
    panel_lp ratio fuel if s01 & region != "`r'", spec(drop `r') post(`R')
}
* (ii) exclude 2008
panel_lp ratio fuel if s01 & year != 2008, spec(excl 2008) post(`R')
* (iii) split the period
panel_lp ratio fuel if s01 & mdate <= tm(2012m12), spec(2001-2012) post(`R')
panel_lp ratio fuel if mdate >= tm(2013m1), spec(2013-2026) post(`R')
* (iv) a price set in world markets as the shock (also for all-household prices)
panel_lp ratio dubai_php if s01, spec(crude in pesos) post(`R')
panel_lp cpi_all dubai_php if s01, spec(crude in pesos) post(`R')
* (v) macroeconomic and food-price controls (current value and 12 lags of each)
panel_lp ratio fuel if s01, spec(macro and food controls) controls(php_usd policy_rate ffpi) post(`R')
panel_lp ratio fuel if s01, spec(food price control) controls(ffpi) post(`R')
postclose `R'

use "$TOUT/step06.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
list spec outcome beta se lo hi if h == 6 & substr(spec, 1, 5) != "drop ", noobs clean abbreviate(24)
quietly summarize beta if h == 6 & substr(spec, 1, 5) == "drop "
display as result "leave one region out, h = 6: " %7.4f r(min) " to " %7.4f r(max) "   Python: -0.0227 to -0.0203"

* Read it: the gap survives (i), (ii) and (iv) and is concentrated in 2001-2012 (iii).
* With world food prices controlled it is no longer distinguishable from zero (v): the
* poor's extra burden moves with food prices. The paper reads food as the channel
* through which fuel reaches the poor, and states that these data cannot separate it.
display as text "Next: do code/stata/teaching/07_2026.do"
