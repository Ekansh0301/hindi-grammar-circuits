#!/usr/bin/env python3
"""Control tasks for the case probe: how much of its accuracy is the model, and how much is the probe
(RQ1_WORK_PLAN.md O1).

F3 reports that a constituent's case marker is recoverable from its own states at 0.89 to 0.92 accuracy
with the marker itself removed. The project has BASELINES for that number (majority class, and the same
probe on the pre-LayerNorm embedding sum) but no CONTROL TASK, which is a different thing and the one
Hewitt and Liang (2019) argue for: a task with the same form and the same label distribution but no
linguistic content, so that what the probe can fit by memorising is measured rather than assumed.

The control task here. Each constituent's head LEMMA is assigned one label, drawn once from the
empirical label distribution with a fixed seed, and every constituent with that head lemma gets it. The
probe then has to learn head-lemma to arbitrary-label, which is pure memorisation: nothing about case
survives. Selectivity is real accuracy minus control accuracy, and it is the number to read, not the
raw accuracy.

  high selectivity   the states carry case, and the probe is reading it
  low selectivity    the probe has enough capacity to memorise the head lemma, so the real accuracy
                     says little about what the model represents

The pair probes (d_syn_order, d_dep_mean) get a permutation check instead, and the docstring says why:
they are ridge regressions scored by OUT-OF-FOLD R^2 with folds grouped by reference, so memorisation
already shows up as a failure to generalise rather than as inflated performance. The permuted run is
reported as a floor, to confirm that it lands at zero rather than to stand in for a control task.
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import f1_score, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from hutb_corpus import BASE, load_trees
from rq1_layer_probe import load_states
from rq1_structure_probe import oof
from runlog import RunLog


def oof_parallel(make, X, y, groups, n_jobs=5):
    """`rq1_structure_probe.oof`, with the five folds fitted in parallel.

    Folds are independent and GroupKFold is deterministic, so this returns exactly what the serial
    version returns; it exists only because this script fits the probe twice per layer (real task and
    control task) over 64 layers, and serially that is five hours of one core.
    """
    splits = list(GroupKFold(n_splits=5).split(X, y, groups))
    parts = Parallel(n_jobs=n_jobs)(
        delayed(lambda tr, te: make().fit(X[tr], y[tr]).predict(X[te]))(tr, te) for tr, te in splits)
    out = np.empty(len(y), dtype=parts[0].dtype)
    for (_, te), pred in zip(splits, parts):
        out[te] = pred
    return out


def head_lemma(refs, ref_ids, heads):
    """The lemma of each unit's head token, for the control task's type. Form is the fallback: a few
    tokens carry no lemma, and an empty type would silently pool them into one."""
    out = []
    for r, h in zip(ref_ids, heads):
        rows = refs.get(str(r), [])
        tok = next((x for x in rows if int(x[0]) == int(h)), None)
        if tok is None:
            out.append(f"__missing_{r}_{h}")
        else:
            lem = (tok[2] or "").strip()
            out.append(lem if lem and lem != "_" else (tok[1] or "").strip())
    return np.array(out)


def control_labels(types, labels, seed=707):
    """One label per TYPE, drawn from the empirical label distribution and fixed for that type."""
    rng = np.random.default_rng(seed)
    pool = np.asarray(labels)
    uniq = pd.unique(types)
    assign = {t: pool[rng.integers(len(pool))] for t in uniq}
    return np.array([assign[t] for t in types])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--dir", default=str(rc / "lm_units"))
    ap.add_argument("--units", default=str(rc / "rq1_features_units.csv"))
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--tag", default="rq1_probe_selectivity")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="Hewitt and Liang control task for the case probe: selectivity per layer, and "
                        "a permutation floor for the pair probes.") as log:
        refs, _ = load_trees()
        clf = lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=3000))
        reg = lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0))
        rows = []

        for m in args.models:
            up = Path(args.dir) / f"units_{m}.npz"
            if up.exists():
                z = np.load(up, allow_pickle=True)
                y, g = z["label"], pd.factorize(z["ref_id"])[0]
                types = head_lemma(refs, z["ref_id"], z["unit_head"])
                yc = control_labels(types, y)
                log.h2(f"model: {m}, case probe against its control task")
                log.kv("constituents / references / distinct head lemmas",
                       f"{len(y):,} / {g.max() + 1:,} / {len(pd.unique(types)):,}")
                log.kv("units per head lemma (mean)", f"{len(y) / len(pd.unique(types)):.2f}")
                maj = pd.Series(y).value_counts().iloc[0] / len(y)
                majc = pd.Series(yc).value_counts().iloc[0] / len(yc)
                log.kv("majority class: real task, control task", f"{maj:.4f}, {majc:.4f}")
                tab = []
                for layer in range(z["states"].shape[1]):
                    X = z["states"][:, layer].astype(np.float32)
                    pr = oof_parallel(clf, X, y, g)
                    pc = oof_parallel(clf, X, yc, g)
                    a_r, a_c = float((pr == y).mean()), float((pc == yc).mean())
                    tab.append([layer, a_r, a_c, a_r - a_c,
                                float(f1_score(y, pr, average="macro")),
                                float(f1_score(yc, pc, average="macro"))])
                    rows.append([m, "case", layer, a_r, a_c, a_r - a_c])
                    print(f"    {m} layer {layer}: real {a_r:.3f} control {a_c:.3f} "
                          f"selectivity {a_r - a_c:+.3f}", flush=True)
                log.table(["layer", "real accuracy", "control accuracy", "selectivity",
                           "real macro-F1", "control macro-F1"], tab)
                best = max(tab, key=lambda r: r[3])
                log.kv("highest selectivity", f"layer {best[0]}, {best[3]:+.4f} "
                                              f"({best[1]:.4f} against {best[2]:.4f})")

            files = sorted(glob.glob(f"{args.dir}/states_{m}_s*_part*.npz"))
            if files:
                tgt = pd.read_csv(args.units, usecols=["ref_id", "var_id", "d_syn_order"]).merge(
                    pd.read_csv(args.features, usecols=["ref_id", "var_id", "d_dep_mean"]),
                    on=["ref_id", "var_id"])
                ref, var, D, _, _ = load_states(f"{args.dir}/states_{m}_s*_part*.npz")
                key = pd.DataFrame({"ref_id": ref, "var_id": var}).merge(tgt, on=["ref_id", "var_id"],
                                                                        how="left")
                ok = key[["d_syn_order", "d_dep_mean"]].notna().all(1).to_numpy()
                g = pd.factorize(ref[ok])[0]
                rng = np.random.default_rng(707)
                perm = rng.permutation(int(ok.sum()))
                log.h2(f"model: {m}, pair probes against a permutation floor")
                mid = D.shape[1] // 2
                tab = []
                for layer in (0, mid, D.shape[1] - 1):
                    X = D[ok, layer]
                    r = [layer]
                    for t in ("d_syn_order", "d_dep_mean"):
                        yv = key.loc[ok, t].to_numpy(float)
                        r.append(float(r2_score(yv, oof(reg, X, yv, g))))
                        r.append(float(r2_score(yv[perm], oof(reg, X, yv[perm], g))))
                    tab.append(r)
                    rows.append([m, "pair", layer, r[1], r[2], r[1] - r[2]])
                log.table(["layer", "R² d_syn_order", "permuted", "R² d_dep_mean", "permuted"], tab)
                log.p("Three layers only: first, middle, output. The permuted column is a floor check, "
                      "not a control task, for the reason in this script's docstring.")

        log.note("Selectivity, not raw accuracy, is what says the states carry case. A probe that "
                 "scores well on the control task has the capacity to memorise the head lemma, and its "
                 "real accuracy then says as much about the probe as about the model.")
        log.note("The control task is a function of the head LEMMA, so it is fixed per type and "
                 "reproducible from the seed; it is not a per-constituent coin flip, which would be a "
                 "random-label baseline and is a weaker check.")
        p = Path(args.dir).parent / f"{args.tag}.csv"
        pd.DataFrame(rows, columns=["model", "probe", "layer", "real", "control",
                                    "selectivity"]).to_csv(p, index=False)
        log.output(str(p), "per-layer real, control and selectivity")


if __name__ == "__main__":
    main()
