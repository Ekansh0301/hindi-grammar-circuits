#!/usr/bin/env python3
"""Figures of the paper (paper/figures/). numpy and matplotlib only; reads course_runs/outputs where a figure needs data.

fig1_design   the two tasks side by side: the clean run, the corrupted run and the metric (no data)

usage: python3 scripts/mi_figures_paper.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

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


if __name__ == "__main__":
    fig1()
    print("wrote", OUT / "fig1_design.pdf")
