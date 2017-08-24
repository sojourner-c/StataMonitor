clear
pause on
set more off
set type double
capture log close

set obs 1
gen x = 1

code_fails_here

exit
