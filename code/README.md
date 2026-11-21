# Code and data for *Similarity of Prandtl–Meyer expansion fans in non-ideal compressible flows*

This folder mirrors the structure of the manuscript: every sub-folder holds the scripts that
produce the figures/tables of one subsection, so that a reader can go from a figure in the paper
to the code that generated it in two clicks.

## Layout

```
code/
├── common/          shared modules (thermodynamics, PM solver, plotting style)
├── data/            input tables (fluid properties, operating conditions) and digitised data
├── II/              Problem formulation, solution method and verification
│   ├── A/           governing equations (no production code; any symbolic check lives here)
│   ├── B/           solution procedure: PM ODE integrator wrapper, Table I conditions, RK4 study
│   └── C/           verification & validation figures (literature, CFD, experiment, error budget)
├── III/             Effect of flow non-ideality
│   ├── A/           range of validity: (T,P) map, admissible (Zt, theta) region
│   ├── B/           Zt sweep: post-expansion Mach number and pressure change vs deflection
│   └── C/           mechanism: Γ(M) along the isentrope, Γt vs Γ1, M2 vs Γ path
├── IV/              Similarity laws
│   ├── A/           Zt as a similarity parameter (six conditions per Zt)
│   ├── B/           test of Γ1: same Γ1, different Pt/Tt
│   └── C/           synthesis of the similarity criterion
└── V/               Fluids with different molecular complexity and molar mass
    ├── A/           complex fluids
    ├── B/           simple fluids
    └── C/           classification and empirical threshold (moved to appendix in the paper)
```

## Conventions

1. **One figure = one script.** Name the script after the paper element it produces
   (`fig03_experiment_validation.py`) and have it write both the figure (`fig03.pdf/png`)
   and the underlying numbers (`fig03.csv`). The CSV is what a reader needs to check the paper.
2. **Shared code lives in `common/`.** Do not copy the PM integrator or the CoolProp wrappers into
   several section folders: duplicated solvers diverge and reviewers notice. Section folders should
   contain only the case setup, the sweep, and the plotting.
3. **No absolute paths.** Every script resolves its own directory (`Path(__file__).parent`) and reads
   inputs from `code/data/`. Command-line flags may override, but the defaults must run as-is.
4. **Same style everywhere.** `common/plotstyle.py` sets the font size, line widths and colour cycle,
   so all figures in the paper are visually consistent.
5. **Reproducible environment.** See `environment.yml`. The numbers in the paper were produced with
   CoolProp 8.0.0 (HEOS backend, fluid `MM` unless stated otherwise).

## Figure → script map (to be filled as the sections are rewritten)

| Paper element | Folder | Script | Output data |
|---|---|---|---|
| Fig. 2a (ν–M vs Cramer 1992) | `II/C` | `fig02_literature_parity.py` → `vv_cramer` | `fig02.csv` |
| Fig. 2b (relative difference) | `II/C` | `fig02_literature_parity.py` → `error` | `fig02.csv` |
| Fig. 3 (experiment, M) | `II/C` | `fig04_experiment.py` → `vv_ex` | `vv_experiment.csv` |
| Fig. 4 (normalised residuals) | `II/C` | `fig04_experiment.py` → `tolerance` | `vv_experiment.csv` |
| Fig. 5 (P–T map) | `III/A` | `fig10_pt_map.py` → `mm_pt_map` | `mm_pt_map.csv` |
| Fig. 6 (M2 vs theta) | `III/B` | `fig05_zt_effect.py` → `mm_m2_theta` | `mm_zt_effect.csv` |
| Fig. 7 (dP vs theta) | `III/B` | `fig05_zt_effect.py` → `mm_dp_theta` | `mm_zt_effect.csv` |
| Fig. 8 (Gamma vs M) | `III/C` | `fig07_gamma_path.py` → `mm_gamma_M` | `mm_gamma_path.csv` |
| Fig. 9 (M2 vs Gamma) | `III/C` | `fig07_gamma_path.py` → `mm_gamma_fit` | `mm_gamma_path.csv` |
| Fig. 10 (1 - R2 vs theta) | `III/C` | `fig07_gamma_path.py` → `mm_gamma_r2` | `mm_gamma_path.csv` |
| IV Fig. 7 (operating points) | `IV/A` | `fig11_zt_similarity.py` → `mm_zt_pt` | `mm_zt_similarity.csv` |
| IV Fig. 8 (M2 bands) | `IV/A` | `fig11_zt_similarity.py` → `mm_zt_band` | `mm_zt_similarity.csv` |
| IV Fig. 9 (spread vs Zt) | `IV/A` | `fig11_zt_similarity.py` → `mm_zt_spread` | `mm_zt_similarity.csv` |
| IV Fig. 10 (Gamma(M) + spread) | `IV/A` | `fig12_zt_path.py` → `mm_zt_gamma` | `mm_zt_path.csv` |
| IV Fig. 5 (Gamma1 families) | `IV/B` | `fig13_gamma1_similarity.py` → `mm_g1_curves` | `mm_g1_similarity.csv` |
| IV Fig. 6 (Gamma(M) paths) | `IV/B` | `fig13_gamma1_similarity.py` → `mm_g1_gamma` | `mm_g1_similarity.csv` |
| IV Fig. 7 (T-s map) | `IV/C` | `fig14_ts_map.py` → `mm_ts_map` | — |
| Fig. 3 (experiment validation) | `II/C` | `fig03_experiment_validation.py` | `fig03.csv` |
| Fig. 4 (CFD single-point check) | `II/C` | `fig04_cfd_check.py` | `fig04.csv` |
| Fig. 5 (M2, ΔP vs θ) | `III/A` | `fig05_mm_sweep.py` | `fig05.csv` |
| Fig. 6 (Γ(M) along the isentrope) | `III/C` | `gamma_paths.py` | `gamma_paths.json` |
| Fig. 7 (M2 vs Γ path) | `III/C` | `gamma_summary.py` | `gamma_summary.csv` |
| Fig. 8–11 (Zt similarity) | `IV/A` | `fig08_zt_similarity.py` | `fig08.csv` |
| Fig. 12–14 (Γ1 test) | `IV/B` | `fig12_gamma1_test.py` | `fig12.csv` |
| Fig. 15–20 (fluid classes) | `V/A`,`V/B` | `fig15_complex.py`, `fig18_simple.py` | … |
| Fig. 21 (classification) | `V/C` | `fig21_classes.py` | `fig21.csv` |

*Figure numbers follow the restructured manuscript and will be updated when the layout is frozen.*

## Data policy

- Inputs in `data/` are either published values (with the source cited in a header comment) or
  values computed by the scripts themselves.
- Experimental points taken from Gajoni et al. (2026, *JFM* **1028**, A41) are **digitised** from the
  published figures unless the authors provide the raw data; digitised points are marked as such in
  the CSV and in the caption.
- Third-party data are redistributed only if the original licence allows it.

## Tags

Tag the repository with the version of the manuscript it supports, e.g. `v1.0-submission`,
and cite the Zenodo DOI of that tag in the Data Availability Statement.
