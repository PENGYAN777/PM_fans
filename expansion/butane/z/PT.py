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
fluidname = "n-Butane"

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

z9_p = [3.037e6, 2.657e6, 2.277e6, 1.898e6, 1.518e6,  1.138e6, ] 
z9_t = [564.53, 546.89, 525.95,  501.70, 472.49, 435.57,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 4.93e6, 4.175e6,  3.416e6, 2.65e6, 2.27e6, 1.518e6,  ]
z8_t = [ 540.28, 520.44, 495.64, 464.78, 446.04, 398.09,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 7.6e6, 6.83e6,  6.07e6, 5.314e6,  4.55e6, 3.03e6, ]
z7_t = [539.72,  530.36, 518.78, 505.01, 487.92, 441.63,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [8.35e6, 7.6e6, 6.83e6, 6.07e6, 5.314e6, 4.55e6, ]
z6_t = [516.03, 509.97, 501.70,  491.23, 478.55, 463.12,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [8.35e6, 7.59e6, 6.83e6, 6.07e6,  5.31e6, 4.55e6, ]
z5_t = [ 491.78, 487.37, 481.31,  473.04, 462.57, 448.79, ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [8.35e6, 7.59e6,  6.83e6, 6.07e6, 5.31e6,  4.55e6, ]
z4_t = [ 465.88, 466.98, 465.33, 459.82, 452.10, 441.08,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,5e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Alkanes n-Butane')
plt.tight_layout()
fig.savefig("files/nButane_z_Contour_PT.pdf")
print("plotcontour.py called")