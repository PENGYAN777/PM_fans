#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IV.B — is the inlet fundamental derivative a similarity parameter?

Families of operating conditions sharing the same Gamma at the fan inlet
(Gamma_1) are built by solving Tt at fixed Pt, and the post-expansion Mach
number is computed for each of them.  The spread within a family measures how
good Gamma_1 is as a similarity parameter.

Figures
    mm_g1_curves.pdf/png   M2(theta) for the three Gamma_1 families
    mm_g1_zt.pdf/png       M2(50 deg) versus Zt for the same conditions

Outputs
    mm_g1_similarity.csv
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
G1S = (0.60, 0.70, 0.80, 0.90)
PRS = (0.85, 1.00, 1.15, 1.30)
THETA = np.linspace(0.0, 50.0, 101)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.1,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def Gamma1(P0, T0):
    try:
        st = cramer_pm.sonic_state(FLUID, P0, T0)
        return CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                          "T", st["T_s"], "D", st["rho_s"], FLUID)
    except Exception:
        return np.nan


def solve_T(P0, target, Tc):
    Ts = np.linspace(1.005, 2.0, 90) * Tc
    Gs = np.array([Gamma1(P0, t) for t in Ts])
    ok = np.isfinite(Gs)
    for i in range(Ts.size - 1):
        if ok[i] and ok[i + 1] and (Gs[i] - target) * (Gs[i + 1] - target) <= 0:
            return brentq(lambda T: Gamma1(P0, T) - target, Ts[i], Ts[i + 1])
    return None


def main():
    Tc, Pc = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
    # same colour convention as the Zt figures: largest value dark
    palette = plt.cm.viridis(np.linspace(0.12, 0.88, len(G1S)))
    colours = dict(zip(sorted(G1S, reverse=True), palette))

    data, rows = {}, []
    for g1 in G1S:
        data[g1] = []
        for pr in PRS:
            P0 = pr * Pc
            T0 = solve_T(P0, g1, Tc)
            if T0 is None:
                continue
            res = cramer_pm.integrate(FLUID, P0, T0)
            M = np.interp(np.deg2rad(THETA), res["nu"], res["M"])
            Gpath = np.array([CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                                         "T", t, "D", d, FLUID)
                              for t, d in zip(res["T"], res["rho"])])
            zt = CP.PropsSI("Z", "P", P0, "T", T0, FLUID)
            g1c = Gamma1(P0, T0)
            data[g1].append(dict(P=pr, T=T0, zt=zt, g1=g1c, M=M,
                                 Mp=res["M"], Gp=Gpath))
            rows.append(np.column_stack([np.full(THETA.size, g1), np.full(THETA.size, pr),
                                         np.full(THETA.size, zt), THETA, M]))
            print("Gamma1=%.2f P/Pc=%.2f  Zt=%.3f  M2(50)=%.3f" % (g1, pr, zt, M[-1]))

    # --- M2(theta) grouped by Gamma_1 -------------------------------------
    fig1, ax1 = plt.subplots(figsize=(3.39, 2.9))
    for g1 in G1S:
        for i, d in enumerate(data[g1]):
            ax1.plot(THETA, d["M"], "-", color=colours[g1], lw=0.9, alpha=0.9,
                     label=r"$\Gamma_1=%.1f$" % g1 if i == 0 else None)
    ax1.set(xlabel=r"$\theta$ [deg]", ylabel=r"$M_2$", xlim=(0, 50))
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="upper left")
    fig1.tight_layout()
    fig1.savefig(os.path.join(HERE, "mm_g1_curves.pdf"))
    fig1.savefig(os.path.join(HERE, "mm_g1_curves.png"))

    # --- Gamma(M) along the isentropes -----------------------------------
    fig2, ax2 = plt.subplots(figsize=(3.39, 2.9))
    for g1 in G1S:
        for i, d in enumerate(data[g1]):
            ax2.plot(d["Mp"], d["Gp"], "-", color=colours[g1], lw=0.8, alpha=0.85,
                     label=r"$\Gamma_1=%.1f$" % g1 if i == 0 else None)
    ax2.set(xlabel=r"$M$", ylabel=r"$\Gamma$", xlim=(1.0, 2.1))
    ax2.tick_params(direction="in", top=True, right=True)
    ax2.legend(frameon=False, loc="lower right")
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "mm_g1_gamma.pdf"))
    fig2.savefig(os.path.join(HERE, "mm_g1_gamma.png"))

    np.savetxt(os.path.join(HERE, "mm_g1_similarity.csv"), np.vstack(rows),
               delimiter=",", comments="",
               header="Gamma1_target,Pt_over_Pc,zt,theta_deg,M2", fmt="%.5f")

    print()
    for g1 in G1S:
        M = np.array([d["M"] for d in data[g1]])
        sp = 100 * np.max((M.max(0) - M.min(0)) / M.mean(0))
        zs = [d["zt"] for d in data[g1]]
        print("Gamma1=%.1f: Zt in [%.2f, %.2f], max spread of M2 = %.1f%%"
              % (g1, min(zs), max(zs), sp))
    print("wrote mm_g1_curves, mm_g1_gamma and mm_g1_similarity.csv")


if __name__ == "__main__":
    main()
