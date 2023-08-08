import delimited using "~/github/otree/group_reputation3/__temp_bots_Aug03_03h56m25.1s/all_apps_wide.csv", varnames(1) clear
set scheme burd
rename participant* p_*
rename session* se_*
rename start1* st_*
rename task11* t11_*
rename task21* t21_*
rename task22* t22_*
rename ds1player* ds_p*
rename ds1group* ds_g*
rename ds1subsession* ds_sub*
rename end1* end_*

label define regions   1  "Australia" 2    "Bangladesh" ///
	3 "China (mainland)" 4 "Hong Kong" 5 "Indonesia" /// 
	6 "India" 7 "Malaysia" 8 "Pakistan" 9 "Russia" ///
	10 "Singapore" 11 "Sri Lanka" 12 "Taiwan" 13 "USA" 14 "Vietnam" 15 "Other"


label values t11_playerbirth_region regions

// I want to collect:
//
// Tab of birth regions
// Tab of PI scores
// number of groups of each sort
tab t11_playerbirth_region
tab t11_playerpi_score
tab t11_playerpol_ideology
hist t11_playerpi_score, percent discrete
encode t11_playersorted_by, gen(sorted_by)
tab sorted_by

///////////////////

// use "/Users/thandfie/Dropbox/Papers - on dropbox/15. DP17 project (Erte,Klaus,Lata,John,Toby)/05. Study 5 (Group reputation defence)/Replication Documentation/Processing and Analysis/Analysis Data/group-rep-full-data.dta", clear
//
// gen test = round((0.7*rnormal(34,4.5)) + (0.3*rnormal(43,7)),1)
// replace test = min(test,45)
// twoway (hist test, discrete fcolor(none) lcolor(red)) || (hist task11playerpi_score, discrete fcolor(gs12) lcolor(blue))