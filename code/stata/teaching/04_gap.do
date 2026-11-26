* =============================================================================
* STEP 4. RQ2: do the poor pay more? The gap
* -----------------------------------------------------------------------------
* Outcome: the change in the gap, d_ratio = d_cpi_all - d_cpi_b30. Its cumulative
* response is the effect on 100 x ln(CPI all / CPI bottom 30%).
*   negative = the bottom 30%'s prices rise more (regressive)
*   positive = all households' prices rise more (progressive)
* Expected (Python): h=3 -0.0149 (0.0075); h=6 -0.0214 (0.0084); h=12 -0.0173 (0.0085);
*                    90% band excludes zero at every horizon from 3 to 12.
* Requires: the program panel_lp from step 3 (run 03 first in the same session).
* =============================================================================

use "$TOUT/panel.dta", clear
xtset rid mdate
capture program list panel_lp
if _rc {
    display as error "Run 03_pass_through.do first (it defines panel_lp)."
    exit 199
}

tempname R
postfile `R' str40 spec str16 outcome str16 shock int h double beta se long nobs ///
    using "$TOUT/step04.dta", replace
panel_lp ratio fuel if s01, spec(baseline) post(`R')
postclose `R'

use "$TOUT/step04.dta", clear
generate double lo = beta - 1.645 * se
generate double hi = beta + 1.645 * se
generate byte significant = (hi < 0) | (lo > 0)
list h beta se lo hi significant, noobs clean

* 4.1 Size: per 10% fuel price rise, the poor's price level rises about 0.21 points more
*     after six months; the all-household level rises about 0.86% (step 3). 0.0214 / 0.086
*     is about 25%: the poor's prices rise about a quarter more.
display as result "relative gap at h = 6: " %4.1f 100 * (-beta[7]) / 0.0856 "%   (Python: 25%)"

* 4.2 A defense question: step 3 gives 0.105 - 0.086 = 0.0196 at h = 6, the direct gap
*     regression 0.0214. They differ because the separate regressions control for each
*     group's own past inflation, while the gap regression controls for the past gap:
*     different models, not an error. In the panel the two are close.

twoway (rarea lo hi h, color(gs13)) (connected beta h, lcolor(black) mcolor(black) msize(small)), ///
    yline(0, lcolor(black)) xlabel(0(2)12) xtitle("Months after the shock") ///
    ytitle("Cumulative response (pp per 1% fuel)") legend(off) scheme(s1mono)
graph export "$TOUT/step04_gap.png", replace width(1600)
display as text "Next: do ${PFX}05_why.do"
