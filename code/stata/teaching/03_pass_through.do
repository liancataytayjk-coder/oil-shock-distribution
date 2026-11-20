* =============================================================================
* STEP 3. RQ1: pass-through to the price level, every horizon, both groups
* -----------------------------------------------------------------------------
* A local projection is step 2 repeated for h = 0, 1, ..., 12: one regression per
* horizon. Here the loop is written out, then wrapped in a small program (panel_lp)
* that steps 4 to 7 reuse.
* Expected (Python), cumulative response per 1% fuel:
*   all households  h=0 0.047 (0.006)   h=6 0.086 (0.013)   h=12 0.102 (0.016)
*   bottom 30%      h=0 0.046 (0.008)   h=6 0.105 (0.019)   h=12 0.116 (0.023)
* =============================================================================

use "$TOUT/panel.dta", clear
xtset rid mdate

* 3.1 The loop, written out, for all households.
tempname R
postfile `R' str40 spec str16 outcome str16 shock int h double beta se long nobs ///
    using "$TOUT/step03.dta", replace
forvalues h = 0/12 {
    capture drop cum
    generate double cum = d_cpi_all
    forvalues j = 1/`h' {
        quietly replace cum = cum + F`j'.d_cpi_all
    }
    local leads ""
    forvalues l = 1/`=`h'-1' {
        local leads "`leads' f`l'_fuel"
    }
    quietly xtscc cum d_fuel l1_cpi_all-l12_cpi_all l1_fuel-l12_fuel `leads' t if s01, fe lag(`=`h'+1')
    post `R' ("baseline") ("d_cpi_all") ("d_fuel") (`h') (_b[d_fuel]) (_se[d_fuel]) (e(N))
}
* note: "forvalues l = 1/0" runs zero times, so there are no leads at h = 0 and h = 1.

* 3.2 The same loop as a program, so the next steps can call it in one line.
*     panel_lp outcome shock [if], spec(name) [controls(varlist)] post(handle)
*     - outcome: cpi_all, cpi_b30 or ratio  (the d_ prefix is added)
*     - shock:   fuel or dubai_php
*     - controls: names whose lags l1_..l12_ exist; their current value is added too
capture program drop panel_lp
program define panel_lp
    syntax namelist(min=2 max=2) [if], SPEC(string) POST(string) [CONTROLS(namelist)]
    tokenize `namelist'
    local y `1'
    local x `2'
    local ctl ""
    foreach c of local controls {
        local ctl "`ctl' d_`c' l1_`c'-l12_`c'"
    }
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
        quietly xtscc cum d_`x' l1_`y'-l12_`y' l1_`x'-l12_`x' `leads' `ctl' t `if', fe lag(`=`h'+1')
        post `post' ("`spec'") ("d_`y'") ("d_`x'") (`h') (_b[d_`x']) (_se[d_`x']) (e(N))
    }
    capture drop cum
end

* 3.3 Bottom 30%, with the program.
panel_lp cpi_b30 fuel if s01, spec(baseline) post(`R')
postclose `R'

* 3.4 The table and the figure.
use "$TOUT/step03.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
list outcome h beta se nobs if inlist(h, 0, 6, 12), noobs clean sepby(outcome)
twoway (rarea lo hi h if outcome == "d_cpi_all", color(gs13)) ///
       (connected beta h if outcome == "d_cpi_all", lcolor(black) mcolor(black) msize(small)) ///
       (connected beta h if outcome == "d_cpi_b30", lcolor(black) lpattern(dash) mcolor(black) ///
            msymbol(Sh) msize(small)), ///
       yline(0, lcolor(black)) xlabel(0(2)12) xtitle("Months after the shock") ///
       ytitle("Cumulative response (% per 1% fuel)") ///
       legend(order(2 "All households (90% band)" 3 "Bottom 30%") ring(0) position(5) cols(1)) ///
       scheme(s1mono)
graph export "$TOUT/step03_passthrough.png", replace width(1600)

* 3.5 Read it: about half of the one-year effect arrives in the month of the shock
*     (0.047 of 0.102). A 10% rise in pump prices leaves prices about 1% higher a year
*     later. The bottom 30%'s price level rises more from the third month on.
display as text "Next: do code/stata/teaching/04_gap.do"
