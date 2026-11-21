#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prandtl-Meyer function in a dense gas, integrated with the *same equations*
as Cramer & Crickenberger (1992), AIAA J. 30(2) 561-564.

Cramer & Crickenberger integrate the system (their Eqs. 8-10)

    dnu/dV =  sqrt(M^2 - 1) / (V M^2)                       (8)
    dM /dV = -(M/V) (1 - Gamma - 1/M^2)                     (9)
    dT /dV = -(T/cv) (dp/dT)|_V                             (10)

from the sonic state (nu = 0, M = 1 at V = V*, Eq. 14).  They used a standard
sixth-order Runge-Kutta scheme; here the same initial-value problem is solved
with an eighth-order adaptive Runge-Kutta (DOP853) at rtol = 1e-10, i.e. the
discretisation error is far below the physical differences of interest.

The only deliberate difference is the thermodynamic model: Cramer &
Crickenberger used the Martin-Hou equation of state (Redlich-Kwong for R134a),
whereas here Gamma, cv and (dp/dT)_V are evaluated with the Helmholtz-energy
multiparameter EOS (HEOS) of CoolProp.  The integration therefore stays exactly
on the isentrope of the HEOS.
"""
import numpy as np
import CoolProp.CoolProp as CP
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def _props(fluid, T, rho):
    """Local thermodynamic quantities needed by Eqs. (8)-(10)."""
    return {
        "Gamma": CP.PropsSI("fundamental_derivative_of_gas_dynamics", "T", T, "D", rho, fluid),
        "cv": CP.PropsSI("O", "T", T, "D", rho, fluid),          # mass specific heat, J/kg/K
        "dPdT": CP.PropsSI("d(P)/d(T)|D", "T", T, "D", rho, fluid),
        "c": CP.PropsSI("A", "T", T, "D", rho, fluid),
        "h": CP.PropsSI("H", "T", T, "D", rho, fluid),
        "P": CP.PropsSI("P", "T", T, "D", rho, fluid),
    }


def sonic_state(fluid, P0, T0):
    """Sonic point on the isentrope through (P0, T0): V_flow = c."""
    s0 = CP.PropsSI("S", "P", P0, "T", T0, fluid)
    h0 = CP.PropsSI("H", "P", P0, "T", T0, fluid)
    rho0 = CP.PropsSI("D", "P", P0, "T", T0, fluid)

    def f(rho):
        T = CP.PropsSI("T", "D", rho, "S", s0, fluid)
        c = CP.PropsSI("A", "D", rho, "S", s0, fluid)
        h = CP.PropsSI("H", "D", rho, "S", s0, fluid)
        return np.sqrt(max(2.0 * (h0 - h), 0.0)) - c

    try:
        rho_s = brentq(f, 0.05 * rho0, rho0, xtol=1e-12, rtol=1e-14)
        T_s = CP.PropsSI("T", "D", rho_s, "S", s0, fluid)
    except Exception:
        # fallback for fluids whose isentrope cannot be parametrised by rho
        # (e.g. hydrogen): locate the sonic point by scanning the pressure
        Ps = np.geomspace(P0, 0.02 * P0, 60)
        d = []
        for p in Ps:
            try:
                T = CP.PropsSI("T", "P", p, "S", s0, fluid)
                c = CP.PropsSI("A", "P", p, "S", s0, fluid)
                h = CP.PropsSI("H", "P", p, "S", s0, fluid)
                d.append(np.sqrt(max(2.0 * (h0 - h), 0.0)) - c)
            except Exception:
                d.append(np.nan)
        d = np.array(d)
        ok = np.isfinite(d)
        i = np.where(np.diff(np.sign(d[ok])) != 0)[0][0]
        idx = np.where(ok)[0]
        pa, pb = Ps[idx[i]], Ps[idx[i + 1]]
        P_s = brentq(lambda p: (np.sqrt(max(2.0 * (h0 - CP.PropsSI("H", "P", p, "S", s0, fluid)), 0.0))
                                - CP.PropsSI("A", "P", p, "S", s0, fluid)),
                     pa, pb, xtol=1e-6)
        T_s = CP.PropsSI("T", "P", P_s, "S", s0, fluid)
        rho_s = CP.PropsSI("D", "P", P_s, "S", s0, fluid)
    return dict(rho_s=rho_s, V_s=1.0 / rho_s, T_s=T_s, s0=s0, h0=h0, rho0=rho0)


def integrate(fluid, P0, T0, Mmax=2.6, rtol=1e-10, atol=1e-12, method="DOP853",
              V_end_factor=60.0):
    """Integrate Eqs. (8)-(10) from the sonic point up to M = Mmax."""
    st = sonic_state(fluid, P0, T0)

    def rhs(V, y):
        nu, M, T = y
        rho = 1.0 / V
        p = _props(fluid, T, rho)
        dnu = np.sqrt(max(M * M - 1.0, 0.0)) / (V * M * M)
        dM = -(M / V) * (1.0 - p["Gamma"] - 1.0 / (M * M))
        dT = -(T / p["cv"]) * p["dPdT"]
        return [dnu, dM, dT]

    def hit_Mmax(V, y):
        return y[1] - Mmax
    hit_Mmax.terminal = True

    V_end = V_end_factor * st["V_s"]
    sol = solve_ivp(rhs, (st["V_s"], V_end), [0.0, 1.0, st["T_s"]], method=method,
                    rtol=rtol, atol=atol, events=hit_Mmax, dense_output=True,
                    max_step=(V_end - st["V_s"]) / 200.0)
    V = sol.t
    nu, M, T = sol.y
    rho = 1.0 / V
    P = np.array([CP.PropsSI("P", "T", t, "D", r, fluid) for t, r in zip(T, rho)])
    return dict(V=V, rho=rho, nu=nu, M=M, T=T, P=P, sonic=st, success=sol.success)


if __name__ == "__main__":
    # Cramer & Crickenberger, Table 1: toluene, T0/Tc = 1.07, P0/Pc = 2.01
    fl = "Toluene"
    Tc, Pc = CP.PropsSI("Tcrit", fl), CP.PropsSI("Pcrit", fl)
    res = integrate(fl, 2.01 * Pc, 1.07 * Tc)
    print(f"toluene: Tc={Tc:.2f} K Pc={Pc/1e6:.3f} MPa")
    print(f"sonic state: T*={res['sonic']['T_s']:.2f} K, rho*={res['sonic']['rho_s']:.2f} kg/m3")
    print(f"nu_max={res['nu'].max():.4f} rad at M={res['M'][res['nu'].argmax()]:.3f}")
    for m in (1.2, 1.4, 1.6, 1.8, 2.0):
        print(f"  M={m:.1f}  nu={np.interp(m, res['M'], res['nu']):.4f} rad")
