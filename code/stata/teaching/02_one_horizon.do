* =============================================================================
* STEP 2. One local projection, one horizon, by hand
* -----------------------------------------------------------------------------
* The question at horizon h = 6: if fuel prices in region r rise 1% in month t,
* how much higher is region r's price level six months later?
*
*   sum_{j=0..6} pi_{r,t+j} = u_r + B_6 f_rt + 12 lags of pi + 12 lags of f
*                             + leads f_{r,t+1} .. f_{r,t+5} + delta t + error
*
* u_r  region fixed effect (each region's own average)
* B_6  the cumulative response after six months: the number we want
* Expected (Python): B_6 = 0.0856, standard error 0.0132 (Driscoll-Kraay), 5,117 observations
* =============================================================================

use "$TOUT/panel.dta", clear
xtset rid mdate

* 2.1 The outcome: the SUM of inflation from t to t+6, i.e. the change in the log price
*     level over seven months. F1. ... F6. take future months of the same region.
generate double cum6 = d_cpi_all
forvalues j = 1/6 {
    replace cum6 = cum6 + F`j'.d_cpi_all
}

* 2.2 The right-hand side.
local lags  "l1_cpi_all-l12_cpi_all l1_fuel-l12_fuel"        // 12 lags of inflation and of fuel
local leads "f1_fuel f2_fuel f3_fuel f4_fuel f5_fuel"           // leads 1 to h-1 = 1 to 5
* (the hyphen ranges work because step 1 created the lags in this order)

* 2.3 Fixed effects, ordinary standard errors: the point estimate.
xtreg cum6 d_fuel `lags' `leads' t if s01, fe
display as result "B_6 (xtreg, fe) = " %7.4f _b[d_fuel] "    Python: 0.0856"

* 2.4 The same regression with Driscoll-Kraay standard errors (lag = h + 1 = 7).
*     Why: (i) the outcome overlaps from month to month, so errors are serially
*     correlated; (ii) all regions are hit by the same national events in the same
*     month, so errors are correlated across regions. Driscoll-Kraay allows both.
xtscc cum6 d_fuel `lags' `leads' t if s01, fe lag(7)
display as result "B_6 = " %7.4f _b[d_fuel] "  s.e. = " %6.4f _se[d_fuel] "  N = " e(N) ///
    "    Python: 0.0856 (0.0132), N = 5,117"

* 2.5 Read it: a 1% fuel price rise raises the all-household price level by about
*     0.086% six months later; a 10% rise, by about 0.86%. The point estimate is the
*     same in 2.3 and 2.4; only the standard error changes.
display as text "Next: do ${PFX}03_pass_through.do"
