#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:35:29 2022

@author: yan

compute Prandtl-Meyer relatiomnships for CoolProp EOS
input: upstream P,Z,M and defletion angle theta.

"""

from scipy.optimize import fsolve
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import CoolProp as CP
from newIOpairs import TGfromZP, PGfromZT, PTfromZG, ZPfromTG, ZTfromPG, ZGfromPT
from RK4 import rk4

"""
0. fluid property
"""
fluidname = "MM"
print("Fluid name:", fluidname)
R = CP.CoolProp.PropsSI("gas_constant",fluidname)
print("universal gas constant:  J/mol/K", R)
W = CP.CoolProp.PropsSI("molar_mass",fluidname)
print("molar mass: kg/mol", W)
Rs = R/W
print("spefific ags constant: J/Kg/K", Rs)
Tc =  CP.CoolProp.PropsSI("Tcrit",fluidname)
print("critical temperature[K]:", Tc)
Pc =  CP.CoolProp.PropsSI("pcrit",fluidname)
print("critical pressure[Pa]:", Pc)
dc = CP.CoolProp.PropsSI('Dmass','P',Pc,'T',Tc,fluidname) 
"""
1. input sonic conditions
"""

# zs = 0.75,0.74,0.71, 0.70, 0.60,0.65,
zs = 0.60# 
gs = 0.7 # 
ps, ts = PTfromZG(zs, gs)
ds = CP.CoolProp.PropsSI('Dmass','P',ps,'T',ts,fluidname) 
Z = CP.CoolProp.PropsSI('Z','P',ps,'T',ts,fluidname)
G = CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','P',ps,'T',ts,fluidname)
print("Z,G:",Z,G)
print("Ps,Ts:",ps,ts)
"""
2. compute data 
"""
V,T,M,nu = rk4(1/ds, 10/ds, ts, 1, 0, 1000)

"""
5. write into csv file
"""    

D = 1/V/dc
t = T/Tc
t = pd.Series(t)
pp = np.zeros(t.size) # Gamma
for i in t.index:
    pp[i] = CP.CoolProp.PropsSI('P','T',t[i]*Tc,'Dmass',D[i]*dc,fluidname)/Pc

pd.DataFrame(pp).to_csv('z5.csv', index_label = "Index", header  = ['pressure']) 
data = pd.read_csv("z5.csv", ",")
# append new columns
D =pd.DataFrame({'density': D, 'temperature': t, 'Mach': M,'nu': nu})
newData = pd.concat([data, D], join = 'outer', axis = 1)
# save newData in csv file
# newData.to_csv("m4sh.csv")
newData.to_csv("z5.csv")
