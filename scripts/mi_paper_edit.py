#!/usr/bin/env python3
"""Paper experiments P1, P2 and P6 (docs/PAPER_EXPERIMENTS.md): edits of agreement orders (ko insertion, role swap)
and the word-order marker control matched in kind. GPU, per model (--model muril | xlmrlarge). Declared before any
run (18 Nov 2026); the design below is copied from the design document, and this file changes no prediction or rule.
Items come from mi_items_paper.py (outputs/items_paper/: agreement_ko.csv, agreement_swap.csv, wordorder_kind.csv).

THE CIRCUIT IS FROZEN. Every stage takes its components from step 4's selection-half results (outputs/exact_*), never
from what it reads: the top 10 heads (and, word order, the top 5 MLPs) of the exact stage, as mi_followup.frozen_object
and mi_followup.frozen_wordorder. Nothing here chooses a component. FRESH DATA ONLY: agreement orders of the documents
outside the contrast pairs (no half), word-order pairs of the 'fresh' pool. Neither half step 4 read is touched.
STATISTICS: document-level sign-flip permutation tests (10,000, seed 707), one-sided only where a direction is declared;
document-bootstrap 95% intervals are descriptive; faithfulness is a ratio of sums over items whose gap exceeds
--min-gap (0.05 bits). Pseudo-log-likelihood is not true surprisal: every margin and gap here is a pseudo-log-
likelihood quantity.

SIGN CONVENTIONS (agreement stages). A.object_pair scores the version's 'correct' sentence against its 'foil'
sentence: M_<v> = log2 P(correct agreeing words) - log2 P(foil agreeing words), in bits, the margin toward the
version's own correct form. For versions none, bhi and orig the correct form is the object-agreeing one. For the ko
version the correct form is the DEFAULT form (masculine singular) and the foil the object-agreeing form, so M_ko is
the margin toward the default form, D_ko = M_ko, and the margin toward the object-agreeing form under ko is
Magree_ko = -M_ko. The CSV carries both: M_<v> (toward the version's correct form) and Magree_<v> (toward the
object-agreeing form; equal to M_<v> except under ko). For the swap version the correct form is the one that agrees
with the swapped sentence's bare noun (the ex-subject, now in the object slot): M_swap is toward that form, so
M_swap > 0 means the verb follows the bare noun. Mobj_<v> is the margin with the object slot's words masked, with the
same sign as M_<v>. The gap is M_<v> - Mobj_<v>; faithfulness is the share of that gap restored by patching the 10
heads jointly from the clean run into the object-masked run (an invariant of a common sign flip).

STAGE ko  (P1). QUESTION: does the circuit respect the boundary of the case rule? In the past tense the verb agrees
  with the first argument that carries no case marker; if the object is marked with ko, no argument is eligible and
  the verb takes the default form. Per fresh order whose subject is masculine singular and whose object phrase is
  one contiguous run, three versions: none (as written), ko (को inserted after the object phrase), bhi (भी inserted
  at the same place; the control: a closed-class particle after the same noun phrase that does not block agreement
  with a bare object). Accounts: case (the bare noun controls) predicts the default form preferred under ko;
  exclusion (any noun not marked ne), plausibility and position predict the object-agreeing form preferred under ko.
  Per order and version: M, the object-masked margin, the faithfulness of the 10 heads, and the share of the verb's
  attention (from the scored span positions, renormalised over real subtokens) that the top 5 heads put on the
  object's words (att5 in the CSV: the mean over the five heads). The attention is read on the sentence with the object-agreeing
  verb form in every version (the foil run under ko, the correct run elsewhere), so that versions differ only by the
  inserted word; the first span row masks the whole span and is identical for both forms.
  PRIMARY AND DECLARED READING (behaviour). (1) CONTROL first: mean M_bhi > 0 with one-sided document sign-flip
  p < 0.05; if not, the record says UNINTERPRETABLE. (2) If the control holds: 'respected' if mean D_ko > 0 with
  one-sided p < 0.05; 'partly respected' if D_ko <= 0 or not significant but mean(M_bhi - Magree_ko) > 0 with
  one-sided p < 0.05; 'not respected' otherwise. Case predicts 'respected'; exclusion, plausibility and position
  predict 'not respected'. PRIMARY (component): the top 5 heads' attention to the object, bhi minus ko, one-sided
  document sign-flip p; the heads GATE ON THE MARKER if p < 0.05 and the fall under ko (bhi minus ko) exceeds the fall
  under bhi (none minus bhi); they do not gate otherwise. WHAT A FAILURE MEANS: if behaviour respects the rule but
  the heads' attention does not fall, the heads carry the object's features without deciding eligibility and
  another component gates (reported, not explained); if behaviour ignores the rule, the models follow a simpler
  heuristic than the grammar and step 4's circuit implements that heuristic. LIMIT: ko on an inanimate object can
  sound marked; bhi matches the insertion, not the markedness.

STAGE role_swap  (P2). QUESTION: does agreement follow case or lexical plausibility? Per fresh order whose subject
  span (without ne) and object span are each contiguous, two versions: orig and swap (the two phrases exchange
  places, ne and every other word stay, positions renumbered; the correct form is the old foil). Per order: M_orig,
  M_swap by order class (SOV-type, OSV-type); the top 5 heads' attention from the verb to the bare noun's slot (the
  version's obj_words) and to the ne-marked noun's slot (the version's subj_words; ne's own share is stored too);
  faithfulness of the 10 heads on both versions. After the swap, in SOV-type orders the bare noun is next to the
  verb; in OSV-type orders the ne-marked noun is. Predictions for M_swap (SOV, OSV): case or structure (> 0, > 0),
  lexical plausibility (< 0, < 0), position (> 0, < 0). DECLARED READING: per order class, mean M_swap with a
  two-sided document sign-flip p. FOLLOWS CASE if M_swap > 0 with p < 0.05 in both classes; FOLLOWS PLAUSIBILITY if
  < 0 with p < 0.05 in both; FOLLOWS POSITION if > 0 in SOV-type and < 0 in OSV-type, both p < 0.05; MIXED
  otherwise. The size of M_swap relative to M_orig is descriptive. COMPONENT READING: the heads FOLLOW THE SLOT if the
  top 5 heads' attention is higher on the bare noun's slot than on the ne-marked noun's slot in both classes (paired
  difference per order in the swap version, one-sided document sign-flip p < 0.05 in each). The 10 heads' faithfulness
  on swap is SAME if within 0.10 of its value on orig (the same orders), LOWER if more than 0.10 below (HIGHER if more
  than 0.10 above). Descriptive: mean M_swap by whether the two phrases have equal length. WHAT A FAILURE MEANS: if
  behaviour follows case but faithfulness drops, another route also carries the judgement (the circuit is incomplete);
  if behaviour follows plausibility or position, step 4's circuit reads the object because objects look like objects
  or sit near the verb, and the agreement claim shrinks accordingly.

STAGE kind  (P6). QUESTION: is the word-order gap read through the moved phrases' markers or through postpositions
  in general? Fresh pairs with at least one moved_psp word and at least as many unmoved words of the closed list
  {ने, को, से, में, पर, का, की, के, तक} as moved markers (wordorder_kind.csv, kind_ok). Versions none (as step 2,
  mi_wordorder.build), psp (every marker of a moved phrase deleted, as follow-up 2) and ctlk (the same number of
  unmoved listed words deleted, random, from both sentences). Pattern of mi_followup.stage_case_wordorder: per
  version the gap, the 10 heads' effect and the 5 MLPs' joint effect (descriptive). PRIMARY: the gap kept under ctlk
  minus under psp, paired per pair, one-sided document sign-flip p. DECISION: 'supported' if p < 0.05 and the gap
  retained under psp is lower than under ctlk; 'inconclusive' if fewer than 100 pairs enter and p >= 0.05;
  'not supported' otherwise. WHAT A FAILURE MEANS: a supported result says moved markers matter more than other
  postpositions; not supported (with enough pairs) says word order is not read through the moved phrases' markers,
  in line with follow-up 2.

ADDENDA (18 Nov, written before any full run; they change item counts and descriptive reports, no primary rule).
FIRST ADDENDUM. (1) Faithfulness of the 10 heads is reported for a version only if that version's mean gap (over the orders
  of the table, or over the orders compared) is at least 1.0 bit; below that the record says NOT ESTIMABLE and no verdict
  is drawn. P2: swap against orig is computed on the orders above the gap floor in both versions (the count is printed):
  'same' within 0.10, 'lower' more than 0.10 below, 'higher' more than 0.10 above, 'not estimable'. (2) P2 heads: 'follow
  the slot' needs attention higher on the bare noun's slot in both classes; higher on the bare noun's slot in SOV-type and
  on the ne-marked noun's slot in OSV-type (both one-sided p < 0.05) is 'follow position'; else 'do not follow the slot'.
  (3) P1 head gating cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic
  role in the model's eyes'. (4) The P1 behaviour reading uses the mean; the share of orders preferring each form is
  printed beside it. (5) P1 attention is read on the object-agreeing verb form in every version.
SECOND ADDENDUM. P1: orders whose object ends in, or is followed by, a particle of {भी, ही, तक, को, से, में, पर, का, की,
  के} and orders whose foil agreeing words are not default forms are skipped (mi_items_paper.py). Every table and DECISION
  is printed over all orders, for the feminine singular object stratum and for the plural object stratum (ko after a
  plural object is ungrammatical); the P1 verdict is the reading over all orders, replaced by the feminine singular
  stratum's if the stratum's reading differs from the overall one or from the plural stratum's (the two phrasings of
  the rule are combined; this is the implementation's reading). Descriptive: D_ko beside -Mobj_none (the default form's own
  prior), paired per order; the top 5 heads' attention on the inserted word beside the object; subtoken counts of को and
  भी; clauses and distinct object heads entering; the head-gating verdict reads 'not read (control failed)' when the
  control failed. P2: the class verdicts are also read within the stratum where the swap-correct form is not the default
  form (subject not masculine singular); if its verdict differs from the overall one the stratum's is the verdict, and
  both are reported. Descriptive: M_swap by that stratum, by equal length, by the number of words in the longer phrase.
  In SOV-type orders the swap yields a canonical order and in OSV-type a non-canonical one, so the class split also
  separates canonical from non-canonical order. P6: the primary test (ctlk, distant listed postpositions) is as declared;
  a secondary control ctls (for each moved marker an unmoved word of the same string nearest to a moved head word, not
  already drawn; the pair enters only if every marker has one) is a fourth version with the same rule; the verdict
  quoted is the secondary's if it has at least 60 pairs and the primary's otherwise, and both are reported. The item
  record holds the distance and composition tables; the headline numbers are repeated here.

CHECKS (every stage, the project's pattern): the head layout; the unedited runs reproduce step 4's margins
(outputs/metric_<model>.csv, M_none and M_obj, 1e-3 bits) for ko 'none' and role_swap 'orig', and step 2's scores for
kind 'none'; patching the embedding output at every position recovers the clean margin or gap on the first five
items of every version built; every version holds the same items in the same order.
"""
import argparse
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
from runlog import RunLog  # noqa: E402

