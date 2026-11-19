#!/usr/bin/env python3
"""Figures for the follow-up experiments (docs/FOLLOWUP_EXPERIMENTS.md), built locally from the pulled outputs.
numpy and matplotlib only. Every number on a figure is computed here from an output file; figures/README_followup.md
lists each figure with the files and checksums it was built from. Conventions as mi_figures.py: a model is always
the same hue (MuRIL blue, XLM-R-large green); a difference or an estimate with an interval is a dot with a whisker,
never a bar; intervals are document bootstraps (2,000, seed 707; descriptive).

  f8   reordering size: share of the gap restored by the 10 heads, and by the 5 MLPs together, per size group
  f9   case-marker control: word order (gap kept after deleting other words minus after deleting the markers) and
       agreement (mean margin as written, with ne deleted, with an unrelated word deleted)
  f10  halves swapped: faithfulness of the 10-head circuit chosen on the selection half and validated on the
       held-out half (step 4), and chosen on the held-out half and validated on the selection half
"""
import csv
import hashlib
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "course_runs" / "outputs"
FIG = ROOT / "course_runs" / "figures"
MODELS = {"muril": ("MuRIL", "#2A78D6"), "xlmrlarge": ("XLM-R-large", "#1BAF7A")}
INK, MUTED, FAINT = "#1C2333", "#6B7385", "#D9DDE5"
MIN_GAP = 0.05
plt.rcParams.update({"font.family": ["Inter", "Noto Sans Devanagari", "DejaVu Sans"], "font.size": 9,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})
USED = {}
GROUPS = [("1", lambda k: k == 1), ("2-3", lambda k: 2 <= k <= 3), ("4+", lambda k: k >= 4)]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:16]


def load(name, fig):
    p = OUT / name
    USED.setdefault(fig, []).append((p.name, sha(p)))
    return np.load(p) if name.endswith(".npz") else p


def doc_index(docs):
    u = sorted(set(docs.tolist()))
    m = {k: i for i, k in enumerate(u)}
    return np.array([m[d] for d in docs]), len(u)


def boot_ratio(num, den, docs, B=2000, seed=707):
    idx, n = doc_index(np.asarray(docs))
    ns, ds = np.zeros(n), np.zeros(n)
    np.add.at(ns, idx, num)
    np.add.at(ds, idx, den)
    pick = np.random.default_rng(seed).integers(0, n, size=(B, n))
    r = ns[pick].sum(1) / ds[pick].sum(1)
    return float(ns.sum() / ds.sum()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def boot_mean(v, docs, B=2000, seed=707):
    v = np.asarray(v, float)
    idx, n = doc_index(np.asarray(docs))
    s, c = np.zeros(n), np.zeros(n)
    np.add.at(s, idx, v)
    np.add.at(c, idx, 1.0)
    pick = np.random.default_rng(seed).integers(0, n, size=(B, n))
    r = s[pick].sum(1) / c[pick].sum(1)
    return float(v.mean()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def dot(ax, x, est, lo, hi, color, filled=True, size=5):
    ax.plot([x, x], [lo, hi], color=color, lw=1.4, solid_capstyle="round", zorder=2)
    ax.plot([x], [est], "o", color=color, mfc=color if filled else "white", mew=1.4, ms=size, zorder=3)


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    print("wrote", name)


def f8():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for ax, (j, title) in zip(axes, ((0, "the 10 heads"), (6, "the 5 MLPs together"))):
        for off, (m, (lab, col)) in zip((-0.07, 0.07), MODELS.items()):
            z = load(f"size_wordorder_{m}.npz", "f8")
            fc, fx, res, kend, docs = z["f_clean"], z["f_corrupt"], z["res"], z["kendall"], z["docs"]
            gap = fc - fx
            keep = np.abs(gap) > MIN_GAP
            for x, (name, fn) in enumerate(GROUPS):
                g = keep & np.array([fn(k) for k in kend])
                est, lo, hi = boot_ratio((res[:, j] - fx)[g], gap[g], docs[g])
                dot(ax, x + off, est, lo, hi, col)
        ax.set_xticks(range(3))
        ax.set_xticklabels([g[0] for g in GROUPS])
        ax.set_xlim(-0.5, 2.5)
        ax.set_xlabel("phrase pairs swapped")
        ax.set_title(f"share of the gap restored by {title}", fontsize=9, color=INK, loc="left")
        ax.axhline(1, color=FAINT, lw=0.8, zorder=0)
        ax.axhline(0, color=FAINT, lw=0.8, zorder=0)
    axes[0].set_ylabel("share of the gap restored")
    axes[0].set_ylim(0, 1.25)
    for (m, (lab, col)), y in zip(MODELS.items(), (0.12, 0.04)):
        axes[1].text(2.45, y, lab, color=col, ha="right", fontsize=8, fontweight="bold")
    save(fig, "f8_reordering_size")


def f9():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1, 1.5]})
    ax = axes[0]
    for x, (m, (lab, col)) in enumerate(MODELS.items()):
        z = load(f"case_wordorder_{m}.npz", "f9")
        d = (z["ctl_f_clean"] - z["ctl_f_corrupt"]) - (z["psp_f_clean"] - z["psp_f_corrupt"])
        est, lo, hi = boot_mean(d, z["docs"])
        dot(ax, x, est, lo, hi, col)
    ax.axhline(0, color=MUTED, lw=0.8, zorder=0)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([v[0] for v in MODELS.values()])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylabel("bits")
    ax.set_title("word order: gap kept after deleting other words,\nminus after deleting the case markers", fontsize=8.5, color=INK, loc="left")
    ax = axes[1]
    labels = ["as written", "ne deleted", "unrelated\nword deleted"]
    for off, (m, (lab, col)) in zip((-0.07, 0.07), MODELS.items()):
        p = load(f"case_agreement_{m}.csv", "f9")
        with open(p, newline="", encoding="utf-8") as f:
            r = list(csv.DictReader(f))
        docs = np.array([x["doc"] for x in r])
        for x, c in enumerate(("none", "ne", "ctl")):
            est, lo, hi = boot_mean([float(y[f"M_{c}"]) for y in r], docs)
            dot(ax, x + off, est, lo, hi, col)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(0, 8.5)
    ax.set_ylabel("agreement margin (bits)")
    ax.set_title("agreement: mean margin for the object-agreeing verb", fontsize=8.5, color=INK, loc="left")
    for (m, (lab, col)), y in zip(MODELS.items(), (0.9, 0.3)):
        ax.text(2.45, y, lab, color=col, ha="right", fontsize=8, fontweight="bold")
    fig.tight_layout()
    save(fig, "f9_case_marker_control")


