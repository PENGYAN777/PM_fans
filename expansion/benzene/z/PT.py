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
fluidname = "Benzene"

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
y = np.linspace(5e5, 5e7,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.6,0.7,0.8,0.9,1.0,1.1], cmap='rainbow')
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

z9_p = [3.42e6, 2.93e6, 2.44e6, 1.95e6, 1.468e6, 9.79e5,   ] 
z9_t = [723.04, 696.34, 664.43, 625.35, 577.15, 512.67,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [6.85e6, 5.87e6, 4.89e6, 3.9e6, 2.9e6,  1.957e6, ]
z8_t = [722.39, 698.94, 670.29, 635.12, 588.87, 526.35,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 8.81e6, 7.83e6, 6.85e6, 5.87e6,  4.89e6, 3.91e6,  ]
z7_t = [ 697.64, 682.66, 664.43, 642.93, 616.23, 583.01,  ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 8.81e6, 7.83e6, 6.85e6, 5.87e6, 4.89e6, 3.9e6,  ]
z6_t = [ 661.17, 647.49, 631.21, 611.02, 586.92, 556.31,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 9.79e6,  8.81e6, 7.83e6, 6.85e6, 5.87e6, 4.89e6,  ]
z5_t = [ 645.54,  636.42, 624.70, 610.37, 592.78, 570.64,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [9.79e6, 9.30e6,  8.81e6, 8.32e6,  7.83e6, 7.34e6,  ]   
z4_t = [ 620.14, 618.83, 616.23, 612.97, 609.07, 603.85,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Alkene Benzene')
plt.tight_layout()
fig.savefig("files/Benzene_z_Contour_PT.pdf")
print("plotcontour.py called")