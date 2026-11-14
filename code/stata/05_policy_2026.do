* =============================================================================
* 05_policy_2026.do  Objective 3 / RQ3: the 2026 oil shock (decision D10)
* Python counterpart: code/python/05_policy_2026.py (rq3_national.csv, rq3_regional.csv)
* 1. estimate the cumulative responses on data up to December 2025 only;
* 2. fuel-driven change in 100 x ln CPI from Dec 2025 to Aug 2026 = sum_s B_(8-s) * f_s,
*    s = 1 (January) .. 8 (August);
* 3. peso cost for a family of five at the poverty line:
*    line = 2023 threshold (per person per year) x 5 / 12 x CPI_b30(Dec 2025) / mean CPI_b30(2023)
*    cost = line x (exp(fuel-driven / 100) - 1)
* Output: output/stata/rq3_stata.csv
* =============================================================================

lp_results_init
local s01 "mdate >= tm(2001m1)"

* ---- 1. responses estimated on data to December 2025 --------------------------
use "$OUT/national.dta", clear
keep if mdate <= tm(2025m12)
tsset mdate
foreach y in d_cpi_all d_cpi_b30 d_ratio {
    lp_irf `y' if `s01', shock(d_fuel) rq(RQ3) spec(national to Dec 2025)
}
use "$OUT/panel.dta", clear
keep if mdate <= tm(2025m12)
xtset rid mdate
foreach y in d_cpi_all d_cpi_b30 {
    lp_irf `y' if `s01', shock(d_fuel) rq(RQ3) spec(panel to Dec 2025) panel
}
frame results {
    export delimited using "$OUT/rq3_irf_stata.csv", replace
    foreach sp in national panel {
        foreach y in d_cpi_all d_cpi_b30 d_ratio {
            forvalues h = 0/12 {
                quietly summarize beta if spec == "`sp' to Dec 2025" & outcome == "`y'" & h == `h'
                scalar B_`sp'_`y'_`h' = r(mean)
            }
        }
    }
}

* ---- 2 and 3. apply them to January-August 2026 ------------------------------
* national
use "$OUT/national.dta", clear
keep if inrange(mdate, tm(2026m1), tm(2026m8))
sort mdate
generate s = _n
foreach y in d_cpi_all d_cpi_b30 d_ratio {
    generate double fd_`y' = .
    forvalues k = 1/8 {
        quietly replace fd_`y' = scalar(B_national_`y'_`=8-`k'') * d_fuel if s == `k'
    }
}
collapse (sum) fd_d_cpi_all fd_d_cpi_b30 fd_d_ratio
generate region = "PH"
tempfile ph
save `ph'

* regions: each region's own fuel path with the panel responses
use "$OUT/panel.dta", clear
keep if inrange(mdate, tm(2026m1), tm(2026m8))
bysort region (mdate): generate s = _n
foreach y in d_cpi_all d_cpi_b30 {
    generate double fd_`y' = .
    forvalues k = 1/8 {
        quietly replace fd_`y' = scalar(B_panel_`y'_`=8-`k'') * d_fuel if s == `k'
    }
}
collapse (sum) fd_d_cpi_all fd_d_cpi_b30, by(region)
append using `ph'

* poverty line for a family of five, carried to December 2025 with each region's bottom-30% CPI
tempfile fd
save `fd'
use "$OUT/panel.dta", clear
append using "$OUT/national.dta", generate(_nat)
replace region = "PH" if _nat == 1
generate year_ = year(dofm(mdate))
bysort region: egen double cpi23 = mean(cond(year_ == 2023, cpi_b30, .))
keep if mdate == tm(2025m12)
keep region cpi_b30 cpi23
merge 1:1 region using `fd', nogenerate
preserve
import delimited "$CLEAN/region_info.csv", clear varnames(1) case(preserve) stringcols(1 2)
keep region threshold_2023
tempfile th
save `th'
restore
merge 1:1 region using `th', keep(master match) nogenerate
generate double poverty_line_family5 = threshold_2023 * 5 / 12 * cpi_b30 / cpi23
generate double extra_cost_php_month = poverty_line_family5 * (exp(fd_d_cpi_b30 / 100) - 1)
order region fd_d_cpi_all fd_d_cpi_b30 fd_d_ratio poverty_line_family5 extra_cost_php_month
list region fd_d_cpi_all fd_d_cpi_b30 extra_cost_php_month, noobs clean
export delimited using "$OUT/rq3_stata.csv", replace
