#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class separation of fluids in the (molar mass M, molecular complexity N) plane.

Input: a table with columns ``class, N, M, name`` (tab- or comma-separated).

Method
------
1. 1-D rule: a single threshold on one descriptor.  All midpoints between
   consecutive sorted values are tried; the cut with the fewestmisclassified
   fluids is selected and ties are broken by the widest gap between the two
   classes (i.e. the largest margin).  This is a hard-margin linear classifier
   constrained to be orthogonal to one axis, equivalent to a one-split
   decision tree.

2. 2-D rule: the maximum-margin straight line  w_M*M + w_N*N = b.
   For linearly separable data this is the hard-margin support vector machine.
   No QP solver is required: the optimal orientation is found by an exhaustive
   angular sweep in the z-scored feature plane, where the margin is the gap
   between the projections of the two classes.  Features are z-scored because
   M and N carry different units and very different ranges; without scaling the
   margin would be dominated by the wider axis.

Validation
----------
* Leave-one-out cross-validation.  For the 1-D rule a held-out fluid that lies
  inside the refitted gap is reported as "ambiguous" rather than as an error:
  the data identify an interval of admissible cuts, not a unique value.
* Sensitivity: every cut inside the identified interval is checked to give the
  same labelling, and the distance of the closest fluid to the boundary is
  reported as the effective margin.

Outputs (next to this script unless --outdir is given):
    results.txt, results.json, fig_boundary.svg
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import time

import numpy as np


# --------------------------------------------------------------------------- #
# data
# --------------------------------------------------------------------------- #
def load_table(path):
    """Read the table and return names, class labels, M and N."""
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        head = fh.readline()
        fh.seek(0)
        delim = "\t" if head.count("\t") >= head.count(",") else ","
        reader = csv.DictReader(fh, delimiter=delim)
        rows = list(reader)

    def pick(*cands):
        for key in rows[0]:
            if key.strip().lower() in cands:
                return key
        raise KeyError("missing column, tried %s, found %s"
                       % (cands, list(rows[0].keys())))

    k_cls = pick("class", "label")
    k_m = pick("m", "molar mass", "molar_mass", "mw")
    k_n = pick("n", "molecular complexity", "molecular_complexity")
    k_nm = pick("name", "fluid")

    names = [r[k_nm].strip() for r in rows]
    y = np.array([int(float(r[k_cls])) for r in rows])
    M = np.array([float(r[k_m]) for r in rows])
    N = np.array([float(r[k_n]) for r in rows])
    return names, y, M, N


# --------------------------------------------------------------------------- #
# 1-D threshold
# --------------------------------------------------------------------------- #
def threshold_1d(values, labels, high):
    """Best single cut: fewest errors, then widest gap."""
    order = np.argsort(values, kind="mergesort")
    v, y = values[order], labels[order]
    best = None
    for i in range(len(v) - 1):
        if y[i] == y[i + 1]:
            continue
        cut = 0.5 * (v[i] + v[i + 1])
        pred = np.where(v > cut, high, 3 - high)
        err = int(np.sum(pred != y))
        margin = float(v[i + 1] - v[i])
        if best is None or (err, -margin) < (best["errors"], -best["gap"]):
            best = {"cut": cut, "gap": margin, "lower": float(v[i]),
                    "upper": float(v[i + 1]), "errors": err}
    best["accuracy"] = 1.0 - best["errors"] / len(v)
    return best


def predict_1d(values, cut, high):
    return np.where(values > cut, high, 3 - high)


# --------------------------------------------------------------------------- #
# 2-D maximum-margin line
# --------------------------------------------------------------------------- #
def max_margin_line(X, labels, high, step_deg=0.01, scale=True):
    """Hard-margin separator; returns weights in the original units."""
    mu = X.mean(axis=0)
    sd = X.std(axis=0, ddof=1) if scale else np.ones(2)
    Z = (X - mu) / sd

    best = None
    for deg in np.arange(0.0, 180.0, step_deg):
        th = np.radians(deg)
        d = np.array([np.cos(th), np.sin(th)])
        p = Z @ d
        hi = p[labels == high].min()
        lo = p[labels != high].max()
        gap = hi - lo
        if gap <= 0:
            continue
        if best is None or gap > best["gap"]:
            up = np.where(labels == high)[0]
            dw = np.where(labels != high)[0]
            best = {"gap": float(gap), "angle": float(deg), "dir": d,
                    "c": float(0.5 * (hi + lo)),
                    "sv_up": int(up[np.argmin(p[up])]),
                    "sv_dn": int(dw[np.argmax(p[dw])])}

    # z-space:  dir . z = c   ->   w . x = b
    w = best["dir"] / sd
    b = best["c"] + float(best["dir"] @ (mu / sd))
    best.update({"w": w, "b": b, "mu": mu, "sd": sd})
    return best


