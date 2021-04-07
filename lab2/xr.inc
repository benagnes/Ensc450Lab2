.options brief
* Custom User Library
.option search = "/local-scratch/localhome/escmc38/Desktop/ensc450/HSPICE/lab2"

***************************************************************
* Title		: xr.inc
* Library 	: stdcells
* Purpose	: CMOS XOR Gate of Scalable strength
*		
***************************************************************

.subckt XR a b z vdd vdds gnd gnds ds=1
Xnota a nota vdd vdds gnd gnds iv ds=2*ds
Xnotb b notb vdd vdds gnd gnds iv ds=2*ds

Xpmos1 vdd notb temp1 vdds pt_cd w=4*ds*Awd#
Xpmos2 temp1 a z vdds pt_cs w=4*ds*Awd#

Xpmos3 vdd nota temp2 vdds pt_cd w=4*ds*Awd#
Xpmos4 temp2 b z vdds pt_cs w=4*ds*Awd#

Xnmos1 gnd b temp3 gnds nt_cd w=2*ds*Awd#
Xnmos2 temp3 a z gnds nt_cs w=2*ds*Awd#

Xnmos3 gnd notb temp4 gnds nt_cd w=2*ds*Awd#
Xnmos4 temp4 nota z gnds nt_cs w=2*ds*Awd#

.ends

.options brief=1
