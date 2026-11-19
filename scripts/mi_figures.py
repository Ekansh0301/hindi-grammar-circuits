#!/usr/bin/env python3
"""Figures for step 4, built locally from the pulled outputs (course_runs/outputs/, or --out-dir). numpy, csv and
matplotlib only (the local Python has no pandas). Every number on a figure is computed here from an output file,
and figures/README.md lists each figure with the files and checksums it was built from. A figure whose inputs are
missing is skipped and said to be.

Conventions (as in the thesis figures): colour does one job per figure. A model is always the same hue (MuRIL
blue, XLM-R-large green); a signed share uses a diverging map centred on zero; a bar is a magnitude from zero and
nothing else; a comparison against random sets is a strip of the random sets with the circuit as one dark mark.

  f1  component maps: share of the gap restored by patching each head (layer x head) and each MLP, object task,
      one panel per model (exact stage)
  f2  where the top components act: share restored at each position class alone, top 10, object task
  f3  A0: the intervening-subject contrast (OSV minus SOV, bits) with nothing masked and with the object, subject
      or ne masked, per model, with sign-flip p
  f4  attention from the verb to the object and to the subject, OSV-type against SOV-type, top heads (A4)
  f5  validation: the head circuit against the random head sets, faithfulness and necessity, per task and model
  f6  word order: share restored by the top 10 components at each site (W3)
  f7  screen against exact: attribution-patching share against exact share, every component, object task
"""
import argparse
import csv
import hashlib
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import TwoSlopeNorm  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODELS = {"muril": ("MuRIL", "#2A78D6"), "xlmrlarge": ("XLM-R-large", "#1BAF7A")}
INK, MUTED, FAINT = "#1C2333", "#6B7385", "#D9DDE5"
plt.rcParams.update({"font.family": ["Inter", "Noto Sans Devanagari", "DejaVu Sans"], "font.size": 9,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
USED = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:16]


def npz(out, name, fig):
    p = out / name
    if not p.exists():
        return None
    USED.setdefault(fig, []).append((p.name, sha(p)))
    return np.load(p, allow_pickle=False)


def rows(out, name, fig):
    p = out / name
    if not p.exists():
        return None
    USED.setdefault(fig, []).append((p.name, sha(p)))
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def keep_share(x, fc, fx, min_gap):
    """Ratio of sums of (x - fx) over (fc - fx), items with |fc - fx| > min_gap; x may be (items, ...)."""
    k = np.abs(fc - fx) > min_gap
    d = (fc - fx)[k].sum()
    return (x[k] - fx[k].reshape((-1,) + (1,) * (x.ndim - 1))).sum(0) / d


def parse(name):
    if "MLP" in name:
        return ("mlp", int(name[1:].split("MLP")[0]), None)
    l, h = name[1:].split("H")
    return ("head", int(l), int(h))


def save(fig, figdir, name, caption, made):
    for ext in ("png", "pdf"):
        fig.savefig(figdir / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    made.append((name, caption, list(USED.get(name.split("_")[0], []))))


def f1(out, figdir, made, mg):
    panels = [(m, npz(out, f"exact_object_{m}.npz", "f1")) for m in MODELS]
    panels = [(m, e) for m, e in panels if e is not None]
    if not panels:
        return
    fig, axes = plt.subplots(1, len(panels), figsize=(5.2 * len(panels), 3.8), squeeze=False, layout="constrained")
    cap = []
    for ax, (m, e) in zip(axes[0], panels):
        share = keep_share(e["exact"], e["f_clean"], e["f_corrupt"], mg)
        comps = [parse(str(c)) for c in e["comps"]]
        L = max(c[1] for c in comps) + 1
        H = max(c[2] for c in comps if c[0] == "head") + 1
        grid = np.full((L, H + 1), np.nan)
        for c, s in zip(comps, share):
            grid[c[1], c[2] if c[0] == "head" else H] = s
        lim = float(np.nanmax(np.abs(grid))) if np.isfinite(grid).any() else 1.0
        lim = lim if lim > 0 else 1.0
        im = ax.imshow(grid, aspect="auto", origin="lower", cmap="RdBu_r", norm=TwoSlopeNorm(0, -lim, lim))
        ax.axvline(H - 0.5, color="white", lw=2)
        ax.set_xticks(list(range(0, H, max(1, H // 6))) + [H])
        ax.set_xticklabels([str(h) for h in range(0, H, max(1, H // 6))] + ["MLP"])
        ax.set_xlabel("head")
        ax.set_ylabel("block")
        ax.set_title(MODELS[m][0], color=MODELS[m][1], loc="left", fontweight="bold")
        fig.colorbar(im, ax=ax, shrink=0.8, label="share of the gap restored")
        best = int(np.nanargmax(share))
        cap.append(f"{MODELS[m][0]}: largest {str(e['comps'][best])} ({share[best]:.2f}), {len(e['ids'])} orders")
    save(fig, figdir, "f1_component_maps_object", "Share of the object-masking gap restored by patching one component "
         "at every position (selection half). " + "; ".join(cap) + ".", made)


def f2(out, figdir, made, mg):
    panels = [(m, npz(out, f"exact_object_{m}.npz", "f2")) for m in MODELS]
    panels = [(m, e) for m, e in panels if e is not None and "by_class" in e]
    if not panels:
        return
    fig, axes = plt.subplots(1, len(panels), figsize=(5.0 * len(panels), 3.6), squeeze=False, layout="constrained")
    for ax, (m, e) in zip(axes[0], panels):
        top = list(e["top"])[:10]
        names = [str(e["comps"][j]) for j in top]
        cls = [str(c) for c in e["classes"]]
        bc = keep_share(e["by_class"][:, :10], e["f_clean"], e["f_corrupt"], mg)   # (10, classes)
        lim = float(np.nanmax(np.abs(bc))) if np.isfinite(bc).any() else 1.0
        lim = lim if lim > 0 else 1.0
        im = ax.imshow(bc, aspect="auto", cmap="RdBu_r", norm=TwoSlopeNorm(0, -lim, lim))
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.set_xticks(range(len(cls)))
        ax.set_xticklabels(cls, rotation=35, ha="right")
        ax.set_title(MODELS[m][0], color=MODELS[m][1], loc="left", fontweight="bold")
        fig.colorbar(im, ax=ax, shrink=0.8, label="share restored, that class only")
    save(fig, figdir, "f2_where_components_act", "Top 10 components of the object task, each patched at one position "
         "class at a time (selection half).", made)


def contrast(rs, value):
    """The baseline's gap-matched contrast, recomputed from per-order rows (variants, object not adjacent)."""
    cells = {}
    for r in rs:
        if r["is_reference"] == "True" or r["object_adjacent"] == "True" or r.get(value) in ("", None):
            continue
        key = (r["ref_id"], r["clause_head"], r["object_verb_gap"])
        cells.setdefault(key, {"OSV": [], "SOV": []})[r["order_class"]].append(float(r[value]))
    per_clause = {}
    for (rid, h, _), v in cells.items():
        if v["OSV"] and v["SOV"]:
            per_clause.setdefault((rid, h), []).append(np.mean(v["OSV"]) - np.mean(v["SOV"]))
    return [np.mean(v) for v in per_clause.values()]


def f3(out, figdir, made, mg):
    data = {m: rows(out, f"metric_{m}.csv", "f3") for m in MODELS}
    data = {m: d for m, d in data.items() if d}
    if not data:
        return
    conds = [("M_none", "nothing masked"), ("M_obj", "object masked"), ("M_subj", "subject masked"), ("M_ne", "ne masked")]
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    for k, (m, d) in enumerate(data.items()):
        for i, (c, lab) in enumerate(conds):
            v = contrast(d, c)
            if not v:
                continue
            mu = float(np.mean(v))
            y = i + (k - 0.5 * (len(data) - 1)) * 0.25
            ax.plot([0, mu], [y, y], color=MODELS[m][1], lw=2)
            ax.plot(mu, y, "o", color=MODELS[m][1], ms=5)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_yticks(range(len(conds)))
    ax.set_yticklabels([l for _, l in conds])
    ax.invert_yaxis()
    ax.set_xlabel("OSV-type minus SOV-type agreement margin (bits), gap-matched")
    for m in data:
        ax.plot([], [], color=MODELS[m][1], lw=2, label=MODELS[m][0])
    ax.legend(frameon=False, loc="lower left")
    save(fig, figdir, "f3_intervening_subject_by_masking", "The intervening-subject contrast of the agreement margin with "
         "nothing, the object, the subject or ne masked (all orders; p in the metric records).", made)


def f4(out, figdir, made, mg):
    data = {m: rows(out, f"attention_{m}.csv", "f4") for m in MODELS}
    data = {m: d for m, d in data.items() if d}
    if not data:
        return
    fig, axes = plt.subplots(1, len(data), figsize=(4.6 * len(data), 3.0), squeeze=False, layout="constrained")
    for ax, (m, d) in zip(axes[0], data.items()):
        heads = [k[len("subject_"):] for k in d[0] if k.startswith("subject_")]
        for i, h in enumerate(heads):
            for j, (to, mk) in enumerate((("object", "s"), ("subject", "o"))):
                v = contrast(d, f"{to}_{h}")          # the stage's statistic: gap-matched, mean per clause
                if not v:
                    continue
                y = i + (j - 0.5) * 0.3
                mu = float(np.mean(v))
                ax.plot([0, mu], [y, y], color=MODELS[m][1], lw=1.5, alpha=0.6)
                ax.plot(mu, y, mk, color=MODELS[m][1], ms=5)
        ax.axvline(0, color=MUTED, lw=0.8)
        ax.set_yticks(range(len(heads)))
        ax.set_yticklabels(heads)
        ax.invert_yaxis()
        ax.set_xlabel("attention share from the verb,\nOSV-type minus SOV-type (gap-matched)")
        ax.set_title(MODELS[m][0], color=MODELS[m][1], loc="left", fontweight="bold")
    axes[0][0].plot([], [], "s", color=MUTED, label="to the object")
    axes[0][0].plot([], [], "o", color=MUTED, label="to the subject")
    axes[0][0].legend(frameon=False, fontsize=8)
    save(fig, figdir, "f4_attention_osv_sov", "Change in attention from the scored verb position to the object and to the "
         "subject when the subject intervenes (OSV-type minus SOV-type, gap-matched, mean per clause, as the attention "
         "record), top 5 heads of the object task and the mean over all heads; p in the record. Descriptive: the "
         "subject is nearer the verb in OSV-type orders.", made)


def f5(out, figdir, made, mg):
    files = [(f"validate_object_{m}.npz", f"{MODELS[m][0]}, object") for m in MODELS] + \
            [("validate_contrast_muril.npz", "MuRIL, attraction")] + \
            [(f"validate_wordorder_{m}.npz", f"{MODELS[m][0]}, word order") for m in MODELS]
    got = [(lab, npz(out, f, "f5"), f) for f, lab in files]
    got = [g for g in got if g[1] is not None]
    if not got:
        return
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 0.55 * len(got) + 1.2), sharey=True, layout="constrained")
    for i, (lab, v, f) in enumerate(got):
        fc, fx = v["f_clean"], v["f_corrupt"]
        k = np.abs(fc - fx) > mg
        gap = (fc - fx)[k].sum()
        faith = (v["faith"][k] - fx[k][:, None]).sum(0) / gap
        if "contrast" in f or "wordorder" in f:
            lost = (fc - fx)[k][:, None] - (v["nec_clean"][k] - v["nec_corrupt"][k])
        else:
            lost = fc[k][:, None] - v["nec_clean"][k]
        nec = lost.sum(0) / gap
        for ax, sh in zip(axes, (faith, nec)):
            ax.plot(sh[1:], np.full(len(sh) - 1, i) + np.random.default_rng(i).uniform(-0.15, 0.15, len(sh) - 1),
                    "|", color=MUTED, alpha=0.5, ms=9)
            ax.plot(sh[0], i, "D", color=INK, ms=6)
    axes[0].set_yticks(range(len(got)))
    axes[0].set_yticklabels([g[0] for g in got])
    axes[0].invert_yaxis()
    axes[0].set_xlabel("faithfulness: share restored by the circuit alone")
    axes[1].set_xlabel("necessity: share lost when it is ablated")
    for ax in axes:
        ax.axvline(0, color=MUTED, lw=0.8)
    save(fig, figdir, "f5_validation", "Held-out half: the circuit (dark diamond) against the matched random sets (grey "
         "ticks); rank and sign-flip p in the validate records.", made)


def f6(out, figdir, made, mg):
    panels = [(m, npz(out, f"sites_wordorder_{m}.npz", "f6")) for m in MODELS]
    panels = [(m, e) for m, e in panels if e is not None]
    if not panels:
        return
    fig, axes = plt.subplots(1, len(panels), figsize=(4.8 * len(panels), 3.4), squeeze=False, layout="constrained")
    for ax, (m, e) in zip(axes[0], panels):
        sh = keep_share(e["sites"], e["f_clean"], e["f_corrupt"], mg)
        lim = float(np.nanmax(np.abs(sh))) if np.isfinite(sh).any() else 1.0
        lim = lim if lim > 0 else 1.0
        im = ax.imshow(sh, aspect="auto", cmap="RdBu_r", norm=TwoSlopeNorm(0, -lim, lim))
        ax.set_yticks(range(len(e["comps"])))
        ax.set_yticklabels([str(c) for c in e["comps"]])
        ax.set_xticks(range(len(e["classes"])))
        ax.set_xticklabels([str(c).replace("_", " ") for c in e["classes"]], rotation=35, ha="right")
        ax.set_title(MODELS[m][0], color=MODELS[m][1], loc="left", fontweight="bold")
        fig.colorbar(im, ax=ax, shrink=0.8, label="share of the order gap restored")
    save(fig, figdir, "f6_wordorder_sites", "Top 5 heads and top 5 MLPs of the word-order exact stage, each patched at "
         "one site at a time (selection half).", made)


def f7(out, figdir, made, mg):
    pts = []
    for m in MODELS:
        n0 = len(USED.get("f7", []))
        s, e = npz(out, f"screen_object_{m}.npz", "f7"), npz(out, f"exact_object_{m}.npz", "f7")
        if s is None or e is None or list(s["ids"]) != list(e["ids"]):
            USED["f7"] = USED.get("f7", [])[:n0]          # not used: not listed as a source
            continue
        a = keep_share(s["atp"].sum(2) + s["f_corrupt"][:, None], s["f_clean"], s["f_corrupt"], mg)
        x = keep_share(e["exact"], e["f_clean"], e["f_corrupt"], mg)
        pts.append((m, a, x))
    if not pts:
        return
    fig, ax = plt.subplots(figsize=(4.0, 3.6))
    cap = []
    for m, a, x in pts:
        ax.plot(a, x, "o", color=MODELS[m][1], ms=3, alpha=0.7, label=MODELS[m][0])
        r = spearmanr(a, x).correlation
        cap.append(f"{MODELS[m][0]} Spearman {r:.2f}")
    lo = min(min(a.min(), x.min()) for _, a, x in pts)
    hi = max(max(a.max(), x.max()) for _, a, x in pts)
    ax.plot([lo, hi], [lo, hi], color=FAINT, lw=1, zorder=0)
    ax.set_xlabel("screened share (attribution patching)")
    ax.set_ylabel("exact share")
    ax.legend(frameon=False)
    save(fig, figdir, "f7_screen_vs_exact", "Every head and MLP, object task: the first-order screen against exact "
         "patching; " + "; ".join(cap) + ".", made)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=str(ROOT / "course_runs" / "outputs"))
    ap.add_argument("--fig-dir", default=str(ROOT / "course_runs" / "figures"))
    ap.add_argument("--min-gap", type=float, default=0.05)
    args = ap.parse_args()
    out, figdir = Path(args.out_dir), Path(args.fig_dir)
    figdir.mkdir(parents=True, exist_ok=True)
    made = []
    for f in (f1, f2, f3, f4, f5, f6, f7):
        f(out, figdir, made, args.min_gap)
    lines = ["# Step 4 figures", "", f"Built by `scripts/mi_figures.py` from `{out}`.", "",
             "| figure | caption | built from (sha256) |", "|---|---|---|"]
    for name, cap, used in made:
        src = ", ".join(f"`{n}` `{h}`" for n, h in used)
        lines.append(f"| `{name}` | {cap} | {src} |")
    missing = [f.__name__ for f in (f1, f2, f3, f4, f5, f6, f7) if not any(n.startswith(f.__name__ + "_") for n, _, _ in made)]
    if missing:
        lines += ["", f"Not built (inputs missing): {', '.join(missing)}."]
    (figdir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(made)} figures -> {figdir}" + (f"; not built: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
