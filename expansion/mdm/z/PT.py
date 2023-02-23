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
fluidname = "MDM"

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
n = 500 # number of points
x = np.linspace(400, Tmax,n)
y = np.linspace(5e4, 5e6,n)
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

z9_p = [4.23e5, 3.83e5, 3.43e5, 3.03e5, 2.63e5, 2.23e5, ]
z9_t = [574.29, 558.44, 544.84, 528.00, 509.07, 488.08, ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [7.75e5, 6.91e5,  6.55e5, 5.95e5, 5.35e5, 4.75e5]
z8_t = [574.29, 558.44,  551.50,  538.87, 524.85, 509.77]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [1.05e6, 1.00e6, 9.47e5, 8.92e5, 8.37e5, 7.82e5]
z7_t = [573.59, 569.74, 558.45, 552.20, 544.13, 535.72]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [1.269e6,1.22e6, 1.13e6, 1.11e6,  1.07e6, 1.02e6]
z6_t = [572.89, 569.74, 558.45, 557.11,  552.90, 547.29]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [1.396e6, 1.38e6, 1.24e6, 1.22e6, 1.21e6, 1.18e6, ]
z5_t = [570.44, 569.74, 558.16, 556.76, 555.71, 553.25, ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)


plt.ylim(5e4,5e6)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for siloxane MDM')
plt.tight_layout()
fig.savefig("files/mdm_z_Contour_PT.pdf")
print("plotcontour.py called")