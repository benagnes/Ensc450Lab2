.options brief

***************************************************************
* Title		: nd.inc
* Library 	: stdcells
* Purpose	: Nand of Scaleable strength
*		
***************************************************************

.subckt ND a b z vdd vdds gnd gnds ds=1
* st is stacked
* cd and cs is common source/drain
Xpmos1 vdd a z  vdds pt_st w=2*ds*Awd# 
Xpmos2 vdd b z  vdds pt_st w=2*ds*Awd#
Xnmos1 st  a z  gnds nt_cd w=2*ds*Awd#
Xnmos2 gnd b st gnds nt_cs w=2*ds*Awd#
.ends

.options brief=1
