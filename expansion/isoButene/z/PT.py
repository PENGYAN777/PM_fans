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
fluidname = "IsoButene"

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
x = np.linspace(300, Tmax,n)
y = np.linspace(5e5, 5e7,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.8,0.9,1.0,1.1,1.2,1.3,1.4], cmap='rainbow')
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

z9_p = [ 2.8e6, 2.40e6,  2.0e6, 1.60e6, 1.2e6, 8.02e5,  ] 
z9_t = [  546.49, 524.94, 499.89, 469.84, 432.26, 383.16,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [4.81e6, 4.21e6, 3.6e6,  3.0e6, 2.4e6, 1.8e6,  ]
z8_t = [526.95, 510.42,  491.38, 468.33, 440.78, 406.71,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 6.4e6, 5.81e6, 5.21e6, 4.6e6, 4.0e6,  3.4e6,   ]
z7_t = [ 512.42, 502.40, 490.38, 476.85, 461.32, 442.78,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [7.21e6, 6.6e6, 6.01e6,  5.41e6, 4.81e6, 4.21e6,  ]
z6_t = [494.38, 486.87, 477.855, 467.83, 456.31, 442.78,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 8.02e6, 7.418e6, 6.81e6, 6.21e6, 5.61e6, 5.01e6,   ]
z5_t = [ 480.36, 475.85, 470.34, 463.32, 454.81, 445.29,   ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 8.02e6, 7.418e6, 6.816e6, 6.21e6, 5.61e6, 5.01e6,  ]   
z4_t = [ 460.32, 458.82, 455.81, 451.30, 444.79, 436.77,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Alkene IsoButene')
plt.tight_layout()
fig.savefig("files/IsoButene_z_Contour_PT.pdf")
print("plotcontour.py called")