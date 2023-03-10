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
fluidname = "CO2"

# update fluid
fluid = CP.AbstractState("HEOS", fluidname)

pc = fluid.keyed_output(CP.iP_critical)
Tc = fluid.keyed_output(CP.iT_critical)
ec = CP.CoolProp.PropsSI('Smass','T',Tc,'P',pc,"PR::MDM")
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
es = CP.CoolProp.PropsSI('Smass','T',Ts,'Q',1,fluidname)

# ----------------
# Contour of Z and Gamma
# ----------------
n = 100 # number of points
x = np.linspace(1000, 3000,n)
y = np.linspace(250, 550,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','Smass',X,'T|gas',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','Smass',X,'T',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [1.0,1.2,1.4,1.6,1.8,2.0], cmap='rainbow')
plt.colorbar()
# ------
# Labels
# ------

plt.plot(es,Ts,'k',lw = lw, solid_capstyle = 'round', label = "LVS")
ax.legend(loc=4) # 2 means left top
# Critical lines
plt.axvline(ec, dashes = [2, 2])
plt.axhline(Tc, dashes = [2, 2])

"""
test points
"""
nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

z9_p = [1.328e7, 1.18e7, 1.03e7, 8.85e6, 7.37e6, 5.9e6, ]
z9_t = [478.04, 471.05, 460.55,  446.559, 429.06, 408.07,]
z9_s = CP.CoolProp.PropsSI('Smass','P',z9_p,'T',z9_t,fluidname)
plt.plot(z9_s,z9_t,'o' ,color=colors[0], lw = lw)

z8_p = [1.328e7,  1.18e7, 1.03e7, 8.85e6, 7.377e6, 5.9e6, ]
z8_t = [415.07, 404.57, 394.07, 380.08, 366.08, 345.09, ]
z8_s = CP.CoolProp.PropsSI('Smass','P',z8_p,'T',z8_t,fluidname)
plt.plot(z8_s,z8_t,'o' ,color=colors[1], lw = lw)

z7_p = [1.328e7, 1.18e7, 1.03e7, 8.85e6, 7.37e6, 5.9e6, ]
z7_t = [380.08,  369.58, 362.59, 348.59, 334.59, 317.10, ]
z7_s = CP.CoolProp.PropsSI('Smass','P',z7_p,'T',z7_t,fluidname)
plt.plot(z7_s,z7_t,'o' ,color=colors[2], lw = lw)

z6_p = [1.328e7, 1.18e7, 1.03e7, 8.85e6, 8.11e6, 6.64e6, ]
z6_t = [359.09, 352.09, 341.59, 331.10, 324.10, 310.10,  ]
z6_s = CP.CoolProp.PropsSI('Smass','P',z6_p,'T',z6_t,fluidname)
plt.plot(z6_s,z6_t,'o' ,color=colors[3], lw = lw)

z5_p = [1.328e7,  1.18e7, 1.03e7, 8.85e6, 8.11e6, 7.02e6, ]
z5_t = [345.09, 338.09, 331.10, 320.60, 313.606+1, 306.61-1,  ]
z5_s = CP.CoolProp.PropsSI('Smass','P',z5_p,'T',z5_t,fluidname)
plt.plot(z5_s,z5_t,'o' ,color=colors[4], lw = lw)

plt.ylim(250,550)
# plt.gca().set_yscale('log')
plt.gca().set_xlim(1000, 2500)
plt.xlabel('Entropy [J/K]')
plt.ylabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for CO2')
plt.tight_layout()
fig.savefig("files/co2_z_Contour_TS.pdf")
print("plotcontour.py called")