PAPER = Path(M.os.environ.get("MI_ITEMS_PAPER", M.ROOT / "course_runs" / "outputs" / "items_paper"))
FLOOR_MEAN_GAP = 1.0   # bits: faithfulness is reported for a version only if its mean gap is at least this (first addendum)
FIELDS = ["correct", "foil", "agree_words", "verb_words", "obj_words", "subj_words", "ne_word"]
LISTS = {c: str for c in ("correct", "foil", "agree_words", "verb_words", "obj_words", "subj_words")}


# ----------------------------------------------------------------------------------------------- items

def read_items(name, versions):
    d = pd.read_csv(PAPER / name, dtype=str)
    if len(d) == 0:
        raise SystemExit(f"{name} is empty")
    for c in ("is_reference", "object_adjacent", "equal_len", "swapcorrect_default", "origcorrect_default"):
        if c in d:
            d[c] = d[c] == "True"
    for c in ("len_subj", "len_obj", "clause_head"):
        if c in d:
            d[c] = d[c].astype(int)
    for v in versions:
        d[f"{v}_ne_word"] = d[f"{v}_ne_word"].astype(int)
    return d


def thin(d, n):
    """n rows spread evenly over d (smoke tests: the first n rows would sit in a handful of documents)."""
    if n >= len(d):
        return d
    return d.iloc[np.unique(np.linspace(0, len(d) - 1, n).round().astype(int))]


def version_of(row, v):
    """SimpleNamespace with the attributes A.object_pair and A.word_class need, as mi_followup.edit_order."""
    return SimpleNamespace(order_id=row.order_id, doc=row.doc, ref_id=row.ref_id,
                           **{k: getattr(row, f"{v}_{k}") for k in FIELDS})


