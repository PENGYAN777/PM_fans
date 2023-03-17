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
fluidname = "Ethylene"

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
n = 100 # number of points
x = np.linspace(Tmin, 500,n)
y = np.linspace(1e5, 5e7,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [1.0, 1.1, 1.2,1.3,1.4,1.5,1.6], cmap='rainbow')
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

z9_p = [ 6.05e6, 5.54e6,  5.04e6, 4.53e6,   4.03e6,  3.53e6,    ]
z9_t = [  424.25, 415.83, 406.71,  396.89,  384.97,  371.64,    ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 6.05e6,   5.54e6, 5.04e6,  4.53e6,  4.03e6, 3.53e6,   ]
z8_t = [  358.31,   350.60, 342.18,  332.36,  321.84, 309.92,   ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [  7.56e6, 7.05e6,  6.55e6, 6.05e6,  5.54e6,  5.04e6,    ]
z7_t = [  344.29, 338.67,  333.06,  326.75,  319.74, 311.32,    ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 9.07e6, 8.57e6,  8.06e6,   7.56e6,  7.06e6,  6.55e6,    ]
z6_t = [  336.57,  333.06,  329.56,  324.65, 319.74,  314.83,    ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 9.07e6, 8.57e6,  8.06e6,  7.56e6,  7.06e6,  6.55e6,  ]
z5_t = [ 322.54, 319.74,  316.23,   312.72, 308.51,  303.60,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ ]
z4_t = [  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)




plt.ylim(1e5,5e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(150, 500)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Ethylene')
plt.tight_layout()
fig.savefig("files/Ethylene_z_Contour_PT.pdf")
print("plotcontour.py called")