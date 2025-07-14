#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mach number comparison with reference data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV files
z34 = pd.read_csv("z34.csv", ",")
num = pd.read_csv("paper_num.csv", ",")

# Sort reference data by ν (column 1 of num)
sorted_indices = np.argsort(num.iloc[:, 1])
sorted_x = num.iloc[sorted_indices, 1]  # ν values
sorted_y = num.iloc[sorted_indices, 0]  # Reference Mach numbers

# --- Plot 1: Mach vs ν ---
fig1, ax1 = plt.subplots(figsize=(4, 4), dpi=300)

# 4th order RK curve
ax1.plot(z34.iloc[:, 6], z34.iloc[:, 5], 'k', lw=2, label="4th order RK")

# Reference data points
ax1.plot(sorted_x, sorted_y, 'ko', markersize=4, label="Cramer et al. 1992")

# Axes labels and limits
ax1.set_xlabel('$\\nu$', fontsize=12)
ax1.set_ylabel('Mach', fontsize=12)
ax1.set_xlim([0, 1.1])
ax1.legend(loc='best', prop={'size': 10})
ax1.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
fig1.savefig("vv_num.eps")

# --- Prepare data for parity plot ---
model_vals = []
ref_vals = []

for i in range(len(num)):
    nu_ref = num.iloc[i, 1]            # ν
    mach_ref = num.iloc[i, 0]          # Reference Mach
    idx_closest = np.argmin(abs(z34.iloc[:, 6] - nu_ref))
    mach_model = z34.iloc[idx_closest, 5]
    
    model_vals.append(mach_model)
    ref_vals.append(mach_ref)
# --- Compute average relative difference in % ---
diffs = []
for model, ref in zip(model_vals, ref_vals):
    rel_diff = (model - ref) / ref * 100
    diffs.append(rel_diff)

average_diff = np.mean(diffs)
print(f"Average relative difference: {average_diff:.2f}%")


# --- Plot 2: Parity plot (Model vs Reference Mach) ---
fig2, ax2 = plt.subplots(figsize=(4, 4), dpi=300)

# Scatter plot of model vs reference
ax2.plot(ref_vals, model_vals, 'ko', label='Data points')

# Axis limits
x_min, x_max = 1.0, 1.8
ax2.set_xlim([x_min, x_max])
ax2.set_ylim([x_min, x_max])

# y = x reference line
ax2.plot([x_min, x_max], [x_min, x_max], 'k--', label='$y = x$')

# ±5% error band
x_vals = np.linspace(x_min, x_max, 100)
ax2.fill_between(x_vals, 0.95 * x_vals, 1.05 * x_vals, color='gray', alpha=0.2, label='±5% Error Band')

# Axes labels
ax2.set_xlabel('Reference Mach (Cramer et al.)', fontsize=12)
ax2.set_ylabel('Model Mach (4th order RK)', fontsize=12)
ax2.legend(loc='best', prop={'size': 10})
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_aspect('equal', adjustable='box')

plt.tight_layout()
fig2.savefig("parity_num.eps")
