#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check the present solver against the theory curves of Gajoni et al. (2026).

The solid 'Theory' curves of Fig. 8(b) were digitised from the vector PDF and
are stored in ``code/data/theory_jfm2026.csv``.  They are recomputed here from
the total conditions of dataset 1 and the measured inlet Mach number; the
deviation measures the implementation error of the present solver, separately
from any model/experiment difference.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cramer_pm  # noqa: E402
import fig04_experiment as EXP  # noqa: E402

THETA = np.array([5.0, 10.0, 15.0, 20.0, 25.0, 30.0])


def main():
    dat = np.loadtxt(os.path.join(ROOT, "data", "theory_jfm2026.csv"),
                     delimiter=",", comments="#")
    rows = []
    print(f"{'Zt':>5} {'max|dM|':>9} {'max rel [%]':>12}")
    for zt in (0.60, 0.75, 0.90):
        b = next(bb for t in EXP.TESTS
                 for bb in EXP.parse_dat(os.path.join(ROOT, "data", "experiment",
                                                      "test_%s.dat" % t))
                 if abs(bb["zt"] - zt) < 1e-6)
        res = cramer_pm.integrate(EXP.FLUID, b["Pt"] * 1e5, b["Tt"] + 273.15)
        nu1 = EXP.nu_from_M(res, b["rows"][0, 3])
        M_here = np.interp(nu1 + np.deg2rad(THETA), res["nu"], res["M"])
        sel = np.isclose(dat[:, 0], zt)
        M_ref = np.interp(THETA, dat[sel, 1], dat[sel, 2])
        d = M_here - M_ref
        print(f"{zt:5.2f} {np.max(np.abs(d)):9.4f} {100 * np.max(np.abs(d) / M_ref):12.3f}")
        rows.append(np.column_stack([np.full(THETA.size, zt), THETA, M_here, M_ref, d]))

    np.savetxt(os.path.join(HERE, "theory_check.csv"), np.vstack(rows), delimiter=",",
               comments="", header="zt,theta_deg,M_here,M_ref_jfm2026,dM", fmt="%.4f")
    print("wrote theory_check.csv")


if __name__ == "__main__":
    main()
