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
z9= pd.read_csv("z9.csv", ",", skiprows=0)
z8= pd.read_csv("z8.csv", ",", skiprows=0)
z7= pd.read_csv("z7.csv", ",", skiprows=0)
z6= pd.read_csv("z6.csv", ",", skiprows=0)
z5= pd.read_csv("z5.csv", ",", skiprows=0)
z4= pd.read_csv("z4.csv", ",", skiprows=0)

"""
1. input theta and upstream Mach number, compute downstream data
"""
n = 20
theta = np.zeros(n) # 

z9_m2 = np.zeros(n) 
z8_m2 = np.zeros(n) 
z7_m2 = np.zeros(n) 
z6_m2 = np.zeros(n) 
z5_m2 = np.zeros(n) 
z4_m2 = np.zeros(n) 

z9_P2 = np.zeros(n) 
z8_P2 = np.zeros(n) 
z7_P2 = np.zeros(n) 
z6_P2 = np.zeros(n) 
z5_P2 = np.zeros(n) 
z4_P2 = np.zeros(n) 

diff_z9 = np.zeros(n) # diff
diff_z8 = np.zeros(n) # diff
diff_z7 = np.zeros(n) # diff
diff_z6 = np.zeros(n) # diff
diff_z5 = np.zeros(n) # diff
diff_z4 = np.zeros(n) # diff


