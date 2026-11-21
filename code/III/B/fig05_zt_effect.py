#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Effect of the total compressibility factor on the Prandtl-Meyer fan.

For the six operating conditions of Table I (siloxane MM, Zt = 0.4 ... 0.9) the
Prandtl-Meyer fan is computed from the sonic point with the same solver used in
Sec. II, and three figures are produced:

    mm_m2_theta.pdf/png    post-expansion Mach number vs deflection angle
    mm_dp_theta.pdf/png    pressure drop across the fan, dP = (P1 - P2)/P1
    mm_mach_nu.pdf/png     Prandtl-Meyer function vs Mach number

The same numbers are also written to mm_zt_effect.csv.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "II", "C"))
import cramer_pm  # noqa: E402

FLUID = "MM"
THETA_MAX = 50.0                      # deg, maximum deflection considered

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.8,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.2,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def style(ax):
    ax.tick_params(direction="in", top=True, right=True, which="both")
    ax.set_xlim(0, THETA_MAX)


def main():
    cond = np.loadtxt(os.path.join(ROOT, "data", "mm_table1.csv"),
                      delimiter=",", comments="#")
    zts, Pt, Tt = cond[:, 0], cond[:, 1], cond[:, 2]

    colors = plt.cm.viridis(np.linspace(0.12, 0.88, zts.size))
    th = np.linspace(0.0, THETA_MAX, 251)
    th_rad = np.deg2rad(th)

    fig1, ax1 = plt.subplots(figsize=(3.4, 2.9))   # M2 vs theta
    fig2, ax2 = plt.subplots(figsize=(3.4, 2.9))   # dP vs theta
    fig3, ax3 = plt.subplots(figsize=(3.4, 2.9))   # nu vs M

    rows = []
    for zt, p0, t0, c in zip(zts, Pt, Tt, colors):
        res = cramer_pm.integrate(FLUID, p0, t0)
        nu, M, P = res["nu"], res["M"], res["P"]

        M2 = np.interp(th_rad, nu, M)              # nu(0) = 0 at the sonic point
        P2 = np.interp(th_rad, nu, P)
        dP = 1.0 - P2 / P2[0]                      # (P1 - P2)/P1, P1 = P(M1 = 1)

        lab = r"$Z_t=%.1f$" % zt
        ax1.plot(th, M2, "-", color=c, label=lab)
        ax2.plot(th, dP, "-", color=c, label=lab)
        ax3.plot(M, nu, "-", color=c, label=lab)

        rows.append(np.column_stack([np.full(th.size, zt), th, M2, dP]))
        print("Zt=%.1f  M2(50 deg)=%.4f  dP(50 deg)=%.4f" % (zt, M2[-1], dP[-1]))

    ax1.set(xlabel=r"$\theta$ [deg]", ylabel=r"$M_2$")
    ax2.set(xlabel=r"$\theta$ [deg]", ylabel=r"$\Delta P$")
    ax3.set(xlabel=r"$M$", ylabel=r"$\nu$ [rad]", xlim=(1.0, 2.4))
    for ax in (ax1, ax2):
        style(ax)
    ax3.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="upper left")
    ax2.legend(frameon=False, loc="upper left")
    ax3.legend(frameon=False, loc="upper left")

    for fig, name in ((fig1, "mm_m2_theta"), (fig2, "mm_dp_theta"), (fig3, "mm_mach_nu")):
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, name + ".pdf"))
        fig.savefig(os.path.join(HERE, name + ".png"))

    np.savetxt(os.path.join(HERE, "mm_zt_effect.csv"), np.vstack(rows), delimiter=",",
               comments="", header="zt,theta_deg,M2,dP_over_P1", fmt="%.4f")
    print("wrote mm_m2_theta, mm_dp_theta, mm_mach_nu and mm_zt_effect.csv")


if __name__ == "__main__":
    main()
