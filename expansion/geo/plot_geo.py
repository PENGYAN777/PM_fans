#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 19:20:51 2022

@author: yan
"""
import math
import numpy as np
from numpy import sin, cos, pi, linspace
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

wall = pd.read_csv("wall.csv", ",", skiprows=0)
dash = pd.read_csv("dash.csv", ",", skiprows=0)
turn = pd.read_csv("max.csv", ",", skiprows=0)
ex1 = pd.read_csv("ex1.csv", ",", skiprows=0)
ex2 = pd.read_csv("ex2.csv", ",", skiprows=0)
ex3 = pd.read_csv("ex3.csv", ",", skiprows=0)

lwh = 2

fig1 = plt.figure( dpi=300)
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# wall
axes.plot(wall.iloc[:,0], wall.iloc[:,1] , 'k', lw=lwh)
axes.plot(dash.iloc[:,0], dash.iloc[:,1] , 'b--', lw=lwh)
# expansion wavs
axes.plot(ex1.iloc[:,0], ex1.iloc[:,1] , 'k-.', lw=lwh)
axes.plot(ex2.iloc[:,0], ex2.iloc[:,1] , 'k-.', lw=lwh)
axes.plot(ex3.iloc[:,0], ex3.iloc[:,1] , 'k-.', lw=lwh)
# hatch along the wall
plt.fill_between([-1,0],[-0.1,-0.1], color="none", hatch="/", edgecolor="k", linewidth=0.0)
plt.fill_between([0,0.866, 0.4, 0],[0, -0.5, -0.35, -0.1], color="none", hatch="/", edgecolor="k", linewidth=0.0)

#draw a circle
angles = linspace(0 * pi, -1/6* pi, 100 )
xs = cos(angles)*0.3
ys = sin(angles)*0.3
plt.plot(xs, ys, 'k--')

# draw arrow
plt.arrow(-0.75, 0.2, 0.5, 0, width = 0.02, color = 'k')
plt.arrow(0.4, -0.1, 0.25, -0.15, width = 0.02, color = 'k')

# Labels
plt.text(0.35, -0.1, '$\\theta$',ha= 'center', size = 15)
plt.text(-0.5, 0.3, '$M_1$', rotation = 0,ha= 'center')
plt.text(0.6, -0.2, '$M_2$', rotation = -30,ha= 'center')


axes.set_aspect('equal', 'box')
plt.axis('off')
fig1.savefig("geo_ex.pdf")

fig2 = plt.figure( dpi=300)
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# wall
axes.plot(wall.iloc[:,0], wall.iloc[:,1] , 'k', lw=lwh)
axes.plot(dash.iloc[:,0], dash.iloc[:,1] , 'b', lw=lwh)
axes.plot(turn.iloc[:,0], turn.iloc[:,1] , 'b--', lw=lwh)
# expansion wavs
axes.plot(ex1.iloc[:,0], ex1.iloc[:,1] , 'k-.', lw=lwh)
axes.plot(ex2.iloc[:,0], ex2.iloc[:,1] , 'k-.', lw=lwh)
axes.plot(ex3.iloc[:,0], ex3.iloc[:,1] , 'k-.', lw=lwh)
# hatch along the wall
plt.fill_between([-1,0],[-0.1,-0.1], color="none", hatch="/", edgecolor="k", linewidth=0.0)
plt.fill_between([0,0.866, 0.4, 0],[0, -0.5, -0.35, -0.1], color="none", hatch="/", edgecolor="k", linewidth=0.0)

#draw a circle
angles = linspace(0 * pi, -1/7* pi, 100 )
xs = cos(angles)*0.3
ys = sin(angles)*0.3
plt.plot(xs, ys, 'k--')

# draw arrow
plt.arrow(-0.75, 0.2, 0.5, 0, width = 0.02, color = 'k')
plt.arrow(0.5, -0.15, 0.25, -0.12, width = 0.02, color = 'k')

# Labels
plt.text(0.4, -0.1, '$\\theta_{max}$',ha= 'center', size = 12)
plt.text(-0.5, 0.3, '$M_1$', rotation = 0,ha= 'center')
plt.text(0.7, -0.2, '$M_2$', rotation = -30,ha= 'center')


axes.set_aspect('equal', 'box')
plt.axis('off')
fig2.savefig("geo_turning.pdf")
