#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechanism: the fundamental derivative along the isentrope.

For the six conditions of Table I the isentrope is walked from the total state
with the HEOS and, for a set of deflection angles, the post-expansion Mach
number, the dnu-weighted average of Gamma and the value of Gamma at the total
state are recorded.

Figures
    mm_gamma_M.pdf/png    Gamma(M) along the isentrope, six Zt
    mm_gamma_fit.pdf/png  (a) M2 vs path average Gamma, (b) M2 vs Gamma_t, both
                          for three deflection angles, (c) R2 of the two
                          correlations as a function of the deflection angle

Outputs
    mm_gamma_M.pdf/png, mm_gamma_fit.pdf/png, mm_gamma_path.csv
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

FLUID = "MM"
M_MAX = 2.6
THETAS = (10.0, 30.0, 50.0)          # panels (a) and (b)
THETA_SWEEP = np.arange(5.0, 51.0, 5.0)   # panel (c)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.2,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def walk(Pt, Tt):
    """M, Gamma and nu along the isentrope, plus Gamma at the total state."""
    s0 = CP.PropsSI("S", "P", Pt, "T", Tt, FLUID)
    h0 = CP.PropsSI("H", "P", Pt, "T", Tt, FLUID)
    Pc = CP.PropsSI("Pcrit", FLUID)

    P = np.geomspace(Pt, 0.02 * Pt, 600)
    T = np.array([CP.PropsSI("T", "P", p, "S", s0, FLUID) for p in P])
    c = np.array([CP.PropsSI("A", "P", p, "S", s0, FLUID) for p in P])
    h = np.array([CP.PropsSI("H", "P", p, "S", s0, FLUID) for p in P])
    g = np.array([CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                             "P", p, "S", s0, FLUID) for p in P])

    single = np.ones(P.size, bool)
    for i, (t, p) in enumerate(zip(T, P)):
        if p < 0.999 * Pc:
            single[i] = t > CP.PropsSI("T", "P", p, "Q", 0, FLUID)
    M = np.sqrt(np.maximum(2.0 * (h0 - h), 0.0)) / c
    ok = single & (M >= 1.0) & (M <= M_MAX)

    idx = np.argsort(M[ok])
    Mo, go = M[ok][idx], g[ok][idx]
    integrand = np.sqrt(Mo ** 2 - 1.0) / (Mo * (1.0 + (go - 1.0) * Mo ** 2))
    nu = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1])
                                          * np.diff(Mo))])
    return dict(M=Mo, Gamma=go, nu=nu, integ=integrand,
                g_t=float(CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                                     "P", Pt, "T", Tt, FLUID)),
                g_in=float(go[0]))


def at_theta(r, theta_deg):
    """M2 and the dnu-weighted Gamma between the inlet and M2(theta)."""
    th = np.deg2rad(theta_deg)
    if r["nu"][-1] < th:
        return np.nan, np.nan
    M2 = float(np.interp(th, r["nu"], r["M"]))
    mask = r["M"] <= M2
    dm = r["integ"][mask]
    gbar = float(np.trapezoid(r["Gamma"][mask] * dm, r["M"][mask])
                 / np.trapezoid(dm, r["M"][mask]))
    return M2, gbar


def fit(x, y):
    p = np.polyfit(x, y, 1)
    pred = np.polyval(p, x)
    r2 = 1.0 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    return p, r2, float(np.max(np.abs(y - pred)))


