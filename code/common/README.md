# `common/` — shared modules

Everything that more than one section needs. Keep this folder small and stable; section folders
must not re-implement any of it.

Planned content (fill in as the sections are rewritten):

| Module | Purpose |
|---|---|
| `thermo.py` | CoolProp (HEOS) wrapper: state from (P,T) or (P,s); `Z`, `Γ`, `c`, `h`; fluid table (`MM`, `MDM`, `D4`, `D6`, `toluene`, `CO2`, …) |
| `pm.py` | Prandtl–Meyer solver: integration of Eq. (5) with RK4, `ν(M)`, inversion `M(ν)`, and the `Γ(M)` path used in Sec. III.C |
| `plotstyle.py` | `matplotlib` rcParams (font 9–10 pt at final size, colour-blind-safe cycle, EPS/PDF export) |
| `paths.py` | Project root resolution and `data/` access, so no script hard-codes a path |

Rule of thumb: if a function is used by two or more figures, it belongs here; if it is used once,
it stays in the section folder.