def att_shares(sess, run, heads, names, words=None):
    """Share of the attention a head pays, from each scored position of the run's rows, to the words of each class in
    `names` (A.CLASSES), renormalised over real subtokens (mi_followup.attention_to_object, for several classes at
    once); mean over rows. `words`: optional list of whitespace word indices whose share is returned under the key
    'words'. Returns {name: (len(heads),)}."""
    with torch.no_grad():
        out = sess.A.base(input_ids=run.ids, attention_mask=torch.ones_like(run.ids), output_attentions=True)
        att = torch.stack(out.attentions, 1)
        q = att[torch.arange(len(run.ids), device=M.DEVICE), :, :, run.pos]
        real = run.pclass != 0
        q = q[..., real] / q[..., real].sum(-1, keepdim=True)
        cl = run.pclass[real]
        res = {}
        for n in names:
            v = q[..., cl == A.CLASSES.index(n)].sum(-1).mean(0).cpu().numpy()
            res[n] = np.array([float(v[h[1], h[2]]) for h in heads])
        if words is not None:
            wo = torch.tensor(run.word_of, device=M.DEVICE)[real]
            v = q[..., torch.isin(wo, torch.tensor(list(words), device=M.DEVICE))].sum(-1).mean(0).cpu().numpy()
            res["words"] = np.array([float(v[h[1], h[2]]) for h in heads])
    return res


def emb_check_agreement(sess, p, fc, args):
    e = M.exact(sess, p, [("emb",)], W.allpos(p), args.max_rows)[0]
    return abs(e - fc)


def pvals(x, docs, one_sided):
    return M.doc_signflip(np.asarray(x, float), docs, one_sided=one_sided)


COPY = ("order_id", "ref_id", "doc", "order_class", "is_reference", "object_adjacent", "object_verb_gap", "subj_gen", "subj_num",
        "obj_gen", "obj_num", "equal_len", "len_subj", "len_obj", "swapcorrect_default", "origcorrect_default", "clause_head",
        "obj_head_word")


def evaluate_orders(args, log, sess, tok, d, versions, heads, att_names, att_run, base_version, tag, inserted=None):
    """For every order of d and every version: margin, object-masked margin, the 10 heads' patch, the top 5 heads'
    attention shares (and, if `inserted` is given, their share on the inserted word of the versions it names). Orders
    where any version fails to build are skipped (all versions hold the same orders)."""
    base = pd.read_csv(M.OUT / f"metric_{args.model}.csv", dtype={"ref_id": str, "order_id": str}).set_index(["ref_id", "order_id"])
    h5 = heads[:5]
    rec, worst, n_check, worst_emb, skipped = [], 0.0, {v: 0 for v in versions}, 0.0, 0
    t0 = time.time()
    for i, row in enumerate(d.itertuples()):
        pairs = {v: A.object_pair(tok, version_of(row, v)) for v in versions}
        if any(p is None for p in pairs.values()):
            skipped += 1
            continue
        r = {c: getattr(row, c) for c in COPY if hasattr(row, c)}
        for v, p in pairs.items():
            fc, fx = M.metric(sess, p.clean), M.metric(sess, p.corrupt)
            hf = M.exact(sess, p, [tuple(heads)], W.allpos(p), args.max_rows)[0]
            r[f"M_{v}"], r[f"Mobj_{v}"], r[f"heads_{v}"] = fc, fx, hf
            sign = -1.0 if (tag == "ko" and v == "ko") else 1.0     # toward the object-agreeing form
            r[f"Magree_{v}"], r[f"Mobjagree_{v}"] = sign * fc, sign * fx
            ins = None
            if inserted is not None and v in inserted:
                ins = [max(int(x) for x in str(getattr(row, f"{v}_obj_words")).split("|")) + 1]
            sh = att_shares(sess, p.clean[att_run(v)], h5, att_names, ins)
            for n in att_names:
                for h, x in zip(h5, sh[n]):
                    r[f"att{n}_{M.cname(h)}_{v}"] = float(x)
                r[f"att{n}5_{v}"] = float(sh[n].mean())
            r[f"attins5_{v}"] = float(sh["words"].mean()) if ins is not None else float("nan")
            if n_check[v] < 5:
                worst_emb = max(worst_emb, emb_check_agreement(sess, p, fc, args))
                n_check[v] += 1
        b = base.loc[(row.ref_id, row.order_id)]
        worst = max(worst, abs(r[f"M_{base_version}"] - b.M_none), abs(r[f"Mobj_{base_version}"] - b.M_obj))
        rec.append(r)
        if (i + 1) % 100 == 0:
            print(f"    {i + 1}/{len(d)}  ({(time.time() - t0) / 60:.1f} min)", flush=True)
    out = pd.DataFrame(rec)
    if len(out) == 0:
        raise SystemExit("no order built in every version")
    mins = (time.time() - t0) / 60
    log.kv(f"check: unedited version ({base_version}) against the metric stage's M_none and M_obj, orders / worst (bits)",
           f"{len(out)} / {worst:.2e}")
    if worst > 1e-3:
        raise SystemExit("the unedited runs do not reproduce step 4's margins")
    log.kv("check: embedding output patched everywhere recovers the clean margin, first five items of every version, worst (bits)",
           f"{worst_emb:.2e}")
    if worst_emb > 5e-3:
        raise SystemExit("patching every position at the embeddings does not recover the clean margin")
    log.kv("orders read / entering (every version built) / skipped", f"{len(d)} / {len(out)} / {skipped}")
    log.kv("timing (loop only): minutes in total / minutes per order (all versions)", f"{mins:.2f} / {mins / max(1, len(d)):.4f}")
    return out


def fs(r, ci=None):
    return "NOT ESTIMABLE (mean gap < 1.0 bit)" if r is None or np.isnan(r) else F.fmt(r, ci)


def share_of(d, v, min_gap, keep_extra=None):
    """Faithfulness of the 10 heads for version v: ratio of sums over the orders whose gap exceeds min_gap (and, if
    given, are in keep_extra). Reported only if the mean gap (over the orders of d, or over keep_extra) is at least
    FLOOR_MEAN_GAP bits, else NaN (NOT ESTIMABLE; first addendum, rule 1). Returns (ratio, interval, gap, orders above the floor)."""
    gap = (d[f"M_{v}"] - d[f"Mobj_{v}"]).to_numpy()
    keep = np.abs(gap) > min_gap
    pool = np.ones(len(gap), bool)
    if keep_extra is not None:
        keep, pool = keep & keep_extra, keep_extra
    mean_gap = float(gap[pool].mean()) if pool.any() else float("nan")
    if keep.sum() < 2 or not mean_gap >= FLOOR_MEAN_GAP:
        return float("nan"), None, gap, int(keep.sum())
    r, ci = F.share(d[f"heads_{v}"].to_numpy(), d[f"Mobj_{v}"].to_numpy(), gap, keep, d.doc.to_numpy())
    return r, ci, gap, int(keep.sum())


# ----------------------------------------------------------------------------------------------- P1

