#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IV.A — why Zt works: the shape of the Gamma(M) path.

For the six conditions that share a given Zt the isentrope and the evolution of
Gamma along it are compared.  Conditions sharing Zt are shown to have almost
identical Gamma(M), and the spread of Gamma along the path is shown to scale
with the spread of the post-expansion Mach number across Zt.

Figures
    mm_zt_gamma.pdf/png   Gamma(M) for the six conditions of Zt = 0.4 and 0.6
    mm_zt_corr.pdf/png    spread of M2 versus spread of the path average of Gamma

Outputs
    mm_zt_path.csv
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
ZTS = (0.40, 0.50, 0.60, 0.70, 0.80, 0.90)
PRS = (1.0, 1.1, 1.2, 1.3, 1.4, 1.5)
GRID = np.linspace(1.0, 2.1, 60)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.1,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def path(zt, pr, Tc, Pc):
    P0 = pr * Pc
    T0 = brentq(lambda T: CP.PropsSI("Z", "P", P0, "T", T, FLUID) - zt,
                1.002 * Tc, 2.5 * Tc, xtol=1e-6)
    res = cramer_pm.integrate(FLUID, P0, T0, Mmax=2.4)
    M, nu = res["M"], res["nu"]
    G = np.array([CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                             "T", t, "D", d, FLUID)
                  for t, d in zip(res["T"], res["rho"])])
    M2 = float(np.interp(np.deg2rad(50.0), nu, M))
    m = M <= M2
    w = np.sqrt(M ** 2 - 1.0) / (M * (1.0 + (G - 1.0) * M ** 2))
    gbar = float(np.trapezoid(G[m] * w[m], M[m]) / np.trapezoid(w[m], M[m]))
    return dict(G=np.interp(GRID, M, G), gbar=gbar, M2=M2)


def main():
    Tc, Pc = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
    palette = plt.cm.viridis(np.linspace(0.12, 0.88, len(ZTS)))
    colour = dict(zip(sorted(ZTS, reverse=True), palette))

    data, rows = {}, []
    for zt in ZTS:
        data[zt] = [path(zt, pr, Tc, Pc) for pr in PRS]

    # --- Gamma(M) for two groups -----------------------------------------
    fig1, ax1 = plt.subplots(figsize=(3.49, 3.2))
    for zt in ZTS:
        c = colour[zt]
        G = np.array([r["G"] for r in data[zt]])
        for g in G:
            ax1.plot(GRID, g, "-", color=c, lw=0.55, alpha=0.55)
        ax1.plot(GRID, G.mean(0), "-", color=c, lw=1.5,
                 label=r"$Z_t=%.1f$" % zt)
    ax1.set(xlabel=r"$M$", ylabel=r"$\Gamma$", xlim=(1.0, 2.1))
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="lower right", ncol=2, fontsize=6.0)

    # inset: spread of the path average Gamma for each group
    axi = fig1.add_axes([0.55, 0.34, 0.31, 0.24])
    dg = [np.ptp([r["gbar"] for r in data[zt]]) for zt in ZTS]
    axi.semilogy(ZTS, dg, "o-", ms=2.6, color="0.25")
    axi.set_ylabel(r"$\Delta\bar\Gamma$", fontsize=6.5, labelpad=0.5)
    axi.tick_params(labelsize=5.5, direction="in", top=True, right=True)
    axi.set_xticks([0.4, 0.7, 0.9])
    axi.set_ylim(2e-4, 2e-1)
    axi.set_title(r"spread within $Z_t$", fontsize=6.0, pad=2)
    fig1.tight_layout()
    fig1.savefig(os.path.join(HERE, "mm_zt_gamma.pdf"))
    fig1.savefig(os.path.join(HERE, "mm_zt_gamma.png"))

    # --- spread of M2 versus spread of Gamma-bar --------------------------
    sM, sG = [], []
    for zt in ZTS:
        M2 = np.array([r["M2"] for r in data[zt]])
        gb = np.array([r["gbar"] for r in data[zt]])
        sM.append(100 * (M2.max() - M2.min()) / M2.mean())
        sG.append(gb.max() - gb.min())
        for r in data[zt]:
            rows.append((zt, r["gbar"], r["M2"]))
    sM, sG = np.array(sM), np.array(sG)
    for zt, a, b in zip(ZTS, sG, sM):
        print("Zt=%.1f  dGbar=%.4f  dM2=%.2f%%" % (zt, a, b))

    np.savetxt(os.path.join(HERE, "mm_zt_path.csv"), np.array(rows), delimiter=",",
               comments="", header="zt,Gamma_bar,M2_50deg", fmt="%.5f")
    for zt, a, b in zip(ZTS, sG, sM):
        print("Zt=%.1f  dGbar=%.4f  dM2=%.2f%%" % (zt, a, b))
    print("wrote mm_zt_gamma and mm_zt_path.csv")


if __name__ == "__main__":
    main()
