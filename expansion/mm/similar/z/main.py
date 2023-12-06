#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 11:18:57 2022

@author: P.Yan

main function of CoolProp extensions
"""
import os
import CoolProp as CP
import math
#os.system('python PT_diagram.py')
#os.system('python plotContour.py')
# new input output pairs
from newIOpairs import TGfromZP, PGfromZT, PTfromZG, ZPfromTG, ZTfromPG, ZGfromPT

#T1,Gamma1 = TGfromZP(0.9, 1e6)

#P2,Gamma2 = PGfromZT(0.9,500)

#P3, T3 =    PTfromZG(0.9, 0.9)

#Z4, P4  = ZPfromTG(500, 0.9)

#Z5, T5  = ZTfromPG(8e6,0.8)

# check consistence of P,T, Z,Gamma
P = 1.57e6
T = 239 + 273.15
# Z,G = ZGfromPT(P,T)

# compute active degree of freedom
print("------------compute N-----------")
fluidname = "MM"


Z = CP.CoolProp.PropsSI('Z','T',T,'P',P,fluidname)
print("Z:",Z)
G = CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',T,'P',P,fluidname)
print("G:",G)

# print('vmax:', math.pi/2*(math.sqrt(2.1/0.1)-1)*180/math.pi)
