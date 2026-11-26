* =============================================================================
* STEP 1. The data: one panel of 17 regions, monthly, 1994-2026
* -----------------------------------------------------------------------------
* What you learn: how the panel is organised, how to declare it to Stata (xtset),
* and why lags and leads must be built WITHIN each region.
* Output: $TOUT/panel.dta
* =============================================================================

* 1.1 Read the panel. One row = one region in one month.
import delimited "$DATA/regional_panel.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2 3 4) bindquote(strict)
describe, short
list region date_str cpi_all cpi_b30 fuel d_cpi_all d_cpi_b30 d_fuel d_ratio in 1/3, noobs clean

* The four variables of the study (all are 100 x the monthly log change):
*   d_fuel     the fuel shock f_rt: CPI sub-index 07.2.2, fuels for personal transport, region r, month t
*   d_cpi_all  inflation of all households in region r
*   d_cpi_b30  inflation of low-income households (the poorest 30% by income) in region r
*   d_ratio    the gap: d_cpi_all - d_cpi_b30  (negative = the poor's prices rose more)

* 1.2 Add the national monthly series used in the robustness checks. They are the same
*     for every region in a given month, so they are merged by month.
preserve
import delimited "$DATA/national_monthly.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2) bindquote(strict)
keep date_str d_dubai_php d_php_usd d_policy_rate d_ffpi
tempfile nat
save `nat'
restore
merge m:1 date_str using `nat', keep(master match) nogenerate

* 1.3 Declare the panel: unit = region, time = month.
generate mdate = monthly(date_str, "YM")
format mdate %tm
encode region, generate(rid)
xtset rid mdate, monthly
xtdescribe

* 1.4 Check the variables: rebuild them from the index levels.
generate double chk1 = 100 * (ln(fuel) - ln(L.fuel)) - d_fuel
generate double chk2 = d_cpi_all - d_cpi_b30 - d_ratio
summarize chk1 chk2
assert abs(chk1) < 1e-6 if !missing(chk1)
assert abs(chk2) < 1e-6 if !missing(chk2)
drop chk1 chk2

* 1.5 Build lags (past values) and leads (future values) ONCE, on the full data.
*     Because the panel is xtset, L. and F. never cross from one region into another:
*     the first month of Region II has a missing lag, not the last month of Region I.
*     We build them before restricting the sample, so January 2001 still gets its
*     twelve lags from 2000.
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
* the shock dates used in the study: January 2001 to August 2026
generate byte s01 = mdate >= tm(2001m1)

* 1.6 A first look: average monthly changes, 2001-2026.
tabstat d_fuel d_cpi_all d_cpi_b30 d_ratio if s01, statistics(n mean sd min max) columns(statistics)

label data "Regional panel for the teaching sequence"
save "$TOUT/panel.dta", replace
display as text "Saved. Next: do ${PFX}02_one_horizon.do"
