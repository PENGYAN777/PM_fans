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




t100 = pd.read_csv("history_0.csv", ",", skiprows=0)
t101 = pd.read_csv("history_10.csv", ",", skiprows=0)


nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))


# axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

# fig 2
fig2 = plt.figure( dpi=300)
lw = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(t100.iloc[:,2] ,t100.iloc[:,3] , color=colors[0], lw=lw, label="level 0")
axes.plot(t101.iloc[:,2] ,t101.iloc[:,3] , color=colors[1], lw=lw, label="level 10")





# axes.set_xlim([0, 3000])
# axes.set_ylim([0,1])
axes.set_xlabel('Number of iteration',fontsize=12)
axes.set_ylabel('Residual of density',fontsize=12) 
# axes.set_title('$P/P_t$ along nozzle centerline',fontsize=14)
axes.legend(loc=0) # 

fig2.savefig("cfd_mm_5d_resudial.pdf")




