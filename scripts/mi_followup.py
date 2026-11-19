#!/usr/bin/env python3
"""Follow-up experiments 1 and 2 (docs/FOLLOWUP_EXPERIMENTS.md): the reordering-size split and the case-marker
control. GPU, per model (--model muril | xlmrlarge). Declared before any run (27 Oct 2026). Items come from
mi_items_extra.py (word order) and mi_items.py (agreement).

THE CIRCUIT IS FROZEN. Every stage takes its components from step 4's selection-half results (outputs/exact_*), never
from what it reads: the top 10 heads and the top 5 MLPs of the exact stage (word order: exact_wordorder; agreement:
exact_object). Nothing here chooses a component, so nothing here is selection.
FRESH DATA ONLY. Word order: the pairs of step 2's 1,000 whose documents are in neither half of step 4's 300 (the
pool 'fresh' of mi_items_extra.py). Agreement: the orders of the documents outside the contrast pairs' 91 (the
rows of agreement_positions.csv with no half). Neither half step 4 read is touched, by construction.

STAGE size  (experiment 1, word order). QUESTION: does the circuit read structure or surface, as the reordering
  grows? The behavioural curve (the written order is preferred more often as more phrase pairs are swapped,
  MuRIL 74.0 to 94.9%, XLM-R-large 72.4 to 94.4%) cannot say. Two readings:
    structure  the models read which phrase moved and what its case marker says; the circuit's share of the gap and
               where it acts (the moved phrases' head words and markers) stay about the same at every size, the gap
               growing because more phrases are out of place
    surface    the models notice displaced words wherever they are; the circuit's share falls with size and its
               action moves to the other words (moved_other, verb, unmoved)
  Per size group (1; 2-3; 4+ for the tests, and 1; 2-3; 4-7; 8+ for the tables), on the fresh pairs: the gap, the
  share of the gap restored by patching the 10 heads alone (faithfulness), by each of the top 5 MLPs and by the
  five jointly, and each of the top 5 heads and top 5 MLPs patched at one site class at a time. PRIMARY: the
  difference in the 10 heads' faithfulness and in the MLPs' joint share between the 4+ group and the group of single
  swaps, with a document-bootstrap 95% interval. DECLARED RULE: size-independent if both intervals lie within
  +-0.10; otherwise size-dependent if either excludes 0; otherwise inconclusive. Applied per quantity (one whose
  interval is within +-0.10 counts as size-independent even if it excludes 0), then combined: independent if both
  are; dependent if either is size-dependent (outside +-0.10 and excluding 0); otherwise inconclusive. The site profile is described, not tested. CHECK: the unpatched runs reproduce step 2's s_ref and s_var
  for every pair (1e-3 bits); patching the embedding output at every position recovers the gap (first five pairs).

STAGE case_wordorder  (experiment 2, word order). QUESTION: is the gap read through the case markers? Per fresh pair
  that has moved_psp words and enough unmoved words: three versions of the pair, from mi_items_extra.py:
    none  the pair as it is (checked against step 2)
    psp   every case marker or postposition of a moved phrase deleted from both sentences
    ctl   as many unmoved words deleted, chosen at random, from both sentences
  Per version: the gap, the 10 heads' effect and the 5 MLPs' joint effect in bits and as a share of that version's
  gap. PRIMARY: the paired difference in gap, ctl minus psp, per pair, with a one-sided document sign-flip p (10,000)
  and a document-bootstrap interval: if the order is read through case markers, deleting them should cost more of
  the gap than deleting as many other words. DECLARED READING: supported if p < 0.05 and the retained gap under psp
  is lower than under ctl; not supported otherwise (the record says which). The circuit's effects are descriptive.
  Limit: both versions change the sentences, so the control matches the number of words deleted, not their kind.

STAGE case_agreement  (experiment 2, agreement; object task as step 4). Per fresh order, three versions: none (as
  written), ne (the ergative marker deleted), ctl (one random word that is neither the agreeing word, the verb
  complex, the object, the subject nor ne, deleted). Per version: the clean margin M (the agreeing words' log2
  ratio, correct over wrong; the correct form is the one that agrees with the object), the margin with the object
  masked, the 10 heads' and the 5 MLPs' faithfulness for the object gap, and the share of the verb's attention that
  the top 5 heads put on the object. PRIMARY: the paired difference in the clean margin, ctl minus ne, with a
  one-sided document sign-flip p: if the object's agreement is licensed by ne, deleting ne should cost more than
  deleting an unrelated word. DECLARED READING: supported if p < 0.05 and the mean margin under ne is lower than
  under ctl; not supported otherwise. The circuit and the attention are descriptive, shown for all fresh orders and
  for the variant orders with a non-adjacent object (the population the circuit was found on). When ne is deleted the correct
  form is no longer the grammatical one, so the margin's fall is the expected behaviour, and the question is
  whether it exceeds the control's; the faithfulness says whether the same heads still carry what remains.
  CHECKS (every stage): the head layout; for the agreement stage the unpatched runs of the unedited version
  reproduce the margins in outputs/metric_<model>.csv (M_none and M_obj, 1e-3 bits); the embedding patch recovers
  the gap on the first five items.
"""
import argparse
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_agreement as A  # noqa: E402
import mi_lib as M  # noqa: E402
import mi_wordorder as W  # noqa: E402
from runlog import RunLog, sha256  # noqa: E402

