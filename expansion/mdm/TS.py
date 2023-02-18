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
ec = CP.CoolProp.PropsSI('Smass','T',Tc,'P',pc,"PR::MDM")
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
n = 200 # number of points
x = np.linspace(100, 1200,n)
y = np.linspace(400, Tmax,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','Smass',X,'T|gas',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','Smass',X,'T',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.4,0.5,0.6,0.7,0.8,0.9,1.0], cmap='rainbow')
plt.colorbar()
# ------
# Labels
# ------

plt.plot(es,Ts,'k',lw = lw, solid_capstyle = 'round', label = "LVS")
ax.legend(loc=4) # 2 means left top
# Critical lines
plt.axvline(ec, dashes = [2, 2])
plt.axhline(Tc, dashes = [2, 2])

"""
test points
"""
z9_p = [4.23e5, 3.83e5, 3.43e5, 3.03e5, 2.63e5, 2.23e5, ]
z9_t = [574.29, 558.44, 544.84, 528.00, 509.07, 488.08, ]
z9_s = CP.CoolProp.PropsSI('Smass','P',z9_p,'T',z9_t,fluidname)
plt.plot(z9_s,z9_t,'ko',lw = lw)

# z8_p = [2.52e6,2.12E6, 1.72E6, 1.32E6, 9.20E5, 5.21E5]
# z8_t = [643.45, 623.76, 598.05, 564.13, 515.98, 443.76]
# z8_s = CP.CoolProp.PropsSI('Smass','P',z8_p,'T',z8_t,fluidname)
# plt.plot(z8_s,z8_t,'ro',lw = lw)

# z7_p = [2.91E6, 2.51E6, 2.11E6, 1.71E6, 1.31E6, 9.08E5 ]
# z7_t = [610.08, 595.31, 576.16, 551.54, 519.26, 474.40]
# z7_s = CP.CoolProp.PropsSI('Smass','P',z7_p,'T',z7_t,fluidname)
# plt.plot(z7_s,z7_t,'bo',lw = lw)

# z6_p = [5e6, 4.3e6,  3.6e6, 2.9e6, 2.2e6, 1.5e6]
# z6_t = [619.38, 612.27, 599.69, 581.08, 553.733, 511.60]
# z6_s = CP.CoolProp.PropsSI('Smass','P',z6_p,'T',z6_t,fluidname)
# plt.plot(z6_s,z6_t,'k*',lw = lw)


plt.ylim(400,Tmax)
# plt.gca().set_yscale('log')
plt.gca().set_xlim(100, 1200)
plt.xlabel('Entropy [J/K]')
plt.ylabel('Temperature [K]')
plt.title('Contour of Z and $\Gamma$ for siloxane MDM')
plt.tight_layout()
fig.savefig("files/mdm_Contour_TS.pdf")
print("plotcontour.py called")