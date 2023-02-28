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
fluidname = "R1233zd(E)"

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

z9_p = [ 2.17e6, 1.99e6, 1.81e6, 1.63e6, 1.45e6, 1.268e6,  ] 
z9_t = [  548.49, 536.47, 523.44, 508.91, 492.88, 475.35,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [3.98e6, 3.62e6, 3.26e6,  2.89e6, 2.53e6, 2.17e6,  ]
z8_t = [ 536.47,  525.45, 512.42, 498.39, 481.86, 463.32,  ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [5.07e6, 4.35e6,3.62e6, 2.90e6, 2.17e6,  2.53e6,    ]
z7_t = [517.93, 501.90, 482.36, 457.81, 426.75, 444.29,   ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [7.24e6,  6.52e6, 5.79e6, 5.07e6, 4.35e6,  3.62e6,  ]
z6_t = [ 521.94, 513.92, 503.90, 491.88, 477.35,  459.32,  ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 7.97e6, 7.24e6, 6.52e6, 5.79e6, 5.07e6, 4.71e6,  ]
z5_t = [ 505.04, 501.40, 494.89, 486.87,  476.35, 469.84,  ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [7.97e6,  7.24e6, 6.52e6, 5.79e6, 5.43e6, 5.07e6,  ]   
z4_t = [ 480.36, 481.86, 479.36, 474.34, 470.84, 466.33,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)

plt.ylim(5e5,2e7)
plt.gca().set_yscale('log')
plt.gca().set_xlim(300, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Halocarbon R1233zd(E)')
plt.tight_layout()
fig.savefig("files/R1233zd(E)_z_Contour_PT.pdf")
print("plotcontour.py called")