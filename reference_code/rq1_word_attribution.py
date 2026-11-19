#!/usr/bin/env python3
"""Where the preference sits, word by word (PREREGISTRATION_DRAFT.md 6.2; RQ1_WORK_PLAN.md E1a, E2a).

Reference and variant contain the same words, so a scorer's summed preference for the reference,
D = Σ_words [s_variant(w) − s_reference(w)], splits exactly over words matched by reference tree
index (positive D: the reference is less surprising). Each word gets one class, in this order of
precedence:

  verb complex      the clause head and its verb-complex dependents (lwg*, pof), which never move
  postposition      xpos PSP
  moved head        head of a unit whose position changes
  moved other       any other word of a unit whose position changes
  unmoved unit      a word of a unit that stays in place
  outside           everything else (material outside the permuted clause region)
  end of sentence   the n-gram models' </s> term (transformers have none)

Reported per scorer and stratum: mean D in bits and each class's share of total D, with 95%
intervals from 2,000 bootstrap replicates over pairs (one variant per reference); separately, the
share carried by the words that are sentence-initial in either sentence.

--uid adds E2a: from each scorer's per-word surprisals, d_uid_var (variance) and d_uid_pow_k
(Σ s^k / n, k = 1.25, 1.5, 2), reference minus variant, and the ΔR² and out-of-fold ΔAUC they add to
L + S + T_mean (transformers) or to L (the trigram).
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

import set1_generator as G
from hutb_corpus import BASE, FC, parse_conllu, set1_variants
from materialise_set1 import official_tokens
from runlog import RunLog

CLASSES = ["verb complex", "postposition", "moved head", "moved other", "unmoved unit", "outside", "end of sentence"]
POWERS = [1.25, 1.5, 2.0]


def word_classes(ref_rows, var_row):
    """tree idx -> class, for one pair."""
    toks = official_tokens(ref_rows)
    by = {t["idx"]: t for t in toks}
    head = int(var_row["clause_head"])
    clause, _ = G.analyse_clause(toks, head)
    order = [int(x) for x in var_row["order"].split("|")]
    moved = {clause["units"][u] for slot, u in enumerate(order) if u != slot}
    cls = {}
    for t in toks:
        i = t["idx"]
        unit = next((d for d, sp in clause["spans"].items() if i in sp), None)
        if i in clause["vc_span"]:
            c = "verb complex"
        elif t["xpos"] == "PSP":
            c = "postposition"
        elif unit is not None and unit in moved:
            c = "moved head" if i == unit else "moved other"
        elif unit is not None:
            c = "unmoved unit"
        else:
            c = "outside"
        cls[i] = c
    cls[-1] = "end of sentence"
    return cls


def load_words(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        return None
    return pd.concat((pd.read_csv(f, usecols=["ref_id", "var_id", "side", "pos", "tree_idx", "s"]) for f in files),
                     ignore_index=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--words-dir", default=str(rc / "lm_units"))
    ap.add_argument("--ngram-words", nargs="*", default=[str(rc / "ngram_words_trigram_old.csv.gz"),
                                                         str(rc / "ngram_words_ngram5.csv.gz")])
    ap.add_argument("--sample", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--units", default=str(rc / "rq1_features_units.csv"))
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--uid", action="store_true")
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--out", default=str(rc / "rq1_word_attribution_pairs.csv"))
    ap.add_argument("--tag", default="rq1_word_attribution")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args, purpose="Exact word-level attribution of each scorer's preference "
                                                  "for the reference; UID measures.") as log:
        scorers = {}
        for m in args.models:
            w = load_words(f"{args.words_dir}/words_{m}_s*_part*.csv.gz")
            if w is not None:
                scorers[m] = w
        for p in args.ngram_words:
            if Path(p).exists():
                scorers[Path(p).name.replace("ngram_words_", "").replace(".csv.gz", "")] = pd.read_csv(p)
        log.kv("scorers", ", ".join(f"{k} ({v[['ref_id', 'var_id']].drop_duplicates().shape[0]:,} pairs)"
                                    for k, v in scorers.items()))

        refs = parse_conllu(FC / "reference_trees.conllu", 8)
        V = set1_variants().set_index("var_id")
        smp = pd.read_csv(args.sample, usecols=["ref_id", "var_id", "order_class"])
        units = pd.read_csv(args.units, usecols=["ref_id", "var_id", "moved_stratum"])
        pairs = set().union(*(set(map(tuple, v[["ref_id", "var_id"]].drop_duplicates().values)) for v in scorers.values()))
        cls_of = {(r, v): word_classes(refs[r], V.loc[v]) for r, v in pairs}

        rows = []
        for name, w in scorers.items():
            w = w.copy()
            w["cls"] = [cls_of[(r, v)][int(i)] for r, v, i in zip(w.ref_id, w.var_id, w.tree_idx)]
            w["signed"] = np.where(w.side == "var", w.s, -w.s)          # s_var - s_ref, summed over words
            per = w.pivot_table(index=["ref_id", "var_id"], columns="cls", values="signed", aggfunc="sum", fill_value=0.0)
            for c in CLASSES:
                if c not in per:
                    per[c] = 0.0
            per["D"] = per[CLASSES].sum(1)
            init = w[w.pos == 0].groupby(["ref_id", "var_id"]).tree_idx.agg(set)
            wi = w.merge(init.rename("init").reset_index(), on=["ref_id", "var_id"])
            per["initial"] = wi[[i in s for i, s in zip(wi.tree_idx, wi.init)]].groupby(["ref_id", "var_id"]).signed.sum()
            per["initial"] = per["initial"].fillna(0.0)
            per = per.reset_index().assign(scorer=name)
            rows.append(per)
        allp = pd.concat(rows, ignore_index=True).merge(smp, on=["ref_id", "var_id"], how="left").merge(
            units, on=["ref_id", "var_id"], how="left")
        allp.to_csv(args.out, index=False, float_format="%.4f")
        log.output(args.out, "per pair and scorer: D and its split by word class")

        rng = np.random.default_rng(707)

        def table(frame, label):
            log.h2(label)
            out = []
            for name, g in frame.groupby("scorer", sort=False):
                n = len(g)
                M = g[CLASSES + ["initial", "D"]].to_numpy()
                idx = [rng.integers(0, n, n) for _ in range(args.bootstrap)]
                bs = np.array([M[k].sum(0) for k in idx])
                shares = bs[:, :-1] / bs[:, -1:]
                est = M.sum(0)[:-1] / M.sum(0)[-1]
                lo, hi = np.percentile(shares, [2.5, 97.5], axis=0)
                out.append([name, n, M[:, -1].mean(), (M[:, -1] > 0).mean()] +
                           [f"{e:.2f} [{a:.2f}, {b:.2f}]" for e, a, b in zip(est, lo, hi)])
            log.table(["scorer", "pairs", "mean D (bits)", "D > 0"] + CLASSES + ["sentence-initial words"], out,
                      floatfmt="{:.3f}")

        common = set.intersection(*(set(map(tuple, g[["ref_id", "var_id"]].values)) for _, g in allp.groupby("scorer")))
        allc = allp[[k in common for k in map(tuple, allp[["ref_id", "var_id"]].values)]]
        log.kv("pairs scored by every scorer (used below)", f"{len(common):,}")
        table(allc, "All pairs: share of the preference D carried by each word class")
        for s in ["arguments_only", "adjuncts_only", "both"]:
            table(allc[allc.moved_stratum == s], f"Moved-unit stratum: {s}")
        table(allc[allc.order_class.isin(["SOV", "OSV"])], "Subject-object clauses (SOV and OSV references)")
        log.p("Shares are ratios of sums over pairs, so pairs with large |D| weigh more; classes can carry "
              "negative shares when those words favour the variant. Sentence-initial words overlap the classes.")

        if args.uid:
            from dominance_analysis import fit_subset, nagelkerke_r2
            from rq1_dominance import SPEC_L, SPEC_S, auc_fast, cluster_bootstrap_auc_diff, cv_predict, joachims, pair_halves
            log.h2("E2a: uniform information density")
            feats = pd.read_csv(args.features)
            L = [c for c in SPEC_L if feats[c].nunique() > 1]
            S = list(SPEC_S)
            res = []
            for name, w in scorers.items():
                w = w[w.pos >= 0]
                g = w.groupby(["ref_id", "var_id", "side"]).s
                u = pd.DataFrame({"var": g.var(ddof=0)})
                for k in POWERS:
                    u[f"pow_{k}"] = g.apply(lambda x, k=k: float((np.clip(x, 0, None) ** k).mean()))
                u = u.unstack("side")
                d = pd.DataFrame({f"d_uid_{c}": u[(c, "ref")] - u[(c, "var")] for c in ["var"] + [f"pow_{k}" for k in POWERS]})
                d = d.reset_index()
                uidc = [c for c in d.columns if c.startswith("d_uid_")]
                x = feats.merge(d, on=["ref_id", "var_id"])
                if name in args.models:
                    t = pd.concat(pd.read_csv(f) for f in sorted(glob.glob(str(rc / f"t_{name}_within_word_l2r_s*.csv"))))
                    x = x.merge(t[["ref_id", "var_id", f"t_{name}_Mean"]], on=["ref_id", "var_id"])
                    base = L + S + [f"t_{name}_Mean"]
                    blabel = "L + S + T mean"
                else:
                    base = list(L)
                    blabel = "L"
                x = x.dropna(subset=base + uidc)
                exp = joachims(x, base + uidc)
                n = pair_halves(exp)
                llnull, _ = fit_subset(exp, "y", [])
                r0 = nagelkerke_r2(fit_subset(exp, "y", base)[0], llnull, len(exp))
                r1 = nagelkerke_r2(fit_subset(exp, "y", base + uidc)[0], llnull, len(exp))
                y, grp = exp["y"].to_numpy(float), exp["grp"].to_numpy()
                p0 = cv_predict(exp[base].to_numpy(float), y, grp)
                p1 = cv_predict(exp[base + uidc].to_numpy(float), y, grp)
                dd, lo, hi, pb = cluster_bootstrap_auc_diff(y, p1, p0, n, B=args.bootstrap)
                res.append([name, blabel, len(x), r0, r1 - r0, auc_fast(y, p0), dd, lo, hi, pb])
            log.table(["scorer", "baseline", "pairs", "R² baseline", "ΔR² with UID", "AUC baseline", "ΔAUC", "95% low",
                       "95% high", "bootstrap p"], res, floatfmt="{:.4g}")


if __name__ == "__main__":
    main()
