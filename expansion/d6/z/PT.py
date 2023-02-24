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
fluidname = "D6"

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
x = np.linspace(500, Tmax,n)
y = np.linspace(1e5, 5e6,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.3, 0.4,0.5,0.6,0.7,0.8,0.9,1.0], cmap='rainbow')
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

z9_p = [2.50e5, 2.306e5,  2.114e5, 1.92e5, 1.73e5,  1.537e5, ] 
z9_t = [666.4, 652.75, 637.44, 620.48, 601.88, 581.63,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [4.80e5, 4.516e5, 4.228e5, 3.94e5, 3.65e5,  3.36e5, ]
z8_t = [663.15, 653.85,639.32, 631.96, 619.93, 606.80, ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [7.2e5, 6.727e5, 6.0e5,  5.76e5,  5.285e5, 4.8e5, ]
z7_t = [666.43, 657.68, 639.32, 636.34,  623.76, 610.08, ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [9.13e5, 8.65e5, 8.168e5, 7.40e5, 7.11e5, 6.727e5, ]
z6_t = [664.79, 658.23, 652.75, 639.32, 634.70, 628.14, ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [1.15e6, 1.10e6,  1.057e6, 1.0e6, 9.61e5, 9.51e5, ]
z5_t = [671.34, 667.53,  663.15, 658.77, 653.85, 652.75, ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ ]
z4_t = [ ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(1e5,5e6)
plt.gca().set_yscale('log')
plt.gca().set_xlim(500, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for siloxane D6')
plt.tight_layout()
fig.savefig("files/d6_z_Contour_PT.pdf")
print("plotcontour.py called")