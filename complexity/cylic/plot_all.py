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

nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

zt = [0.6,0.7,0.8,0.9]
maxdiff_pro = [2.5, 1.4, 1.3, 1.2 ] 
maxdiff_pen = [1.8,  0.7, 0.6, 0.6] 
maxdiff_hex = [1.4, 0.7, 0.6, 0.55 ] 




wh = 0.02
plt.bar(zt,maxdiff_pro,color=colors[0], width = wh,label="$CycloPropane$")
plt.bar(zt,maxdiff_pen,color=colors[1], width = wh,label="$CycloPentane$")
plt.bar(zt,maxdiff_hex,color=colors[2], width = wh,label="$CycloHexane$")


plt.xticks(np.arange(min(zt), max(zt)+1, 0.1))

axes.set_xlim([0.55, 0.95])
axes.set_xlabel('$Z_t$',fontsize=12)
axes.set_ylabel('$(\Delta M_2)_{\max}\%$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("cylic.eps")








