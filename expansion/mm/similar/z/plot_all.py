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

z51= pd.read_csv("z5/z1.csv", ",", skiprows=0)
z52= pd.read_csv("z5/z2.csv", ",", skiprows=0)
z53= pd.read_csv("z5/z3.csv", ",", skiprows=0)
z54= pd.read_csv("z5/z4.csv", ",", skiprows=0)
z55= pd.read_csv("z5/z5.csv", ",", skiprows=0)
z56= pd.read_csv("z5/z6.csv", ",", skiprows=0)

z41= pd.read_csv("z4/z1.csv", ",", skiprows=0)
z42= pd.read_csv("z4/z2.csv", ",", skiprows=0)
z43= pd.read_csv("z4/z3.csv", ",", skiprows=0)
z44= pd.read_csv("z4/z4.csv", ",", skiprows=0)
z45= pd.read_csv("z4/z5.csv", ",", skiprows=0)
z46= pd.read_csv("z4/z6.csv", ",", skiprows=0)


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
Z5
"""    
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z51_m2 = np.zeros(n) 
z52_m2 = np.zeros(n) 
z53_m2 = np.zeros(n) 
z54_m2 = np.zeros(n) 
z55_m2 = np.zeros(n) 
z56_m2 = np.zeros(n) 

z51_P2 = np.zeros(n) 
z52_P2 = np.zeros(n) 
z53_P2 = np.zeros(n) 
z54_P2 = np.zeros(n) 
z55_P2 = np.zeros(n) 
z56_P2 = np.zeros(n) 
for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z51.iloc[:,6][np.argmin(abs(z51.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z51.iloc[:,5][np.argmin(abs(z51.iloc[:,6]-nu2))] 
    z51_m2[i] = M2
    P2 = z51.iloc[:,2][np.argmin(abs(z51.iloc[:,6]-nu2))] 
    z51_P2[i] = P2
    # for z2
    nu1 = z52.iloc[:,6][np.argmin(abs(z52.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z52.iloc[:,5][np.argmin(abs(z52.iloc[:,6]-nu2))] 
    z52_m2[i] = M2
    P2 = z52.iloc[:,2][np.argmin(abs(z52.iloc[:,6]-nu2))] 
    z52_P2[i] = P2
    # for z3
    nu1 = z53.iloc[:,6][np.argmin(abs(z53.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z53.iloc[:,5][np.argmin(abs(z53.iloc[:,6]-nu2))] 
    z53_m2[i] = M2
    P2 = z53.iloc[:,2][np.argmin(abs(z53.iloc[:,6]-nu2))] 
    z53_P2[i] = P2
    # for z4
    nu1 = z54.iloc[:,6][np.argmin(abs(z54.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z54.iloc[:,5][np.argmin(abs(z54.iloc[:,6]-nu2))] 
    z54_m2[i] = M2
    P2 = z54.iloc[:,2][np.argmin(abs(z54.iloc[:,6]-nu2))] 
    z54_P2[i] = P2
    # for z5
    nu1 = z55.iloc[:,6][np.argmin(abs(z55.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z55.iloc[:,5][np.argmin(abs(z55.iloc[:,6]-nu2))] 
    z55_m2[i] = M2
    P2 = z55.iloc[:,2][np.argmin(abs(z55.iloc[:,6]-nu2))] 
    z55_P2[i] = P2
    # for z6
    nu1 = z56.iloc[:,6][np.argmin(abs(z56.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z56.iloc[:,5][np.argmin(abs(z56.iloc[:,6]-nu2))] 
    z56_m2[i] = M2
    P2 = z56.iloc[:,2][np.argmin(abs(z56.iloc[:,6]-nu2))] 
    z56_P2[i] = P2
"""
Z4
"""    
theta = np.zeros(n) # rad
smallest = np.zeros(n) # min
largest = np.zeros(n) # max
diff = np.zeros(n) # diff

z41_m2 = np.zeros(n) 
z42_m2 = np.zeros(n) 
z43_m2 = np.zeros(n) 
z44_m2 = np.zeros(n) 
z45_m2 = np.zeros(n) 
z46_m2 = np.zeros(n)

z41_P2 = np.zeros(n) 
z42_P2 = np.zeros(n) 
z43_P2 = np.zeros(n) 
z44_P2 = np.zeros(n) 
z45_P2 = np.zeros(n) 
z46_P2 = np.zeros(n)  
for i in range(50):
    theta[i] = i*math.pi/180 # rad
    M1 = 1.0 # upstream Mach number
    # for z1
    nu1 = z41.iloc[:,6][np.argmin(abs(z41.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z41.iloc[:,5][np.argmin(abs(z41.iloc[:,6]-nu2))] 
    z41_m2[i] = M2
    P2 = z41.iloc[:,2][np.argmin(abs(z41.iloc[:,6]-nu2))] 
    z41_P2[i] = P2
    # for z2
    nu1 = z42.iloc[:,6][np.argmin(abs(z42.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z42.iloc[:,5][np.argmin(abs(z42.iloc[:,6]-nu2))] 
    z42_m2[i] = M2
    P2 = z42.iloc[:,2][np.argmin(abs(z42.iloc[:,6]-nu2))] 
    z42_P2[i] = P2
    # for z3
    nu1 = z43.iloc[:,6][np.argmin(abs(z43.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z43.iloc[:,5][np.argmin(abs(z43.iloc[:,6]-nu2))] 
    z43_m2[i] = M2
    P2 = z43.iloc[:,2][np.argmin(abs(z43.iloc[:,6]-nu2))] 
    z43_P2[i] = P2
    # for z4
    nu1 = z44.iloc[:,6][np.argmin(abs(z44.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z44.iloc[:,5][np.argmin(abs(z44.iloc[:,6]-nu2))] 
    z44_m2[i] = M2
    P2 = z44.iloc[:,2][np.argmin(abs(z44.iloc[:,6]-nu2))] 
    z44_P2[i] = P2
    # for z5
    nu1 = z45.iloc[:,6][np.argmin(abs(z45.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z45.iloc[:,5][np.argmin(abs(z45.iloc[:,6]-nu2))] 
    z45_m2[i] = M2
    P2 = z45.iloc[:,2][np.argmin(abs(z45.iloc[:,6]-nu2))] 
    z45_P2[i] = P2
    # for z6
    nu1 = z46.iloc[:,6][np.argmin(abs(z46.iloc[:,5]-M1))] 
    nu2 = nu1 + theta[i]
    M2 = z46.iloc[:,5][np.argmin(abs(z46.iloc[:,6]-nu2))] 
    z46_m2[i] = M2
    P2 = z46.iloc[:,2][np.argmin(abs(z46.iloc[:,6]-nu2))] 
    z46_P2[i] = P2
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

axes.plot(theta/math.pi*180  , z51_m2 , color=colors[4], lw=lwh, label="$Z_t=0.5$")
axes.plot(theta/math.pi*180  , z52_m2 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , z53_m2 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , z54_m2 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , z55_m2 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , z56_m2 , color=colors[4], lw=lwh)

axes.plot(theta/math.pi*180  , z41_m2 , color=colors[5], lw=lwh, label="$Z_t=0.4$")
axes.plot(theta/math.pi*180  , z42_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , z43_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , z44_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , z45_m2 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , z46_m2 , color=colors[5], lw=lwh)


axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$M_2$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("mm_z_M2_theta.eps")


###############################################################################
fig3 = plt.figure( dpi=300)
lwh = 2
axes = fig3.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
# see  the corresponding coolprop.py, to see pp[i]]pt or Pc
axes.plot(theta/math.pi*180  , (9.326e5-z91_P2*1.55e6)/9.326e5 , color=colors[0], lw=lwh, label="$Z_t=0.9$")
axes.plot(theta/math.pi*180  , (799090-z92_P2*1301200)/799090 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (645291-z93_P2*1051200)/645291 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (491774-z94_P2*801200)/491774 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (338036-z95_P2*551200)/338036 , color=colors[0], lw=lwh)
axes.plot(theta/math.pi*180  , (193900-z96_P2*301200)/193900. , color=colors[0], lw=lwh)

axes.plot(theta/math.pi*180  , (1582060-z81_P2*1939000)/1582060 , color=colors[1], lw=lwh, label="$Z_t=0.8$")
axes.plot(theta/math.pi*180  , (1331849-z82_P2*1939000)/1331849 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (1080330-z83_P2*1939000)/1080330 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (828923-z84_P2*1939000)/828923 , color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (577307-z85_P2*1939000)/577307, color=colors[1], lw=lwh)
axes.plot(theta/math.pi*180  , (326059-z86_P2*1939000)/326059 , color=colors[1], lw=lwh)

axes.plot(theta/math.pi*180  , (1842050-z71_P2*1939000)/1842050, color=colors[2], lw=lwh, label="$Z_t=0.7$")
axes.plot(theta/math.pi*180  , (1614170-z72_P2*1939000)/1614170 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (1357225-z73_P2*1939000)/1357225 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (1100537-z74_P2*1939000)/1100537 , color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (842130-z75_P2*1939000)/842130, color=colors[2], lw=lwh)
axes.plot(theta/math.pi*180  , (583746-z76_P2*1939000)/583746 , color=colors[2], lw=lwh)

axes.plot(theta/math.pi*180  , (3296937-z61_P2*1939000)/3296937, color=colors[3], lw=lwh, label="$Z_t=0.6$")
axes.plot(theta/math.pi*180  , (2840875-z62_P2*1939000)/2840875 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (2382805-z63_P2*1939000)/2382805 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (1842050-z64_P2*1939000)/1842050 , color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (1459008-z65_P2*1939000)/1459008, color=colors[3], lw=lwh)
axes.plot(theta/math.pi*180  , (991418-z66_P2*1939000)/991418 , color=colors[3], lw=lwh)

axes.plot(theta/math.pi*180  , (3393155-z51_P2*1939000)/3393155, color=colors[4], lw=lwh, label="$Z_t=0.5$")
axes.plot(theta/math.pi*180  , (2985434-z52_P2*1939000)/2985434 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , (2552357-z53_P2*1939000)/2552357 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , (2103684-z54_P2*1939000)/2103684 , color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , (1651383-z55_P2*1939000)/1651383, color=colors[4], lw=lwh)
axes.plot(theta/math.pi*180  , (1192358-z56_P2*1939000)/1192358 , color=colors[4], lw=lwh)

axes.plot(theta/math.pi*180  , (2841787-z41_P2*1939000)/2841787, color=colors[5], lw=lwh, label="$Z_t=0.4$")
axes.plot(theta/math.pi*180  , (2601013-z42_P2*1939000)/2601013 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , (2333376-z43_P2*1939000)/2333376 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , (2048691-z44_P2*1939000)/2048691 , color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , (1737507-z45_P2*1939000)/1737507, color=colors[5], lw=lwh)
axes.plot(theta/math.pi*180  , (1417853-z46_P2*1939000)/1417853 , color=colors[5], lw=lwh)


axes.set_xlabel('$\\theta$ $[^o]$',fontsize=12)
axes.set_ylabel('$\Delta P$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig3.savefig("mm_z_M2_theta_dp.eps")

################################################################################
fig2 = plt.figure( dpi=300)
lwh = 2
axes = fig2.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure

zt = [0.4,0.5,0.6,0.7,0.8,0.9]
maxdiff = [0.4,0.7,1.0,3.0,6.0,9.2] 
maxdiff.reverse()

plt.bar(zt,maxdiff,color ='b', width = 0.02)
axes.set_xlabel('$Z_t$',fontsize=12)
axes.set_ylabel('$(\Delta M_2)_{\max}\%$',fontsize=12) 
# axes.set_title('$Z_t = 0.9$',fontsize=14)
# axes.legend(loc=0 , prop={'size': 10}) # 
fig2.savefig("mm_z_M2_zt.eps")
