#!/usr/bin/env python3
"""Paper experiments P3 and P4 (docs/PAPER_EXPERIMENTS.md): head-set size and MLP sets. GPU, per task and model
(--task object | wordorder, --model muril | xlmrlarge). Declared 18 Nov 2026, before any run. The design, the
predictions and the decision rules are those of the design document; this docstring restates them.

THE CIRCUIT IS FROZEN and the data are FRESH. Components are ranked from step 4's selection-half outputs
(outputs/exact_*, outputs/screen_wordorder_*), never from what a stage reads. Fresh data, so neither half step 4 read
is touched. Agreement (task object): the orders of the documents outside the contrast pairs (no half), variant orders
(not the attested one) whose object is not adjacent to the verb, up to 400 drawn with seed 710; object-masking pairs
as step 4 (mi_agreement.object_pair), metric M. Word order: the 'fresh' pool of outputs/items_extra/wordorder_pool.csv
(471 pairs), up to 300 drawn with seed 710, built as step 2 (mi_wordorder.build), metric minus the mean per-word
surprisal; gap = surprisal of the reordered minus the written sentence. Pseudo-log-likelihood is not true surprisal:
every margin and gap here is a pseudo-log-likelihood quantity. Ratios of sums over items above the gap floor (--min-gap,
0.05 bits), as step 4. Document-level sign-flip tests (10,000, seed 707); document-bootstrap intervals are descriptive.

STAGE setsize (P3): is a judgement carried by a compact set of heads or by many?
  QUESTION. For agreement ten heads are sufficient and necessary; for word order they are sufficient but not necessary
  (step 4: necessity 0.06 and 0.09). One explanation is redundancy (many heads can do the job, so removing ten changes
  little); another is that the heads are not what computes it (the MLPs are). Removing more heads separates them.
  SETS. Heads ranked by step 4's selection-half exact share where the exact stage patched them. Agreement: every head
  (exact_object). Word order: the exact stage patched the screen's top 30 heads and 30 heads matched to them by block, so
  those 60 are ranked by exact share (mi_wordorder.top_of_exact) and every remaining head follows, ranked by its
  attribution-patching share from the screen (summed over site classes, ratio of sums over pairs above the floor, as
  mi_wordorder.stage_exact computes it; signed, largest first). The record counts, per K, how many of the K heads were
  ranked by the screen alone (word order with 60 patched heads: none for K up to 40, a fact the record states; heads
  outside the 60 are never reached). Sets: the top K for K in {5, 10, 20, 40}. K = 10 must equal step 4's frozen 10 heads
  (asserted). RANDOM COMPARATORS: mi_lib.matched_random_sets, 100 sets for K up to 20 and 50 for K = 40 (half of
  --n-random), seed 707, with its counts of distinct sets and layer-unmatched replacements (if a K cannot be matched by
  block, as in MuRIL's crowded late layers, the function falls back to the nearest block and counts it; the record
  shows it).
  MEASURES. Faithfulness: the set patched jointly from the clean into the corrupted run. Necessity: the set
  mean-ablated in the clean run (agreement: share of the clean margin lost; word order: both runs ablated, share of the
  gap lost, 1 - ablated gap / gap), means from held-out IndicCorp text with separate means for special, masked and
  other positions (mi_lib.estimate_means), exactly as validate. For K = 10 and K = 40 also necessity under ZERO
  ablation (the component's output set to zero at every position, the same hook), as a second ablation type. Per K:
  the share with a document-bootstrap interval, the random sets' mean and 95th percentile, the rank of the top-K set
  among its random sets (1 = no random set reaches it), the sign-flip p of the per-item top-K minus random-mean
  difference. The 2-nat language-modelling check (mi_lib.readability, held-out sentences) for the top-K set and for 10 of
  its random sets, with the means (and, for K = 10 and 40, the top set under zero ablation).
  DECLARED READING (per task and model), as P3 with the third addendum's labels (18 Nov, before any full run). D =
  necessity at K = 40 minus necessity at K = 10 (mean ablation), with a document-bootstrap interval.
    REDUNDANCY SUPPORTED          D >= 0.20 with the interval excluding 0, and the top-40 set ranks first among its
                                  random sets (necessity)
    HEADS NOT NECESSARY EVEN JOINTLY   necessity at K = 40 stays below 0.50
    COMPACT                       necessity at K = 10 is already at least 0.90 (agreement's step 4 value)
  The three are checked independently. (a) A label that rests on a K whose language-modelling cost exceeds 2 nats prints
  NOT READ in place of its verdict (COMPACT rests on K = 10, HEADS NOT NECESSARY on K = 40, REDUNDANCY on both). (b) When
  REDUNDANCY SUPPORTED and HEADS NOT NECESSARY EVEN JOINTLY both hold, the line prints REDUNDANCY SUPPORTED (partial:
  K = 40 still below 0.50). (c) None holding and none unread: NONE OF THE THREE. The same is computed under zero
  ablation; a verdict that differs between mean and zero ablation is called ABLATION-DEPENDENT.
  Reported beside the rank, per K: the top-K minus random-K necessity (the shares' difference, so the random comparator
  carries the weight, not only the rank), the number of distinct heads the random sets use (at K = 40 the random sets
  overlap each other heavily, so the rank is a weak criterion), and for word order the number of the K heads that the
  exact stage drew as the screen's top 30 and as the 30 matched random heads (exact_wordorder_<model>.npz 'kind'; the
  pool of 60). The K = 40 comparison is 'the top 40 of a 60-head pool against the rest of the same layers' (printed as
  a note for word order). The results of each K are saved to the npz as it finishes (same file name; final save at the
  end), so a killed job leaves the finished Ks. The prediction: agreement compact in both models; word order
  redundant or head-independent.
  WHAT A FAILURE MEANS. If the language-modelling check fails (more than 2 nats) for the top-K set, the necessity at
  that K is not read as the judgement's (NOT READ). If the heads are not necessary even at K = 40 while the
  language-modelling cost is within 2 nats, the judgement does not run through the heads alone.

STAGE mlpsets (P4): do the frozen MLPs matter specifically, or would any late MLPs do?  (third addendum's design)
  The frozen five are the top five MLPs by single share, so a set holding more of them scores higher under any
  additivity; 'ranks first among 200 random sets' was decided by a few near-identical neighbours. The question is
  whether these five matter specifically or any late MLPs would do. SETS (seed 710, never the frozen set, no duplicates).
  MuRIL (12 MLPs): all 791 other 5-subsets. XLM-R-large (24 MLPs): every subset sharing four of the frozen five (95), and
  random subsets stratified by the overlap with the frozen five (the number of frozen MLPs contained): 60 with overlap
  3, 40 with 2, 30 with 1, 30 with 0. SMOKE: --n-random N replaces these counts by N sets per overlap class (at most the
  number that exist; random draws); without --limit the option is refused (the full design takes no count). The record
  prints the number of sets in each overlap class. DATA as setsize.
  MEASURES. Faithfulness (joint patch) for every set. Necessity (mean ablation, as above) for the frozen set and a
  stratified random sample of the sets: 100 (MuRIL) or 60 (XLM-R-large), seed 710, stratified by overlap count
  (proportional allocation by largest remainder, at least 2 per class that has that many, which this script decides
  because the addendum does not say; --n-nec overrides the size for smoke tests). The 2-nat language-modelling check
  for the frozen set and 10 sets drawn across overlap classes (2 per class, seed 710, topped up at random; not the first
  ten). The LM check is reported and necessity is read only if the frozen set's cost is within 2 nats.
  DECLARED READING (the addendum). BEST = the set sharing at most three of the frozen MLPs with the highest
  faithfulness. SPECIFIC if the frozen set's faithfulness exceeds BEST's by at least 0.02 AND the one-sided document
  sign-flip p (10,000, seed 707) of the per-item difference (frozen minus BEST, items above the floor) is below 0.05.
  DEPTH if not SPECIFIC and a regression of the sets' faithfulness (every set, the frozen one included, its overlap
  being 5) on the mean block index of the set's MLPs (0-based) and the overlap count gives the block index a positive
  coefficient whose document-bootstrap 95% interval excludes 0. The interval: 1,000 draws, seed 707; each draw
  resamples the documents with replacement, recomputes every set's faithfulness as a ratio of sums over the items of
  the resampled documents (above the floor), and refits the least-squares regression; percentiles 2.5 and 97.5 of the
  block-index coefficient. NEITHER otherwise. A set within 0.02 of the frozen set is a tie, not a defeat (the 0.02 margin
  of SPECIFIC is the tie band; the record counts the sets within the band and those above it). Descriptive: the share of
  sets within 0.02 of the frozen set, and the means by overlap count (faithfulness over all sets, necessity over the
  sample). The label names the frozen blocks, not 'upper' MLPs. Selecting the best of many sets on the same data
  favours the random side, so SPECIFIC is the conservative reading.
  WHAT A FAILURE MEANS. If other sets restore as much, a joint MLP patch restores the gap because MLPs are numerous and
  late, not because these five are special: DEPTH says late MLPs matter, NEITHER says the data do not decide.

CHECKS (every stage, as mi_followup): the head layout; word order: the unpatched runs reproduce step 2's scores
(mi_wordorder.gaps_checked, 1e-3 bits); agreement: the unpatched runs reproduce outputs/metric_<model>.csv's M_none and
M_obj (1e-3 bits); patching the embedding output at every position recovers the gap on the first five items.
OUTPUTS (M.OUT): setsize_<task>_<model>.npz, mlpsets_<task>_<model>.npz; record mi_paper_<stage>_<task>_<model>.md.
"""
import argparse
import itertools
import math
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_agreement as A  # noqa: E402
import mi_followup as F  # noqa: E402
import mi_lib as M  # noqa: E402
import mi_wordorder as W  # noqa: E402
from runlog import RunLog, sha256  # noqa: E402

