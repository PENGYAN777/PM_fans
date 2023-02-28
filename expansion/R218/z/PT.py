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
fluidname = "R218"

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
y = np.linspace(5e5, 2e7,n)
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

z9_p = [ 1.84e6, 1.716e6, 1.58e6,  1.45e6, 1.32e6, 1.18e6,  ] 
z9_t = [ 436.91, 429.34,  421.20, 412.22, 402.68, 391.74,   ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 3.16e6, 2.9e6, 2.64e6, 2.376e6, 2.11e6, 1.85e6,  ]
z8_t = [ 424.85, 416.99, 408.01, 398.19, 387.25, 374.63,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 4.22e6, 3.82e6, 3.43e6, 3.03e6, 2.64e6, 2.24e6,  ]
z7_t = [ 415.31, 407.73,399.04, 388.93,  376.87, 362.84,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 5.28e6, 4.88e6, 4.488e6, 4.09e6, 3.69e6, 3.3e6,   ]
z6_t = [ 407.45, 403.24, 398.19,  392.30, 385.29,  376.87,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [5.28e6, 4.88e6, 4.488e6, 4.09e6, 3.69e6, 3.3e6,   ]
z5_t = [ 390.90, 387.81, 383.88, 378.83, 372.94, 365.65,   ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 5.28e6, 4.88e6, 4.49e6, 4.09e6,  3.69e6, 3.3e6,  ]   
z4_t = [ 375.19, 374.62, 372.94,  369.58, 365.09, 359.19,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(250, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Halocarbon R218')
plt.tight_layout()
fig.savefig("files/R218_z_Contour_PT.pdf")
print("plotcontour.py called")