* =============================================================================
* TEACHING SEQUENCE, step 0: set up
* Who Pays for Oil Shocks?  Fuel price pass-through in the Philippine regional panel
* -----------------------------------------------------------------------------
* Run the steps in order, from the repository's top folder:
*     do code/stata/teaching/00_setup.do
*     do code/stata/teaching/01_data.do
*     do code/stata/teaching/02_one_horizon.do      ... and so on to 08_check.do
* Each step explains what it does and prints the value Python obtained, so you can
* see your own result appear next to it. Step 08 checks every result at once.
* Needs Stata 17 and -xtscc- (Driscoll-Kraay standard errors; installed below).
* =============================================================================

version 17
clear all
set more off
set varabbrev off

global ROOT  "`c(pwd)'"
global CLEAN "$ROOT/data/clean"
global TEACH "$ROOT/code/stata/teaching"
global TOUT  "$ROOT/output/stata_teaching"

capture confirm file "$CLEAN/regional_panel.csv"
if _rc {
    display as error "Run this file from the repository's top folder (data/clean/ not found)."
    exit 601
}
capture mkdir "$ROOT/output"
capture mkdir "$TOUT"

capture which xtscc
if _rc ssc install xtscc, replace

display as text "Set up. Next: do code/stata/teaching/01_data.do"
