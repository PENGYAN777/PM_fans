# II/C — verification against Cramer & Crickenberger (1992)

| File | Role |
|---|---|
| `cramer_pm.py` | Integrates the Prandtl–Meyer ODE system **in the form used by Cramer & Crickenberger** (their Eqs. 8–10, independent variable = specific volume V), from the sonic state; `Γ`, `c_v` and `(∂p/∂T)_V` come from the CoolProp HEOS. |
| `fig02_literature_parity.py` | Produces **two independent figures**: `vv_cramer` (ν(M), this work vs the digitised curve) and `error` (relative Mach-number difference at matched ν), plus `fig02.csv`. |
| `../data/cramer1992_toluene.csv` | Seven points digitised from their Fig. 2 (ν = 0.4–1.0 rad in steps of 0.1), with ±0.02 in M. |

## What Cramer & Crickenberger did

* System (their Eqs. 8–10), integrated from the sonic point (ν = 0, M = 1, V = V*),
  with a **standard sixth-order Runge–Kutta** scheme.
* EOS: **Martin–Hou** for SF₆, toluene, pyridine, chlorobenzene and FC-75;
  **Redlich–Kwong** for R134a. Ideal-gas c_v as a power law c_v∞ = a T^n.
* Toluene stagnation state (their Table 1): T₀/T_c = 1.07, P₀/P_c = 2.01, V₀/V_c = 0.67.

## What we do

* Same equations, same sonic initial condition, same unknown.
  Integrator: DOP853 (8th-order explicit RK, rtol = 1e-10). The initial-value problem
  is identical to theirs; only the discretisation differs, and tightening/loosening the
  tolerance by two orders of magnitude changes ν by less than 1e-8 rad, i.e. four orders
  of magnitude below the 1 % effects discussed here.
* EOS: CoolProp **HEOS** (Helmholtz-energy multiparameter EOS; the toluene parameters
  reproduce T_c = 591.75 K, P_c = 4.1263 MPa, ρ_c = 291.99 kg m⁻³ of Lemmon & Span 2006).

## Result

* At the same (T₀, P₀) the HEOS gives **V₀/V_c = 0.693** versus **0.67** in Martin–Hou
  (+3.4 % in specific volume), and Z₀ = 0.344.
* Along the isentrope the computed curve reproduces the published one to within
  **1.6 % in M at matched ν** (7 points, ν = 0.4–1.0 rad). The digitisation uncertainty of
  the 1992 scan is ±0.02 in M, i.e. ±1.3 %, so the deviations sit at the level of the
  digitisation band and of the 3.4 % EOS difference at the stagnation state.
* `fig02.csv` lists all seven comparisons; the near-vertical section (ν ≈ 0.4–0.6, where
  M is non-monotone) is the part least well resolved by the scan.
* `error.pdf/png` shows the deviation alone: the ±1.3 % digitisation band is quoted in the
  text and in `fig02.csv` but is deliberately not drawn in the figure.

## Reproduce

```bash
cd code/II/C
MPLCONFIGDIR=/tmp/mpl python fig02_literature_parity.py
```

## Validation against the experiment (Gajoni et al., 2026)

| File | Purpose |
|---|---|
| `data/experiment/test_A1.dat` ... | raw experimental tables (total conditions, and P, M with their 95 % uncertainties) |
| `data/theory_jfm2026.csv` | Prandtl-Meyer theory curves of Ref. 30, digitised from their Fig. 8 (vector PDF) |
| `fig04_experiment.py` | compares the calculated Mach number with dataset 1 (A1 + B1, three Z_t) and writes `vv_ex.pdf/png` and `tolerance.pdf/png` |
| `check_theory_jfm2026.py` | recomputes the published theory curves: max deviation 0.013 / 0.19 / 0.24 % for Zt = 0.60 / 0.75 / 0.90 |
| `vv_ex.pdf/png` | Mach number vs deflection angle (calculation + measurements) |
| `tolerance.pdf/png` | residuals normalised by the combined uncertainty |
| `vv_experiment.csv` | measured and computed Mach numbers and normalised residuals |
| `theory_check.csv` | present vs published theory curves |

Reproduce:

```bash
python fig04_experiment.py        # experiment comparison (M only)
python check_theory_jfm2026.py    # implementation check vs published theory
```

Result: the calculation reproduces the published theory curves to within 0.25 % in M,
so the residual against the measurements (up to 2.7 %, i.e. 2.6 sigma of the combined
uncertainty) is a model/experiment difference, not an implementation error.
