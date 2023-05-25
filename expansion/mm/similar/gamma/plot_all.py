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


"""
0. get data
"""
g91= pd.read_csv("g9/z1.csv", ",", skiprows=0)
g92= pd.read_csv("g9/z2.csv", ",", skiprows=0)
g93= pd.read_csv("g9/z3.csv", ",", skiprows=0)
g94= pd.read_csv("g9/z4.csv", ",", skiprows=0)
g95= pd.read_csv("g9/z5.csv", ",", skiprows=0)
g96= pd.read_csv("g9/z6.csv", ",", skiprows=0)

g851= pd.read_csv("g85/z1.csv", ",", skiprows=0)
g852= pd.read_csv("g85/z2.csv", ",", skiprows=0)
g853= pd.read_csv("g85/z3.csv", ",", skiprows=0)
g854= pd.read_csv("g85/z4.csv", ",", skiprows=0)
g855= pd.read_csv("g85/z5.csv", ",", skiprows=0)
g856= pd.read_csv("g85/z6.csv", ",", skiprows=0)

g81= pd.read_csv("g8/z1.csv", ",", skiprows=0)
g82= pd.read_csv("g8/z2.csv", ",", skiprows=0)
g83= pd.read_csv("g8/z3.csv", ",", skiprows=0)
g84= pd.read_csv("g8/z4.csv", ",", skiprows=0)
g85= pd.read_csv("g8/z5.csv", ",", skiprows=0)
g86= pd.read_csv("g8/z6.csv", ",", skiprows=0)

g751= pd.read_csv("g75/z1.csv", ",", skiprows=0)
g752= pd.read_csv("g75/z2.csv", ",", skiprows=0)
g753= pd.read_csv("g75/z3.csv", ",", skiprows=0)
g754= pd.read_csv("g75/z4.csv", ",", skiprows=0)
g755= pd.read_csv("g75/z5.csv", ",", skiprows=0)
g756= pd.read_csv("g75/z6.csv", ",", skiprows=0)

g71= pd.read_csv("g7/z1.csv", ",", skiprows=0)
g72= pd.read_csv("g7/z2.csv", ",", skiprows=0)
g73= pd.read_csv("g7/z3.csv", ",", skiprows=0)
g74= pd.read_csv("g7/z4.csv", ",", skiprows=0)
g75= pd.read_csv("g7/z5.csv", ",", skiprows=0)
g76= pd.read_csv("g7/z6.csv", ",", skiprows=0)

"""
1. input theta and upstream Mach number, compute downstream data
"""
n = 50
"""
g9
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

g91_m2 = np.zeros(n) 
g92_m2 = np.zeros(n) 
g93_m2 = np.zeros(n) 
g94_m2 = np.zeros(n) 
g95_m2 = np.zeros(n) 
g96_m2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = g91.iloc[:,6][np.argmin(abs(g91.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g91.iloc[:,5][np.argmin(abs(g91.iloc[:,6]-nu2))] 
    g91_m2[i] = M2
    # for z2
    nu1 = g92.iloc[:,6][np.argmin(abs(g92.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g92.iloc[:,5][np.argmin(abs(g92.iloc[:,6]-nu2))] 
    g92_m2[i] = M2
    # for z3
    nu1 = g93.iloc[:,6][np.argmin(abs(g93.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g93.iloc[:,5][np.argmin(abs(g93.iloc[:,6]-nu2))] 
    g93_m2[i] = M2
    # for z4
    nu1 = g94.iloc[:,6][np.argmin(abs(g94.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g94.iloc[:,5][np.argmin(abs(g94.iloc[:,6]-nu2))] 
    g94_m2[i] = M2
    # for z5
    nu1 = g95.iloc[:,6][np.argmin(abs(g95.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g95.iloc[:,5][np.argmin(abs(g95.iloc[:,6]-nu2))] 
    g95_m2[i] = M2
    # for z6
    nu1 = g96.iloc[:,6][np.argmin(abs(g96.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g96.iloc[:,5][np.argmin(abs(g96.iloc[:,6]-nu2))] 
    g96_m2[i] = M2
    
"""
g85
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

