#!/usr/bin/env python3
"""Step 4, agreement: which heads and MLPs compute object agreement, and why an intervening subject misleads
MuRIL and not XLM-R-large (REMAINING_EXPERIMENTS.md, section A). GPU, per model (--model muril | xlmrlarge).
Declared before any run (23 Oct 2026). Items, pairs and the document split come from mi_items.py.

THE METRIC. M = log2 P(correct agreeing words | rest) - log2 P(wrong agreeing words | rest), in bits, the rest of
the sentence identical in both. The agreeing words whose wrong form differs ("the span") are scored as one
left-to-right chain over their subtokens: row i masks span subtoken i and every later span subtoken. So M is a
proper log-probability ratio of the two verb complexes in one context, unlike the baseline's whole-sentence
margin A, which also rescores every other word against a different verb. M costs about an eighth of A.

TWO CORRUPTIONS, because the two questions differ:
  object   (both models) the clean run is the order as written; the corrupted run masks every word of the object
           phrase (its subtree before the verb complex) in every row. Masking is in distribution for a masked
           LM, unlike noise. What restores M is what carries the object's agreement features to the verb.
  contrast (the attraction itself) the clean run is an SOV-type order and the corrupted run the OSV-type order of
           the same clause at the same object-verb gap (the 670 contrast pairs); positions are aligned word by
           word through the tree index. What restores M is what produces the attraction. XLM-R-large shows no
           attraction (baseline: -0.21 bits, p 0.58), so for it this task has no gap to recover and is screened
           only; MuRIL's is the one patched exactly.

STAGES (each writes outputs/<stage>_<task>_<model>.* and a record mi_<stage>_<task>_<model>.md)
  metric     A0, every order (5,265): M with nothing masked, with the object phrase masked, with the subject
             phrase masked (ne kept), with ne masked. Per condition: share M > 0, mean M, and the intervening-
             subject contrast exactly as the baseline (gap-matched, variants, object not adjacent, per clause,
             document-level sign flip, 10,000, seed [707, model index]). CHECKS: on orders whose span is one
             tokenizer word, M reproduces lm_units.score_words' surprisals of that word (at least 20 orders, 1e-3
             bits); on orders whose span has two or more words, M reproduces an independent one-pass-at-a-time
             computation through the model's own full logits (at least 10 orders, 1e-3 bits). DECISION RULE (revised
             on review, 23 Oct, before any run): M is used by the later stages if both checks pass, its Spearman
             correlation with the baseline's whole-sentence A over all orders is at least 0.5, it prefers the
             correct form in at least 80% of orders, and, for MuRIL, its intervening-subject contrast is negative
             with p < 0.05 (the baseline's finding). XLM-R-large's contrast is reported, not gated on: a more
             sensitive metric may find a small effect the baseline missed, and the object task does not depend on
             it. Otherwise the record says REJECTED and the later stages refuse to run; falling back to the
             whole-sentence margin would then need a code change, made and reviewed before any rerun. Only a full
             run (no --limit) writes the decision.
  screen     A1 (task object) and the A3 screen (task contrast): attribution patching of every head and MLP, per
             position class (special, agree, verb, object, subject, ne, other), on the selection half.
  exact      A2 (task object) and A3 (task contrast, MuRIL): every component patched alone at every position, on
             the selection half; then the top 20 by that share patched at each position class alone, and the top
             K for K in 1, 2, 5, 10, 20 patched jointly. Recovered share = ratio of sums over items whose gap
             |f_clean - f_corrupt| exceeds --min-gap bits, with a document-bootstrap interval (descriptive). Spearman
             between the screen and the exact shares says whether the screen is trustworthy for this model.
             CHECK: patching the embedding output at every position recovers the gap (ratio of sums within 1e-3,
             worst item 5e-3 bits), on the first five items.
  attention  A4 (eager attention): for the top 5 heads of the object task's exact stage, and for every head, the
             attention from the scored span position of each row (a [MASK], with the later span subtokens masked
             too: the rows of the correct sentence's span chain, nothing else masked) to the object, subject and ne
             words, renormalised over real subtokens. Orders of the selection half's contrast pairs. Contrast of each share,
             OSV-type minus SOV-type, gap-matched as the baseline, document sign flip. Descriptive: the subject is
             nearer the verb in an OSV-type order, so a shift of attention toward it is partly distance; it is read
             against A2 and A5 and against the other model, never alone.
  path       A5, path patching into the top 5 heads of the object task: in the object-masked run, only the head's
             keys and values are patched from the clean run, at the object words, the subject words, ne, every
             position, and (control) as many randomly chosen 'other' positions as the object has (seed 707).
             The share of the gap restored through each sender set, selection half.
  every stage first checks the head layout on one sentence (mi_lib.check_head_layout: attention probabilities of
             head h times value slice h equal slice h of the attention output projection's input, 1e-3), so a
             head's slice, key and value are that head's.
  --half     selection by default, held-out for validate; smoke tests pass --half selection to every stage, so
             no component is chosen, and no screen or patching stage run, on the held-out half before the full
             validation runs. (The metric stage scores every order of both halves by design: it chooses nothing.)
             A validate run with --half selection is refused unless --limit is set (a smoke test).
  validate   AV, on the held-out half, once. The circuit is the top --k HEADS of the exact stage (selection half);
             MLPs are judged apart (revised after the smoke tests, 23 Oct, before any full run): a model has one MLP
             per block, 12 or 24, and the top components are mostly MLPs, so a "circuit" of MLPs leaves too few to
             draw matched random sets from (the smoke test replaced most of them by heads), and mean-ablating that
             many MLPs breaks the model (MuRIL +5.2 nats). Each of the top --k-mlp MLPs is instead patched again on
             the held-out half, and its share there is reported beside its selection-half share (replication). Faithfulness: the corrupted run with only the circuit patched (jointly) from the clean run.
             Necessity: the clean run with the circuit mean-ablated (means over special, masked and other positions
             separately, from held-out IndicCorp text, mi_lib.estimate_means). Both against --n-random component
             sets matched in type and layer as far as the circuit allows (mi_lib.matched_random_sets, seed 707; the record counts unmatched replacements and distinct sets): the circuit's rank among them (empirical p), and a
             document-level sign flip of the per-item circuit-minus-random-mean difference (10,000). The
             language-modelling check: mean surprisal per subtoken on 100 held-out sentences with the circuit and
             with 10 of the random sets ablated, against the unablated model (2-nat rule).
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
from runlog import RunLog, sha256  # noqa: E402

CLASSES = ["special", "agree", "verb", "object", "subject", "ne", "other"]
ITEMS = M.ITEMS
MODEL_INDEX = {"muril": 0, "xlmrlarge": 2}   # seed index each model had in the baseline (baseline_check.py)


def ints(s):
    s = str(s)
    return [int(x) for x in s.split("|")] if s and s != "nan" else []


def word_class(o):
    agree, verb = set(ints(o.agree_words)), set(ints(o.verb_words))
    obj, subj, ne = set(ints(o.obj_words)), set(ints(o.subj_words)), int(o.ne_word)

    def f(w):
        if w in agree:
            return 1
        if w in verb:
            return 2
        if w in obj:
            return 3
        if w in subj:
            return 4
        if w == ne:
            return 5
        return 6
    return f


def runs_for(tok, o, cond="none"):
    mask = {"none": [], "obj": ints(o.obj_words), "subj": ints(o.subj_words), "ne": [int(o.ne_word)]}[cond]
    wc = word_class(o)
    a = M.span_run(tok, o.correct, ints(o.agree_words), +1, mask, wc)
    b = M.span_run(tok, o.foil, ints(o.agree_words), -1, mask, wc)
    if a is None or b is None or a.ids.shape[1] > 256 or b.ids.shape[1] > 256:
        return None
    return [a, b]


def ident(run):
    return torch.arange(run.ids.shape[1], device=run.ids.device)


def object_pair(tok, o):
    clean, corr = runs_for(tok, o, "none"), runs_for(tok, o, "obj")
    if clean is None or corr is None:
        return None
    return M.Pair(corrupt=corr, clean=clean, align=[ident(r) for r in corr],
                  meta={"id": o.order_id, "doc": o.doc})


def contrast_pair(tok, osv, sov, pid, doc):
    corr = runs_for(tok, osv, "none")
    if corr is None:
        return None
    t_osv, t_sov = ints(osv.tok_order), ints(sov.tok_order)
    w_sov = {t: i for i, t in enumerate(t_sov)}
    wmap = {i: w_sov[t] for i, t in enumerate(t_osv)}
    clean, align = [], []
    for run, text in zip(corr, (sov.correct, sov.foil)):
        c, a = M.mapped_run(tok, run, text, wmap, word_class(sov))
        clean.append(c)
        align.append(a)
    return M.Pair(corrupt=corr, clean=clean, align=align, meta={"id": pid, "doc": doc})


LISTS = {c: str for c in ("tok_order", "agree_words", "verb_words", "obj_words", "subj_words")}


def read_positions():
    return pd.read_csv(ITEMS / "agreement_positions.csv", dtype=LISTS)


def load_items(args, half):
    half = args.half or half
    pos = read_positions()
    cp = pd.read_csv(ITEMS / "contrast_pairs.csv")
    if args.task == "object":
        o = pos[pos.in_contrast & (pos.half == half)]
        if args.limit:
            o = o.head(args.limit)
        return [("o", r) for r in o.itertuples()]
    c = cp[cp.half == half]
    if args.limit:
        c = c.head(args.limit)
    by = pos.set_index(["ref_id", "order_id"])
    return [("c", r, by.loc[(r.ref_id, r.osv_order)], by.loc[(r.ref_id, r.sov_order)]) for r in c.itertuples()]


def build_pairs(tok, items):
    out, skipped = [], 0
    for it in items:
        p = object_pair(tok, it[1]) if it[0] == "o" else contrast_pair(tok, it[2], it[3], it[1].pair_id, it[1].doc)
        if p is None:
            skipped += 1
        else:
            out.append(p)
    return out, skipped


def gaps(sess, pairs):
    fc = np.array([M.metric(sess, p.clean) for p in pairs])
    fx = np.array([M.metric(sess, p.corrupt) for p in pairs])
    return fc, fx


def contrast_test(df, value, seed):
    """The baseline's gap-matched contrast on any per-order value: variants, object not adjacent, OSV-type minus
    SOV-type within clause and gap, averaged per clause, document-level sign flip."""
    z = df[~df.is_reference & ~df.object_adjacent]
    g = z.groupby(["ref_id", "clause_head", "object_verb_gap", "order_class"])[value].mean().unstack()
    if not {"OSV", "SOV"} <= set(g.columns):
        return 0, float("nan"), float("nan")
    g = g.dropna(subset=["OSV", "SOV"])
    if g.empty:
        return 0, float("nan"), float("nan")
    cell = (g["OSV"] - g["SOV"]).groupby(level=["ref_id", "clause_head"]).mean()
    docs = [r.split("__")[0] for r, _ in cell.index]
    sums = pd.Series(cell.to_numpy()).groupby(docs).sum().to_numpy()
    rng = np.random.default_rng(seed)
    null = np.array([(sums * rng.choice([-1.0, 1.0], len(sums))).sum() for _ in range(10000)])
    p = (1 + int((np.abs(null) >= abs(sums.sum())).sum())) / 10001
    return len(cell), float(cell.mean()), p


# ----------------------------------------------------------------------------------------------- stages

def naive_margin(model, tok, o):
    """M computed independently of mi_lib's runs and hooks: one pass at a time, through the model's full logits."""
    agree = set(ints(o.agree_words))
    tot = 0.0
    for text, sign in ((o.correct, 1.0), (o.foil, -1.0)):
        ids, groups, gw, nw, word_of, off = M.tokenise(tok, text)
        span = [p for p in range(len(ids)) if word_of[p] in agree]
        for i, q in enumerate(span):
            x = torch.tensor([ids], device=M.DEVICE)
            x[0, span[i:]] = tok.mask_token_id
            with torch.no_grad():
                lp = torch.log_softmax(model(input_ids=x).logits[0, q].float(), -1)[ids[q]]
            tot += sign * float(lp) / M.LN2
    return tot


def stage_metric(args, log, model, tok, sess):
    import lm_units as U
    pos = read_positions()
    if args.limit:
        pos = pos.head(args.limit)
    conds = ["none", "obj", "subj", "ne"]
    rows, n1, w1, n2, w2 = [], 0, 0.0, 0, 0.0
    for i, o in enumerate(pos.itertuples(), 1):
        rec = {"order_id": o.order_id, "ref_id": o.ref_id}
        for cnd in conds:
            rs = runs_for(tok, o, cnd)
            rec[f"M_{cnd}"] = None if rs is None else M.metric(sess, rs)
        span_words = ints(o.agree_words)
        if rec["M_none"] is not None and len(span_words) == 1 and n1 < 200:
            # spans that are one tokenizer word: the rows are exactly that word's within_word_l2r passes
            g = U.whitespace_groups(tok, o.correct)
            if sum(1 for w in g[2] if w == span_words[0]) == 1:
                sc = U.score_words(model, tok, M.DEVICE, o.correct, args.batch_size, layers=False)[0]
                sf = U.score_words(model, tok, M.DEVICE, o.foil, args.batch_size, layers=False)[0]
                w1 = max(w1, abs(sf[span_words[0]] - sc[span_words[0]] - rec["M_none"]))
                n1 += 1
        if rec["M_none"] is not None and len(span_words) >= 2 and n2 < 50:
            w2 = max(w2, abs(naive_margin(model, tok, o) - rec["M_none"]))
            n2 += 1
        rows.append(rec)
        if i % 500 == 0:
            print(f"    {i:,}/{len(pos):,}", flush=True)
    d = pos.merge(pd.DataFrame(rows), on=["order_id", "ref_id"])
    base = pd.read_csv(M.ROOT / "data" / "agreement" / f"agreement_scores_{args.model}.csv")
    d = d.merge(base, on=["ref_id", "order_id"], how="left", validate="one_to_one")
    d["A"] = d.sum_foil - d.sum_correct
    f = M.OUT / f"metric_{args.model}.csv"
    d.drop(columns=["correct", "foil"]).to_csv(f, index=False)
    log.output(str(f), "per order: M under each masking condition, and the baseline's whole-sentence A")
    log.kv("check: single-word spans against score_words, orders / worst difference (bits)", f"{n1} / {w1:.2e}")
    log.kv("check: multi-word spans against a one-pass-at-a-time computation through the full logits (independent "
           "of the runs, hooks and batching; it shares the tokenisation and the span definition), orders / worst (bits)",
           f"{n2} / {w2:.2e}")
    if w1 > 1e-3 or w2 > 1e-3:
        raise SystemExit("the span margin does not reproduce an independent computation")
    k = MODEL_INDEX[args.model]
    tab = []
    for cnd in conds:
        x = d.dropna(subset=[f"M_{cnd}"])
        n, eff, p = contrast_test(x, f"M_{cnd}", [707, k])
        tab.append([cnd, len(x), float((x[f"M_{cnd}"] > 0).mean()), float(x[f"M_{cnd}"].mean()), n, eff, p])
    log.table(["masked", "orders", "correct preferred (M > 0)", "mean M (bits)", "clauses", "OSV minus SOV (bits)",
               "sign-flip p"], tab, floatfmt="{:.4g}")
    x = d.dropna(subset=["M_none", "A"])
    rho = float(x.M_none.corr(x.A, method="spearman"))
    log.kv("Pearson / Spearman of M (nothing masked) with the baseline's A, orders",
           f"{x.M_none.corr(x.A):.3f} / {rho:.3f} ({len(x):,})")
    _, _, share, _, _, eff, p = tab[0]
    rules = [("single-word check on at least 20 orders", n1 >= 20), ("multi-word check on at least 10 orders", n2 >= 10),
             ("Spearman with A at least 0.5", rho >= 0.5), ("M > 0 in at least 80% of orders", share >= 0.8)]
    if args.model == "muril":
        rules.append(("intervening-subject contrast negative, p < 0.05", eff < 0 and p < 0.05))
    log.table(["rule", "met"], [[r, "yes" if ok else "NO"] for r, ok in rules])
    verdict = all(ok for _, ok in rules)
    if args.limit:
        log.kv("DECISION", f"not written (--limit {args.limit}: only a full run decides)")
    else:
        log.kv("DECISION (metric used by the later stages)", "ACCEPTED" if verdict else "REJECTED")
        (M.OUT / f"metric_{args.model}.decision").write_text("ACCEPTED\n" if verdict else "REJECTED\n")


def require_metric(args):
    """The metric stage's decision, or the author's recorded override of a REJECTED one
    (metric_<model>.override: who decided, when, and why). Returns the text to log."""
    f = M.OUT / f"metric_{args.model}.decision"
    o = M.OUT / f"metric_{args.model}.override"
    if f.exists() and f.read_text().strip() == "ACCEPTED":
        return "ACCEPTED by the metric stage's declared rule"
    if f.exists() and o.exists() and o.read_text().strip():
        return "REJECTED by the declared rule, used under the author's recorded override: " + " ".join(o.read_text().split())
    raise SystemExit("the metric stage has not ACCEPTED the span margin for this model, and no override is recorded")


def stage_screen(args, log, model, tok, sess):
    pairs, skipped = build_pairs(tok, load_items(args, "selection"))
    fc, fx = gaps(sess, pairs)
    att = np.zeros((len(pairs), len(sess.A.components()), len(CLASSES)))
    for i, p in enumerate(pairs):
        att[i], comps = M.atp(sess, p, len(CLASSES), chunk=args.chunk)
        if (i + 1) % 50 == 0:
            print(f"    {i + 1}/{len(pairs)}", flush=True)
    comps = sess.A.components()
    keep = np.abs(fc - fx) > args.min_gap
    f = M.OUT / f"screen_{args.task}_{args.model}.npz"
    np.savez_compressed(f, atp=att, f_clean=fc, f_corrupt=fx, ids=np.array([str(p.meta["id"]) for p in pairs]),
                        docs=np.array([p.meta["doc"] for p in pairs]), comps=np.array([M.cname(c) for c in comps]),
                        classes=np.array(CLASSES))
    log.output(str(f), "attribution per item x component x position class; clean and corrupted metrics")
    log.kv("items / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
    log.kv("mean clean / corrupted metric (bits); total gap", f"{fc.mean():.3f} / {fx.mean():.3f}; {(fc - fx)[keep].sum():.2f}")
    tot = att.sum(2)
    share = tot[keep].sum(0) / (fc - fx)[keep].sum()
    order = np.argsort(-np.abs(share))[:20]
    log.table(["component", "screened share of the gap"] + [f"via {c}" for c in CLASSES],
              [[M.cname(comps[j]), float(share[j])] + [float(att[keep][:, j, c].sum() / (fc - fx)[keep].sum())
                                                        for c in range(len(CLASSES))] for j in order])
    log.p("Shares are first-order estimates (attribution patching): the exact stage checks them.")


def stage_exact(args, log, model, tok, sess):
    pairs, skipped = build_pairs(tok, load_items(args, "selection"))
    fc, fx = gaps(sess, pairs)
    keep = np.abs(fc - fx) > args.min_gap
    gap = fc - fx
    docs = [p.meta["doc"] for p in pairs]
    comps = sess.A.components()
    allpos = lambda p: (lambda ri: torch.arange(p.corrupt[ri].ids.shape[1], device=M.DEVICE))
    # check on the first five items: the embedding output patched at every position restores the clean run
    worst_emb, num, den = 0.0, 0.0, 0.0
    for p, a, b in list(zip(pairs, fc, fx))[:5]:
        e = M.exact(sess, p, [("emb",)], allpos(p), args.max_rows)[0]
        worst_emb = max(worst_emb, abs(e - a))
        num, den = num + (e - b), den + (a - b)
    log.kv("check: embedding output patched everywhere, ratio of sums / worst item (bits)",
           f"{num / den if den else float('nan'):.6f} / {worst_emb:.2e}")
    if (den and abs(num / den - 1) > 1e-3) or worst_emb > 5e-3:
        raise SystemExit("a patching check failed: the alignment or the hooks are wrong")

    res = np.zeros((len(pairs), len(comps)))
    for i, p in enumerate(pairs):
        res[i] = M.exact(sess, p, comps, allpos(p), args.max_rows)
        if (i + 1) % 25 == 0:
            print(f"    {i + 1}/{len(pairs)}", flush=True)
    share = (res - fx[:, None])[keep].sum(0) / gap[keep].sum()
    top = list(np.argsort(-share)[:20])
    # the top 20 at each position class alone
    bycls = np.zeros((len(pairs), len(top), len(CLASSES)))
    for i, p in enumerate(pairs):
        for c in range(len(CLASSES)):
            sel = lambda ri, c=c: torch.nonzero(p.corrupt[ri].pclass == c)[:, 0]
            bycls[i, :, c] = M.exact(sess, p, [comps[j] for j in top], sel, args.max_rows)
    # joint top K
    Ks = [1, 2, 5, 10, 20]
    joint = np.zeros((len(pairs), len(Ks)))
    for i, p in enumerate(pairs):
        joint[i] = M.exact(sess, p, [tuple(comps[j] for j in top[:k]) for k in Ks], allpos(p), args.max_rows)
    f = M.OUT / f"exact_{args.task}_{args.model}.npz"
    np.savez_compressed(f, exact=res, by_class=bycls, joint=joint, top=np.array(top), Ks=np.array(Ks), f_clean=fc,
                        f_corrupt=fx, ids=np.array([str(p.meta["id"]) for p in pairs]), docs=np.array(docs),
                        comps=np.array([M.cname(c) for c in comps]), classes=np.array(CLASSES))
    log.output(str(f), "exact patching: every component alone; the top 20 per position class; the top K jointly")
    log.kv("items / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
    rows = []
    for j in top:
        lo, hi = M.doc_bootstrap_ratio((res[:, j] - fx)[keep], gap[keep], np.array(docs)[keep])
        rows.append([M.cname(comps[j]), float(share[j]), f"[{lo:.3f}, {hi:.3f}]"] +
                    [float((bycls[:, top.index(j), c] - fx)[keep].sum() / gap[keep].sum()) for c in range(len(CLASSES))])
    log.table(["component", "share of the gap restored", "document bootstrap 95%"] + [f"at {c} only" for c in CLASSES], rows)
    log.table(["top K patched jointly", "share restored"],
              [[k, float((joint[:, n] - fx)[keep].sum() / gap[keep].sum())] for n, k in enumerate(Ks)])
    sf = M.OUT / f"screen_{args.task}_{args.model}.npz"
    if sf.exists():
        s = np.load(sf)
        if list(s["ids"]) == [str(p.meta["id"]) for p in pairs]:
            from scipy.stats import spearmanr
            sk = np.abs(s["f_clean"] - s["f_corrupt"]) > args.min_gap
            sshare = s["atp"].sum(2)[sk].sum(0) / (s["f_clean"] - s["f_corrupt"])[sk].sum()
            rho = spearmanr(sshare, share).correlation
            overlap = len(set(np.argsort(-sshare)[:20]) & set(top))
            log.kv("screen against exact: Spearman over components / top-20 overlap", f"{rho:.3f} / {overlap} of 20")
            log.kv("screen input", f"{sf.name} (sha256 {sha256(sf)})")
        else:
            log.kv("screen against exact", "not compared: the screen was run on other items")


def top_heads(args, n):
    """The n heads with the largest exact share of the object task (selection half), from the full ranking."""
    ex = np.load(M.OUT / f"exact_object_{args.model}.npz")
    names = list(ex["comps"])
    sk = np.abs(ex["f_clean"] - ex["f_corrupt"]) > args.min_gap
    share = (ex["exact"] - ex["f_corrupt"][:, None])[sk].sum(0) / (ex["f_clean"] - ex["f_corrupt"])[sk].sum()
    return [M.cparse(names[j]) for j in np.argsort(-share) if "MLP" not in names[j]][:n]


def stage_attention(args, log, model, tok, sess):
    heads = top_heads(args, 5)
    log.kv("heads read (top 5 heads of the object task, exact stage)", ", ".join(M.cname(h) for h in heads))
    pos = read_positions()
    o = pos[pos.in_contrast & (pos.half == (args.half or "selection"))]
    if args.limit:
        o = o.head(args.limit)
    A = sess.A
    rows = []
    for r in o.itertuples():
        run = runs_for(tok, r, "none")
        if run is None:
            continue
        run = run[0]                                            # the correct sentence
        out = A.base(input_ids=run.ids, attention_mask=torch.ones_like(run.ids), output_attentions=True)
        att = torch.stack(out.attentions, 1)                    # (R, L, H, T, T)
        q = att[torch.arange(len(run.ids), device=M.DEVICE), :, :, run.pos]   # (R, L, H, T) from each scored position
        real = run.pclass != 0
        q = q[..., real] / q[..., real].sum(-1, keepdim=True)
        cl = run.pclass[real]
        share = {c: q[..., cl == CLASSES.index(c)].sum(-1).mean(0) for c in ("object", "subject", "ne")}  # (L, H)
        rec = {"order_id": r.order_id, "ref_id": r.ref_id, "clause_head": r.clause_head,
               "object_verb_gap": r.object_verb_gap, "order_class": r.order_class, "is_reference": r.is_reference,
               "object_adjacent": r.object_adjacent}
        for c, v in share.items():
            v = v.cpu().numpy()
            for h in heads:
                rec[f"{c}_{M.cname(h)}"] = float(v[h[1], h[2]])
            rec[f"{c}_all"] = float(v.mean())
        rows.append(rec)
    d = pd.DataFrame(rows)
    f = M.OUT / f"attention_{args.model}.csv"
    d.to_csv(f, index=False)
    log.output(str(f), "per order: attention share from the scored span to object, subject and ne, per head read")
    k = MODEL_INDEX[args.model]
    tab = []
    for h in [M.cname(h) for h in heads] + ["all"]:
        for c in ("object", "subject", "ne"):
            n, eff, p = contrast_test(d, f"{c}_{h}", [707, k])
            tab.append([h, c, float(d[f"{c}_{h}"].mean()), n, eff, p])
    log.table(["head", "to", "mean share", "clauses", "OSV minus SOV", "sign-flip p"], tab, floatfmt="{:.4g}")
    log.note("Descriptive: in an OSV-type order the subject is nearer the verb, so part of any shift toward it is distance.")


def stage_path(args, log, model, tok, sess):
    heads = top_heads(args, 5)
    args.task = "object"
    pairs, skipped = build_pairs(tok, load_items(args, "selection"))
    fc, fx = gaps(sess, pairs)
    keep = np.abs(fc - fx) > args.min_gap
    senders = ["object", "subject", "ne", "all", "random other"]
    res = np.zeros((len(pairs), len(heads), len(senders)))
    rng = np.random.default_rng(707)
    for i, p in enumerate(pairs):
        for ri, (cr, cl) in enumerate(zip(p.corrupt, p.clean)):
            R, T = cr.ids.shape
            act = M.cache(sess, cl, kinds=("k", "v"))
            cls = cr.pclass
            n_obj = int((cls == CLASSES.index("object")).sum())
            other = torch.nonzero(cls == CLASSES.index("other"))[:, 0].cpu().numpy()
            rnd = np.sort(rng.choice(other, size=min(n_obj, len(other)), replace=False)) if len(other) else other
            sets = {"object": torch.nonzero(cls == 3)[:, 0], "subject": torch.nonzero(cls == 4)[:, 0],
                    "ne": torch.nonzero(cls == 5)[:, 0], "all": torch.arange(T, device=M.DEVICE),
                    "random other": torch.tensor(rnd, dtype=torch.long, device=M.DEVICE)}
            for hi, h in enumerate(heads):
                for si, s in enumerate(senders):
                    P = sets[s]
                    if P.numel() == 0:
                        lp, _ = sess.forward(cr.ids, cr.pos, cr.tgt)
                    else:
                        PP = P[None, :].expand(R, -1)
                        rows = torch.arange(R, device=M.DEVICE)
                        c0, c1 = sess._head_cols(h[2])
                        patches = {}
                        for kind in ("k", "v"):
                            val = act[(kind, h[1])][rows[:, None], p.align[ri][PP], c0:c1]
                            patches[(kind, h[1])] = [(rows, PP, h[2], val)]
                        lp, _ = sess.forward(cr.ids, cr.pos, cr.tgt, patches=patches)
                    res[i, hi, si] += float((cr.w * lp).sum())
    f = M.OUT / f"path_{args.model}.npz"
    np.savez_compressed(f, path=res, f_clean=fc, f_corrupt=fx, heads=np.array([M.cname(h) for h in heads]),
                        senders=np.array(senders), ids=np.array([str(p.meta["id"]) for p in pairs]))
    log.output(str(f), "per item x receiver head x sender set: metric with only that head's keys and values patched")
    log.kv("items / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
    log.table(["receiver head"] + [f"through {s}" for s in senders],
              [[M.cname(h)] + [float((res[:, hi, si] - fx)[keep].sum() / (fc - fx)[keep].sum()) for si in range(len(senders))]
               for hi, h in enumerate(heads)])


def stage_validate(args, log, model, tok, sess):
    ex = np.load(M.OUT / f"exact_{args.task}_{args.model}.npz")
    log.kv("exact-stage input", f"exact_{args.task}_{args.model}.npz (sha256 {sha256(M.OUT / f'exact_{args.task}_{args.model}.npz')})")
    names = list(ex["comps"])
    sk = np.abs(ex["f_clean"] - ex["f_corrupt"]) > args.min_gap
    sel_share = (ex["exact"] - ex["f_corrupt"][:, None])[sk].sum(0) / (ex["f_clean"] - ex["f_corrupt"])[sk].sum()
    order = list(np.argsort(-sel_share))
    circuit = tuple(M.cparse(names[j]) for j in order if "MLP" not in names[j])[: args.k]
    top_mlps = [j for j in order if "MLP" in names[j]][: args.k_mlp]
    comps = sess.A.components()
    rand, rstats = M.matched_random_sets(comps, circuit, args.n_random, seed=707)
    log.kv("half read", args.half or "heldout")
    log.kv("random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched",
           f"{rstats['distinct']} of {args.n_random} / {rstats['replacements']} / {rstats['layer-unmatched']} / {rstats['type-unmatched']}")
    log.kv("circuit (the top K heads of the exact stage, selection half)", ", ".join(M.cname(c) for c in circuit))
    pairs, skipped = build_pairs(tok, load_items(args, "heldout"))
    fc, fx = gaps(sess, pairs)
    keep = np.abs(fc - fx) > args.min_gap
    docs = np.array([p.meta["doc"] for p in pairs])
    allpos = lambda p: (lambda ri: torch.arange(p.corrupt[ri].ids.shape[1], device=M.DEVICE))
    sets = [circuit] + rand
    faith = np.zeros((len(pairs), len(sets)))
    for i, p in enumerate(pairs):
        faith[i] = M.exact(sess, p, sets, allpos(p), args.max_rows)
    est, held = M.heldout_sentences(args.sentences, args.n_mean, args.n_read)
    means, cnt = M.estimate_means(sess, tok, est)
    log.kv("mean-estimation positions: special / masked / other", " / ".join(f"{int(x):,}" for x in cnt))
    # necessity. object task: the clean margin lost when the set is ablated in the clean run. contrast task: the
    # attraction gap lost when the set is ablated in both orders, 1 - (ablated gap) / (gap)
    nec_c = np.zeros((len(pairs), len(sets)))
    nec_x = np.zeros((len(pairs), len(sets)))
    for i, p in enumerate(pairs):
        nec_c[i] = M.ablated_metric(sess, p.clean, sets, means, args.max_rows)
        if args.task == "contrast":
            nec_x[i] = M.ablated_metric(sess, p.corrupt, sets, means, args.max_rows)
    gap = fc - fx
    lost = (fc[:, None] - nec_c) if args.task == "object" else (gap[:, None] - (nec_c - nec_x))
    f_share = (faith - fx[:, None])[keep].sum(0) / gap[keep].sum()
    n_share = lost[keep].sum(0) / gap[keep].sum()
    # MLPs: replication of each top MLP's own share on the held-out half (too few MLPs for random-set controls)
    mlp_c = [M.cparse(names[j]) for j in top_mlps]
    rep = np.zeros((len(pairs), len(mlp_c)))
    for i, p in enumerate(pairs):
        rep[i] = M.exact(sess, p, mlp_c, allpos(p), args.max_rows) if mlp_c else []
    r0 = M.readability(sess, tok, held)
    rc = M.readability(sess, tok, held, circuit, means)
    rr = [M.readability(sess, tok, held, s, means) for s in rand[:10]]
    f = M.OUT / f"validate_{args.task}_{args.model}.npz"
    np.savez_compressed(f, faith=faith, nec_clean=nec_c, nec_corrupt=nec_x, f_clean=fc, f_corrupt=fx, docs=docs,
                        sets=np.array(["|".join(M.cname(c) for c in s) for s in sets]), mlp_heldout=rep,
                        mlp_names=np.array([M.cname(c) for c in mlp_c]), mlp_sel_share=sel_share[top_mlps])
    log.output(str(f), "held-out half: metric with each set patched (faithfulness) and ablated (necessity); set 0 is the circuit")
    log.kv("items / skipped / with a gap above --min-gap", f"{len(pairs)} / {skipped} / {int(keep.sum())}")
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
              [[M.cname(c), float(sel_share[top_mlps[n]]), float((rep[:, n] - fx)[keep].sum() / gap[keep].sum()),
                "[%.3f, %.3f]" % M.doc_bootstrap_ratio((rep[:, n] - fx)[keep], gap[keep], docs[keep])]
               for n, c in enumerate(mlp_c)])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", required=True, choices=["metric", "screen", "exact", "attention", "path", "validate"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--task", default="object", choices=["object", "contrast"])
    ap.add_argument("--limit", type=int, default=None, help="first N items only (smoke tests)")
    ap.add_argument("--half", default=None, choices=["selection", "heldout"],
                    help="override the half a stage reads (smoke tests: selection, so the held-out half stays unread)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--chunk", type=int, default=16, help="rows per backward pass in the screen")
    ap.add_argument("--max-rows", type=int, default=256, help="rows per forward in exact patching")
    ap.add_argument("--batch-size", type=int, default=None)
    ap.add_argument("--k", type=int, default=10, help="heads in the validated circuit (declared: 10)")
    ap.add_argument("--k-mlp", type=int, default=5, help="top MLPs whose shares are replicated on the held-out half")
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--n-mean", type=int, default=300, help="held-out sentences for the ablation means")
    ap.add_argument("--n-read", type=int, default=100, help="held-out sentences for the language-modelling check")
    ap.add_argument("--sentences", default=str(M.ROOT / "data" / "heldout_text" / "readability_sentences.txt"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    args.batch_size = args.batch_size or M.MODELS[args.model][1]
    M.OUT.mkdir(parents=True, exist_ok=True)
    task = "" if args.stage in ("metric", "attention", "path") else f"_{args.task}"
    tag = args.record_tag or f"mi_{args.stage}{task}_{args.model}"
    # refusals that depend on the arguments alone come before the record is opened, so a refused run never
    # overwrites the record of a real one with a FAILED one
    if args.half == "heldout" and args.stage != "validate":
        raise SystemExit("only the validate stage reads the held-out half")
    if args.stage == "validate" and args.half == "selection" and not args.limit:
        raise SystemExit("a full validate run reads the held-out half; --half selection is for smoke tests (--limit)")
    if args.task == "contrast" and args.model != "muril" and args.stage in ("exact", "validate"):
        raise SystemExit("XLM-R-large shows no attraction to recover (baseline p 0.58): the contrast task is screened only")
    metric_status = require_metric(args) if args.stage != "metric" else None
    if args.task == "contrast" and args.stage in ("exact", "validate", "screen") and (M.OUT / "contrast_task.dropped").exists():
        raise SystemExit("the contrast task was dropped (contrast_task.dropped): see REMAINING_EXPERIMENTS.md")
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    with RunLog(tag, __file__, args, purpose=f"Step 4 agreement, stage {args.stage}{task.replace('_', ', task ')}, {args.model}.") as log:
        if metric_status:
            log.kv("metric", metric_status)
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            lay = M.check_head_layout(sess, tok, read_positions().correct.iloc[0])
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            {"metric": stage_metric, "screen": stage_screen, "exact": stage_exact, "attention": stage_attention,
             "path": stage_path, "validate": stage_validate}[args.stage](args, log, model, tok, sess)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