KS = [5, 10, 20, 40]
ZERO_KS = [10, 40]            # also necessity under zero ablation
SEED_DATA, SEED_SETS = 710, 707
N_ITEMS = {"object": 400, "wordorder": 300}


# ----------------------------------------------------------------------------------------------- data

def load_data(args, tok, sess, log):
    """Fresh items, built and checked. Returns (pairs, fc, fx, docs, ids)."""
    rng = np.random.default_rng(SEED_DATA)
    if args.task == "object":
        pos = A.read_positions()
        fresh = pos[(~pos.in_contrast) & pos.half.isna() & (~pos.is_reference) & (~pos.object_adjacent)]
        fresh = fresh.iloc[rng.choice(len(fresh), size=min(N_ITEMS["object"], len(fresh)), replace=False)]
        if args.limit:
            fresh = fresh.head(args.limit)
        pairs, rows, skipped = [], [], 0
        for r in fresh.itertuples():
            pr = A.object_pair(tok, r)
            if pr is None:
                skipped += 1
            else:
                pairs.append(pr)
                rows.append(r)
        fc, fx = A.gaps(sess, pairs)
        base = pd.read_csv(M.OUT / f"metric_{args.model}.csv").set_index(["ref_id", "order_id"])
        worst = 0.0
        for r, a, b in zip(rows, fc, fx):
            m = base.loc[(r.ref_id, r.order_id)]
            worst = max(worst, abs(a - m.M_none), abs(b - m.M_obj))
        log.kv("check: unpatched runs against the metric stage's M_none and M_obj, orders / worst (bits)", f"{len(pairs)} / {worst:.2e}")
        if worst > 1e-3:
            raise SystemExit("the unedited runs do not reproduce step 4's margins")
        log.kv("fresh variant orders with the object not adjacent: available / drawn / built / skipped",
               f"{int(((~pos.in_contrast) & pos.half.isna() & (~pos.is_reference) & (~pos.object_adjacent)).sum())} / {len(fresh)} / {len(pairs)} / {skipped}")
    else:
        pool = F.read_pool()
        fresh = pool[pool.pool == "fresh"]
        avail = len(fresh)
        fresh = fresh.iloc[rng.choice(len(fresh), size=min(N_ITEMS["wordorder"], len(fresh)), replace=False)]
        if args.limit:     # the same number from every size bin, so no group is empty
            fresh = pd.concat([g.head(max(1, args.limit // 4)) for _, g in fresh.groupby("bin")])
        step2 = pd.read_csv(W.STEP2 / f"patching_{args.model}.csv").set_index(["ref_id", "var_id"])
        pairs, skipped = W.build(tok, list(fresh.itertuples()), step2)
        fc, fx = W.gaps_checked(sess, pairs, log)
        log.kv("fresh pairs: available / drawn / built / skipped", f"{avail} / {len(fresh)} / {len(pairs)} / {skipped}")
    F.embedding_check(sess, pairs, fc, fx, args, log, "fresh items")
    docs = np.array([p.meta["doc"] for p in pairs])
    ids = np.array([str(p.meta["id"]) for p in pairs])
    keep = np.abs(fc - fx) > args.min_gap
    log.kv("items / documents / with a gap above --min-gap / mean gap (bits)",
           f"{len(pairs)} / {len(set(docs.tolist()))} / {int(keep.sum())} / {float((fc - fx).mean()):.3f}")
    if keep.sum() < 2 or len(set(docs[keep].tolist())) < 2:
        raise SystemExit("fewer than two documents above the gap floor: the statistics are undefined")
    return pairs, fc, fx, docs, ids


# ----------------------------------------------------------------------------------------------- rankings

def ranking_object(args):
    """Every head, by the exact share of the object task (selection half), as mi_followup.frozen_object. Returns
    (heads, source per head, share dict)."""
    ex = np.load(M.OUT / f"exact_object_{args.model}.npz")
    names = list(ex["comps"])
    keep = np.abs(ex["f_clean"] - ex["f_corrupt"]) > args.min_gap
    sh = (ex["exact"] - ex["f_corrupt"][:, None])[keep].sum(0) / (ex["f_clean"] - ex["f_corrupt"])[keep].sum()
    heads = [M.cparse(names[j]) for j in np.argsort(-sh) if "MLP" not in names[j]]
    return heads, ["exact"] * len(heads), {names[j]: float(sh[j]) for j in range(len(names))}


def ranking_wordorder(args, comps):
    """The heads the exact stage patched, by exact share, then every other head by the screen's share."""
    ranked, exact_share = W.top_of_exact(args, 10 ** 6, "head")
    s = np.load(M.OUT / f"screen_wordorder_{args.model}.npz")
    if list(s["comps"]) != [M.cname(c) for c in comps]:
        raise SystemExit("the screen's component order differs from the model's")
    sk = np.abs(s["f_clean"] - s["f_corrupt"]) > args.min_gap
    sshare = s["atp"].sum(2)[sk].sum(0) / (s["f_clean"] - s["f_corrupt"])[sk].sum()
    done = set(ranked)
    rest = [comps[j] for j in np.argsort(-sshare) if comps[j][0] == "head" and comps[j] not in done]
    share = dict(exact_share)
    share.update({M.cname(comps[j]): float(sshare[j]) for j in range(len(comps)) if comps[j][0] == "head" and comps[j] not in done})
    return ranked + rest, ["exact"] * len(ranked) + ["screen"] * len(rest), share


# ----------------------------------------------------------------------------------------------- measures

def faithfulness(sess, pairs, sets, max_rows, tag):
    out = np.zeros((len(pairs), len(sets)))
    t0 = time.time()
    for i, p in enumerate(pairs):
        out[i] = M.exact(sess, p, sets, W.allpos(p), max_rows)
        if (i + 1) % 50 == 0:
            print(f"    {tag} faithfulness {i + 1}/{len(pairs)}", flush=True)
    return out, time.time() - t0


def necessity(sess, pairs, sets, means, task, max_rows, tag):
    nc = np.zeros((len(pairs), len(sets)))
    nx = np.zeros((len(pairs), len(sets)))
    t0 = time.time()
    for i, p in enumerate(pairs):
        nc[i] = M.ablated_metric(sess, p.clean, sets, means, max_rows)
        if task == "wordorder":
            nx[i] = M.ablated_metric(sess, p.corrupt, sets, means, max_rows)
        if (i + 1) % 50 == 0:
            print(f"    {tag} necessity {i + 1}/{len(pairs)}", flush=True)
    return nc, nx, time.time() - t0


def lost_of(task, fc, fx, nc, nx):
    """Per item and set: the part of the gap lost when the set is ablated (agreement: the clean margin lost; word
    order: the gap lost, gap - (ablated clean - ablated corrupted))."""
    return fc[:, None] - nc if task == "object" else (fc - fx)[:, None] - (nc - nx)


def summarise(effect, gap, keep, docs):
    """effect (items, sets), set 0 the set under test, the rest its random comparators."""
    sh = effect[keep].sum(0) / gap[keep].sum()
    rand = sh[1:]
    lo, hi = M.doc_bootstrap_ratio(effect[keep, 0], gap[keep], docs[keep])
    diff = (effect[:, 0] - effect[:, 1:].mean(1))[keep]
    return {"share": float(sh[0]), "ci": (lo, hi), "rand_mean": float(rand.mean()), "rand_p95": float(np.percentile(rand, 95)),
            "rank": 1 + int((rand > sh[0]).sum()), "n_ge": int((rand >= sh[0]).sum()), "n_rand": len(rand),
            "p": M.doc_signflip(diff, docs[keep]), "p_one": M.doc_signflip(diff, docs[keep], one_sided=True), "all": sh}


def lm_rows(label, r0, r, within=2.0):
    return [label, float(r), float(r - r0), "yes" if r - r0 <= within else "no"]


def verdict(n10, n40, lo, hi, first40, lm10, lm40, limit=2.0):
    """P3's declared reading with the third addendum's labels. A label resting on a K whose language-modelling cost
    exceeds 2 nats is NOT READ; REDUNDANCY SUPPORTED and HEADS NOT NECESSARY EVEN JOINTLY together print the partial
    label; every label that holds and is read is listed."""
    ok10, ok40 = lm10 <= limit, lm40 <= limit
    red = n40 - n10 >= 0.20 and lo > 0 and first40
    notnec = n40 < 0.50
    comp = n10 >= 0.90
    held, unread = [], []
    if not (ok10 and ok40):
        unread.append("REDUNDANCY SUPPORTED")
    elif red and notnec:
        held.append("REDUNDANCY SUPPORTED (partial: K = 40 still below 0.50)")
    elif red:
        held.append("REDUNDANCY SUPPORTED")
    if not ok40:
        unread.append("HEADS NOT NECESSARY EVEN JOINTLY")
    elif notnec and not (red and ok10):
        held.append("HEADS NOT NECESSARY EVEN JOINTLY")
    if not ok10:
        unread.append("COMPACT")
    elif comp:
        held.append("COMPACT")
    parts = []
    if held:
        parts.append(" + ".join(held))
    if unread:
        why = "K = 10 language-modelling cost %.2f nats" % lm10 if not ok10 else ""
        why2 = "K = 40 language-modelling cost %.2f nats" % lm40 if not ok40 else ""
        parts.append("NOT READ: " + ", ".join(unread) + " (" + "; ".join(x for x in (why, why2) if x) + " > 2)")
    if not parts:
        return "NONE OF THE THREE"
    return "; ".join(parts)


# ----------------------------------------------------------------------------------------------- stages

def stage_setsize(args, log, sess, tok):
    comps = sess.A.components()
    pairs, fc, fx, docs, ids = load_data(args, tok, sess, log)
    gap = fc - fx
    keep = np.abs(gap) > args.min_gap
    if args.task == "object":
        ranking, source, share = ranking_object(args)
        frozen = F.frozen_object(args)[0]
    else:
        ranking, source, share = ranking_wordorder(args, comps)
        frozen = F.frozen_wordorder(args)[0]
    if tuple(ranking[:10]) != tuple(frozen):
        raise SystemExit("the ranking's top 10 differ from step 4's frozen 10 heads")
    log.kv("ranking: top 10 equal to step 4's frozen 10 heads (asserted)", ", ".join(M.cname(c) for c in frozen))
    kind_of = {}
    if args.task == "wordorder":
        ex = np.load(M.OUT / f"exact_wordorder_{args.model}.npz")
        kind_of = {str(ex["comps"][ex["idx"][j]]): str(ex["kind"][j]) for j in range(len(ex["idx"]))}
    n_exact = source.count("exact")
    log.kv("ranking: heads ranked by exact share / by the screen alone (of all heads)", f"{n_exact} / {len(ranking) - n_exact}")
    log.table(["rank", "head", "ranked by", "share (exact; screened where ranked by the screen)"],
              [[i + 1, M.cname(c), source[i], share[M.cname(c)]] for i, c in enumerate(ranking[:max(KS)])], floatfmt="{:.4f}")
    est, held = M.heldout_sentences(args.sentences, args.n_mean, args.n_read)
    means, cnt = M.estimate_means(sess, tok, est)
    zeros = {k: torch.zeros_like(v) for k, v in means.items()}
    log.kv("mean-estimation positions: special / masked / other", " / ".join(f"{int(x):,}" for x in cnt))
    r0 = M.readability(sess, tok, held)
    out = {"f_clean": fc, "f_corrupt": fx, "docs": docs, "ids": ids, "Ks": np.array(KS),
           "ranking": np.array([M.cname(c) for c in ranking[:max(KS)]]), "ranked_by": np.array(source[:max(KS)])}
    f = M.OUT / f"setsize_{args.task}_{args.model}.npz"
    R = {}       # per K: results
    lm = []
    t_f = t_n = 0.0
    n_sets_total = n_nec_total = 0
    for K in KS:
        top = tuple(ranking[:K])
        n_r = args.n_random if K <= 20 else max(1, args.n_random // 2)
        rand, rst = M.matched_random_sets(comps, top, n_r, seed=SEED_SETS)
        sets = [top] + rand
        n_screen = sum(1 for c in top if source[ranking.index(c)] == "screen")
        n_top30 = sum(1 for c in top if kind_of.get(M.cname(c), "").startswith("screen top 30"))
        n_matched = sum(1 for c in top if kind_of.get(M.cname(c), "").startswith("matched random"))
        n_distinct = len({c for s_ in rand for c in s_})
        log.h2(f"K = {K}")
        log.kv("heads of the set ranked by the screen alone", f"{n_screen} of {K}")
        if args.task == "wordorder":
            log.kv("heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads", f"{n_top30} / {n_matched} (of {K})")
        log.kv("distinct heads used by the random sets (of the heads outside the top-K set)", f"{n_distinct} of {len(comps) - sum(1 for c in comps if c[0] == 'mlp') - K}")
        log.kv("random sets: distinct of asked / replacements / layer-unmatched / type-unmatched",
               f"{rst['distinct']} of {n_r} / {rst['replacements']} / {rst['layer-unmatched']} / {rst['type-unmatched']}")
        log.kv("set", ", ".join(M.cname(c) for c in top))
        faith, tf = faithfulness(sess, pairs, sets, args.max_rows, f"K={K}")
        nc, nx, tn = necessity(sess, pairs, sets, means, args.task, args.max_rows, f"K={K}")
        t_f, t_n, n_sets_total = t_f + tf, t_n + tn, n_sets_total + len(sets)
        n_nec_total += len(sets)
        res = {"faith": summarise(faith - fx[:, None], gap, keep, docs),
               "mean": summarise(lost_of(args.task, fc, fx, nc, nx), gap, keep, docs), "n_screen": n_screen, "rst": rst,
               "n_top30": n_top30, "n_matched": n_matched, "n_distinct": n_distinct}
        lost = {"mean": lost_of(args.task, fc, fx, nc, nx)}
        out.update({f"faith_K{K}": faith, f"nec_clean_K{K}": nc, f"nec_corrupt_K{K}": nx,
                    f"sets_K{K}": np.array(["|".join(M.cname(c) for c in s) for s in sets])})
        if K in ZERO_KS:
            zc, zx, tz = necessity(sess, pairs, sets, zeros, args.task, args.max_rows, f"K={K} zero")
            t_n += tz
            n_nec_total += len(sets)
            lost["zero"] = lost_of(args.task, fc, fx, zc, zx)
            res["zero"] = summarise(lost["zero"], gap, keep, docs)
            out.update({f"zero_clean_K{K}": zc, f"zero_corrupt_K{K}": zx})
        res["lost"] = lost
        rc = M.readability(sess, tok, held, top, means)
        rr = [M.readability(sess, tok, held, s, means) for s in rand[:10]]
        res["lm"] = {"mean": rc - r0}
        lm += [lm_rows(f"K={K} top set, mean ablation", r0, rc)] + [lm_rows(f"K={K} random set {i}, mean ablation", r0, x) for i, x in enumerate(rr)]
        if K in ZERO_KS:
            rz = M.readability(sess, tok, held, top, zeros)
            res["lm"]["zero"] = rz - r0
            lm.append(lm_rows(f"K={K} top set, zero ablation", r0, rz))
        R[K] = res
        np.savez_compressed(f, **out)     # partial save: every finished K is kept if the job is killed
        print(f"    saved {f.name} after K = {K}", flush=True)
    np.savez_compressed(f, **out)
    log.output(str(f), "per item and set: faithfulness and ablated metrics (set 0 of each K is the top-K set); zero ablation for K = 10, 40")
    log.kv("items / with a gap above --min-gap / documents", f"{len(pairs)} / {int(keep.sum())} / {len(set(docs[keep].tolist()))}")
    log.kv("timing: seconds per item per set (faithfulness, over all K) / per item per ablated set (necessity, mean and zero; word order ablates both runs)",
           f"{t_f / (len(pairs) * n_sets_total):.4f} ({n_sets_total} sets) / {t_n / (len(pairs) * n_nec_total):.4f} ({n_nec_total} ablated sets)")

    hdr = ["K", "set", "from screen alone", "share (restored by patching, or lost by ablating)", "document bootstrap 95%", "random sets, mean",
           "random sets, 95th pct", "rank among random (1 = best)", "top-K minus random-K", "sign-flip p (set minus random mean)",
           "random sets distinct", "distinct heads in random sets", "top-K heads: screen top 30 / matched random (word order)"]
    for name, key in (("Faithfulness (patch the set into the corrupted run)", "faith"),
                      ("Necessity, mean ablation (share lost when the set is ablated)", "mean"),
                      ("Necessity, zero ablation", "zero")):
        rows = []
        for K in KS:
            if key not in R[K]:
                continue
            s = R[K][key]
            rows.append([K, f"top {K}", R[K]["n_screen"], s["share"], f"[{s['ci'][0]:.3f}, {s['ci'][1]:.3f}]", s["rand_mean"],
                         s["rand_p95"], f"{s['rank']} of {s['n_rand'] + 1}", s["share"] - s["rand_mean"], s["p"], R[K]["rst"]["distinct"],
                         R[K]["n_distinct"], f"{R[K]['n_top30']} / {R[K]['n_matched']}" if args.task == "wordorder" else "-"])
        log.h2(name)
        log.table(hdr, rows, floatfmt="{:.4g}")
    log.h2("Language-modelling check (held-out nats per subtoken; the 2-nat rule)")
    log.kv("unablated", f"{r0:.4f}")
    log.table(["model", "held-out nats per subtoken", "minus unablated", "within 2 nats"], lm)

    log.h2("Declared reading (P3): necessity at K = 40 minus at K = 10")
    labels = {}
    for abl in ("mean", "zero"):
        n10, n40 = R[10][abl]["share"], R[40][abl]["share"]
        d_item = R[40]["lost"][abl][:, 0] - R[10]["lost"][abl][:, 0]
        lo, hi = M.doc_bootstrap_ratio(d_item[keep], gap[keep], docs[keep])
        first40 = R[40][abl]["n_ge"] == 0
        lm10, lm40 = R[10]["lm"][abl], R[40]["lm"][abl]
        v = verdict(n10, n40, lo, hi, first40, lm10, lm40)
        note = []
        labels[abl] = (v, note)
        log.table(["ablation", "necessity K=10", "necessity K=40", "K=40 minus K=10", "document bootstrap 95%",
                   "top-40 ranks first among random (necessity)", "LM cost K=10 / K=40 (nats)", "verdict"],
                  [[abl, n10, n40, n40 - n10, f"[{lo:.3f}, {hi:.3f}]", "yes" if first40 else "no", f"{lm10:.2f} / {lm40:.2f}", v]],
                  floatfmt="{:.4g}")
        log.kv(f"DECISION setsize {args.task} {args.model} ({abl} ablation)", v + ("; " + "; ".join(note) if note else ""))
    dep = labels["mean"][0] != labels["zero"][0]
    log.kv(f"DECISION setsize {args.task} {args.model}",
           f"{labels['mean'][0]} (mean ablation)" + (f"; ABLATION-DEPENDENT: zero ablation gives {labels['zero'][0]}" if dep else "; the same under zero ablation"))
    log.note("Word order: the exact stage patched only 60 heads (the screen's top 30 and 30 matched heads), so every top-K set "
             "up to K = 40 is drawn from those 60 and no K here reaches a head the screen ranked low; word-order sets are "
             "the best of a pre-selected pool." if args.task == "wordorder" else
             "Agreement: every head was patched exactly, so the ranking is exact for all K.")
    if args.task == "wordorder":
        log.note("The K = 40 comparison is: the top 40 of a 60-head pool against the rest of the same layers. About a third of "
                 "the top 40 are heads the exact stage drew as matched random heads (counts per K in the first table).")


DECLARED_COUNTS = {3: 60, 2: 40, 1: 30, 0: 30}      # XLM-R-large random subsets by overlap with the frozen five
N_NEC = {"muril": 100, "xlmrlarge": 60}


def mlp_design(L, fl, per_class=None, seed=SEED_DATA, k=5):
    """The 5-subsets of the L blocks' MLPs under test, never the frozen set, no duplicates. Returns (list of sorted
    layer tuples, overlap array). per_class None is the declared design: when every subset can be enumerated cheaply
    (C(L, 5) <= 2000: MuRIL, 791 others) all of them; otherwise (XLM-R-large) all sets sharing k-1 of the frozen five
    and DECLARED_COUNTS random sets for overlap 3, 2, 1, 0. per_class = N (smoke tests): N random sets per overlap
    class (fewer where fewer exist)."""
    rng = np.random.default_rng(seed)
    fz = frozenset(fl)
    rest = [l for l in range(L) if l not in fz]
    ov = lambda c: len(fz & set(c))
    sets = []
    if math.comb(L, k) <= 2000:
        pool = {c: [] for c in range(k)}
        for c in itertools.combinations(range(L), k):
            if frozenset(c) != fz:
                pool[ov(c)].append(c)
        for c in range(k):
            if per_class is None:
                sets += pool[c]
            else:
                pick = rng.choice(len(pool[c]), size=min(per_class, len(pool[c])), replace=False)
                sets += [pool[c][i] for i in sorted(pick)]
    else:
        for c in range(k - 1, -1, -1):
            total = math.comb(k, c) * math.comb(len(rest), k - c)
            want = DECLARED_COUNTS.get(c) if per_class is None else per_class
            if want is None:              # overlap k - 1, declared design: every such subset
                for keep_ in itertools.combinations(sorted(fz), c):
                    for r in itertools.combinations(rest, k - c):
                        sets.append(tuple(sorted(keep_ + r)))
                continue
            seen = set()
            want = min(want, total)
            while len(seen) < want:
                a = rng.choice(sorted(fz), size=c, replace=False) if c else []
                b = rng.choice(rest, size=k - c, replace=False)
                seen.add(tuple(sorted(int(x) for x in list(a) + list(b))))
            sets += sorted(seen)
    sets = [tuple(int(x) for x in s) for s in sets]
    assert len(set(sets)) == len(sets) and all(frozenset(s) != fz for s in sets)
    return sets, np.array([ov(s) for s in sets])


def stratified_sample(overlap, n, seed=SEED_DATA, min_per=2):
    """Indices (sorted) of a random sample of n of the sets, stratified by overlap count: proportional allocation by
    largest remainder with at least min_per from each class that has that many (then reduced from the largest classes)."""
    rng = np.random.default_rng(seed)
    cls = sorted(set(overlap.tolist()))
    size = np.array([int((overlap == c).sum()) for c in cls])
    n = min(n, int(size.sum()))
    ideal = n * size / size.sum()
    alloc = np.maximum(np.minimum(min_per, size), np.floor(ideal)).astype(int)
    while alloc.sum() > n:
        j = int(np.argmax(np.where(alloc > np.minimum(min_per, size), alloc, -1)))
        alloc[j] -= 1
    while alloc.sum() < n:
        j = int(np.argmax(np.where(alloc < size, ideal - alloc, -np.inf)))
        alloc[j] += 1
    out = []
    for c, a in zip(cls, alloc):
        idx = np.flatnonzero(overlap == c)
        out += list(rng.choice(idx, size=int(a), replace=False))
    return np.array(sorted(out))


def lm_sample(overlap, n=10, seed=SEED_DATA):
    """n sets drawn across the overlap classes (2 per class, then topped up at random), never the first n."""
    rng = np.random.default_rng(seed + 1)
    out = []
    for c in sorted(set(overlap.tolist())):
        idx = np.flatnonzero(overlap == c)
        out += list(rng.choice(idx, size=min(2, len(idx)), replace=False))
    left = [i for i in range(len(overlap)) if i not in out]
    while len(out) < min(n, len(overlap)) and left:
        out.append(left.pop(int(rng.integers(len(left)))))
    return np.array(sorted(out[:n]))


def depth_regression(effect, gap, keep, docs, blocks, overlap, B=1000, seed=707):
    """Faithfulness of the sets (ratio of sums over items above the floor) regressed on the mean block index and the
    overlap count; document-bootstrap percentile interval of each coefficient (resample documents, recompute each set's
    ratio of sums over the resampled documents, refit). Returns (beta, ci) for [intercept, block index, overlap]."""
    d = docs[keep]
    u = sorted(set(d.tolist()))
    pos = {k_: i for i, k_ in enumerate(u)}
    idx = np.array([pos[x] for x in d])
    Dm = np.zeros((len(u), effect.shape[1]))
    np.add.at(Dm, idx, effect[keep])
    gd = np.zeros(len(u))
    np.add.at(gd, idx, gap[keep])
    X = np.column_stack([np.ones(len(blocks)), blocks, overlap])
    pinv = np.linalg.pinv(X)
    beta = pinv @ (Dm.sum(0) / gd.sum())
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(u), size=(B, len(u)))
    counts = np.stack([np.bincount(p_, minlength=len(u)) for p_ in pick]).astype(float)
    share = (counts @ Dm) / (counts @ gd)[:, None]
    bs = (pinv @ share.T).T
    return beta, np.percentile(bs, [2.5, 97.5], axis=0).T


def stage_mlpsets(args, log, sess, tok):
    from scipy.stats import spearmanr
    pairs, fc, fx, docs, ids = load_data(args, tok, sess, log)
    gap = fc - fx
    keep = np.abs(gap) > args.min_gap
    frozen = tuple((F.frozen_object(args)[1] if args.task == "object" else F.frozen_wordorder(args)[1]))
    fl = [c[1] for c in frozen]
    log.kv("frozen top 5 MLPs (step 4 selection half)", ", ".join(M.cname(c) for c in frozen))
    L = sess.A.L
    subs, ov_r = mlp_design(L, fl, args.n_random)
    sets = [frozen] + [tuple(("mlp", l) for l in s) for s in subs]
    overlap = np.concatenate([[5], ov_r])
    blocks = np.array([np.mean([c[1] for c in s]) for s in sets])
    log.kv("sets tested (frozen set + others) / design",
           f"{len(sets)} ({len(subs)} others) / " + ("smoke: %d per overlap class" % args.n_random if args.n_random else "declared"))
    log.kv("number of sets by overlap with the frozen five (0 / 1 / 2 / 3 / 4)", " / ".join(str(int((ov_r == c).sum())) for c in range(5)))
    if not args.n_random:
        if L == 12 and len(subs) != 791:
            raise SystemExit("the MuRIL design must be all 791 other subsets")
        if L != 12 and [int((ov_r == c).sum()) for c in range(5)] != [30, 30, 40, 60, 95]:
            raise SystemExit("the XLM-R-large design must be 95 / 60 / 40 / 30 / 30 by overlap 4 / 3 / 2 / 1 / 0")
    nec_idx = stratified_sample(ov_r, args.n_nec or N_NEC[args.model]) + 1     # indices into sets (0 is the frozen set)
    log.kv("necessity sample (random, stratified by overlap; frozen set always included): size / by overlap 0 to 4",
           f"{len(nec_idx)} / " + " / ".join(str(int((overlap[nec_idx] == c).sum())) for c in range(5)))
    est, held = M.heldout_sentences(args.sentences, args.n_mean, args.n_read)
    means, cnt = M.estimate_means(sess, tok, est)
    log.kv("mean-estimation positions: special / masked / other", " / ".join(f"{int(x):,}" for x in cnt))
    faith, tf = faithfulness(sess, pairs, sets, args.max_rows, "mlps")
    nsets = [sets[0]] + [sets[i] for i in nec_idx]
    nc, nx, tn = necessity(sess, pairs, nsets, means, args.task, args.max_rows, "mlps")
    lost = lost_of(args.task, fc, fx, nc, nx)
    r0 = M.readability(sess, tok, held)
    rc = M.readability(sess, tok, held, frozen, means)
    lm_idx = lm_sample(ov_r) + 1
    rr = [M.readability(sess, tok, held, sets[i], means) for i in lm_idx]
    f = M.OUT / f"mlpsets_{args.task}_{args.model}.npz"
    np.savez_compressed(f, faith=faith, nec_clean=nc, nec_corrupt=nx, nec_idx=np.concatenate([[0], nec_idx]), f_clean=fc, f_corrupt=fx,
                        docs=docs, ids=ids, overlap=overlap, blocks=blocks, lm_idx=lm_idx,
                        sets=np.array(["|".join(M.cname(c) for c in s) for s in sets]))
    log.output(str(f), "per item and set: faithfulness (all sets) and ablated metrics (nec_idx = the frozen set and the necessity sample); "
                       "set 0 is the frozen top 5 MLPs; overlap = frozen MLPs contained")
    log.kv("timing: seconds per item per set (faithfulness, %d sets / necessity, %d sets)" % (len(sets), len(nsets)),
           f"{tf / (len(pairs) * len(sets)):.4f} / {tn / (len(pairs) * len(nsets)):.4f}")

    eff = faith - fx[:, None]
    sh = eff[keep].sum(0) / gap[keep].sum()
    fa = summarise(eff, gap, keep, docs)
    ne = summarise(lost, gap, keep, docs)
    names = lambda s: ", ".join(M.cname(c) for c in s)
    log.h2("Frozen top 5 MLPs against the other sets (descriptive: rank among all others, difference from their mean)")
    log.table(["measure", "frozen set", "document bootstrap 95%", "others, mean", "others, 95th pct",
               "rank among others (1 = best)", "sign-flip p, two-sided", "sign-flip p, one-sided"],
              [[n, s["share"], f"[{s['ci'][0]:.3f}, {s['ci'][1]:.3f}]", s["rand_mean"], s["rand_p95"], f"{s['rank']} of {s['n_rand'] + 1}", s["p"], s["p_one"]]
               for n, s in (("faithfulness (all sets)", fa), ("necessity (sample)", ne))], floatfmt="{:.4g}")
    log.h2("Sets by the number of the frozen five they contain")
    rows = []
    ov_n = overlap[np.concatenate([[0], nec_idx])]
    for c in range(6):
        m = overlap == c
        mn = ov_n == c
        rows.append([c, int(m.sum()), float(sh[m].mean()) if m.any() else "-", float(sh[m].max()) if m.any() else "-",
                     int(mn.sum()), float(ne["all"][mn].mean()) if mn.any() else "-"])
    log.table(["frozen MLPs contained", "sets", "mean faithfulness", "best faithfulness", "sets with necessity", "mean necessity"], rows, floatfmt="{:.4g}")
    log.note("The row for 5 is the frozen set itself.")
    rho, p_rho = spearmanr(overlap[1:], sh[1:])
    log.kv("Spearman of the overlap count with faithfulness over the other sets: rho / p (two-sided)", f"{rho:.3f} / {p_rho:.4g}")

    # ---- decision
    log.h2("Declared reading (P4, third addendum)")
    tie = 0.02
    cand = np.flatnonzero(overlap[1:] <= 3) + 1
    b = int(cand[np.argmax(sh[cand])])
    margin = float(sh[0] - sh[b])
    diff = (eff[:, 0] - eff[:, b])[keep]
    p_best = M.doc_signflip(diff, docs[keep], one_sided=True)
    lo_b, hi_b = M.doc_bootstrap_ratio((eff[:, 0] - eff[:, b])[keep], gap[keep], docs[keep])
    specific = bool(margin >= tie and p_best < 0.05)
    log.kv("best set sharing at most three of the frozen MLPs: set / overlap / faithfulness", f"{names(sets[b])} / {int(overlap[b])} / {sh[b]:.4f}")
    log.kv("frozen set faithfulness minus best (margin 0.02 declared) / document bootstrap 95% (descriptive) / one-sided sign-flip p",
           f"{margin:.4f} / [{lo_b:.3f}, {hi_b:.3f}] / {p_best:.4g}")
    b4 = np.flatnonzero(overlap[1:] == 4) + 1
    if len(b4):
        j4 = int(b4[np.argmax(sh[b4])])
        log.kv("descriptive: best set sharing four of the frozen five: set / faithfulness / frozen minus it",
               f"{names(sets[j4])} / {sh[j4]:.4f} / {sh[0] - sh[j4]:.4f}")
    oth = sh[1:]
    log.kv("descriptive: other sets within 0.02 of the frozen set (ties, either side) / above it by more than 0.02 / of all others",
           f"{int((np.abs(oth - sh[0]) <= tie).sum())} ({100 * float((np.abs(oth - sh[0]) <= tie).mean()):.1f}%) / {int((oth > sh[0] + tie).sum())} / {len(oth)}")
    log.table(["overlap", "sets", "within 0.02 of the frozen set", "above it by more than 0.02"],
              [[c, int((ov_r == c).sum()), int(((np.abs(oth - sh[0]) <= tie) & (ov_r == c)).sum()), int(((oth > sh[0] + tie) & (ov_r == c)).sum())] for c in range(5)])
    beta, ci = depth_regression(eff, gap, keep, docs, blocks, overlap.astype(float), B=1000)
    log.table(["term", "coefficient", "document bootstrap 95% (1,000 draws, seed 707)"],
              [[n, float(beta[i]), f"[{ci[i][0]:.4f}, {ci[i][1]:.4f}]"] for i, n in enumerate(["intercept", "mean block index (per block)", "overlap count"])],
              floatfmt="{:.4g}")
    depth = bool((not specific) and beta[1] > 0 and ci[1][0] > 0)
    label = "SPECIFIC" if specific else ("DEPTH" if depth else "NEITHER")
    fb = ", ".join(str(l) for l in sorted(fl, reverse=True))
    log.kv("SPECIFIC (margin >= 0.02 and p < 0.05) / DEPTH (block-index coefficient > 0, interval excludes 0)",
           f"{'yes' if specific else 'no'} / {'yes' if depth else 'no'}")
    log.h2("Language-modelling check (held-out nats per subtoken; frozen set and 10 sets drawn across overlap classes)")
    log.kv("unablated", f"{r0:.4f}")
    log.table(["model", "overlap", "held-out nats per subtoken", "minus unablated", "within 2 nats"],
              [["frozen top 5 MLPs ablated", 5] + lm_rows("", r0, rc)[1:]] +
              [[f"set {names(sets[i])}", int(overlap[i])] + lm_rows("", r0, x)[1:] for i, x in zip(lm_idx, rr)])
    lm_note = "" if rc - r0 <= 2 else f"; necessity not read (the frozen set's language-modelling cost is {rc - r0:.2f} nats > 2)"
    log.kv(f"DECISION mlpsets {args.task} {args.model}", f"{label} (frozen MLPs of blocks {fb})" + lm_note)
    log.note("Selecting the best of many sets on the same data favours the other sets, so SPECIFIC is the conservative reading; "
             "the regression includes the frozen set (overlap 5).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", required=True, choices=["setsize", "mlpsets"])
    ap.add_argument("--task", required=True, choices=["object", "wordorder"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None, help="first N items only (smoke tests)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--chunk", type=int, default=16, help="accepted for launcher symmetry with mi_agreement; unused here")
    ap.add_argument("--max-rows", type=int, default=256, help="rows per forward in patching and ablation")
    ap.add_argument("--n-random", type=int, default=None, help="setsize: random head sets for K up to 20 (half for K = 40), default 100; "
                    "mlpsets: smoke tests only, N sets per overlap class instead of the declared design (needs --limit)")
    ap.add_argument("--n-nec", type=int, default=None, help="mlpsets: size of the necessity sample (default 100 MuRIL, 60 XLM-R-large)")
    ap.add_argument("--n-mean", type=int, default=300, help="held-out sentences for the ablation means")
    ap.add_argument("--n-read", type=int, default=100, help="held-out sentences for the language-modelling check")
    ap.add_argument("--sentences", default=str(M.ROOT / "data" / "heldout_text" / "readability_sentences.txt"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    if args.stage == "mlpsets" and (args.n_random or args.n_nec) and not args.limit:
        raise SystemExit("mlpsets has a declared design: --n-random and --n-nec are for smoke tests (with --limit) only")
    if args.stage == "setsize" and args.n_random is None:
        args.n_random = 100
    if args.task == "object":
        A.require_metric(SimpleNamespace(model=args.model))
    M.OUT.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"mi_paper_{args.stage}_{args.task}_{args.model}"
    with RunLog(tag, __file__, args, purpose=f"Paper experiments, stage {args.stage}, task {args.task}, {args.model}.") as log:
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            text = pd.read_csv(M.ITEMS / "wordorder_pairs.csv").ref_text.iloc[0]
            lay = M.check_head_layout(sess, tok, text)
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            {"setsize": stage_setsize, "mlpsets": stage_mlpsets}[args.stage](args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
