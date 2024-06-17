#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:40:12 2024

@author: yan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import os
import CoolProp as CP
from IPython import get_ipython;   
get_ipython().magic('reset -sf')
os.system('clear')


c9 = pd.read_csv("c9.csv", ",", skiprows=0)
c10 = pd.read_csv("c10.csv", ",", skiprows=0)



# fig 2
fig2 = plt.figure( dpi=300)
lw = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(c9.iloc[:,-3] ,c9.iloc[:,2] , 'k', lw=lw, label="n = 32k")
axes.plot(c10.iloc[:,-3] ,c10.iloc[:,2], 'k--', lw=lw, label="n = 40k")

axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# axes.set_xlim([40, 160])
# axes.set_ylim([1,1.3])
axes.set_xlabel('$X[mm]$',fontsize=12)
axes.set_ylabel('Mach',fontsize=12) 
# axes.set_title('$P/P_t$ along nozzle centerline',fontsize=14)
axes.legend(loc=0) # 

fig2.savefig("cfd_mm_5d_mach.pdf")


# fig 3
fig3 = plt.figure( dpi=300)
lw = 2
axes = fig3.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(c9.iloc[:,-3] ,c9.iloc[:,6] , 'k', lw=lw, label="n = 32k")
axes.plot(c10.iloc[:,-3] ,c10.iloc[:,6], 'k--', lw=lw, label="n = 40k")

# axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
axes.ticklabel_format(axis='both', style='sci', scilimits=(0,0))
# axes.set_xlim([40, 160])
# axes.set_ylim([1,1.3])
axes.set_xlabel('$X[mm]$',fontsize=12)
axes.set_ylabel('P[Pa]',fontsize=12) 
# axes.set_title('$P/P_t$ along nozzle centerline',fontsize=14)
axes.legend(loc=0) # 

fig3.savefig("cfd_mm_5d_p.pdf")



