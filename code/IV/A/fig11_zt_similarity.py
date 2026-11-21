#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IV.A — the total compressibility factor as a similarity parameter.

For each of the six values of Zt considered in the paper, six operating
conditions are built at P/Pc = 1.0, 1.1, ... 1.5 (Tt solved for the required
Zt), and the Prandtl-Meyer fan is computed for each of them.

The spread of the post-expansion Mach number among conditions sharing the same
Zt is the measure of how good Zt is as a similarity parameter.

Figures
    mm_zt_pt.pdf/png      operating conditions in the (T/Tc, P/Pc) plane
    mm_zt_band.pdf/png    M2(theta): mean curve and min-max band for each Zt
    mm_zt_spread.pdf/png  maximum spread of M2 and dP versus Zt

Outputs
    mm_zt_similarity.csv
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
THETA = np.linspace(0.0, 50.0, 101)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.1,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def run_case(zt, pr, Tc, Pc):
    P0 = pr * Pc
    T0 = brentq(lambda T: CP.PropsSI("Z", "P", P0, "T", T, FLUID) - zt,
                1.002 * Tc, 2.5 * Tc, xtol=1e-6)
    res = cramer_pm.integrate(FLUID, P0, T0)
    nu, M, P = res["nu"], res["M"], res["P"]
    M2 = np.interp(np.deg2rad(THETA), nu, M)
    P2 = np.interp(np.deg2rad(THETA), nu, P)
    dP = 1.0 - P2 / P2[0]
    return dict(T0=T0, M=M2, dP=dP,
                g_t=CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                               "P", P0, "T", T0, FLUID))


def main():
    Tc, Pc = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
    # same colour convention as Sec. III: Zt = 0.9 dark, Zt = 0.4 light
    palette = plt.cm.viridis(np.linspace(0.12, 0.88, len(ZTS)))
    colour = dict(zip(sorted(ZTS, reverse=True), palette))

    data, rows = {}, []
    for zt in ZTS:
        c = colour[zt]
        data[zt] = []
        for pr in PRS:
            r = run_case(zt, pr, Tc, Pc)
            data[zt].append(r)
            rows.append(np.column_stack([np.full(THETA.size, zt), np.full(THETA.size, pr),
                                         THETA, r["M"], r["dP"]]))
            print("Zt=%.2f P/Pc=%.2f Tt=%.1f K Gt=%.2f M2(50)=%.3f"
                  % (zt, pr, r["T0"], r["g_t"], r["M"][-1]))

    # --- (T, P) map of the operating conditions ---------------------------
    fig1, ax1 = plt.subplots(figsize=(3.39, 2.9))
    for zt in ZTS:
        c, pts = colour[zt], data[zt]
        ax1.plot([p["T0"] / Tc for p in pts], list(PRS), "o-", ms=3.2, lw=0.7,
                 mfc="none", color=c, label=r"$Z_t=%.1f$" % zt)
    ax1.set(xlabel=r"$T_t/T_c$", ylabel=r"$P_t/P_c$", ylim=(0.95, 1.55))
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="lower right", ncol=2)
    fig1.tight_layout()
    fig1.savefig(os.path.join(HERE, "mm_zt_pt.pdf"))
    fig1.savefig(os.path.join(HERE, "mm_zt_pt.png"))

    # --- M2 and dP: mean and band ----------------------------------------
    fig2, (axM, axP) = plt.subplots(2, 1, figsize=(3.39, 4.5), sharex=True)
    spread = []
    for zt in ZTS:
        c = colour[zt]
        M = np.array([r["M"] for r in data[zt]])
        P = np.array([r["dP"] for r in data[zt]])
        axM.fill_between(THETA, M.min(0), M.max(0), color=c, alpha=0.35, lw=0)
        axM.plot(THETA, M.mean(0), "-", color=c, label=r"$Z_t=%.1f$" % zt)
        axP.fill_between(THETA, P.min(0), P.max(0), color=c, alpha=0.35, lw=0)
        axP.plot(THETA, P.mean(0), "-", color=c)
        spread.append(100 * np.max((M.max(0) - M.min(0)) / M.mean(0)))
    axM.set(ylabel=r"$M_2$", xlim=(0, 50))
    axP.set(xlabel=r"$\theta$ [deg]", ylabel=r"$\Delta P$", xlim=(0, 50))
    for a in (axM, axP):
        a.tick_params(direction="in", top=True, right=True)
    axM.legend(frameon=False, loc="upper left")
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "mm_zt_band.pdf"))
    fig2.savefig(os.path.join(HERE, "mm_zt_band.png"))

    # --- spread versus Zt -------------------------------------------------
    spread_p = []
    for zt in ZTS:
        dP = np.array([r["dP"] for r in data[zt]])
        mean = dP.mean(0)
        ok = mean > 1e-3                       # skip theta = 0, where dP = 0
        spread_p.append(100 * np.max((dP.max(0) - dP.min(0))[ok] / mean[ok]))
    fig3, ax3 = plt.subplots(figsize=(3.39, 2.7))
    ax3.semilogy(ZTS, spread, "o-", ms=4, color="#1f4fd1", label=r"$M_2$")
    ax3.semilogy(ZTS, spread_p, "s-", ms=3.6, color="#c0392b", label=r"$\Delta P$")
    ax3.axhline(1.0, color="0.5", ls=":", lw=0.8)
    ax3.axhline(3.0, color="0.75", ls=":", lw=0.8)
    ax3.text(0.42, 1.15, r"$1\%$", fontsize=6.5, color="0.45")
    ax3.text(0.42, 3.5, r"$3\%$", fontsize=6.5, color="0.55")
    ax3.set(xlabel=r"$Z_t$", ylabel="max spread [%]", xlim=(0.36, 0.94))
    ax3.tick_params(direction="in", top=True, right=True)
    ax3.legend(frameon=False, loc="upper right")
    fig3.tight_layout()
    fig3.savefig(os.path.join(HERE, "mm_zt_spread.pdf"))
    fig3.savefig(os.path.join(HERE, "mm_zt_spread.png"))

    np.savetxt(os.path.join(HERE, "mm_zt_similarity.csv"), np.vstack(rows),
               delimiter=",", comments="",
               header="zt,Pt_over_Pc,theta_deg,M2,dP_over_P1", fmt="%.5f")
    print("spread M2 [%%]:", " ".join("%.2f" % s for s in spread))
    print("spread dP [%%]:", " ".join("%.2f" % s for s in spread_p))
    print("wrote mm_zt_pt, mm_zt_band, mm_zt_spread and mm_zt_similarity.csv")


if __name__ == "__main__":
    main()
