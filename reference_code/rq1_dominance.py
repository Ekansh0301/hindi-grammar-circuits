#!/usr/bin/env python3
"""
EXPERIMENT: RQ1 dominance analysis — does transformer surprisal (T) explain
variance in Hindi word-order choice beyond lexical (L) and structural (S)
predictors?

PROTOCOL, AS SPECIFIED
  - Joachims (2002) symmetric-difference encoding: each reference-variant pair
    contributes F_ref - F_var with label 1 and its negation with label 0.
  - Firth (1993) bias-reduced logistic regression, because the separation this
    task produces makes maximum likelihood diverge.
  - Nagelkerke R^2 over all 2^K subset models; general, conditional and
    complete dominance (Budescu 1993; Azen & Budescu 2003).
  - GroupKFold by REFERENCE sentence. The sample already holds one variant per
    reference, so grouping is belt and braces rather than the only guard.
  - Significance: McNemar for paired prediction disagreement, a bootstrap over
    references for the paired AUC difference (cluster_bootstrap_auc_diff, which
    replaced DeLong), Benjamini-Hochberg across the whole family of tests reported here.

WHAT CHANGED UNDER THIS SCRIPT relative to every earlier dominance run:
  - S is computed from REPAIRED variant trees. The shipped trees reattach
    displaced arcs to the root, which let arc count alone name the reference in
    92.5% of pairs (Results/rq1_structural_leak.md).
  - The sample is stratified by word-order type and severity quartile, and
    word-order labels come from the verb-group rule, not the VM-only labelling
    that ships as word_orders.csv (Results/rq1_word_order_labels.md).
  - T uses within_word_l2r masking, verified against minicons.
  - L carries two added order-sensitive lexical features, reported separately
    from the spec-only set so the specified analysis stands on its own.

The spec-only and extended feature sets are BOTH reported. If they disagree,
that disagreement is the result, and is not resolved by picking one.
"""
import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from hutb_corpus import BASE
from runlog import RunLog
from dominance_analysis import fit_firth, nagelkerke_r2, run_dominance_analysis

# d_kenlm_mean_filt scores with the same token filter the model was trained
# with, so train and test distributions match and OOV is zero by construction.
# The unfiltered column is kept in the feature file for the comparison reported
# in rq1_kenlm_oov_impact.md, but is not the predictor.
SPEC_L = ["d_kenlm_mean_filt", "d_logfreq", "d_semantic_sim", "d_case_density",
          "d_same_case_bigram"]
EXTRA_L = ["d_semsim_adj_mean", "d_semsim_adj_max"]
# Declared extensions, each reported as its own set so its effect is visible
# rather than folded into one "everything" number.
CASE_L = ["d_casemarker_mean"]
WEIGHT_S = ["d_weight_inv_norm"]
SPEC_S = ["d_dep_mean", "d_dlt_mean", "d_is_inv_norm"]


def joachims(df, cols):
    """Symmetric expansion: the pair contributes its difference with label 1 and
    the negated difference with label 0, so the classifier cannot learn an
    intercept that encodes the answer."""
    pos = df[cols].copy()
    pos["y"] = 1
    pos["grp"] = df["ref_id"].values
    neg = (-df[cols]).copy()
    neg["y"] = 0
    neg["grp"] = df["ref_id"].values
    return pd.concat([pos, neg], ignore_index=True)


def cv_predict(X, y, groups, n_splits=5, seed=707):
    """Out-of-fold predicted probabilities from Firth logistic regression,
    grouped by reference so no reference appears in both train and test."""
    from sklearn.model_selection import GroupKFold
    import statsmodels.api as sm
    pred = np.full(len(y), np.nan)
    gkf = GroupKFold(n_splits=n_splits)
    for tr, te in gkf.split(X, y, groups):
        Xtr = sm.add_constant(X[tr], has_constant="add")
        beta = fit_firth(Xtr, y[tr], return_beta=True)
        Xte = sm.add_constant(X[te], has_constant="add")
        pred[te] = 1 / (1 + np.exp(-Xte @ beta))
    return pred


def auc(y, p):
    o = np.argsort(p)
    r = np.empty(len(p), float)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and p[o[j + 1]] == p[o[i]]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    n1 = y.sum()
    n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def pair_halves(exp):
    """The Joachims expansion stacks every pair's forward row, then every pair's
    mirror row, in the same order (see joachims()). Checked, not assumed: if the
    two halves do not carry the same reference ids in the same order, the pair
    structure every test below relies on does not hold."""
    n = len(exp) // 2
    g = exp["grp"].to_numpy()
    if len(exp) % 2 or not (g[:n] == g[n:]).all():
        raise AssertionError("expanded rows are not two aligned halves of the same pairs")
    return n


