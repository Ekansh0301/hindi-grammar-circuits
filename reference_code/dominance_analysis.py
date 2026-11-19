#!/usr/bin/env python3
"""
Dominance analysis engine -- Section 6.3's actual method for RQ1/H1, and
the single biggest piece of missing methodology identified in the audit.
Doesn't exist anywhere else in this project or in Chinmay's pipeline
(which used simple classifier-F1 comparison + PCA instead -- a different,
simpler method).

Method: Budescu (1993) / Azen & Budescu (2003), cited in the proposal as
ref [6]. For K predictor SETS (here L, S, T), fit all 2^K subset logistic
regressions on the Joachims difference features, compute Nagelkerke's R^2
for each, and decompose each set's contribution three ways:
  - General dominance: average incremental R^2 across ALL 2^(K-1) subsets
    of the other predictor sets.
  - Conditional dominance: that same average, broken out BY model size
    (0, 1, ... K-1 other predictors already in the model) -- a profile,
    not one collapsed number.
  - Complete dominance: the strict pairwise version -- does T's
    incremental R^2 exceed L's in EVERY matched comparison, not just on
    average? This is what "T completely dominates L" actually requires.

Section 6.3's own words: "The critical diagnostic is the conditional
redundancy pattern, not general dominance of T over S... A lexical
dominance pattern shows small delta-R^2(T|L) and large delta-R^2(T|S)...
A structural sensitivity pattern shows the opposite." That's exactly what
`conditional_dominance` reports per predictor set below.

Nagelkerke R^2 is used specifically (not McFadden's or Cox-Snell's alone)
because it's the monotonic transform of the likelihood ratio that
decomposes additively over the logistic-regression likelihood -- the
proposal's own footnote states this is what makes the additive dominance
decomposition mathematically valid in the first place.

USAGE
    python3 dominance_analysis.py --data <csv> --predictor-config L:col1,col2 S:col3,col4 T:col5 --label-col Label
"""
import argparse
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


# ── NAGELKERKE R^2 ──────────────────────────────────────────────────────
def nagelkerke_r2(llf, llnull, n):
    """Nagelkerke (1991): normalizes Cox & Snell's R^2 by its own maximum
    achievable value, so it reaches 1.0 for a perfect model -- Cox-Snell
    alone caps below 1 for binary outcomes, which breaks the additive
    decomposition the proposal's methodology depends on."""
    cs_r2 = 1 - np.exp((2 / n) * (llnull - llf))
    max_r2 = 1 - np.exp((2 / n) * llnull)
    return cs_r2 / max_r2


def fit_firth(X, y, max_iter=200, tol=1e-8, return_beta=False):
    """Firth (1993) bias-reduced logistic regression, via the standard
    IRLS-with-hat-matrix-correction algorithm (Heinze & Schemper 2002).

    Needed because plain MLE (statsmodels.Logit) hit a singular Hessian on
    the real pilot data -- confirmed this is (quasi-)complete separation,
    not a bug: this classifier is already known from prior HUTB work to
    hit 90%+ accuracy on surprisal alone, so on a few hundred rows even a
    handful of predictors separate the classes almost perfectly, and
    unregularized MLE diverges. The proposal's own ridge-regression
    fallback (Section 6.3) is explicitly scoped to collinearity (condition
    index >= 30), not separation, and ridge would bias the variance
    partitioning dominance analysis depends on -- the proposal says so
    directly. Firth's method is the standard statistical fix for
    separation specifically, because it corrects the likelihood itself
    (a principled small-sample bias correction) rather than adding an
    arbitrary shrinkage penalty, so likelihood-based inference (LRTs,
    Nagelkerke R^2 built on the log-likelihood) stays valid.

    Verified against statsmodels on non-separable synthetic data first
    (coefficients matched to within 0.004) before trusting it on data
    where plain MLE actually fails.

    Returns (penalized_loglik, n_params), or the coefficient vector when
    `return_beta` is set -- needed for out-of-fold prediction, where the fitted
    model has to be applied to held-out rows rather than only scored."""
    n, p = X.shape
    beta = np.zeros(p)
    for _ in range(max_iter):
        eta = X @ beta
        pi = 1 / (1 + np.exp(-eta))
        W = np.clip(pi * (1 - pi), 1e-10, None)
        XtWX = (X.T * W) @ X
        XtWX_inv = np.linalg.inv(XtWX)
        h = W * np.einsum("ij,jk,ik->i", X, XtWX_inv, X)
        U_star = X.T @ (y - pi + h * (0.5 - pi))
        delta = XtWX_inv @ U_star
        beta_new = beta + delta
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new
    eta = X @ beta
    pi = 1 / (1 + np.exp(-eta))
    pi_c = np.clip(pi, 1e-12, 1 - 1e-12)
    W = np.clip(pi * (1 - pi), 1e-10, None)
    XtWX = (X.T * W) @ X
    _, logdet = np.linalg.slogdet(XtWX)
    penalized_ll = np.sum(y * np.log(pi_c) + (1 - y) * np.log(1 - pi_c)) + 0.5 * logdet
    if return_beta:
        return beta
    return penalized_ll, p


