* =============================================================================
* 02_lp_program.do  The local projection estimator (Stata version of code/python/lp.py)
* -----------------------------------------------------------------------------
* For each horizon h = 0..H the outcome h months ahead (or, by default, the sum of
* the outcome from t to t+h: the cumulative response) is regressed on
*   the shock x_t,
*   p lags of the outcome and of the shock,
*   the Teulings-Zubanov leads x_{t+1}..x_{t+h-1}   (leads(paper), the default, decision D4)
*                      or x_{t+1}..x_{t+h}           (leads(full), decision D13)
*                      or none                        (leads(none)),
*   optional controls (current value and p lags) and exogenous dummies (current only),
*   a linear trend t and a constant;
* national: OLS with Newey-West standard errors, h+1 lags  (newey, force);
* panel   : region fixed effects, Driscoll-Kraay standard errors, h+1 lags (xtscc, fe).
* The -if- condition selects the SHOCK DATES only: lags, leads and future outcomes
* still come from months outside it, exactly as in the Python code.
*
* Each estimate is posted to the frame -results- (created by -lp_results_init-).
*
* Syntax
*   lp_irf depvar [if], shock(varname) rq(string) spec(string)
*          [horizons(12) lags(12) leads(paper|full|none) noncumulative panel
*           controls(varlist) exog(varlist) interact(varlist)]
* =============================================================================

capture program drop lp_results_init
program define lp_results_init
    capture frame drop results
    frame create results str8 rq str40 spec str24 outcome str24 shock str32 term ///
        byte cumulative int h double beta double se long nobs
end

capture program drop lp_irf
program define lp_irf
    version 17
    syntax varname(numeric) [if], SHOCK(varname numeric) RQ(string) SPEC(string) ///
        [HORizons(integer 12) LAGs(integer 12) LEADS(string) NONCUMulative PANEL ///
         CONTROLS(varlist numeric) EXOG(varlist numeric) INTERACT(varlist numeric)]

    local y `varlist'
    if "`leads'" == "" local leads "paper"
    if !inlist("`leads'", "paper", "full", "none") {
        display as error "leads() must be paper, full or none"
        exit 198
    }
    local cum = ("`noncumulative'" == "")

    * controls enter with their current value and p lags
    local ctl ""
    foreach c of local controls {
        local ctl "`ctl' L(0/`lags').`c'"
    }
    * shock x group interactions
    local ix ""
    foreach g of local interact {
        capture drop _ix_`g'
        quietly generate double _ix_`g' = `shock' * `g'
        local ix "`ix' _ix_`g'"
    }

    forvalues k = 0/`horizons' {
        capture drop _dep
        if `cum' {
            quietly generate double _dep = `y'
            forvalues j = 1/`k' {
                quietly replace _dep = _dep + F`j'.`y'
            }
        }
        else {
            quietly generate double _dep = F`k'.`y'
        }
        local ld ""
        if "`leads'" == "paper" & `k' >= 2 local ld "F(1/`=`k'-1').`shock'"
        if "`leads'" == "full"  & `k' >= 1 local ld "F(1/`k').`shock'"

        * turn every lag and lead into a plain (temporary) variable, so that both
        * -newey- and -xtscc- see ordinary regressors
        quietly tsrevar L(1/`lags').`y' L(1/`lags').`shock' `ld' `ctl'
        local tsv "`r(varlist)'"
        local rhs "`shock' `ix' `tsv' `exog' t"

        if "`panel'" != "" {
            quietly xtscc _dep `rhs' `if', fe lag(`=`k'+1')
        }
        else {
            quietly newey _dep `rhs' `if', lag(`=`k'+1') force
        }
        frame post results ("`rq'") ("`spec'") ("`y'") ("`shock'") ("shock") (`cum') (`k') ///
            (_b[`shock']) (_se[`shock']) (e(N))
        foreach g of local interact {
            frame post results ("`rq'") ("`spec'") ("`y'") ("`shock'") ("shock_x_`g'") (`cum') (`k') ///
                (_b[_ix_`g']) (_se[_ix_`g']) (e(N))
        }
    }
    capture drop _dep
    foreach g of local interact {
        capture drop _ix_`g'
    }
end

* a short display of one specification's cumulative responses at h = 0, 6 and 12
capture program drop lp_show
program define lp_show
    syntax, SPEC(string) OUTCOME(string)
    frame results: list rq spec outcome term h beta se nobs ///
        if spec == "`spec'" & outcome == "`outcome'" & cumulative == 1 & inlist(h, 0, 6, 12), ///
        noobs clean
end
