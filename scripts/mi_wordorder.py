#!/usr/bin/env python3
"""Step 4, word order: which heads and MLPs carry the preference for the written order (REMAINING_EXPERIMENTS.md,
section W). GPU, per model (--model muril | xlmrlarge). Declared before any run (23 Oct 2026). Pairs and the
document split come from mi_items.py (300 of step 2's 1,000 patched pairs, split by document into halves of about
150; mi_items' record has the counts).

THE METRIC AND THE PAIR are step 2's (rq1_patching.py, denoising): the corrupted run is the reordered sentence
scored within_word_l2r, the clean run the written sentence with the same words masked the same way in every row
(aligned word by word through the tree), and the metric minus the mean per-word surprisal. So clean minus
corrupted is the order gap S(reordered) - S(written), and a patch's recovered share is
(S(reordered) - S*(reordered)) / (S(reordered) - S(written)), a ratio of sums over pairs whose gap exceeds
--min-gap bits in either direction.
CHECKS (every stage, every pair it reads): the unpatched corrupted and clean metrics reproduce step 2's s_var and
s_ref for the pair (patching_<model>.csv, copied in results/outputs/patching/) to 1e-3 bits. The exact stage
also checks that patching the embedding output at every position recovers the gap (ratio of sums within 1e-3,
worst pair 5e-3 bits), step 2's 'all at layer 0'.

STAGES (outputs/<stage>_wordorder_<model>.*, records mi_<stage>_wordorder_<model>.md)
  screen    W1: attribution patching of every head and MLP, per site class (special, moved_heads, moved_psp,
            moved_other, verb, unmoved), selection half.
  exact     W2: heads and MLPs apart (revised after the smoke tests, 23 Oct, before any full run: the top
            components are mostly MLPs and a model has only one per block). Patched alone at every position,
            selection half: the screen's top 30 HEADS by absolute share, EVERY MLP, and 30 heads matched by block to
            the top 30 (mi_lib.matched_random_sets, seed 707). DECISION: the screen ranks heads usefully for this
            model if, over the 60 heads, the Spearman correlation of screened and exact shares is at least 0.5 and
            at least 7 of the 10 heads with the largest exact shares belong to the screen's top 30. If not, the
            record says so and the later stages use the exact shares all the same, stated as a limitation.
  sites     W3: the top 5 heads and the top 5 MLPs of the exact stage, each patched at one site class at a time,
            selection half: where in the sentence each component's contribution is read.
  validate  WV: held-out half, once. The circuit is the top --k (10) HEADS of the exact stage. Faithfulness: the
            reordered run with only the circuit patched. Necessity: both runs with the circuit mean-ablated, the
            gap lost, 1 - (ablated gap) / (gap). Against --n-random head sets matched by block, with the same
            language-modelling check as the agreement validation. The top --k-mlp (5) MLPs are patched again on
            the held-out half and their shares there reported beside their selection-half shares (replication).
  every stage first checks the head layout (mi_lib.check_head_layout), as the agreement stages do. --half
            overrides the half a stage reads (smoke tests: selection, so the held-out half stays unread).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_lib as M  # noqa: E402
from runlog import RunLog  # noqa: E402

SITES = ["moved_heads", "moved_psp", "moved_other", "verb", "unmoved"]
CLASSES = ["special"] + SITES
ITEMS = M.ITEMS
STEP2 = M.ROOT / "results" / "outputs" / "patching"


def ints(s):
    return [int(x) for x in str(s).split("|")]


def build(tok, rows, step2, tol=1e-3):
    pairs, skipped, worst = [], 0, 0.0
    for r in rows:
        site = ints(r.var_site)
        v2r = ints(r.var_to_ref)
        ref_site = {v2r[i]: s for i, s in enumerate(site)}
        base = M.l2r_run(tok, r.var_text, word_class=lambda w: site[w] + 1)
        if base is None or base.ids.shape[1] > 256:
            skipped += 1
            continue
        clean, a = M.mapped_run(tok, base, r.ref_text, dict(enumerate(v2r)), word_class=lambda w: ref_site[w] + 1)
        pairs.append(M.Pair(corrupt=[base], clean=[clean], align=[a],
                            meta={"id": f"{r.ref_id}|{r.var_id}", "doc": r.doc, "s2": step2.loc[(r.ref_id, r.var_id)]}))
    return pairs, skipped


def load(args, tok, half):
    wo = pd.read_csv(ITEMS / "wordorder_pairs.csv", dtype={"var_to_ref": str, "var_site": str})
    wo = wo[wo.half == (args.half or half)]
    if args.limit:
        wo = wo.head(args.limit)
    step2 = pd.read_csv(STEP2 / f"patching_{args.model}.csv").set_index(["ref_id", "var_id"])
    return build(tok, list(wo.itertuples()), step2)


def gaps_checked(sess, pairs, log):
    fc = np.array([M.metric(sess, p.clean) for p in pairs])
    fx = np.array([M.metric(sess, p.corrupt) for p in pairs])
    s_ref = np.array([p.meta["s2"].s_ref for p in pairs])
    s_var = np.array([p.meta["s2"].s_var for p in pairs])
    worst = float(max(np.abs(-fc - s_ref).max(), np.abs(-fx - s_var).max()))
    log.kv("check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)", f"{worst:.2e}")
    if worst > 1e-3:
        raise SystemExit("the runs do not reproduce step 2's scores: the pairs or the passes differ")
    return fc, fx


def allpos(p):
    return lambda ri: torch.arange(p.corrupt[ri].ids.shape[1], device=M.DEVICE)


def stage_screen(args, log, sess, tok):
    pairs, skipped = load(args, tok, "selection")
    fc, fx = gaps_checked(sess, pairs, log)
    keep = np.abs(fc - fx) > args.min_gap
    comps = sess.A.components()
    att = np.zeros((len(pairs), len(comps), len(CLASSES)))
    for i, p in enumerate(pairs):
        att[i], _ = M.atp(sess, p, len(CLASSES), chunk=args.chunk)
        if (i + 1) % 25 == 0:
            print(f"    {i + 1}/{len(pairs)}", flush=True)
    f = M.OUT / f"screen_wordorder_{args.model}.npz"
    np.savez_compressed(f, atp=att, f_clean=fc, f_corrupt=fx, ids=np.array([p.meta["id"] for p in pairs]),
                        docs=np.array([p.meta["doc"] for p in pairs]), comps=np.array([M.cname(c) for c in comps]),
                        classes=np.array(CLASSES))
    log.output(str(f), "attribution per pair x component x site class")
    log.kv("pairs / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
    share = att.sum(2)[keep].sum(0) / (fc - fx)[keep].sum()
    order = np.argsort(-np.abs(share))[:30]
    log.table(["component", "screened share"] + [f"via {c}" for c in CLASSES],
              [[M.cname(comps[j]), float(share[j])] + [float(att[keep][:, j, c].sum() / (fc - fx)[keep].sum())
                                                        for c in range(len(CLASSES))] for j in order])


def stage_exact(args, log, sess, tok):
    s = np.load(M.OUT / f"screen_wordorder_{args.model}.npz")
    comps = sess.A.components()
    sk = np.abs(s["f_clean"] - s["f_corrupt"]) > args.min_gap
    sshare = s["atp"].sum(2)[sk].sum(0) / (s["f_clean"] - s["f_corrupt"])[sk].sum()
    # heads and MLPs apart (revised after the smoke tests, 23 Oct): the screen's top 30 HEADS, every MLP, and 30
    # random heads matched to the top 30 by block
    top = [j for j in np.argsort(-np.abs(sshare)) if comps[j][0] == "head"][:30]
    mlps = [j for j in range(len(comps)) if comps[j][0] == "mlp"]
    msets, mst = M.matched_random_sets(comps, tuple(comps[j] for j in top), 1, seed=707)
    rnd = [comps.index(c) for c in msets[0]]
    log.kv("matched random 30 heads: layer-unmatched / type-unmatched replacements", f"{mst['layer-unmatched']} / {mst['type-unmatched']}")
    pairs, skipped = load(args, tok, "selection")
    if [p.meta["id"] for p in pairs] != list(s["ids"]):
        raise SystemExit("the screen was run on other pairs")
    fc, fx = gaps_checked(sess, pairs, log)
    keep = np.abs(fc - fx) > args.min_gap
    gap = fc - fx
    num, den, worst = 0.0, 0.0, 0.0
    for p, a, b in list(zip(pairs, fc, fx))[:5]:
        e = M.exact(sess, p, [("emb",)], allpos(p), args.max_rows)[0]
        worst, num, den = max(worst, abs(e - a)), num + (e - b), den + (a - b)
    log.kv("check: embedding output patched everywhere, ratio of sums / worst pair (bits)", f"{num / den:.6f} / {worst:.2e}")
    if abs(num / den - 1) > 1e-3 or worst > 5e-3:
        raise SystemExit("patching every position at the embeddings does not recover the gap")
    idx = top + mlps + rnd
    kind = ["screen top 30 head"] * len(top) + ["MLP (all)"] * len(mlps) + ["matched random head"] * len(rnd)
    res = np.zeros((len(pairs), len(idx)))
    for i, p in enumerate(pairs):
        res[i] = M.exact(sess, p, [comps[j] for j in idx], allpos(p), args.max_rows)
        if (i + 1) % 25 == 0:
            print(f"    {i + 1}/{len(pairs)}", flush=True)
    eff = res - fx[:, None]
    share = eff[keep].sum(0) / gap[keep].sum()
    docs = np.array([p.meta["doc"] for p in pairs])
    T, R = list(range(len(top))), list(range(len(top) + len(mlps), len(idx)))
    d = (np.abs(eff[:, T]).mean(1) - np.abs(eff[:, R]).mean(1))[keep]
    p_screen = M.doc_signflip(d, docs[keep], one_sided=True)
    from scipy.stats import spearmanr
    H = T + R
    rho = float(spearmanr(sshare[[idx[k] for k in H]], share[H]).correlation)
    in_top = int(sum(1 for k in sorted(H, key=lambda k: -share[k])[:10] if k in set(T)))
    f = M.OUT / f"exact_wordorder_{args.model}.npz"
    np.savez_compressed(f, exact=res, idx=np.array(idx), kind=np.array(kind), f_clean=fc, f_corrupt=fx,
                        ids=np.array([p.meta["id"] for p in pairs]), docs=docs, comps=np.array([M.cname(c) for c in comps]))
    log.output(str(f), "exact patching, each component alone at every position: the screen's top 30 heads, every MLP, "
               "30 matched random heads")
    log.kv("pairs / with a gap above --min-gap", f"{len(pairs)} / {int(keep.sum())}")
    log.kv("screen's top 30 heads against 30 heads matched by block: mean |effect| per pair (bits), document sign-flip "
           "p (one-sided; descriptive)", f"{np.abs(eff[:, T]).mean():.4f} vs {np.abs(eff[:, R]).mean():.4f}, p = {p_screen:.4g}")
    log.kv("heads: Spearman of screened and exact shares over the 60 / of the 10 largest exact shares, in the screen's "
           "top 30", f"{rho:.3f} / {in_top}")
    log.p("The comparison is among the 60 heads patched exactly: a head the screen ranked outside its top 30 is "
          "patched only if drawn as a matched random head, so YES says the screen's top heads beat heads matched "
          "to them by block, not that no stronger head was missed.")
    ok = rho >= 0.5 and in_top >= 7
    log.kv("DECISION (the screen ranks heads usefully for this model)", "YES" if ok else
           "NO: the later stages use the exact shares of the 60 patched heads, a limitation")
    rows = []
    for k in np.argsort(-share):
        lo, hi = M.doc_bootstrap_ratio(eff[keep, k], gap[keep], docs[keep])
        rows.append([M.cname(comps[idx[k]]), kind[k], float(sshare[idx[k]]), float(share[k]), f"[{lo:.3f}, {hi:.3f}]"])
    log.table(["component", "drawn as", "screened share", "exact share", "document bootstrap 95%"], rows)


def top_of_exact(args, k, which):
    """The k heads (which='head') or MLPs (which='mlp') with the largest exact share among those patched."""
    e = np.load(M.OUT / f"exact_wordorder_{args.model}.npz")
    keep = np.abs(e["f_clean"] - e["f_corrupt"]) > args.min_gap
    share = (e["exact"] - e["f_corrupt"][:, None])[keep].sum(0) / (e["f_clean"] - e["f_corrupt"])[keep].sum()
    names, idx = list(e["comps"]), list(e["idx"])
    ranked = [M.cparse(names[idx[j]]) for j in np.argsort(-share)]
    out = []
    for c in ranked:
        if c[0] == which and c not in out:
            out.append(c)
    return out[:k], {M.cname(M.cparse(names[idx[j]])): float(share[j]) for j in range(len(idx))}


def stage_sites(args, log, sess, tok):
    top = top_of_exact(args, 5, "head")[0] + top_of_exact(args, 5, "mlp")[0]
    pairs, skipped = load(args, tok, "selection")
    fc, fx = gaps_checked(sess, pairs, log)
    keep = np.abs(fc - fx) > args.min_gap
    res = np.zeros((len(pairs), len(top), len(CLASSES)))
    for i, p in enumerate(pairs):
        for c in range(len(CLASSES)):
            sel = lambda ri, c=c: torch.nonzero(p.corrupt[ri].pclass == c)[:, 0]
            res[i, :, c] = M.exact(sess, p, top, sel, args.max_rows)
    f = M.OUT / f"sites_wordorder_{args.model}.npz"
    np.savez_compressed(f, sites=res, f_clean=fc, f_corrupt=fx, comps=np.array([M.cname(c) for c in top]),
                        classes=np.array(CLASSES))
    log.output(str(f), "the exact stage's top 10, each patched at one site class at a time")
    g = (fc - fx)[keep].sum()
    log.table(["component"] + [f"at {c} only" for c in CLASSES],
              [[M.cname(c)] + [float((res[:, j, k] - fx)[keep].sum() / g) for k in range(len(CLASSES))]
               for j, c in enumerate(top)])


def stage_validate(args, log, sess, tok):
    heads, sel_share = top_of_exact(args, args.k, "head")
    circuit = tuple(heads)
    mlp_c, _ = top_of_exact(args, args.k_mlp, "mlp")
    comps = sess.A.components()
    rand, rstats = M.matched_random_sets(comps, circuit, args.n_random, seed=707)
    log.kv("half read", args.half or "heldout")
    log.kv("random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched",
           f"{rstats['distinct']} of {args.n_random} / {rstats['replacements']} / {rstats['layer-unmatched']} / {rstats['type-unmatched']}")
    log.kv("circuit (the top K heads of the exact stage, selection half)", ", ".join(M.cname(c) for c in circuit))
    pairs, skipped = load(args, tok, "heldout")
    fc, fx = gaps_checked(sess, pairs, log)
    keep = np.abs(fc - fx) > args.min_gap
    gap = fc - fx
    docs = np.array([p.meta["doc"] for p in pairs])
    sets = [circuit] + rand
    faith = np.zeros((len(pairs), len(sets)))
    for i, p in enumerate(pairs):
        faith[i] = M.exact(sess, p, sets, allpos(p), args.max_rows)
    est, held = M.heldout_sentences(args.sentences, args.n_mean, args.n_read)
    means, cnt = M.estimate_means(sess, tok, est)
    log.kv("mean-estimation positions: special / masked / other", " / ".join(f"{int(x):,}" for x in cnt))
    nc = np.zeros((len(pairs), len(sets)))
    nx = np.zeros((len(pairs), len(sets)))
    for i, p in enumerate(pairs):
        nc[i] = M.ablated_metric(sess, p.clean, sets, means, args.max_rows)
        nx[i] = M.ablated_metric(sess, p.corrupt, sets, means, args.max_rows)
    lost = gap[:, None] - (nc - nx)
    f_share = (faith - fx[:, None])[keep].sum(0) / gap[keep].sum()
    n_share = lost[keep].sum(0) / gap[keep].sum()
    rep = np.zeros((len(pairs), len(mlp_c)))
    for i, p in enumerate(pairs):
        if mlp_c:
            rep[i] = M.exact(sess, p, mlp_c, allpos(p), args.max_rows)
    r0 = M.readability(sess, tok, held)
    rc = M.readability(sess, tok, held, circuit, means)
    rr = [M.readability(sess, tok, held, s, means) for s in rand[:10]]
    f = M.OUT / f"validate_wordorder_{args.model}.npz"
    np.savez_compressed(f, faith=faith, nec_clean=nc, nec_corrupt=nx, f_clean=fc, f_corrupt=fx, docs=docs,
                        sets=np.array(["|".join(M.cname(c) for c in s) for s in sets]), mlp_heldout=rep,
                        mlp_names=np.array([M.cname(c) for c in mlp_c]),
                        mlp_sel_share=np.array([sel_share[M.cname(c)] for c in mlp_c]))
    log.output(str(f), "held-out half: each set patched (faithfulness) and ablated in both runs (necessity); set 0 is the circuit")
    log.kv("pairs / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
    rows = []
    for name, sh, per_item in (("faithfulness (share restored by patching only the set)", f_share, faith - fx[:, None]),
                               ("necessity (share of the gap lost by ablating the set)", n_share, lost)):
        rank_p = (1 + int((sh[1:] >= sh[0]).sum())) / (1 + len(rand))
        diff = (per_item[:, 0] - per_item[:, 1:].mean(1))[keep]
        p = M.doc_signflip(diff, docs[keep])
        lo, hi = M.doc_bootstrap_ratio(per_item[keep, 0], gap[keep], docs[keep])
        rows.append([name, float(sh[0]), f"[{lo:.3f}, {hi:.3f}]", float(np.mean(sh[1:])), float(np.percentile(sh[1:], 95)),
                     rank_p, p])
    log.table(["test", "circuit", "document bootstrap 95%", "random sets, mean", "random sets, 95th percentile",
               "rank p among random sets", "document sign-flip p, circuit minus random mean"], rows, floatfmt="{:.4g}")
    log.table(["model", "held-out nats per subtoken", "minus unablated", "within 2 nats"],
              [["unablated", r0, 0.0, "yes"], ["circuit ablated", rc, rc - r0, "yes" if rc - r0 <= 2 else "no"]] +
              [[f"random set {i}", x, x - r0, "yes" if x - r0 <= 2 else "no"] for i, x in enumerate(rr)])
    log.table(["MLP (top by the exact stage)", "share, selection half", "share, held-out half", "document bootstrap 95%"],
              [[M.cname(c), sel_share[M.cname(c)], float((rep[:, n] - fx)[keep].sum() / gap[keep].sum()),
                "[%.3f, %.3f]" % M.doc_bootstrap_ratio((rep[:, n] - fx)[keep], gap[keep], docs[keep])]
               for n, c in enumerate(mlp_c)])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", required=True, choices=["screen", "exact", "sites", "validate"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--half", default=None, choices=["selection", "heldout"])
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--chunk", type=int, default=16)
    ap.add_argument("--max-rows", type=int, default=256)
    ap.add_argument("--k", type=int, default=10, help="heads in the validated circuit")
    ap.add_argument("--k-mlp", type=int, default=5, help="top MLPs replicated on the held-out half")
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--n-mean", type=int, default=300, help="held-out sentences for the ablation means")
    ap.add_argument("--n-read", type=int, default=100, help="held-out sentences for the language-modelling check")
    ap.add_argument("--sentences", default=str(M.ROOT / "data" / "heldout_text" / "readability_sentences.txt"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if args.half == "heldout" and args.stage != "validate":
        raise SystemExit("only the validate stage reads the held-out half")
    if args.stage == "validate" and args.half == "selection" and not args.limit:
        raise SystemExit("a full validate run reads the held-out half; --half selection is for smoke tests (--limit)")
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    M.OUT.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"mi_{args.stage}_wordorder_{args.model}"
    with RunLog(tag, __file__, args, purpose=f"Step 4 word order, stage {args.stage}, {args.model}.") as log:
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            text = pd.read_csv(ITEMS / "wordorder_pairs.csv").ref_text.iloc[0]
            lay = M.check_head_layout(sess, tok, text)
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            {"screen": stage_screen, "exact": stage_exact, "sites": stage_sites,
             "validate": stage_validate}[args.stage](args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
