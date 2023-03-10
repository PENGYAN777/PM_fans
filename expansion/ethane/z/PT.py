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
fluidname = "Ethane"

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
x = np.linspace(Tmin, 600,n)
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

z9_p = [ 5.84e6, 5.11e6,  4.38e6,  3.65e6,   2.92e6,  2.19e6,    ]
z9_t = [  456.51,  443.18, 427.05,  408.11,  384.27,   354.11,   ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [  5.84e6,  5.11e6,  4.38e6, 3.65e6,   2.92e6,  2.19e6,  ]
z8_t = [  386.37,  373.74,  359.02, 341.48,  320.44,  294.49,   ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [  8.77e6,  8.04e6,  7.31e6,  6.57e6,  5.84e6,  5.11e6,  ]
z7_t = [  385.67,   379.36, 371.64,  362.52,  352.70,  340.78,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 8.77e6,  8.04e6, 7.3e6,  6.57e6,  5.84e6,  5.11e6,    ]
z6_t = [  363.22,  357.61, 350.60, 342.88,  333.76, 323.24,   ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [  ]
z5_t = [  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ ]
z4_t = [  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)




plt.ylim(1e5,5e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(150, 600)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Ethane ')
plt.tight_layout()
fig.savefig("files/Ethane _z_Contour_PT.pdf")
print("plotcontour.py called")