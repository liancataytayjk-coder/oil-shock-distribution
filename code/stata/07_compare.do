* =============================================================================
* 07_compare.do  Does Stata reproduce Python?
* Compares
*   (1) every cumulative local projection estimate with code/stata/expected_results.csv
*       (written by code/python/04_estimate.py);
*   (2) the 2026 fuel-driven rise and peso cost with output/tables/rq3_regional.csv;
*   (3) the VAR responses with output/tables/var_comparison.csv;
*   (4) the summary statistics with output/tables/desc_summary.csv.
* Point estimates should agree to about 1e-8; standard errors may differ by a few
* percent because of different small-sample corrections (reported as a ratio).
* Output: output/stata/compare_report.csv and a summary in the log.
* =============================================================================

* ---- (1) local projections --------------------------------------------------
import delimited "$CODE/expected_results.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2 3 4 5) bindquote(strict)
rename (beta se nobs) (beta_py se_py nobs_py)
tempfile py
save `py'

import delimited "$OUT/estimates_stata.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2 3 4 5) bindquote(strict)
keep if cumulative == 1
drop cumulative
merge 1:1 rq spec outcome shock term h using `py'

display as text _n "Specifications estimated in Stata only (_merge == 1) or Python only (_merge == 2):"
tabulate _merge
generate double diff_beta = abs(beta - beta_py)
generate double ratio_se = se / se_py
generate byte nobs_equal = (nobs == nobs_py)

display as text _n "Absolute difference in point estimates (matched estimates):"
summarize diff_beta if _merge == 3, detail
quietly count if _merge == 3 & diff_beta > 1e-6
local nbad = r(N)
display as text "Estimates differing by more than 1e-6: " as result `nbad'
if `nbad' > 0 {
    list rq spec outcome term h beta beta_py nobs nobs_py if _merge == 3 & diff_beta > 1e-6, ///
        noobs clean abbreviate(12)
}
display as text _n "Ratio of standard errors, Stata / Python:"
summarize ratio_se if _merge == 3, detail
quietly count if _merge == 3 & nobs_equal == 0
display as text "Estimates with a different number of observations: " as result r(N)
export delimited rq spec outcome shock term h beta beta_py diff_beta se se_py ratio_se nobs nobs_py _merge ///
    using "$OUT/compare_report.csv", replace

* ---- (2) the 2026 application -------------------------------------------------
import delimited "$TAB/rq3_regional.csv", clear varnames(1) case(preserve) stringcols(1)
keep region fuel_driven_all fuel_driven_b30 extra_cost_php_month
rename (fuel_driven_all fuel_driven_b30 extra_cost_php_month) (fd_all_py fd_b30_py cost_py)
tempfile r3
save `r3'
import delimited "$OUT/rq3_stata.csv", clear varnames(1) case(preserve) stringcols(1)
merge 1:1 region using `r3', nogenerate
generate double diff_fd_b30 = abs(fd_d_cpi_b30 - fd_b30_py)
generate double diff_cost = abs(extra_cost_php_month - cost_py)
display as text _n "2026: fuel-driven rise in the bottom-30% CPI and peso cost, Stata vs Python"
list region fd_d_cpi_b30 fd_b30_py extra_cost_php_month cost_py, noobs clean
summarize diff_fd_b30 diff_cost

* ---- (3) the VAR ----------------------------------------------------------------
import delimited "$TAB/var_comparison.csv", clear varnames(1) case(preserve) stringcols(1)
keep outcome h var var_onetime
rename (var var_onetime) (var_py onetime_py)
tempfile v
save `v'
import delimited "$OUT/var_stata.csv", clear varnames(1) case(preserve) stringcols(1)
merge 1:1 outcome h using `v', nogenerate
generate double diff_var = abs(var_cum - var_py)
generate double diff_onetime = abs(var_onetime - onetime_py)
display as text _n "VAR: cumulative responses, Stata vs Python"
list outcome h var_cum var_py var_onetime onetime_py if inlist(h, 0, 6, 12), noobs clean
summarize diff_var diff_onetime

* ---- (4) summary statistics -------------------------------------------------------
import delimited "$OUT/desc_summary_stata.csv", clear varnames(1) case(preserve) stringcols(1 2)
keep if period == "2001-2026 (full)"
list variable n mean sd min max, noobs clean
display as text "Compare with output/tables/desc_summary.csv (period 2001–2026 (full))."
