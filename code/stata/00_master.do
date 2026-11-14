* =============================================================================
* Who Pays for Oil Shocks? Stata 17 replication of the Python results
* -----------------------------------------------------------------------------
* Run from the repository's top folder:
*     cd "C:/path/to/oil-shock-distribution"
*     do code/stata/00_master.do
*
* What it does
*   01_import.do        imports the cleaned CSV files (written by the Python pipeline,
*                       data/clean/) and checks every derived variable against the levels
*   02_lp_program.do    defines -lp_irf-, the local projection estimator used everywhere
*   03_descriptive.do   summary statistics, annual inflation, ADF tests (Objective 1)
*   04_estimate.do      RQ1, RQ2, the "why" divisions, every robustness check (Objective 2)
*   05_policy_2026.do   the 2026 out-of-sample test and peso cost by region (Objective 3)
*   06_var.do           VAR with fuel ordered first (decision D14)
*   07_compare.do       compares every Stata estimate with Python's
*                       (code/stata/expected_results.csv and output/tables/*.csv)
*
* Results go to output/stata/. The log is output/stata/stata_log.smcl.
* Needs Stata 17 and the user-written command -xtscc- (Driscoll-Kraay standard errors),
* which this file installs from SSC if it is missing.
*
* Point estimates should equal Python's to about 1e-8. Standard errors can differ
* slightly because the two programs use different small-sample corrections.
* =============================================================================

version 17
clear all
set more off
set varabbrev off

global ROOT  "`c(pwd)'"
global CLEAN "$ROOT/data/clean"
global TAB   "$ROOT/output/tables"
global CODE  "$ROOT/code/stata"
global OUT   "$ROOT/output/stata"

capture confirm file "$CLEAN/national_monthly.csv"
if _rc {
    display as error "Run this file from the repository's top folder (data/clean/ not found)."
    exit 601
}
capture mkdir "$ROOT/output"
capture mkdir "$OUT"

capture which xtscc
if _rc {
    display as text "Installing xtscc from SSC ..."
    ssc install xtscc, replace
}

capture log close _all
log using "$OUT/stata_log.smcl", replace name(main)

timer clear 1
timer on 1
do "$CODE/01_import.do"
do "$CODE/02_lp_program.do"
do "$CODE/03_descriptive.do"
do "$CODE/04_estimate.do"
do "$CODE/05_policy_2026.do"
do "$CODE/06_var.do"
do "$CODE/07_compare.do"
timer off 1
timer list 1

log close main
