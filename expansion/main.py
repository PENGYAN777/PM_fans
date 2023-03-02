#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 11:18:57 2022

@author: P.Yan

main function of CoolProp extensions
"""
import os
import CoolProp as CP

# compute active degree of freedom
print("------------compute N-----------")
fluidname = "oxygen"
Pc = CP.CoolProp.PropsSI('Pcrit',fluidname)
Tc = CP.CoolProp.PropsSI('Tcrit',fluidname)
print("fluid name:", fluidname)
R = CP.CoolProp.PropsSI('GAS_CONSTANT',fluidname)
print("Universal gas constant:", R)
MW = CP.CoolProp.PropsSI('M',fluidname)
print("molar mass:", MW)
Rs = R/MW
print("specific gas constant:", Rs)
cv = CP.CoolProp.PropsSI('CVMASS','T', Tc, 'P', Pc*0.1,  fluidname)
Z = CP.CoolProp.PropsSI('Z','T', Tc, 'P', Pc*0.1,  fluidname)
print("Z = :", Z)
N = 2*cv/Rs
print("N = :", N)
