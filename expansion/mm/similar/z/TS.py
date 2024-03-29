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
n = 50 # number of points
y = np.linspace(400, Tmax,n)
x = np.linspace(600, 1600,n)
X,Y = np.meshgrid(x,y)
Z =  CP.CoolProp.PropsSI('Z','Smass',X,'T|gas',Y,fluidname)
Gamma =  CP.CoolProp.PropsSI('fundamental_derivative_of_gas_dynamics','Smass',X,'T',Y,fluidname)
#print(Z.shape)
levels = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
cp = plt.contour(X, Y, Z, levels, colors='black', linestyles='dashed')
plt.clabel(cp, inline=True,  fontsize=10)
plt.contourf(X, Y, Gamma, [0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4], cmap='rainbow')
plt.colorbar(label='$\Gamma$')
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

z9_p = [1.55e6,1.30E6,  1.05E6, 8.01E5, 5.51E5, 3.01E5]
z9_t = [673, 654.39, 624.85, 585.46, 531.30, 449.23]
z9_s = CP.CoolProp.PropsSI('Smass','P',z9_p,'T',z9_t,fluidname)
plt.plot(z9_s,z9_t,'o' ,color=colors[0],lw = lw,label = "Z=0.9")

z8_p = [2.52e6,2.12E6, 1.72E6, 1.32E6, 9.20E5, 5.21E5]
z8_t = [643.45, 623.76, 598.05, 564.13, 515.98, 443.76]
z8_s = CP.CoolProp.PropsSI('Smass','P',z8_p,'T',z8_t,fluidname)
plt.plot(z8_s,z8_t,'o' ,color=colors[1],lw = lw,label = "Z=0.8")

z7_p = [2.91E6, 2.51E6, 2.11E6, 1.71E6, 1.31E6, 9.08E5 ]
z7_t = [610.08, 595.31, 576.16, 551.54, 519.26, 474.40]
z7_s = CP.CoolProp.PropsSI('Smass','P',z7_p,'T',z7_t,fluidname)
plt.plot(z7_s,z7_t,'o' ,color=colors[2],lw = lw,label = "Z=0.7")

z6_p = [5e6, 4.3e6,  3.6e6, 2.9e6, 2.2e6, 1.5e6]
z6_t = [619.38, 612.27, 599.69, 581.08, 553.733, 511.60]
z6_s = CP.CoolProp.PropsSI('Smass','P',z6_p,'T',z6_t,fluidname)
plt.plot(z6_s,z6_t,'o' ,color=colors[3],lw = lw,label = "Z=0.6")

z5_p = [5e6, 4.35e6, 3.70e6, 3.05E6, 2.40E6, 1.75E6]
z5_t = [589.29, 588.20, 580.54, 567.41, 546.62, 515.98]
z5_s = CP.CoolProp.PropsSI('Smass','P',z5_p,'T',z5_t,fluidname)
plt.plot(z5_s,z5_t,'o' ,color=colors[4],lw = lw,label = "Z=0.5")

z4_p = [4e6,   3.6e6, 3.2e6, 2.8e6, 2.4e6, 2e6]
z4_t = [563.03,  561.94, 557.01, 548.81, 539.86, 523.09]
z4_s = CP.CoolProp.PropsSI('Smass','P',z4_p,'T',z4_t,fluidname)
plt.plot(z4_s,z4_t,'o' ,color=colors[5],lw = lw,label = "Z=0.4")

ax.legend(loc=4) # 2 means left top

plt.ylim(400,Tmax)
# plt.gca().set_yscale('log')
plt.gca().set_xlim(600, 1600)
plt.xlabel('S [J/K]')
plt.ylabel('T [K]')
# plt.title('Contour of Z and $\Gamma$ for siloxane MM')
plt.tight_layout()
fig.savefig("files/mm_z_Contour_TS.eps")
print("plotcontour.py called")