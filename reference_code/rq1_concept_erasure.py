#!/usr/bin/env python3
"""Does licensing a scrambled order depend on argument role or on the case marker? LEACE erasure (EXTENSION I2).

Declared before any run (2 Oct 2026).

  layer        each model's layer of highest case-probe selectivity (rq1_probe_selectivity.md): MuRIL 7,
               IndicBERT-v2 7, mBERT 8, XLM-R-large 12, as hidden-state indices (0 is the embeddings), so the
               eraser acts on the output of encoder block L
  fit data     the constituent states the case probe was trained on (lm_units/units_<model>.npz: 2,000 sample
               references, each unit pooled over its words without its own postposition, full sentence input)
  erasers      LEACE, closed form (Belrose et al. 2023): x -> x - W+ P W (x - mu), W the whitening of the
               states' covariance, P the projection onto the span of W Cov(x, z):
                 role     z = gold relation in {k1, k2, other}
                 marker   z = case label (0, ne, ko, se, me, par, ka, other)
                 control  z = a Hewitt-and-Liang control label: one label per head lemma, drawn from the role
                          labels' distribution (rq1_probe_selectivity.control_labels), same rank as role
                 random   a random subspace of the role eraser's rank, removed in the whitened space
               each fitted once, then applied to EVERY position's state at that layer while scoring
  check        after each eraser, an out-of-fold linear probe (folds grouped by reference) for its own concept
               on the fit units: it must fall to the majority rate (within 0.02) for role and marker, or the
               run stops (enforced on review, 2 Oct)
  measure      mean surprisal over whitespace words in every condition; the published T averages over
               tokenizer words, so the no-erasure condition, not the published T, is the baseline
  scoring      every RQ1 pair (T files t_<tag>er<k>_s0.csv for rq1_four_block.py) and the OSV transition pairs
               of rq1_osv_transitions (cells OSV->SOV, OSV->OSV), within_word_l2r through the real head
  damage       mean surprisal per subtoken on the 500 held-out sentences, per condition
  analysis     per condition: the reference-preferred rate on all pairs, on the pairs whose reference is not one
               of the 2,000 fit references, and in the OSV cells; the OSV defence change against no erasure and
               against the random eraser, each with a document-level sign-flip permutation p on the per-pair
               change in the preference indicator. The decomposition per condition is rq1_four_block.py on the
               T files.
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import lm_units as U
from hutb_corpus import BASE, load_trees, parse_conllu, FC, text_of
from pll_scorer import load_masked_lm
from rq1_probe_selectivity import control_labels, head_lemma
from runlog import RunLog

LAYER = {"muril": 7, "indicbert": 7, "mbert": 8, "xlmrlarge": 12}
CONDITIONS = ["none", "role", "marker", "control", "random"]


def leace(X, Z):
    """(A, b) with x' = x @ A.T + b erasing every linear predictor of the one-hot Z from X."""
    mu = X.mean(0)
    Xc = X - mu
    cov = Xc.T @ Xc / len(X)
    ev, V = np.linalg.eigh(cov)
    keep = ev > ev.max() * 1e-10
    W = (V[:, keep] / np.sqrt(ev[keep])) @ V[:, keep].T            # cov^{-1/2} on its support
    Wp = (V[:, keep] * np.sqrt(ev[keep])) @ V[:, keep].T           # cov^{1/2}
    Zc = Z - Z.mean(0)
    M = W @ (Xc.T @ Zc / len(X))
    u, s, _ = np.linalg.svd(M, full_matrices=False)
    U_ = u[:, s > s.max() * 1e-8] if s.size and s.max() > 0 else u[:, :0]
    P = U_ @ U_.T
    E = Wp @ P @ W
    return np.eye(X.shape[1]) - E, E @ mu, U_.shape[1], (W, Wp, mu, V[:, keep])


def random_eraser(white, rank, d, seed=707):
    """A random rank-`rank` subspace of the covariance's support, removed in the whitened space."""
    W, Wp, mu, support = white
    q, _ = np.linalg.qr(support @ np.random.default_rng(seed).standard_normal((support.shape[1], rank)))
    E = Wp @ (q @ q.T) @ W
    return np.eye(d) - E, E @ mu