def ko_report(args, log, d, label, versions, h5):
    """All P1 tables and DECISION lines for the orders d (one stratum). Returns {'beh', 'gate', 'ctl_ok'}."""
    docs = d.doc.to_numpy()
    L = f"[{label}] "
    rows = []
    for v in versions:
        r, ci, gap, nk = share_of(d, v, args.min_gap)
        rows.append([v, len(d), float((d[f"Magree_{v}"] > 0).mean()), float(d[f"Magree_{v}"].mean()), float(d[f"M_{v}"].mean()),
                     float(d[f"Mobj_{v}"].mean()), float(gap.mean()), nk, fs(r, ci), float(d[f"attobject5_{v}"].mean())])
    log.h2(L + "Per version")
    log.table(["version", "orders", "object-agreeing form preferred (Magree > 0)", "mean Magree (bits)",
               "mean M, toward the version's correct form", "mean Mobj (same sign)", "mean gap (bits)", "orders above the gap floor",
               "10 heads: share of the gap restored", "top 5 heads: attention to the object"], rows, floatfmt="{:.4g}")
    r = d[~d.is_reference & ~d.object_adjacent]
    if len(r):
        rrows = []
        for v in versions:
            rr, ci, gap, nk = share_of(r, v, args.min_gap)
            rrows.append([v, len(r), float(r[f"Magree_{v}"].mean()), float(gap.mean()), nk, fs(rr, ci), float(r[f"attobject5_{v}"].mean())])
        log.h2(L + "Per version, variant orders with the object not adjacent only (the population the circuit was found on)")
        log.table(["version", "orders", "mean Magree (bits)", "mean gap (bits)", "orders above the gap floor",
                   "10 heads: share", "top 5 heads: attention to the object"], rrows, floatfmt="{:.4g}")
    log.h2(L + "Attention to the object by head and version (mean share of the verb's attention)")
    log.table(["head"] + list(versions), [[M.cname(h)] + [float(d[f"attobject_{M.cname(h)}_{v}"].mean()) for v in versions] for h in h5],
              floatfmt="{:.4g}")
    log.kv(L + "clauses / distinct object head words / documents entering",
           f"{len(set(zip(d.ref_id, d.clause_head)))} / {d.obj_head_word.nunique()} / {d.doc.nunique()}")
    # behaviour
    mb, mk = d.M_bhi.to_numpy(), d.M_ko.to_numpy()          # M_bhi toward object-agreeing; M_ko = D_ko toward default
    p_ctl = pvals(mb, docs, True)
    ctl_ok = bool(mb.mean() > 0 and p_ctl < 0.05)
    p_d = pvals(mk, docs, True)
    drop = mb + mk                                          # M_bhi - Magree_ko
    p_drop = pvals(drop, docs, True)
    lo_b, hi_b = F.boot_mean(mb, docs)
    lo_k, hi_k = F.boot_mean(mk, docs)
    lo_d, hi_d = F.boot_mean(drop, docs)
    log.h2(L + "Primary (behaviour): control, then the rule")
    log.table(["quantity", "mean (bits)", "document bootstrap 95%", "one-sided document sign-flip p"],
              [["control: M_bhi (object-agreeing form under bhi)", float(mb.mean()), f"[{lo_b:.3f}, {hi_b:.3f}]", p_ctl],
               ["D_ko = M_ko (default form under ko)", float(mk.mean()), f"[{lo_k:.3f}, {hi_k:.3f}]", p_d],
               ["M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi)", float(drop.mean()),
                f"[{lo_d:.3f}, {hi_d:.3f}]", p_drop],
               ["descriptive: M_bhi - M_none", float((d.M_bhi - d.M_none).mean()), "-", float("nan")]], floatfmt="{:.4g}")
    log.kv(L + "share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)",
           f"{float((mk > 0).mean()):.3f} / {float((mk < 0).mean()):.3f}")
    log.kv(L + "DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)",
           "control holds" if ctl_ok else "UNINTERPRETABLE")
    if not ctl_ok:
        beh = "UNINTERPRETABLE (the control failed)"
    elif mk.mean() > 0 and p_d < 0.05:
        beh = "respected"
    elif drop.mean() > 0 and p_drop < 0.05:
        beh = "partly respected"
    else:
        beh = "not respected"
    log.kv(L + "DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing "
           "preference falls more under ko than under bhi, p < 0.05; else not respected)", beh)
    # descriptive: the default form's own prior (the object-masked margin toward the default form is -Mobj_none)
    prior = -d.Mobj_none.to_numpy()
    dd = mk - prior
    lo_p, hi_p = F.boot_mean(prior, docs)
    lo_dd, hi_dd = F.boot_mean(dd, docs)
    log.h2(L + "Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order")
    log.table(["quantity", "mean (bits)", "document bootstrap 95%"],
              [["D_ko (margin toward the default form, object present, ko inserted)", float(mk.mean()), f"[{lo_k:.3f}, {hi_k:.3f}]"],
               ["-Mobj_none (margin toward the default form, object masked, no insertion)", float(prior.mean()), f"[{lo_p:.3f}, {hi_p:.3f}]"],
               ["D_ko minus -Mobj_none (paired)", float(dd.mean()), f"[{lo_dd:.3f}, {hi_dd:.3f}]"]], floatfmt="{:.4g}")
    # components
    a_n, a_b, a_k = (d[f"attobject5_{v}"].to_numpy() for v in ("none", "bhi", "ko"))
    dif = a_b - a_k
    p_att = pvals(dif, docs, True)
    lo, hi = F.boot_mean(dif, docs)
    fall_ko, fall_bhi = float(dif.mean()), float((a_n - a_b).mean())
    log.h2(L + "Primary (component): the top 5 heads' attention to the object")
    log.table(["bhi minus ko (fall under ko)", "document bootstrap 95%", "one-sided document sign-flip p", "none minus bhi (fall under bhi)",
               "mean attention: none / bhi / ko"],
              [[fall_ko, f"[{lo:.3f}, {hi:.3f}]", p_att, fall_bhi, f"{a_n.mean():.3f} / {a_b.mean():.3f} / {a_k.mean():.3f}"]],
              floatfmt="{:.4g}")
    log.h2(L + "Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object")
    log.table(["version", "attention on the object", "attention on the inserted word", "object + inserted word"],
              [[v, float(d[f"attobject5_{v}"].mean()), float(d[f"attins5_{v}"].mean()),
                float((d[f"attobject5_{v}"] + d[f"attins5_{v}"]).mean())] for v in ("bhi", "ko")] +
              [["none", float(d.attobject5_none.mean()), "-", "-"]], floatfmt="{:.4g}")
    gate = bool(p_att < 0.05 and fall_ko > fall_bhi)
    if not ctl_ok:
        gv = "not read (control failed)"
    else:
        gv = "gate on the marker" if gate else "do not gate"
    log.kv(L + "DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; "
           "read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' "
           "from 'ko changes the noun's syntactic role in the model's eyes'", gv)
    return {"beh": beh, "gate": gv, "ctl_ok": ctl_ok}


