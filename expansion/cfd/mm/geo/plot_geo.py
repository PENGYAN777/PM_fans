#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 19:20:51 2022

@author: yan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

top = pd.read_csv("top.csv", ",", skiprows=0)
bot = pd.read_csv("bot.csv", ",", skiprows=0)
inlet = pd.read_csv("inlet.csv", ",", skiprows=0)
outlet = pd.read_csv("outlet.csv", ",", skiprows=0)


fig1 = plt.figure( dpi=300)
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(top.iloc[:,0]  , top.iloc[:,1] , 'k', lw=2, label="Slip top wall")
axes.plot(inlet.iloc[:,0]  , inlet.iloc[:,1] , 'r', lw=2, label="Riemann inlet")
axes.plot(outlet.iloc[:,0]  , outlet.iloc[:,1] , 'g', lw=2, label="Riemann outlet")
axes.plot(bot.iloc[:,0]  , bot.iloc[:,1] , 'b', lw=2, label="Slip bot wall")
axes.set_xlabel('X [mm]',fontsize=12)
#axes.set_yscale("log")
axes.set_ylabel('Y [mm]',fontsize=12) 
axes.set_aspect('equal', 'box')
axes.set_title('Geometry with $\\theta=5^o$',fontsize=14)

axes.legend(loc=0 , prop={'size': 10}) # 
# axes.set_xlim(0,8)
# axes.set_ylim(0,8)
#axes.legend(loc=2) # 2 means left top
fig1.savefig("geo_cfd.eps")
