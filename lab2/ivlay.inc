.options brief

***************************************************************
* Title		: inv.inc
* Library 	: stdcells
* Purpose	: Inverter of Scaleable strength
*		
***************************************************************

.subckt IVLAY a z vdd vdds gnd gnds ds=1
M1 Z A GND GND  NCH  L=180E-9 W=500E-9 AD=+2.40000000E-13 AS=+2.40000000E-13 
+PD=+1.09600000E-05 PS=+1.09600000E-05 NRD=+5.40000000E-01 NRS=+5.40000000E-01 
+M=1.0 
M0 Z A VDD VDD  PCH  L=180E-9 W=1E-6 AD=+4.80000000E-13 AS=+4.80000000E-13 
+PD=+2.96000000E-06 PS=+2.96000000E-06 NRD=+2.70000000E-01 NRS=+2.70000000E-01 
+M=1.0 
.ends

.options brief=1
