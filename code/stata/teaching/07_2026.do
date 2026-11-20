* =============================================================================
* STEP 7. RQ3: the 2026 shock, out of sample
* -----------------------------------------------------------------------------
* 1. Estimate the responses B_h on data that END in December 2025.
* 2. Apply them to the actual 2026 fuel price changes f_1 (January) .. f_8 (August):
*        fuel-driven change in 100 x ln P by August = sum_{s=1..8} B_(8-s) f_s
* 3. Compare with what actually happened; price the bottom-30% change in pesos.
* 4. (optional) A block bootstrap for the uncertainty of the prediction.
* Expected (Python), national fuel path, change Dec 2025 -> Aug 2026:
*     all households 2.62 (actual 4.81); bottom 30% 3.34 (actual 5.98);
*     gap -0.77, 90% band [-1.45, -0.25] (actual -1.18); cost PHP 499 a month; extra PHP 109
* Requires panel_lp from step 3.
* =============================================================================

* 7.0 The national 2026 fuel path, the national price changes and the poverty line.
import delimited "$CLEAN/national_monthly.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate
forvalues s = 1/8 {
    quietly summarize d_fuel if mdate == tm(2025m12) + `s'
    scalar f`s' = r(mean)
}
foreach v in cpi_all cpi_b30 {
    quietly summarize `v' if mdate == tm(2025m12)
    scalar `v'_dec = r(mean)
    quietly summarize `v' if mdate == tm(2026m8)
    scalar act_`v' = 100 * ln(r(mean) / `v'_dec)
}
scalar act_ratio = act_cpi_all - act_cpi_b30
quietly summarize cpi_b30 if inrange(mdate, tm(2023m1), tm(2023m12))
scalar cpi23 = r(mean)
preserve
import delimited "$CLEAN/region_info.csv", clear varnames(1) case(preserve) stringcols(1 2)
quietly summarize threshold_2023 if region == "PH"
scalar thr = r(mean)
restore
scalar line = thr * 5 / 12 * cpi_b30_dec / cpi23
display as text "poverty line, family of five, Dec 2025 prices: PHP " %6.0f line "   (Python: 14,714)"

* 7.1 Estimate on data to December 2025 only. The leads were built on the full data in
*     step 1, so they are rebuilt here: no month after December 2025 may enter.
use "$TOUT/panel.dta", clear
keep if mdate <= tm(2025m12)
xtset rid mdate
drop f*_fuel
forvalues q = 1/12 {
    quietly generate double f`q'_fuel = F`q'.d_fuel
}
capture program list panel_lp
if _rc {
    display as error "Run 03_pass_through.do first (it defines panel_lp)."
    exit 199
}
tempname R
postfile `R' str40 spec str16 outcome str16 shock int h double beta se long nobs ///
    using "$TOUT/step07_irf.dta", replace
foreach y in cpi_all cpi_b30 ratio {
    panel_lp `y' fuel if s01, spec(to Dec 2025) post(`R')
}
postclose `R'

* 7.2 Apply them: sum_s B_(8-s) f_s.
preserve
use "$TOUT/step07_irf.dta", clear
foreach y in cpi_all cpi_b30 ratio {
    scalar fd_`y' = 0
    forvalues s = 1/8 {
        quietly summarize beta if outcome == "d_`y'" & h == 8 - `s'
        scalar fd_`y' = fd_`y' + r(mean) * f`s'
    }
    display as result "`y': fuel-driven " %5.2f fd_`y' "   actual " %5.2f act_`y'
}
restore
scalar cost_b30 = line * (exp(fd_cpi_b30 / 100) - 1)
scalar extra = line * (exp(fd_cpi_b30 / 100) - exp(fd_cpi_all / 100))
display as result "fuel-driven cost, poverty-line family of five: PHP " %4.0f cost_b30 ///
    " a month; extra over average inflation: PHP " %4.0f extra "   (Python: 499 and 109)"

tempname E
postfile `E' str16 series double fuel_driven actual using "$TOUT/step07.dta", replace
post `E' ("d_cpi_all") (fd_cpi_all) (act_cpi_all)
post `E' ("d_cpi_b30") (fd_cpi_b30) (act_cpi_b30)
post `E' ("d_ratio") (fd_ratio) (act_ratio)
postclose `E'

* 7.3 (optional) Uncertainty of the prediction: a block bootstrap.
*     Resample whole 12-month blocks of months (all regions together, so the correlation
*     across regions and within a year is kept), re-estimate all 13 horizons, recompute the
*     prediction. Python uses overlapping ("moving") blocks and 999 draws; here
*     non-overlapping blocks and fewer draws, so the band will be close but not identical.
local REPS 199                                   // set to 0 to skip
if `REPS' > 0 {
    * every variable the regressions need, built before resampling
    foreach y in cpi_all cpi_b30 ratio {
        forvalues h = 0/12 {
            quietly generate double c`h'_`y' = d_`y'
            forvalues j = 1/`h' {
                quietly replace c`h'_`y' = c`h'_`y' + F`j'.d_`y'
            }
        }
    }
    keep if s01
    generate int block = floor((mdate - tm(2001m1)) / 12)
    tempname BS
    postfile `BS' double fd_all fd_b30 fd_gap using "$TOUT/step07_boot.dta", replace
    set seed 20261120
    forvalues r = 1/`REPS' {
        preserve
        quietly bsample, cluster(block)
        foreach y in cpi_all cpi_b30 ratio {
            scalar s_`y' = 0
            forvalues s = 1/8 {
                local h = 8 - `s'
                local leads ""
                forvalues l = 1/`=`h'-1' {
                    local leads "`leads' f`l'_fuel"
                }
                quietly areg c`h'_`y' d_fuel l1_`y'-l12_`y' l1_fuel-l12_fuel `leads' t, absorb(rid)
                scalar s_`y' = s_`y' + _b[d_fuel] * f`s'
            }
        }
        post `BS' (s_cpi_all) (s_cpi_b30) (s_ratio)
        restore
    }
    postclose `BS'
    use "$TOUT/step07_boot.dta", clear
    _pctile fd_gap, percentiles(5 95)
    display as result "gap: 90% bootstrap band [" %5.2f r(r1) ", " %5.2f r(r2) "]   (Python: [-1.45, -0.25])"
}

* Read it: a model that never saw 2026 predicts about half of the price surge and that
* the poor's prices rise more; the band for the gap excludes zero.
display as text "Next: do code/stata/teaching/08_check.do"
