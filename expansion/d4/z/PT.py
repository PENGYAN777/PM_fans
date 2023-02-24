#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 16:05:08 2022

@author: yan

plot (P,T) diagram. show contour of compressibility factor Z and 
fundamental derivative of gasdynamics Gamma
"""

import matplotlib
import numpy as np
import CoolProp as CP
import matplotlib.pyplot as plt
import scipy.interpolate


# give fluid name
fluidname = "D4"

# update fluid
fluid = CP.AbstractState("HEOS", fluidname)

pc = fluid.keyed_output(CP.iP_critical)
Tc = fluid.keyed_output(CP.iT_critical)
Tmin =  CP.CoolProp.PropsSI("Ttriple",fluidname)
Tmax =  CP.CoolProp.PropsSI("Tmax",fluidname)
pmax = fluid.keyed_output(CP.iP_max)
pmin = fluid.keyed_output(CP.iP_min)
fillcolor = 'g'

# fig = plt.figure(figsize = (6,6))
# ax = fig.add_subplot(111)
fig = plt.figure(figsize=(6,5))
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax = fig.add_axes([left, bottom, width, height]) 
lw = 3


# ----------------
# Saturation curve
# ----------------
Ts = np.linspace(Tmin, Tc, 1000)
ps = CP.CoolProp.PropsSI('P','T',Ts,'Q',0,fluidname)

# ----------------
# Contour of Z and Gamma
# ----------------
n = 200 # number of points
x = np.linspace(400, 1000,n)
y = np.linspace(1e5, 8e6,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.4,0.5,0.6,0.7,0.8,0.9,1.0], cmap='rainbow')
plt.colorbar()
# ------
# Labels
# ------

plt.plot(Ts,ps,'k',lw = lw, solid_capstyle = 'round', label = "LVS")
ax.legend(loc=4) # 2 means left top
# Critical lines
plt.axvline(Tc, dashes = [2, 2])
plt.axhline(pc, dashes = [2, 2])

"""
test points
"""
nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

z9_p = [1.61e6, 1.28e6, 9.43e5, 6.06e5, 4.378e5,  2.69e5, ] 
z9_t = [799.20, 771.94, 730.26, 666.13,  616.43, 545.89, ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [1.616e6, 1.41e6, 1.21e6,  1.01e6, 8.08e5,  6.06e5, ]
z8_t = [706.21,  690.18, 670.94,  645.29, 614.83,  574.75, ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [1.616e6, 1.48e6, 1.41e6, 1.28e6, 1.21e6, 1.077e6, ]
z7_t = [658.11,  648.49, 642.08, 629.29, 622.84, 608.41, ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [1.616e6, 1.48e6, 1.414e6, 1.29e6, 1.21e6, 1.077e6, ]
z6_t = [629.25, 619.64,  614.83,  603.60, 597.19, 580.63, ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [2.42e6,  2.22e6,  2.02e6, 1.818e6, 1.61e6, 1.41e6, ]
z5_t = [646.89, 642.08,   634.06, 624.44, 613.22, 600.10, ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [2.42e6, 2.22e6, 2.02e6, 1.818e6, 1.616e6, 1.41e6, ]
z4_t = [629.26, 626.05, 624.24, 613.22,  603.60, 592.38, ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(1e5,8e6)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, 1000)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for siloxane D4')
plt.tight_layout()
fig.savefig("files/d4_z_Contour_PT.pdf")
print("plotcontour.py called")