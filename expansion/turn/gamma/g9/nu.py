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

"""
0. get data
"""
z1= pd.read_csv("z1.csv", ",", skiprows=0)
z2= pd.read_csv("z2.csv", ",", skiprows=0)
z3= pd.read_csv("z3.csv", ",", skiprows=0)
z4= pd.read_csv("z4.csv", ",", skiprows=0)
z5= pd.read_csv("z5.csv", ",", skiprows=0)
z6= pd.read_csv("z6.csv", ",", skiprows=0)



"""
1. ifind M^* and compute nu(M^*)
"""
gamma = 0.9


M = math.sqrt(1/(1-gamma)) # upstream Mach number
# for z1
z1_nu = z1.iloc[:,6][np.argmin(abs(z1.iloc[:,5]-M))] 
z2_nu = z2.iloc[:,6][np.argmin(abs(z2.iloc[:,5]-M))] 
z3_nu = z3.iloc[:,6][np.argmin(abs(z3.iloc[:,5]-M))] 
z4_nu = z4.iloc[:,6][np.argmin(abs(z4.iloc[:,5]-M))] 
z5_nu = z5.iloc[:,6][np.argmin(abs(z5.iloc[:,5]-M))] 
z6_nu = z6.iloc[:,6][np.argmin(abs(z6.iloc[:,5]-M))] 


z = [0.85, 0.8, 0.75, 0.7, 0.65, 0.6]
nu = [z1_nu, z2_nu, z3_nu, z4_nu, z5_nu, z6_nu]    


    


"""
2. plot
"""
# n = 10
# colors = plt.cm.tab20(np.linspace(0, 1, n))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(z  , nu , 'ko', lw=lwh)


axes.set_xlabel('$Z_1$',fontsize=12)
axes.set_ylabel('$\\nu^*(M^*)$',fontsize=12) 
axes.set_title('$\\nu^*(M^*)$ vs $Z_1$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("g9_nu_z.pdf")


