* =============================================================================
* STEP 5. Why the sign? The budget-share calculation (descriptive)
* -----------------------------------------------------------------------------
* If both groups paid the SAME price change within each spending category, their
* inflation would differ only because they spend different shares:
*     gap from budget shares = sum_k  B_k (w_all,k - w_b30,k) / 100
* B_k: twelve-month response of division k of the CPI to a 1% fuel rise
* w_g,k: 2018 budget share of division k in group g's basket (percent)
* Positive = progressive. The division indices for the bottom 30% exist only nationally
* and only from 2013, so B_k comes from the national all-income divisions, 2001-2026.
* Expected (Python): food -0.0124, housing +0.0092, transport +0.0108, total +0.0101.
* This is an accounting exercise outside the regression model: it describes, it does
* not test.
* =============================================================================

* 5.1 Twelve-month responses of the 13 divisions (national series, Newey-West errors).
import delimited "$DATA/national_monthly.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate

tempname D
postfile `D' str2 coicop double beta se using "$TOUT/step05_divisions.dta", replace
forvalues c = 1/13 {
    local cc : display %02.0f `c'
    capture drop cum12
    generate double cum12 = d_c`cc'
    forvalues j = 1/12 {
        quietly replace cum12 = cum12 + F`j'.d_c`cc'
    }
    quietly newey cum12 d_fuel L(1/12).d_c`cc' L(1/12).d_fuel F(1/11).d_fuel t ///
        if mdate >= tm(2001m1), lag(13) force
    post `D' ("`cc'") (_b[d_fuel]) (_se[d_fuel])
}
postclose `D'

* 5.2 The 2018 budget shares of the two baskets.
import delimited "$DATA/weights_2018.csv", clear varnames(1) case(preserve) stringcols(1 2 3 4 5)
keep if geo_code == "old" & region == "PH" & strlen(coicop) == 2
keep basket coicop item weight
reshape wide weight, i(coicop item) j(basket) string
rename (weightall weightb30) (w_all w_b30)

* 5.3 Combine and add up.
merge 1:1 coicop using "$TOUT/step05_divisions.dta", nogenerate
generate double contribution = beta * (w_all - w_b30) / 100
format w_all w_b30 %5.1f
format beta se %6.3f
format contribution %8.4f
list coicop item w_all w_b30 beta contribution, noobs clean abbreviate(14)
quietly summarize contribution
display as result "gap from budget shares alone = " %7.4f r(sum) "    Python: +0.0101"
save "$TOUT/step05.dta", replace

* 5.4 Read it: food pushes the gap toward regressive, because the poor spend 55% of their
*     budget on it against 38%; housing and transport push it the other way. On budget
*     shares alone the rich should lose more. The estimated gap (step 4) is regressive,
*     so prices must rise faster WITHIN the categories the poor buy.
display as text "Next: do ${PFX}06_geography.do"