def fit_subset(df, y_col, predictor_cols):
    """Fits Firth logistic regression on the given predictor columns
    (empty list = null/intercept-only model). Returns (llf, n_params)."""
    y = df[y_col].to_numpy().astype(float)
    if predictor_cols:
        X = sm.add_constant(df[predictor_cols].to_numpy())
    else:
        X = np.ones((len(df), 1))
    return fit_firth(X, y)


# ── CORE DOMINANCE ANALYSIS ─────────────────────────────────────────────
def run_dominance_analysis(df, y_col, predictor_sets, verbose=True):
    """predictor_sets: dict {set_name: [column, ...]}, e.g.
    {'L': [...], 'S': [...], 'T': [...]}. Fits all 2^K subset models
    exactly once (r=0, the empty combo, is guaranteed first by
    itertools.combinations' ordering, so llnull is always known before
    it's needed for any other subset's R^2)."""
    names = list(predictor_sets.keys())
    K = len(names)
    n = len(df)

    subset_llf, subset_nparams, subset_r2 = {}, {}, {}
    llnull = None

    if verbose:
        print(f"[*] Fitting all {2**K} subset models on n={n} rows ...")
    for r in range(K + 1):
        for combo in itertools.combinations(names, r):
            cols = [c for nm in combo for c in predictor_sets[nm]]
            llf, nparams = fit_subset(df, y_col, cols)
            key = frozenset(combo)
            subset_llf[key] = llf
            subset_nparams[key] = nparams
            if not combo:
                llnull = llf
            subset_r2[key] = nagelkerke_r2(llf, llnull, n)
            if verbose:
                label = "+".join(sorted(combo)) if combo else "Null"
                print(f"    {label:<12} R^2={subset_r2[key]:.4f}  llf={llf:.2f}  k={nparams}")

    # ── General + conditional dominance ─────────────────────────────
    general_dominance, conditional_dominance = {}, {}
    for target in names:
        others = [nm for nm in names if nm != target]
        all_deltas = []
        cond = {}
        for r in range(len(others) + 1):
            level_deltas = []
            for combo in itertools.combinations(others, r):
                base_key = frozenset(combo)
                full_key = frozenset(combo) | {target}
                delta = subset_r2[full_key] - subset_r2[base_key]
                level_deltas.append(delta)
                all_deltas.append(delta)
            cond[r] = float(np.mean(level_deltas))
        conditional_dominance[target] = cond
        # General dominance is the mean of the CONDITIONAL dominance values across
        # subset SIZES (Budescu 1993; Azen & Budescu 2003) -- average within each
        # size first, then across sizes. An earlier version took the mean over all
        # subsets pooled, which weights each size by how many subsets it has: with
        # three blocks the size-1 level has two subsets and was counted twice. That
        # is not general dominance, and it is detectable, because the defining
        # property below failed by ~0.15 in every cell (weights summed to ~0.81
        # against a full-model R^2 of ~0.96).
        general_dominance[target] = float(np.mean(list(cond.values())))

    # Defining property: general dominance weights sum to the full-model R^2.
    # Checked on every run so this can never silently regress again.
    gd_sum = sum(general_dominance.values())
    r2_full = subset_r2[frozenset(names)]
    if abs(gd_sum - r2_full) > 1e-6:
        raise AssertionError(
            f"general dominance weights sum to {gd_sum:.6f} but full-model R^2 is "
            f"{r2_full:.6f}; the decomposition is not additive, so it is not general "
            f"dominance")

    # ── Complete dominance (pairwise) ───────────────────────────────
    def complete_dominance(a, b):
        rest = [nm for nm in names if nm not in (a, b)]
        a_ge_b_all, b_ge_a_all = True, True
        rows = []
        for r in range(len(rest) + 1):
            for combo in itertools.combinations(rest, r):
                base = frozenset(combo)
                delta_a = subset_r2[base | {a}] - subset_r2[base]
                delta_b = subset_r2[base | {b}] - subset_r2[base]
                rows.append((sorted(combo) or ["(none)"], delta_a, delta_b))
                if delta_a < delta_b:
                    a_ge_b_all = False
                if delta_b < delta_a:
                    b_ge_a_all = False
        if a_ge_b_all and not b_ge_a_all:
            verdict = f"{a} completely dominates {b}"
        elif b_ge_a_all and not a_ge_b_all:
            verdict = f"{b} completely dominates {a}"
        elif a_ge_b_all and b_ge_a_all:
            verdict = "tied in every matched comparison"
        else:
            verdict = "no complete dominance either way -- only general/conditional apply"
        return verdict, rows

    # ── LRT: full model vs each major reduced model ─────────────────
    def lrt(full_key, reduced_key):
        stat = 2 * (subset_llf[full_key] - subset_llf[reduced_key])
        df_diff = subset_nparams[full_key] - subset_nparams[reduced_key]
        p = stats.chi2.sf(stat, df_diff) if df_diff > 0 else float("nan")
        return stat, df_diff, p

    return {
        "names": names, "n": n,
        "subset_r2": subset_r2, "subset_llf": subset_llf, "subset_nparams": subset_nparams,
        "general_dominance": general_dominance, "conditional_dominance": conditional_dominance,
        "complete_dominance": complete_dominance, "lrt": lrt,
    }