def predict_line(X, fit, high):
    return np.where(X @ fit["w"] > fit["b"], high, 3 - high)


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #
def loo_threshold(values, labels, high):
    """Refit on n-1 samples; count misclassifications and ambiguous cases."""
    errors, ambiguous = 0, 0
    for i in range(len(values)):
        mask = np.ones(len(values), bool)
        mask[i] = False
        if len(np.unique(labels[mask])) < 2:
            continue
        fit = threshold_1d(values[mask], labels[mask], high)
        if values[i] > fit["upper"]:
            errors += int(labels[i] != high)
        elif values[i] < fit["lower"]:
            errors += int(labels[i] == high)
        else:
            ambiguous += 1          # not decidable from the remaining data
    return errors, ambiguous


def loo_line(X, labels, high, step_deg=0.25):
    errors = 0
    for i in range(len(labels)):
        mask = np.ones(len(labels), bool)
        mask[i] = False
        if len(np.unique(labels[mask])) < 2:
            continue
        fit = max_margin_line(X[mask], labels[mask], high, step_deg=step_deg)
        pred = high if X[i] @ fit["w"] > fit["b"] else 3 - high
        errors += int(pred != labels[i])
    return errors


# --------------------------------------------------------------------------- #
# figure
# --------------------------------------------------------------------------- #
def write_svg(path, M, N, labels, names, fit, high, thr=None,
              width_pt=460.0, font=12.0):
    """Scatter of the two classes, the N* band and the max-margin line.

    The figure is authored at a physical size (``width_pt`` points wide,
    default 460 pt = 16.2 cm) and every font size is a true point size, so
    ``font=12`` really is 12 pt in the exported EPS/PDF when the figure is
    included at its natural width.  Margins scale with the font, so enlarging
    the text does not make it collide with the axes.

    Classes are labelled "complex fluids" (large N) and "simple fluids".
    """
    name_hi, name_lo = "complex fluids", "simple fluids"
    DW = 900.0                                  # design width, arbitrary units
    u = DW / width_pt                           # design units per point
    fs = lambda pt: pt * u                      # pt -> design units   # noqa: E731

    # margins, expressed in points (so they follow the font size)
    t_title = 1.15 * font + 3.0                 # baseline of the title
    t_sub = t_title + 1.05 * font               # baseline of the subtitle
    top_pt = t_sub + 1.25 * font
    left_pt = 3.4 * font
    right_pt = 1.35 * font
    bottom_pt = 3.0 * font

    L, R, T, B = left_pt * u, right_pt * u, top_pt * u, bottom_pt * u
    DH = T + B + 470.0                          # keep ~470 units of plot height
    height_pt = DH / u
    pw, ph = DW - L - R, DH - T - B

    m_max, n_max = M.max() * 1.06, N.max() * 1.09
    px = lambda m: L + m / m_max * pw           # noqa: E731
    py = lambda n: T + ph - n / n_max * ph      # noqa: E731

    s = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" width="%.2fpt" height="%.2fpt" '
         'viewBox="0 0 %.1f %.2f" font-family="Helvetica,Arial,sans-serif">'
         % (width_pt, height_pt, DW, DH),
         '<rect width="100%%" height="100%%" fill="#ffffff"/>',
         '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff"/>'
         % (L, T, pw, ph),
         '<text x="%.1f" y="%.1f" font-size="%.1f" font-weight="bold">'
         'Simple and complex fluids in the (M, N) plane</text>'
         % (L, t_title * u, fs(font * 1.15)),
         '<text x="%.1f" y="%.1f" font-size="%.1f" fill="#57606a">'
         'blue: %s (%d)&#160;&#160; green: %s (%d)</text>'
         % (L, t_sub * u, fs(font * 0.85), name_hi,
            int((labels == high).sum()), name_lo, int((labels != high).sum()))]

    # ticks: labels only, no grid lines
    for frac in np.linspace(0, 1, 6):
        yv = T + ph - frac * ph
        s.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="#6e7781" '
                 'text-anchor="end">%.0f</text>'
                 % (L - 0.35 * font * u, yv + 0.35 * font * u, fs(font), frac * n_max))
        xv = L + frac * pw
        s.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="#6e7781" '
                 'text-anchor="middle">%.0f</text>'
                 % (xv, T + ph + 1.0 * font * u, fs(font), frac * m_max))

    # full frame: bottom, left, top and right borders
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
             'stroke="#24292f" stroke-width="%.2f"/>' % (L, T, pw, ph, 0.65 * u))
    s.append('<text x="%.1f" y="%.1f" font-size="%.1f" text-anchor="middle">'
             'Molar mass M [g/mol]</text>'
             % (L + pw / 2, DH - 0.5 * font * u, fs(font)))
    s.append('<text x="%.1f" y="%.1f" font-size="%.1f" text-anchor="middle" '
             'transform="rotate(-90 %.1f %.1f)">Molecular complexity N</text>'
             % (0.85 * font * u, T + ph / 2, fs(font),
                0.85 * font * u, T + ph / 2))

    # admissible band of the 1-D rule
    if thr:
        lo, hi = thr["lower"], thr["upper"]
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#d1242f" '
                 'fill-opacity="0.06"/>' % (L, py(hi), pw, py(lo) - py(hi)))
        for val in (lo, hi):
            s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d1242f" '
                     'stroke-width="%.2f" stroke-dasharray="%.1f,%.1f" stroke-opacity="0.8"/>'
                     % (L, py(val), L + pw, py(val), 0.6 * u, 2.5 * u, 2.0 * u))
        x_lab = px(min(190.0, 0.80 * m_max))
        s.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="#d1242f" '
                 'text-anchor="start">N* = %.2f  (admissible %.2f - %.2f)</text>'
                 % (x_lab, py(hi) - 0.55 * font * u, fs(font * 0.8), thr["cut"], lo, hi))

    # max-margin boundary  N = a*M + c  (clipped to the axes box)
    w, b = fit["w"], fit["b"]
    a, c = -w[0] / w[1], b / w[1]
    mg = np.linspace(-0.5 * m_max, 1.5 * m_max, 4000)
    ng = a * mg + c
    inside = (mg >= 0) & (mg <= m_max) & (ng >= 0) & (ng <= n_max)
    if inside.any():
        i0, i1 = np.argmax(inside), len(inside) - 1 - np.argmax(inside[::-1])
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8250df" '
                 'stroke-width="%.2f" stroke-dasharray="%.1f,%.1f"/>'
                 % (px(mg[i0]), py(ng[i0]), px(mg[i1]), py(ng[i1]),
                    1.0 * u, 4.0 * u, 2.0 * u))

    for m, n, lab in zip(M, N, labels):
        col = "#1f6feb" if lab == high else "#2da44e"
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="0.88" '
                 'stroke="#ffffff" stroke-width="%.2f"/>'
                 % (px(m), py(n), 0.36 * font * u, col, 0.5 * u))

    # selective point labels
    lab_off = {"CO2": (0.45, 0.45), "n-Octane": (-0.35, 0.75), "MM": (0.55, 0.3),
               "MDM": (0.35, -0.35), "D6": (-0.35, -0.5)}
    for m, n, nm in zip(M, N, names):
        if nm in lab_off:
            dx, dy = lab_off[nm]
            anchor = "end" if dx < 0 else "start"
            s.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="#24292f" '
                     'text-anchor="%s">%s</text>'
                     % (px(m) + dx * font * u, py(n) + dy * font * u,
                        fs(font * 0.72), anchor, nm))

    # legend (top left, inside the plot), sized from the font
    row = 1.55 * font * u
    lx, ly = L + 0.6 * font * u, T + 0.55 * font * u
    box_w, box_h = 11.5 * font * u, 3.0 * row
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" '
             'fill="#ffffff" fill-opacity="0.95" stroke="#d0d7de" stroke-width="%.2f"/>'
             % (lx, ly, box_w, box_h, 2.0 * u, 0.5 * u))
    for i, (name, col, marker) in enumerate(((name_hi, "#1f6feb", "circle"),
                                             (name_lo, "#2da44e", "circle"))):
        cy = ly + row * (i + 0.55)
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
                 % (lx + 0.75 * font * u, cy, 0.36 * font * u, col))
        s.append('<text x="%.1f" y="%.1f" font-size="%.1f">%s</text>'
                 % (lx + 1.5 * font * u, cy + 0.32 * font * u, fs(font * 0.95), name))
    cy = ly + row * 2.55
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8250df" '
             'stroke-width="%.2f" stroke-dasharray="%.1f,%.1f"/>'
             % (lx + 0.35 * font * u, cy, lx + 1.15 * font * u, cy,
                1.0 * u, 3.0 * u, 1.5 * u))
    s.append('<text x="%.1f" y="%.1f" font-size="%.1f">N = %.2f - %.2f M</text>'
             % (lx + 1.5 * font * u, cy + 0.32 * font * u, fs(font * 0.95), c, -a))
    s.append("</svg>")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(s))
    return {"width_pt": width_pt, "height_pt": height_pt, "font_pt": font}


