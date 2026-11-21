#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prandtl-Meyer fan along an isentrope, parametrised by pressure.

The fan is built with (P, s) calls only: for simple fluids the expansion
reaches densities at which the (rho, s) flash of CoolProp is not available,
whereas the (P, s) calls stay well defined.  The curve is truncated at the
single-phase limit, i.e. where the isentrope meets the saturation curve.

Returned arrays are the deflection theta [deg], the Mach number, and the
pressure drop dP = (P1 - P2)/P1, all from the sonic point up to the last
single-phase state.
"""
import numpy as np
import CoolProp.CoolProp as CP
from scipy.optimize import brentq


def fan(fluid, P0, T0, n=500):
    """theta, M2, dP along the fan; dP is referred to the sonic pressure."""
    s0 = CP.PropsSI("S", "P", P0, "T", T0, fluid)
    h0 = CP.PropsSI("H", "P", P0, "T", T0, fluid)
    Pc = CP.PropsSI("Pcrit", fluid)

    P = np.geomspace(P0, 0.005 * P0, n)
    T = np.full(n, np.nan)
    M = np.full(n, np.nan)
    G = np.full(n, np.nan)
    for i, p in enumerate(P):
        try:
            t = CP.PropsSI("T", "P", p, "S", s0, fluid)
            if p < Pc and t <= CP.PropsSI("T", "P", p, "Q", 0, fluid):
                break
            c = CP.PropsSI("A", "P", p, "S", s0, fluid)
            h = CP.PropsSI("H", "P", p, "S", s0, fluid)
            T[i] = t
            M[i] = np.sqrt(max(2.0 * (h0 - h), 0.0)) / c
            G[i] = CP.PropsSI("fundamental_derivative_of_gas_dynamics",
                              "P", p, "S", s0, fluid)
        except Exception:
            break

    ok = np.isfinite(M) & (M >= 1.0)
    if ok.sum() < 5:
        return None
    P, M, G = P[ok], M[ok], G[ok]
    i = np.argsort(M)
    M, G, P = M[i], G[i], P[i]

    integ = np.sqrt(M ** 2 - 1.0) / (M * (1.0 + (G - 1.0) * M ** 2))
    nu = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(M))])
    dP = 1.0 - P / P[0]
    return np.rad2deg(nu), M, dP


def state_for(fluid, zt, pr):
    """Total temperature giving Z(Pt, Tt) = zt at Pt = pr * Pc."""
    Tc, Pc = CP.PropsSI("Tcrit", fluid), CP.PropsSI("Pcrit", fluid)
    return brentq(lambda T: CP.PropsSI("Z", "P", pr * Pc, "T", T, fluid) - zt,
                  1.002 * Tc, 2.5 * Tc, xtol=1e-6)


def value_at(th_curve, arr, theta):
    """Interpolate a quantity at the deflection theta, or None if not reached."""
    if th_curve[-1] < theta:
        return None
    return float(np.interp(theta, th_curve, arr))