for i in range(n):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.6 # upstream Mach number
    # for z9
    nu1 = z9.iloc[:,6][np.argmin(abs(z9.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z9.iloc[:,5][np.argmin(abs(z9.iloc[:,6]-nu2))] 
    z9_m2[i] = M2
    P2 = z9.iloc[:,2][np.argmin(abs(z9.iloc[:,6]-nu2))] 
    z9_P2[i] = P2
    # D2 = z9.iloc[:,3][np.argmin(abs(z9.iloc[:,6]-nu2))] 
    # z9_D2[i] = D2
    # T2 = z9.iloc[:,4][np.argmin(abs(z9.iloc[:,6]-nu2))] 
    # z9_T2[i] = T2
    # for z8
    nu1 = z8.iloc[:,6][np.argmin(abs(z8.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z8.iloc[:,5][np.argmin(abs(z8.iloc[:,6]-nu2))] 
    z8_m2[i] = M2
    P2 = z8.iloc[:,2][np.argmin(abs(z8.iloc[:,6]-nu2))] 
    z8_P2[i] = P2

    # for z7
    nu1 = z7.iloc[:,6][np.argmin(abs(z7.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z7.iloc[:,5][np.argmin(abs(z7.iloc[:,6]-nu2))] 
    z7_m2[i] = M2
    P2 = z7.iloc[:,2][np.argmin(abs(z7.iloc[:,6]-nu2))] 
    z7_P2[i] = P2

    # for z6
    nu1 = z6.iloc[:,6][np.argmin(abs(z6.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z6.iloc[:,5][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_m2[i] = M2
    P2 = z6.iloc[:,2][np.argmin(abs(z6.iloc[:,6]-nu2))] 
    z6_P2[i] = P2
    
    # for z5
    nu1 = z5.iloc[:,6][np.argmin(abs(z5.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z5.iloc[:,5][np.argmin(abs(z5.iloc[:,6]-nu2))] 
    z5_m2[i] = M2
    P2 = z5.iloc[:,2][np.argmin(abs(z5.iloc[:,6]-nu2))] 
    z5_P2[i] = P2
    
    # for z4
    nu1 = z4.iloc[:,6][np.argmin(abs(z4.iloc[:,5]-M1))] 
    nu2 = nu1 - theta[i]
    M2 = z4.iloc[:,5][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z4_m2[i] = M2
    P2 = z4.iloc[:,2][np.argmin(abs(z4.iloc[:,6]-nu2))] 
    z4_P2[i] = P2
    


"""
2. plot
"""
nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , z9_m2 , color=colors[0], lw=lwh, label="$Z_t = 0.9$")
axes.plot(theta/math.pi*180  , z8_m2 , color=colors[1], lw=lwh, label="$Z_t = 0.8$")
axes.plot(theta/math.pi*180  , z7_m2 , color=colors[2], lw=lwh, label="$Z_t = 0.7$")
axes.plot(theta/math.pi*180  , z6_m2 , color=colors[3], lw=lwh, label="$Z_t = 0.6$")
axes.plot(theta/math.pi*180  , z5_m2 , color=colors[4], lw=lwh, label="$Z_t = 0.5$")
axes.plot(theta/math.pi*180  , z4_m2 , color=colors[5], lw=lwh, label="$Z_t = 0.4$")

axes.set_xlabel('$\\theta$(degree)',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
axes.set_title('$M_2$ vs $\\theta$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("com_nicfd_M2_theta.pdf")

fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , z9_P2 , color=colors[0], lw=lwh, label="$Z_t = 0.9$")
axes.plot(theta/math.pi*180  , z8_P2 , color=colors[1], lw=lwh, label="$Z_t = 0.8$")
axes.plot(theta/math.pi*180  , z7_P2 , color=colors[2], lw=lwh, label="$Z_t = 0.7$")
axes.plot(theta/math.pi*180  , z6_P2 , color=colors[3], lw=lwh, label="$Z_t = 0.6$")
axes.plot(theta/math.pi*180  , z5_P2 , color=colors[4], lw=lwh, label="$Z_t = 0.5$")
axes.plot(theta/math.pi*180  , z4_P2 , color=colors[5], lw=lwh, label="$Z_t = 0.4$")


axes.set_xlabel('$\\theta$(degree)',fontsize=12)
axes.set_ylabel('$P_2/P_t$',fontsize=12) 
axes.set_title('$P_2/P_t$ vs $\\theta$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("com_nicfd_P2_theta.pdf")

"""
3. plot Delat P
"""

diff_z9 = np.zeros(n) # diff
diff_z8 = np.zeros(n) # diff
diff_z7 = np.zeros(n) # diff
diff_z6 = np.zeros(n) # diff
diff_z5 = np.zeros(n) # diff
diff_z4 = np.zeros(n) # diff

for i in range(n):
    diff_z9[i] = (z9_P2[i] - z9_P2[0])/( z9_P2[0])
    diff_z8[i] = (z8_P2[i] - z8_P2[0])/( z8_P2[0])
    diff_z7[i] = (z7_P2[i] - z7_P2[0])/( z7_P2[0])
    diff_z6[i] = (z6_P2[i] - z6_P2[0])/( z6_P2[0])
    diff_z5[i] = (z5_P2[i] - z5_P2[0])/( z5_P2[0])
    diff_z4[i] = (z4_P2[i] - z4_P2[0])/( z4_P2[0])

fig3 = plt.figure( dpi=300)
lwh = 2
axes = fig3.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180 ,  diff_z9 , color=colors[0], lw=lwh, label="$Z_t = 0.9$")
axes.plot(theta/math.pi*180 ,  diff_z8 , color=colors[1], lw=lwh, label="$Z_t = 0.8$")
axes.plot(theta/math.pi*180 ,  diff_z7 , color=colors[2], lw=lwh, label="$Z_t = 0.7$")
axes.plot(theta/math.pi*180 ,  diff_z6 , color=colors[3], lw=lwh, label="$Z_t = 0.6$")
axes.plot(theta/math.pi*180 ,  diff_z5 , color=colors[4], lw=lwh, label="$Z_t = 0.5$")
axes.plot(theta/math.pi*180 ,  diff_z4 , color=colors[5], lw=lwh, label="$Z_t = 0.4$")

axes.set_xlabel('$\\theta$(degree)',fontsize=12)
axes.set_ylabel('$\\Delta P$',fontsize=12) 
axes.set_title('$\\Delta P$ vs $\\theta$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig3.savefig("com_nicfd_dP2_theta.pdf")
