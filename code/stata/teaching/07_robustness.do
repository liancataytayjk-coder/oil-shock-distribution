* =============================================================================
* STEP 7. Robustness: two checks
* -----------------------------------------------------------------------------
*   (i)  shock = world crude price (Dubai, in pesos) instead of the retail fuel price.
*        The retail price is set at home and could respond to the exchange rate or demand;
*        the crude price is set in world markets.
*        Python: all households, 12 months 0.041; gap 6 months -0.0116 (0.0050)
*   (ii) leave one region out at a time.   Python: gap at 6 months between -0.0227 and -0.0203
* Two further estimates, reported in the manuscript's limitations, are at the end:
*   the period split (2001-2012: -0.0541; 2013-2026: -0.0091) and the world food price
*   control (gap -0.0036, not significant).
* Requires panel_lp from step 3.
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
    using "$TOUT/step07.dta", replace

* (i) world crude price in pesos as the shock
panel_lp cpi_all dubai_php if s01, spec(crude in pesos) post(`R')
panel_lp cpi_b30 dubai_php if s01, spec(crude in pesos) post(`R')
panel_lp ratio dubai_php if s01, spec(crude in pesos) post(`R')

* (ii) leave one region out
quietly levelsof region, local(regions)
foreach r of local regions {
    panel_lp ratio fuel if s01 & region != "`r'", spec(drop `r') post(`R')
}

* for the limitations paragraph
panel_lp ratio fuel if s01 & mdate <= tm(2012m12), spec(2001-2012) post(`R')
panel_lp ratio fuel if mdate >= tm(2013m1), spec(2013-2026) post(`R')
panel_lp ratio fuel if s01, spec(food price control) controls(ffpi) post(`R')
postclose `R'

use "$TOUT/step07.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
list spec outcome beta se lo hi if inlist(h, 6, 12) & substr(spec, 1, 5) != "drop ", noobs clean abbreviate(20)
quietly summarize beta if h == 6 & substr(spec, 1, 5) == "drop "
display as result "leave one region out, h = 6: " %7.4f r(min) " to " %7.4f r(max) "   Python: -0.0227 to -0.0203"
display as text "Next: do code/stata/teaching/08_check.do"
