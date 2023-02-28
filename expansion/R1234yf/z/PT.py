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
fluidname = "R1234yf"

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
x = np.linspace(280, Tmax,n)
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

z9_p = [ 1.18e6, 1.11e6, 1.05e6, 9.81e5, 9.25e5, 8.45e5,  ] 
z9_t = [ 396.55, 390.38, 383.76, 376.71, 371.64, 361.50,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 2.36e6, 2.2e6, 2.03e6, 1.86e6, 1.60e6, 1.43e6,  ]
z8_t = [ 402.06, 394.79, 386.63, 378.03, 363.92, 353.12,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [3.04e6, 2.7e6, 2.42e6, 2.03e6, 1.69e6, 1.86e6,  ]
z7_t = [393.24,  382.22, 371.64, 355.99, 339.68, 348.05,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 4.06e6, 3.89e6, 3.72e6, 3.55e6, 3.38e6, 3.21e6,  ]
z6_t = [ 399.42, 395.89, 392.14, 388.17, 383.98, 379.48,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 4.73e6, 4.56e6, 4.39e6, 4.22e6, 4.06e6, 3.89e6,  ]
z5_t = [ 398.98, 396.33, 393.46, 390.60, 387.51, 384.21,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [5.41e6, 5.14e6, 4.87e6, 4.6e6, 4.33e6,  4.46e6,  ]   
z4_t = [ 397.43, 394.79,391.92, 388.83, 385.09, 386.85,   ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(280, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Halocarbon R1234yf')
plt.tight_layout()
fig.savefig("files/R1234yf_z_Contour_PT.pdf")
print("plotcontour.py called")