def f10():
    cells = [("object", "agreement"), ("wordorder", "word order")]
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    y = 0
    ticks, labs = [], []
    for task, tl in cells:
        for m, (lab, col) in MODELS.items():
            for off, (src, filled) in zip((0.12, -0.12), ((f"validate_{task}_{m}.npz", True), (f"swap/validate_{task}_{m}.npz", False))):
                z = load(src, "f10")
                fc, fx, docs = z["f_clean"], z["f_corrupt"], z["docs"]
                gap = fc - fx
                k = np.abs(gap) > MIN_GAP
                est, lo, hi = boot_ratio((z["faith"][:, 0] - fx)[k], gap[k], docs[k])
                ax.plot([lo, hi], [y + off] * 2, color=col, lw=1.4, solid_capstyle="round")
                ax.plot([est], [y + off], "o", color=col, mfc=col if filled else "white", mew=1.4, ms=5)
            ticks.append(y)
            labs.append(f"{tl}, {lab}")
            y += 1
        y += 0.4
    ax.set_yticks(ticks)
    ax.set_yticklabels(labs)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("faithfulness: share of the gap restored by the 10 heads alone")
    ax.plot([], [], "o", color=INK, label="chosen on selection, validated on held-out (step 4)")
    ax.plot([], [], "o", color=INK, mfc="white", mew=1.4, label="chosen on held-out, validated on selection (swapped)")
    ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.4, -0.22))
    save(fig, "f10_halves_swapped")


CAPTIONS = {
    "f8_reordering_size": "Fresh word-order pairs (documents step 4 never read), by number of phrase pairs swapped: the share of the gap restored by the 10 frozen heads and by the 5 frozen MLPs together, with document-bootstrap 95% intervals (descriptive). The intervals of the 4+ group minus single swaps are in `mi_followup_size_<model>.md`.",
    "f9_case_marker_control": "Left: word order, the paired difference in the gap kept (bits) after deleting as many unmoved words minus after deleting the moved phrases' case markers; positive means the markers mattered more; interval is a document bootstrap, the test is in `mi_followup_case_wordorder_<model>.md`. Right: agreement, mean margin (bits) for the object-agreeing verb as written, with ne deleted, and with one unrelated word deleted (fresh orders).",
    "f10_halves_swapped": "Faithfulness of the 10-head circuit on the half it was not chosen on: step 4 (filled) against the halves swapped (open), per task and model, with document-bootstrap 95% intervals; the comparison is in `mi_swap_compare.md`.",
}


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    f8()
    f9()
    f10()
    lines = ["# Follow-up figures", "", "Built by `scripts/mi_figures_followup.py` from `course_runs/outputs`.", "",
             "| figure | caption | built from (sha256) |", "|---|---|---|"]
    for k, cap in CAPTIONS.items():
        fid = k.split("_")[0]
        src = ", ".join(f"`{n}` `{h}`" for n, h in USED.get(fid, []))
        lines.append(f"| `{k}` | {cap} | {src} |")
    (FIG / "README_followup.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
