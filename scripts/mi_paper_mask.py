#!/usr/bin/env python3
"""Paper experiment P7 (docs/PAPER_EXPERIMENTS.md): masked-slot follow-up to the role swap (P2). GPU, per model
(--model muril | xlmrlarge), one stage, swap_mask. Declared 18 Nov 2026 after P2 ran, before any code for P7 and before
any P7 run; the design below is copied from the design document, and this file changes no prediction or rule.

QUESTION. P2 found that after the swap both models prefer the verb form that agrees with the old object, which now sits
in the ne-marked slot, and that the top heads' attention goes to the nearer noun (MuRIL) or to the ne-marked slot
(XLM-R-large). That does not say what the verb reads. P7 masks one thing at a time in the same sentences and reads the
margin.

ITEMS. The 2,132 fresh orders of outputs/items_paper/agreement_swap.csv (mi_items_paper.py) and both versions, orig and
swap, as P2 (the circuit is frozen; no half step 4 read is touched). Per version and order, four conditions built with
mi_agreement.runs_for: none; obj (the bare noun's slot masked, the version's obj_words); subj (the ne-marked noun's slot
masked, the version's subj_words, without ne); ne (the marker ne masked). The margin M_<v>_<cond> is the span margin of
step 4 (mi_lib.metric over the correct run, weight +1, and the foil run, weight -1: log2 P(correct agreeing words) minus
log2 P(foil agreeing words), in bits) toward the version's own correct form; for swap that is the form that agrees with
the swapped sentence's bare noun, as in P2, so M_swap > 0 means the verb agrees with the bare noun. An order is kept only
if all eight runs build (the skipped count is printed).

PREDICTIONS. If the verb reads the ne-marked noun after the swap, masking it removes the pull toward the object-agreeing
form and M_swap rises. If it reads position or a default form, it does not.

DECLARED READING (per order class, SOV and OSV, and in the stratum where the swap-correct form is not the default form,
swapcorrect_default == False, as P2; the stratum's reading is the verdict if it differs from the overall one). Let
R = M_swap(subj) - M_swap(none), paired per order, mean with a one-sided (upward) document sign-flip p (10,000, seed 707)
and a document-bootstrap interval.
  THE VERB READS THE NE-MARKED NOUN: R >= 1.0 bit with p < 0.05 and mean M_swap(subj) > 0, in both order classes.
  PARTLY: R >= 1.0 bit with p < 0.05 but mean M_swap(subj) <= 0 in at least one class.
  NOT: otherwise.
The same contrast for the bare noun's slot, M_swap(obj) - M_swap(none), has the opposite expectation: a fall of at least
1.0 bit with p < 0.05 (one-sided, downward) means the verb also reads the bare noun. Masking ne is reported and not
graded. The same four conditions on orig are the unswapped reference (M_orig(subj), M_orig(obj), M_orig(ne)); M_orig(obj)
reproduces the object-masked margin of step 4 (check, 1e-3 bits).
Implementation readings (the most literal reading of the declaration; stated so the paper reports them): (a) 'in both
order classes' is carried to PARTLY, so PARTLY needs R >= 1.0 bit with p < 0.05 in both classes and mean M_swap(subj) <= 0
in at least one; (b) the bare-noun reading ('also reads the bare noun') is likewise taken as the fall in both classes, and
each class's flag is printed; (c) the stratum's verdict replaces the overall one when the two differ and the stratum is
evaluable (the P2 rule).

DESCRIPTIVE. The 10 frozen heads' faithfulness for the subj corruption on swap (clean none, corrupted subj, the heads of
mi_followup.frozen_object patched jointly, mi_lib.exact), reported only if that condition's mean gap (M_swap(none) minus
M_swap(subj)) is at least 1.0 bit, as the first addendum of P2 (else NOT ESTIMABLE); the share of orders whose preference
changes sign under each mask (and the share that goes from the wrong to the right form).

WHAT A FAILURE MEANS. If masking the ne-marked noun leaves M_swap negative, the swap's pull toward the old object is not
carried by that noun's slot alone (position, the default form or the verb's own cues carry it), and the paper says the
swap result is not localised to a noun. If it flips the margin, the swap result is the ne-marked noun's pull.

LIMIT. Masking is a corruption that may itself change the sentence's acceptability. The swapped sentences are odd in
meaning, so a model's preference after the swap may reflect oddness more than agreement. P7 cannot separate the two.

CHECKS: the head layout; M_orig(none) and M_orig(obj) reproduce step 4's metric_<model>.csv M_none and M_obj (1e-3 bits,
stop on failure, per order); M_orig and M_swap(none) agree with P2's role_swap_<model>.csv where it is present (the signs
match; a stop above 1e-2 bits, the worst is printed); patching the embedding output at every position recovers the clean
margin on the first five orders of the faithfulness pair; both versions hold the same words of every order, apart from the agreeing words.
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
import mi_paper_edit as E  # noqa: E402
import mi_wordorder as W  # noqa: E402
from runlog import RunLog  # noqa: E402

CONDS = ("none", "obj", "subj", "ne")
VERSIONS = ("orig", "swap")
CLASSES = ["SOV", "OSV"]
BIT = 1.0     # declared threshold (bits)


# ----------------------------------------------------------------------------------------------- measurement

def measure(args, log, sess, tok, d, heads):
    """One row per order: the margin of every version under every condition, and the 10 heads' patch for the subj
    corruption on swap. Orders where any of the eight runs fails to build are skipped."""
    base = pd.read_csv(M.OUT / f"metric_{args.model}.csv", dtype={"ref_id": str, "order_id": str}).set_index(["ref_id", "order_id"])
    p2f = M.ROOT / "course_runs" / "outputs" / f"role_swap_{args.model}.csv"
    p2 = pd.read_csv(p2f, dtype={"ref_id": str, "order_id": str}).set_index(["ref_id", "order_id"]) if p2f.exists() else None
    rec, skipped, bad_words = [], 0, 0
    worst_step4, worst_p2, worst_emb, n_emb, n_p2 = 0.0, 0.0, 0.0, 0, 0
    t0 = time.time()
    for i, row in enumerate(d.itertuples()):
        if sorted(w for k, w in enumerate(row.orig_correct.split(" ")) if k not in A.ints(row.orig_agree_words)) != \
                sorted(w for k, w in enumerate(row.swap_correct.split(" ")) if k not in A.ints(row.swap_agree_words)):
            bad_words += 1     # the agreeing words differ by design (the swap-correct form is the old foil)
        runs = {v: {c: A.runs_for(tok, E.version_of(row, v), c) for c in CONDS} for v in VERSIONS}
        if any(r is None for v in runs.values() for r in v.values()):
            skipped += 1
            continue
        r = {c: getattr(row, c) for c in E.COPY if hasattr(row, c)}
        for v in VERSIONS:
            for c in CONDS:
                r[f"M_{v}_{c}"] = M.metric(sess, runs[v][c])
        b = base.loc[(row.ref_id, row.order_id)]
        worst_step4 = max(worst_step4, abs(r["M_orig_none"] - b.M_none), abs(r["M_orig_obj"] - b.M_obj))
        if worst_step4 > 1e-3:
            raise SystemExit(f"the unedited runs do not reproduce step 4's margins (order {row.order_id}: "
                             f"M_none {r['M_orig_none']:.5f} against {b.M_none:.5f}, M_obj {r['M_orig_obj']:.5f} against {b.M_obj:.5f})")
        if p2 is not None and (row.ref_id, row.order_id) in p2.index:
            q = p2.loc[(row.ref_id, row.order_id)]
            worst_p2 = max(worst_p2, abs(r["M_orig_none"] - q.M_orig), abs(r["M_swap_none"] - q.M_swap))
            n_p2 += 1
            if worst_p2 > 1e-2:
                raise SystemExit(f"M_orig / M_swap(none) do not match P2's role_swap file (order {row.order_id})")
        # faithfulness pair: swap version, clean none, corrupted subj
        cl, cr = runs["swap"]["none"], runs["swap"]["subj"]
        p = M.Pair(corrupt=cr, clean=cl, align=[A.ident(x) for x in cr], meta={"id": row.order_id, "doc": row.doc})
        r["heads_swap_subj"] = M.exact(sess, p, [tuple(heads)], W.allpos(p), args.max_rows)[0]
        if n_emb < 5:
            worst_emb = max(worst_emb, E.emb_check_agreement(sess, p, r["M_swap_none"], args))
            n_emb += 1
        rec.append(r)
        if (i + 1) % 100 == 0:
            print(f"    {i + 1}/{len(d)}  ({(time.time() - t0) / 60:.1f} min)", flush=True)
    out = pd.DataFrame(rec)
    if len(out) == 0:
        raise SystemExit("no order built in every version and condition")
    mins = (time.time() - t0) / 60
    log.kv("check: unedited version (orig, none and obj) against the metric stage's M_none and M_obj, orders / worst (bits)",
           f"{len(out)} / {worst_step4:.2e}")
    log.kv("check: orig and swap(none) against P2's role_swap file, orders in common / worst (bits)",
           f"{n_p2} / {worst_p2:.2e}" if p2 is not None else "file not present in this output folder: not run")
    log.kv("check: embedding output patched everywhere recovers the clean margin (swap, none), first five orders, worst (bits)",
           f"{worst_emb:.2e}")
    if worst_emb > 5e-3:
        raise SystemExit("patching every position at the embeddings does not recover the clean margin")
    log.kv("check: orders whose two versions hold different words apart from the agreeing words (must be 0)", str(bad_words))
    if bad_words:
        raise SystemExit("the two versions of an order hold different words")
    log.kv("orders read / entering (all eight runs built) / skipped", f"{len(d)} / {len(out)} / {skipped}")
    log.kv("timing (loop only): minutes in total / minutes per order (all eight conditions and the patch)",
           f"{mins:.2f} / {mins / max(1, len(d)):.4f}")
    return out


# ----------------------------------------------------------------------------------------------- readings

def stratum_reading(log, x, label):
    """The contrasts of the declared reading on the orders x, by order class. Returns (verdict, bare-noun reading)."""
    rows, brows, res = [], [], {}
    for c in CLASSES:
        y = x[x.order_class == c]
        if len(y) < 2 or y.doc.nunique() < 2:
            res[c] = None
            rows.append([c, len(y), float("nan"), float("nan"), "-", float("nan"), float("nan")])
            brows.append([c, len(y), float("nan"), "-", float("nan")])
            continue
        docs = y.doc.to_numpy()
        R = (y.M_swap_subj - y.M_swap_none).to_numpy()
        Rb = (y.M_swap_obj - y.M_swap_none).to_numpy()
        pR, pRb = E.pvals(R, docs, True), E.pvals(-Rb, docs, True)
        lo, hi = F.boot_mean(R, docs)
        lob, hib = F.boot_mean(Rb, docs)
        res[c] = {"R": float(R.mean()), "p": pR, "msubj": float(y.M_swap_subj.mean()),
                  "Rb": float(Rb.mean()), "pb": pRb}
        rows.append([c, len(y), float(y.M_swap_none.mean()), float(R.mean()), f"[{lo:.3f}, {hi:.3f}]", pR, float(y.M_swap_subj.mean())])
        brows.append([c, len(y), float(Rb.mean()), f"[{lob:.3f}, {hib:.3f}]", pRb])
    log.h2(f"[{label}] Primary: R = M_swap(subj) - M_swap(none), paired per order (one-sided document sign-flip, upward)")
    log.table(["class", "orders", "mean M_swap(none) (bits)", "mean R (bits)", "document bootstrap 95%",
               "one-sided p (R > 0)", "mean M_swap(subj) (bits)"], rows, floatfmt="{:.4g}")
    log.h2(f"[{label}] Bare noun's slot: M_swap(obj) - M_swap(none), paired per order (one-sided document sign-flip, downward)")
    log.table(["class", "orders", "mean change (bits)", "document bootstrap 95%", "one-sided p (fall)"], brows, floatfmt="{:.4g}")
    if any(v is None for v in res.values()):
        return "not evaluable (an order class has too few orders)", "not evaluable"
    rok = {c: res[c]["R"] >= BIT and res[c]["p"] < 0.05 for c in CLASSES}
    if all(rok.values()):
        verdict = "the verb reads the ne-marked noun" if all(res[c]["msubj"] > 0 for c in CLASSES) else "partly"
    else:
        verdict = "not"
    bflag = {c: res[c]["Rb"] <= -BIT and res[c]["pb"] < 0.05 for c in CLASSES}
    bare = "also reads the bare noun" if all(bflag.values()) else "does not (in both classes) also read the bare noun"
    log.kv(f"[{label}] flags per class: R >= 1.0 bit with p < 0.05 / mean M_swap(subj) > 0 / bare-noun fall >= 1.0 bit with p < 0.05",
           "; ".join(f"{c}: {rok[c]} / {res[c]['msubj'] > 0} / {bflag[c]}" for c in CLASSES))
    return verdict, bare


def stage_swap_mask(args, log, sess, tok):
    d0 = E.read_items("agreement_swap.csv", VERSIONS)
    if args.limit:     # smoke tests: the same number from each order class and default-form stratum, so no group is empty
        d0 = pd.concat([E.thin(g, max(1, args.limit // 4)) for _, g in d0.groupby(["order_class", "swapcorrect_default"])])
    heads, mlps = F.frozen_object(args)
    log.kv("frozen circuit (step 4 selection half, object task): 10 heads", ", ".join(M.cname(c) for c in heads))
    log.p("Signs: M_<version>_<cond> is the span margin toward the version's own correct form (bits). For swap that is the "
          "form that agrees with the swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the "
          "verb follows the bare noun. Conditions: none; obj (the bare noun's slot masked, the version's obj_words); subj "
          "(the ne-marked noun's slot masked, its subj_words, without ne); ne (the marker masked).")
    d = measure(args, log, sess, tok, d0, heads)
    f = M.OUT / f"swap_mask_{args.model}.csv"
    d.to_csv(f, index=False)
    log.output(str(f), "per fresh order (one row; both versions orig and swap): the span margin M_<version>_<cond> for every "
                       "condition (none, obj, subj, ne), and the 10 heads' patch for the swap subj corruption")

    # tables of M by class, version and condition
    st = d[~d.swapcorrect_default]
    groups = [("all orders", d), ("swap-correct form is not the default form", st)]
    log.kv("orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents",
           f"{len(st)} / {st.doc.nunique()}")
    for label, x in groups:
        rows = []
        for c in CLASSES + ["all"]:
            y = x if c == "all" else x[x.order_class == c]
            for v in VERSIONS:
                rows.append([c, v, len(y), y.doc.nunique()] +
                            [float(y[f"M_{v}_{k}"].mean()) if len(y) else float("nan") for k in CONDS] +
                            [float((y[f"M_{v}_{k}"] > 0).mean()) if len(y) else float("nan") for k in CONDS])
        log.h2(f"[{label}] Mean margin M (bits) and share of orders with M > 0, by class, version and condition")
        log.table(["class", "version", "orders", "documents"] + [f"M {k}" for k in CONDS] + [f"M>0 {k}" for k in CONDS],
                  rows, floatfmt="{:.4g}")

    # declared reading
    v_all, b_all = stratum_reading(log, d, "all orders")
    log.kv("DECISION (the ne-marked noun's slot, all orders; declared: the verb reads the ne-marked noun if R >= 1.0 bit with p < 0.05 and "
           "mean M_swap(subj) > 0 in both classes; partly if R >= 1.0 bit with p < 0.05 but mean M_swap(subj) <= 0 in a class; else not)", v_all)
    log.kv("DECISION (the bare noun's slot, all orders; declared: a fall of at least 1.0 bit with one-sided p < 0.05 means the verb also reads the bare noun)", b_all)
    if len(st):
        v_st, b_st = stratum_reading(log, st, "swap-correct form is not the default form")
    else:
        v_st, b_st = "not evaluable", "not evaluable"
    log.kv("DECISION (the ne-marked noun's slot, stratum where the swap-correct form is not the default form)", v_st)
    log.kv("DECISION (the bare noun's slot, stratum where the swap-correct form is not the default form)", b_st)
    final = v_all if (v_st == v_all or v_st.startswith("not evaluable")) else v_st
    log.kv("DECISION (P7 verdict on the ne-marked noun's slot; P2 rule: the stratum's verdict if it differs from the overall one)",
           f"{final} (all orders: {v_all}; stratum: {v_st})")
    bfinal = b_all if (b_st == b_all or b_st.startswith("not evaluable")) else b_st
    log.kv("DECISION (P7 reading of the bare noun's slot, same rule)", f"{bfinal} (all orders: {b_all}; stratum: {b_st})")

    # ne: reported, not graded; orig as the unswapped reference
    erows = []
    for c in CLASSES + ["all"]:
        y = d if c == "all" else d[d.order_class == c]
        for v in VERSIONS:
            row = [c, v, len(y)]
            for k in ("obj", "subj", "ne"):
                dif = (y[f"M_{v}_{k}"] - y[f"M_{v}_none"]).to_numpy()
                lo, hi = F.boot_mean(dif, y.doc.to_numpy()) if len(y) > 1 and y.doc.nunique() > 1 else (float("nan"),) * 2
                row.append(f"{dif.mean():.3f} [{lo:.3f}, {hi:.3f}]")
            erows.append(row)
    log.h2("Change of the margin under each mask (M_<cond> minus M_none, paired per order), all orders, both versions "
           "(orig is the unswapped reference; ne is reported and not graded); mean and document bootstrap 95% (descriptive)")
    log.table(["class", "version", "orders", "obj", "subj", "ne"], erows)
    nrows = []
    for c in CLASSES:
        y = d[d.order_class == c]
        dif = (y.M_swap_ne - y.M_swap_none).to_numpy()
        nrows.append([c, len(y), float(dif.mean()), E.pvals(dif, y.doc.to_numpy(), False)])
    log.h2("Masking ne on swap, two-sided document sign-flip (reported, not graded)")
    log.table(["class", "orders", "mean M_swap(ne) - M_swap(none) (bits)", "two-sided p"], nrows, floatfmt="{:.4g}")

    # share of orders whose preference changes sign under each mask
    srows = []
    for label, x in groups:
        for c in CLASSES + ["all"]:
            y = x if c == "all" else x[x.order_class == c]
            for v in VERSIONS:
                n0 = y[f"M_{v}_none"].to_numpy()
                row = [label, c, v, len(y)]
                for k in ("obj", "subj", "ne"):
                    mk = y[f"M_{v}_{k}"].to_numpy()
                    ch = float((np.sign(mk) != np.sign(n0)).mean()) if len(y) else float("nan")
                    up = float(((n0 <= 0) & (mk > 0)).mean()) if len(y) else float("nan")
                    row.append(f"{ch:.3f} / {up:.3f}")
                srows.append(row)
    log.h2("Descriptive: share of orders whose preference changes sign under each mask / share that goes from M <= 0 (none) to M > 0 (masked)")
    log.table(["stratum", "class", "version", "orders", "obj", "subj", "ne"], srows)

    # faithfulness of the 10 heads for the subj corruption on swap
    frows, fres = [], None
    for c in CLASSES + ["all"]:
        y = d if c == "all" else d[d.order_class == c]
        gap = (y.M_swap_none - y.M_swap_subj).to_numpy()
        keep = np.abs(gap) > args.min_gap
        mg = float(gap.mean()) if len(y) else float("nan")
        if keep.sum() < 2 or not mg >= E.FLOOR_MEAN_GAP:
            sh = "NOT ESTIMABLE (mean gap < 1.0 bit)"
        else:
            r, ci = F.share(y.heads_swap_subj.to_numpy(), y.M_swap_subj.to_numpy(), gap, keep, y.doc.to_numpy())
            sh = F.fmt(r, ci)
        if c == "all":
            fres = sh
        frows.append([c, len(y), mg, int(keep.sum()), sh])
    log.h2("Descriptive: the 10 frozen heads' faithfulness for the subj corruption on swap (clean none, corrupted subj); the gap is "
           "M_swap(none) - M_swap(subj), so it is negative where masking the ne-marked noun raises the margin")
    log.table(["class", "orders", "mean gap (bits)", "orders above the gap floor", "10 heads: share of the gap restored"], frows, floatfmt="{:.4g}")
    log.kv("DECISION (descriptive: the 10 heads' faithfulness for the subj corruption on swap, all orders; reported only if the mean gap is "
           "at least 1.0 bit)", fres)
    log.p("Limit: masking is a corruption that may itself change the sentence's acceptability, and the swapped sentences are odd in "
          "meaning, so a preference after the swap may reflect oddness more than agreement; P7 cannot separate the two. "
          "Pseudo-log-likelihood is not true surprisal.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage", default="swap_mask", choices=["swap_mask"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None, help="N orders, N/4 from each order class and default-form stratum (smoke tests)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--max-rows", type=int, default=256)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    note = A.require_metric(SimpleNamespace(model=args.model))
    M.OUT.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"mi_paper_swap_mask_{args.model}"
    with RunLog(tag, __file__, args, purpose=f"Paper experiment P7, stage swap_mask, {args.model}.") as log:
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
            stage_swap_mask(args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
