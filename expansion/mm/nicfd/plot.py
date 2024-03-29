#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:59:53 2023

@author: yan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
"""
read csv file
"""

z9= pd.read_csv("z9.csv", ",", skiprows=0)
z8= pd.read_csv("z8.csv", ",", skiprows=0)
z7= pd.read_csv("z7.csv", ",", skiprows=0)
z6= pd.read_csv("z6.csv", ",", skiprows=0)
z5= pd.read_csv("z5.csv", ",", skiprows=0)
z4= pd.read_csv("z4.csv", ",", skiprows=0)

"""
plot 
"""
n = 10
colors = plt.cm.tab20(np.linspace(0, 1, n))
# fig1 = plt.figure( dpi=300)
# lwh = 2
# axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# axes.plot(z9.iloc[:,3] , z9.iloc[:,5] , 'k', lw=lwh, label="$Z_t = 0.9$")
# axes.plot(z8.iloc[:,3] , z8.iloc[:,5] , 'r', lw=lwh, label="$Z_t = 0.8$")
# axes.plot(z7.iloc[:,3] , z7.iloc[:,5] , 'b', lw=lwh, label="$Z_t = 0.7$")
# axes.plot(z6.iloc[:,3] , z6.iloc[:,5] , 'k--', lw=lwh, label="$Z_t = 0.6$")
# axes.plot(z5.iloc[:,3] , z5.iloc[:,5] , 'r--', lw=lwh, label="$Z_t = 0.5$")
# axes.plot(z4.iloc[:,3] , z4.iloc[:,5] , 'b--', lw=lwh, label="$Z_t = 0.4$")

# axes.set_xlabel('$\\rho/\\rho_t$',fontsize=12)
# axes.set_ylabel('Mach',fontsize=12) 
# axes.set_title('Mach number vs $\\rho/\\rho_t$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
# fig1.savefig("Mach_rho.pdf")

fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(z9.iloc[:,5] , z9.iloc[:,6] , color=colors[0], lw=lwh, label="$Z_t = 0.9$")
axes.plot(z8.iloc[:,5] , z8.iloc[:,6] , color=colors[1], lw=lwh, label="$Z_t = 0.8$")
axes.plot(z7.iloc[:,5] , z7.iloc[:,6] , color=colors[2], lw=lwh, label="$Z_t = 0.7$")
axes.plot(z6.iloc[:,5] , z6.iloc[:,6] , color=colors[3], lw=lwh, label="$Z_t = 0.6$")
axes.plot(z5.iloc[:,5] , z5.iloc[:,6] , color=colors[4], lw=lwh, label="$Z_t = 0.5$")
axes.plot(z4.iloc[:,5] , z4.iloc[:,6] , color=colors[5], lw=lwh, label="$Z_t = 0.4$")

axes.set_xlabel('$M_2$',fontsize=12)
axes.set_ylabel('$\\nu$',fontsize=12) 
# axes.set_title('$\\nu$ vs post-expansion Mach number',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("mm_nicfd_Mach_nu.eps")