def probe_acc(X, y, groups):
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    p = cross_val_predict(clf, X, y, groups=groups, cv=GroupKFold(5))
    return float((p == y).mean()), float(pd.Series(y).value_counts(normalize=True).iloc[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--conditions", nargs="+", default=CONDITIONS)
    ap.add_argument("--sentences", default="data/heldout_text/readability_sentences.txt")
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--osv-pairs", default=str(rc / "rq1_osv_transition_pairs.csv"))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--permutations", type=int, default=10000)
    ap.add_argument("--out-dir", default=str(rc / "concept_erasure"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    L = LAYER[args.tag]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with RunLog(args.record_tag or f"rq1_concept_erasure_{args.tag}", __file__, args,
                purpose="LEACE erasure of role against marker, and what it does to the order preference.") as log:
        z = np.load(rc / "lm_units" / f"units_{args.tag}.npz", allow_pickle=True)
        X = z["states"][:, L].astype(np.float64)
        rel, lab, rid = z["rel"].astype(str), z["label"].astype(str), z["ref_id"].astype(str)
        role = np.where(np.isin(rel, ["k1", "k2"]), rel, "other")
        refs10 = parse_conllu(FC / "reference_trees.conllu", 10)
        ctrl = control_labels(head_lemma(refs10, rid, z["unit_head"]), role)
        groups = pd.factorize(rid)[0]
        log.kv("layer / fit units / fit references", f"{L} / {len(X):,} / {len(set(rid)):,}")
        onehot = lambda y: pd.get_dummies(pd.Series(y)).to_numpy(float)
        erasers, rows = {}, []
        A, b, r_role, white = leace(X, onehot(role))
        erasers["role"] = (A, b)
        Am, bm, r_marker, _ = leace(X, onehot(lab))
        erasers["marker"] = (Am, bm)
        erasers["control"] = leace(X, onehot(ctrl))[:2]
        erasers["random"] = random_eraser(white, r_role, X.shape[1])
        base_rows = [["(no erasure)", c, *probe_acc(X, y, groups)] for c, y in (("role", role), ("marker", lab))]
        for name, (A_, b_) in erasers.items():
            Xe = X @ A_.T + b_
            for cname, y in (("role", role), ("marker", lab)):
                rows.append([name, cname, *probe_acc(Xe, y, groups)])
        log.h2("Linear probes on the fit units, before and after each eraser (out of fold, grouped by reference)")
        log.table(["eraser", "probe for", "accuracy", "majority rate"], base_rows + rows, floatfmt="{:.4f}")
        log.kv("rank removed: role / marker", f"{r_role} / {r_marker}")
        log.kv("covariance rank / dimensions", f"{white[3].shape[1]} / {X.shape[1]}")
        for name, cname, acc, maj in rows:
            if name == cname and acc > maj + 0.02:
                raise SystemExit(f"the {name} eraser leaves {cname} decodable ({acc:.3f} against majority {maj:.3f})")

        model, tok, device = load_masked_lm(args.model)
        model.eval()
        block = model.base_model.encoder.layer[L - 1]
        refs, vars_ = load_trees()
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]]
        osv = pd.read_csv(args.osv_pairs)
        osv = osv[osv.transition.isin(["OSV->SOV", "OSV->OSV"])][["ref_id", "var_id", "transition"]]
        if args.limit:
            pairs, osv = pairs.head(args.limit), osv.head(args.limit)
        lines = [l.strip() for l in open(args.sentences, encoding="utf-8") if 8 <= len(l.split()) <= 40]
        held_idx = np.random.default_rng(707).choice(len(lines), size=min(500, len(lines)), replace=False)
        held = [lines[i] for i in sorted(held_idx)]
        fit_refs = set(rid)
        summary = []
        for cond in args.conditions:
            hook = None
            if cond != "none":
                A_, b_ = erasers[cond]
                At = torch.tensor(A_.T, dtype=torch.float32, device=device)
                bt = torch.tensor(b_, dtype=torch.float32, device=device)

                def f(mod, inp, outp, At=At, bt=bt):
                    h = outp[0] if isinstance(outp, tuple) else outp
                    h2 = (h.float() @ At + bt).to(h.dtype)
                    return (h2,) + tuple(outp[1:]) if isinstance(outp, tuple) else h2
                hook = block.register_forward_hook(f)
            try:
                with torch.no_grad():
                    tot, nsub = 0.0, 0
                    for text in held:
                        a = U.score_words(model, tok, device, text, args.batch_size, layers=False)
                        if a is not None:
                            tot += float(np.sum(a[0])) * np.log(2)
                            nsub += sum(a[1])
                    readability = tot / nsub

                    def score(df):
                        res = []
                        for r in df.itertuples():
                            a = U.score_words(model, tok, device, text_of(refs[r.ref_id], True), args.batch_size, layers=False)
                            v = U.score_words(model, tok, device, text_of(vars_[r.var_id], False), args.batch_size, layers=False)
                            if a is not None and v is not None:
                                res.append({"ref_id": r.ref_id, "var_id": r.var_id, "ref_Mean": float(np.mean(a[0])),
                                            "var_Mean": float(np.mean(v[0]))})
                        return pd.DataFrame(res)
                    t = score(pairs)
                    o = score(osv).merge(osv, on=["ref_id", "var_id"])
            finally:
                if hook is not None:
                    hook.remove()
            k = CONDITIONS.index(cond)
            col = f"t_{args.tag}er{k}_Mean"
            t[col] = t.ref_Mean - t.var_Mean
            o["d"] = o.ref_Mean - o.var_Mean
            tf, of = out / f"t_{args.tag}er{k}_s0.csv", out / f"osv_{args.tag}er{k}.csv"
            t.to_csv(tf, index=False)
            o.to_csv(of, index=False)
            log.output(str(tf), f"RQ1 pairs, condition {cond}")
            log.output(str(of), f"OSV transition pairs, condition {cond}")
            unseen = t[~t.ref_id.isin(fit_refs)]
            summary.append([cond, readability, float((t[col] < 0).mean()), float((unseen[col] < 0).mean()),
                            float((o[o.transition == "OSV->SOV"].d < 0).mean()),
                            float((o[o.transition == "OSV->OSV"].d < 0).mean())])
            print(f"    condition {cond} done", flush=True)
        log.h2("Per condition")
        log.table(["condition", "held-out nats per subtoken", "reference preferred, all RQ1 pairs",
                   "same, references not used to fit", "OSV defence (OSV->SOV)", "OSV->OSV"], summary, floatfmt="{:.4f}")

        if "none" in args.conditions:
            log.h2("Change in the OSV defence and in the RQ1 preference, against no erasure and against random")
            rng = np.random.default_rng(707)

            def load(cond, kind):
                k = CONDITIONS.index(cond)
                return pd.read_csv(out / (f"osv_{args.tag}er{k}.csv" if kind == "osv" else f"t_{args.tag}er{k}_s0.csv"))
            res = []
            for kind in ("osv", "rq1"):
                for cond in [c for c in args.conditions if c not in ("none",)]:
                    for against in [x for x in ("none", "random") if x in args.conditions and x != cond]:
                        a, b = load(cond, kind), load(against, kind)
                        if kind == "osv":
                            m = a.merge(b[["ref_id", "var_id", "d"]], on=["ref_id", "var_id"], suffixes=("", "_b"))
                            m = m[m.transition == "OSV->SOV"]
                            ca, cb = "d", "d_b"
                        else:
                            ca = f"t_{args.tag}er{CONDITIONS.index(cond)}_Mean"
                            cb = f"t_{args.tag}er{CONDITIONS.index(against)}_Mean"
                            m = a[["ref_id", "var_id", ca]].merge(b[["ref_id", "var_id", cb]], on=["ref_id", "var_id"])
                        delta = (m[ca] < 0).astype(float) - (m[cb] < 0).astype(float)
                        doc = m.ref_id.str.split("__").str[0]
                        sums = delta.groupby(doc).sum().to_numpy()
                        obs = sums.sum() / len(m)
                        null = (rng.choice([-1.0, 1.0], size=(args.permutations, len(sums))) @ sums) / len(m)
                        p = (1 + int((np.abs(null) >= abs(obs)).sum())) / (1 + args.permutations)
                        res.append(["OSV->SOV" if kind == "osv" else "RQ1 pairs", cond, against, len(m), obs, p])
            log.table(["pairs", "eraser", "against", "n", "change in reference-preferred rate", "document sign-flip p"],
                      res, floatfmt="{:.4g}")


if __name__ == "__main__":
    main()
