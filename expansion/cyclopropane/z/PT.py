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
fluidname = "CycloPropane"

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
x = np.linspace(250, Tmax,n)
y = np.linspace(5e5, 5e7,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.6,0.7,0.8,0.9,1.0,1.1,1.2], cmap='rainbow')
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

z9_p = [ 2.51e6, 2.23e6, 1.95e6, 1.67e6, 2.09e6, 2.37e6, ] 
z9_t = [467.10, 449.42, 430.70, 410.25, 440.06, 458.44,   ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [5.02e6, 3.62e6, 4.74e6, 4.46e6, 4.18e6, 3.9e6,  ]
z8_t = [471.026, 428.62, 463.64, 455.32, 446.99, 437.98,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [6.69e6, 5.3e6, 6.41e6, 6.13e6, 5.86e6, 5.58e6,  ]
z7_t = [ 460.86, 433.47, 455.66, 450.46, 445.26, 439.37,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [8.37e6,  5.58e6, 7.81e6,  7.25e6, 6.69e6, 6.13e6,  ]
z6_t = [457.74, 416.49, 451.16, 443.53, 435.21, 426.19,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [1.116e7, 6.97e6, 1.03e7, 9.48e6, 8.64e6, 7.81e6,  ]
z5_t = [461.21, 425.15, 456.70, 450.81, 443.87, 435.21,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 1.11e7, 8.369e6, 1.06e7, 1.0e7, 9.48e6, 8.92e6,  ]   
z4_t = [ 440.75, 429.66, 440.06, 438.67, 436.25,  433.47, ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(250, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Cyclic Alkanes CycloPropane')
plt.tight_layout()
fig.savefig("files/CycloPropane_z_Contour_PT.pdf")
print("plotcontour.py called")