#!/usr/bin/env python3
"""Items for step 4: word positions of the agreement orders, the contrast pairs, the document split, and the
word-order pairs with their alignment and sites. CPU only; runs on Ada against the thesis corpus (HUTB_BASE and
HUTB_CORPUS from mi_common.sh). Declared before any run (23 Oct 2026):

AGREEMENT ORDERS (data/agreement/agreement_items.csv, 5,265 orders of 459 clauses)
  Every order is rebuilt from the reference tree exactly as rq1_agreement_order.py --stage build built it (the
  clause's k1 subject marked ne, its bare k2 object, the verb complex as the generator's R2 span, the agreeing
  words, and for a variant the generator's renumbering of the stored unit order). Kept per order, as whitespace
  word indices of the stored sentence:
    tok_order       the reference tree index of every surface word, in order (the alignment between two orders)
    agree_words     the agreeing words whose wrong form differs from the attested one (the scored span)
    verb_words      the whole verb complex
    obj_words       the object's subtree words before the verb complex (as the build's object span)
    subj_words      the subject's subtree words except ne
    ne_word, obj_head, subj_head
  checks (any failure stops the run): the rebuilt sentence equals the stored correct sentence; the words where
  the stored correct and wrong sentences differ are exactly agree_words; order class and object-verb gap
  reproduce the stored ones; object, subject and verb words are disjoint.

CONTRAST PAIRS: the baseline check's selection (baseline_check.py): variant orders whose object is not adjacent to
  the verb; within a clause and an object-verb gap, every OSV-type order paired with every SOV-type order. The
  counts must reproduce 670 pairs, 207 cells, 102 clauses, 91 documents.

DOCUMENT SPLIT: the documents of the contrast pairs, sorted and permuted with seed 707; the first half (rounded
  up) is the selection half, the rest the held-out half. Components are chosen on the selection half only; the
  held-out half is read once, by the validation stages.

WORD-ORDER PAIRS: step 2's 1,000 patched pairs (rq1_sample_n12000.csv, seed 707, as rq1_patching.py), of which
  300 are drawn with seed 708 and split by document with the same rule (seed 707 on their own documents).
  Kept per pair: both texts, the reference word of every variant word (by tree index), and the site of every
  variant word, computed exactly as rq1_patching.py computes it (moved_heads, moved_psp, moved_other, verb,
  unmoved). check: with each model's tokenizer the subtoken count of every site equals step 2's n_<site> for the
  pair (patching_<model>.csv), so the sites are the ones step 2 patched.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "reference_code"))

import lm_units as U  # noqa: E402
import order_model as O  # noqa: E402
import set1_generator as G  # noqa: E402
from hutb_corpus import BASE, FC, is_null_form, load_trees, parse_conllu, set1_variants, text_of  # noqa: E402
from materialise_set1 import official_tokens  # noqa: E402
from runlog import RunLog  # noqa: E402

SITES = ["moved_heads", "moved_psp", "moved_other", "verb", "unmoved"]


def pipe(xs):
    return "|".join(str(int(x)) for x in xs)


def g_(f):
    return f.get("gen") if f.get("gen") in ("m", "f") else "any"


def n_(f):
    return f.get("num") if f.get("num") in ("sg", "pl") else "any"


def agreement_positions(d, log):
    refs = parse_conllu(FC / "reference_trees.conllu", 10)
    V = set1_variants().set_index("var_id")
    rows = []
    for r in d.itertuples():
        toks = official_tokens(refs[r.ref_id])
        by = {t["idx"]: t for t in toks}
        kids = G.children(toks)
        h = int(r.clause_head)
        deps = {}
        for k in kids.get(h, []):
            deps.setdefault(by[k]["deprel"], []).append(k)
        s_, o_ = deps["k1"][0], deps["k2"][0]
        assert len(deps["k1"]) == 1 and len(deps["k2"]) == 1, r.order_id
        ne = [g for g in kids.get(s_, []) if by[g]["form"] == "ने" and by[g]["deprel"] == "lwg__psp"]
        if len(ne) != 1:
            raise SystemExit(f"{r.ref_id} {r.order_id}: {len(ne)} ne postpositions on the subject")
        span = {h} | {i for k in kids.get(h, []) if G.is_verb_complex_rel(by[k]["deprel"]) for i in G.subtree(kids, k)}
        vc = sorted(k for k in span if by[k]["xpos"].startswith("V"))
        agreeing = [k for k in vc if g_(G.feats_dict({"feats": by[k]["feats"]})) != "any"
                    or n_(G.feats_dict({"feats": by[k]["feats"]})) != "any"]
        foil = dict(zip(agreeing, str(r.foil_forms).split("|")))
        if len(foil) != len(agreeing):
            raise SystemExit(f"{r.ref_id} {r.order_id}: foil forms do not match the agreeing words")
        if r.is_reference:
            pos = {k: k for k in by}
        else:
            vr = V.loc[r.order_id]
            if vr.ref_id != r.ref_id or int(vr.clause_head) != h:
                raise SystemExit(f"{r.order_id}: variant does not belong to {r.ref_id} clause {h}")
            gen, _ = G.analyse_clause(toks, h)
            new = G.renumber(toks, gen, [int(x) for x in str(vr.order).split("|")])
            pos = {old: new.get(old, old) for old in by}
        surface = sorted((k for k in by if not is_null_form(by[k]["form"])), key=lambda k: pos[k])
        words = [by[k]["form"] for k in surface]
        if " ".join(words) != r.correct:
            raise SystemExit(f"{r.ref_id} {r.order_id}: rebuilt sentence differs from the stored one")
        w = {k: i for i, k in enumerate(surface)}
        pv = min(w[k] for k in span if k in w)
        obj = sorted(w[k] for k in G.subtree(kids, o_) if k in w and w[k] < pv)
        subj = sorted(w[k] for k in G.subtree(kids, s_) if k in w and k != ne[0])
        verb = sorted(w[k] for k in span if k in w)
        agree = sorted(w[k] for k in agreeing if foil[k] != by[k]["form"])
        diff = [i for i, (a, b) in enumerate(zip(r.correct.split(" "), r.foil.split(" "))) if a != b]
        if diff != agree or len(r.correct.split(" ")) != len(r.foil.split(" ")):
            raise SystemExit(f"{r.ref_id} {r.order_id}: correct and wrong sentences differ outside the agreeing words")
        gap = pv - obj[-1] - 1
        cls = "OSV" if w[o_] < w[s_] else "SOV"
        if gap != int(r.object_verb_gap) or cls != r.order_class:
            raise SystemExit(f"{r.ref_id} {r.order_id}: gap or order class does not reproduce")
        if set(obj) & set(subj) or set(obj) & set(verb) or set(subj) & set(verb) or w[ne[0]] in set(obj) | set(verb):
            raise SystemExit(f"{r.ref_id} {r.order_id}: object, subject and verb words overlap")
        rows.append({"ref_id": r.ref_id, "order_id": r.order_id, "clause_head": h, "doc": O.doc_of(r.ref_id),
                     "is_reference": bool(r.is_reference), "order_class": r.order_class,
                     "object_adjacent": bool(r.object_adjacent), "object_verb_gap": int(r.object_verb_gap),
                     "correct": r.correct, "foil": r.foil, "tok_order": pipe(surface), "agree_words": pipe(agree),
                     "verb_words": pipe(verb), "obj_words": pipe(obj), "subj_words": pipe(subj),
                     "ne_word": w[ne[0]], "obj_head": w[o_], "subj_head": w[s_]})
    out = pd.DataFrame(rows)
    log.kv("orders rebuilt and checked", f"{len(out):,} of {len(d):,}")
    return out


def contrast_pairs(pos):
    z = pos[~pos.is_reference & ~pos.object_adjacent]
    rows = []
    for (rid, h, gap), g in z.groupby(["ref_id", "clause_head", "object_verb_gap"]):
        o, s = g[g.order_class == "OSV"], g[g.order_class == "SOV"]
        for a in o.order_id:
            for b in s.order_id:
                rows.append({"ref_id": rid, "clause_head": h, "object_verb_gap": gap, "doc": O.doc_of(rid),
                             "osv_order": a, "sov_order": b})
    return pd.DataFrame(rows)


def split_docs(docs, seed=707):
    u = sorted(set(docs))
    perm = np.random.default_rng(seed).permutation(len(u))
    sel = {u[i] for i in perm[: (len(u) + 1) // 2]}
    return {d: ("selection" if d in sel else "heldout") for d in u}


def word_order_pairs(args, log):
    refs, vars_ = load_trees()
    vt = set1_variants().set_index("var_id")
    pairs = pd.read_csv(BASE / "Results_Checks" / "rq1_sample_n12000.csv")[["ref_id", "var_id"]]
    pick = pairs.iloc[np.sort(np.random.default_rng(707).choice(len(pairs), size=1000, replace=False))]
    sub = pick.iloc[np.sort(np.random.default_rng(708).choice(len(pick), size=args.n_wordorder, replace=False))]
    rows = []
    for r in sub.itertuples():
        rt, vtr = refs[r.ref_id], vars_[r.var_id]
        v = vt.loc[r.var_id]
        rtext, vtext = text_of(rt, True), text_of(vtr, False)
        ridx, vidx = U.set1_surface_indices(rt, v.to_dict() | {"var_id": r.var_id}, vtr)
        rpos = {t: k for k, t in enumerate(ridx)}
        # sites exactly as rq1_patching.py
        toks = official_tokens(rt)
        by = {t_["idx"]: t_ for t_ in toks}
        kids = G.children(toks)
        head = int(v.clause_head)
        c = O.Clause(toks, head)
        order = [int(x) for x in str(v.order).split("|")]
        moved_units = [c.units[u] for k, u in enumerate(order) if u != k and c.surface[u]]
        moved_heads = {O.representative(by, kids, d) for d in moved_units}
        moved_psp = {k_ for d in moved_units for h in {d, O.representative(by, kids, d)}
                     for k_ in kids.get(h, []) if by[k_]["deprel"] == "lwg__psp"}
        verb = {head} | {i for k_ in kids.get(head, []) if G.is_verb_complex_rel(by[k_]["deprel"])
                         for i in G.subtree(kids, k_)}
        moved_words = {k_ for d in moved_units for k_ in G.subtree(kids, d)}
        site_words = {"moved_heads": moved_heads, "moved_psp": moved_psp,
                      "moved_other": moved_words - moved_heads - moved_psp, "verb": verb}
        site_words["unmoved"] = set(vidx) - moved_words - verb
        site = []
        for t in vidx:
            lab = [s for s in SITES if t in site_words[s]]
            # rq1_patching assigns a word to every site whose set contains it; the sets are disjoint by
            # construction except that moved_heads, moved_psp and verb could share a word in a degenerate tree
            if len(lab) != 1:
                raise SystemExit(f"{r.var_id}: tree word {t} is in {len(lab)} sites")
            site.append(SITES.index(lab[0]))
        rows.append({"ref_id": r.ref_id, "var_id": r.var_id, "doc": O.doc_of(r.ref_id), "ref_text": rtext,
                     "var_text": vtext, "var_to_ref": pipe(rpos[t] for t in vidx), "var_site": pipe(site)})
    return pd.DataFrame(rows)


def check_sites(wo, log):
    """Subtoken count per site under each model's tokenizer against step 2's records of the same pairs."""
    from transformers import AutoTokenizer
    sys.path.insert(0, str(HERE))
    from mi_lib import MODELS
    rc = BASE / "Results_Checks" / "patching"
    rows = []
    for tag, (path, _) in MODELS.items():
        f = rc / f"patching_{tag}.csv"
        if not f.exists():
            raise SystemExit(f"{f} missing: cannot check the sites against step 2")
        step2 = pd.read_csv(f).set_index(["ref_id", "var_id"])
        tok = AutoTokenizer.from_pretrained(path)
        bad = 0
        for r in wo.itertuples():
            g = U.whitespace_groups(tok, r.var_text)
            ids, groups, gw, nw = g
            sub = np.zeros(len(SITES), int)
            site = [int(x) for x in r.var_site.split("|")]
            for k, pos in enumerate(groups):
                sub[site[gw[k]]] += len(pos)
            want = step2.loc[(r.ref_id, r.var_id), [f"n_{s}" for s in SITES]].to_numpy()
            bad += int((sub != want).any())
        rows.append([tag, len(wo), bad])
        if bad:
            raise SystemExit(f"{tag}: {bad} pairs whose site subtoken counts differ from step 2's")
    log.table(["tokenizer", "pairs", "pairs whose site counts differ from step 2"], rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-wordorder", type=int, default=300)
    ap.add_argument("--out-dir", default=None, help="default: MI_ITEMS, else course_runs/outputs/items")
    ap.add_argument("--record-tag", default="mi_items")
    args = ap.parse_args()
    import os
    out = Path(args.out_dir or os.environ.get("MI_ITEMS", ROOT / "course_runs" / "outputs" / "items"))
    out.mkdir(parents=True, exist_ok=True)
    with RunLog(args.record_tag, __file__, args, purpose="Items, pairs and the document split for step 4.") as log:
        d = pd.read_csv(ROOT / "data" / "agreement" / "agreement_items.csv")
        pos = agreement_positions(d, log)
        cp = contrast_pairs(pos)
        cells = cp.groupby(["ref_id", "clause_head", "object_verb_gap"]).ngroups
        clauses = cp.groupby(["ref_id", "clause_head"]).ngroups
        log.table(["contrast pairs", "cells", "clauses", "documents"], [[len(cp), cells, clauses, cp.doc.nunique()]])
        if (len(cp), cells, clauses, cp.doc.nunique()) != (670, 207, 102, 91):
            raise SystemExit("the contrast selection does not reproduce the baseline check's counts")
        half = split_docs(cp.doc)
        cp["half"] = cp.doc.map(half)
        cp.insert(0, "pair_id", range(len(cp)))
        in_pairs = set(cp.osv_order) | set(cp.sov_order)
        pos["in_contrast"] = pos.order_id.isin(in_pairs)
        pos["half"] = pos.doc.map(half)
        rows = []
        for hname in ("selection", "heldout"):
            c = cp[cp.half == hname]
            o = pos[pos.in_contrast & (pos.half == hname)]
            rows.append([hname, c.doc.nunique(), c.groupby(["ref_id", "clause_head"]).ngroups, len(c), len(o),
                         int((o.order_class == "OSV").sum()), int((o.order_class == "SOV").sum())])
        log.table(["half", "documents", "clauses", "contrast pairs", "orders in pairs", "OSV-type", "SOV-type"], rows)
        f1, f2 = out / "agreement_positions.csv", out / "contrast_pairs.csv"
        pos.to_csv(f1, index=False)
        cp.to_csv(f2, index=False)
        log.output(str(f1), "every agreement order with word positions, document and half")
        log.output(str(f2), "OSV-type / SOV-type pairs within clause and gap, with the half")

        wo = word_order_pairs(args, log)
        wh = split_docs(wo.doc)
        wo["half"] = wo.doc.map(wh)
        check_sites(wo, log)
        log.table(["word-order half", "documents", "pairs"],
                  [[h, wo[wo.half == h].doc.nunique(), int((wo.half == h).sum())] for h in ("selection", "heldout")])
        f3 = out / "wordorder_pairs.csv"
        wo.to_csv(f3, index=False)
        log.output(str(f3), "300 of step 2's patched pairs: texts, word alignment, sites, half")


if __name__ == "__main__":
    main()
