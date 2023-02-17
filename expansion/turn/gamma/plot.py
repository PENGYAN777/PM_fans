#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:47:12 2023

@author: user
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
1. compute M*
"""
n = 100
gamma = np.linspace(0.1,0.99,n) # `Gamma
M= np.zeros(n) # Mach numer

M = 1/(1-gamma)


"""
3. plot
"""

fig1 = plt.figure( dpi=300)
lwh = 2
axes = fig1.add_axes([0.15, 0.15, 0.7, 0.7]) #size of figure
axes.plot(gamma , M , 'k', lw=lwh, label="$M^*$")

axes.set_xlabel('$\\Gamma_1$',fontsize=12)
axes.set_ylabel('$M^*$',fontsize=12) 
axes.set_title('$M^*$ vs $\\Gamma_1$',fontsize=14)
axes.legend(loc=0 , prop={'size': 10}) # 
fig1.savefig("ex_turn_gamma.pdf")