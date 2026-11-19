#!/usr/bin/env python3
"""Figures of the paper (paper/figures/). numpy and matplotlib only; reads course_runs/outputs where a figure needs data.

fig1_design   the two tasks side by side: the clean run, the corrupted run and the metric (no data)
fig2_components  top ten heads, head-set size, top five MLPs (word order)
fig3_agreement   what agreement reads: ko and bhi insertion, role swap, masked slot
fig4_wordorder   what word order reads: marker deletion against two controls, cue strata

usage: python3 scripts/mi_figures_paper.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

import sys  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mi_paper_numbers as N  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper" / "figures"

# colour-blind-safe palette (Okabe and Ito): one hue per phrase role, grey for the rest
BLUE, ORANGE, GREY, DARK = "#cfe3f3", "#f6d9c2", "#ececec", "#333333"
EDGE = "#555555"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 6.5, "pdf.fonttype": 42, "ps.fonttype": 42})


def box(ax, x, y, w, h, text, fill, size=6.5, dashed=False, style="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.003,rounding_size=0.015", fc=fill, ec=EDGE,
                                lw=0.6, ls=(0, (3, 2)) if dashed else "-"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=DARK, style=style)


def gloss(ax, x, w, y, text):
    ax.text(x + w / 2, y, text, ha="center", va="top", fontsize=5, color="#666666", style="italic")


def arrow(ax, x, y0, y1, label):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>", mutation_scale=7, lw=0.8, color=DARK))
    ax.text(x + 0.025, (y0 + y1) / 2, label, ha="left", va="center", fontsize=5.8, color=DARK)


def panel_word_order(ax):
    ax.set_title("(a) Word order", loc="left", fontsize=7.5, fontweight="bold", pad=2)
    ws = [0.215, 0.235, 0.285, 0.225]
    gap = 0.013
    xs = [0.0]
    for w in ws[:-1]:
        xs.append(xs[-1] + w + gap)
    h = 0.15
    y_clean, y_corr = 0.70, 0.26
    ax.text(0.0, y_clean + h + 0.045, "clean run: the written sentence", fontsize=6.5, fontweight="bold", va="bottom")
    ax.text(0.0, y_corr + h + 0.045, "corrupted run: its reordering", fontsize=6.5, fontweight="bold", va="bottom")
    clean = [("George ne", BLUE, "George-ERG"), ("aropon ko", ORANGE, "allegations-ACC"),
             ("sarasar galat", GREY, "utterly false"), ("bataya hai", GREY, "called")]
    order = [1, 0, 2, 3]
    for i, (t, c, g) in enumerate(clean):
        box(ax, xs[i], y_clean, ws[i], h, t, c)
        gloss(ax, xs[i], ws[i], y_clean - 0.012, g)
    # the reordered sentence: the first two phrases swap places (each keeps its colour)
    x = 0.0
    for k in order:
        t, c, g = clean[k]
        box(ax, x, y_corr, ws[k], h, t, c)
        gloss(ax, x, ws[k], y_corr - 0.012, g)
        x += ws[k] + gap
    arrow(ax, 0.50, 0.625, 0.545, "")
    ax.text(0.535, 0.585, "patch one head or one MLP output", fontsize=5.8, va="center")
    ax.text(0.0, 0.035, r"gap = surprisal(reordered) $-$ surprisal(written)", fontsize=6.3, va="center")
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0, 1)
    ax.axis("off")


def panel_agreement(ax):
    ax.set_title("(b) Agreement", loc="left", fontsize=7.5, fontweight="bold", pad=2)
    h = 0.15
    y_clean, y_corr = 0.70, 0.26
    ax.text(0.0, y_clean + h + 0.045, "clean run: the sentence as written", fontsize=6.5, fontweight="bold", va="bottom")
    ax.text(0.0, y_corr + h + 0.045, "corrupted run: the object masked", fontsize=6.5, fontweight="bold", va="bottom")
    xs = {"s": (0.0, 0.215), "o": (0.23, 0.26), "vc": (0.505, 0.215), "vw": (0.735, 0.215)}
    for y, obj_text, obj_fill, obj_hatch in ((y_clean, "kitaab", ORANGE, None), (y_corr, "[MASK]", "#f7f7f7", True)):
        box(ax, *xs["s"][:1], y, xs["s"][1], h, "Ram ne", BLUE)
        box(ax, xs["o"][0], y, xs["o"][1], h, obj_text, obj_fill, dashed=bool(obj_hatch))
        box(ax, xs["vc"][0], y, xs["vc"][1], h, "padhi", "#dcefd8")
        box(ax, xs["vw"][0], y, xs["vw"][1], h, "padha", GREY)
    gloss(ax, *xs["s"][:1], xs["s"][1], y_clean - 0.012, "Ram-ERG")
    gloss(ax, xs["o"][0], xs["o"][1], y_clean - 0.012, "book (f)")
    gloss(ax, xs["vc"][0], xs["vc"][1], y_clean - 0.012, "correct (f)")
    gloss(ax, xs["vw"][0], xs["vw"][1], y_clean - 0.012, "wrong (m)")
    arrow(ax, 0.30, 0.625, 0.545, "")
    ax.text(0.335, 0.585, "patch one head or one MLP output", fontsize=5.8, va="center")
    ax.text(0.0, 0.035, r"$M=\log_2 P(\mathrm{padhi})-\log_2 P(\mathrm{padha})$;  gap = $M_{\mathrm{clean}}-M_{\mathrm{masked}}$",
            fontsize=6.3, va="center")
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0, 1)
    ax.axis("off")


C_MODEL = {"muril": "#0072B2", "xlmrlarge": "#D55E00"}   # one colour per model in every figure
L_MODEL = {"muril": "MuRIL", "xlmrlarge": "XLM-R-large"}
GREYP = "#8a8a8a"


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2, width=0.5, labelsize=6)
    for s in ("left", "bottom"):
        ax.spines[s].set_linewidth(0.5)


def ci_pt(ax, x, v, lo, hi, color, marker, filled=True, size=3.6, lw=0.9):
    ax.errorbar([x], [v], yerr=[[v - lo], [hi - v]], fmt=marker, ms=size, color=color, mfc=color if filled else "white",
                mec=color, mew=0.9, elinewidth=lw, capsize=1.5, capthick=0.7, zorder=3)


def cell_panel(ax, cells, title, ymax=1.28):
    """Faithfulness (filled circle) and necessity (open square) of a set of components in four or two cells, with the
    comparison sets (grey: mean and 95th percentile)."""
    ax.set_title(title, loc="left", fontsize=6.8, fontweight="bold", pad=2)
    for i, (m, st) in enumerate(cells):
        for j, (key, mk, fill) in enumerate((("faithfulness", "o", True), ("necessity", "s", False))):
            x = i + (-0.17 if j == 0 else 0.17)
            v = st[key]
            ci_pt(ax, x, v["share"], v["ci"][0], v["ci"][1], C_MODEL[m], mk, fill)
            rm, rp = v["rand_mean"], v["rand_p95"]
            ax.plot([x + 0.0, x + 0.0], [rm, rp], color=GREYP, lw=2.2, alpha=0.55, solid_capstyle="butt", zorder=1)
            ax.plot([x], [rm], marker="_", ms=4, color="#555555", zorder=2)
    ax.axhline(1.0, color="#bbbbbb", lw=0.5, ls=":", zorder=0)
    ax.axhline(0.0, color="#bbbbbb", lw=0.5, zorder=0)
    ax.set_ylim(-0.1, ymax)
    ax.set_xlim(-0.6, len(cells) - 0.4)
    style(ax)


def fig2():
    num = N.main_numbers() if hasattr(N, "main_numbers") else None
    v = {t: {m: N.validate(t, m) for m in N.MODELS} for t in N.TASKS}
    ss = {t: {m: N.setsize(t, m) for m in N.MODELS} for t in N.TASKS}
    ml = {m: N.mlpsets("wordorder", m) for m in N.MODELS}
    fig = plt.figure(figsize=(6.3, 2.35))
    a = fig.add_axes([0.065, 0.20, 0.40, 0.58])
    b = fig.add_axes([0.55, 0.20, 0.20, 0.58])
    c = fig.add_axes([0.81, 0.20, 0.18, 0.58])
    cells = [("muril", v["object"]["muril"]), ("xlmrlarge", v["object"]["xlmrlarge"]),
             ("muril", v["wordorder"]["muril"]), ("xlmrlarge", v["wordorder"]["xlmrlarge"])]
    cell_panel(a, cells, "(a) Top ten heads")
    a.set_xticks(range(4))
    a.set_xticklabels(["MuRIL", "XLM-R", "MuRIL", "XLM-R"], fontsize=6)
    a.text(0.5, -0.24, "agreement", ha="center", fontsize=6.3, transform=a.get_xaxis_transform())
    a.text(2.5, -0.24, "word order", ha="center", fontsize=6.3, transform=a.get_xaxis_transform())
    a.set_ylabel("share of the gap", fontsize=6.5)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", ls="", color="#444444", ms=3.4, label="faithfulness"),
               Line2D([], [], marker="s", ls="", color="#444444", mfc="white", ms=3.4, label="necessity"),
               Line2D([], [], color=GREYP, lw=2.2, alpha=0.55, label="random or other sets: mean to 95th pct"),
               Line2D([], [], color="#444444", lw=0.9, ls="-", label="agreement (b)"),
               Line2D([], [], color="#444444", lw=0.9, ls="--", label="word order (b)")]
    fig.legend(handles=handles, loc="upper center", ncol=5, fontsize=5.6, frameon=False, bbox_to_anchor=(0.5, 1.01),
               handletextpad=0.3, columnspacing=1.0)
    # (b) necessity against head-set size
    b.set_title("(b) Necessity, top K heads", loc="left", fontsize=6.8, fontweight="bold", pad=2)
    Ks = [5, 10, 20, 40]
    for t, ls in (("object", "-"), ("wordorder", "--")):
        for m in N.MODELS:
            y = [ss[t][m][k]["necessity"]["share"] for k in Ks]
            lo = [ss[t][m][k]["necessity"]["ci"][0] for k in Ks]
            hi = [ss[t][m][k]["necessity"]["ci"][1] for k in Ks]
            off = -0.04 if m == "muril" else 0.04
            xs = np.arange(4) + off
            b.errorbar(xs, y, yerr=[np.array(y) - lo, np.array(hi) - y], color=C_MODEL[m], ls=ls, lw=0.9, marker="o" if t == "object" else "s",
                       ms=2.6, mfc="white", capsize=1.2, elinewidth=0.6)
    b.set_xticks(range(4))
    b.set_xticklabels([str(k) for k in Ks], fontsize=6)
    b.set_xlabel("top K heads", fontsize=6.3, labelpad=1)
    b.set_ylim(-0.1, 1.28)
    b.axhline(1.0, color="#bbbbbb", lw=0.5, ls=":")
    style(b)
    # (c) the top five MLPs, word order
    cm = [(m, {"faithfulness": {"share": ml[m]["faith"]["share"], "ci": ml[m]["faith"]["ci"], "rand_mean": ml[m]["faith"]["others_mean"],
                                 "rand_p95": ml[m]["faith"]["others_p95"]},
               "necessity": {"share": ml[m]["necessity"]["share"], "ci": ml[m]["necessity"]["ci"], "rand_mean": ml[m]["necessity"]["others_mean"],
                             "rand_p95": ml[m]["necessity"]["others_p95"]}}) for m in N.MODELS]
    cell_panel(c, cm, "(c) Top five MLPs")
    c.set_xticks(range(2))
    c.set_xticklabels(["MuRIL", "XLM-R"], fontsize=6)
    c.set_yticklabels([])
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig2_components.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


def fig3():
    ko = {m: N.ko(m) for m in N.MODELS}
    rs = {m: N.role_swap(m) for m in N.MODELS}
    mk = {m: N.swap_mask(m) for m in N.MODELS}
    fig = plt.figure(figsize=(6.3, 2.35))
    a = fig.add_axes([0.085, 0.20, 0.235, 0.58])
    b = fig.add_axes([0.415, 0.20, 0.235, 0.58])
    c = fig.add_axes([0.745, 0.20, 0.245, 0.58])
    # (a) inserting bhi or ko after the object: margin toward the object-agreeing form
    a.set_title("(a) Marker after the object", loc="left", fontsize=6.8, fontweight="bold", pad=2)
    for m in N.MODELS:
        off = -0.06 if m == "muril" else 0.06
        for i, v in enumerate(("none", "bhi", "ko")):
            mean, lo, hi = ko[m][v]["magree"]
            ci_pt(a, i + off, mean, lo, hi, C_MODEL[m], "o" if m == "muril" else "s", True, 3.4)
        a.plot(np.arange(3) + off, [ko[m][v]["magree"][0] for v in ("none", "bhi", "ko")], color=C_MODEL[m], lw=0.7, zorder=2)
    a.axhline(0, color="#999999", lw=0.5)
    a.set_xticks(range(3))
    a.set_xticklabels(["as written", "+ bhi", "+ ko"], fontsize=6)
    a.set_xlim(-0.5, 2.5)
    a.set_ylabel("margin toward the object-\nagreeing form (bits)", fontsize=5.8, labelpad=1)
    a.text(-0.45, -1.2, "below 0: default\nform preferred", fontsize=5.3, ha="left", va="top", color="#444444")
    style(a)
    # (b) role swap: margin toward the form that agrees with the bare noun, unswapped and swapped
    b.set_title("(b) Noun phrases swapped", loc="left", fontsize=6.8, fontweight="bold", pad=2)
    for m in N.MODELS:
        off = -0.09 if m == "muril" else 0.09
        for i, cls in enumerate(("SOV", "OSV")):
            r = rs[m][f"all_{cls}"]
            ci_pt(b, i + off, r["orig"][0], r["orig"][1], r["orig"][2], C_MODEL[m], "o" if m == "muril" else "s", False, 3.4)
            ci_pt(b, i + off, r["swap"][0], r["swap"][1], r["swap"][2], C_MODEL[m], "o" if m == "muril" else "s", True, 3.4)
    b.axhline(0, color="#999999", lw=0.5)
    b.set_xticks(range(2))
    b.set_xticklabels(["SOV-type", "OSV-type"], fontsize=6)
    b.set_xlim(-0.5, 1.5)
    b.set_ylabel("margin toward the bare\nnoun's form (bits)", fontsize=5.8, labelpad=1)
    style(b)
    # (c) masked slot after the swap
    c.set_title("(c) One slot masked", loc="left", fontsize=6.8, fontweight="bold", pad=2)
    conds = ("none", "obj", "subj")
    for m in N.MODELS:
        for cls, ls, mkr in (("SOV", "-", "o"), ("OSV", "--", "s")):
            vals = [mk[m][f"all_{cls}"][k] for k in conds]
            xs = np.arange(3) + (-0.05 if m == "muril" else 0.05)
            c.errorbar(xs, [v[0] for v in vals], yerr=[[v[0] - v[1] for v in vals], [v[2] - v[0] for v in vals]], color=C_MODEL[m],
                       ls=ls, lw=0.8, marker=mkr, ms=2.8, mfc=C_MODEL[m] if cls == "SOV" else "white", capsize=1.2, elinewidth=0.6)
    c.axhline(0, color="#999999", lw=0.5)
    c.set_xticks(range(3))
    c.set_xticklabels(["no noun\nmasked", "bare\nnoun", "ne-marked\nnoun"], fontsize=6)
    c.set_xlim(-0.4, 2.4)
    style(c)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", ls="", color=C_MODEL["muril"], ms=3.4, label="MuRIL"),
               Line2D([], [], marker="s", ls="", color=C_MODEL["xlmrlarge"], ms=3.4, label="XLM-R-large"),
               Line2D([], [], marker="o", ls="", color="#444444", mfc="white", ms=3.4, label="unswapped (b)"),
               Line2D([], [], marker="o", ls="", color="#444444", ms=3.4, label="swapped (b)"),
               Line2D([], [], color="#444444", lw=0.9, ls="-", label="SOV-type (c)"),
               Line2D([], [], color="#444444", lw=0.9, ls="--", label="OSV-type (c)")]
    fig.legend(handles=handles, loc="upper center", ncol=6, fontsize=5.6, frameon=False, bbox_to_anchor=(0.5, 1.01),
               handletextpad=0.3, columnspacing=1.0)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig3_agreement.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


def _cases(model):
    z = np.load(N.OUT / f"case_wordorder_{model}.npz", allow_pickle=True)
    g = lambda v: z[f"{v}_f_clean"] - z[f"{v}_f_corrupt"]
    d_rand = g("ctl") - g("psp")
    k = np.load(N.OUT / f"kind_{model}.npz", allow_pickle=True)
    gp = dict(zip(k["ids_psp"], k["psp_f_clean"] - k["psp_f_corrupt"]))
    gk = dict(zip(k["ids_ctlk"], k["ctlk_f_clean"] - k["ctlk_f_corrupt"]))
    dk = dict(zip(k["ids_ctlk"], k["docs_ctlk"]))
    ids = [i for i in k["ids_ctlk"] if i in gp]
    d_kind = np.array([gk[i] - gp[i] for i in ids])
    return (N.boot_mean(d_rand, z["docs"]), len(d_rand)), (N.boot_mean(d_kind, np.array([dk[i] for i in ids])), len(ids))


def fig4():
    fig = plt.figure(figsize=(6.3, 2.15))
    a = fig.add_axes([0.20, 0.20, 0.25, 0.58])
    b = fig.add_axes([0.555, 0.20, 0.205, 0.58])
    c = fig.add_axes([0.79, 0.20, 0.205, 0.58])
    a.set_title("(a) Deleting the moved markers", loc="left", fontsize=6.8, fontweight="bold", pad=2, x=-0.62)
    rows = [("other words,\nsame number", 0), ("distant\npostpositions", 1)]
    for m in N.MODELS:
        (r, nr), (k, nk) = _cases(m)
        for j, (res, n) in enumerate(((r, nr), (k, nk))):
            y = 1 - j + (0.12 if m == "muril" else -0.12)
            mean, lo, hi = res
            a.errorbar([mean], [y], xerr=[[mean - lo], [hi - mean]], fmt="o" if m == "muril" else "s", ms=3.4, color=C_MODEL[m],
                       capsize=1.5, elinewidth=0.9)
    a.axvline(0, color="#999999", lw=0.5)
    a.set_yticks([1, 0])
    a.set_yticklabels([r[0] for r in rows], fontsize=6)
    a.set_ylim(-0.6, 1.6)
    a.set_xlabel("gap kept after the control minus\nafter the markers (bits)", fontsize=6.0, labelpad=1)
    style(a)
    from matplotlib.lines import Line2D as _L
    a.legend(handles=[_L([], [], marker="o", ls="", color=C_MODEL["muril"], ms=3, label="MuRIL"), _L([], [], marker="s", ls="", color=C_MODEL["xlmrlarge"], ms=3, label="XLM-R")], fontsize=5.4, frameon=False, loc="lower right", handletextpad=0.2, borderaxespad=0.1)
    for ax, m, ttl in ((b, "muril", "(b) MuRIL"), (c, "xlmrlarge", "(c) XLM-R-large")):
        rows_ = N.read_csv(N.OUT / f"cues_{m}.csv")
        gap = N.col(rows_, "gap")
        eff = N.col(rows_, "eff_5 MLPs jointly")
        st = np.array([r["stratum_kenlm"] for r in rows_])
        ax.set_title(ttl, loc="left", fontsize=6.8, fontweight="bold", pad=2)
        for s, mk, col, lab in (("agrees", "o", "#b5b5b5", "n-gram cue agrees"), ("disagrees", "x", C_MODEL[m], "n-gram cue disagrees")):
            sel = st == s
            ax.scatter(gap[sel], eff[sel], s=4 if s == "agrees" else 7, marker=mk, color=col, lw=0.6, label=lab, zorder=2)
            xs = np.linspace(np.nanmin(gap[sel]), np.nanmax(gap[sel]), 20)
            co = np.polyfit(gap[sel], eff[sel], 1)
            ax.plot(xs, np.polyval(co, xs), color="#444444" if s == "agrees" else C_MODEL[m], lw=0.9, zorder=3)
        ax.set_xlabel("gap (bits)", fontsize=6.2, labelpad=1)
        if m == "muril":
            ax.set_ylabel("effect of the five MLPs (bits)", fontsize=6.0)
        style(ax)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", ls="", color="#b5b5b5", ms=3, label="n-gram cue favours the written order"),
               Line2D([], [], marker="x", ls="", color="#333333", ms=3.4, label="n-gram cue favours the reordered order"),
               Line2D([], [], color="#444444", lw=0.9, label="least-squares line per group")]
    fig.legend(handles=handles, loc="upper center", ncol=3, fontsize=5.6, frameon=False, bbox_to_anchor=(0.5, 1.01),
               handletextpad=0.3, columnspacing=1.0)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig4_wordorder.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


def fig1():
    fig = plt.figure(figsize=(6.3, 2.0))
    a = fig.add_axes([0.01, 0.0, 0.47, 0.93])
    b = fig.add_axes([0.52, 0.0, 0.47, 0.93])
    panel_word_order(a)
    panel_agreement(b)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig1_design.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


def _rows(path, ncols):
    """Table rows of a run record as lists of cells (numbers kept as text)."""
    rows = []
    for line in path.read_text().splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def fig_heads():
    """The top five agreement heads: attention from the verb to the object, and the gap restored through the object."""
    rec = ROOT / "course_runs" / "records"
    heads, att, via_obj, via_all, model_of = [], [], [], [], []
    for m in N.MODELS:
        a = {r[0]: float(r[2]) for r in _rows(rec / f"mi_attention_{m}.md", 6) if len(r) == 6 and r[1] == "object" and r[0] != "all"}
        p = {r[0]: (float(r[1]), float(r[4])) for r in _rows(rec / f"mi_path_{m}.md", 6) if len(r) == 6 and r[0].startswith("L")}
        for h in p:
            heads.append(h); att.append(a[h]); via_obj.append(p[h][0]); via_all.append(p[h][1]); model_of.append(m)
    n = len(heads)
    ypos = [i if i < 5 else i + 0.8 for i in range(n)]
    fig = plt.figure(figsize=(3.3, 2.35))
    a = fig.add_axes([0.20, 0.19, 0.36, 0.67])
    b = fig.add_axes([0.66, 0.19, 0.32, 0.67])
    for ax in (a, b):
        style(ax)
        ax.set_ylim(max(ypos) + 0.7, -0.7)
    a.set_yticks(ypos)
    a.set_yticklabels(heads, fontsize=7)
    b.set_yticks([])
    for y, m, v in zip(ypos, model_of, att):
        a.barh(y, v, height=0.7, color=C_MODEL[m])
    for y, m, v, w in zip(ypos, model_of, via_obj, via_all):
        b.barh(y, w, height=0.7, color="#d9d9d9")
        b.barh(y, v, height=0.7, color=C_MODEL[m])
    a.set_xlim(0, 0.8)
    b.set_xlim(0, 0.35)
    a.set_title("(a) Attention to object", loc="left", fontsize=7.2, fontweight="bold", pad=2)
    b.set_title("(b) Gap restored", loc="left", fontsize=7.2, fontweight="bold", pad=2)
    a.set_xlabel("share of the verb's attention", fontsize=6.8, labelpad=1)
    b.set_xlabel("share of the gap", fontsize=6.8, labelpad=1)
    a.text(0.0, ypos[2], "MuRIL", fontsize=6.4, color=C_MODEL["muril"], ha="right", va="center", rotation=90,
           transform=a.get_yaxis_transform(), x=-0.30) if False else None
    b.text(0.99, ypos[4] + 0.25, "at the object", fontsize=6.4, ha="right", va="bottom", color=DARK, transform=b.get_yaxis_transform()) if False else None
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=C_MODEL["muril"], label="MuRIL"), Patch(color=C_MODEL["xlmrlarge"], label="XLM-R-large"),
                        Patch(color="#d9d9d9", label="light grey: at all positions")],
               loc="upper center", ncol=3, fontsize=6.4, frameon=False, bbox_to_anchor=(0.5, 1.02), handletextpad=0.4,
               columnspacing=0.9, handlelength=1.0)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_heads.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


def fig_subject():
    """Where the intervening-subject contrast lies: OSV-type minus SOV-type orders, by word class."""
    rec = ROOT / "course_runs" / "records"
    names = [("A", "Whole sentence"), ("A_agree", "Agreeing words"), ("A_verb", "Rest of verb"), ("A_object", "Object"),
             ("A_subject", "Subject"), ("A_ne", "ne"), ("A_other", "Other words")]
    val = {}
    for m in N.MODELS:
        d = {r[0]: float(r[3]) for r in _rows(rec / f"mi_decompose_{m}.md", 5) if len(r) == 5 and r[0] in dict(names)}
        val[m] = [d[k] for k, _ in names]
    fig = plt.figure(figsize=(3.3, 2.1))
    ax = fig.add_axes([0.31, 0.19, 0.66, 0.72])
    style(ax)
    y = np.arange(len(names))
    for j, m in enumerate(N.MODELS):
        ax.barh(y + (-0.19 if j == 0 else 0.19), val[m], height=0.36, color=C_MODEL[m],
                label="MuRIL" if m == "muril" else "XLM-R-large")
    ax.axvline(0, color="#444444", lw=0.6)
    ax.axhline(0.5, color="#bbbbbb", lw=0.5, ls=":")
    ax.set_yticks(y)
    ax.set_yticklabels([n for _, n in names], fontsize=6.8)
    ax.set_ylim(len(names) - 0.5, -0.5)
    ax.set_xlabel("OSV-type minus SOV-type orders (bits)", fontsize=6.8, labelpad=1)
    
    fig.legend(*ax.get_legend_handles_labels(), loc="upper center", ncol=2, fontsize=6.4, frameon=False, bbox_to_anchor=(0.62, 1.02), handlelength=1.0)
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_subject.{ext}", dpi=300 if ext == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig_heads()
    fig_subject()
    print("wrote figures in", OUT)
