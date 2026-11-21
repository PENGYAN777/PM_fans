#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thermodynamic map of the Prandtl-Meyer fan in the (T, P) plane.

For the six operating conditions of Table I the isentrope is drawn from the
total state down to the post-expansion state at theta = 50 deg, together with
the vapour-liquid saturation curve of MM.  The figure shows that every fan
remains in the single-phase region, and how close to the critical point the
least non-ideal condition (Zt = 0.4) runs.

Outputs
    mm_pt_map.pdf/png    (T, P) diagram with the six isentropes
    mm_pt_map.csv        T, P along each isentrope and the marked states
"""
import os
import sys

import numpy as np
import CoolProp.CoolProp as CP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "II", "C"))
import cramer_pm  # noqa: E402

FLUID = "MM"
THETA_MAX = 50.0

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.2,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def main():
    cond = np.loadtxt(os.path.join(ROOT, "data", "mm_table1.csv"),
                      delimiter=",", comments="#")
    zts, Pt, Tt = cond[:, 0], cond[:, 1], cond[:, 2]
    colors = plt.cm.viridis(np.linspace(0.12, 0.88, zts.size))

    Tc, Pc = CP.PropsSI("Tcrit", FLUID), CP.PropsSI("Pcrit", FLUID)
    Ttrip = CP.PropsSI("Ttriple", FLUID)

    fig, ax = plt.subplots(figsize=(3.39, 3.2))

    # saturation curve
    Ts = np.linspace(Ttrip + 0.5, Tc, 300)
    Ps = np.array([CP.PropsSI("P", "T", t, "Q", 0, FLUID) for t in Ts])
    ax.plot(Ts / Tc, Ps / Pc, "-", color="0.35", lw=1.1, label="saturation")
    ax.plot([1.0], [1.0], "k*", ms=6, label="critical point")

    rows, gmin = [], []
    for zt, p0, t0, c in zip(zts, Pt, Tt, colors):
        s0 = CP.PropsSI("S", "P", p0, "T", t0, FLUID)
        res = cramer_pm.integrate(FLUID, p0, t0)
        nu, M, T = res["nu"], res["M"], res["T"]
        P = res["P"]

        # fan path from the sonic point to theta = 50 deg
        i50 = int(np.argmin(np.abs(np.rad2deg(nu) - THETA_MAX)))
        Tf, Pf = T[: i50 + 1], P[: i50 + 1]

        # inlet segment, from the total state to the sonic point
        Pg_in = np.geomspace(p0, Pf[0], 40)
        Tg_in = np.array([CP.PropsSI("T", "P", p, "S", s0, FLUID) for p in Pg_in])

        ax.plot(Tg_in / Tc, Pg_in / Pc, ":", color=c, lw=0.9)
        ax.plot(Tf / Tc, Pf / Pc, "-", color=c, lw=1.2, label=r"$Z_t=%.1f$" % zt)
        ax.plot(t0 / Tc, p0 / Pc, "s", ms=3.2, mfc="none", mec=c, mew=0.8)
        ax.plot(Tf[0] / Tc, Pf[0] / Pc, "o", ms=3.0, color=c)
        ax.plot(Tf[-1] / Tc, Pf[-1] / Pc, "^", ms=3.6, mfc="none", mec=c, mew=0.8)

        rows.append(np.column_stack([np.full(Tf.size, zt), Tf, Pf]))

        Gt = CP.PropsSI("fundamental_derivative_of_gas_dynamics", "P", p0, "T", t0, FLUID)
        Gf = np.array([CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                                  "T", t, "D", d, FLUID)
                       for t, d in zip(Tf, res["rho"][: i50 + 1])])
        gmin.append((zt, Gt, Gf.min()))

    ax.set_yscale("log")
    ax.set(xlabel=r"$T/T_c$", ylabel=r"$P/P_c$", xlim=(0.85, 1.35), ylim=(0.05, 3.0))
    ax.tick_params(direction="in", top=True, right=True, which="both")
    ax.legend(frameon=False, loc="upper right", ncol=2, fontsize=6.2,
              handlelength=1.0, columnspacing=0.8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "mm_pt_map.pdf"))
    fig.savefig(os.path.join(HERE, "mm_pt_map.png"))

    np.savetxt(os.path.join(HERE, "mm_pt_map.csv"), np.vstack(rows), delimiter=",",
               comments="", header="zt,T_K,P_Pa", fmt="%.3f")
    with open(os.path.join(HERE, "mm_gamma_check.csv"), "w") as f:
        f.write("# Gamma at the total state and minimum along the fan (0-50 deg)\n")
        f.write("zt,Gamma_t,Gamma_min_fan\n")
        for z, gt, gm in gmin:
            f.write("%.2f,%.3f,%.3f\n" % (z, gt, gm))
            print("Zt=%.1f  Gamma_t=%.3f  Gamma_min(fan)=%.3f" % (z, gt, gm))
    print("wrote mm_pt_map.pdf/png/csv and mm_gamma_check.csv")


if __name__ == "__main__":
    main()