def print_report(results, l_name="L", s_name="S", t_name="T"):
    names = results["names"]
    full_key = frozenset(names)

    print("\n" + "=" * 70)
    print("GENERAL DOMINANCE (average incremental Nagelkerke R^2)")
    print("=" * 70)
    for nm in names:
        print(f"  {nm:<4} {results['general_dominance'][nm]:.4f}")

    print("\n" + "=" * 70)
    print("CONDITIONAL DOMINANCE (by model size -- the diagnostic that actually matters)")
    print("=" * 70)
    for nm in names:
        cond = results["conditional_dominance"][nm]
        profile = "  ".join(f"size{k}={v:.4f}" for k, v in sorted(cond.items()))
        print(f"  {nm:<4} {profile}")

    if t_name in names and l_name in names and s_name in names:
        d_t_given_l = results["subset_r2"][frozenset({l_name, t_name})] - results["subset_r2"][frozenset({l_name})]
        d_t_given_s = results["subset_r2"][frozenset({s_name, t_name})] - results["subset_r2"][frozenset({s_name})]
        print(f"\n  Section 6.3's actual diagnostic:")
        print(f"    delta R^2({t_name}|{l_name}) = {d_t_given_l:.4f}   (lexical-dominance pattern needs this SMALL, <0.01)")
        print(f"    delta R^2({t_name}|{s_name}) = {d_t_given_s:.4f}   (lexical-dominance pattern needs this LARGE, >0.03)")
        if d_t_given_l < 0.01 and d_t_given_s > 0.03:
            print(f"    -> LEXICAL DOMINANCE pattern (H1, Section 3, supported)")
        elif d_t_given_l > 0.03 and d_t_given_s < 0.01:
            print(f"    -> STRUCTURAL SENSITIVITY pattern (H1 falsified)")
        else:
            print(f"    -> Neither clean pattern -- report both deltas as-is, this is a real, informative outcome too")

    print("\n" + "=" * 70)
    print("COMPLETE DOMINANCE (pairwise, strict)")
    print("=" * 70)
    for a, b in itertools.combinations(names, 2):
        verdict, _ = results["complete_dominance"](a, b)
        print(f"  {a} vs {b}: {verdict}")

    print("\n" + "=" * 70)
    print("LIKELIHOOD RATIO TESTS (full model vs each major reduced model)")
    print("=" * 70)
    for nm in names:
        reduced_key = frozenset(n for n in names if n != nm)
        stat, df_diff, p = results["lrt"](full_key, reduced_key)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
        print(f"  Full vs (Full - {nm}):  chi2={stat:.2f}  df={df_diff}  p={p:.4g}  {sig}")

    print(f"\nFull model ({'+'.join(names)}) Nagelkerke R^2 = {results['subset_r2'][full_key]:.4f}")
    print(f"Null model R^2 = {results['subset_r2'][frozenset()]:.4f}  (should be ~0.0, sanity check)")


def main():
    parser = argparse.ArgumentParser(description="Dominance analysis (Budescu/Azen) for the Joachims classifier")
    parser.add_argument("--data", required=True, help="CSV with difference features + a binary label column")
    parser.add_argument("--label-col", default="Label")
    parser.add_argument("--l-cols", nargs="+", default=[])
    parser.add_argument("--s-cols", nargs="+", default=[])
    parser.add_argument("--t-cols", nargs="+", default=[])
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    print(f"[*] Loaded {len(df)} rows from {args.data}")

    predictor_sets = {}
    if args.l_cols:
        predictor_sets["L"] = args.l_cols
    if args.s_cols:
        predictor_sets["S"] = args.s_cols
    if args.t_cols:
        predictor_sets["T"] = args.t_cols

    needed_cols = [c for cols in predictor_sets.values() for c in cols] + [args.label_col]
    missing = [c for c in needed_cols if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing columns in {args.data}: {missing}")

    df = df.dropna(subset=needed_cols)
    print(f"[*] {len(df)} rows after dropping NaNs in needed columns")

    results = run_dominance_analysis(df, args.label_col, predictor_sets)
    print_report(results)


if __name__ == "__main__":
    main()
