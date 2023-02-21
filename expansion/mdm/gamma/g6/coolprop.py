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
fluidname = "MDM"
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
# dc = CP.CoolProp.PropsSI('Dmass','P',Pc,'T',Tc,fluidname) 
"""
1. input sonic conditions
"""

ps = 0.8*Pc - 0.06*Pc*4# sonic pressure
gs = 0.6 # sonic Gamma
zs, ts = ZTfromPG(ps,gs)
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

D = 1/V
t = T
t = pd.Series(t)
pp = np.zeros(t.size) # Gamma
for i in t.index:
    if abs(t[i]-Tc)<0.01*Tc:
        t[i] = 0.99*Tc
    pp[i] = CP.CoolProp.PropsSI('P','T',t[i],'Dmass',D[i],fluidname)

pd.DataFrame(pp).to_csv('z5.csv', index_label = "Index", header  = ['pressure']) 
data = pd.read_csv("z5.csv", ",")
# append new columns
D =pd.DataFrame({'density': D, 'temperature': t, 'Mach': M,'nu': nu})
newData = pd.concat([data, D], join = 'outer', axis = 1)
# save newData in csv file
# newData.to_csv("m4sh.csv")
newData.to_csv("z5.csv")
