#!/usr/bin/env python3
"""
POST HOC analysis of P5 (docs/PAPER_EXPERIMENTS.md, third addendum). It was added AFTER P5 was run and its outcome read,
to interpret that outcome; it is not part of P5's declared rule and changes none of P5's labels. Local CPU analysis of
the file outputs/cues_<model>.csv written by mi_paper_cues.py; numpy and csv only (no pandas, no torch).

QUESTION. P5's strata (lexical cue agrees / disagrees) differ in their mean gap (the disagrees stratum has small gaps),
and a share is effect / gap, so a stratum with small gaps and a roughly constant effect shows a higher share by
arithmetic. Does the circuit's effect in bits differ between the strata once the pair's own gap is held fixed?
MODEL (per model, per circuit part: the 10 heads; the 5 MLPs jointly; per lexical cue: d_kenlm_mean_filt (the primary
cue) and d_ngram2_mean_filt (the second)): over pairs with |gap| > 0.05 bits (the P5 floor) and a cue that is neither
missing nor exactly 0,
    effect_bits = b0 + b1 * gap + b2 * stratum,    stratum = 0 (cue agrees: d < 0), 1 (cue disagrees: d > 0),
ordinary least squares. b2 is the stratum coefficient (bits): the change in the circuit's effect at the same gap.
Interval for b2: a document bootstrap, 1,000 draws, seed 707: resample the documents with replacement, refit on the
pairs of the resampled documents (a pair counts as often as its document is drawn), take the 2.5th and 97.5th
percentiles. Draws in which a stratum is empty are dropped and counted (stop if more than 1%). Descriptive, not a test.
Also printed, per stratum: the intercept and slope of the effect on the gap (separate OLS fits), and the mean gap.
READING (written before the numbers were read; the review that suggested the analysis expected a coefficient near 0):
if b2 and its interval lie within +-0.1 bit, the strata do not differ in the circuit's effect at the same gap, and the
upward 'cue-dependent' label of P5 is not evidence that the circuit tracks the cue; otherwise the record says so.
Outputs: records/mi_paper_cues_gap_<model>.md.
"""
import argparse
import csv
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("HUTB_RESULTS_DIR", str(ROOT / "course_runs" / "records"))
sys.path.insert(0, str(ROOT / "reference_code"))
from runlog import RunLog  # noqa: E402

OUT = Path(os.environ.get("MI_OUT", ROOT / "course_runs" / "outputs"))
PARTS = [("10 heads", "eff_10 heads"), ("5 MLPs jointly", "eff_5 MLPs jointly")]
CUES = ["d_kenlm_mean_filt", "d_ngram2_mean_filt"]
BAND = 0.10


def ols(y, gap, st):
    A = np.column_stack([np.ones(len(y)), gap, st])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return beta


def ols2(y, gap):
    A = np.column_stack([np.ones(len(y)), gap])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return beta


def boot_b2(y, gap, st, docs, B, seed=707):
    u = sorted(set(docs.tolist()))
    idx = {d: [] for d in u}
    for i, d in enumerate(docs):
        idx[d].append(i)
    members = [np.array(idx[d]) for d in u]
    rng = np.random.default_rng(seed)
    out, bad = [], 0
    for _ in range(B):
        pick = rng.integers(0, len(u), size=len(u))
        ii = np.concatenate([members[k] for k in pick])
        if st[ii].min() == st[ii].max():
            bad += 1
            continue
        out.append(ols(y[ii], gap[ii], st[ii])[2])
    if bad > 0.01 * B:
        raise SystemExit("more than 1% of bootstrap draws had an empty stratum")
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["muril", "xlmrlarge"])
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()
    with open(OUT / f"cues_{args.model}.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    col = lambda k: np.array([float(r[k]) if r[k] not in ("", "nan") else np.nan for r in rows])
    docs = np.array([r["doc"] for r in rows])
    gap = col("gap")
    keep = np.abs(gap) > args.min_gap
    with RunLog(f"mi_paper_cues_gap_{args.model}", __file__, args,
                purpose="P5 POST HOC: circuit effect regressed on gap and stratum (added after P5 was read)") as log:
        log.p("**POST HOC.** This analysis was added after P5 was run and read, to interpret its outcome. It is not part of "
              "P5's declared rule; P5's labels stand as run.")
        log.kv("pairs / above the gap floor / documents", f"{len(rows)} / {int(keep.sum())} / {len(set(docs.tolist()))}")
        for cue in CUES:
            v = col(cue)
            ok = keep & ~np.isnan(v) & (v != 0)
            st = (v > 0).astype(float)
            log.h2(f"Strata by {cue} (agrees = 0: d < 0; disagrees = 1: d > 0), pairs above the floor")
            log.kv("pairs agrees / disagrees (documents)", f"{int((ok & (st == 0)).sum())} / {int((ok & (st == 1)).sum())} "
                   f"({len(set(docs[ok & (st == 0)].tolist()))} / {len(set(docs[ok & (st == 1)].tolist()))})")
            trs, srs = [], []
            for nm, ecol in PARTS:
                y = col(ecol)
                b = ols(y[ok], gap[ok], st[ok])
                lo, hi, bad = boot_b2(y[ok], gap[ok], st[ok], docs[ok], args.boot)
                within = lo >= -BAND and hi <= BAND and abs(b[2]) <= BAND
                trs.append([nm, float(b[0]), float(b[1]), float(b[2]), f"[{lo:.3f}, {hi:.3f}]", bad,
                            "within +-0.1 bit" if within else "NOT within +-0.1 bit"])
                for s, sn in ((0, "agrees"), (1, "disagrees")):
                    m = ok & (st == s)
                    b2 = ols2(y[m], gap[m])
                    srs.append([nm, sn, int(m.sum()), float(gap[m].mean()), float(y[m].mean()), float(b2[0]), float(b2[1]),
                                float(y[m].sum() / gap[m].sum())])
            log.table(["circuit part", "intercept b0 (bits)", "gap slope b1", "stratum coefficient b2 (bits)",
                       "document bootstrap 95% (1,000 draws, seed 707)", "draws dropped", "reading"], trs, "{:.3f}")
            log.table(["circuit part", "stratum", "pairs", "mean gap", "mean effect (bits)", "intercept (bits)", "slope on gap",
                       "ratio of sums (share)"], srs, "{:.3f}")
        log.note("Post hoc and descriptive. A stratum coefficient near 0 with the share still higher in the disagrees "
                 "stratum means the share difference follows from the smaller gaps (effect roughly constant in bits).")


if __name__ == "__main__":
    main()
