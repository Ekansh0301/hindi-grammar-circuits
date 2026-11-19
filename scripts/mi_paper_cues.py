#!/usr/bin/env python3
"""
P5 (docs/PAPER_EXPERIMENTS.md): cue strata. Does the word-order circuit compute more than adjacency statistics?
Local CPU analysis of existing outputs; numpy, scipy and csv only (no torch, so mi_lib is not imported; the small
helpers below are copies of mi_followup's numpy-only ones).

DESIGN (declared before the run)
  Data: the 471 fresh pairs of outputs/size_wordorder_<model>.npz (per-pair patching of the 10 heads, each of 5 MLPs,
  the 5 MLPs jointly) joined by (ref_id, var_id) to data/features/rq1_features_ngram.csv and _all.csv. All 471 must be
  found, none duplicated.
  Gap of a pair = f_clean - f_corrupt (bits; positive: the model finds the reordered sentence more surprising, i.e.
  prefers the written order). Share restored by a set = ratio of sums of (res_j - f_corrupt) over gaps, over pairs with
  |gap| > 0.05 (the gap floor).
  SIGN CHECK (mandatory, before any stratification): the d_ features are reference minus variant (reference_code states
  this for the thesis's per-sentence scores), so for a surprisal-type cue a NEGATIVE value means the written sentence is
  the less surprising one. The direction is not taken on trust: the script prints the Spearman of each cue with the gap
  and aborts if the lexical cue's correlation with the gap does not have the sign that convention predicts (negative).
  STRATA by the lexical cue d_kenlm_mean_filt (second analysis: d_ngram2_mean_filt): AGREES if the cue favours the
  written order (d < 0), DISAGREES if it favours the reordered one (d > 0); cue exactly 0 or missing: excluded, counted.
  Per stratum: pairs, documents, pairs above the floor, share preferring the written order (gap > 0), mean gap, share
  restored by the 10 heads and by the 5 MLPs jointly with a document-bootstrap 95% interval (descriptive).
  PRIMARY RULE (as follow-up 1's size rule), for each of the two quantities the difference disagrees minus agrees with a
  document-bootstrap 95% interval: CUE-INDEPENDENT if both intervals lie within +-0.10; CUE-DEPENDENT if either point
  estimate lies outside +-0.10 and its interval excludes 0; INCONCLUSIVE otherwise; INCONCLUSIVE if either stratum has
  fewer than 40 pairs above the floor.
  DESCRIPTIVE: Spearman of each cue (d_kenlm_mean_filt, d_ngram2_mean_filt, d_dep_total, d_is_inv_norm,
  d_casemarker_mean, kendall) with the gap and with the 5 MLPs' joint effect in bits; OLS of the gap on the standardised
  cue families (lexical, distance, structure), labelled descriptive.
  Outputs: outputs/cues_<model>.csv and records/mi_paper_cues_<model>.md.
"""
import argparse
import csv
import os
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("HUTB_RESULTS_DIR", str(ROOT / "course_runs" / "records"))
sys.path.insert(0, str(ROOT / "reference_code"))
from runlog import RunLog  # noqa: E402

OUT = Path(os.environ.get("MI_OUT", ROOT / "course_runs" / "outputs"))
CUES = ["d_kenlm_mean_filt", "d_ngram2_mean_filt", "d_dep_total", "d_is_inv_norm", "d_casemarker_mean"]
BAND = 0.10


def fmt(r, ci=None):
    return f"{r:.3f}" if ci is None else f"{r:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


def _group_sums(num, den, docs, g):
    u = sorted(set(docs.tolist()))
    pos = {k: i for i, k in enumerate(u)}
    idx = np.array([pos[d] for d in docs])
    n, d = np.zeros(len(u)), np.zeros(len(u))
    np.add.at(n, idx[g], num[g])
    np.add.at(d, idx[g], den[g])
    return n, d


def boot_ratio(num, den, docs, g, B=2000, seed=707):
    """Ratio of sums over mask g with a document-bootstrap 95% percentile interval (descriptive)."""
    n, d = _group_sums(num, den, docs, g)
    pick = np.random.default_rng(seed).integers(0, len(n), size=(B, len(n)))
    r = n[pick].sum(1) / d[pick].sum(1)
    return float(n.sum() / d.sum()), (float(np.nanpercentile(r, 2.5)), float(np.nanpercentile(r, 97.5)))


def boot_diff_ratio(num, den, docs, g1, g2, B=2000, seed=707):
    """Ratio(g2) - ratio(g1) with a document-bootstrap 95% interval (copy of mi_followup's helper)."""
    n1, d1 = _group_sums(num, den, docs, g1)
    n2, d2 = _group_sums(num, den, docs, g2)
    pick = np.random.default_rng(seed).integers(0, len(n1), size=(B, len(n1)))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = n2[pick].sum(1) / d2[pick].sum(1) - n1[pick].sum(1) / d1[pick].sum(1)
    if np.isnan(r).mean() > 0.01:
        raise SystemExit("more than 1% of bootstrap draws missed every document of a group")
    pt = n2.sum() / d2.sum() - n1.sum() / d1.sum()
    return float(pt), (float(np.nanpercentile(r, 2.5)), float(np.nanpercentile(r, 97.5)))