def mcnemar_pairs(y, p1, p2, n):
    """Exact McNemar at the PAIR level.

    Only the forward row of each pair is used. Its mirror row carries the same
    decision (the model is fitted on a symmetric design), so counting both --
    as an earlier version did -- doubles b and c and overstates significance.
    """
    from scipy import stats
    yf = y[:n]
    c1, c2 = (p1[:n] > 0.5) == (yf == 1), (p2[:n] > 0.5) == (yf == 1)
    b = int((c1 & ~c2).sum())
    c = int((~c1 & c2).sum())
    p = float(stats.binomtest(b, b + c, 0.5).pvalue) if b + c else 1.0
    return b, c, p


def auc_fast(y, p):
    from sklearn.metrics import roc_auc_score
    return roc_auc_score(y, p)


def bootstrap_index(rng, n, clusters=None):
    """Indices of one bootstrap replicate: pairs when `clusters` is None, whole clusters otherwise.

    `clusters` is one label per pair (for example the document a reference comes from). Resampling
    documents keeps the pairs of a document together, which is what an interval must do when pairs from
    one document share its topic, its writer and its vocabulary.
    """
    if clusters is None:
        return rng.integers(0, n, n)
    uniq, inv = np.unique(clusters, return_inverse=True)
    rows_of = [np.flatnonzero(inv == i) for i in range(len(uniq))]
    return np.concatenate([rows_of[i] for i in rng.integers(0, len(uniq), len(uniq))])


def cluster_bootstrap_auc_diff(y, p1, p2, n, B=2000, seed=707, clusters=None):
    """AUC(p1) - AUC(p2), with a bootstrap that resamples REFERENCES (or `clusters`, when given).

    Replaces DeLong's test. DeLong's variance assumes the positive and negative
    samples are independent; in the Joachims design every positive row has a
    mirror negative row from the same pair, so DeLong treats dependent rows as
    independent evidence (the clustered-ROC problem; Obuchowski 1997). Resampling
    whole pairs -- and with one variant per reference, whole references -- keeps
    each positive row with its own mirror in every replicate.
    Two-sided p from the bootstrap distribution, floored at 1/B.
    """
    rng = np.random.default_rng(seed)
    obs = auc_fast(y, p1) - auc_fast(y, p2)
    diffs = np.empty(B)
    for b in range(B):
        k = bootstrap_index(rng, n, clusters)
        idx = np.concatenate([k, k + n])
        diffs[b] = auc_fast(y[idx], p1[idx]) - auc_fast(y[idx], p2[idx])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return obs, lo, hi, max(p, 1.0 / B)


