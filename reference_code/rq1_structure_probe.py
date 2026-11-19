#!/usr/bin/env python3
"""Structure per layer (PREREGISTRATION_DRAFT.md 7.3; RQ1_WORK_PLAN.md F3).

Case probe. From units_<model>.npz (rq1_lm_units.py --what units): each constituent's pooled states
without its own postpositions; label = its case marker (0, ne, ko, se, me, par, ka, other).
Multinomial logistic regression, C = 1.0, standardised inside folds, 5-fold grouped by reference.
Per layer: accuracy and macro-F1, against the majority class and against the same probe on the pooled
pre-LayerNorm embedding sum of the same words (the control).

Pair probes. From states_<model>_s*_part*.npz (pooled reference-minus-variant difference): ridge
regression, alpha = 1.0, standardised inside folds, 5-fold grouped by reference, predicting
d_syn_order (E1) and d_dep_mean; out-of-fold R² per layer. The control is layer 0 (the pooled
pre-LayerNorm difference is zero by construction, so it cannot serve).
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import f1_score, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from hutb_corpus import BASE
from rq1_layer_probe import load_states
from runlog import RunLog


def oof(make, X, y, groups, predict_proba=False):
    out = np.empty(len(y), dtype=y.dtype) if not predict_proba else np.zeros(len(y))
    for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
        out[te] = make().fit(X[tr], y[tr]).predict(X[te])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--dir", default=str(rc / "lm_units"))
    ap.add_argument("--units", default=str(rc / "rq1_features_units.csv"))
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--out", default=str(rc / "rq1_structure_probe.csv"))
    ap.add_argument("--tag", default="rq1_structure_probe")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args, purpose="Is case marking decodable from a constituent without its "
                                                  "marker, and are order expectation and dependency length "
                                                  "decodable from the pair difference, layer by layer?") as log:
        tgt = pd.read_csv(args.units, usecols=["ref_id", "var_id", "d_syn_order"]).merge(
            pd.read_csv(args.features, usecols=["ref_id", "var_id", "d_dep_mean"]), on=["ref_id", "var_id"])
        rows = []
        clf = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000))
        reg = lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0))
        for m in args.models:
            up = Path(args.dir) / f"units_{m}.npz"
            if up.exists():
                z = np.load(up)
                y, g = z["label"], pd.factorize(z["ref_id"])[0]
                log.h2(f"model: {m}, case probe")
                log.kv("constituents / references", f"{len(y):,} / {g.max() + 1:,}")
                vc = pd.Series(y).value_counts()
                log.kv("labels", ", ".join(f"{k} {v}" for k, v in vc.items()))
                maj = vc.iloc[0] / len(y)
                ctrl = oof(clf, z["pre"].astype(np.float32), y, g)
                c_acc, c_f1 = float((ctrl == y).mean()), float(f1_score(y, ctrl, average="macro"))
                log.kv("majority-class accuracy", f"{maj:.4f}")
                log.kv("control (pre-LayerNorm embedding sum): accuracy, macro-F1", f"{c_acc:.4f}, {c_f1:.4f}")
                tab = []
                for layer in range(z["states"].shape[1]):
                    p = oof(clf, z["states"][:, layer].astype(np.float32), y, g)
                    acc, f1 = float((p == y).mean()), float(f1_score(y, p, average="macro"))
                    tab.append([layer, acc, f1, acc - c_acc])
                    rows.append([m, "case", layer, acc, f1])
                    print(f"    {m} case layer {layer}: {acc:.3f}", flush=True)
                log.table(["layer", "accuracy", "macro-F1", "accuracy minus control"], tab)
            files = sorted(glob.glob(f"{args.dir}/states_{m}_s*_part*.npz"))
            if files:
                ref, var, D, _, _ = load_states(f"{args.dir}/states_{m}_s*_part*.npz")
                key = pd.DataFrame({"ref_id": ref, "var_id": var}).merge(tgt, on=["ref_id", "var_id"], how="left")
                ok = key[["d_syn_order", "d_dep_mean"]].notna().all(1).to_numpy()
                g = pd.factorize(ref[ok])[0]
                log.h2(f"model: {m}, pair probes (out-of-fold R²)")
                log.kv("pairs", f"{ok.sum():,}")
                tab = []
                for layer in range(D.shape[1]):
                    X = D[ok, layer]
                    r = [layer]
                    for t in ["d_syn_order", "d_dep_mean"]:
                        yv = key.loc[ok, t].to_numpy(float)
                        r.append(float(r2_score(yv, oof(reg, X, yv, g))))
                    tab.append(r)
                    rows.append([m, "pair", layer, r[1], r[2]])
                log.table(["layer", "R² d_syn_order", "R² d_dep_mean"], tab)
                log.p("Layer 0 is the control row.")
        pd.DataFrame(rows, columns=["model", "probe", "layer", "a", "b"]).to_csv(args.out, index=False)
        log.output(args.out, "case probe: a = accuracy, b = macro-F1; pair probe: a = R² d_syn_order, b = R² d_dep_mean")


if __name__ == "__main__":
    main()
