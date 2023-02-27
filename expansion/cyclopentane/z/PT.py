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
fluidname = "Cyclopentane"

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
x = np.linspace(350, Tmax,n)
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

z9_p = [1.37e6, 1.28e6, 1.188e6, 1.1e6, 1.0e6, 9.14e5,   ] 
z9_t = [ 532.46, 521.94, 506.60, 498.09, 484.77, 471.44,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [2.7e6,  2.60e6, 2.46e6, 2.33e6, 2.19e6, 2.057e6,  ]
z8_t = [544.39, 536.67, 528.25, 519.84, 508.60, 501.60,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [3.88e6, 3.65e6,  3.42e6,  3.2e6, 2.97e6, 2.74e6, ]
z7_t = [ 545.79, 537.37, 528.95,  519.14, 506.60, 498.09,  ] 
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [4.80e6, 4.57e6, 4.34e6, 4.11e6, 3.88e6, 3.42e6,  ]
z6_t = [545.09, 538.78, 532.46, 526.15, 518.43, 503.00,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [5.71e6, 5.48e6,  5.25e6, 5.028e6, 4.80e6, 4.57e6,  ]
z5_t = [545.79, 541.58, 537.37,  532.46, 527.55, 522.64,   ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 6.17e6, 5.94e6, 5.714e6, 5.48e6, 5.25e6, 5.028e6,  ]   
z4_t = [541.58, 538.07, 534.57, 531.06, 527.55, 523.34,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(350, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Cyclic Alkanes Cyclopentane')
plt.tight_layout()
fig.savefig("files/Cyclopentane_z_Contour_PT.pdf")
print("plotcontour.py called")