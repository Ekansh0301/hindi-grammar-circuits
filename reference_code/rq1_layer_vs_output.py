#!/usr/bin/env python3
"""Does a readable middle layer predict the attested order better than the model's own output? (M4)

rq1_layerwise_decomposition.py enters each layer's lens surprisal as T and reports ΔR² and a ΔAUC with a
pair-bootstrap interval. Under the Jacobian lens a readable layer before the output adds more than the
output in every model, and under the tuned lens mBERT's layer 10 does. That comparison has never been
tested: the bootstrap interval is anti-conservative (rq1_null_calibration_sign.md), and taking the best
layer and then looking at its interval selects on the outcome. This is the test, specified before it is
run:

  for every lens (logit, tuned, Jacobian), every model, and EVERY layer the declared 2-nat rule calls
  readable other than the output itself:

    A = L + S + E1 + T_layer,   B = L + S + E1 + T_output

  both fitted out of fold on the same folds (rq1_dominance.cv_predict, grouped by reference), on the same
  pairs. Per pair, the log-loss of B minus the log-loss of A, averaged over the pair's forward and mirrored
  rows, so a positive difference means the layer predicts that pair's attested order better.

  The evidence is a sign-flip permutation p on the mean difference, with the flip made per DOCUMENT
  (the pair differences of one document are summed and that sum's sign is flipped), because pairs from one
  document share topic, writer and vocabulary; 10,000 flips; (1 + count) / (1 + flips), two-sided. Under
  "the layer and the output predict equally well" the document sums are symmetric about zero, so this is
  exact for that null. Holm across the readable layers within each lens and model, so testing every layer
  costs what it should; Benjamini-Hochberg across the whole run is reported beside it.

  Reported but not evidence: the difference in out-of-fold AUC and in per-pair accuracy (forward row above
  0.5), and the two ΔR²(T | L,S).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from hutb_corpus import BASE
from rq1_dominance import SPEC_L, SPEC_S, auc_fast, bh, cv_predict
from rq1_layerwise_decomposition import expand, layer_differences, r2
from runlog import RunLog


def holm(ps):
    order = np.argsort(ps)
    adj, run = np.empty(len(ps)), 0.0
    for rank, i in enumerate(order):
        run = max(run, (len(ps) - rank) * ps[i])
        adj[i] = min(1.0, run)
    return adj


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--lenses", nargs="+", default=["logit", "tuned", "jacobian"])
    ap.add_argument("--words-dir", default=str(rc / "lm_units"))
    ap.add_argument("--flips", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=707)
    ap.add_argument("--tag", default="rq1_layer_vs_output")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="Readable layers against the output, by a document-level sign-flip test.") as log:
        feats = pd.read_csv(rc / "rq1_features_all.csv").merge(
            pd.read_csv(rc / "rq1_features_units.csv"), on=["ref_id", "var_id"])
        rng = np.random.default_rng(args.seed)
        tests, summary = [], []
        for lens_name in args.lenses:
            for m in args.models:
                diffs, lens = layer_differences(args.words_dir, m, lens_name)
                suffix = "" if lens_name == "logit" else f"_{lens_name}"
                rf = Path(args.words_dir) / f"readability_{m}{suffix}.csv"
                if not rf.exists():
                    raise SystemExit(f"{rf} not found: readability decides which layers are tested")
                r = pd.read_csv(rf)
                read = {int(k): str(v).strip().lower() in ("yes", "true") for k, v in zip(r.layer, r["readable"])}
                d = feats.merge(diffs, on=["ref_id", "var_id"])
                L = [c for c in SPEC_L if d[c].nunique() > 1]
                withE = L + list(SPEC_S) + ["d_syn_order"]
                d = d.dropna(subset=withE + lens).reset_index(drop=True)
                n, out = len(d), lens[-1]
                cand = [c for c in lens[:-1] if read.get(int(c[5:]), False)]
                log.h2(f"{lens_name} lens, {m}")
                log.kv("pairs / readable layers before the output", f"{n:,} / "
                       + (", ".join(c[5:] for c in cand) or "none"))
                if not cand:
                    continue
                doc = d.ref_id.str.split("__").str[0].to_numpy()
                codes, docs = pd.factorize(doc)
                log.kv("documents (the flip unit)", f"{len(docs):,}")
                Xo, y, g = expand(d, withE + [out])
                po = cv_predict(Xo, y, g)
                eps = 1e-12

                def pair_loss(p):
                    ll = -(y * np.log(np.clip(p, eps, 1)) + (1 - y) * np.log(np.clip(1 - p, eps, 1)))
                    return 0.5 * (ll[:n] + ll[n:])
                lo_out, auc_out, acc_out = pair_loss(po), auc_fast(y, po), float((po[:n] > 0.5).mean())
                r2_out = r2(d, L + list(SPEC_S) + [out]) - r2(d, L + list(SPEC_S))
                signs = rng.choice([-1.0, 1.0], size=(args.flips, len(docs)))
                rows, ps = [], []
                for c in cand:
                    Xl, _, _ = expand(d, withE + [c])
                    pl = cv_predict(Xl, y, g)
                    delta = lo_out - pair_loss(pl)                      # > 0: the layer is better
                    sums = np.bincount(codes, weights=delta, minlength=len(docs))
                    obs = sums.sum() / n
                    null = (signs @ sums) / n
                    p = (1 + int((np.abs(null) >= abs(obs)).sum())) / (1 + args.flips)
                    r2_l = r2(d, L + list(SPEC_S) + [c]) - r2(d, L + list(SPEC_S))
                    rows.append([int(c[5:]), obs, p, auc_fast(y, pl) - auc_out,
                                 float((pl[:n] > 0.5).mean()) - acc_out, r2_l, r2_out])
                    ps.append(p)
                adj = holm(np.array(ps))
                for row, a in zip(rows, adj):
                    row.insert(3, float(a))
                    tests.append([f"{lens_name} {m} layer {row[0]}", row[2]])
                log.table(["layer", "mean log-loss gain over the output (nats per pair)", "permutation p",
                           "Holm p (this lens and model)", "ΔAUC, layer minus output", "Δaccuracy",
                           "ΔR²(T_layer | L,S)", "ΔR²(T_output | L,S)"], rows, floatfmt="{:.4g}")
                best = max(rows, key=lambda r: r[1])
                summary.append([lens_name, m, len(cand), best[0], best[1], best[3],
                                sum(1 for r in rows if r[1] > 0 and r[3] < 0.05),
                                sum(1 for r in rows if r[1] < 0 and r[3] < 0.05)])
        if tests:
            adj = bh([p for _, p in tests])
            log.h2("Benjamini-Hochberg across every test in this run")
            log.table(["test", "permutation p", "BH p"], [[t, p, a] for (t, p), a in zip(tests, adj)],
                      floatfmt="{:.4g}")
        log.h2("Summary")
        log.table(["lens", "model", "readable layers tested", "layer with the largest gain", "its gain (nats)",
                   "its Holm p", "layers better than the output (Holm p < 0.05)",
                   "layers worse than the output (Holm p < 0.05)"], summary, floatfmt="{:.4g}")
        log.p(f"{args.flips:,} document-level sign flips per test, so no p is below {1 / (1 + args.flips):.5f}. "
              "A positive gain means the layer's surprisal predicts the attested order better than the "
              "output's, with L + S + E1 in both models.")


if __name__ == "__main__":
    main()