EXTRA = Path(M.os.environ.get("MI_ITEMS_EXTRA", M.ROOT / "course_runs" / "outputs" / "items_extra"))
SIZE_BINS = [("1", lambda k: k == 1), ("2-3", lambda k: 2 <= k <= 3), ("4-7", lambda k: 4 <= k <= 7), ("8+", lambda k: k >= 8)]
SIZE_GROUPS = [("1", lambda k: k == 1), ("2-3", lambda k: 2 <= k <= 3), ("4+", lambda k: k >= 4)]


# ----------------------------------------------------------------------------------------------- statistics

def doc_sums(values, docs):
    u = sorted(set(docs.tolist()))
    idx = {k: i for i, k in enumerate(u)}
    out = np.zeros(len(u))
    np.add.at(out, [idx[x] for x in docs], values)
    return out


def boot_diff_ratio(num, den, docs, g1, g2, B=2000, seed=707):
    """95% percentile interval of ratio(g2) - ratio(g1), ratios of sums, resampling documents (descriptive)."""
    docs = np.asarray(docs)
    u = sorted(set(docs.tolist()))
    pos = {k: i for i, k in enumerate(u)}
    idx = np.array([pos[d] for d in docs])
    n1, d1, n2, d2 = (np.zeros(len(u)) for _ in range(4))
    np.add.at(n1, idx[g1], np.asarray(num)[g1])
    np.add.at(d1, idx[g1], np.asarray(den)[g1])
    np.add.at(n2, idx[g2], np.asarray(num)[g2])
    np.add.at(d2, idx[g2], np.asarray(den)[g2])
    pick = np.random.default_rng(seed).integers(0, len(u), size=(B, len(u)))
    with np.errstate(divide="ignore", invalid="ignore"):
        r = n2[pick].sum(1) / d2[pick].sum(1) - n1[pick].sum(1) / d1[pick].sum(1)
    if np.isnan(r).mean() > 0.01:
        raise SystemExit("more than 1% of bootstrap draws missed every document of a group")
    return float(np.nanpercentile(r, 2.5)), float(np.nanpercentile(r, 97.5))


def boot_mean(values, docs, B=2000, seed=707):
    """95% percentile interval of the mean of per-item values, resampling documents (descriptive)."""
    values, docs = np.asarray(values, float), np.asarray(docs)
    u = sorted(set(docs.tolist()))
    idx = {k: i for i, k in enumerate(u)}
    s, n = np.zeros(len(u)), np.zeros(len(u))
    np.add.at(s, [idx[x] for x in docs], values)
    np.add.at(n, [idx[x] for x in docs], 1.0)
    pick = np.random.default_rng(seed).integers(0, len(u), size=(B, len(u)))
    r = s[pick].sum(1) / n[pick].sum(1)
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def share(res, fx, gap, keep, docs=None):
    """(ratio of sums, document bootstrap interval) of the share of the gap a patch restores."""
    num, den = (res - fx)[keep], gap[keep]
    r = float(num.sum() / den.sum())
    if docs is None:
        return r, None
    return r, M.doc_bootstrap_ratio(num, den, np.asarray(docs)[keep])


