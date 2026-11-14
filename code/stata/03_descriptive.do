* =============================================================================
* 03_descriptive.do  Objective 1: summary statistics, annual inflation, ADF tests
* Python counterpart: code/python/03_descriptive.py (output/tables/desc_*.csv)
* Output: output/stata/desc_summary_stata.csv, desc_annual_stata.csv, desc_adf_stata.csv
* =============================================================================

use "$OUT/national.dta", clear
tsset mdate

* ---- summary statistics of monthly changes by period -------------------------
tempname S
postfile `S' str20 period str12 variable long n double mean sd min max annualised_mean ///
    using "$OUT/desc_summary_stata.dta", replace
local periods `" "2001-2026 (full)" "2001-2012" "2013-2019" "2020-2025" "2026 (Jan-Aug)" "'
local a1 = tm(2001m1)
local b1 = tm(2026m8)
local a2 = tm(2001m1)
local b2 = tm(2012m12)
local a3 = tm(2013m1)
local b3 = tm(2019m12)
local a4 = tm(2020m1)
local b4 = tm(2025m12)
local a5 = tm(2026m1)
local b5 = tm(2026m8)
local i = 0
foreach p of local periods {
    local ++i
    foreach v in d_fuel d_cpi_all d_cpi_b30 d_ratio {
        quietly summarize `v' if inrange(mdate, `a`i'', `b`i'')
        post `S' ("`p'") ("`v'") (r(N)) (r(mean)) (r(sd)) (r(min)) (r(max)) (12 * r(mean))
    }
}
postclose `S'
preserve
use "$OUT/desc_summary_stata.dta", clear
list if period == "2001-2026 (full)", noobs clean
export delimited using "$OUT/desc_summary_stata.csv", replace
restore

* ---- annual averages of year-on-year inflation --------------------------------
foreach v in cpi_all cpi_b30 fuel {
    quietly generate double yoy_`v' = 100 * (`v' / L12.`v' - 1)
}
generate double yoy_gap = yoy_cpi_b30 - yoy_cpi_all
preserve
keep if inrange(mdate, tm(2001m1), tm(2026m8))
collapse (mean) yoy_cpi_all yoy_cpi_b30 yoy_gap yoy_fuel, by(year)
export delimited using "$OUT/desc_annual_stata.csv", replace
quietly count if yoy_gap > 0 & year <= 2025
display as text "bottom-30% inflation higher in " r(N) " of 25 years (2001-2025)"
restore

* ---- augmented Dickey-Fuller tests --------------------------------------------
* Python chooses the lag length by AIC (statsmodels adfuller, autolag="AIC"); Stata's
* -dfuller- takes a fixed lag length, so we use the lag Python chose (desc_adf.csv) and
* compare the statistics.
generate double ln_fuel = ln(fuel)
generate double ln_all  = ln(cpi_all)
generate double ln_b30  = ln(cpi_b30)
generate double ln_ratio = ratio / 100
preserve
import delimited "$TAB/desc_adf.csv", clear varnames(1) stringcols(1 2)
forvalues r = 1/`=_N' {
    local lag`r' = lags[`r']
}
restore
tempname A
postfile `A' str24 series str18 form double adf_stat p_value lags long nobs using "$OUT/desc_adf_stata.dta", replace
local r = 0
foreach v in ln_fuel ln_all ln_b30 ln_ratio {
    local ++r
    quietly dfuller `v' if inrange(mdate, tm(2001m1), tm(2026m8)), trend lags(`lag`r'')
    post `A' ("`v'") ("level") (r(Zt)) (r(p)) (`lag`r'') (r(N))
    local ++r
    quietly dfuller D.`v' if inrange(mdate, tm(2001m2), tm(2026m8)), lags(`lag`r'')
    post `A' ("`v'") ("first difference") (r(Zt)) (r(p)) (`lag`r'') (r(N))
}
postclose `A'
use "$OUT/desc_adf_stata.dta", clear
list, noobs clean
export delimited using "$OUT/desc_adf_stata.csv", replace
