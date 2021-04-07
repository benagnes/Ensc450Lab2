.options brief

***************************************************************
* Title		: inv.inc
* Library 	: stdcells
* Purpose	: Inverter of Scaleable strength
*		
***************************************************************

.subckt IV a z vdd vdds gnd gnds ds=1
Xpmos vdd a z vdds pt_st w=2*ds*Awd# 
Xnmos gnd a z gnds nt_st w=ds*Awd#
.ends

.options brief=1
