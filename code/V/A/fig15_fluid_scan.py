#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sec. V — Zt similarity test for one fluid, truncated at the single-phase limit.

For each Zt in ZTS six conditions are built at Pt/Pc = 1.0 ... 1.5 (Tt solved so
that Z(Pt,Tt) = Zt) and the fan is computed with fluid_fan.fan, which stops where
the isentrope meets the saturation curve.  The spread of M2 and dP among the
conditions of the same Zt is evaluated at the largest deflection for which all of
them are still single phase (theta_eval, at most 50 deg) and reported together
with theta_eval.

Usage
    python fig15_fluid_scan.py <FluidName>
"""
import os
import sys

import numpy as np
import CoolProp.CoolProp as CP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fluid_fan import fan, state_for, value_at  # noqa: E402

ZTS = (0.40, 0.50, 0.60, 0.70, 0.80, 0.90)
# wide pressure sampling, as in the original similarity study: low-Zt states
# are then far from the saturation curve and the fan can develop
PRS = (0.5, 0.8, 1.1, 1.6, 2.2, 3.0)
THETA_MAX = 50.0


def scan(fluid):
    rows = []
    for zt in ZTS:
        curves = []
        for pr in PRS:
            try:
                T0 = state_for(fluid, zt, pr)
                fc = fan(fluid, pr * CP.PropsSI("Pcrit", fluid), T0)
            except Exception:
                fc = None
            if fc is not None:
                curves.append(fc)
        if len(curves) < 3:
            rows.append((zt, len(curves), np.nan, np.nan, np.nan, np.nan, np.nan))
            continue
        th_max = np.array([c[0][-1] for c in curves])
        th_eval = min(THETA_MAX, th_max.min())
        M2 = [value_at(c[0], c[1], th_eval) for c in curves]
        dP = [value_at(c[0], c[2], th_eval) for c in curves]
        M2 = np.array([m for m in M2 if m is not None])
        dP = np.array([d for d in dP if d is not None])
        if M2.size < 3:
            rows.append((zt, len(curves), np.nan, np.nan, np.nan, np.nan, np.nan))
            continue
        rows.append((zt, len(curves),
                     100 * (M2.max() - M2.min()) / M2.mean(),
                     100 * (dP.max() - dP.min()) / dP.mean(), th_eval,
                     th_max.mean(),
                     100 * (th_max.max() - th_max.min()) / th_max.mean()))
    return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    fluid = sys.argv[1]
    print("fluid: %s   Tc=%.2f K  Pc=%.4f MPa"
          % (fluid, CP.PropsSI("Tcrit", fluid), CP.PropsSI("Pcrit", fluid) / 1e6))
    print("Zt    n_cond  theta_eval  dM2 [%]  dP [%]   theta_max  d_theta_max [%]")
    rows = scan(fluid)
    for zt, n, sm, sp, th, tmm, dtm in rows:
        print("%.2f  %6d  %10.1f  %7.2f  %6.2f   %8.1f  %12.1f"
              % (zt, n, th, sm, sp, tmm, dtm))
    hi = [r for r in rows if r[0] >= 0.6 - 1e-9 and np.isfinite(r[2])]
    if hi:
        print("max over Zt in [0.6, 0.9]:  M2 %.2f %%   dP %.2f %%"
              % (max(r[2] for r in hi), max(r[3] for r in hi)))
    path = os.path.join(HERE, "fluid_scan.csv")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# fluid,Zt,n_cond,spread_M2,spread_dP,theta_eval,theta_max_mean,d_thetamax\n")
        for zt, n, sm, sp, th, tmm, dtm in rows:
            f.write("%s,%.2f,%d,%.3f,%.3f,%.1f,%.1f,%.1f\n"
                    % (fluid, zt, n, sm, sp, th, tmm, dtm))


if __name__ == "__main__":
    main()
