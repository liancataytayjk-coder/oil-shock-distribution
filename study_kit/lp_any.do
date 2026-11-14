* =============================================================================
* lp_any.do  Run a local projection on ANY dataset in Stata 17
* -----------------------------------------------------------------------------
* Uses -lp_irf- from code/stata/02_lp_program.do. Edit the five lines marked EDIT and run:
*     do study_kit/lp_any.do
* For a single series the data must be -tsset-; for a panel, -xtset- (unit and time).
* Lags, leads and future outcomes respect the declared calendar, so gaps and unit
* boundaries are handled automatically. The -if- condition selects shock dates only.
* =============================================================================

version 17
clear all
set more off
do "code/stata/02_lp_program.do"                  // defines lp_irf, lp_results_init, lp_show

* ---- EDIT: data, time variable, outcome, shock, sample --------------------------
import delimited "data/clean/national_monthly.csv", clear varnames(1) case(preserve)   // EDIT
generate mdate = monthly(date_str, "YM")                                             // EDIT
format mdate %tm
tsset mdate                       // for a panel: encode region, gen(id)  then  xtset id mdate
local y      d_cpi_all            // EDIT: outcome (e.g. monthly inflation, 100 x dln)
local x      d_fuel               // EDIT: shock   (e.g. monthly fuel price change, 100 x dln)
local sample "mdate >= tm(2001m1)"   // EDIT: shock dates to use

* ---- estimate ------------------------------------------------------------------------
lp_results_init
lp_irf `y' if `sample', shock(`x') rq(ANY) spec(my run) horizons(12) lags(12) leads(paper)
*   options: leads(full) or leads(none); noncumulative; panel (needs xtset and xtscc);
*            controls(varlist); exog(varlist); interact(varlist)

* ---- show, save and plot -------------------------------------------------------------
frame results {
    generate double lo = beta - 1.645 * se
    generate double hi = beta + 1.645 * se
    list h beta se lo hi nobs, noobs clean
    export delimited using "lp_result_stata.csv", replace
    twoway (rarea lo hi h, color(gs13)) (connected beta h, lcolor(black) mcolor(black) msize(small)), ///
        yline(0, lcolor(black)) legend(off) xtitle("Periods after the shock (h)") ///
        ytitle("Cumulative response") scheme(s1mono)
    graph export "lp_result_stata.png", replace width(1600)
}
