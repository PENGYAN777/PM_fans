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
1. input theta and upstream Mach number, compute downstream data
"""
n = 30
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z1_m2 = np.zeros(n) 
z2_m2 = np.zeros(n) 
z3_m2 = np.zeros(n) 
z4_m2 = np.zeros(n) 
z5_m2 = np.zeros(n) 
z6_m2 = np.zeros(n) 


# z1_P2 = np.zeros(n) 
# z1_T2 = np.zeros(n) 
# z1_D2 = np.zeros(n) 



for i in range(n):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z1.iloc[:,6][np.argmin(abs(z1.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z1.iloc[:,5][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    z1_m2[i] = M2
    # P2 = z1.iloc[:,2][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    # z1_P2[i] = P2
    # D2 = z1.iloc[:,3][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    # z1_D2[i] = D2
    # T2 = z1.iloc[:,4][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    # z1_T2[i] = T2
    # for z2
    nu1 = z2.iloc[:,6][np.argmin(abs(z2.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z2.iloc[:,5][np.argmin(abs(z2.iloc[:,6]-nu2))] 
    z2_m2[i] = M2
    # for z3
    nu1 = z3.iloc[:,6][np.argmin(abs(z3.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z3.iloc[:,5][np.argmin(abs(z3.iloc[:,6]-nu2))] 
    z3_m2[i] = M2
    # for z4
    nu1 = z4.iloc[:,6][np.argmin(abs(z4.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z4.iloc[:,5][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z4_m2[i] = M2
    # for z5
    nu1 = z5.iloc[:,6][np.argmin(abs(z5.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z5.iloc[:,5][np.argmin(abs(z5.iloc[:,6]-nu2))] 
    z5_m2[i] = M2
    # for z6
    nu1 = z6.iloc[:,6][np.argmin(abs(z6.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z6.iloc[:,5][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_m2[i] = M2
    
    
    smallest[i] = min([z1_m2[i],z2_m2[i],z3_m2[i],z4_m2[i],z5_m2[i] ,z6_m2[i]  ])
    largest[i] = max([z1_m2[i],z2_m2[i],z3_m2[i],z4_m2[i],z5_m2[i] ,z6_m2[i]  ])
    diff[i] = (largest[i]-smallest[i])/largest[i] * 100


    


"""
2. plot
"""

nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , z1_m2 , color=colors[2], alpha=0.1, lw=lwh, label="Z71")
axes.plot(theta/math.pi*180  , z2_m2 , color=colors[2], alpha=0.2,lw=lwh,  label="Z72")
axes.plot(theta/math.pi*180  , z3_m2 , color=colors[2], alpha=0.3, lw=lwh, label="Z73")
axes.plot(theta/math.pi*180  , z4_m2 , color=colors[2], alpha=0.4, lw=lwh, label="Z74")
axes.plot(theta/math.pi*180  , z5_m2 , color=colors[2], alpha=0.5, lw=lwh, label="Z75")
axes.plot(theta/math.pi*180  , z6_m2 , color=colors[2], alpha=0.6, lw=lwh, label="Z76")


ax2 = axes.twinx()
ax2.plot(theta/math.pi*180  , diff , 'k*', lw=lwh)
ax2.set_ylabel('$\\Delta M_2$(%)',fontsize=12)
# ax2.set_ylim([0,3])

axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
axes.set_title('$Z_t = 0.7$',fontsize=14)
axes.legend(loc=4 , prop={'size': 10}) # 
fig1.savefig("Ethane_z7_M2_theta.pdf")



