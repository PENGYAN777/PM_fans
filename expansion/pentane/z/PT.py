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
fluidname = "n-Pentane"

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

z9_p = [2.69e6, 2.357e6,  2.02e6, 1.68e6, 1.347e6, 1.01e6, ] 
z9_t = [621.94, 603.00, 580.56,  554.61,  523.04, 483.06, ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 4.71e6, 4.04e6, 3.367e6, 2.69e6,  2.02e6, 2.357e6, ]
z8_t = [602.30, 583.36, 559.52, 530.06, 492.18,  512.52, ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [6.06e6, 5.39e6, 4.71e6, 4.04e6,  3.7e6,  3.03e6, ]
z7_t = [582.66, 570.04, 554.61, 536.37, 525.85, 502.00,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [6.735e6, 6.06e6,  5.39e6, 4.714e6, 4.04e6, 3.36e6, ]
z6_t = [560.92,  551.80, 540.58, 527.25,  510.42, 490.08, ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [6.73e6, 6.06e6, 5.39e6, 4.71e6, 4.04e6,  3.36e6, ]
z5_t = [538.47, 531.46, 521.64,  509.72, 494.99, 476.75, ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [6.73e6, 6.06e6, 5.39e6, 4.71e6, 4.377e6, 3.7e6,  ]
z4_t = [516.73, 513.92, 508.31, 499.20, 493.58, 479.56,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Alkanes n-Pentane')
plt.tight_layout()
fig.savefig("files/nPentane_z_Contour_PT.pdf")
print("plotcontour.py called")