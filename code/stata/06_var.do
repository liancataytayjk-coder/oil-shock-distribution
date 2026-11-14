* =============================================================================
* 06_var.do  VAR with fuel ordered first next to the local projections (decision D14)
* Python counterpart: var_irf() in code/python/04_estimate.py (output/tables/var_comparison.csv)
* VAR(12) in (d_fuel, y) with a constant and a linear trend, shock dates 2001m1-2026m8,
* Cholesky ordering with fuel first; the response is scaled to a 1% fuel change on impact.
*   var       : cumulative orthogonalised response / impact response of fuel to its own shock
*   var_onetime: response of y to a single 1% fuel change with later fuel changes held at zero,
*               computed from the y-equation: r_h = b0 f_h + sum_j a_yy(j) r_(h-j) + a_yf(j) f_(h-j),
*               b0 = cov(u_y, u_f) / var(u_f)
* Output: output/stata/var_stata.csv
* =============================================================================

use "$OUT/national.dta", clear
tsset mdate
tempname V
postfile `V' str12 outcome int h double var_cum var_onetime using "$OUT/var_stata.dta", replace

foreach y in d_cpi_all d_ratio {
    quietly var d_fuel `y' if mdate >= tm(2001m1), lags(1/12) exog(t)
    display as text "VAR for `y': " e(N) " months (Python: 308 for d_cpi_all, 307 for d_ratio)"
    matrix Sig = e(Sigma)
    scalar b0 = Sig[2, 1] / Sig[1, 1]

    * one-time fuel change: f_0 = 1, f_h = 0 afterwards
    scalar cum1 = 0
    forvalues h = 0/12 {
        scalar r`h' = cond(`h' == 0, b0, 0)
        forvalues j = 1/`=min(`h', 12)' {
            if `h' >= 1 {
                local op = cond(`j' == 1, "L", "L`j'")
                scalar r`h' = r`h' + _b[`y':`op'.`y'] * r`=`h'-`j''
                if `j' == `h' scalar r`h' = r`h' + _b[`y':`op'.d_fuel]
            }
        }
        scalar cum1 = cum1 + r`h'
        scalar one`h' = cum1
    }

    * standard Cholesky impulse response
    capture erase "$OUT/var_`y'.irf"
    quietly irf create chol, set("$OUT/var_`y'.irf", replace) step(12) replace
    preserve
    use "$OUT/var_`y'.irf", clear
    quietly summarize oirf if impulse == "d_fuel" & response == "d_fuel" & step == 0
    scalar p00 = r(mean)
    keep if impulse == "d_fuel" & response == "`y'"
    sort step
    forvalues h = 0/12 {
        post `V' ("`y'") (`h') (coirf[`=`h'+1'] / p00) (one`h')
    }
    restore
    irf set, clear
}
postclose `V'
use "$OUT/var_stata.dta", clear
list if inlist(h, 0, 6, 12), noobs clean
export delimited using "$OUT/var_stata.csv", replace
