#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:46:40 2023

@author: yan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:04:05 2023

compute downstream Mach number  for nonideal flow

@author: yan
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


"""
0. get data
"""
z91= pd.read_csv("z9/z1.csv", ",", skiprows=0)
z92= pd.read_csv("z9/z2.csv", ",", skiprows=0)
z93= pd.read_csv("z9/z3.csv", ",", skiprows=0)
z94= pd.read_csv("z9/z4.csv", ",", skiprows=0)
z95= pd.read_csv("z9/z5.csv", ",", skiprows=0)
z96= pd.read_csv("z9/z6.csv", ",", skiprows=0)

z81= pd.read_csv("z8/z1.csv", ",", skiprows=0)
z82= pd.read_csv("z8/z2.csv", ",", skiprows=0)
z83= pd.read_csv("z8/z3.csv", ",", skiprows=0)
z84= pd.read_csv("z8/z4.csv", ",", skiprows=0)
z85= pd.read_csv("z8/z5.csv", ",", skiprows=0)
z86= pd.read_csv("z8/z6.csv", ",", skiprows=0)

z71= pd.read_csv("z7/z1.csv", ",", skiprows=0)
z72= pd.read_csv("z7/z2.csv", ",", skiprows=0)
z73= pd.read_csv("z7/z3.csv", ",", skiprows=0)
z74= pd.read_csv("z7/z4.csv", ",", skiprows=0)
z75= pd.read_csv("z7/z5.csv", ",", skiprows=0)
z76= pd.read_csv("z7/z6.csv", ",", skiprows=0)

z61= pd.read_csv("z6/z1.csv", ",", skiprows=0)
z62= pd.read_csv("z6/z2.csv", ",", skiprows=0)
z63= pd.read_csv("z6/z3.csv", ",", skiprows=0)
z64= pd.read_csv("z6/z4.csv", ",", skiprows=0)
z65= pd.read_csv("z6/z5.csv", ",", skiprows=0)
z66= pd.read_csv("z6/z6.csv", ",", skiprows=0)