def read_features():
    rows = {}
    for name in ("rq1_features_ngram.csv", "rq1_features_all.csv"):
        with open(ROOT / "data" / "features" / name, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                key = (r["ref_id"], r["var_id"])
                if key in rows and name.endswith("ngram.csv"):
                    raise SystemExit(f"duplicate key in {name}: {key}")
                rows.setdefault(key, {}).update({k: v for k, v in r.items() if k not in ("ref_id", "var_id")})
    return rows


def tofloat(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else np.nan
    except (TypeError, ValueError):
        return np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=["muril", "xlmrlarge"])
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--min-stratum", type=int, default=40)
    ap.add_argument("--boot", type=int, default=2000)
    args = ap.parse_args()
    z = np.load(OUT / f"size_wordorder_{args.model}.npz", allow_pickle=True)
    res, fc, fx = z["res"], z["f_clean"], z["f_corrupt"]
    ids, docs, kendall = z["ids"], z["docs"], z["kendall"]
    names = [str(s) for s in z["set_names"]]
    assert names[0] == "10 heads" and names[-1] == "5 MLPs jointly", names
    n = len(ids)
    gap = fc - fx
    keep = np.abs(gap) > args.min_gap

    with RunLog(f"mi_paper_cues_{args.model}", __file__, args,
                purpose="P5: cue strata of the word-order circuit (local, existing outputs)") as log:
        feats = read_features()
        keys = [tuple(s.split("|")) for s in ids]
        assert len(set(keys)) == n, "duplicate pair ids"
        missing = [k for k in keys if k not in feats]
        assert not missing, f"{len(missing)} pairs not found in features, e.g. {missing[:2]}"
        X = {c: np.array([tofloat(feats[k].get(c)) for k in keys]) for c in CUES}
        X["kendall"] = kendall.astype(float)
        log.h2("Join")
        log.kv("pairs joined", f"{n} of {n}, none duplicated")
        log.kv("documents", len(set(docs.tolist())))
        log.kv("pairs above the gap floor", f"{int(keep.sum())} (|gap| > {args.min_gap} bits)")
        log.kv("missing values", ", ".join(f"{c} {int(np.isnan(X[c]).sum())}" for c in CUES))

        heads_num, mlps_num = res[:, 0] - fx, res[:, -1] - fx
        log.h2("Overall share restored (whole set, for plausibility against follow-up 1)")
        for j, nm in enumerate(names):
            r, ci = boot_ratio(res[:, j] - fx, gap, docs, keep, args.boot)
            log.kv(nm, fmt(r, ci))

        # ---- sign check
        log.h2("Sign check (before any stratification)")
        log.p("Convention. The d_ features are reference minus variant (the thesis scripts define per-sentence "
              "differences as reference minus variant, e.g. rq1_late_ablation: d = ref_Mean - var_Mean; the "
              "surprisal-type cues d_kenlm and d_ngram2 are n-gram surprisal differences). Reference is the written "
              "sentence, so a NEGATIVE value of d_kenlm_mean_filt or d_ngram2_mean_filt means the written sentence is "
              "less surprising to the n-gram model, i.e. the cue favours the written order. The pair's gap is "
              "f_clean - f_corrupt, positive when the model prefers the written order. If the convention holds, the "
              "Spearman of these cues with the gap is NEGATIVE. The check below tests this on the data; the script "
              "aborts if the lexical cue shows the opposite sign.")
        rows = []
        for c in CUES + ["kendall"]:
            m = ~np.isnan(X[c])
            rho, p = spearmanr(X[c][m], gap[m])
            rows.append([c, int(m.sum()), float(rho), float(p)])
        log.table(["cue", "n", "Spearman with gap", "p"], rows, "{:.4g}")
        rho_lex = rows[0][2]
        if not rho_lex < 0:
            raise SystemExit(f"SIGN CHECK FAILED: Spearman(d_kenlm_mean_filt, gap) = {rho_lex:.3f} is not negative")
        agree_of = lambda v: v < 0   # cue favours the written order
        log.p("Result: lexical cues are negatively related to the gap, consistent with reference minus variant "
              "surprisal. Direction used: d < 0 favours the written order (agrees), d > 0 favours the reordered "
              "one (disagrees). For d_dep_total (dependency distance, smaller is easier) and d_is_inv_norm, the "
              "same reference minus variant convention applies; their correlations with the gap are descriptive and "
              "signs are read from the table above, not used for strata.")

        # ---- strata
        analyses = {}
        for cue in ("d_kenlm_mean_filt", "d_ngram2_mean_filt"):
            v = X[cue]
            ok = ~np.isnan(v) & (v != 0)
            ag, dg = ok & agree_of(v), ok & ~agree_of(v)
            log.h2(f"Strata by {cue}")
            log.kv("excluded (cue 0 or missing)", int((~ok).sum()))
            trs = []
            for nm, g in (("agrees (cue favours written)", ag), ("disagrees (cue favours reordered)", dg)):
                a = g & keep
                sh_h, ci_h = boot_ratio(heads_num, gap, docs, a, args.boot)
                sh_m, ci_m = boot_ratio(mlps_num, gap, docs, a, args.boot)
                trs.append([nm, int(g.sum()), len(set(docs[g].tolist())), int(a.sum()),
                            f"{100 * (gap[g] > 0).mean():.1f}%", float(gap[g].mean()),
                            fmt(sh_h, ci_h), fmt(sh_m, ci_m)])
            log.table(["stratum", "pairs", "docs", "above floor", "prefers written", "mean gap (bits)",
                       "10 heads share", "5 MLPs share"], trs, "{:.3f}")
            n_ag, n_dg = int((ag & keep).sum()), int((dg & keep).sum())
            d_h, ci_h = boot_diff_ratio(heads_num, gap, docs, ag & keep, dg & keep, args.boot)
            d_m, ci_m = boot_diff_ratio(mlps_num, gap, docs, ag & keep, dg & keep, args.boot)
            log.table(["quantity", "disagrees minus agrees", "95% doc-bootstrap interval"],
                      [["10 heads", d_h, f"[{ci_h[0]:.3f}, {ci_h[1]:.3f}]"],
                       ["5 MLPs jointly", d_m, f"[{ci_m[0]:.3f}, {ci_m[1]:.3f}]"]], "{:.3f}")
            if min(n_ag, n_dg) < args.min_stratum:
                dec = "INCONCLUSIVE (a stratum has fewer than 40 pairs above the floor)"
            else:
                diffs = [(d_h, ci_h), (d_m, ci_m)]
                if any(abs(d) > BAND and (ci[0] > 0 or ci[1] < 0) for d, ci in diffs):
                    dec = "CUE-DEPENDENT"
                elif all(ci[0] >= -BAND and ci[1] <= BAND for _, ci in diffs):
                    dec = "CUE-INDEPENDENT"
                else:
                    dec = "INCONCLUSIVE"
            tag = "PRIMARY" if cue == "d_kenlm_mean_filt" else "second analysis"
            log.p(f"**DECISION ({tag}, {cue}, {args.model}): {dec}** "
                  f"(strata above floor: agrees {n_ag}, disagrees {n_dg}; band +-{BAND})")
            analyses[cue] = (ag, dg)

        # ---- descriptive
        log.h2("Descriptive: Spearman with the gap and with the 5 MLPs' joint effect (bits)")
        eff = res[:, -1] - fx
        rows = []
        for c in CUES + ["kendall"]:
            m = ~np.isnan(X[c])
            r1, p1 = spearmanr(X[c][m], gap[m])
            r2, p2 = spearmanr(X[c][m], eff[m])
            rows.append([c, int(m.sum()), float(r1), float(p1), float(r2), float(p2)])
        log.table(["cue", "n", "rho gap", "p", "rho MLP effect", "p"], rows, "{:.4g}")
        log.h2("Descriptive: OLS of the gap on standardised cue families (not a test)")
        fam = ["d_kenlm_mean_filt", "d_dep_total", "d_is_inv_norm", "d_casemarker_mean"]
        m = np.all([~np.isnan(X[c]) for c in fam], axis=0)
        A = np.column_stack([(X[c][m] - X[c][m].mean()) / X[c][m].std() for c in fam])
        A1 = np.column_stack([np.ones(m.sum()), A])
        beta, *_ = np.linalg.lstsq(A1, gap[m], rcond=None)
        r2 = 1 - ((gap[m] - A1 @ beta) ** 2).sum() / ((gap[m] - gap[m].mean()) ** 2).sum()
        log.kv("pairs in the regression", int(m.sum()))
        log.kv("R^2", f"{r2:.3f}")
        log.table(["term", "coefficient (bits per SD)"], [["intercept", float(beta[0])]] +
                  [[f, float(b)] for f, b in zip(fam, beta[1:])], "{:.3f}")
        log.note("Descriptive only: the cues are correlated with each other and with reordering size, and the "
                 "gap is not a response with a known noise model.")

        # ---- csv
        path = OUT / f"cues_{args.model}.csv"
        strat = np.array(["excluded"] * n, dtype=object)
        ag, dg = analyses["d_kenlm_mean_filt"]
        strat[ag], strat[dg] = "agrees", "disagrees"
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "doc", "kendall"] + CUES + ["gap", "above_floor"] +
                       [f"eff_{s}" for s in names] + ["stratum_kenlm"])
            for i in range(n):
                w.writerow([ids[i], docs[i], int(kendall[i])] + [X[c][i] for c in CUES] +
                           [gap[i], int(keep[i])] + [res[i, j] - fx[i] for j in range(len(names))] + [strat[i]])
        log.output(path, "per-pair cues, gap, set effects (bits), stratum")


if __name__ == "__main__":
    main()