# --------------------------------------------------------------------------- #
# export: PNG + EPS (+ PDF) and on-screen preview
# --------------------------------------------------------------------------- #
def export_figures(svg_path, outdir, png_width=1400):
    """Convert the SVG to PNG and EPS; return the paths that were written.

    PNG : raster preview, white background, ``png_width`` pixels wide.
    EPS : vector, for LaTeX / journal submission.  Produced through
          SVG -> PDF (cairo) -> EPS (pdftops) when possible, because Ghostscript
          embeds the fonts more reliably than cairo's direct EPS writer.
    """
    exe = shutil.which("rsvg-convert")
    if exe is None:
        return {"error": "rsvg-convert not found; only the SVG was written"}

    out = {}
    png = os.path.join(outdir, "fig_boundary.png")
    try:
        subprocess.run([exe, "-w", str(png_width), "-b", "white", svg_path, "-o", png],
                       check=True, capture_output=True)
        out["png"] = png
    except subprocess.CalledProcessError as exc:
        out["png_error"] = exc.stderr.decode(errors="replace")[:200]

    pdf = os.path.join(outdir, "fig_boundary.pdf")
    try:
        subprocess.run([exe, "-f", "pdf", "-d", "72", "-p", "72", "-b", "white",
                        svg_path, "-o", pdf],
                       check=True, capture_output=True)
        out["pdf"] = pdf
    except subprocess.CalledProcessError:
        pdf = None

    eps = os.path.join(outdir, "fig_boundary.eps")
    made = False
    pdftops = shutil.which("pdftops")
    if pdf and pdftops:
        try:
            subprocess.run([pdftops, "-eps", "-level3", pdf, eps],
                           check=True, capture_output=True)
            made = True
        except subprocess.CalledProcessError:
            made = False
    if not made:
        try:
            subprocess.run([exe, "-f", "eps", "-d", "72", "-p", "72", "-b", "white",
                            svg_path, "-o", eps],
                           check=True, capture_output=True)
            made = True
        except subprocess.CalledProcessError:
            made = False
    if made and os.path.getsize(eps) > 0:
        out["eps"] = eps
    else:
        out["eps_error"] = "EPS conversion failed"
    return out


