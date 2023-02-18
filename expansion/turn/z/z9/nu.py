#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:04:05 2023

compute downstream Mach number  for nonideal flow

@author: yan
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import CoolProp as CP
"""
0. get data
"""
z1= pd.read_csv("z1.csv", ",", skiprows=0)
# z2= pd.read_csv("z2.csv", ",", skiprows=0)
# z3= pd.read_csv("z3.csv", ",", skiprows=0)
# z4= pd.read_csv("z4.csv", ",", skiprows=0)
# z5= pd.read_csv("z5.csv", ",", skiprows=0)
# z6= pd.read_csv("z6.csv", ",", skiprows=0)



"""
1. find M^* and compute nu(M^*)
"""
fluidname = "MM"
P1 = z1.iloc[0,2]
T1 = z1.iloc[0,4]
Z1 = CP.CoolProp.PropsSI('Z','P',P1,'T',T1,fluidname) 
G1 = CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','P',P1,'T',T1,fluidname)

M1 = math.sqrt(1/(1-G1)) # upstream Mach number
# # for z1
# z1_nu = z1.iloc[:,6][np.argmin(abs(z1.iloc[:,5]-M1))] 



    


"""
2. plot
"""
# n = 10
# colors = plt.cm.tab20(np.linspace(0, 1, n))

# fig1 = plt.figure( dpi=300)
# lwh = 2
# axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# axes.plot(z  , nu , 'ko', lw=lwh)


# axes.set_xlabel('$Z_1$',fontsize=12)
# axes.set_ylabel('$\\nu^*(M^*)$',fontsize=12) 
# axes.set_title('$\\nu^*(M^*)$ vs $Z_1$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
# fig1.savefig("g9_nu_z.pdf")


