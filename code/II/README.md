# II — Problem formulation, solution method and verification

| Sub-folder | Contents | Paper element |
|---|---|---|
| `A/` | Governing equations for the non-ideal PM fan (Eqs. 3–5). No production code expected; anything used to check the algebra (symbolic or numeric spot checks) goes here. | Eqs. (3)–(5) |
| `B/` | Solution procedure: wrapper around `common/pm.py`, the six operating conditions of Table I, the RK4 step-convergence check, the M1 = 1 starting procedure. | Table I, Eq. (5), Sec. II.B text |
| `C/` | Verification and validation: literature parity (Cramer 1992), CFD single-point check, experiment (Gajoni 2026) with error bars, error-budget table. | Figs. 2–4, Table II |

**Rule for this section:** a reader must be able to reproduce every number quoted in II.C with
`python fig0X_*.py`, without editing a single line.
