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
wh = 0.02

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

zt = [0.6,0.7,0.8,0.9]
maxdiff_mm = [ 3, 1.5, 1.2, 0.5] 
maxdiff_mdm = [  0.5, 0.4, 0.35, 0.25] 

plt.bar(zt,maxdiff_mm,color=colors[0], width = wh,label="$MM$")
plt.bar(zt,maxdiff_mdm,color=colors[1], width = wh,label="$MDM$")
plt.xticks(np.arange(min(zt), max(zt)+1, 0.1))

axes.set_xlim([0.55, 0.95])
axes.set_xlabel('$Z_t$',fontsize=12)
axes.set_ylabel('$(\Delta M_2)_{\max}\%$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("mm_mdm.eps")


##############################################################
fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

zt = [0.6,0.7,0.8,0.9]
maxdiff_mm = [1.0,3.0,6.0,9.2] 
maxdiff_d4 = [ 2.0, 1.75, 0.8,  0.5, ] 
maxdiff_d6 = [  1.0, 0.7,0.6,0.2] 

plt.bar(zt,maxdiff_d4,color=colors[0], width = wh,label="$D4$")
plt.bar(zt,maxdiff_d6,color=colors[1], width = wh,label="$D6$")
plt.xticks(np.arange(min(zt), max(zt)+1, 0.1))

axes.set_xlim([0.55, 0.95])
axes.set_xlabel('$Z_t$',fontsize=12)
axes.set_ylabel('$(\Delta M_2)_{\max}\%$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("d4_d6.eps")






