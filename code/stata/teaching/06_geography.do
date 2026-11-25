* =============================================================================
* STEP 6. Does geography matter? A response for every region
* -----------------------------------------------------------------------------
* Replace the single shock term B_h f_rt with one term per region:
*     sum_s B_{h,s} (f_rt x 1[r = s])        s = 1..17
* The lags, leads, trend and fixed effects stay common, so each B_{h,s} is region s's
* own response. Then test H0: all 17 responses are equal (a Wald test).
* Expected (Python), six months after a 1% fuel shock:
*   all households: from 0.058 to 0.110; Wald chi2(16) = 55.3, p < 0.001
*   gap:            from -0.053 to +0.009; Wald chi2(16) = 27.7, p = 0.034
*   correlation of the regional gap with the 2018 poverty rate: about 0.2
* Stata's -test- reports an F statistic: F = W / 16 (same p-value up to the small-
* sample correction).
* =============================================================================

use "$TOUT/panel.dta", clear
xtset rid mdate

* 6.1 The interactions: shock x region indicator, one variable per region.
*     -encode- numbered the regions alphabetically (BARMM = 1, CAR = 2, ...), the same
*     order Python uses.
quietly levelsof rid, local(ids)
local sx ""
foreach s of local ids {
    quietly generate double sx_`s' = d_fuel * (rid == `s')
    local sx "`sx' sx_`s'"
}

* 6.2 Estimate for both outcomes at h = 6 and h = 12, and test equality.
tempname G T
postfile `G' str8 region str16 outcome int h double beta se long nobs using "$TOUT/step06.dta", replace
postfile `T' str16 outcome int h double F df1 p using "$TOUT/step06_wald.dta", replace
foreach y in cpi_all ratio {
    foreach h in 6 12 {
        capture drop cum
        quietly generate double cum = d_`y'
        forvalues j = 1/`h' {
            quietly replace cum = cum + F`j'.d_`y'
        }
        local leads ""
        forvalues l = 1/`=`h'-1' {
            local leads "`leads' f`l'_fuel"
        }
        quietly xtscc cum `sx' l1_`y'-l12_`y' l1_fuel-l12_fuel `leads' t if s01, fe lag(`=`h'+1')
        foreach s of local ids {
            local code : label (rid) `s'
            post `G' ("`code'") ("d_`y'") (`h') (_b[sx_`s']) (_se[sx_`s']) (e(N))
        }
        * H0: sx_1 = sx_2 = ... = sx_17
        local eq ""
        foreach s of local ids {
            local eq "`eq' = sx_`s'"
        }
        local eq = substr("`eq'", 4, .)
        quietly test `eq'
        post `T' ("d_`y'") (`h') (r(F)) (r(df)) (r(p))
        display as result "d_`y', h = `h': F(" r(df) ", " r(df_r) ") = " %5.2f r(F) ///
            "  (chi2 = " %5.1f r(F) * r(df) ")  p = " %5.3f r(p)
    }
}
postclose `G'
postclose `T'

* 6.3 How do the regional responses relate to poverty and food spending?
import delimited "$CLEAN/region_info.csv", clear varnames(1) case(preserve) stringcols(1 2)
keep region region_name poverty_2018 food_share_2018
tempfile info
save `info'
use "$TOUT/step06.dta", clear
merge m:1 region using `info', keep(master match) nogenerate
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
sort outcome h beta
list region_name beta se lo hi if outcome == "d_ratio" & h == 6, noobs clean abbreviate(20)
foreach y in d_cpi_all d_ratio {
    foreach h in 6 12 {
        quietly correlate beta poverty_2018 if outcome == "`y'" & h == `h'
        local c1 = r(rho)
        quietly correlate beta food_share_2018 if outcome == "`y'" & h == `h'
        display as text "`y', h = `h': correlation with poverty " %5.2f `c1' ", with food share " %5.2f r(rho)
    }
}

* 6.4 Read it: regions differ, significantly, in how much their prices rise and in how
*     unequally; but the differences do not follow poverty or food shares.
display as text "Next: do code/stata/teaching/07_robustness.do"
