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
fluidname = "MM"

# update fluid
fluid = CP.AbstractState("HEOS", fluidname)

pc = fluid.keyed_output(CP.iP_critical)
Tc = fluid.keyed_output(CP.iT_critical)
ec = CP.CoolProp.PropsSI('Smass','T',Tc,'P',pc,fluidname)
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
es = CP.CoolProp.PropsSI('Smass','T',Ts,'Q',1,fluidname)

# ----------------
# Contour of Z and Gamma
# ----------------
n = 100 # number of points
y = np.linspace(Tmin, Tmax,n)
x = np.linspace(300, 1600,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','Smass',X,'T|gas',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','Smass',X,'T',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4], cmap='rainbow')
plt.colorbar(location='right', orientation='vertical', label='$\Gamma$')
# ------
# Labels
# ------

plt.plot(es,Ts,'k',lw = lw, solid_capstyle = 'round', label = "LVS")
plt.plot(0,0,'k--',lw = lw/2, solid_capstyle = 'round', label = "Z")

# Critical lines
plt.axvline(ec, dashes = [2, 2])
plt.axhline(Tc, dashes = [2, 2])

"""
test points
"""
nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

g9_p = [1.35e6, 2.04e6, 2.53e6, 2.84e6, 2.94e6, 2.89e6]
g9_t = [604.06, 619.49, 616.75, 607.89, 595.31, 581.08]
g9_s = CP.CoolProp.PropsSI('Smass','P',g9_p,'T',g9_t,fluidname)
plt.plot(g9_s,g9_t,'o' ,color=colors[0], lw = lw,label = "$\Gamma=0.9$")

g85_p = [1.1e6, 1.398e6, 1.97e6, 2.37e6,  2.6e6, 1.65e6,   ]
g85_t = [552, 571.78,  588.20,  589.29,  572.88, 581.63,  ]
g85_s = CP.CoolProp.PropsSI('Smass','P',g85_p,'T',g85_t,fluidname)
plt.plot(g85_s,g85_t,'o' ,color=colors[1], lw = lw,label = "$\Gamma=0.85$")

g8_p = [8.01e5, 1.516e6,  1.97e6, 2.28e6, 2.4e6, 2.41e6,  ]
g8_t = [497.38, 555.92,  568.50, 569.60, 563.58, 554.28,  ]
g8_s = CP.CoolProp.PropsSI('Smass','P',g8_p,'T',g8_t,fluidname)
plt.plot(g8_s,g8_t,'o' ,color=colors[2], lw = lw,label = "$\Gamma=0.8$")

g75_p = [ 7.85e5, 1.34e6, 1.55e6, 1.73e6, 1.88e6, 2.0e6,  ]
g75_t = [ 480.42, 532.94, 543.33, 549.90,  553.73, 555.37, ]
g75_s = CP.CoolProp.PropsSI('Smass','P',g75_p,'T',g75_t,fluidname)
plt.plot(g75_s,g75_t,'o' ,color=colors[3], lw = lw,label = "$\Gamma=0.75$")

g7_p = [ 6.9e5, 8.3e5, 1.24e6, 1.34e6, 2.0e6 , 1.75e6,   ]
g7_t = [ 457, 476, 515.98, 522.54, 544.98, 540.60, ]
g7_s = CP.CoolProp.PropsSI('Smass','P',g7_p,'T',g7_t,fluidname)
plt.plot(g7_s,g7_t,'o' ,color=colors[5], lw = lw,label = "$\Gamma=0.7$")

ax.legend(loc=4) # 2 means left top

plt.ylim(400,Tmax)
# plt.gca().set_yscale('log')
plt.gca().set_xlim(600, 1400)
plt.xlabel('S [J/K]')
plt.ylabel('T [K]')
# plt.title('Contour of Z and $\Gamma$ for siloxane MM')
plt.tight_layout()
fig.savefig("files/mm_g_Contour_TS.eps")
print("plotcontour.py called")