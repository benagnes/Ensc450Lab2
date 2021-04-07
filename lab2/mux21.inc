.options brief
* Custom User Library
.option search = "/local-scratch/localhome/escmc38/Desktop/ensc450/HSPICE/lab2"

***************************************************************
* Title		: tristate_2to1_mux.inc
* Library 	: stdcells
* Purpose	: 2 to 1 Mutiplexer of Scaleable strength
*             z = not(s)*d0 + s*d1
*		
***************************************************************

.subckt MUX21 s d0 d1 z vdd vdds gnd gnds ds=1
Xinv1 s nots vdd vdds gnd gnds iv ds=ds

Xpmos1 vdd d1 temp1 vdds pt_cd w=4*ds*Awd#
Xpmos2 temp1 nots notz vdds pt_cs w=4*ds*Awd#

Xpmos3 vdd d0 temp2 vdds pt_cd w=4*ds*Awd#
Xpmos4 temp2 s notz vdds pt_cs w=4*ds*Awd#

Xnmos1 gnd d0 temp3 gnds nt_cd w=2*ds*Awd#
Xnmos2 temp3 nots notz gnds nt_cs w=2*ds*Awd#

Xnmos3 gnd d1 temp4 gnds nt_cd w=2*ds*Awd#
Xnmos4 temp4 s notz gnds nt_cs w=2*ds*Awd#

Xinv2 notz z vdd vdds gnd gnds iv ds=ds

.ends

.options brief=1
