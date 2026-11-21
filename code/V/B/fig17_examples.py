#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sec. V — two representative behaviours at Zt = 0.60.

The six operating conditions sharing Zt = 0.60 are plotted for a complex fluid
(MM) and for a simple one (ammonia): the curves collapse and reach the same
deflection for MM, whereas for ammonia they fan out and are truncated at very
different single-phase limits.

Outputs
    mm_examples.pdf/png
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
sys.path.insert(0, os.path.join(ROOT, "V", "A"))
from fluid_fan import fan, state_for  # noqa: E402

ZT = 0.60
PRS = (0.5, 0.8, 1.1, 1.6, 2.2, 3.0)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
                     "ytick.labelsize": 8, "legend.fontsize": 6.2,
                     "axes.linewidth": 0.8, "lines.linewidth": 1.0,
                     "figure.dpi": 300, "savefig.bbox": "tight"})


def main():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), sharey=False)
    for ax, fluid, tag in zip(axes, ("MM", "Ammonia"), ("(a)", "(b)")):
        Pc = CP.PropsSI("Pcrit", fluid)
        for pr in PRS:
            try:
                T0 = state_for(fluid, ZT, pr)
                r = fan(fluid, pr * Pc, T0)
            except Exception:
                r = None
            if r is None:
                continue
            ax.plot(r[0], r[1], "-", lw=1.1,
                    label=r"$P_t/P_c=%.1f$" % pr)
        ax.set(xlabel=r"$\theta$ [deg]", ylabel=r"$M_2$", xlim=(0, 60))
        ax.set_title(r"%s %s, $Z_t=0.60$" % (tag, "MM" if fluid == "MM" else "Ammonia"))
        ax.tick_params(direction="in", top=True, right=True)
        ax.legend(frameon=False, loc="upper left", ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "mm_examples.pdf"))
    fig.savefig(os.path.join(HERE, "mm_examples.png"))
    print("wrote mm_examples.pdf/png")


if __name__ == "__main__":
    main()