def bh(pvals):
    """Benjamini-Hochberg adjusted p-values, in the input order."""
    p = np.asarray(pvals, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.empty(n)
    prev = 1.0
    for rank, i in enumerate(reversed(o), 1):
        prev = min(prev, p[i] * n / (n - rank + 1))
        adj[i] = prev
    return adj


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--features", default=str(BASE / "Results_Checks" / "rq1_features_all.csv"))
    ap.add_argument("--t-features", nargs="+", required=True,
                    help="one or more t_<model>_*.csv files from rq1_transformer_surprisal.py")
    ap.add_argument("--surprisal", default="Mean",
                    help="which T feature is the spec measure (proposal: Mean)")
    ap.add_argument("--extended-t", action="store_true",
                    help="use all nine T features instead of the specified mean only")
    ap.add_argument("--is-in-L", action="store_true",
                    help="spec robustness check: move information status from S into L")
    ap.add_argument("--no-is", action="store_true",
                    help="robustness: drop information status from S so every pair is kept. "
                         "IS needs >= 2 preverbal arguments on both sides, which removes "
                         "2,238 of 10,284 pairs and so changes the population analysed")
    ap.add_argument("--all-pairs", action="store_true",
                    help="drop both predictors that need >= 2 preverbal arguments, so all pairs are kept")
    ap.add_argument("--order-classes", nargs="+", default=None,
                    help="restrict to pairs whose reference is in these word-order classes (column "
                         "order_class of --sample), e.g. SOV OSV for clauses with a subject-object "
                         "pair (SET1_CONSTRUCTION_PLAN.md, 9b)")
    ap.add_argument("--sample", default=str(BASE / "Results_Checks" / "rq1_sample_n12000.csv"))
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--tag", default="rq1_dominance")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="RQ1 dominance analysis with the repaired trees, the stratified "
                        "sample and spec-compliant masking.") as log:
        feats = pd.read_csv(args.features)
        if args.order_classes:
            smp = pd.read_csv(args.sample, usecols=["ref_id", "var_id", "order_class"])
            keep = smp[smp.order_class.isin(args.order_classes)][["ref_id", "var_id"]]
            feats = feats.merge(keep, on=["ref_id", "var_id"])
            log.kv("restricted to reference word-order classes", ", ".join(args.order_classes))
        log.kv("pairs with L and S", f"{len(feats):,}")

        tf = {}
        for p in args.t_features:
            d = pd.read_csv(p)
            model = [c for c in d.columns if c.startswith("t_")][0].split("_")[1]
            tf.setdefault(model, []).append(d)
        models = {m: pd.concat(v, ignore_index=True) for m, v in tf.items()}
        for m, d in models.items():
            log.kv(f"pairs scored by {m}", f"{len(d):,}")

        common = None
        for d in models.values():
            ids = set(map(tuple, d[["ref_id", "var_id"]].values))
            common = ids if common is None else (common & ids)
        log.kv("pairs scored by EVERY model (the analysis set)", f"{len(common):,}")
        log.p("Models are compared only on pairs all of them scored. Skips fall on the "
              "longest sentences, so comparing models on their own scored sets would "
              "compare them on different samples.")

        results = {}
        tests = []
        for m, d in models.items():
            log.h2(f"model: {m}")
            df = feats.merge(d, on=["ref_id", "var_id"], how="inner")
            df = df[[tuple(x) in common for x in df[["ref_id", "var_id"]].values]]

            tcols = ([c for c in df.columns if c.startswith(f"t_{m}_")]
                     if args.extended_t else [f"t_{m}_{args.surprisal}"])
            L = [c for c in SPEC_L if c in df.columns]
            extra = [c for c in EXTRA_L if c in df.columns]
            S = [c for c in SPEC_S if c in df.columns]
            if args.no_is:
                S = [c for c in S if not c.startswith("d_is")]
                log.kv("robustness check", "information status dropped from S")
            if args.all_pairs:
                # Two specified predictors are undefined unless a sentence has at least
                # two preverbal arguments: information status (S) and the preverbal
                # semantic similarity L(iii). Both go missing on the SAME 2,238 pairs,
                # so dropping only one of them recovers nothing -- an earlier run of
                # --no-is found exactly that. Dropping both is the only way to analyse
                # every pair and see whether restricting to multi-argument sentences
                # changes the conclusion.
                S = [c for c in S if not c.startswith("d_is")]
                L = [c for c in L if c != "d_semantic_sim"]
                extra = []
                log.kv("robustness check", "IS and preverbal semantic similarity dropped; every pair kept")
            if args.is_in_L:
                moved = [c for c in S if c.startswith("d_is")]
                S = [c for c in S if c not in moved]
                L = L + moved
                log.kv("robustness check", "information status moved from S into L")

            # Running the extended set when no extended features exist would fit
            # the identical model twice and enter the SAME test twice into the
            # Benjamini-Hochberg family, inflating the correction against us.
            cm = [c for c in CASE_L if c in df.columns]
            ew = [c for c in WEIGHT_S if c in df.columns]
            S_spec = list(S)
            sets = [("spec-only", L, S_spec)]
            if extra:
                sets.append(("L + semantic similarity", L + extra, S_spec))
            if extra and cm and ew:
                sets.append(("all extensions (L + semsim + case markers; S + end-weight)",
                             L + extra + cm, S_spec + ew))
            if not extra:
                log.note("The added lexical features are not present in this feature "
                         "file, so only the spec-only set is fitted.")
            # Extensions that need extra structure (end-weight needs >= 2 preverbal
            # constituents) have more missing values, so after dropna they are fitted
            # on FEWER rows than the spec set. Comparing their R^2 or AUC to the spec
            # set would then mix the feature's effect with a change of sample. So
            # every set is ALSO fitted on the rows complete for all of them, and the
            # extension comparison is read from that matched block only. The spec
            # set on its own maximal rows stays the primary analysis.
            if len(sets) > 1:
                need = sorted({c for _, a, b in sets for c in a + b} | set(tcols))
                matched_idx = df[need].dropna().index
                sets = sets + [(f"{lab} [matched rows]", a, b) for lab, a, b in sets]
                log.kv("rows complete for every set (the matched block)", f"{len(matched_idx):,}")
            else:
                matched_idx = None
            for label, lset, S in sets:
                S = list(S)
                cols = lset + S + tcols
                base_df = df.loc[matched_idx] if label.endswith("[matched rows]") else df
                sub = base_df[["ref_id"] + cols].dropna()
                # A predictor that is constant on the fitted rows carries no
                # information and makes X'WX singular, so Firth cannot invert it.
                # Two of the five specified lexical predictors ARE constant here --
                # mean log-frequency and case density are functions of the word
                # multiset, which a permutation cannot change -- so this is not a
                # numerical nuisance to be regularised away, it is the design
                # asserting itself. They are dropped from the MODEL and kept in the
                # REPORT: a predictor that is provably zero is a result.
                const = [c for c in cols if sub[c].nunique() <= 1]
                if const:
                    log.kv("dropped as constant (zero variance under permutation)",
                           ", ".join(const))
                    cols = [c for c in cols if c not in const]
                    lset = [c for c in lset if c not in const]
                    S = [c for c in S if c not in const]
                    tcols = [c for c in tcols if c not in const]
                    sub = base_df[["ref_id"] + cols].dropna()
                if not (lset and S and tcols):
                    log.note("A whole predictor block is empty after dropping constants; "
                             "the three-way decomposition is not defined here.")
                    continue
                if len(sub) < 200:
                    log.note(f"{label}: only {len(sub)} complete rows after dropping "
                             f"missing values — too few to fit; check predictor coverage")
                    continue
                log.h3(f"{label}  (n pairs = {len(sub):,})")
                log.kv("L", ", ".join(lset))
                log.kv("S", ", ".join(S))
                log.kv("T", f"{len(tcols)} feature(s): " + ", ".join(tcols))
                exp = joachims(sub, cols)
                res = run_dominance_analysis(exp, "y",
                                             {"L": lset, "S": S, "T": tcols}, verbose=False)
                full = frozenset(["L", "S", "T"])
                log.table(["block", "general dominance", "conditional k=0", "k=1", "k=2"],
                          [[nm, res["general_dominance"][nm]]
                           + [res["conditional_dominance"][nm][k] for k in range(3)]
                           for nm in ("L", "S", "T")])
                log.kv("full-model Nagelkerke R^2", f"{res['subset_r2'][full]:.4f}")
                log.kv("dR^2(T | L)",
                       f"{res['subset_r2'][frozenset(['L','T'])] - res['subset_r2'][frozenset(['L'])]:.4f}")
                log.kv("dR^2(T | S)",
                       f"{res['subset_r2'][frozenset(['S','T'])] - res['subset_r2'][frozenset(['S'])]:.4f}")
                log.kv("dR^2(T | L,S)",
                       f"{res['subset_r2'][full] - res['subset_r2'][frozenset(['L','S'])]:.4f}")

                # out-of-fold comparison of L+S against L+S+T
                y = exp["y"].to_numpy().astype(float)
                g = exp["grp"].to_numpy()
                npair = pair_halves(exp)
                p_ls = cv_predict(exp[lset + S].to_numpy(float), y, g)
                p_all = cv_predict(exp[cols].to_numpy(float), y, g)
                a1, a2 = auc_fast(y, p_all), auc_fast(y, p_ls)
                d, lo, hi, pbs = cluster_bootstrap_auc_diff(y, p_all, p_ls, npair,
                                                             B=args.bootstrap)
                b, c, pmc = mcnemar_pairs(y, p_all, p_ls, npair)
                log.table(["comparison", "AUC L+S+T", "AUC L+S", "ΔAUC", "95% low", "95% high",
                           "bootstrap p", "McNemar b", "c", "McNemar p (pairs)"],
                          [[f"{m} / {label}", a1, a2, d, lo, hi, pbs, b, c, pmc]],
                          floatfmt="{:.4g}")
                tests.append((f"{m} / {label} / AUC (reference bootstrap)", pbs))
                tests.append((f"{m} / {label} / McNemar (pairs)", pmc))
                results[(m, label)] = res

        if tests:
            log.h2("Benjamini-Hochberg correction across the reported family")
            adj = bh([p for _, p in tests])
            log.table(["test", "raw p", "BH-adjusted p", "significant at 0.05"],
                      [[n, p, a, "yes" if a < 0.05 else "no"]
                       for (n, p), a in zip(tests, adj)], floatfmt="{:.4g}")
            log.p("The family is every test in this run. Correcting within the run rather "
                  "than per comparison is what keeps the count honest when several models "
                  "and two feature sets are reported together.")


if __name__ == "__main__":
    main()
