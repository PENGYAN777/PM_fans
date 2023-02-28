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
fluidname = "RC318"

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

z9_p = [ 2.5e6,  2.22e6, 1.94e6, 1.66e6, 1.39e6, 1.11e6,   ] 
z9_t = [ 517.49, 505.19,  490.30, 473.47,452.76, 427.51,   ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [ 4.16e6, 3.61e6, 3.05e6, 2.5e6,  1.94e6,  1.39e6,   ]
z8_t = [496.13,  483.18, 466.35, 446.29, 420.39,  384.49,   ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [ 5.55e6, 5e6, 4.44e6, 3.89e6, 3.33e6, 2.77e6,  ]
z7_t = [ 480.59, 473.47, 464.41, 453.41, 439.17, 422.39,   ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [ 6.1e6, 5.55e6,  5e6, 4.44e6, 3.88e6,  3.33e6,   ]
z6_t = [  461.17, 456.64, 450.17, 441.75, 431.40, 419.10,   ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 6.1e6, 5.55e6, 5e6, 4.44e6, 3.9e6, 3.33e6,    ]
z5_t = [ 441.10, 438.52, 433.99, 427.51, 418.45,  407.45,    ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [ 6.1e6, 5.55e6, 5e6, 4.44e6, 3.9e6, 3.33e6,    ]   
z4_t = [  419.10, 421.69, 420.39,  416.51,  410.04, 401.62,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Halocarbon RC318')
plt.tight_layout()
fig.savefig("files/RC318_z_Contour_PT.pdf")
print("plotcontour.py called")