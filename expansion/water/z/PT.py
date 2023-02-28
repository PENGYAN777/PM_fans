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
fluidname = "Water"

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
x = np.linspace(400, 1200,n)
y = np.linspace(5e6, 5e8,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [1.0,1.1,1.2,1.3,1.4,1.5,1.6], cmap='rainbow')
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

z9_p = [3.53e7, 2.87e7, 2.2e7, 1.54e7,  1.21e7, 8.8e6,  ]
z9_t = [978.75, 938.67, 887.37, 816.83,  771.94, 712.62,  ]
plt.plot(z9_t,z9_p,'o' ,color=colors[0], lw = lw)

z8_p = [3.53e7, 2.87e7,  2.2e7,  1.54e7,  8.8e6, 4.19e7,     ]
z8_t = [848.89,  812.02, 765.53,  704.61,  614.83,  877.75,   ]
plt.plot(z8_t,z8_p,'o' ,color=colors[1], lw = lw)

z7_p = [4.41e7, 3.97e7, 3.53e7,  3.09e7, 2.65e7,  2.2e7,     ]
z7_t = [818.43, 802.40,  783.16, 762.32,  738.27,  707.81,   ]
plt.plot(z7_t,z7_p,'o' ,color=colors[2], lw = lw)

z6_p = [5.5e7, 5.07e7,  4.6e7,  4.19e7,  3.75e7, 3.31e7,     ]
z6_t = [804.00, 794.38,  781.56,  768.73,  754.3, 735.07,    ]
plt.plot(z6_t,z6_p,'o' ,color=colors[3], lw = lw)

z5_p = [ 5.5e7, 5.07e7, 4.63e7,  4.19e7,  3.75e7, 3.31e7,    ]
z5_t = [ 769.73, 760.72,  751.10, 741.48, 727.05,  712.62,   ]
plt.plot(z5_t,z5_p,'o' ,color=colors[4], lw = lw)

z4_p = [5.51e7, 5.07e7, 4.6e7, 4.2e7, 3.97e7,  4.4e7,  ]
z4_t = [735.07, 731.86, 727.05, 719.04, 714.29,  723.84,  ]
plt.plot(z4_t,z4_p,'o' ,color=colors[5], lw = lw)




plt.ylim(5e6,5e8)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, 1200)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for Water')
plt.tight_layout()
fig.savefig("files/Water_z_Contour_PT.pdf")
print("plotcontour.py called")