def stage_ko(args, log, sess, tok):
    versions = ("none", "ko", "bhi")
    d0 = read_items("agreement_ko.csv", versions)
    d0["obj_kind"] = [("fem" if (g == "f" and n == "sg") else ("pl" if n == "pl" else "other")) for g, n in zip(d0.obj_gen, d0.obj_num)]
    if args.limit:     # smoke tests: the same number from each object-number stratum, so neither is empty
        d0 = pd.concat([thin(g, max(1, args.limit // 2)) for _, g in d0.groupby("obj_kind")])
    heads, mlps = F.frozen_object(args)
    log.kv("frozen circuit (step 4 selection half, object task): 10 heads", ", ".join(M.cname(c) for c in heads))
    h5 = heads[:5]
    log.p("Signs: M_<v> is the margin toward the version's own correct form (bits). Under ko the correct form is the "
          "DEFAULT form, so M_ko = D_ko, the margin toward the default form; Magree_<v> is the margin toward the "
          "object-agreeing form (equal to M_<v> except Magree_ko = -M_ko). Mobj_<v> is the object-masked margin with the "
          "sign of M_<v>. Attention is read on the sentence with the object-agreeing verb form in every version.")
    log.kv("subtokens of को / भी in this model's tokenizer", " / ".join(
        f"{w}: {len(tok.tokenize(w))} ({' '.join(tok.tokenize(w))})" for w in ("को", "भी")))
    att_run = lambda v: 1 if v == "ko" else 0
    d = evaluate_orders(args, log, sess, tok, d0, versions, heads, ("object",), att_run, "none", "ko", inserted=("ko", "bhi"))
    f = M.OUT / f"ko_{args.model}.csv"
    d.to_csv(f, index=False)
    log.output(str(f), "per fresh order and version (none, ko, bhi): margins (toward the version's correct form and toward "
                       "the object-agreeing form), object-masked margins, the 10 heads' patch, attention to the object and to the inserted word")
    strata = [("all orders", np.ones(len(d), bool)),
              ("feminine singular object", ((d.obj_gen == "f") & (d.obj_num == "sg")).to_numpy()),
              ("plural object", (d.obj_num == "pl").to_numpy())]
    res = {}
    for label, mask in strata:
        x = d[mask]
        if len(x) < 2 or x.doc.nunique() < 2:
            log.kv(f"[{label}] orders entering", f"{len(x)}: too few for a stratum reading")
            res[label] = None
            continue
        res[label] = ko_report(args, log, x, label, versions, h5)
    a, fm, pl = res["all orders"], res["feminine singular object"], res["plural object"]
    if a is None:
        raise SystemExit("too few orders for the reading over all orders")
    log.h2("P1 verdict")
    log.kv("behaviour reading: all orders / feminine singular stratum / plural stratum",
           " / ".join(r["beh"] if r else "not evaluable" for r in (a, fm, pl)))
    log.kv("head-gating reading: all orders / feminine singular stratum / plural stratum",
           " / ".join(r["gate"] if r else "not evaluable" for r in (a, fm, pl)))
    differ = fm is not None and (fm["beh"] != a["beh"] or (pl is not None and fm["beh"] != pl["beh"]))
    src, why = (fm, "the feminine singular stratum's (the readings differ: ko after a plural object is ungrammatical)") if differ else \
        (a, "the reading over all orders (the readings agree)" if fm is not None else
         "the reading over all orders (the feminine singular stratum was not evaluable)")
    log.kv("DECISION (P1 verdict; second addendum: the reading over all orders, replaced by the feminine singular stratum's if the "
           "readings differ)", f"behaviour: {src['beh']}; head gating: {src['gate']}; taken from {why}")


# ----------------------------------------------------------------------------------------------- P2

def swap_verdict(log, x, classes, label):
    """Class table and the behaviour verdict of the declared reading on the orders x. Returns (verdict, results)."""
    res, trows = {}, []
    for c in classes:
        y = x[x.order_class == c]
        if len(y) < 2 or y.doc.nunique() < 2:
            res[c] = None
            trows.append([c, len(y), float("nan"), "-", float("nan"), float("nan")])
            continue
        m = y.M_swap.to_numpy()
        p = pvals(m, y.doc.to_numpy(), False)
        lo, hi = F.boot_mean(m, y.doc.to_numpy())
        res[c] = (m.mean(), p)
        ratio = float(y.M_swap.mean() / y.M_orig.mean()) if y.M_orig.mean() != 0 else float("nan")
        trows.append([c, len(y), float(m.mean()), f"[{lo:.3f}, {hi:.3f}]", p, ratio])
    log.h2(f"[{label}] Primary (behaviour): M_swap by order class (two-sided document sign-flip)")
    log.table(["class", "orders", "mean M_swap (bits)", "document bootstrap 95%", "two-sided document sign-flip p",
               "descriptive: mean M_swap / mean M_orig"], trows, floatfmt="{:.4g}")
    if any(v is None for v in res.values()):
        return "not evaluable (an order class has too few orders)", res
    pos = {c: res[c][0] > 0 and res[c][1] < 0.05 for c in classes}
    neg = {c: res[c][0] < 0 and res[c][1] < 0.05 for c in classes}
    if all(pos.values()):
        verdict = "follows case"
    elif all(neg.values()):
        verdict = "follows plausibility"
    elif pos["SOV"] and neg["OSV"]:
        verdict = "follows position"
    else:
        verdict = "mixed"
    return verdict, res


def slot_reading(log, x, classes, label):
    """The heads' reading of the slot: 'follow the slot' / 'follow position' / 'do not follow the slot'."""
    arows, up, dn = [], [], []
    for c in classes:
        y = x[x.order_class == c]
        if len(y) < 2 or y.doc.nunique() < 2:
            up.append(False)
            dn.append(False)
            arows.append([c, len(y), float("nan"), "-", float("nan"), float("nan")])
            continue
        dif = (y.attobject5_swap - y.attsubject5_swap).to_numpy()
        p_up = pvals(dif, y.doc.to_numpy(), True)
        p_dn = pvals(-dif, y.doc.to_numpy(), True)
        lo, hi = F.boot_mean(dif, y.doc.to_numpy())
        arows.append([c, len(y), float(dif.mean()), f"[{lo:.3f}, {hi:.3f}]", p_up, p_dn])
        up.append(bool(dif.mean() > 0 and p_up < 0.05))
        dn.append(bool(dif.mean() < 0 and p_dn < 0.05))
    log.h2(f"[{label}] Primary (component): the top 5 heads' attention, bare noun's slot minus ne-marked noun's slot, swap version")
    log.table(["class", "orders", "mean difference (bare minus ne-marked slot)", "document bootstrap 95%",
               "one-sided p (bare higher)", "one-sided p (ne-marked higher)"], arows, floatfmt="{:.4g}")
    if all(up):
        return "follow the slot"
    if up[0] and dn[1]:
        return "follow position"
    return "do not follow the slot"


def stage_role_swap(args, log, sess, tok):
    versions = ("orig", "swap")
    d0 = read_items("agreement_swap.csv", versions)
    if args.limit:     # smoke tests: the same number from each order class and default-form stratum, so no group is empty
        d0 = pd.concat([thin(g, max(1, args.limit // 4)) for _, g in d0.groupby(["order_class", "swapcorrect_default"])])
    heads, mlps = F.frozen_object(args)
    log.kv("frozen circuit (step 4 selection half, object task): 10 heads", ", ".join(M.cname(c) for c in heads))
    log.p("Signs: M_<v> is the margin toward the version's correct form. For swap that is the form that agrees with the "
          "swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the verb follows the bare "
          "noun. The bare noun's slot is the version's obj_words, the ne-marked noun's slot its subj_words. Attention is read "
          "on the correct-form run of each version (for the first scored row of a span, which masks the whole span, the two "
          "forms are identical; later rows differ only in multi-subtoken spans).")
    d = evaluate_orders(args, log, sess, tok, d0, versions, heads, ("object", "subject", "ne"), lambda v: 0, "orig", "swap")
    f = M.OUT / f"role_swap_{args.model}.csv"
    d.to_csv(f, index=False)
    log.output(str(f), "per fresh order and version (orig, swap): margins, object-masked margins, the 10 heads' patch, "
                       "attention to the bare noun's slot, the ne-marked noun's slot and ne")
    h5 = heads[:5]
    classes = ["SOV", "OSV"]
    rows = []
    for c in classes + ["all"]:
        x = d if c == "all" else d[d.order_class == c]
        for v in versions:
            r, ci, gap, nk = share_of(x, v, args.min_gap) if len(x) else (float("nan"), None, np.zeros(0), 0)
            rows.append([c, v, len(x), x.doc.nunique(), float(x[f"M_{v}"].mean()) if len(x) else float("nan"),
                         float((x[f"M_{v}"] > 0).mean()) if len(x) else float("nan"),
                         float(gap.mean()) if len(x) else float("nan"), nk, fs(r, ci),
                         float(x[f"attobject5_{v}"].mean()) if len(x) else float("nan"),
                         float(x[f"attsubject5_{v}"].mean()) if len(x) else float("nan"),
                         float(x[f"attne5_{v}"].mean()) if len(x) else float("nan")])
    log.h2("Per order class and version")
    log.table(["class", "version", "orders", "documents", "mean M (bits)", "M > 0", "mean gap (bits)", "orders above the gap floor",
               "10 heads: share of the gap restored", "top 5 heads: attention to the bare noun's slot", "to the ne-marked noun's slot", "to ne"],
              rows, floatfmt="{:.4g}")
    # behaviour: overall, then within the stratum where the swap-correct form is not the default form
    v_all, _ = swap_verdict(log, d, classes, "all orders")
    log.kv("DECISION (behaviour, all orders; declared: follows case if M_swap > 0, p < 0.05 in both classes; plausibility if < 0 in "
           "both; position if > 0 in SOV and < 0 in OSV; else mixed)", v_all)
    st = d[~d.swapcorrect_default]
    log.kv("orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents",
           f"{len(st)} / {st.doc.nunique()}")
    v_st, _ = swap_verdict(log, st, classes, "swap-correct form is not the default form")
    log.kv("DECISION (behaviour, stratum where the swap-correct form is not the default form)", v_st)
    final = v_all if (v_st == v_all or v_st.startswith("not evaluable")) else v_st
    log.kv("DECISION (P2 behaviour verdict; second addendum: the stratum's verdict if it differs from the overall one)",
           f"{final} (all orders: {v_all}; stratum: {v_st})")
    # components
    s_all = slot_reading(log, d, classes, "all orders")
    log.kv("DECISION (heads; declared: follow the slot if attention is higher on the bare noun's slot in both classes, p < 0.05; "
           "follow position if higher on the bare noun's slot in SOV and on the ne-marked noun's slot in OSV, both p < 0.05; "
           "else do not follow the slot)", s_all)
    s_st = slot_reading(log, st, classes, "swap-correct form is not the default form") if len(st) else "not evaluable"
    log.kv("descriptive: heads reading in the stratum where the swap-correct form is not the default form", s_st)
    log.h2("Attention by head and version: bare noun's slot / ne-marked noun's slot (mean share of the verb's attention)")
    log.table(["head"] + [f"{v}: {t}" for v in versions for t in ("bare", "ne-marked")],
              [[M.cname(h)] + [float(d[f"att{n}_{M.cname(h)}_{v}"].mean()) for v in versions for n in ("object", "subject")] for h in h5],
              floatfmt="{:.4g}")
    # faithfulness on the orders above the gap floor in both versions
    both = ((d.M_orig - d.Mobj_orig).abs() > args.min_gap).to_numpy() & ((d.M_swap - d.Mobj_swap).abs() > args.min_gap).to_numpy()
    r0, ci0, _, n0 = share_of(d, "orig", args.min_gap, both)
    r1, ci1, _, n1 = share_of(d, "swap", args.min_gap, both)
    log.h2("The 10 heads' faithfulness, swap against orig (the orders above the gap floor in both versions)")
    mg = [float((d[f"M_{v}"] - d[f"Mobj_{v}"])[both].mean()) if both.any() else float("nan") for v in versions]
    log.table(["orders above the floor in both versions", "mean gap on them: orig / swap (bits)", "orig", "swap", "swap minus orig"],
              [[int(both.sum()), f"{mg[0]:.3f} / {mg[1]:.3f}", fs(r0, ci0), fs(r1, ci1),
                float(r1 - r0) if not (np.isnan(r0) or np.isnan(r1)) else float("nan")]], floatfmt="{:.4g}")
    if np.isnan(r0) or np.isnan(r1):
        fv = "not estimable"
    else:
        fd = r1 - r0
        fv = "same" if abs(fd) <= 0.10 else ("lower" if fd < 0 else "higher")
    log.kv("DECISION (faithfulness, first addendum: same if within 0.10 of orig on the same orders, lower if more than 0.10 below, higher "
           "if more than 0.10 above, not estimable if either version's mean gap on those orders is under 1.0 bit)", fv)
    # descriptive splits
    log.h2("Descriptive: M_swap by the swap-correct form being the default form, by class")
    srows = []
    for b in (False, True):
        for c in classes:
            y = d[(d.swapcorrect_default == b) & (d.order_class == c)]
            srows.append([str(b), c, len(y), y.doc.nunique(), float(y.M_swap.mean()) if len(y) else float("nan"),
                          float((y.M_swap > 0).mean()) if len(y) else float("nan")])
    log.table(["swap-correct form is the default", "class", "orders", "documents", "mean M_swap (bits)", "M_swap > 0"], srows, floatfmt="{:.4g}")
    log.h2("Descriptive: M_swap by whether the two phrases have equal length")
    erows = []
    for e in (True, False):
        x = d[d.equal_len == e]
        erows.append([str(e), len(x), x.doc.nunique(), float(x.M_swap.mean()) if len(x) else float("nan"),
                      float((x.M_swap > 0).mean()) if len(x) else float("nan")])
    log.table(["equal length", "orders", "documents", "mean M_swap (bits)", "M_swap > 0"], erows, floatfmt="{:.4g}")
    longer = np.maximum(d.len_subj.to_numpy(), d.len_obj.to_numpy())
    lrows = []
    for name, lo_, hi_ in (("1", 1, 1), ("2", 2, 2), ("3-4", 3, 4), ("5-8", 5, 8), ("9+", 9, 10 ** 6)):
        mk = (longer >= lo_) & (longer <= hi_)
        y = d[mk]
        lrows.append([name, int(mk.sum()), y.doc.nunique(), float(y.M_swap.mean()) if mk.any() else float("nan"),
                      float((y.M_swap > 0).mean()) if mk.any() else float("nan")])
    log.h2("Descriptive: M_swap by the number of words in the longer phrase")
    log.table(["words in the longer phrase", "orders", "documents", "mean M_swap (bits)", "M_swap > 0"], lrows, floatfmt="{:.4g}")
    log.p("Note: in SOV-type orders the swap yields a canonical order (ne-marked noun first, bare noun next to the verb) and in "
          "OSV-type orders a non-canonical one, so the class split separates canonical from non-canonical order as well as position.")


# ----------------------------------------------------------------------------------------------- P6

def ints_(s):
    return [int(x) for x in str(s).split("|")] if str(s) not in ("", "nan") else []


def stage_kind(args, log, sess, tok):
    kind = pd.read_csv(PAPER / "wordorder_kind.csv", dtype=str)
    kind["kind_ok"], kind["ctls_ok"] = kind.kind_ok == "True", kind.ctls_ok == "True"
    kind = kind[kind.kind_ok | kind.ctls_ok]
    if args.limit:     # smoke tests: pairs of both tests
        kind = pd.concat([thin(kind[kind.kind_ok], args.limit), thin(kind[kind.ctls_ok], args.limit)]).drop_duplicates(["ref_id", "var_id"])
    if len(kind) == 0:
        raise SystemExit("wordorder_kind.csv holds no entering pair")
    pool = F.read_pool()
    need = ["ref_id", "var_id", "ref_text", "var_text", "var_to_ref", "var_site", "ref_text_psp", "var_text_psp",
            "var_to_ref_psp", "var_site_psp", "dropped_psp", "psp_ok"]
    kc = ["ref_id", "var_id", "doc", "kind_ok", "ctls_ok", "dropped_ctlk", "dropped_ctls", "dist_psp", "dist_ctlk", "dist_ctls"] + \
         [f"{a}_{t}" for t in ("ctlk", "ctls") for a in ("ref_text", "var_text", "var_to_ref", "var_site")]
    m = kind[kc].merge(pool[need], on=["ref_id", "var_id"], how="inner", validate="one_to_one")
    if len(m) != len(kind):
        raise SystemExit("a kind pair is not in the pool")
    m = m[m.psp_ok]
    rows = list(m.itertuples())
    step2 = pd.read_csv(W.STEP2 / f"patching_{args.model}.csv").set_index(["ref_id", "var_id"])
    built = {"none": W.build(tok, rows, step2)[0], "psp": F.build_edited(tok, rows, "psp")[0],
             "ctlk": F.build_edited(tok, [r for r in rows if r.kind_ok], "ctlk")[0],
             "ctls": F.build_edited(tok, [r for r in rows if r.ctls_ok], "ctls")[0]}
    doc_of = {p.meta["id"]: p.meta["doc"] for v in built.values() for p in v}
    idl = {k: [p.meta["id"] for p in v] for k, v in built.items()}
    sets_ = {"primary": [i for i in idl["none"] if i in set(idl["psp"]) and i in set(idl["ctlk"])],
             "secondary": [i for i in idl["none"] if i in set(idl["psp"]) and i in set(idl["ctls"])]}
    log.kv("pairs built per version (none / psp / ctlk / ctls)", " / ".join(str(len(idl[k])) for k in built))
    log.kv("pairs entering the primary test (kind_ok, built in none, psp, ctlk) / the secondary test (ctls_ok, built in none, psp, ctls)",
           f"{len(sets_['primary'])} / {len(sets_['secondary'])}")
    heads, mlps = F.frozen_wordorder(args)
    log.kv("frozen circuit (step 4 selection half): 10 heads", ", ".join(M.cname(c) for c in heads))
    log.kv("frozen circuit: top 5 MLPs", ", ".join(M.cname(c) for c in mlps))
    sets = F.circuit_sets(heads, mlps)
    t0 = time.time()
    fc0, fx0 = W.gaps_checked(sess, built["none"], log)
    out = {}
    for cond, pairs in built.items():
        if len(pairs) == 0:
            out[cond] = None
            continue
        if cond == "none":
            fc, fx = fc0, fx0
        else:
            fc = np.array([M.metric(sess, p.clean) for p in pairs])
            fx = np.array([M.metric(sess, p.corrupt) for p in pairs])
        F.embedding_check(sess, pairs, fc, fx, args, log, f"version {cond}")     # raises above 5e-3 on the worst pair
        res = np.zeros((len(pairs), len(sets)))
        for i, p in enumerate(pairs):
            res[i] = M.exact(sess, p, sets, W.allpos(p), args.max_rows)
            if (i + 1) % 50 == 0:
                print(f"    {cond}: {i + 1}/{len(pairs)}", flush=True)
        out[cond] = (fc, fx, res)
    mins = (time.time() - t0) / 60
    log.kv("timing: minutes in total / minutes per pair (all versions)", f"{mins:.2f} / {mins / max(1, len(idl['none'])):.4f}")
    f = M.OUT / f"kind_{args.model}.npz"
    np.savez_compressed(f, set_names=np.array(F.SET_NAMES),
                        **{f"ids_{c}": np.array(idl[c]) for c in built},
                        **{f"docs_{c}": np.array([doc_of[i] for i in idl[c]]) for c in built},
                        **{f"{c}_{k}": v for c, o in out.items() if o is not None
                           for k, v in (("f_clean", o[0]), ("f_corrupt", o[1]), ("res", o[2]))})
    log.output(str(f), "per pair and version (none, psp, ctlk, ctls; each version's own pair list ids_<version>): clean and corrupted metrics, the circuit's patches")
    log.p("Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every "
          "word's weight by n/(n-k): 'retained' is compared between psp and a control (equal counts); its level against the "
          "unedited gap carries that factor.")
    pos = {c: {i: k for k, i in enumerate(idl[c])} for c in built}

    def take(cond, ids):
        ix = [pos[cond][i] for i in ids]
        fc, fx, res = out[cond]
        return fc[ix], fx[ix], res[ix]

    def test(name, ctl, ids):
        if len(ids) < 2:
            log.kv(f"{name}: pairs entering", f"{len(ids)}: no test")
            return "inconclusive", len(ids)
        docs = np.array([doc_of[i] for i in ids])
        v = {c: take(c, ids) for c in ("none", "psp", ctl)}
        base_gap = (v["none"][0] - v["none"][1]).sum()
        rws = []
        for cond, (fc, fx, res) in v.items():
            gap = fc - fx
            keep = np.abs(gap) > args.min_gap
            eff = [(res[:, j] - fx) for j in (0, 6)]
            rws.append([cond, len(gap), float(gap.mean()), float(gap.sum() / base_gap), float(eff[0].mean()),
                        F.fmt(*F.share(res[:, 0], fx, gap, keep, docs)), float(eff[1].mean()), F.fmt(*F.share(res[:, 6], fx, gap, keep, docs))])
        log.h2(f"{name}: per version")
        log.table(["version", "pairs", "mean gap (bits)", "gap retained (share of the unedited gap)", "10 heads: mean effect (bits)",
                   "10 heads: share of that version's gap", "5 MLPs jointly: mean effect (bits)", "5 MLPs jointly: share of that version's gap"],
                  rws, floatfmt="{:.4g}")
        gp, gc = (v[c][0] - v[c][1] for c in ("psp", ctl))
        dd = gc - gp
        p1 = M.doc_signflip(dd, docs, one_sided=True)
        lo, hi = F.boot_mean(dd, docs)
        log.h2(f"{name}: gap kept after deleting the control words ({ctl}) minus gap kept after deleting the moved markers (paired per pair)")
        log.table(["mean difference (bits)", "document bootstrap 95%", "one-sided document sign-flip p", f"retained psp / {ctl}"],
                  [[float(dd.mean()), f"[{lo:.3f}, {hi:.3f}]", p1, f"{gp.sum() / base_gap:.3f} / {gc.sum() / base_gap:.3f}"]], floatfmt="{:.4g}")
        if p1 < 0.05 and gp.sum() < gc.sum():
            dec = "supported"
        elif len(ids) < 100 and p1 >= 0.05:
            dec = "inconclusive"
        else:
            dec = "not supported"
        log.kv(f"DECISION ({name}; declared: supported if p < 0.05 and the gap retained under psp is lower than under {ctl}; inconclusive "
               f"if fewer than 100 pairs enter and p >= 0.05; not supported otherwise; pairs entering: {len(ids)}). 'Supported' reads: "
               + ("deleting the moved phrases' markers costs more than deleting as many distant listed postpositions"
                  if ctl == "ctlk" else "deleting the moved phrases' markers costs more than deleting as many unmoved words of the same "
                  "strings nearest to a moved head"), dec)
        for lab, j in (("5 MLPs' joint effect", 6), ("10 heads' effect", 0)):
            dm = (v[ctl][2][:, j] - v[ctl][1]) - (v["psp"][2][:, j] - v["psp"][1])
            lo, hi = F.boot_mean(dm, docs)
            log.kv(f"{name}: descriptive: the {lab} (bits), {ctl} minus psp, mean and document bootstrap 95%", f"{dm.mean():.3f} [{lo:.3f}, {hi:.3f}]")
        return dec, len(ids)

    dec_p, n_p = test("Primary (ctlk)", "ctlk", sets_["primary"])
    dec_s, n_s = test("Secondary (ctls)", "ctls", sets_["secondary"])
    quoted = dec_s if n_s >= 60 else dec_p
    log.kv("DECISION (P6 quoted verdict; second addendum: the secondary test's if it has at least 60 pairs, else the primary's; the paper "
           "states both)", f"{quoted} (primary ctlk: {dec_p}, {n_p} pairs; secondary ctls: {dec_s}, {n_s} pairs; quoted from "
           f"the {'secondary' if n_s >= 60 else 'primary'})")
    # headline numbers of the item record, for the pairs entering each test
    k = m.set_index(["ref_id", "var_id"])
    for name, col, ids in (("primary", "dropped_ctlk", sets_["primary"]), ("secondary", "dropped_ctls", sets_["secondary"])):
        sub = k.loc[[tuple(i.split("|")) for i in ids]]
        mw, cw = [], []
        for r in sub.itertuples():
            vw = r.var_text.split(" ")
            mw += [vw[i] for i in ints_(r.dropped_psp)]
            cw += [vw[i] for i in ints_(getattr(r, col))]
        gm, gcn = sum(w in ("का", "की", "के") for w in mw), sum(w in ("का", "की", "के") for w in cw)
        dcol = "dist_ctlk" if name == "primary" else "dist_ctls"
        log.kv(f"item record, {name} test: mean distance to the nearest moved head word (per-pair means): markers / control",
               f"{sub.dist_psp.astype(float).mean():.2f} / {sub[dcol].astype(float).mean():.2f}")
        log.kv(f"item record, {name} test: genitive (का, की, के) share: markers / control",
               f"{gm}/{len(mw)} ({100 * gm / max(1, len(mw)):.0f}%) / {gcn}/{len(cw)} ({100 * gcn / max(1, len(cw)):.0f}%)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", required=True, choices=["ko", "role_swap", "kind"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None, help="N items spread evenly over the file (smoke tests; role_swap takes N/2 per class)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--max-rows", type=int, default=256)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    note = None
    if args.stage in ("ko", "role_swap"):
        note = A.require_metric(SimpleNamespace(model=args.model))
    M.OUT.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"mi_paper_{args.stage}_{args.model}"
    with RunLog(tag, __file__, args, purpose=f"Paper experiments, stage {args.stage}, {args.model}.") as log:
        if note:
            log.kv("metric decision", note)
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            text = pd.read_csv(M.ITEMS / "wordorder_pairs.csv").ref_text.iloc[0]
            lay = M.check_head_layout(sess, tok, text)
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            {"ko": stage_ko, "role_swap": stage_role_swap, "kind": stage_kind}[args.stage](args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
