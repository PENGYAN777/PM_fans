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
fluidname = "CycloHexane"

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
x = np.linspace(400, Tmax,n)
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

z9_p = [2.04e6, 1.837e6, 1.632e6, 1.428e6, 1.22e6, 1.02e6,  ] 
z9_t = [ 661.52, 642.28, 619.94, 595.79, 569.338, 538.87,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [3.67e6, 3.26e6, 2.85e6, 2.45e6, 2.04e6, 1.63e6,  ]
z8_t = [ 649.49, 629.46, 607.01, 581.36, 548.06, 518.03,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [6.12e6, 5.71e6, 5.3e6, 4.89e6,  4.49e6, 3.878e6,  ]
z7_t = [ 669.54,659.92, 648.69,  636.67, 623.84,  601.40,  ] 
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [7.75e6, 7.348e6, 6.94e6, 5.92e6, 5.3e6, 4.69e6,  ]
z6_t = [659.92, 654.31, 647.89,  628.65, 614.23, 597.39,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [7.75e6, 7.14e6, 6.53e6, 5.92e6, 5.307e6, 4.69e6,  ]
z5_t = [ 631.86, 625.45, 616.63, 606.21, 594.12, 579.76,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 7.75e6,  7.14e6, 6.53e6, 5.92e6, 5.30e6,  4.69e6,  ]   
z4_t = [ 607.01, 603.80, 598.99, 591.78, 582.16, 570.14,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Cyclic Alkanes CycloHexane')
plt.tight_layout()
fig.savefig("files/CycloHexane_z_Contour_PT.pdf")
print("plotcontour.py called")