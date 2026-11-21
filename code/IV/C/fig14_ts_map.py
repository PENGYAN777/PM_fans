#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IV.C — the (T, s) map behind the similarity criterion.

Two panels, both in the (T, s) plane of MM: the bands of the fundamental
derivative Gamma are shown in colour, the isolines of Z as black dashed lines,
together with the saturation curve, the critical point and the isentropic
expansion paths of the Zt = 0.50 and Zt = 0.90 conditions.

(a) the near-critical region, where the Zt = 0.50 conditions expand;
(b) the high-temperature region, where the Zt = 0.90 conditions expand.

The contrast between the two panels is the criterion: in (b) the Z isoline runs
parallel to the Gamma bands, in (a) it crosses them.

Outputs
    mm_ts_map.pdf/png
"""
import os
import sys

import numpy as np
import CoolProp.CoolProp as CP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "II", "C"))
import cramer_pm  # noqa: E402

FLUID = "MM"
PRS = (1.0, 1.1, 1.2, 1.3, 1.4, 1.5)
ZOOM = {0.50: ((760.0, 1160.0), (470.0, 620.0)),
        0.90: ((1520.0, 1830.0), (630.0, 780.0))}
TINT = {0.50: "#e07020", 0.90: "#1f4fd1"}

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.2,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.0,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def main():
    Tc, Pc = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
    Ttrip = CP.PropsSI("Ttriple", FLUID)

    # --- global field ------------------------------------------------------
    n = 120
    T = np.linspace(450.0, 830.0, n)
    s = np.linspace(700.0, 1850.0, n)
    SS, TT = np.meshgrid(s, T)
    Z = np.full(TT.shape, np.nan)
    G = np.full(TT.shape, np.nan)
    for i in range(n):
        for j in range(n):
            try:
                Z[i, j] = CP.PropsSI("Z", "Smass", SS[i, j], "T|gas", TT[i, j], FLUID)
                G[i, j] = CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                                     "Smass", SS[i, j], "T", TT[i, j], FLUID)
            except Exception:
                pass

    Tsat = np.linspace(Ttrip + 1.0, Tc, 400)
    Ssat = np.array([CP.PropsSI("S", "T", t, "Q", 1, FLUID) for t in Tsat])

    # --- expansion paths ---------------------------------------------------
    paths = {0.50: [], 0.90: []}
    for zt in paths:
        for pr in PRS:
            P0 = pr * Pc
            T0 = brentq(lambda T0: CP.PropsSI("Z", "P", P0, "T", T0, FLUID) - zt,
                        1.002 * Tc, 2.5 * Tc, xtol=1e-6)
            s0 = CP.PropsSI("S", "P", P0, "T", T0, FLUID)
            res = cramer_pm.integrate(FLUID, P0, T0)
            T2 = float(np.interp(np.deg2rad(50.0), res["nu"], res["T"]))
            paths[zt].append((s0, T0, T2))

    # --- two panels --------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75))
    levels = np.arange(0.6, 1.25, 0.05)
    for ax, zt in zip(axes, (0.50, 0.90)):
        cf = ax.contourf(SS, TT, G, levels, cmap="viridis", extend="both")
        cz = ax.contour(SS, TT, Z, [zt], colors="k",
                        linestyles="--", linewidths=1.1)
        ax.clabel(cz, fmt=r"$Z=%.1f$", fontsize=6.5, inline=True, colors="k")
        ax.contour(SS, TT, G, [1.0], colors="k", linewidths=1.0)
        ax.plot(Ssat, Tsat, "k-", lw=1.4)
        ax.plot([CP.PropsSI("S", "T", Tc, "P", Pc, FLUID)], [Tc], "k*", ms=5)
        for s0, Ta, Tb in paths[zt]:
            ax.plot([s0, s0], [Tb, Ta], "-", color=TINT[zt], lw=1.4)
            ax.plot([s0], [Ta], "o", ms=3.0, mfc="white", mec=TINT[zt], mew=0.9)
            ax.plot([s0], [Tb], "v", ms=2.8, mfc="white", mec=TINT[zt], mew=0.9)
        (sx, sy) = ZOOM[zt]
        ax.set(xlim=sx, ylim=sy, xlabel=r"$s$ [J kg$^{-1}$ K$^{-1}$]",
               title=r"(%s) $Z_t=%.2f$ conditions" % ("ab"[zt == 0.90], zt))
        ax.tick_params(direction="in", top=True, right=True)
    axes[0].set_ylabel(r"$T$ [K]")

    cb = fig.colorbar(cf, ax=axes, pad=0.015, aspect=28)
    cb.set_label(r"$\Gamma$")
    cb.ax.tick_params(labelsize=7.5)
    fig.savefig(os.path.join(HERE, "mm_ts_map.pdf"))
    fig.savefig(os.path.join(HERE, "mm_ts_map.png"))
    print("wrote mm_ts_map.pdf/png")


if __name__ == "__main__":
    main()
