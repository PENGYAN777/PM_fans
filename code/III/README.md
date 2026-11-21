# III — Effect of flow non-ideality on the expansion fan (siloxane MM)

The section is organised as **validity → effect → mechanism**.

| Sub-folder | Contents | Paper element |
|---|---|---|
| `A/` | **Range of validity** of the one-dimensional isentropic fan: single-phase check along the isentropes, `Gamma > 0`, admissible `(Zt, theta)` region. | Fig. 4 (T–P map), supplementary (Zt, θ) |
| `B/` | Effect of non-ideality within the range fixed in `A/`: post-expansion Mach number and pressure change versus deflection angle for the six conditions of Table I. | Figs. 5, 6 |
| `C/` | **Mechanism**: `Gamma(M)` along each isentrope, the `dnu`-weighted path average, `Gammat` (M = 0) versus `Gamma1` (M = 1), and the correlation between `M2` and the Γ path. | Figs. 7, 8 |

The former `B/` (CFD comparison) has been dropped; a one-sentence statement on the
2-D inviscid check is kept in III.A.

## A/ — scripts

| File | Purpose | Output |
|---|---|---|
| `fig10_pt_map.py` | `(T, P)` map: the six isentropes against the saturation curve | `mm_pt_map.pdf/png`, `mm_pt_map.csv`, `mm_gamma_check.csv` |
| `fig09_domain.py` | admissible `(Zt, theta)` region from the single-phase and `Gamma > 0` criteria | `mm_domain.pdf/png`, `mm_domain.csv` |

## C/ — scripts

| File | Purpose | Output |
|---|---|---|
| `fig07_gamma_path.py` | walks the six isentropes, computes `Gamma(M)`, the `dnu`-weighted average and the correlations with `M2` | `mm_gamma_M.pdf/png`, `mm_gamma_fit.pdf/png`, `mm_gamma_r2.pdf/png`, `mm_gamma_path.csv` |

Result: `M2` against the path average gives `R2 = 0.994` at 50 deg (0.994-1.000 for 10-50 deg),
against `Gamma_1` `R2 = 0.989`, and against `Gamma_t` only `0.049` (the least non-ideal case has the
largest `Gamma_t` and the lowest `M2`). The path average must be taken over the actual fan (1 -> M2),
not over the whole integrated path.

## B/ — scripts

| File | Purpose | Output |
|---|---|---|
| `fig05_zt_effect.py` | M2 and dP versus deflection angle, and nu(M), for the six Zt of Table I | `mm_m2_theta.pdf/png`, `mm_dp_theta.pdf/png`, `mm_mach_nu.pdf/png`, `mm_zt_effect.csv` |

Input: `code/data/mm_table1.csv` (Table I conditions). The solver is `code/II/C/cramer_pm.py`
(DOP853, rtol 1e-10), i.e. the same code used for the verification of Sec. II.

Note: the figures originally produced by `theta.py` (fixed-step RK4/Simpson tables `z4.csv` ... `z9.csv`)
differ from these by at most 0.004 in M2 (0.4 %, largest at small deflection) and 0.003 in dP, because
in that code the Prandtl-Meyer function was advanced with the Mach number frozen at the beginning of
each step.
