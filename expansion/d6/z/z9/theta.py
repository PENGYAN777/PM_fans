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
n = 50
theta = np.zeros(n) # rad
smallest_m = np.zeros(n) # min Mach
largest_m = np.zeros(n) # max Mach
diff_m = np.zeros(n) # diff Mach

smallest_p = np.zeros(n) # min P
largest_p = np.zeros(n) # max P
diff_p = np.zeros(n) # diff P

z1_m2 = np.zeros(n) 
z2_m2 = np.zeros(n) 
z3_m2 = np.zeros(n) 
z4_m2 = np.zeros(n) 
z5_m2 = np.zeros(n) 
z6_m2 = np.zeros(n) 


z1_P2 = np.zeros(n) 
z2_P2 = np.zeros(n) 
z3_P2 = np.zeros(n) 
z4_P2 = np.zeros(n) 
z5_P2 = np.zeros(n) 
z6_P2 = np.zeros(n) 




for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z1.iloc[:,6][np.argmin(abs(z1.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z1.iloc[:,5][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    z1_m2[i] = M2
    P2 = z1.iloc[:,2][np.argmin(abs(z1.iloc[:,6]-nu2))] 
    z1_P2[i] = P2
    # for z2
    nu1 = z2.iloc[:,6][np.argmin(abs(z2.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z2.iloc[:,5][np.argmin(abs(z2.iloc[:,6]-nu2))] 
    z2_m2[i] = M2
    P2 = z2.iloc[:,2][np.argmin(abs(z2.iloc[:,6]-nu2))] 
    z2_P2[i] = P2
    # for z3
    nu1 = z3.iloc[:,6][np.argmin(abs(z3.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z3.iloc[:,5][np.argmin(abs(z3.iloc[:,6]-nu2))] 
    z3_m2[i] = M2
    P2 = z3.iloc[:,2][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z3_P2[i] = P2
    # for z4
    nu1 = z4.iloc[:,6][np.argmin(abs(z4.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z4.iloc[:,5][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z4_m2[i] = M2
    P2 = z4.iloc[:,2][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z4_P2[i] = P2
    # for z5
    nu1 = z5.iloc[:,6][np.argmin(abs(z5.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z5.iloc[:,5][np.argmin(abs(z5.iloc[:,6]-nu2))] 
    z5_m2[i] = M2
    P2 = z5.iloc[:,2][np.argmin(abs(z5.iloc[:,6]-nu2))] 
    z5_P2[i] = P2
    # for z6
    nu1 = z6.iloc[:,6][np.argmin(abs(z6.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z6.iloc[:,5][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_m2[i] = M2
    P2 = z6.iloc[:,2][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_P2[i] = P2
    
    smallest_m[i] = min([z1_m2[i],z2_m2[i],z3_m2[i],z4_m2[i],z5_m2[i], z6_m2[i] ])
    largest_m[i] = max([z1_m2[i],z2_m2[i],z3_m2[i],z4_m2[i],z5_m2[i], z6_m2[i] ])
    diff_m[i] = (largest_m[i]-smallest_m[i])/largest_m[i] * 100
    
    smallest_p[i] = min([(z1.iloc[0,-1]-z1_P2[i]*z1.iloc[1,-1])/z1.iloc[0,-1], (z2.iloc[0,-1]-z2_P2[i]*z2.iloc[1,-1])/z2.iloc[0,-1],(z3.iloc[0,-1]-z3_P2[i]*z3.iloc[1,-1])/z3.iloc[0,-1],
                         (z4.iloc[0,-1]-z1_P2[i]*z4.iloc[1,-1])/z4.iloc[0,-1],(z5.iloc[0,-1]-z5_P2[i]*z5.iloc[1,-1])/z5.iloc[0,-1],(z6.iloc[0,-1]-z6_P2[i]*z6.iloc[1,-1])/z6.iloc[0,-1]]) 
    largest_p[i] = max([(z1.iloc[0,-1]-z1_P2[i]*z1.iloc[1,-1])/z1.iloc[0,-1], (z2.iloc[0,-1]-z2_P2[i]*z2.iloc[1,-1])/z2.iloc[0,-1],(z3.iloc[0,-1]-z3_P2[i]*z3.iloc[1,-1])/z3.iloc[0,-1],
                         (z4.iloc[0,-1]-z1_P2[i]*z4.iloc[1,-1])/z4.iloc[0,-1],(z5.iloc[0,-1]-z5_P2[i]*z5.iloc[1,-1])/z5.iloc[0,-1],(z6.iloc[0,-1]-z6_P2[i]*z6.iloc[1,-1])/z6.iloc[0,-1]])
    diff_p[i] = (largest_p[i]-smallest_p[i])/largest_p[i] * 100

    


"""
2. plot
"""
n = 10
colors = plt.cm.tab20(np.linspace(0, 1, n))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , z1_m2 , color=colors[1], alpha=0.1, lw=lwh, label="Z91")
axes.plot(theta/math.pi*180  , z2_m2 , color=colors[1], alpha=0.2,lw=lwh, label="Z92")
axes.plot(theta/math.pi*180  , z3_m2 , color=colors[1], alpha=0.3, lw=lwh, label="Z93")
axes.plot(theta/math.pi*180  , z4_m2 , color=colors[1], alpha=0.4, lw=lwh, label="Z94")
axes.plot(theta/math.pi*180  , z5_m2 , color=colors[1], alpha=0.5, lw=lwh, label="Z95")
axes.plot(theta/math.pi*180  , z6_m2 , color=colors[1], alpha=0.6, lw=lwh, label="Z96")

ax2 = axes.twinx()
ax2.plot(theta/math.pi*180  , diff_m , 'k*', lw=lwh)
ax2.set_ylabel('$\\Delta M_2$(%)',fontsize=12)


axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
axes.set_title('$Z_t = 0.9$',fontsize=14)
# axes.legend(loc=4 , prop={'size': 10}) # 
fig1.savefig("d6_Z9_M2_theta.eps")

###################################################################

fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , (z1.iloc[0,-1]-z1_P2*z1.iloc[1,-1])/z1.iloc[0,-1] , color=colors[1], alpha=0.1, lw=lwh, label="Z91")
axes.plot(theta/math.pi*180  , (z2.iloc[0,-1]-z2_P2*z2.iloc[1,-1])/z2.iloc[0,-1], color=colors[1], alpha=0.2,lw=lwh, label="Z92")
axes.plot(theta/math.pi*180  , (z3.iloc[0,-1]-z3_P2*z3.iloc[1,-1])/z3.iloc[0,-1] , color=colors[1], alpha=0.3, lw=lwh, label="Z93")
axes.plot(theta/math.pi*180  , (z4.iloc[0,-1]-z4_P2*z4.iloc[1,-1])/z4.iloc[0,-1] , color=colors[1], alpha=0.4, lw=lwh, label="Z94")
axes.plot(theta/math.pi*180  , (z5.iloc[0,-1]-z5_P2*z5.iloc[1,-1])/z5.iloc[0,-1] , color=colors[1], alpha=0.5, lw=lwh, label="Z95")
axes.plot(theta/math.pi*180  , (z6.iloc[0,-1]-z6_P2*z6.iloc[1,-1])/z6.iloc[0,-1], color=colors[1], alpha=0.6, lw=lwh, label="Z96")

ax2 = axes.twinx()
ax2.plot(theta/math.pi*180  , abs(diff_p) , 'k*', lw=lwh)
ax2.set_ylabel('diff of $\\Delta P$(%)',fontsize=12)
# ax2.set_ylim(0,2 )

axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$\\Delta P$',fontsize=12) 
axes.set_title('$Z_t = 0.9$',fontsize=14)
# axes.legend(loc=4 , prop={'size': 10}) # 
fig2.savefig("d6_Z9_P2_theta.eps")


