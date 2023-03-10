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
fluidname = "Ammonia"

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
y = np.linspace(1e6, 1e8,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [1.0,1.1, 1.2,1.3,1.4,1.5, 1.6], cmap='rainbow')
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

z9_p = [ 1.7e7, 1.47e7,1.24e7, 1.02e7, 7.9e6, 5.66e6,   ]
z9_t = [  623.64, 606.61, 586.17, 560.62, 528.25, 484.82,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 2.26e7, 2.04e7, 1.81e7, 1.58e7, 1.13e7, 9.06e6,  ]
z8_t = [ 568.28, 557.21, 544.44, 529.11, 489.93, 463.52,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 3.17e7, 2.94e7, 2.72e7, 2.49e7,  2.26e7, 2.15e7,  ]
z7_t = [ 548.69, 543.58,  537.62, 529.96, 521.44, 516.33,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [3.28e7,  2.9e7,  2.6e7,  2.26e7, 1.9e7, 1.58e7,  ]
z6_t = [ 515.48,  510.37, 501.85, 491.63, 477.15, 459.27,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [3.28e7, 2.94e7,  2.6e7, 2.26e7, 1.92e7, 1.58e7,  ]
z5_t = [ 484.82, 483.11, 478.00, 470.34, 458.41, 443.08,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [2.94e7, 2.72e7,  2.49e7,  2.26e7,  2.04e7, 2.15e7,   ]
z4_t = [455.01, 456.71,  455.86,  453.31, 448.19,  450.75,   ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)




plt.ylim(1e6,1e8)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Ammonia')
plt.tight_layout()
fig.savefig("files/Ammonia_z_Contour_PT.pdf")
print("plotcontour.py called")