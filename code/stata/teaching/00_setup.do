* =============================================================================
* TEACHING SEQUENCE, step 0: set up
* Who Pays for Oil Shocks?  Fuel price pass-through in the Philippine regional panel
* -----------------------------------------------------------------------------
* Start Stata in EITHER folder, then run the steps in order:
*   (a) the repository's top folder:   do code/stata/teaching/00_setup.do
*   (b) the unzipped stata_pack folder: do 00_setup.do
* The data are in the subfolder data/ next to this file (CSV files, and the same
* tables in data/stata_data.xlsx with a data dictionary). Nothing has to be built first.
* Each step explains what it does and prints the value Python obtained, so you can
* see your own result appear next to it. Step 08 checks every result at once.
* Needs Stata 17 and -xtscc- (Driscoll-Kraay standard errors; installed below).
* =============================================================================

version 17
clear all
set more off
set varabbrev off

* 0.1 Where am I? Find the folder that holds the do-files.
global ROOT "`c(pwd)'"
if fileexists("$ROOT/code/stata/teaching/00_setup.do") {
    global TEACH "$ROOT/code/stata/teaching"           // (a) started in the repository
    global TOUT  "$ROOT/output/stata_teaching"
    global PFX   "code/stata/teaching/"                // how to call the next step
}
else if fileexists("$ROOT/00_setup.do") {
    global TEACH "$ROOT"                               // (b) started in stata_pack
    global TOUT  "$ROOT/output"
    global PFX   ""
}
else {
    display as error "Start Stata in the repository's top folder or in the stata_pack folder (use cd)."
    exit 601
}
global DATA "$TEACH/data"

* 0.2 Are all the data files there?
foreach f in regional_panel national_monthly weights_2018 region_info rq2_weights_decomposition {
    capture confirm file "$DATA/`f'.csv"
    if _rc {
        display as error "Missing data file: $DATA/`f'.csv"
        exit 601
    }
}

* 0.3 A folder for the results, and the one user-written command.
capture mkdir "$ROOT/output"
capture mkdir "$TOUT"
capture which xtscc
if _rc ssc install xtscc, replace

display as text "Data:    $DATA"
display as text "Results: $TOUT"
display as text "Set up. Next: do ${PFX}01_data.do"