"""
1. input theta and upstream Mach number, compute downstream data
"""
n = 50
"""
Z9
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z91_m2 = np.zeros(n) 
z92_m2 = np.zeros(n) 
z93_m2 = np.zeros(n) 
z94_m2 = np.zeros(n) 
z95_m2 = np.zeros(n) 
z96_m2 = np.zeros(n) 

z91_P2 = np.zeros(n) 
z92_P2 = np.zeros(n) 
z93_P2 = np.zeros(n) 
z94_P2 = np.zeros(n) 
z95_P2 = np.zeros(n) 
z96_P2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z91.iloc[:,6][np.argmin(abs(z91.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z91.iloc[:,5][np.argmin(abs(z91.iloc[:,6]-nu2))] 
    z91_m2[i] = M2
    P2 = z91.iloc[:,2][np.argmin(abs(z91.iloc[:,6]-nu2))] 
    z91_P2[i] = P2
    # for z2
    nu1 = z92.iloc[:,6][np.argmin(abs(z92.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z92.iloc[:,5][np.argmin(abs(z92.iloc[:,6]-nu2))] 
    z92_m2[i] = M2
    P2 = z92.iloc[:,2][np.argmin(abs(z92.iloc[:,6]-nu2))] 
    z92_P2[i] = P2
    # for z3
    nu1 = z93.iloc[:,6][np.argmin(abs(z93.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z93.iloc[:,5][np.argmin(abs(z93.iloc[:,6]-nu2))] 
    z93_m2[i] = M2
    P2 = z93.iloc[:,2][np.argmin(abs(z93.iloc[:,6]-nu2))] 
    z93_P2[i] = P2
    # for z4
    nu1 = z94.iloc[:,6][np.argmin(abs(z94.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z94.iloc[:,5][np.argmin(abs(z94.iloc[:,6]-nu2))] 
    z94_m2[i] = M2
    P2 = z94.iloc[:,2][np.argmin(abs(z94.iloc[:,6]-nu2))] 
    z94_P2[i] = P2
    # for z5
    nu1 = z95.iloc[:,6][np.argmin(abs(z95.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z95.iloc[:,5][np.argmin(abs(z95.iloc[:,6]-nu2))] 
    z95_m2[i] = M2
    P2 = z95.iloc[:,2][np.argmin(abs(z95.iloc[:,6]-nu2))] 
    z95_P2[i] = P2
    # for z6
    nu1 = z96.iloc[:,6][np.argmin(abs(z96.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z96.iloc[:,5][np.argmin(abs(z96.iloc[:,6]-nu2))] 
    z96_m2[i] = M2
    P2 = z96.iloc[:,2][np.argmin(abs(z96.iloc[:,6]-nu2))] 
    z96_P2[i] = P2
"""
Z8
"""
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z81_m2 = np.zeros(n) 
z82_m2 = np.zeros(n) 
z83_m2 = np.zeros(n) 
z84_m2 = np.zeros(n) 
z85_m2 = np.zeros(n) 
z86_m2 = np.zeros(n) 

z81_P2 = np.zeros(n) 
z82_P2 = np.zeros(n) 
z83_P2 = np.zeros(n) 
z84_P2 = np.zeros(n) 
z85_P2 = np.zeros(n) 
z86_P2 = np.zeros(n) 

for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z81.iloc[:,6][np.argmin(abs(z81.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z81.iloc[:,5][np.argmin(abs(z81.iloc[:,6]-nu2))] 
    z81_m2[i] = M2
    P2 = z81.iloc[:,2][np.argmin(abs(z81.iloc[:,6]-nu2))] 
    z81_P2[i] = P2
    # for z2
    nu1 = z82.iloc[:,6][np.argmin(abs(z82.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z82.iloc[:,5][np.argmin(abs(z82.iloc[:,6]-nu2))] 
    z82_m2[i] = M2
    P2 = z82.iloc[:,2][np.argmin(abs(z82.iloc[:,6]-nu2))] 
    z82_P2[i] = P2
    # for z3
    nu1 = z83.iloc[:,6][np.argmin(abs(z83.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z83.iloc[:,5][np.argmin(abs(z83.iloc[:,6]-nu2))] 
    z83_m2[i] = M2
    P2 = z83.iloc[:,2][np.argmin(abs(z83.iloc[:,6]-nu2))] 
    z83_P2[i] = P2
    # for z4
    nu1 = z84.iloc[:,6][np.argmin(abs(z84.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z84.iloc[:,5][np.argmin(abs(z84.iloc[:,6]-nu2))] 
    z84_m2[i] = M2
    P2 = z84.iloc[:,2][np.argmin(abs(z84.iloc[:,6]-nu2))] 
    z84_P2[i] = P2
    # for z5
    nu1 = z85.iloc[:,6][np.argmin(abs(z85.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z85.iloc[:,5][np.argmin(abs(z85.iloc[:,6]-nu2))] 
    z85_m2[i] = M2
    P2 = z85.iloc[:,2][np.argmin(abs(z85.iloc[:,6]-nu2))] 
    z85_P2[i] = P2
    # for z6
    nu1 = z86.iloc[:,6][np.argmin(abs(z86.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z86.iloc[:,5][np.argmin(abs(z86.iloc[:,6]-nu2))] 
    z86_m2[i] = M2
    P2 = z86.iloc[:,2][np.argmin(abs(z86.iloc[:,6]-nu2))] 
    z86_P2[i] = P2
"""
Z7
"""    
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z71_m2 = np.zeros(n) 
z72_m2 = np.zeros(n) 
z73_m2 = np.zeros(n) 
z74_m2 = np.zeros(n) 
z75_m2 = np.zeros(n) 
z76_m2 = np.zeros(n) 

z71_P2 = np.zeros(n) 
z72_P2 = np.zeros(n) 
z73_P2 = np.zeros(n) 
z74_P2 = np.zeros(n) 
z75_P2 = np.zeros(n) 
z76_P2 = np.zeros(n) 
for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z71.iloc[:,6][np.argmin(abs(z71.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z71.iloc[:,5][np.argmin(abs(z71.iloc[:,6]-nu2))] 
    z71_m2[i] = M2
    P2 = z71.iloc[:,2][np.argmin(abs(z71.iloc[:,6]-nu2))] 
    z71_P2[i] = P2
    # for z2
    nu1 = z72.iloc[:,6][np.argmin(abs(z72.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z72.iloc[:,5][np.argmin(abs(z72.iloc[:,6]-nu2))] 
    z72_m2[i] = M2
    P2 = z72.iloc[:,2][np.argmin(abs(z72.iloc[:,6]-nu2))] 
    z72_P2[i] = P2
    # for z3
    nu1 = z73.iloc[:,6][np.argmin(abs(z73.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z73.iloc[:,5][np.argmin(abs(z73.iloc[:,6]-nu2))] 
    z73_m2[i] = M2
    P2 = z73.iloc[:,2][np.argmin(abs(z73.iloc[:,6]-nu2))] 
    z73_P2[i] = P2
    # for z4
    nu1 = z74.iloc[:,6][np.argmin(abs(z74.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z74.iloc[:,5][np.argmin(abs(z74.iloc[:,6]-nu2))] 
    z74_m2[i] = M2
    P2 = z74.iloc[:,2][np.argmin(abs(z74.iloc[:,6]-nu2))] 
    z74_P2[i] = P2
    # for z5
    nu1 = z75.iloc[:,6][np.argmin(abs(z75.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z75.iloc[:,5][np.argmin(abs(z75.iloc[:,6]-nu2))] 
    z75_m2[i] = M2
    P2 = z75.iloc[:,2][np.argmin(abs(z75.iloc[:,6]-nu2))] 
    z75_P2[i] = P2
    # for z6
    nu1 = z76.iloc[:,6][np.argmin(abs(z76.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z76.iloc[:,5][np.argmin(abs(z76.iloc[:,6]-nu2))] 
    z76_m2[i] = M2
    P2 = z76.iloc[:,2][np.argmin(abs(z76.iloc[:,6]-nu2))] 
    z76_P2[i] = P2
"""
Z6
"""    
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z61_m2 = np.zeros(n) 
z62_m2 = np.zeros(n) 
z63_m2 = np.zeros(n) 
z64_m2 = np.zeros(n) 
z65_m2 = np.zeros(n) 
z66_m2 = np.zeros(n) 

z61_P2 = np.zeros(n) 
z62_P2 = np.zeros(n) 
z63_P2 = np.zeros(n) 
z64_P2 = np.zeros(n) 
z65_P2 = np.zeros(n) 
z66_P2 = np.zeros(n) 
for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z61.iloc[:,6][np.argmin(abs(z61.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z61.iloc[:,5][np.argmin(abs(z61.iloc[:,6]-nu2))] 
    z61_m2[i] = M2
    P2 = z61.iloc[:,2][np.argmin(abs(z61.iloc[:,6]-nu2))] 
    z61_P2[i] = P2
    # for z2
    nu1 = z62.iloc[:,6][np.argmin(abs(z62.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z62.iloc[:,5][np.argmin(abs(z62.iloc[:,6]-nu2))] 
    z62_m2[i] = M2
    P2 = z62.iloc[:,2][np.argmin(abs(z62.iloc[:,6]-nu2))] 
    z62_P2[i] = P2
    # for z3
    nu1 = z63.iloc[:,6][np.argmin(abs(z63.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z63.iloc[:,5][np.argmin(abs(z63.iloc[:,6]-nu2))] 
    z63_m2[i] = M2
    P2 = z63.iloc[:,2][np.argmin(abs(z63.iloc[:,6]-nu2))] 
    z63_P2[i] = P2
    # for z4
    nu1 = z64.iloc[:,6][np.argmin(abs(z64.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z64.iloc[:,5][np.argmin(abs(z64.iloc[:,6]-nu2))] 
    z64_m2[i] = M2
    P2 = z64.iloc[:,2][np.argmin(abs(z64.iloc[:,6]-nu2))] 
    z64_P2[i] = P2
    # for z5
    nu1 = z65.iloc[:,6][np.argmin(abs(z65.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z65.iloc[:,5][np.argmin(abs(z65.iloc[:,6]-nu2))] 
    z65_m2[i] = M2
    P2 = z65.iloc[:,2][np.argmin(abs(z65.iloc[:,6]-nu2))] 
    z65_P2[i] = P2
    # for z6
    nu1 = z66.iloc[:,6][np.argmin(abs(z66.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z66.iloc[:,5][np.argmin(abs(z66.iloc[:,6]-nu2))] 
    z66_m2[i] = M2
    P2 = z66.iloc[:,2][np.argmin(abs(z66.iloc[:,6]-nu2))] 
    z66_P2[i] = P2

"""
2. plot
"""

nc = 10
colors = plt.cm.tab20(np.linspace(0, 1, nc))

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(theta/math.pi*180  , z91_m2 , color=colors[0], lw=lwh, label="$Z_t=0.9$")
axes.plot(theta/math.pi*180  , z92_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , z93_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , z94_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , z95_m2 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , z96_m2 , color=colors[0], lw=lwh)

axes.plot(theta/math.pi*180  , z81_m2 , color=colors[1], lw=lwh,label="$Z_t=0.8$")
axes.plot(theta/math.pi*180  , z82_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , z83_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , z84_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , z85_m2 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , z86_m2 , color=colors[1], lw=lwh)

axes.plot(theta/math.pi*180  , z71_m2 , color=colors[2], lw=lwh, label="$Z_t=0.7$")
axes.plot(theta/math.pi*180  , z72_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , z73_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , z74_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , z75_m2 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , z76_m2 , color=colors[2], lw=lwh)

axes.plot(theta/math.pi*180  , z61_m2 , color=colors[3], lw=lwh, label="$Z_t=0.6$")
axes.plot(theta/math.pi*180  , z62_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , z63_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , z64_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , z65_m2 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , z66_m2 , color=colors[3], lw=lwh)




axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("Propylene_z_M2_theta.eps")

###############################################################################
fig3 = plt.figure( dpi=300)
lwh = 2
axes = fig3.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# see  the corresponding coolprop.py, to see pp[i]]pt or Pc
axes.plot(theta/math.pi*180  , (2432525-z91_P2*4099500)/2432525, color=colors[0], lw=lwh, label="$Z_t=0.9$")
axes.plot(theta/math.pi*180  , (2159863-z92_P2*3644000)/2159863 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (1889025-z93_P2* 3188500)/1889025 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (1618187-z94_P2*2733000)/1618187, color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (1345526.-z95_P2*2277500.)/1345526., color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (1073776.-z96_P2*1822000)/1073776. , color=colors[0], lw=lwh)

axes.plot(theta/math.pi*180  , (4327250-z81_P2*7288000)/4327250 , color=colors[1], lw=lwh, label="$Z_t=0.8$")
axes.plot(theta/math.pi*180  , (3970236-z82_P2*6604750)/3970236 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (3563295-z83_P2*5921500)/3563295 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (3150883-z84_P2*5238250)/3150883 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (2737103-z85_P2*  4555000)/2737103 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (2322639-z86_P2*3871750)/2322639 , color=colors[1], lw=lwh)

axes.plot(theta/math.pi*180  , (5549439-z71_P2*9110000)/5549439, color=colors[2], lw=lwh, label="$Z_t=0.7$")
axes.plot(theta/math.pi*180  , (5005484-z72_P2*8199000)/5005484 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (4327250-z73_P2*7288000)/4327250 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (3893407-z74_P2*6377000)/3893407, color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (3339421-z75_P2*5466000)/3339421, color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (2778139-z76_P2*4555000)/2778139, color=colors[2], lw=lwh)

axes.plot(theta/math.pi*180  , (5642454-z61_P2*9110000)/5642454, color=colors[3], lw=lwh, label="$Z_t=0.6$")
axes.plot(theta/math.pi*180  , (5093028-z62_P2*8199000)/5093028, color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (4327250-z63_P2*7288000)/4327250, color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (3972288-z64_P2*6377000)/3972288 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (3404167-z65_P2*5466000)/3404167, color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (2833766-z66_P2*4555000.)/2833766 , color=colors[3], lw=lwh)




axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$\Delta P$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig3.savefig("Propylene_z_dp_theta.eps")



