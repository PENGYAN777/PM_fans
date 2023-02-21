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
# z9_p = [1.328e7, 1.1e7, 8.70e6, 6.418e6, 4.13e6,  1.84e6, ]
# z9_t = [478.04, 464.05,  443.06, 415.07, 373.08, 296.11, ]
# z9_s = CP.CoolProp.PropsSI('Smass','P',z9_p,'T',z9_t,fluidname)
# plt.plot(z9_s,z9_t,'ko',lw = lw)

# z8_p = [1.328e7, 1.106e7, 8.85e6, 6.64e6, 4.426e6,  3.98e6, ]
# z8_t = [415.07, 401.07, 380.08, 355.59, 320.60, 310.11, ]
# z8_s = CP.CoolProp.PropsSI('Smass','P',z8_p,'T',z8_t,fluidname)
# plt.plot(z8_s,z8_t,'ro',lw = lw)

# z7_p = [1.328e7, 1.18e7, 1.03e7, 8.85e6, 7.39e6, 5.90e6, ]
# z7_t = [380.08, 369.58, 362.59, 348.58, 334.60, 317.10,  ]
# z7_s = CP.CoolProp.PropsSI('Smass','P',z7_p,'T',z7_t,fluidname)
plt.plot(z7_s,z7_t,'bo',lw = lw)

# z6_p = [1.269e6,1.22e6, 1.13e6, 1.11e6,  1.07e6, 1.02e6]
# z6_t = [572.89, 569.74, 558.45, 557.11,  552.90, 547.29]
# z6_s = CP.CoolProp.PropsSI('Smass','P',z6_p,'T',z6_t,fluidname)
# plt.plot(z6_s,z6_t,'k*',lw = lw)

# z5_p = [1.396e6, 1.38e6, 1.24e6, 1.22e6, 1.21e6, 1.18e6, ]
# z5_t = [570.44, 569.74, 558.16, 556.76, 555.71, 553.25, ]
# z5_s = CP.CoolProp.PropsSI('Smass','P',z6_p,'T',z6_t,fluidname)
# plt.plot(z5_s,z5_t,'k*',lw = lw)

plt.ylim(250,550)
# plt.gca().set_yscale('log')
plt.gca().set_xlim(1000, 2500)
plt.xlabel('Entropy [J/K]')
plt.ylabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for CO2')
plt.tight_layout()
fig.savefig("files/co2_z_Contour_TS.pdf")
print("plotcontour.py called")