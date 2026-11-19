#!/usr/bin/env python3
"""RQ1 four-block decomposition L, S, E, T on Set 1 (PREREGISTRATION_DRAFT.md 6.3, items 1, 3, 5).

E is structural expectation with no word identities (E1 `d_syn_order` by default). For each
transformer:

  - general and conditional dominance of L, S, E, T (16 subset models, Firth, Nagelkerke R²);
  - ΔR²(E | L, S), ΔR²(T | L, S), ΔR²(T | L, S, E);
  - absorbed share = 1 − ΔR²(T | L, S, E) / ΔR²(T | L, S): the part of T's unique contribution
    that a predictor without word identities also provides, with a 95% interval from a bootstrap
    over references;
  - out-of-fold AUC of L+S, L+S+E, L+S+T, L+S+E+T; ΔAUC(E over L+S) and ΔAUC(T over L+S+E) with
    reference-bootstrap intervals and pair-level McNemar; Benjamini-Hochberg over the run;
  - condition index of every block combination.

--acc adds the declared S extensions (d_pron_inv; d_bare_obj and d_bare_obj_nonspec only where
they differ in at least 200 pairs). --moved-stratum and --order-classes restrict the pairs
(strata under 200 pairs are skipped, as declared).
"""
import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from dominance_analysis import fit_subset, nagelkerke_r2, run_dominance_analysis
from hutb_corpus import BASE
from rq1_dominance import (auc_fast, bh, bootstrap_index, cluster_bootstrap_auc_diff, cv_predict, joachims,
                           mcnemar_pairs, pair_halves)
from runlog import RunLog

L_COLS = ["d_kenlm_mean_filt", "d_semantic_sim", "d_same_case_bigram"]
S_COLS = ["d_dep_mean", "d_dlt_mean", "d_is_inv_norm"]
ACC_COLS = ["d_pron_inv", "d_bare_obj", "d_bare_obj_nonspec"]
BLOCKS = ["L", "S", "E", "T"]
MIN_PAIRS = 200


def condition_index(frame):
    z = (frame - frame.mean()) / frame.std(ddof=0)
    s = np.linalg.svd(z.to_numpy(float), compute_uv=False)
    return float(s[0] / s[-1])


