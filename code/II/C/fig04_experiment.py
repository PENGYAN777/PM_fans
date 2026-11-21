#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation of the Mach number against the experiment of Gajoni et al. (2026).

The raw data are the four files ``test_A1.dat`` ... ``test_B2.dat`` in
``code/data/experiment/``: total conditions with their expanded uncertainties
and, for each deflection angle, the measured Mach number (from schlieren) with
its expanded uncertainty (95 % confidence level).

Dataset 1 (tests A1 + B1) is used: the Prandtl-Meyer fan is recomputed from the
measured total conditions and the measured inlet Mach number, and the Mach
number at each deflection is compared with the measurement.  The residuals are
normalised by the combined uncertainty, which includes the propagation of the
total-pressure and total-temperature uncertainties.

Outputs
    vv_experiment.pdf/png   (a) M vs theta, (b) normalised residuals
    vv_experiment.csv       measured and computed Mach numbers, and residuals
"""
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cramer_pm  # noqa: E402

FLUID = "MM"
TESTS = ("A1", "B1")                      # dataset 1
COLORS = {0.60: "#1f77b4", 0.75: "#e07020", 0.90: "#2ca02c"}
MARKERS = {"A1": "o", "B1": "s"}
LABELS = {0.60: r"$Z_t=0.60$", 0.75: r"$Z_t=0.75$", 0.90: r"$Z_t=0.90$"}

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 7.5,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.3,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def parse_dat(path):
    """Return a list of blocks, one per Z_t value."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for chunk in re.split(r"-{5,}", txt):
        m = re.search(r"ZT\s*=\s*([\d.]+)", chunk)
        if not m:
            continue
        pt = re.search(r"PT.*?=\s*([-\d.]+)\s*±\s*([-\d.]+)", chunk)
        tt = re.search(r"TT.*?=\s*([-\d.]+)\s*±\s*([-\d.]+)", chunk)
        rows = []
        for line in chunk.splitlines():
            f = line.split()
            if len(f) < 5:
                continue
            try:
                th, P, uP, M, uM = (float(f[0]), float(f[1]), float(f[2]),
                                    float(f[3]), float(f[4]))
            except ValueError:
                continue
            rows.append((th, P, uP, M, uM))
        out.append(dict(zt=float(m.group(1)),
                        Pt=float(pt.group(1)), uPt=float(pt.group(2)),
                        Tt=float(tt.group(1)), uTt=float(tt.group(2)),
                        rows=np.array(rows)))
    return out


def nu_from_M(res, M_in):
    """Turning angle accumulated between the sonic point and M_in."""
    M, nu = res["M"], res["nu"]
    i = int(np.argmax(M))                       # ascending branch only
    return float(np.interp(M_in, M[: i + 1], nu[: i + 1]))


def Mach_curve(Pt, TtK, M_in, th_deg):
    res = cramer_pm.integrate(FLUID, Pt, TtK)
    return np.interp(nu_from_M(res, M_in) + np.deg2rad(th_deg), res["nu"], res["M"])


def curve_with_uncertainty(b, th_deg):
    """Nominal curve plus the band induced by the Pt and Tt uncertainties."""
    M_in = b["rows"][0, 3]
    nom = Mach_curve(b["Pt"] * 1e5, b["Tt"] + 273.15, M_in, th_deg)
    var = [Mach_curve((b["Pt"] + s * b["uPt"]) * 1e5, b["Tt"] + 273.15, M_in, th_deg)
           for s in (+1, -1)]
    var += [Mach_curve(b["Pt"] * 1e5, b["Tt"] + s * b["uTt"] + 273.15, M_in, th_deg)
            for s in (+1, -1)]
    var = np.array(var)
    return nom, 0.5 * (var.max(axis=0) - var.min(axis=0))


def main():
    data = {}
    for t in TESTS:
        for b in parse_dat(os.path.join(ROOT, "data", "experiment", "test_%s.dat" % t)):
            data[(t, round(b["zt"], 2))] = b

    fig1, ax1 = plt.subplots(figsize=(3.5, 2.7))     # Mach number
    fig2, ax2 = plt.subplots(figsize=(3.4, 2.4))     # residuals
    rows, stats = [], []

    for zt in (0.60, 0.75, 0.90):
        for t in TESTS:
            b = data[(t, zt)]
            th, uM, M = b["rows"][:, 0], b["rows"][:, 4], b["rows"][:, 3]
            M_calc, uM_c = curve_with_uncertainty(b, th)
            u_tot = np.hypot(uM, uM_c)
            z = (M_calc - M) / u_tot

            c, mk = COLORS[zt], MARKERS[t]
            ax1.errorbar(th, M, yerr=uM, fmt=mk, ms=3.2, mfc="none", mec=c,
                         ecolor=c, elinewidth=0.6, capsize=1.5,
                         label=LABELS[zt] if t == TESTS[0] else None)
            ax2.plot(th, z, mk + "-", ms=3.0, mfc="none", color=c, lw=0.9,
                     alpha=0.95 if t == TESTS[0] else 0.55)

            rows.append(np.column_stack([np.full(th.size, zt), np.full(th.size, float(t[1])),
                                         th, M, M_calc, z]))
            stats.append((t, zt, np.max(np.abs((M_calc - M) / M)),
                          np.max(np.abs(z)), np.sqrt(np.mean(z ** 2))))
            print("%s  Zt=%.2f  max|dM|/M=%.2f%%  max|z|=%.2f  rms z=%.2f"
                  % (t, zt, 100 * np.max(np.abs((M_calc - M) / M)),
                     np.max(np.abs(z)), np.sqrt(np.mean(z ** 2))))

        b = data[("A1", zt)]
        thg = np.linspace(0, 30, 121)
        ax1.plot(thg, Mach_curve(b["Pt"] * 1e5, b["Tt"] + 273.15, b["rows"][0, 3], thg),
                 "-", color=COLORS[zt], lw=1.3)

    ax1.set(xlabel=r"$\theta$ [deg]", ylabel=r"$M$")
    ax1.tick_params(direction="in", top=True, right=True)
    ax1.legend(frameon=False, loc="upper left")
    fig1.tight_layout()
    fig1.savefig(os.path.join(HERE, "vv_ex.pdf"))
    fig1.savefig(os.path.join(HERE, "vv_ex.png"))

    ax2.axhspan(-1, 1, color="0.9", zorder=0)
    ax2.axhline(0, color="k", lw=0.6, ls=":")
    ax2.set(xlabel=r"$\theta$ [deg]",
            ylabel=r"$(M_{\rm calc}-M_{\rm exp})/U$", ylim=(-3.5, 3.5))
    ax2.tick_params(direction="in", top=True, right=True)
    fig2.tight_layout()
    fig2.savefig(os.path.join(HERE, "tolerance.pdf"))
    fig2.savefig(os.path.join(HERE, "tolerance.png"))

    np.savetxt(os.path.join(HERE, "vv_experiment.csv"), np.vstack(rows), delimiter=",",
               comments="", header="zt,test,theta_deg,M_exp,M_calc,z", fmt="%.4f")
    z_all = np.array([s[3] for s in stats])
    print("dataset 1: max |dM|/M = %.2f %%,  max |z| = %.2f"
          % (100 * max(s[2] for s in stats), z_all.max()))
    print("wrote vv_ex.pdf/png, tolerance.pdf/png, vv_experiment.csv")


if __name__ == "__main__":
    main()
