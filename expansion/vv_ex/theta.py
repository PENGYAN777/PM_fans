#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:04:05 2023

Compute downstream Mach number for nonideal flow

@author: yan
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# --- Load Data ---
z6 = pd.read_csv("z6.csv", ",", skiprows=0)

# --- Inputs ---
n = 50
theta = np.zeros(n)
z6_m2 = np.zeros(n)
z6_P2 = np.zeros(n)
z6_T2 = np.zeros(n)
z6_D2 = np.zeros(n)

# Experimental data
theta_e = [0, 10, 20, 30]                # degrees
m_e = [1.20743, 1.40517, 1.58064, 1.73713]
um = [0.006, 0.009, 0.011, 0.009]        # uncertainty
m0 = 1.20743                             # upstream Mach

# --- Theoretical Computation ---
for i in range(n):
    theta[i] = i * math.pi / 180  # radians
    M1 = m0
    nu1 = z6.iloc[:, 6][np.argmin(abs(z6.iloc[:, 5] - M1))]
    nu2 = nu1 + theta[i]
    idx = np.argmin(abs(z6.iloc[:, 6] - nu2))
    
    z6_m2[i] = z6.iloc[idx, 5]
    z6_P2[i] = z6.iloc[idx, 2]
    z6_D2[i] = z6.iloc[idx, 3]
    z6_T2[i] = z6.iloc[idx, 4]

# Extract theory values at experimental angles for parity plot
m2_theory = []
for angle in theta_e:
    idx = int(angle)  # theta sampled every 1 degree
    m2_theory.append(z6_m2[idx])
m2_theory = np.array(m2_theory)
m2_exp = np.array(m_e)

# Compute ±5% error bounds for parity plot
lower_bound = m2_exp * 0.95
upper_bound = m2_exp * 1.05

# Common figure size and dpi for both plots
figsize = (6, 5)  # width, height in inches
dpi = 300
lwh = 2

# --- Figure 1: M2 vs θ ---
fig1, axes1 = plt.subplots(figsize=(4, 4), dpi=300)
# axes1 = fig1.add_axes([0.15, 0.15, 0.7, 0.7])
axes1.plot(theta / math.pi * 180, z6_m2, 'k', lw=lwh, label="Computed solutions")
axes1.errorbar(theta_e, m_e, yerr=um, fmt='ko', capsize=5, label="Experiment data")

axes1.set_xlabel('$\\theta$ $[^o]$', fontsize=12)
axes1.set_ylabel('$M_2$', fontsize=12)
axes1.set_xlim([0, 30])
axes1.set_ylim([1.2, 1.8])
axes1.legend(loc=0, prop={'size': 10})
# axes1.set_title('$M_2$ vs $\\theta$', fontsize=14)
fig1.savefig("vv_mm_M2_theta.eps")

# --- Figure 2: Parity Plot ---
fig2, axes2 = plt.subplots(figsize=(4, 4), dpi=300)
# axes2 = fig2.add_axes([0.15, 0.15, 0.7, 0.7])
axes2.plot(m2_exp, m2_theory, 'ko', label='Data Points')
axes2.errorbar(m2_exp, m2_theory, yerr=um, fmt='none', ecolor='black', capsize=5)
axes2.plot(m2_exp, m2_exp, 'k--', label='y = x')
axes2.fill_between(m2_exp, lower_bound, upper_bound, color='gray', alpha=0.1, label='±5% Error Band')

axes2.set_xlabel('Experimental $M_2$', fontsize=12)
axes2.set_ylabel('Computed $M_2$', fontsize=12)
axes2.set_xlim([1.2, 1.8])
axes2.set_ylim([1.2, 1.8])
axes2.set_aspect('equal', adjustable='box')
axes2.legend(loc=0, prop={'size': 10})
# axes2.set_title('Parity Plot', fontsize=14)
fig2.savefig("vv_mm_M2_parity.eps")

plt.show()

# --- Compute average relative difference ---
rel_diffs = (m2_theory - m2_exp) / m2_exp * 100
avg_diff = np.mean(rel_diffs)
print("Relative differences (%):", rel_diffs)
print(f"Average relative difference: {avg_diff:.2f}%")
