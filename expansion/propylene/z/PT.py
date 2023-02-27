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
fluidname = "Propylene"

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

z9_p = [4.1e6, 3.64e6, 3.188e6, 2.73e6, 2.27e6, 1.82e6,  ] 
z9_t = [ 508.31, 493.98, 477.45,  458.71, 436.12, 409.12,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [7.288e6, 6.6e6, 5.92e6, 5.23e6, 4.55e6, 3.87e6,  ]
z8_t = [490.13, 479.66, 468.63, 454.96, 439.43, 421.24,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [9.11e6, 8.19e6, 7.288e6, 6.377e6, 5.466e6, 4.55e6,  ]
z7_t = [ 466.98, 456.16, 447.69, 435.02, 419.59, 401.10,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [9.11e6, 8.199e6, 7.288e6, 6.377e6, 5.466e6,  4.55e6, ]
z6_t = [439.42, 432.26, 422.89, 411.32, 397.54, 380.46,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [9.11e6, 8.199e6, 7.288e6, 6.377e6, 5.466e6, 4.55e6,  ]
z5_t = [ 420.14, 414.63, 406.91, 396.99, 384.87, 369.44,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [9.11e6, 8.42e6, 7.743e6, 7.06e6, 6.377e6, 6.718e6,  ]   
z4_t = [401.95, 400.85, 398.09, 393.68, 388.17, 390.93,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(250, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Alkene Propylene')
plt.tight_layout()
fig.savefig("files/Propylene_z_Contour_PT.pdf")
print("plotcontour.py called")