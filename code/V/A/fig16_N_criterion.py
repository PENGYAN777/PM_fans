#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sec. V — the similarity criterion as a function of the molecular complexity N.

For every fluid of the list the spread of the post-expansion Mach number and of
the single-phase extent of the fan are plotted against N, together with the 5 %
threshold used as engineering criterion.  The spreads are those computed at
Zt = 0.70 (see fig15_fluid_scan.py).

Outputs
    mm_N_criterion.pdf/png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.5,
                     "axes.linewidth": 0.8, "figure.dpi": 300,
                     "savefig.bbox": "tight"})

ZTS = (0.60, 0.70)


def main():
    N = {}
    with open(os.path.join(ROOT, "data", "fluids_v.csv")) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            a = line.strip().split(",")
            if len(a) >= 3:
                N[a[0]] = float(a[1])

    d = np.genfromtxt(os.path.join(HERE, "fluid_scan.csv"), delimiter=",",
                      names=True, dtype=None, encoding=None)
    sel = np.abs(d["Zt"] - ZTS[0]) < 1e-9
    rows = []
    for f, m2, dt in zip(d["fluid"][sel], d["spread_M2"][sel], d["d_thetamax"][sel]):
        if f in N and np.isfinite(m2) and np.isfinite(dt):
            rows.append((N[f], f, m2, dt))
    rows.sort()
    n = np.array([r[0] for r in rows])
    m2 = np.array([r[2] for r in rows])
    dt = np.array([r[3] for r in rows])
    sel7 = np.abs(d["Zt"] - ZTS[1]) < 1e-9
    n7, m27, dt7 = [], [], []
    for f, a, b in zip(d["fluid"][sel7], d["spread_M2"][sel7], d["d_thetamax"][sel7]):
        if f in N and np.isfinite(a) and np.isfinite(b):
            n7.append(N[f]); m27.append(a); dt7.append(b)
    n7, m27, dt7 = np.array(n7), np.array(m27), np.array(dt7)

    fig, ax = plt.subplots(figsize=(3.49, 3.35))
    ax.semilogy(n, dt, "o", ms=4.2, mfc="none", mec="#1f4fd1", mew=0.9,
                label=r"$\Delta\theta_{\max}$, $Z_t=0.6$")
    ax.semilogy(n, m2, "s", ms=3.6, mfc="none", mec="#e07020", mew=0.9,
                label=r"$\Delta M_2$, $Z_t=0.6$")
    ax.semilogy(n7, dt7, "o", ms=3.4, mfc="none", mec="#1f4fd1", mew=0.8, alpha=0.45,
                label=r"$\Delta\theta_{\max}$, $Z_t=0.7$")
    ax.semilogy(n7, m27, "s", ms=2.9, mfc="none", mec="#e07020", mew=0.8, alpha=0.45,
                label=r"$\Delta M_2$, $Z_t=0.7$")
    ax.axvspan(19.0, 25.0, color="0.92", zorder=0)
    ax.axhline(5.0, color="0.4", ls="--", lw=0.9)
    ax.axvline(25.0, color="0.4", ls=":", lw=0.9)
    ax.text(21.5, 150, "transition", fontsize=6.2, color="0.35", ha="center")
    ax.text(26, 0.35, r"$N=25$", fontsize=6.5, color="0.35")
    ax.text(3.2, 5.8, r"$5\%$", fontsize=6.5, color="0.35")
    for x, f, a, b in rows:
        if f in ("MM", "Water", "Propane", "R134a", "D6", "Hydrogen"):
            ax.annotate(f, (x, b), textcoords="offset points", xytext=(4, 4),
                        fontsize=5.8, color="0.3")
    ax.set(xscale="log", xlabel=r"molecular complexity $N$",
           ylabel="spread [%]", ylim=(0.2, 300), xlim=(2.5, 320))
    ax.tick_params(direction="in", top=True, right=True, which="both")
    ax.legend(frameon=True, framealpha=0.9, loc="upper right", fontsize=5.4,
              handletextpad=0.4, labelspacing=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "mm_N_criterion.pdf"))
    fig.savefig(os.path.join(HERE, "mm_N_criterion.png"))
    print("wrote mm_N_criterion.pdf/png")


if __name__ == "__main__":
    main()
