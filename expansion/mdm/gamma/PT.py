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
fluidname = "MDM"

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
n = 500 # number of points
x = np.linspace(400, Tmax,n)
y = np.linspace(5e4, 5e6,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','T',X,'P',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','T',X,'P',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.4,0.5,0.6,0.7,0.8,0.9,1.0], cmap='rainbow')
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
z9_p = [4.23e5, 3.80e5, 3.38e5, 2.96e5,  2.53e5, 2.11e5, ]
z9_t = [569.88, 552.99, 539.66, 520.32, 500.76, 478.09, ]
plt.plot(z9_t,z9_p,'ko',lw = lw)

z8_p = [7.05e5, 6.34e5, 5.64e5,4.93e5, 4.23e5,  3.52e5, ]
z8_t = [569.88,  557.44, 543.44, 527.43, 508.98, 486.98, ]
plt.plot(z8_t,z8_p,'ro',lw = lw)

z7_p = [9.16e5, 8.178e5, 7.75e5, 7.05e5,6.34e5,  5.64e5, ]
z7_t = [570.55, 558.45, 552.99, 542.32, 530.54, 517.21, ]
plt.plot(z7_t,z7_p,'bo',lw = lw)

z6_p = [1.128e6, 9.588e5, 9.16e5, 8.74e5, 7.89e5,  7.05e5, ]
z6_t = [573.89, 558.45,  554.99, 550.10,  539.66, 527.43, ]
plt.plot(z6_t,z6_p,'k*',lw = lw)

z5_p = [1.27e6, 1.226e6, 1.057e6, 1.015e6, 9.306e5,  8.46e5, ]
z5_t = [572.33,  570.11, 558.45, 554.99, 546.77, 539.43, ]
plt.plot(z5_t,z5_p,'r*',lw = lw)


plt.ylim(5e4,5e6)
plt.gca().set_yscale('log')
plt.gca().set_xlim(400, Tmax)
plt.ylabel('Pressure [Pa]')
plt.xlabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for siloxane MDM')
plt.tight_layout()
fig.savefig("files/mdm_g_Contour_PT.pdf")
print("plotcontour.py called")