g851_m2 = np.zeros(n) 
g852_m2 = np.zeros(n) 
g853_m2 = np.zeros(n) 
g854_m2 = np.zeros(n) 
g855_m2 = np.zeros(n) 
g856_m2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = g851.iloc[:,6][np.argmin(abs(g851.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g851.iloc[:,5][np.argmin(abs(g851.iloc[:,6]-nu2))] 
    g851_m2[i] = M2
    # for z2
    nu1 = g852.iloc[:,6][np.argmin(abs(g852.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g852.iloc[:,5][np.argmin(abs(g852.iloc[:,6]-nu2))] 
    g852_m2[i] = M2
    # for z3
    nu1 = g853.iloc[:,6][np.argmin(abs(g853.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g853.iloc[:,5][np.argmin(abs(g853.iloc[:,6]-nu2))] 
    g853_m2[i] = M2
    # for z4
    nu1 = g854.iloc[:,6][np.argmin(abs(g854.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g854.iloc[:,5][np.argmin(abs(g854.iloc[:,6]-nu2))] 
    g854_m2[i] = M2
    # for z5
    nu1 = g855.iloc[:,6][np.argmin(abs(g855.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g855.iloc[:,5][np.argmin(abs(g855.iloc[:,6]-nu2))] 
    g855_m2[i] = M2
    # for z6
    nu1 = g856.iloc[:,6][np.argmin(abs(g856.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g856.iloc[:,5][np.argmin(abs(g856.iloc[:,6]-nu2))] 
    g856_m2[i] = M2

"""
g8
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

g81_m2 = np.zeros(n) 
g82_m2 = np.zeros(n) 
g83_m2 = np.zeros(n) 
g84_m2 = np.zeros(n) 
g85_m2 = np.zeros(n) 
g86_m2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = g81.iloc[:,6][np.argmin(abs(g81.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g81.iloc[:,5][np.argmin(abs(g81.iloc[:,6]-nu2))] 
    g81_m2[i] = M2
    # for z2
    nu1 = g82.iloc[:,6][np.argmin(abs(g82.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g82.iloc[:,5][np.argmin(abs(g82.iloc[:,6]-nu2))] 
    g82_m2[i] = M2
    # for z3
    nu1 = g83.iloc[:,6][np.argmin(abs(g83.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g83.iloc[:,5][np.argmin(abs(g83.iloc[:,6]-nu2))] 
    g83_m2[i] = M2
    # for z4
    nu1 = g84.iloc[:,6][np.argmin(abs(g84.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g84.iloc[:,5][np.argmin(abs(g84.iloc[:,6]-nu2))] 
    g84_m2[i] = M2
    # for z5
    nu1 = g85.iloc[:,6][np.argmin(abs(g85.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g85.iloc[:,5][np.argmin(abs(g85.iloc[:,6]-nu2))] 
    g85_m2[i] = M2
    # for z6
    nu1 = g86.iloc[:,6][np.argmin(abs(g86.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g86.iloc[:,5][np.argmin(abs(g86.iloc[:,6]-nu2))] 
    g86_m2[i] = M2

"""
g75
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

g751_m2 = np.zeros(n) 
g752_m2 = np.zeros(n) 
g753_m2 = np.zeros(n) 
g754_m2 = np.zeros(n) 
g755_m2 = np.zeros(n) 
g756_m2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = g751.iloc[:,6][np.argmin(abs(g751.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g751.iloc[:,5][np.argmin(abs(g751.iloc[:,6]-nu2))] 
    g751_m2[i] = M2
    # for z2
    nu1 = g752.iloc[:,6][np.argmin(abs(g752.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g752.iloc[:,5][np.argmin(abs(g752.iloc[:,6]-nu2))] 
    g752_m2[i] = M2
    # for z3
    nu1 = g753.iloc[:,6][np.argmin(abs(g753.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g753.iloc[:,5][np.argmin(abs(g753.iloc[:,6]-nu2))] 
    g753_m2[i] = M2
    # for z4
    nu1 = g754.iloc[:,6][np.argmin(abs(g754.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g754.iloc[:,5][np.argmin(abs(g754.iloc[:,6]-nu2))] 
    g754_m2[i] = M2
    # for z5
    nu1 = g755.iloc[:,6][np.argmin(abs(g755.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g755.iloc[:,5][np.argmin(abs(g755.iloc[:,6]-nu2))] 
    g755_m2[i] = M2
    # for z6
    nu1 = g756.iloc[:,6][np.argmin(abs(g756.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g756.iloc[:,5][np.argmin(abs(g756.iloc[:,6]-nu2))] 
    g756_m2[i] = M2
    
"""
g7
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

g71_m2 = np.zeros(n) 
g72_m2 = np.zeros(n) 
g73_m2 = np.zeros(n) 
g74_m2 = np.zeros(n) 
g75_m2 = np.zeros(n) 
g76_m2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = g71.iloc[:,6][np.argmin(abs(g71.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g71.iloc[:,5][np.argmin(abs(g71.iloc[:,6]-nu2))] 
    g71_m2[i] = M2
    # for z2
    nu1 = g72.iloc[:,6][np.argmin(abs(g72.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g72.iloc[:,5][np.argmin(abs(g72.iloc[:,6]-nu2))] 
    g72_m2[i] = M2
    # for z3
    nu1 = g73.iloc[:,6][np.argmin(abs(g73.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g73.iloc[:,5][np.argmin(abs(g73.iloc[:,6]-nu2))] 
    g73_m2[i] = M2
    # for z4
    nu1 = g74.iloc[:,6][np.argmin(abs(g74.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g74.iloc[:,5][np.argmin(abs(g74.iloc[:,6]-nu2))] 
    g74_m2[i] = M2
    # for z5
    nu1 = g75.iloc[:,6][np.argmin(abs(g75.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g75.iloc[:,5][np.argmin(abs(g75.iloc[:,6]-nu2))] 
    g75_m2[i] = M2
    # for z6
    nu1 = g76.iloc[:,6][np.argmin(abs(g76.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = g76.iloc[:,5][np.argmin(abs(g76.iloc[:,6]-nu2))] 
    g76_m2[i] = M2
"""
2. plot
"""

nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , g91_m2 , color=colors[0], lw=lwh, label="$\Gamma_1=0.90$")
axes.plot(theta/math.pi*180  , g92_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , g93_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , g94_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , g95_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , g96_m2 , color=colors[0], lw=lwh)

axes.plot(theta/math.pi*180  , g851_m2 , color=colors[1], lw=lwh, label="$\Gamma_1=0.85$")
axes.plot(theta/math.pi*180  , g852_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , g853_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , g854_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , g855_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , g856_m2 , color=colors[1], lw=lwh)

axes.plot(theta/math.pi*180  , g81_m2 , color=colors[2], lw=lwh, label="$\Gamma_1=0.80$")
axes.plot(theta/math.pi*180  , g82_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , g83_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , g84_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , g85_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , g86_m2 , color=colors[2], lw=lwh)

axes.plot(theta/math.pi*180  , g751_m2 , color=colors[3], lw=lwh, label="$\Gamma_1=0.75$")
axes.plot(theta/math.pi*180  , g752_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , g753_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , g754_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , g755_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , g756_m2 , color=colors[3], lw=lwh)

axes.plot(theta/math.pi*180  , g71_m2 , color=colors[5], lw=lwh, label="$\Gamma_1=0.70$")
axes.plot(theta/math.pi*180  , g72_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , g73_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , g74_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , g75_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , g76_m2 , color=colors[5], lw=lwh)

axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("mm_g_M2_theta.eps")

################################################################################
fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

g1 = [0.7,0.75,0.8,0.85,0.9]
maxdiff = [12,10, 12, 6, 8] 
maxdiff.reverse()


plt.bar(g1,maxdiff,color ='b', width = 0.02)
axes.set_xlabel('$\Gamma_1$',fontsize=12)
axes.set_ylabel('$(\Delta M_2)_{\max}\%$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("mm_g_M2_g1.eps")
