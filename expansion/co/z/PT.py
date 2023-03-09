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
fluidname = "CO"

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
x = np.linspace(Tmin, 550,n)
y = np.linspace(pmin, 5e7,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [1.0,1.2,1.4,1.6,1.8,2.0], cmap='rainbow')
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

z9_p = [ 5.24e6, 4.54e6,  3.84e6, 3.14e6,  2.49e6,  1.74e6,    ]
z9_t = [ 210.22, 204.21, 194.99,  187.77,  175.75,  159.72,    ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 5.24e6, 4.54e6, 3.84e6,  3.14e6,  2.44e6,  1.74e6,  ]
z8_t = [ 178.15, 172.54,  165.33,  156.51,  145.69, 131.66,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 5.24e6, 5.59e6,  6.29e6,  4.89e6,  4.19e6, 3.84e6,   ]
z7_t = [ 162.12,  164.53,  168.53,  159.72, 153.70,  150.10,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 6.29e6, 5.94e6,  5.59e6,  5.24e6, 4.89e6,  4.71e6,    ]
z6_t = [ 158.51,  156.91, 154.91,  152.90,  150.50, 149.90,    ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ ]
z5_t = [  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [  ]
z4_t = [ ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)




plt.ylim(1e5,5e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(Tmin, 300)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for CO')
plt.tight_layout()
fig.savefig("files/co_z_Contour_PT.pdf")
print("plotcontour.py called")