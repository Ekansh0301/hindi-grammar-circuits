#!/usr/bin/env python3
"""Layer-wise reference-vs-variant probe (PREREGISTRATION_DRAFT.md 7.1; RQ1_WORK_PLAN.md F1).

Input: states_<model>_s*_part*.npz from rq1_lm_units.py --what states (pooled hidden-state
difference, reference minus variant, per layer). For each layer:

  probe     L2 logistic regression, C = 1.0, on the standardised difference (scaler fitted inside
            each training fold); Joachims mirror rows (x, 1) and (−x, 0); 5-fold grouped by reference
  control   a random-label control: the same probe after flipping each pair's labels with probability
            1/2 (seed 707), which destroys the reference/variant identity while keeping the design;
            selectivity = accuracy minus control accuracy. This is NOT Hewitt and Liang's (2019) control
            task, which gives each word type a fixed random label the probe could memorise; flipped
            labels carry no learnable signal at all, so the control is expected at chance and
            selectivity here is close to accuracy minus 0.5. (The Hewitt and Liang control of this
            project is the case probe's, rq1_probe_selectivity.py.)

The layer-0 identity check is carried by the states files themselves: pre_ln_maxabs, the largest
difference of the pooled pre-LayerNorm embedding sum, must be ~0 for every pair (its maximum is
reported); a probe on that input is at chance by construction. hidden_states[0] (after the
embedding LayerNorm) is reported as layer 0 and need not be at chance.

Reported next to each model's surprisal single-feature accuracy (t_<model>_Mean < 0) on the same pairs.
No L + S classifier is fitted: --features is read but not used. Also: mean cosine similarity of pooled
reference and variant states per layer (descriptive, 7.4).
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from hutb_corpus import BASE
from runlog import RunLog


def load_states(pattern):
    files = sorted(glob.glob(pattern))
    parts = [np.load(f) for f in files]
    return (np.concatenate([p["ref_id"] for p in parts]), np.concatenate([p["var_id"] for p in parts]),
            np.concatenate([p["diff"] for p in parts]).astype(np.float32),
            np.concatenate([p["cos"] for p in parts]), np.concatenate([p["pre_ln_maxabs"] for p in parts]))


def probe(X, groups, flip):
    """Out-of-fold accuracy and AUC of the mirror-row probe; flip: per-pair label flips."""
    n = len(X)
    Xe = np.vstack([X, -X])
    y = np.r_[np.ones(n), np.zeros(n)]
    y = np.where(np.r_[flip, flip], 1 - y, y)
    g = np.r_[groups, groups]
    p = np.zeros(2 * n)
    for tr, te in GroupKFold(n_splits=5).split(Xe, y, g):
        clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000))
        p[te] = clf.fit(Xe[tr], y[tr]).predict_proba(Xe[te])[:, 1]
    return float(((p > 0.5) == (y == 1)).mean()), float(roc_auc_score(y, p))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--states-dir", default=str(rc / "lm_units"))
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--out", default=str(rc / "rq1_layer_probe.csv"))
    ap.add_argument("--tag", default="rq1_layer_probe")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args, purpose="Where in each model reference and variant become linearly "
                                                  "separable, against surprisal's single-feature accuracy.") as log:
        feats = pd.read_csv(args.features)
        rows = []
        for m in args.models:
            ref, var, D, cos, pre = load_states(f"{args.states_dir}/states_{m}_s*_part*.npz")
            if len(ref) == 0:
                log.note(f"{m}: no states files")
                continue
            log.h2(f"model: {m}")
            log.kv("pairs", f"{len(ref):,}")
            log.kv("largest pooled pre-LayerNorm difference (identity check)", f"{pre.max():.3g}")
            if pre.max() > 1e-3:
                raise SystemExit(f"{m}: identity check failed")
            groups = pd.factorize(ref)[0]
            flip = np.random.default_rng(707).random(len(ref)) < 0.5
            t = pd.concat(pd.read_csv(f) for f in sorted(glob.glob(str(rc / f"t_{m}_within_word_l2r_s*.csv"))))
            key = pd.DataFrame({"ref_id": ref, "var_id": var})
            tm = key.merge(t[["ref_id", "var_id", f"t_{m}_Mean"]], on=["ref_id", "var_id"], how="left")[f"t_{m}_Mean"]
            log.kv("surprisal single-feature accuracy on these pairs", f"{(tm < 0).mean():.4f}")
            out = []
            for layer in range(D.shape[1]):
                acc, auc = probe(D[:, layer], groups, np.zeros(len(ref), bool))
                cacc, cauc = probe(D[:, layer], groups, flip)
                out.append([layer, acc, auc, cacc, acc - cacc, float(cos[:, layer].mean())])
                rows.append([m, layer, acc, auc, cacc, acc - cacc, float(cos[:, layer].mean())])
                print(f"    {m} layer {layer}: acc {acc:.3f} control {cacc:.3f}", flush=True)
            log.table(["layer", "probe accuracy", "probe AUC", "control accuracy", "selectivity",
                       "mean cosine(ref, var)"], out, floatfmt="{:.4f}")
        pd.DataFrame(rows, columns=["model", "layer", "acc", "auc", "control_acc", "selectivity", "cos"]).to_csv(
            args.out, index=False)
        log.output(args.out, "probe results per model and layer")


if __name__ == "__main__":
    main()
