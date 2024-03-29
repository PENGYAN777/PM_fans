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

z34= pd.read_csv("z34.csv", ",", skiprows=0)
md = pd.read_csv("paper_mrho.csv", ",", skiprows=0)
num = pd.read_csv("paper_num.csv", ",", skiprows=0)
"""
plot 
"""
# fig1 = plt.figure( dpi=300)
# lwh = 2
# axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# axes.plot(z34.iloc[:,3] , z34.iloc[:,5] , 'k', lw=lwh, label="4th order RK")
# axes.plot(md.iloc[:,0] , md.iloc[:,1] , 'ko', lw=lwh/2, label="Cramer et.al 1992")


# axes.set_xlabel('$\\rho/\\rho_c$',fontsize=12)
# axes.set_ylabel('M',fontsize=12) 
# axes.set_title('Mach number vs $\\rho/\\rho_c$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
# fig1.savefig("vv_mrho.eps")

# diff = 0
# for i in range(0,17,1):
#     x = md.iloc[i,0]
#     y = z34.iloc[:,5][np.argmin(abs(z34.iloc[:,3]-x))]
#     diff = diff + (y - md.iloc[i,1])/md.iloc[i,1]*100
# diff = diff/18.
# print('average diff:',diff)


fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(z34.iloc[:,5] , z34.iloc[:,6] , 'k', lw=lwh, label="4th order RK")
axes.plot(num.iloc[:,0] , num.iloc[:,1] , 'ko', lw=lwh/2, label="Cramer et.al 1992")

axes.set_xlabel('Mach',fontsize=12)
axes.set_ylabel('$\\nu$',fontsize=12) 
plt.xlim([1, 1.75])
# axes.set_title('$\\nu$ vs Mach number',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("vv_num.eps")

# diff = 0
# for i in range(0,13,1):
#     x = num.iloc[i,0]
#     y = z34.iloc[:,6][np.argmin(abs(z34.iloc[:,5]-x))]
#     diff = diff + (y - num.iloc[i,1])/num.iloc[i,1]*100
# diff = diff/14
diff = 0
for i in range(0,13,1):
    x = num.iloc[i,1]
    y = z34.iloc[:,5][np.argmin(abs(z34.iloc[:,6]-x))]
    diff = diff + (y - num.iloc[i,0])/num.iloc[i,0]*100
diff = diff/14
print('average diff:',diff)