def fmt(r, ci=None):
    return f"{r:.3f}" if ci is None else f"{r:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


# ----------------------------------------------------------------------------------------------- frozen circuit

def frozen_wordorder(args):
    heads, _ = W.top_of_exact(args, 10, "head")
    mlps, _ = W.top_of_exact(args, 5, "mlp")
    return heads, mlps


def frozen_object(args):
    ex = np.load(M.OUT / f"exact_object_{args.model}.npz")
    names = list(ex["comps"])
    keep = np.abs(ex["f_clean"] - ex["f_corrupt"]) > args.min_gap
    sh = (ex["exact"] - ex["f_corrupt"][:, None])[keep].sum(0) / (ex["f_clean"] - ex["f_corrupt"])[keep].sum()
    order = list(np.argsort(-sh))
    heads = [M.cparse(names[j]) for j in order if "MLP" not in names[j]][:10]
    mlps = [M.cparse(names[j]) for j in order if "MLP" in names[j]][:5]
    return heads, mlps


def circuit_sets(heads, mlps):
    """Patched jointly: the 10 heads; each of the 5 MLPs alone; the 5 MLPs together."""
    return [tuple(heads)] + list(mlps) + [tuple(mlps)]


SET_NAMES = ["10 heads"] + [f"MLP {i + 1}" for i in range(5)] + ["5 MLPs jointly"]


def embedding_check(sess, pairs, fc, fx, args, log, label):
    worst, num, den = 0.0, 0.0, 0.0
    for p, a, b in list(zip(pairs, fc, fx))[:5]:
        e = M.exact(sess, p, [("emb",)], W.allpos(p), args.max_rows)[0]
        worst, num, den = max(worst, abs(e - a)), num + (e - b), den + (a - b)
    log.kv(f"check: embedding output patched everywhere, {label}: ratio of sums / worst pair (bits)",
           f"{num / den if den else float('nan'):.6f} / {worst:.2e}")
    if (den and abs(num / den - 1) > 1e-3) or worst > 5e-3:
        raise SystemExit("patching every position at the embeddings does not recover the gap")


# ----------------------------------------------------------------------------------------------- word-order pool

def read_pool():
    pool = pd.read_csv(EXTRA / "wordorder_pool.csv", dtype=str)
    for c in ("kendall", "n_psp"):
        pool[c] = pool[c].astype(int)
    pool["psp_ok"] = pool.psp_ok == "True"
    return pool


def build_edited(tok, rows, tag):
    """Like mi_wordorder.build, for the pool's edited columns (_psp, _ctl): no step 2 record exists for them."""
    pairs, skipped = [], 0
    for r in rows:
        ref_text, var_text = getattr(r, f"ref_text_{tag}"), getattr(r, f"var_text_{tag}")
        site, v2r = W.ints(getattr(r, f"var_site_{tag}")), W.ints(getattr(r, f"var_to_ref_{tag}"))
        ref_site = {v2r[i]: s for i, s in enumerate(site)}
        base = M.l2r_run(tok, var_text, word_class=lambda w, site=site: site[w] + 1)
        if base is None or base.ids.shape[1] > 256:
            skipped += 1
            continue
        clean, a = M.mapped_run(tok, base, ref_text, dict(enumerate(v2r)), word_class=lambda w, rs=ref_site: rs[w] + 1)
        pairs.append(M.Pair(corrupt=[base], clean=[clean], align=[a], meta={"id": f"{r.ref_id}|{r.var_id}", "doc": r.doc}))
    return pairs, skipped


