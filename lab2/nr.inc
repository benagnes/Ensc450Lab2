.options brief

***************************************************************
* Title		: nr.inc
* Library 	: stdcells
* Purpose	: Nor of Scaleable strength
*		
***************************************************************

.subckt NR a b z vdd vdds gnd gnds  ds=1
Xpmos1 vdd b st vdds pt_cs w=4*ds*Awd#
Xpmos2 st  a  z vdds pt_cd w=4*ds*Awd#
Xnmos1 gnd a  z gnds nt_st w=ds*Awd#
Xnmos2 gnd b  z gnds nt_st w=ds*Awd#
.ends

.options brief=1
