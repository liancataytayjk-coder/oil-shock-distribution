* =============================================================================
* STEP 9. The figures of the manuscript, in Stata
* -----------------------------------------------------------------------------
* Draws, from the results saved in steps 3, 4 and 6 (run them first):
*   fig1_trends.png       year-on-year inflation, the difference between the groups, fuel prices
*   fig2_passthrough.png  cumulative response of both price levels, with 90% bands
*   fig3_gap.png          cumulative response of the gap, with 90% band
*   fig4_regions.png      region-specific responses after 6 months, two panels
* All in black and white (scheme s1mono), as journals print them. Output: $TOUT/
* =============================================================================

set scheme s1mono
graph set window fontface "Times New Roman"

* ---------------------------------------------------------------- Figure 1: trends
import delimited "$DATA/national_monthly.csv", clear varnames(1) case(preserve) ///
    stringcols(1 2) bindquote(strict)
generate mdate = monthly(date_str, "YM")
format mdate %tm
tsset mdate
* year-on-year inflation: the percentage change over twelve months
foreach v in cpi_all cpi_b30 fuel {
    generate double yoy_`v' = 100 * (`v' / L12.`v' - 1)
}
generate double yoy_gap = yoy_cpi_b30 - yoy_cpi_all
keep if mdate >= tm(2001m1)

twoway (line yoy_cpi_all mdate, lcolor(black)) (line yoy_cpi_b30 mdate, lcolor(black) lpattern(dash)), ///
    ytitle("% year on year") xtitle("") title("(a) Inflation", size(medsmall) position(11)) ///
    legend(order(1 "All households" 2 "Low-income households") ring(0) position(1) cols(1)) ///
    name(f1a, replace) nodraw
twoway (area yoy_gap mdate, color(gs10)), yline(0, lcolor(black)) ///
    ytitle("pp") xtitle("") title("(b) Low-income minus all households", size(medsmall) position(11)) ///
    name(f1b, replace) nodraw
twoway (line yoy_fuel mdate, lcolor(black)), yline(0, lcolor(black)) ///
    ytitle("% year on year") xtitle("") title("(c) Retail fuel price index", size(medsmall) position(11)) ///
    name(f1c, replace) nodraw
graph combine f1a f1b f1c, cols(1) xsize(6) ysize(7)
graph export "$TOUT/fig1_trends.png", replace width(2000)

* ---------------------------------------------------------------- Figure 2: pass-through
use "$TOUT/step03.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
twoway (rarea lo hi h if outcome == "d_cpi_all", color(gs13) lwidth(none))           ///
       (rline lo hi h if outcome == "d_cpi_b30", lcolor(black) lpattern(dot))           ///
       (connected beta h if outcome == "d_cpi_all", lcolor(black) mcolor(black) msize(small)) ///
       (connected beta h if outcome == "d_cpi_b30", lcolor(black) lpattern(dash)      ///
            mcolor(black) msymbol(Sh) msize(small)),                                     ///
       yline(0, lcolor(black)) xlabel(0(2)12) xtitle("Months after the shock")          ///
       ytitle("Cumulative response (% per 1% fuel)")                                    ///
       legend(order(3 "All households (90% band shaded)" 4 "Low-income households (90% band dotted)") ///
              ring(0) position(5) cols(1))
graph export "$TOUT/fig2_passthrough.png", replace width(2000)

* ---------------------------------------------------------------- Figure 3: the gap
use "$TOUT/step04.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
twoway (rarea lo hi h, color(gs13) lwidth(none))                                    ///
       (connected beta h, lcolor(black) mcolor(black) msize(small)),                 ///
       yline(0, lcolor(black)) xlabel(0(2)12) xtitle("Months after the shock")      ///
       ytitle("Cumulative response (pp per 1% fuel)") legend(off)                   ///
       text(-0.037 6 "Below zero: low-income households' prices rise more", size(small))
graph export "$TOUT/fig3_gap.png", replace width(2000)

* ---------------------------------------------------------------- Figure 4: regions
* pooled estimates at h = 6, drawn as dashed lines
use "$TOUT/step03.dta", clear
quietly summarize beta if outcome == "d_cpi_all" & h == 6
local pooled_all = r(mean)
use "$TOUT/step04.dta", clear
quietly summarize beta if h == 6
local pooled_gap = r(mean)

* region names
import delimited "$DATA/region_info.csv", clear varnames(1) case(preserve) stringcols(1 2)
keep region region_name
tempfile names
save `names'

use "$TOUT/step06.dta", clear
keep if h == 6
merge m:1 region using `names', keep(master match) nogenerate
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
* order the regions by their gap (most negative at the bottom)
bysort region: egen double gap6 = max(cond(outcome == "d_ratio", beta, .))
egen pos = group(gap6)
* turn the positions 1..17 into region names on the vertical axis
preserve
keep if outcome == "d_ratio"
sort pos
forvalues i = 1/`=_N' {
    local nm = region_name[`i']
    label define posl `i' "`nm'", add
}
restore
label values pos posl

twoway (rcap lo hi pos if outcome == "d_cpi_all", horizontal lcolor(black))             ///
       (scatter pos beta if outcome == "d_cpi_all", mcolor(black) msize(small)),         ///
       xline(`pooled_all', lpattern(dash) lcolor(black)) xline(0, lcolor(black))         ///
       ylabel(1(1)17, valuelabel angle(0) labsize(vsmall) nogrid) ytitle("")             ///
       xtitle("Response after 6 months (% per 1% fuel)", size(small))                    ///
       title("(a) Pass-through, all households", size(medsmall) position(11))            ///
       legend(off) name(f4a, replace) nodraw
twoway (rcap lo hi pos if outcome == "d_ratio", horizontal lcolor(black))               ///
       (scatter pos beta if outcome == "d_ratio", mcolor(black) msize(small)),           ///
       xline(`pooled_gap', lpattern(dash) lcolor(black)) xline(0, lcolor(black))         ///
       ylabel(1(1)17, nolabels nogrid) ytitle("")                                        ///
       xtitle("Response after 6 months (pp per 1% fuel)", size(small))                   ///
       title("(b) Gap, all minus low-income", size(medsmall) position(11))               ///
       legend(off) name(f4b, replace) nodraw
graph combine f4a f4b, cols(2) xsize(9) ysize(5)
graph export "$TOUT/fig4_regions.png", replace width(2400)

display as text "Figures written to $TOUT"