def main():
    cond = np.loadtxt(os.path.join(ROOT, "data", "mm_table1.csv"),
                      delimiter=",", comments="#")
    zts, Pt, Tt = cond[:, 0], cond[:, 1], cond[:, 2]
    colors = plt.cm.viridis(np.linspace(0.12, 0.88, zts.size))
    res = [walk(p0, t0) for p0, t0 in zip(Pt, Tt)]

    # --- Gamma(M) ---------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(3.39, 2.9))
    for zt, r, c in zip(zts, res, colors):
        ax1.plot(r["M"], r["Gamma"], "-", color=c, label=r"$Z_t=%.1f$" % zt)
    ax1.axhline(1.0, color="0.45", ls=":", lw=0.9)
    ax1.set(xlabel=r"$M$", ylabel=r"$\Gamma$", xlim=(1.0, 2.3), ylim=(0.5, 1.1))
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="lower right")
    fig1.tight_layout()
    fig1.savefig(os.path.join(HERE, "mm_gamma_M.pdf"))
    fig1.savefig(os.path.join(HERE, "mm_gamma_M.png"))

    # --- correlations at three deflection angles -------------------------
    gt = np.array([r["g_t"] for r in res])
    g1 = np.array([r["g_in"] for r in res])

    fig2, ax0 = plt.subplots(figsize=(3.39, 2.9))
    fig3, ax1 = plt.subplots(figsize=(3.39, 2.7))
    marks = ("o", "s", "^")
    txt = {"a": [], "b": []}
    for th, mk in zip(THETAS, marks):
        M2 = np.array([at_theta(r, th)[0] for r in res])
        gb = np.array([at_theta(r, th)[1] for r in res])

        p, r2, dmax = fit(gb, M2)
        ax0.plot(gb, M2, mk, ms=4.0, mfc="none", mew=0.9,
                   label=r"$\theta=%d^\circ$ ($R^2=%.3f$)" % (th, r2))
        xx = np.linspace(gb.min(), gb.max(), 10)
        ax0.plot(xx, np.polyval(p, xx), "-", color="0.55", lw=0.7)







    ax0.set(xlabel=r"$\bar\Gamma$", ylabel=r"$M_2$", title=None)
    ax0.tick_params(direction="in", top=True, right=True)
    ax0.legend(frameon=False, loc="upper left", fontsize=6.0)

    # --- R2 versus theta --------------------------------------------------
    r2b, r21, r2t = [], [], []
    for th in THETA_SWEEP:
        M2 = np.array([at_theta(r, th)[0] for r in res])
        gb = np.array([at_theta(r, th)[1] for r in res])
        r2b.append(fit(gb, M2)[1])
        r21.append(fit(g1, M2)[1])
        r2t.append(fit(gt, M2)[1])
    ax1.semilogy(THETA_SWEEP, 1 - np.array(r2b), "o-", ms=3.0, color="#1f4fd1",
                   label=r"$\bar\Gamma$")
    ax1.semilogy(THETA_SWEEP, 1 - np.array(r21), "s-", ms=3.0, color="#2ca02c",
                   label=r"$\Gamma_1$")
    ax1.semilogy(THETA_SWEEP, 1 - np.array(r2t), "^-", ms=3.0, color="#c0392b",
                   label=r"$\Gamma_t$")
    ax1.set(xlabel=r"$\theta$ [deg]", ylabel=r"$1-R^2$",
              title=None)
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="lower right")

    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "mm_gamma_fit.pdf"))
    fig2.savefig(os.path.join(HERE, "mm_gamma_fit.png"))
    fig3.tight_layout()
    fig3.savefig(os.path.join(HERE, "mm_gamma_r2.pdf"))
    fig3.savefig(os.path.join(HERE, "mm_gamma_r2.png"))

    # --- csv --------------------------------------------------------------
    with open(os.path.join(HERE, "mm_gamma_path.csv"), "w") as f:
        f.write("# Gamma_t: total state; Gamma_1: fan inlet; Gamma_bar: dnu-weighted\n")
        f.write("theta_deg,zt,Gamma_t,Gamma_1,Gamma_bar,M2\n")
        for th in THETA_SWEEP:
            for zt, r in zip(zts, res):
                M2, gb = at_theta(r, th)
                f.write("%.0f,%.2f,%.4f,%.4f,%.4f,%.4f\n"
                        % (th, zt, r["g_t"], r["g_in"], gb, M2))
    for th, a, b, c in zip(THETA_SWEEP, r2b, r21, r2t):
        print("theta=%2.0f  R2(Gbar)=%.4f  R2(G1)=%.4f  R2(Gt)=%.4f" % (th, a, b, c))
    print("wrote mm_gamma_M, mm_gamma_fit, mm_gamma_r2 and mm_gamma_path.csv")


if __name__ == "__main__":
    main()
