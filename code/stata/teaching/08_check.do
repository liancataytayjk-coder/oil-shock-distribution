* =============================================================================
* STEP 8. Did Stata reproduce Python?
* -----------------------------------------------------------------------------
* Compares every result of steps 3-7 with the values the Python pipeline wrote
* (code/stata/teaching/expected_panel.csv, expected_2026.csv and
* output/tables/rq2_weights_decomposition.csv).
* Point estimates should agree to about 1e-8. Standard errors may differ a little,
* because -xtscc- and Python's -linearmodels- use different small-sample corrections.
* =============================================================================

* 8.1 Local projections (steps 3, 4 and 6)
use "$TOUT/step03.dta", clear
append using "$TOUT/step04.dta" "$TOUT/step06.dta"
tempfile st
save `st'
import delimited "$TEACH/expected_panel.csv", clear varnames(1) case(preserve) stringcols(1 2 3 4)
drop rq
rename (beta se nobs) (beta_py se_py nobs_py)
merge 1:1 spec outcome shock h using `st'
display as text _n "matched estimates (_merge == 3); Stata-only rows are the other left-out regions:"
tabulate _merge
generate double diff = abs(beta - beta_py)
generate double se_ratio = se / se_py
summarize diff se_ratio if _merge == 3
quietly count if _merge == 3 & diff > 1e-6
display as result "estimates differing by more than 1e-6: " r(N)
list spec outcome h beta beta_py if _merge == 3 & diff > 1e-6, noobs clean
quietly count if _merge == 3 & nobs != nobs_py
display as result "estimates with a different number of observations: " r(N)

* 8.2 The budget-share calculation (step 5)
import delimited "$ROOT/output/tables/rq2_weights_decomposition.csv", clear varnames(1) ///
    case(preserve) stringcols(1)
keep coicop contrib_gap
merge 1:1 coicop using "$TOUT/step05.dta", nogenerate
generate double diff = abs(contribution - contrib_gap)
summarize diff
display as result "largest difference in a division's contribution: " %9.2e r(max)

* 8.3 The 2026 prediction (step 7)
import delimited "$TEACH/expected_2026.csv", clear varnames(1) case(preserve) stringcols(1)
rename (fuel_driven actual) (fd_py act_py)
merge 1:1 series using "$TOUT/step07.dta", nogenerate
generate double diff = abs(fuel_driven - fd_py)
list series fuel_driven fd_py actual act_py diff, noobs clean
display as text _n "Done. If every difference is below 1e-6, Stata reproduces the study."
