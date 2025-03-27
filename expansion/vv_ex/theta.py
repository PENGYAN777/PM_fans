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

z6= pd.read_csv("z6.csv", ",", skiprows=0)


"""
1. input theta and upstream Mach number, compute downstream data
"""
n = 50
theta = np.zeros(n) # Gamma


z6_m2 = np.zeros(n)  

z6_P2 = np.zeros(n)  

z6_T2 = np.zeros(n)  

z6_D2 = np.zeros(n)  

# expriment data
theta_e = [0,10,20,30]
m_e = [ 1.2227, 1.4034, 1.5676, 1.7343, ]
um = [0.0064, 0.0084, 0.0136, 0.0081, ]

m0 = 1.2227

for i in range(n):
    theta[i] = i*math.pi/180 # rad
    M1 = m0 # upstream Mach number

    # for z6
    nu1 = z6.iloc[:,6][np.argmin(abs(z6.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z6.iloc[:,5][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_m2[i] = M2
    P2 = z6.iloc[:,2][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_P2[i] = P2
    D2 = z6.iloc[:,3][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_D2[i] = D2
    T2 = z6.iloc[:,4][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_T2[i] = T2
    
    


"""
2. plot
"""
nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

axes.plot(theta/math.pi*180  , z6_m2 , 'k', lw=lwh, label="Theory")
# axes.plot(theta_e  , m_e , 'ko', lw=lwh, label="Experiment")
# Plot m_e with uncertainty bars
axes.errorbar(theta_e, m_e, yerr=um, fmt='ko', capsize=5, label="Experiment with Uncertainty")



# Add 5% shaded region around sorted num.iloc[:,0] values
lower_bound = np.array(m_e) * 0.95  # Convert list to NumPy array
upper_bound = np.array(m_e) * 1.05


# Fill the region between the bounds with lightgreen color
axes.fill_between(theta_e , lower_bound, upper_bound, color='gray', alpha=0.1, label="±5% Error Band")

axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
axes.set_xlim([0, 30]) 
axes.set_ylim([1.1, 1.9]) 
# axes.set_title('$M_2$ vs $\\theta$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("vv_mm_M2_theta.eps")

# fig2 = plt.figure( dpi=300)
# lwh = 2
# axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# axes.plot(theta/math.pi*180  , z9_P2 , color=colors[0], lw=lwh, label="$Z_t = 0.9$")
# axes.plot(theta/math.pi*180  , z8_P2 , color=colors[1], lw=lwh, label="$Z_t = 0.8$")
# axes.plot(theta/math.pi*180  , z7_P2 , color=colors[2], lw=lwh, label="$Z_t = 0.7$")
# axes.plot(theta/math.pi*180  , z6_P2 , color=colors[3], lw=lwh, label="$Z_t = 0.6$")
# axes.plot(theta/math.pi*180  , z5_P2 , color=colors[4], lw=lwh, label="$Z_t = 0.5$")
# axes.plot(theta/math.pi*180  , z4_P2 , color=colors[5], lw=lwh, label="$Z_t = 0.4$")


# axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
# axes.set_ylabel('$P_2/P_t$',fontsize=12) 
# axes.set_title('$P_2/P_t$ vs $\\theta$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
# fig2.savefig("mm_nicfd_P2_theta.eps")

# """
# 3. plot Delat P
# """

# diff_z9 = np.zeros(n) # diff
# diff_z8 = np.zeros(n) # diff
# diff_z7 = np.zeros(n) # diff
# diff_z6 = np.zeros(n) # diff
# diff_z5 = np.zeros(n) # diff
# diff_z4 = np.zeros(n) # diff

# for i in range(n):

#     diff_z6[i] = -(z6_P2[i] - z6_P2[0])/( z6_P2[0])


# fig3 = plt.figure( dpi=300)
# lwh = 2
# axes = fig3.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

# axes.plot(theta/math.pi*180 ,  diff_z6 , color=colors[3], lw=lwh, label="$Z_t = 0.6$")


# axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
# axes.set_ylabel('$\\Delta P$',fontsize=12) 
# # axes.set_title('$\\Delta P$ vs $\\theta$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
# fig3.savefig("vv_mm_dP2_theta.eps")