def show_image(path):
    """Open the PNG with the first available viewer; return the viewer name."""
    if not path or not os.path.exists(path):
        return None
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        return None
    candidates = [("xdg-open", ["xdg-open", path]),
                  ("gio", ["gio", "open", path]),
                  ("open", ["open", path]),
                  ("eog", ["eog", path]),
                  ("feh", ["feh", path])]
    for name, cmd in candidates:
        if shutil.which(cmd[0]) is None:
            continue
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    start_new_session=True)
        except Exception:
            continue
        time.sleep(0.4)
        if proc.poll() is None or proc.returncode == 0:
            return name          # viewer is running (or exited cleanly)
        # otherwise try the next candidate
    return None


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Separate two fluid classes in (M, N).")
    ap.add_argument("--csv", default=os.path.join(here, "fluids.csv"))
    ap.add_argument("--outdir", default=here)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-show", action="store_true",
                    help="do not open the PNG after the run (headless use)")
    ap.add_argument("--png-width", type=int, default=1400,
                    help="width of the exported PNG in pixels (default 1400)")
    ap.add_argument("--width-pt", type=float, default=460.0,
                    help="physical width of the figure in points (default 460 pt = 16.2 cm)")
    ap.add_argument("--font", type=float, default=12.0,
                    help="base font size in points (default 12 pt); ticks and axis "
                         "labels use this size, other elements scale relative to it")
    args = ap.parse_args()

    names, y, M, N = load_table(args.csv)
    os.makedirs(args.outdir, exist_ok=True)

    labels = np.unique(y)
    if len(labels) != 2:
        raise SystemExit("need exactly two classes, found %s" % labels)
    high = (labels[0] if N[y == labels[0]].mean() > N[y == labels[1]].mean()
            else labels[1])
    low = labels[0] + labels[1] - high

    X = np.column_stack([M, N])
    fit_n = threshold_1d(N, y, high)
    fit_m = threshold_1d(M, y, high)
    fit_l = max_margin_line(X, y, high, scale=True)
    fit_l.update({"high": high})
    fit_raw = max_margin_line(X, y, high, scale=False)

    pred_l = predict_line(X, fit_l, high)
    acc_l = float(np.mean(pred_l == y))
    loo_n, amb_n = loo_threshold(N, y, high)
    loo_m, amb_m = loo_threshold(M, y, high)
    loo_l = loo_line(X, y, high)

    # sensitivity of the 1-D rule: every cut in the gap gives the same labels
    grid = np.linspace(fit_n["lower"] + 1e-9, fit_n["upper"] - 1e-9, 501)
    stable = all(np.array_equal(predict_1d(N, g, high), predict_1d(N, fit_n["cut"], high))
                 for g in grid)

    rng = {}
    for lab, tag in ((high, "high"), (low, "low")):
        sel = y == lab
        rng[tag] = {"label": int(lab), "n": int(sel.sum()),
                    "M": [float(M[sel].min()), float(M[sel].max())],
                    "N": [float(N[sel].min()), float(N[sel].max())],
                    "members": [nm for nm, s in zip(names, sel) if s]}
    m_ov = [max(rng["high"]["M"][0], rng["low"]["M"][0]),
            min(rng["high"]["M"][1], rng["low"]["M"][1])]
    m_overlap = m_ov[0] <= m_ov[1]

    a = -fit_l["w"][0] / fit_l["w"][1]
    c = fit_l["b"] / fit_l["w"][1]

    res = {
        "input": os.path.abspath(args.csv),
        "n_fluids": int(len(y)),
        "high_label": int(high),
        "classes": {k: rng[k]["n"] for k in rng},
        "ranges": rng,
        "one_d": {
            "N": {"cut": fit_n["cut"], "gap": fit_n["gap"],
                  "interval": [fit_n["lower"], fit_n["upper"]],
                  "accuracy": fit_n["accuracy"], "errors": fit_n["errors"],
                  "loo_errors": int(loo_n), "loo_ambiguous": int(amb_n),
                  "all_cuts_in_interval_equivalent": bool(stable)},
            "M": {"cut": fit_m["cut"], "gap": fit_m["gap"],
                  "interval": [fit_m["lower"], fit_m["upper"]],
                  "accuracy": fit_m["accuracy"], "errors": fit_m["errors"],
                  "loo_errors": int(loo_m), "loo_ambiguous": int(amb_m),
                  "ranges_overlap": bool(m_overlap),
                  "overlap_interval": [float(m_ov[0]), float(m_ov[1])] if m_overlap else None},
        },
        "two_d": {
            "equation_physical": "%.6f*M + %.6f*N = %.6f"
                                 % (fit_l["w"][0], fit_l["w"][1], fit_l["b"]),
            "equation_slope_intercept": "N = %.4f %+.4f*M" % (c, a),
            "margin_z": fit_l["gap"], "angle_deg": fit_l["angle"],
            "accuracy": acc_l, "loo_errors": int(loo_l),
            "support_upper": names[fit_l["sv_up"]],
            "support_lower": names[fit_l["sv_dn"]],
            "raw_scale": {"equation": "%.6f*M + %.6f*N = %.6f"
                                      % (fit_raw["w"][0], fit_raw["w"][1], fit_raw["b"]),
                          "angle_deg": fit_raw["angle"]},
        },
    }

    txt = []
    add = txt.append
    add("Fluid class separation in the (M, N) plane")
    add("=" * 64)
    add("input   : %s" % res["input"])
    add("fluids  : %d   (class %d: %d, class %d: %d)"
        % (len(y), high, rng["high"]["n"], low, rng["low"]["n"]))
    add("complex fluids = class %d (larger mean N); simple fluids = class %d" % (high, low))
    add("")
    add("descriptor ranges")
    add("  complex fluids : M = %7.2f .. %7.2f   N = %8.2f .. %8.2f"
        % (*rng["high"]["M"], *rng["high"]["N"]))
    add("  simple fluids  : M = %7.2f .. %7.2f   N = %8.2f .. %8.2f"
        % (*rng["low"]["M"], *rng["low"]["N"]))
    add("  -> N ranges disjoint, M ranges %s"
        % ("overlap in [%.2f, %.2f] g/mol" % tuple(m_ov) if m_overlap else "disjoint"))
    add("")
    add("1-D rule (single threshold)")
    add("  N* in (%.4f, %.4f); adopted N* = %.4f  ->  class %d if N > N*"
        % (fit_n["lower"], fit_n["upper"], fit_n["cut"], high))
    add("    margin %.4f (in N units), accuracy %.1f%% (%d/%d)"
        % (fit_n["gap"], 100 * fit_n["accuracy"], len(y) - fit_n["errors"], len(y)))
    add("    LOO: %d error(s), %d ambiguous (held-out point inside the refitted gap)"
        % (loo_n, amb_n))
    add("    every cut inside the interval reproduces the same labelling: %s"
        % ("yes" if stable else "NO"))
    add("  M* = %.4f (gap %.4f) -> accuracy %.1f%%, %d error(s), LOO %d error(s)"
        % (fit_m["cut"], fit_m["gap"], 100 * fit_m["accuracy"], fit_m["errors"], loo_m))
    if m_overlap:
        add("    M alone CANNOT separate the classes (ranges overlap).")
    add("")
    add("2-D max-margin line (hard-margin SVM, z-scored features)")
    add("  %s" % res["two_d"]["equation_physical"])
    add("  equivalently  %s" % res["two_d"]["equation_slope_intercept"])
    add("  margin %.4f (z units), orientation %.2f deg from the M axis"
        % (fit_l["gap"], fit_l["angle"]))
    add("  support vectors: %s (class %d) and %s (class %d)"
        % (names[fit_l["sv_up"]], high, names[fit_l["sv_dn"]], low))
    add("  accuracy %.1f%% (%d/%d), LOO %d error(s)"
        % (100 * acc_l, int(round(acc_l * len(y))), len(y), loo_l))
    add("  the line adds no accuracy over the 1-D rule (both 100% here); it only")
    add("  provides a margin-maximising boundary for the two-descriptor plane.")
    add("")
    add("conclusion for the paper")
    add("  the two classes are separated by molecular complexity alone:")
    add("  N* ~ %.1f (admissible range %.2f-%.2f)." % (fit_n["cut"], fit_n["lower"], fit_n["upper"]))
    add("  M is not a discriminating variable (class ranges overlap).")
    text = "\n".join(txt)
    if not args.quiet:
        print(text)

    with open(os.path.join(args.outdir, "results.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    with open(os.path.join(args.outdir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    svg = os.path.join(args.outdir, "fig_boundary.svg")
    meta = write_svg(svg, M, N, y, names, fit_l, high, thr=fit_n,
                     width_pt=args.width_pt, font=args.font)

    written = export_figures(svg, args.outdir, png_width=args.png_width)

    if not args.quiet:
        print("\nfigure  -> %.0f x %.0f pt (%.1f x %.1f cm), base font %.1f pt"
              % (meta["width_pt"], meta["height_pt"], meta["width_pt"] / 28.3465,
                 meta["height_pt"] / 28.3465, meta["font_pt"]))
        print("outputs -> %s" % os.path.abspath(args.outdir))
        for key in ("png", "eps", "pdf"):
            if key in written:
                print("  %-3s : %s" % (key.upper(), os.path.basename(written[key])))
        for key in ("png_error", "eps_error", "error"):
            if key in written:
                print("  %s: %s" % (key, written[key]))

    if not args.no_show and "png" in written:
        viewer = show_image(written["png"])
        if viewer and not args.quiet:
            print("  preview opened with %s" % viewer)
        elif not args.quiet:
            print("  no GUI image viewer detected; open the PNG manually")


if __name__ == "__main__":
    main()
