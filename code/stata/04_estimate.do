* =============================================================================
* 04_estimate.do  Objective 2: RQ1, RQ2, the "why" divisions and every robustness check
* Python counterpart: code/python/04_estimate.py (output/tables/estimates.csv)
* Output: output/stata/estimates_stata.csv  (same columns and spec names as Python)
* Every specification is estimated twice in Python (one-month and cumulative outcome);
* here only the cumulative responses, the ones reported in the papers, are estimated.
* Running time: about 15-30 minutes (the panel regressions are the slow part).
* =============================================================================

lp_results_init
local s01 "mdate >= tm(2001m1)"

* ---------------------------------------------------------------- national
use "$OUT/national.dta", clear
tsset mdate

* RQ1: pass-through to the price level of each group
lp_irf d_cpi_all if `s01', shock(d_fuel) rq(RQ1) spec(baseline)
lp_irf d_cpi_b30 if `s01', shock(d_fuel) rq(RQ1) spec(baseline)
lp_show, spec(baseline) outcome(d_cpi_all)

* RQ2: the gap, national
lp_irf d_ratio if `s01', shock(d_fuel) rq(RQ2) spec(national)
lp_show, spec(national) outcome(d_ratio)

* RQ2 why: the 13 divisions of the all-income CPI ...
forvalues c = 1/13 {
    local cc : display %02.0f `c'
    lp_irf d_c`cc' if `s01', shock(d_fuel) rq(WHY) spec(division)
}
* ... and four divisions in both baskets, 2013-2026 (exploratory)
foreach cc in 01 04 07 11 {
    lp_irf d_c`cc'     if mdate >= tm(2013m1), shock(d_fuel) rq(WHY) spec(2013- all income)
    lp_irf d_b30_c`cc' if mdate >= tm(2013m1), shock(d_fuel) rq(WHY) spec(2013- bottom 30%)
}

* core robustness (national)
foreach y in d_cpi_all d_ratio {
    lp_irf `y' if `s01', shock(d_dubai_php) rq(ROB) spec(dubai crude php)
    lp_irf `y' if `s01', shock(d_fuel) rq(ROB) spec(macro controls) controls(d_php_usd d_policy_rate d_ffpi)
    lp_irf `y' if `s01' & year != 2020, shock(d_fuel) rq(ROB) spec(excl 2020)
    lp_irf `y' if `s01', shock(d_fuel) rq(ROB) spec(TZ leads 1..h) leads(full)
}

* appendix robustness (national)
foreach y in d_cpi_all d_ratio {
    lp_irf `y' if `s01', shock(d_fuel) rq(APP) spec(p=6) lags(6)
    lp_irf `y' if `s01', shock(d_fuel) rq(APP) spec(p=18) lags(18)
    lp_irf `y' if `s01' & mdate <= tm(2025m12), shock(d_fuel) rq(APP) spec(excl 2026)
    lp_irf `y' if `s01', shock(d_fuel) rq(APP) spec(splice dummies) exog(jan2012 jan2018)
    lp_irf `y' if `s01', shock(d_fuel) rq(APP) spec(asymmetry) interact(pos)
    lp_irf `y' if `s01' & mdate <= tm(2019m6), shock(d_fuel) rq(APP) spec(to Jun 2019)
    lp_irf `y' if mdate >= tm(2019m1), shock(d_gasoline) rq(APP) spec(gasoline 07.2.2.2)
    lp_irf `y' if mdate >= tm(2018m1), shock(d_wb_gasoline_php) rq(APP) spec(WB pump price)
}
lp_irf d_ratio if `s01' & year != 2008, shock(d_fuel) rq(APP) spec(national excl 2008)
lp_irf d_ratio if mdate >= tm(2013m1), shock(d_fuel) rq(APP) spec(national 2013-2026)

* ---------------------------------------------------------------- panel
use "$OUT/panel.dta", clear
xtset rid mdate

lp_irf d_ratio if `s01', shock(d_fuel) rq(RQ2) spec(panel) panel
lp_show, spec(panel) outcome(d_ratio)

lp_irf d_ratio if `s01', shock(d_fuel) rq(ROB) spec(panel TZ leads 1..h) panel leads(full)
lp_irf d_ratio if `s01' & mdate <= tm(2012m12), shock(d_fuel) rq(ROB) spec(panel 2001-2012) panel
lp_irf d_ratio if mdate >= tm(2013m1), shock(d_fuel) rq(ROB) spec(panel 2013-2026) panel

* leave one region out
quietly levelsof region, local(regions)
foreach r of local regions {
    lp_irf d_ratio if `s01' & region != "`r'", shock(d_fuel) rq(ROB) spec(drop `r') panel
}

* region groups: shock x group indicator (the indicator itself is absorbed by the fixed effects)
foreach g in high_poverty high_food mindanao island {
    lp_irf d_ratio if `s01', shock(d_fuel) rq(APP) spec(x `g') panel interact(`g')
}
lp_irf d_ratio if `s01' & year != 2008, shock(d_fuel) rq(APP) spec(panel excl 2008) panel
lp_irf d_ratio if `s01' & new_geo_ext != 1, shock(d_fuel) rq(APP) spec(drop flagged 2026) panel
lp_irf d_ratio if `s01', shock(d_fuel_nat) rq(APP) spec(national shock) panel

* ---------------------------------------------------------------- save
frame results {
    export delimited using "$OUT/estimates_stata.csv", replace
    display as text _N " estimates written to output/stata/estimates_stata.csv"
}
