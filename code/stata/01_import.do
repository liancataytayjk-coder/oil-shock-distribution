* =============================================================================
* 01_import.do  Import the cleaned data and check the derived variables
* Input : data/clean/national_monthly.csv, regional_panel.csv, region_info.csv
* Output: output/stata/national.dta, panel.dta
* =============================================================================

* ---- national monthly series ------------------------------------------------
import delimited "$CLEAN/national_monthly.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate, monthly

* every shock and outcome is 100 x the monthly log change of an index level;
* the gap is all-income minus bottom-30% inflation. Rebuild and compare.
foreach pair in "fuel d_fuel" "cpi_all d_cpi_all" "cpi_b30 d_cpi_b30" {
    tokenize `pair'
    quietly generate double _chk = 100 * (ln(`1') - ln(L.`1')) - `2'
    quietly summarize _chk
    if r(N) > 0 & max(abs(r(min)), abs(r(max))) > 1e-6 {
        display as error "`2' does not match 100 x dln(`1')"
        exit 9
    }
    drop _chk
}
quietly generate double _chk = d_cpi_all - d_cpi_b30 - d_ratio
quietly summarize _chk
assert max(abs(r(min)), abs(r(max))) < 1e-6
drop _chk
display as text "national: derived variables check out (" _N " months)"
label data "National monthly series, Jan 1994 - Aug 2026 (from data/clean)"
save "$OUT/national.dta", replace

* ---- region information (groups, poverty threshold) --------------------------
import delimited "$CLEAN/region_info.csv", clear varnames(1) case(preserve) stringcols(1 2)
tempfile info
save `info'

* ---- regional panel ----------------------------------------------------------
import delimited "$CLEAN/regional_panel.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2 3 4) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
encode region, generate(rid)
xtset rid mdate, monthly
merge m:1 region using `info', keepusing(threshold_2023 high_poverty high_food mindanao island) ///
    keep(master match) nogenerate
xtset rid mdate, monthly

quietly generate double _chk = 100 * (ln(fuel) - ln(L.fuel)) - d_fuel
quietly summarize _chk
assert r(N) == 0 | max(abs(r(min)), abs(r(max))) < 1e-6
drop _chk
quietly generate double _chk = d_cpi_all - d_cpi_b30 - d_ratio
quietly summarize _chk
assert max(abs(r(min)), abs(r(max))) < 1e-6
drop _chk
quietly levelsof region
display as text "panel: " r(r) " regions, derived variables check out"
label data "Regional panel, 17 regions (old geographic code)"
save "$OUT/panel.dta", replace
