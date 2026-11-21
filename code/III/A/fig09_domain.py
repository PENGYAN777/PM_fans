#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domain of admissibility of the Prandtl-Meyer fan in the (Zt, theta) plane.

For each value of the total compressibility factor the total temperature is
found that gives that Zt at a fixed reduced pressure (Pt/Pc = 1.2), the fan is
integrated from the sonic point, and the largest deflection is recorded at which

  (i)  the flow is still single phase  (T > Tsat(P), checked for P < Pc),
  (ii) the flow is still classical     (Gamma > 0),

whichever occurs first.  If the isentrope becomes two-phase before the sonic
point, no fan exists and the admissible deflection is zero.

Outputs
    mm_domain.pdf/png    admissible (Zt, theta) region and the range used in the paper
    mm_domain.csv        Zt, Tt, theta_max and the limiting mechanism
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
P_RED = 1.2                      # Pt/Pc of the sweep
Z_GRID = np.round(np.arange(0.28, 0.95, 0.04), 3)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 7.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.2,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def theta_max_for(zt, Pc, Tc):
    """Largest admissible deflection for a given Zt, or (0, reason)."""
    P0 = P_RED * Pc
    try:
        T0 = brentq(lambda T: CP.PropsSI("Z", "P", P0, "T", T, FLUID) - zt,
                    Tc * 1.002, Tc * 2.5, xtol=1e-6)
    except ValueError:
        return 0.0, "no single-phase total state", np.nan

    try:
        res = cramer_pm.integrate(FLUID, P0, T0, Mmax=6.0, V_end_factor=600.0)
    except Exception:
        return 0.0, "two-phase at the sonic point", T0

    T, P, nu = res["T"], res["P"], np.rad2deg(res["nu"])
    for i, (t, p) in enumerate(zip(T, P)):
        if p < Pc and t <= CP.PropsSI("T", "P", p, "Q", 0, FLUID):
            return float(nu[i]), "saturation crossing", T0
        g = CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                       "T", t, "D", res["rho"][i], FLUID)
        if g <= 0.0:
            return float(nu[i]), "Gamma <= 0", T0
    return float(nu[-1]), "vacuum limit (P -> 0)", T0


def main():
    Pc, Tc = CP.PropsSI("Pcrit", FLUID), CP.PropsSI("Tcrit", FLUID)
    rows = []
    for zt in Z_GRID:
        th, why, T0 = theta_max_for(zt, Pc, Tc)
        rows.append((zt, T0, th, why))
        print("Zt=%.2f  Tt=%s K  theta_max=%6.1f deg  (%s)"
              % (zt, "%.2f" % T0 if np.isfinite(T0) else "--", th, why))

    rows = np.array(rows, dtype=object)
    zt = np.array([r[0] for r in rows], float)
    th = np.array([r[2] for r in rows], float)

    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    ax.fill_between(zt, 0, th, color="0.85", lw=0,
                    label="admissible fan")
    ax.plot(zt, th, "o-", ms=2.6, color="#1f4fd1", lw=1.1)
    ax.add_patch(plt.Rectangle((0.4, 0), 0.5, 50, fill=False, ls="--",
                               ec="#c0392b", lw=1.0))
    ax.text(0.63, 54, "range used\nin this paper", color="#c0392b",
            fontsize=7, ha="center", va="bottom")
    ax.annotate("two-phase at the sonic point", xy=(0.28, 5), xytext=(0.36, 30),
                fontsize=6.5, arrowprops=dict(arrowstyle="-", lw=0.6, color="0.3"))
    ax.set(xlabel=r"$Z_t$", ylabel=r"$\theta_{\max}$ [deg]", xlim=(0.26, 0.95),
           ylim=(0, 175))
    ax.tick_params(direction="in", top=True, right=True)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "mm_domain.pdf"))
    fig.savefig(os.path.join(HERE, "mm_domain.png"))

    with open(os.path.join(HERE, "mm_domain.csv"), "w") as f:
        f.write("# Pt/Pc = %.1f; theta_max from the single-phase and Gamma > 0 criteria\n" % P_RED)
        f.write("zt,Tt_K,theta_max_deg,limiting_mechanism\n")
        for z, t0, t, w in rows:
            f.write("%.2f,%s,%.2f,%s\n" % (z, "%.2f" % t0 if np.isfinite(t0) else "", t, w))
    print("wrote mm_domain.pdf/png/csv")


if __name__ == "__main__":
    main()
