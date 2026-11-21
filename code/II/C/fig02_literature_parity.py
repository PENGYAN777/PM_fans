#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification against Cramer & Crickenberger (1992) -- toluene.

Two separate figures (easier to place in the manuscript as Fig. 2a / Fig. 2b):

    fig02a  nu(M)   : this work (HEOS) vs the digitised published curve
    fig02b  dM/M(ν) : Mach-number difference at matched nu, with the
                      digitisation uncertainty of the 1992 scan

Everything is written next to this script (fig02a.pdf/png, fig02b.pdf/png,
fig02.csv).
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cramer_pm  # noqa: E402

FLUID = "Toluene"
TC, PC = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
P0, T0 = 2.01 * PC, 1.07 * TC

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 8,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.4,
                     "figure.dpi": 300, "savefig.bbox": "tight"})

# --- this work -------------------------------------------------------------
res = cramer_pm.integrate(FLUID, P0, T0)
M, nu = res["M"], res["nu"]

# --- published curve -------------------------------------------------------
dat = np.loadtxt(os.path.join(ROOT, "data", "cramer1992_toluene.csv"),
                 delimiter=",", comments="#", skiprows=6)
nu_d, M_d, sM = dat[:, 0], dat[:, 1], dat[:, 2]
M_here = np.interp(nu_d, nu, M)
dm = (M_here - M_d) / M_d * 100.0

# tolerance bands used in the text
sigma_pct = 100.0 * np.max(sM) / np.min(M_d)

# --- Fig. 2a: nu(M) --------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.4, 2.9))
ax.plot(M, nu, "-", color="#1f4fd1", label="This work (HEOS)")
ax.errorbar(M_d, nu_d, xerr=sM, fmt="o", ms=4.0, mfc="none", mec="k",
            ecolor="k", elinewidth=0.8, capsize=2.2,
            label="Cramer & Crickenberger (1992)")
ax.set(xlabel=r"$M$", ylabel=r"$\nu$ [rad]", xlim=(1.0, 2.3), ylim=(0, 1.6))
ax.tick_params(direction="in", top=True, right=True)
ax.legend(loc="upper left", frameon=False)
fig.savefig(os.path.join(HERE, "vv_cramer.pdf"))
fig.savefig(os.path.join(HERE, "vv_cramer.png"))
plt.close(fig)

# --- Fig. 2b: relative difference -----------------------------------------
fig, ax = plt.subplots(figsize=(3.4, 2.4))
ax.axhline(0, color="k", lw=0.6, ls=":")
ax.plot(nu_d, dm, "o-", ms=4.0, color="#1f4fd1")
ax.set(xlabel=r"$\nu$ [rad]",
       ylabel=r"$(M_{\mathrm{here}}-M_{1992})/M_{1992}$ [%]",
       xlim=(0.35, 1.05), ylim=(-3, 3))
ax.tick_params(direction="in", top=True, right=True)
fig.savefig(os.path.join(HERE, "error.pdf"))
fig.savefig(os.path.join(HERE, "error.png"))
plt.close(fig)

np.savetxt(os.path.join(HERE, "fig02.csv"),
           np.column_stack([nu_d, M_d, sM, M_here, dm]), delimiter=",",
           header="nu_rad,M_1992,M_sigma,M_here,dM_percent", comments="")

print("nu   | M_1992 | M_here | dM [%]")
for a, b, c, d in zip(nu_d, M_d, M_here, dm):
    print(f"{a:4.2f} | {b:6.3f} | {c:6.3f} | {d:+5.2f}")
print("max |dM| = %.2f %%   (digitisation uncertainty +-%.2f %%, not shown in the figure)"
      % (np.max(np.abs(dm)), sigma_pct))