def stage_size(args, log, sess, tok):
    pool = read_pool()
    fresh = pool[pool.pool == "fresh"]
    if args.limit:     # smoke tests: the same number from every size bin, so no group is empty
        fresh = pd.concat([g.head(max(1, args.limit // 4)) for _, g in fresh.groupby("bin")])
    step2 = pd.read_csv(W.STEP2 / f"patching_{args.model}.csv").set_index(["ref_id", "var_id"])
    pairs, skipped = W.build(tok, list(fresh.itertuples()), step2)
    info = fresh.assign(id=fresh.ref_id + "|" + fresh.var_id).set_index("id")
    ids = [p.meta["id"] for p in pairs]
    kend = np.array([int(info.loc[i, "kendall"]) for i in ids])
    nw = np.array([len(info.loc[i, "var_text"].split()) for i in ids])
    docs = np.array([p.meta["doc"] for p in pairs])
    fc, fx = W.gaps_checked(sess, pairs, log)
    embedding_check(sess, pairs, fc, fx, args, log, "fresh pairs")
    gap = fc - fx
    heads, mlps = frozen_wordorder(args)
    h5, _ = W.top_of_exact(args, 5, "head")
    log.kv("frozen circuit (step 4 selection half): 10 heads", ", ".join(M.cname(c) for c in heads))
    log.kv("frozen circuit: top 5 MLPs", ", ".join(M.cname(c) for c in mlps))
    sets = circuit_sets(heads, mlps)
    res = np.zeros((len(pairs), len(sets)))
    top = h5 + mlps
    sites = np.zeros((len(pairs), len(top), len(W.CLASSES)))
    for i, p in enumerate(pairs):
        res[i] = M.exact(sess, p, sets, W.allpos(p), args.max_rows)
        for c in range(len(W.CLASSES)):
            sel = lambda ri, c=c, p=p: torch.nonzero(p.corrupt[ri].pclass == c)[:, 0]
            sites[i, :, c] = M.exact(sess, p, top, sel, args.max_rows)
        if (i + 1) % 50 == 0:
            print(f"    {i + 1}/{len(pairs)}", flush=True)
    f = M.OUT / f"size_wordorder_{args.model}.npz"
    np.savez_compressed(f, res=res, sites=sites, f_clean=fc, f_corrupt=fx, ids=np.array(ids), docs=docs, kendall=kend,
                        n_words=nw, set_names=np.array(SET_NAMES), site_comps=np.array([M.cname(c) for c in top]),
                        classes=np.array(W.CLASSES))
    log.output(str(f), "per fresh pair: the circuit's patches (10 heads, 5 MLPs singly and jointly) and the top 10 components per site class")
    keep = np.abs(gap) > args.min_gap
    log.kv("fresh pairs built / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")

    def rows_for(groups):
        out = []
        for name, fn in groups:
            g = np.array([fn(k) for k in kend])
            kg = keep & g
            out.append((name, g, kg))
        return out

    bins, groups = rows_for(SIZE_BINS), rows_for(SIZE_GROUPS)
    for title, grp in (("four size bins (as the slide)", bins), ("three size groups (the tests)", groups)):
        log.h2(f"By reordering size: {title}")
        log.table(["size", "pairs", "documents", "mean words", "mean gap (bits)"] + [f"share: {n}" for n in SET_NAMES[:2] + SET_NAMES[-1:]],
                  [[n, int(g.sum()), len(set(docs[g])), float(nw[g].mean()), float(gap[kg].mean())] +
                   [fmt(*share(res[:, j], fx, gap, kg, docs)) for j in (0, 1, 6)]
                   for n, g, kg in grp])
    log.h2("Each MLP alone, by size group (ratio of sums)")
    log.table(["size"] + SET_NAMES[1:6], [[n] + [float(share(res[:, j], fx, gap, kg)[0]) for j in range(1, 6)] for n, g, kg in groups])
    for lab, sl in (("the top 5 heads", slice(0, 5)), ("the top 5 MLPs", slice(5, 10))):
        log.h2(f"Where {lab} act: mean share of the gap restored when patched at one site class only")
        log.table(["size"] + list(W.CLASSES),
                  [[n] + [float(np.mean([((sites[:, j, c] - fx)[kg].sum() / gap[kg].sum()) for j in range(sl.start, sl.stop)]))
                          for c in range(len(W.CLASSES))] for n, g, kg in groups])
    log.h2("Primary: the 4+ group minus single swaps")
    g1, g2 = groups[0][2], groups[2][2]
    rows, verdict = [], []
    for j, name in ((0, "10 heads, faithfulness"), (6, "5 MLPs jointly")):
        num, den = (res[:, j] - fx), gap
        # ratio-of-sums difference, resampling documents, over the pairs above the gap floor
        d = (num[g2].sum() / den[g2].sum()) - (num[g1].sum() / den[g1].sum())
        lo, hi = boot_diff_ratio(num, den, docs, g1, g2)
        v = "size-independent" if (lo >= -0.10 and hi <= 0.10) else ("size-dependent" if (lo > 0 or hi < 0) else "inconclusive")
        rows.append([name, float(d), f"[{lo:.3f}, {hi:.3f}]", v])
        verdict.append(v)
    log.table(["quantity", "4+ minus single swaps", "document bootstrap 95%", "declared rule"], rows)
    final = "size-independent" if all(v == "size-independent" for v in verdict) else (
        "size-dependent" if any(v == "size-dependent" for v in verdict) else "inconclusive")
    log.kv("DECISION (declared rule: both within +-0.10 = size-independent; otherwise either excludes 0 = size-dependent; else inconclusive)", final)
    from scipy.stats import spearmanr
    log.kv("Spearman of reordering size with the per-pair gap (bits), fresh pairs above the floor",
           f"{spearmanr(kend[keep], gap[keep]).correlation:.3f}")


def stage_case_wordorder(args, log, sess, tok):
    pool = read_pool()
    fresh = pool[(pool.pool == "fresh") & pool.psp_ok]
    if args.limit:
        fresh = fresh.head(args.limit)
    rows = list(fresh.itertuples())
    step2 = pd.read_csv(W.STEP2 / f"patching_{args.model}.csv").set_index(["ref_id", "var_id"])
    built = {"none": W.build(tok, rows, step2)[0], "psp": build_edited(tok, rows, "psp")[0], "ctl": build_edited(tok, rows, "ctl")[0]}
    common = set.intersection(*[{p.meta["id"] for p in v} for v in built.values()])
    built = {k: [p for p in v if p.meta["id"] in common] for k, v in built.items()}
    ids = [p.meta["id"] for p in built["none"]]
    for k, v in built.items():
        if [p.meta["id"] for p in v] != ids:
            raise SystemExit("the versions do not hold the same pairs in the same order")
    docs = np.array([p.meta["doc"] for p in built["none"]])
    log.kv("pairs entering (with moved_psp words, all three versions built)", f"{len(ids)} of {len(rows)}")
    heads, mlps = frozen_wordorder(args)
    sets = circuit_sets(heads, mlps)
    fc0, fx0 = W.gaps_checked(sess, built["none"], log)
    out = {}
    for cond, pairs in built.items():
        if cond == "none":
            fc, fx = fc0, fx0
        else:
            fc = np.array([M.metric(sess, p.clean) for p in pairs])
            fx = np.array([M.metric(sess, p.corrupt) for p in pairs])
        embedding_check(sess, pairs, fc, fx, args, log, f"version {cond}")
        res = np.zeros((len(pairs), len(sets)))
        for i, p in enumerate(pairs):
            res[i] = M.exact(sess, p, sets, W.allpos(p), args.max_rows)
            if (i + 1) % 50 == 0:
                print(f"    {cond}: {i + 1}/{len(pairs)}", flush=True)
        out[cond] = (fc, fx, res)
    f = M.OUT / f"case_wordorder_{args.model}.npz"
    np.savez_compressed(f, ids=np.array(ids), docs=docs, set_names=np.array(SET_NAMES),
                        **{f"{c}_{k}": v for c, (fc, fx, res) in out.items() for k, v in (("f_clean", fc), ("f_corrupt", fx), ("res", res))})
    log.output(str(f), "per pair and version: clean and corrupted metrics, the circuit's patches")
    log.p("Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every "
          "word's weight by n/(n-k): 'retained' is compared between psp and ctl (equal counts); its level against the "
          "unedited gap carries that factor.")
    log.h2("Per version")
    rows = []
    base_gap = (out["none"][0] - out["none"][1]).sum()
    for cond, (fc, fx, res) in out.items():
        gap = fc - fx
        keep = np.abs(gap) > args.min_gap
        eff = [(res[:, j] - fx) for j in (0, 6)]
        rows.append([cond, len(gap), float(gap.mean()), float(gap.sum() / base_gap), float(eff[0].mean()),
                     fmt(*share(res[:, 0], fx, gap, keep, docs)), float(eff[1].mean()), fmt(*share(res[:, 6], fx, gap, keep, docs))])
    log.table(["version", "pairs", "mean gap (bits)", "gap retained (share of the unedited gap)",
               "10 heads: mean effect (bits)", "10 heads: share of that version's gap", "5 MLPs jointly: mean effect (bits)",
               "5 MLPs jointly: share of that version's gap"], rows)
    gn, gp, gc = (out[c][0] - out[c][1] for c in ("none", "psp", "ctl"))
    d = gc - gp
    p1 = M.doc_signflip(d, docs, one_sided=True)
    lo, hi = boot_mean(d, docs)
    log.h2("Primary: gap kept after deleting other words minus gap kept after deleting the case markers (paired per pair)")
    log.table(["mean difference (bits)", "document bootstrap 95%", "one-sided document sign-flip p", "retained psp / ctl"],
              [[float(d.mean()), f"[{lo:.3f}, {hi:.3f}]", p1, f"{gp.sum() / base_gap:.3f} / {gc.sum() / base_gap:.3f}"]],
              floatfmt="{:.4g}")
    ok = p1 < 0.05 and gp.sum() < gc.sum()
    log.kv("DECISION (declared: supported if p < 0.05 and the gap retained under psp is lower than under ctl)",
           "supported" if ok else "not supported")
    dm = (out["ctl"][2][:, 6] - out["ctl"][1]) - (out["psp"][2][:, 6] - out["psp"][1])
    log.kv("descriptive: the 5 MLPs' joint effect (bits), ctl minus psp, mean and document bootstrap 95%",
           f"{dm.mean():.3f} [{boot_mean(dm, docs)[0]:.3f}, {boot_mean(dm, docs)[1]:.3f}]")


# ----------------------------------------------------------------------------------------------- agreement edits

def edit_order(o, drop):
    """The order with the whitespace words `drop` deleted from both sentences and every position renumbered. ne_word
    becomes -1 when ne itself is deleted."""
    drop = set(drop)
    cw, fw = o.correct.split(" "), o.foil.split(" ")
    if len(cw) != len(fw):
        raise SystemExit("the correct and the wrong sentence differ in length")
    shift = lambda i: i - sum(1 for d in drop if d < i)
    lst = lambda s: "|".join(str(shift(i)) for i in A.ints(s) if i not in drop)
    if any(i in drop for i in A.ints(o.agree_words)):
        raise SystemExit("an agreeing word would be deleted")
    return SimpleNamespace(order_id=o.order_id, doc=o.doc, ref_id=o.ref_id,
                           correct=" ".join(w for i, w in enumerate(cw) if i not in drop),
                           foil=" ".join(w for i, w in enumerate(fw) if i not in drop),
                           agree_words=lst(o.agree_words), verb_words=lst(o.verb_words), obj_words=lst(o.obj_words),
                           subj_words=lst(o.subj_words), ne_word=-1 if int(o.ne_word) in drop else shift(int(o.ne_word)))


def attention_to_object(sess, run, heads):
    """Share of the attention a head pays, from each scored position of the correct sentence's rows, to the object
    words (renormalised over real subtokens), as mi_agreement's attention stage; mean over rows. Returns (len(heads),)."""
    out = sess.A.base(input_ids=run.ids, attention_mask=torch.ones_like(run.ids), output_attentions=True)
    att = torch.stack(out.attentions, 1)
    q = att[torch.arange(len(run.ids), device=M.DEVICE), :, :, run.pos]
    real = run.pclass != 0
    q = q[..., real] / q[..., real].sum(-1, keepdim=True)
    cl = run.pclass[real]
    v = q[..., cl == A.CLASSES.index("object")].sum(-1).mean(0).cpu().numpy()
    return np.array([float(v[h[1], h[2]]) for h in heads])


def stage_case_agreement(args, log, sess, tok):
    pos = A.read_positions()
    fresh = pos[(~pos.in_contrast) & pos.half.isna()]
    if args.limit:
        fresh = fresh.head(args.limit)
    base = pd.read_csv(M.OUT / f"metric_{args.model}.csv").set_index(["ref_id", "order_id"])
    heads, mlps = frozen_object(args)
    h5 = heads[:5]
    sets = [tuple(heads), tuple(mlps)]
    log.kv("frozen circuit (step 4 selection half, object task): 10 heads", ", ".join(M.cname(c) for c in heads))
    log.kv("frozen circuit: the 5 MLPs", ", ".join(M.cname(c) for c in mlps))
    conds = ("none", "ne", "ctl")
    rec, worst, n_check, skipped = [], 0.0, 0, 0
    for i, o in enumerate(fresh.itertuples()):
        n = len(o.correct.split(" "))
        words = o.correct.split(" ")
        busy = set(A.ints(o.agree_words)) | set(A.ints(o.verb_words)) | set(A.ints(o.obj_words)) | set(A.ints(o.subj_words)) | {int(o.ne_word)}
        other = [w for w in range(n) if w not in busy and words[w] != "।"]   # not the sentence-final danda
        if not other:
            skipped += 1
            continue
        pick = int(np.random.default_rng([709, i]).choice(other))
        versions = {"none": o, "ne": edit_order(o, {int(o.ne_word)}), "ctl": edit_order(o, {pick})}
        pairs = {c: A.object_pair(tok, v) for c, v in versions.items()}
        if any(p is None for p in pairs.values()):
            skipped += 1
            continue
        r = {"order_id": o.order_id, "doc": o.doc, "ref_id": o.ref_id, "is_reference": bool(o.is_reference),
             "object_adjacent": bool(o.object_adjacent)}
        for c, p in pairs.items():
            fc, fx = M.metric(sess, p.clean), M.metric(sess, p.corrupt)
            res = M.exact(sess, p, sets, W.allpos(p), args.max_rows)
            r[f"M_{c}"], r[f"Mobj_{c}"], r[f"heads_{c}"], r[f"mlps_{c}"] = fc, fx, res[0], res[1]
            a = attention_to_object(sess, p.clean[0], h5)
            for h, v in zip(h5, a):
                r[f"att_{M.cname(h)}_{c}"] = float(v)
            if c == "none" and n_check < 5:
                e = M.exact(sess, p, [("emb",)], W.allpos(p), args.max_rows)[0]
                if abs(e - fc) > 5e-3:
                    raise SystemExit("patching every position at the embeddings does not recover the clean margin")
                n_check += 1
        # the unedited version against step 4's A0 record for the same order (the metric stage's M_none and M_obj)
        b = base.loc[(o.ref_id, o.order_id)]
        worst = max(worst, abs(r["M_none"] - b.M_none), abs(r["Mobj_none"] - b.M_obj))
        rec.append(r)
        if (i + 1) % 200 == 0:
            print(f"    {i + 1}/{len(fresh)}", flush=True)
    d = pd.DataFrame(rec)
    f = M.OUT / f"case_agreement_{args.model}.csv"
    d.to_csv(f, index=False)
    log.output(str(f), "per fresh order and version: the clean and object-masked margins, the circuit's patches, attention to the object")
    log.kv("check: unedited version against the metric stage's M_none and M_obj, orders / worst (bits)", f"{len(d)} / {worst:.2e}")
    if worst > 1e-3:
        raise SystemExit("the unedited runs do not reproduce step 4's margins")
    log.kv("check: embedding output patched everywhere recovers the clean margin, first items", f"{n_check} items, within 5e-3 bits")
    log.kv("fresh orders read / entering (all three versions built) / skipped", f"{len(fresh)} / {len(d)} / {skipped}")
    docs = d.doc.to_numpy()
    rows = []
    for c in conds:
        gap = (d[f"M_{c}"] - d[f"Mobj_{c}"]).to_numpy()
        keep = np.abs(gap) > args.min_gap
        fx = d[f"Mobj_{c}"].to_numpy()
        rows.append([c, len(d), float((d[f"M_{c}"] > 0).mean()), float(d[f"M_{c}"].mean()), float(d[f"Mobj_{c}"].mean()),
                     float(gap.mean()), fmt(*share(d[f"heads_{c}"].to_numpy(), fx, gap, keep, docs)),
                     fmt(*share(d[f"mlps_{c}"].to_numpy(), fx, gap, keep, docs)),
                     float(np.mean([d[f"att_{M.cname(h)}_{c}"].mean() for h in h5]))])
    log.h2("Per version")
    log.table(["version", "orders", "correct preferred (M > 0)", "mean M (bits)", "mean M, object masked", "mean gap (bits)",
               "10 heads: share of the gap restored", "5 MLPs jointly: share", "mean attention to the object, top 5 heads"],
              rows, floatfmt="{:.4g}")
    log.p("Step 4's circuit was found on variant orders with the object not adjacent to the verb. The table below is the "
          "same, restricted to those orders (the fresh set also holds the attested orders and adjacent objects).")
    r = d[~d.is_reference & ~d.object_adjacent]
    rd = r.doc.to_numpy()
    rrows = []
    for c in conds:
        gap = (r[f"M_{c}"] - r[f"Mobj_{c}"]).to_numpy()
        keep = np.abs(gap) > args.min_gap
        fx = r[f"Mobj_{c}"].to_numpy()
        rrows.append([c, len(r), float(r[f"M_{c}"].mean()), float(gap.mean()),
                      fmt(*share(r[f"heads_{c}"].to_numpy(), fx, gap, keep, rd)),
                      fmt(*share(r[f"mlps_{c}"].to_numpy(), fx, gap, keep, rd)),
                      float(np.mean([r[f"att_{M.cname(h)}_{c}"].mean() for h in h5]))])
    log.h2("Per version, variant orders with the object not adjacent only")
    log.table(["version", "orders", "mean M (bits)", "mean gap (bits)", "10 heads: share", "5 MLPs jointly: share",
               "mean attention to the object, top 5 heads"], rrows, floatfmt="{:.4g}")
    dif = (d.M_ctl - d.M_ne).to_numpy()
    p1 = M.doc_signflip(dif, docs, one_sided=True)
    lo, hi = boot_mean(dif, docs)
    log.h2("Primary: clean margin after deleting an unrelated word minus after deleting ne (paired per order)")
    log.table(["mean difference (bits)", "document bootstrap 95%", "one-sided document sign-flip p", "mean M: ne / ctl"],
              [[float(dif.mean()), f"[{lo:.3f}, {hi:.3f}]", p1, f"{d.M_ne.mean():.3f} / {d.M_ctl.mean():.3f}"]], floatfmt="{:.4g}")
    ok = p1 < 0.05 and d.M_ne.mean() < d.M_ctl.mean()
    log.kv("DECISION (declared: supported if p < 0.05 and the mean margin under ne is lower than under ctl)",
           "supported" if ok else "not supported")
    log.h2("Attention to the object by head and version (mean share of the verb's attention)")
    log.table(["head"] + list(conds), [[M.cname(h)] + [float(d[f"att_{M.cname(h)}_{c}"].mean()) for c in conds] for h in h5],
              floatfmt="{:.4g}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", required=True, choices=["size", "case_wordorder", "case_agreement"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None, help="first N items only (smoke tests)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--max-rows", type=int, default=256)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    if args.stage == "case_agreement":
        A.require_metric(SimpleNamespace(model=args.model))
    M.OUT.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"mi_followup_{args.stage}_{args.model}"
    with RunLog(tag, __file__, args, purpose=f"Follow-up, stage {args.stage}, {args.model}.") as log:
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            text = pd.read_csv(M.ITEMS / "wordorder_pairs.csv").ref_text.iloc[0]
            lay = M.check_head_layout(sess, tok, text)
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            {"size": stage_size, "case_wordorder": stage_case_wordorder,
             "case_agreement": lambda a, l, s, t: stage_case_agreement(a, l, s, t)}[args.stage](args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