def r2_of(exp, cols_by_key, keys):
    """Nagelkerke R² of the listed block combinations on one expanded frame."""
    n = len(exp)
    llnull, _ = fit_subset(exp, "y", [])
    return {k: nagelkerke_r2(fit_subset(exp, "y", cols_by_key(k))[0], llnull, n) for k in keys}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--units", default=str(rc / "rq1_features_units.csv"))
    ap.add_argument("--sample", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--t-features", nargs="+", required=True)
    ap.add_argument("--e-cols", nargs="+", default=["d_syn_order"])
    ap.add_argument("--acc", action="store_true")
    ap.add_argument("--s-extra-file", default=None,
                    help="CSV of ref_id, var_id and extra memory-cost predictors to add to S (with --s-extra-cols)")
    ap.add_argument("--s-extra-cols", nargs="+", default=None)
    ap.add_argument("--ngram", default=str(rc / "rq1_features_ngram.csv"))
    ap.add_argument("--l-trigram", default="d_kenlm_mean_filt",
                    help="L's trigram column; a column of --ngram replaces it (the L-series, prereg 6.3(2))")
    ap.add_argument("--moved-stratum", default=None, choices=["arguments_only", "adjuncts_only", "both"])
    ap.add_argument("--order-classes", nargs="+", default=None)
    ap.add_argument("--sev-q", nargs="+", default=None, help="restrict to severity quartiles of the sample (e.g. Q1)")
    ap.add_argument("--keep", default=None, help="CSV of ref_id, var_id: restrict to these pairs")
    ap.add_argument("--bootstrap", type=int, default=2000, help="replicates for the AUC differences")
    ap.add_argument("--share-bootstrap", type=int, default=200, help="replicates for the absorbed share")
    ap.add_argument("--cluster", default="reference", choices=["reference", "document"],
                    help="unit of the cross-validation folds and of every bootstrap. 'reference' is one "
                         "pair, the default every RQ1 number uses; 'document' keeps the pairs of one "
                         "document together, which is the stricter reading when pairs from a document "
                         "share its topic and its vocabulary")
    ap.add_argument("--tag", default="rq1_four_block")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="Four-block decomposition L, S, E, T: how much of transformer surprisal's "
                        "unique contribution a structure-only order model also provides.") as log:
        df = pd.read_csv(args.features).merge(pd.read_csv(args.units), on=["ref_id", "var_id"], how="inner")
        if args.s_extra_file:
            if not args.s_extra_cols:
                raise SystemExit("--s-extra-file needs --s-extra-cols")
            df = df.merge(pd.read_csv(args.s_extra_file)[["ref_id", "var_id"] + args.s_extra_cols],
                          on=["ref_id", "var_id"], how="inner")
            log.kv("extra S predictors", ", ".join(args.s_extra_cols) + f" (from {args.s_extra_file})")
        if args.l_trigram != "d_kenlm_mean_filt":
            df = df.merge(pd.read_csv(args.ngram), on=["ref_id", "var_id"], how="inner")
            log.kv("L's trigram replaced by", args.l_trigram)
        smp = pd.read_csv(args.sample, usecols=["ref_id", "var_id", "order_class", "sev_q"])
        df = df.merge(smp, on=["ref_id", "var_id"], how="left")
        if args.moved_stratum:
            df = df[df.moved_stratum == args.moved_stratum]
            log.kv("moved-unit stratum", args.moved_stratum)
        if args.keep:
            df = df.merge(pd.read_csv(args.keep)[["ref_id", "var_id"]], on=["ref_id", "var_id"])
            log.kv("restricted to pairs listed in", args.keep)
        if args.sev_q:
            df = df[df.sev_q.isin(args.sev_q)]
            log.kv("severity quartiles", ", ".join(args.sev_q))
        if args.order_classes:
            df = df[df.order_class.isin(args.order_classes)]
            log.kv("reference word-order classes", ", ".join(args.order_classes))
        log.kv("pairs with L, S and unit features", f"{len(df):,}")

        S = list(S_COLS) + list(args.s_extra_cols or [])
        if args.acc:
            for c in ACC_COLS:
                nz = int((df[c] != 0).sum())
                if c == "d_pron_inv" or nz >= MIN_PAIRS:
                    S.append(c)
                else:
                    log.kv(f"{c} not entered", f"differs in {nz} pairs, under the floor of {MIN_PAIRS}")
        E = list(args.e_cols)

        models = {}
        for p in args.t_features:
            d = pd.read_csv(p)
            m = [c for c in d.columns if c.startswith("t_")][0].split("_")[1]
            models.setdefault(m, []).append(d)
        models = {m: pd.concat(v, ignore_index=True) for m, v in models.items()}
        common = set.intersection(*(set(map(tuple, d[["ref_id", "var_id"]].values)) for d in models.values()))

        tests, summary = [], []
        for m, tdf in models.items():
            log.h2(f"model: {m}")
            tcol = f"t_{m}_Mean"
            x = df.merge(tdf[["ref_id", "var_id", tcol]], on=["ref_id", "var_id"])
            x = x[[k in common for k in map(tuple, x[["ref_id", "var_id"]].values)]]
            blocks = {"L": [args.l_trigram if c == "d_kenlm_mean_filt" else c for c in L_COLS], "S": S, "E": E, "T": [tcol]}
            cols = [c for b in BLOCKS for c in blocks[b]]
            sub = x[["ref_id"] + cols].dropna()
            const = [c for c in cols if sub[c].nunique() <= 1]
            if const:
                log.kv("dropped as constant", ", ".join(const))
                blocks = {b: [c for c in v if c not in const] for b, v in blocks.items()}
                cols = [c for c in cols if c not in const]
            if len(sub) < MIN_PAIRS or not all(blocks.values()):
                log.note(f"{len(sub)} complete pairs or an empty block: not fitted")
                continue
            for b in BLOCKS:
                log.kv(b, ", ".join(blocks[b]))
            log.kv("pairs", f"{len(sub):,}")

            log.h3("Condition index of each block combination (standardised pair differences)")
            ci_rows = []
            for r in range(1, 5):
                for combo in itertools.combinations(BLOCKS, r):
                    cc = [c for b in combo for c in blocks[b]]
                    ci_rows.append(["+".join(combo), len(cc), condition_index(sub[cc])])
            log.table(["blocks", "predictors", "condition index"], ci_rows, floatfmt="{:.1f}")
            if max(r[2] for r in ci_rows) >= 30:
                log.note("A condition index reaches 30: the proposal's ridge rule applies.")

            exp = joachims(sub, cols)
            # One cluster label per pair, in the order the forward rows have.
            clust = (sub.ref_id.str.split("__").str[0].to_numpy() if args.cluster == "document" else None)
            if clust is not None:
                log.kv("clustering unit", f"document ({len(np.unique(clust)):,} documents, "
                                          f"{len(sub) / len(np.unique(clust)):.1f} pairs each)")
            res = run_dominance_analysis(exp, "y", blocks, verbose=False)
            R = res["subset_r2"]
            f = lambda *bs: R[frozenset(bs)]
            log.h3("Dominance")
            log.table(["block", "general dominance", "R² alone", "k=1", "k=2", "k=3"],
                      [[b, res["general_dominance"][b], res["conditional_dominance"][b][0]]
                       + [res["conditional_dominance"][b][k] for k in (1, 2, 3)] for b in BLOCKS])
            dE = f("L", "S", "E") - f("L", "S")
            dT = f("L", "S", "T") - f("L", "S")
            dTE = f("L", "S", "E", "T") - f("L", "S", "E")
            share = 1 - dTE / dT

            # bootstrap over references for the absorbed share and the two increments
            keys = [frozenset(k) for k in (("L", "S"), ("L", "S", "E"), ("L", "S", "T"), ("L", "S", "E", "T"))]
            by_key = lambda k: [c for b in BLOCKS if b in k for c in blocks[b]]
            n = pair_halves(exp)
            rng = np.random.default_rng(707)
            boot = []
            for _ in range(args.share_bootstrap):
                kk = bootstrap_index(rng, n, clust)
                e = exp.iloc[np.concatenate([kk, kk + n])].reset_index(drop=True)
                rr = r2_of(e, by_key, keys)
                bt = rr[keys[2]] - rr[keys[0]]
                bte = rr[keys[3]] - rr[keys[1]]
                boot.append((rr[keys[1]] - rr[keys[0]], bt, bte, 1 - bte / bt))
            boot = np.array(boot)
            ci = lambda j: np.percentile(boot[:, j], [2.5, 97.5])
            log.table(["quantity", "estimate", "95% low", "95% high"],
                      [["full-model R²", f("L", "S", "E", "T"), np.nan, np.nan],
                       ["ΔR²(E | L, S)", dE, *ci(0)],
                       ["ΔR²(T | L, S)", dT, *ci(1)],
                       ["ΔR²(T | L, S, E)", dTE, *ci(2)],
                       ["absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S)", share, *ci(3)]])
            log.p(f"Intervals: {args.share_bootstrap} bootstrap replicates over references.")

            y = exp["y"].to_numpy(float)
            g = exp["grp"].to_numpy() if clust is None else np.r_[clust, clust]
            pred = {k: cv_predict(exp[by_key(frozenset(k))].to_numpy(float), y, g)
                    for k in (("L", "S"), ("L", "S", "E"), ("L", "S", "T"), ("L", "S", "E", "T"))}
            rows = []
            pair_acc = lambda p: float((p[:n] > 0.5).mean())
            for lab, a, b in [("E over L+S", ("L", "S", "E"), ("L", "S")),
                              ("T over L+S", ("L", "S", "T"), ("L", "S")),
                              ("T over L+S+E", ("L", "S", "E", "T"), ("L", "S", "E"))]:
                d_, lo, hi, pb = cluster_bootstrap_auc_diff(y, pred[a], pred[b], n, B=args.bootstrap,
                                                            clusters=clust)
                bb, cc, pm = mcnemar_pairs(y, pred[a], pred[b], n)
                rows.append([lab, auc_fast(y, pred[b]), auc_fast(y, pred[a]), d_, lo, hi, pb,
                             pair_acc(pred[b]), pair_acc(pred[a]), pair_acc(pred[a]) - pair_acc(pred[b]),
                             bb, cc, pm])
                tests += [(f"{m}: {lab} (AUC)", pb), (f"{m}: {lab} (McNemar)", pm)]
            log.h3(f"Out-of-fold AUC and per-pair accuracy (grouped 5-fold by {args.cluster})")
            log.table(["comparison", "AUC without", "AUC with", "ΔAUC", "95% low", "95% high",
                       "bootstrap p", "accuracy without", "accuracy with", "Δaccuracy",
                       "McNemar b", "c", "McNemar p"], rows, floatfmt="{:.4g}")
            log.p("Accuracy is per pair -- is the reference scored above its own variant -- which is what "
                  "the task asks and what McNemar tests. AUC is taken over every positive row against "
                  "every negative row, including rows from different pairs, so it also rewards a "
                  "predictor for having a consistent sign; read the two together, and see "
                  "`rq1_null_calibration_permute.md` for how far apart they can be pushed.")
            summary.append([m, len(sub), f("L", "S"), dE, dT, dTE, share, *ci(3),
                            rows[0][3], rows[2][3]])

        if summary:
            log.h2("Summary")
            log.table(["model", "pairs", "R²(L+S)", "ΔR²(E|L,S)", "ΔR²(T|L,S)", "ΔR²(T|L,S,E)",
                       "absorbed share", "95% low", "95% high", "ΔAUC E over L+S", "ΔAUC T over L+S+E"],
                      summary)
        if tests:
            log.h2("Benjamini-Hochberg across every test in this run")
            adj = bh([p for _, p in tests])
            log.table(["test", "raw p", "BH p", "significant at 0.05"],
                      [[t, p, a, "yes" if a < 0.05 else "no"] for (t, p), a in zip(tests, adj)],
                      floatfmt="{:.4g}")


if __name__ == "__main__":
    main()
