#!/usr/bin/env python3
"""Object agreement under reordering (EXTENSION_RESEARCH_2026-10-02.md V3, the first item).

In a Hindi perfective clause with an ergative subject (marked ne), the verb agrees in gender and number with an
unmarked object, never with the subject. Reordering moves the subject between the object and the verb (OSV),
which tells two ways a model could know agreement apart: a nearest-noun heuristic would be pulled toward the
subject there, while a model that knows ne-marked subjects do not control agreement would not. Declared before
any run (3 Oct 2026):

--stage build (CPU)
  clauses   Training news references only (Testing stays sealed; the forms lexicon below is built from Training
            too). A clause qualifies when its head is a verb with a k1 dependent marked ne (a ne postposition on
            the k1 head) and a k2 dependent that is a bare noun (no postposition), and the verb complex agrees
            with the object: every verbal word of the verb complex (the generator's R2 span: the main verb and
            every auxiliary, however deeply attached) that marks gender or number (HDTB writes 'any' where a form
            does not mark it, as हैं: gen-any, num-pl) marks the object head's value on each feature it marks
  foil      the subject head's gender and number, when explicit (not 'any') and different from the object's in
            gender or number. Every agreeing word of the verb complex is replaced by a form the Training
            references attest with the same lemma, part of speech, vibhakti and TAM features and the subject's
            gender and number (the most frequent such form, ties by form). A clause any of whose agreeing words
            has no attested foil form is left out, counted. So the foil is the verb agreeing with the wrong
            argument, the subject, in a form Hindi has. A word that marks only number (है, हैं) is switched by
            number (key gender 'any'), so the foil agrees with the subject throughout (revised on review, 3 Oct,
            before any scoring: such words were left unchanged, giving self-contradicting foils like दिया हैं in 66
            of 471 clauses)
  orders    the reference, and its Set 1 variants of the same clause (bigram_ok, at most --cap per reference, seed
            707): each item is one order, written twice, with the attested verb forms and with the foil forms.
            Each order is classed by where the subject stands: between the object and the verb (OSV-type) or
            before the object (SOV-type); and by whether the object is adjacent to the verb complex
  check     every rebuilt correct order equals the stored text (the reference's, or the variant's), or the run
            stops; the foil differs from it only in the replaced words

--stage score (GPU, per model): the summed within_word_l2r PLL (bits) of each correct and each foil sentence,
  pll_scorer.word_surprisals with no context. A = sum(foil) - sum(correct): positive means the model prefers the
  correct agreement. Item ids: a variant's var_id, or reference@<clause head> (two references have two clauses).

--stage analyse (CPU): per model, the share of items with A > 0 and mean A, overall, by order class, by object
  adjacency and for the attested order alone; and the contrast: within each clause, over its VARIANT orders whose
  object is NOT adjacent to the verb complex, mean A of the OSV-type minus the SOV-type, on clauses with both,
  tested by a document-level sign flip of the per-clause differences (10,000). Restricting both sides to a
  non-adjacent object and leaving the attested order out makes the two classes differ in what stands between the
  object and the verb (the ne-marked subject, or some other phrase), not in adjacency, distance class or
  attestedness (revised on review, 3 Oct: OSV-type orders never have the object adjacent, SOV-type ones half the
  time, and almost every attested order is SOV-type). A nearest-noun heuristic predicts a negative contrast;
  agreement that respects case predicts none. The mean gap between object and verb (words) is reported for both
  sides. Because OSV-type orders put the object further from the verb (mean gap about 12 words against 4), the
  PRIMARY contrast is gap-matched: within a clause, OSV-type minus SOV-type mean A at each gap (in words) found in
  both classes, averaged over those gaps, so the two sides have the object equally far from the verb and differ
  only in whether the subject is among the intervening words; the unmatched non-adjacent contrast is secondary.
"""
import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

import order_model as O
import set1_generator as G
from hutb_corpus import BASE, FC, is_null_form, parse_conllu, set1_variants
from materialise_set1 import official_tokens
from runlog import RunLog

FEATS = ("gen", "num", "vib", "tam")


def fd(t):
    return G.feats_dict({"feats": t["feats"]})


def text(tokens):
    return " ".join(t["form"] for t in tokens if not is_null_form(t["form"]))


def build(args, rc, out):
    with RunLog(args.tag or "rq1_agreement_order_build", __file__, args,
                purpose="Agreement items: ergative clauses with a bare object, correct and subject-agreeing foil verbs.") as log:
        refs = parse_conllu(FC / "reference_trees.conllu", 10)
        meta = pd.read_csv(FC / "clauses.tsv", sep="\t", usecols=["ref_id", "split", "domain"]).drop_duplicates("ref_id")
        train = set(meta[(meta.split == "Training") & (meta.domain == "news")].ref_id)
        # forms lexicon from Training: (lemma, xpos, vib, tam, gen, num) -> form counts
        lex = defaultdict(Counter)

        def g_(f):
            return f.get("gen") if f.get("gen") in ("m", "f") else "any"

        def n_(f):
            return f.get("num") if f.get("num") in ("sg", "pl") else "any"
        for rid in train:
            for t in official_tokens(refs[rid]):
                f = fd(t)
                if g_(f) != "any" or n_(f) != "any":
                    lex[(t["lemma"], t["xpos"], f.get("vib", ""), f.get("tam", ""), g_(f), n_(f))][t["form"]] += 1
        V = set1_variants()
        V = V[V.bigram_ok.astype(str) == "True"]
        rng = np.random.default_rng(args.seed)
        cnt = Counter()
        items = []
        for rid in sorted(train):
            toks = official_tokens(refs[rid])
            by = {t["idx"]: t for t in toks}
            kids = G.children(toks)
            for h, t in by.items():
                if not t["xpos"].startswith("V") or t["deprel"] in ("lwg__vaux",):
                    continue
                deps = defaultdict(list)
                for k in kids.get(h, []):
                    deps[by[k]["deprel"]].append(k)
                if len(deps.get("k1", [])) != 1 or len(deps.get("k2", [])) != 1:
                    continue
                s_, o_ = deps["k1"][0], deps["k2"][0]
                if not any(by[g]["form"] == "ने" and by[g]["deprel"] == "lwg__psp" for g in kids.get(s_, [])):
                    continue
                if any(by[g]["deprel"] == "lwg__psp" for g in kids.get(o_, [])) or not by[o_]["xpos"].startswith("N"):
                    continue
                cnt["a. ergative clauses with a bare noun object (Training news)"] += 1
                fo, fs = fd(by[o_]), fd(by[s_])
                # the verb complex: the generator's R2 span (head and the subtrees of its lwg* / pof* dependents);
                # its verbal words (main verb and every auxiliary, however deeply attached) carry agreement
                span = {h} | {i for k in kids.get(h, []) if G.is_verb_complex_rel(by[k]["deprel"])
                              for i in G.subtree(kids, k)}
                vc = sorted(k for k in span if by[k]["xpos"].startswith("V"))
                agreeing = [k for k in vc if g_(fd(by[k])) != "any" or n_(fd(by[k])) != "any"]
                if not agreeing or fo.get("gen") not in ("m", "f") or fo.get("num") not in ("sg", "pl") or \
                        any((g_(fd(by[k])) not in ("any", fo["gen"])) or (n_(fd(by[k])) not in ("any", fo["num"]))
                            for k in agreeing) or \
                        not any(g_(fd(by[k])) != "any" for k in agreeing):
                    cnt["b. left out: the verb complex does not show the object's gender and number"] += 1
                    continue
                if fs.get("gen") not in ("m", "f") or fs.get("num") not in ("sg", "pl"):
                    cnt["c. left out: the subject's gender or number is not explicit"] += 1
                    continue
                if (fs["gen"], fs["num"]) == (fo["gen"], fo["num"]):
                    cnt["d. left out: subject and object agree in gender and number (no foil)"] += 1
                    continue
                foil = {}
                for k in agreeing:
                    f = fd(by[k])
                    c = lex.get((by[k]["lemma"], by[k]["xpos"], f.get("vib", ""), f.get("tam", ""),
                                 fs["gen"] if g_(f) != "any" else "any", fs["num"] if n_(f) != "any" else "any"))
                    if not c:
                        break
                    foil[k] = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
                if len(foil) != len(agreeing):
                    cnt["e. left out: no attested foil form for some agreeing word"] += 1
                    continue
                if all(foil[k] == by[k]["form"] for k in foil):
                    cnt["f. left out: the foil forms equal the attested ones (syncretism)"] += 1
                    continue
                cnt["g. items: clauses with a foil"] += 1
                c = O.Clause(toks, h)
                orders = [(f"reference@{h}", None)]
                if c.ok():
                    vv = V[(V.ref_id == rid) & (V.clause_head == h)]
                    if len(vv) > args.cap:
                        vv = vv.iloc[np.sort(rng.choice(len(vv), args.cap, replace=False))]
                    orders += [(r.var_id, r) for r in vv.itertuples()]
                gen, _ = G.analyse_clause(toks, h)
                ftoks = [dict(t, form=foil.get(t["idx"], t["form"])) for t in toks]
                for name, vr in orders:
                    if vr is None:
                        corr, fl, stored = toks, ftoks, text(toks)
                        pos = {t["idx"]: i for i, t in enumerate(toks)}
                    else:
                        order = [int(x) for x in str(vr.order).split("|")]
                        corr, fl, stored = G.variant_tokens(toks, gen, order), G.variant_tokens(ftoks, gen, order), vr.text
                        new = G.renumber(toks, gen, order)
                        pos = {old: new[old] for old in new}
                        pos = {old: pos.get(old, old) for old in by}
                    if text(corr) != stored:
                        raise SystemExit(f"{rid} {name}: the rebuilt correct sentence differs from the stored text")
                    changed = sum(1 for k in foil if foil[k] != by[k]["form"])
                    wc, wf = [t["form"] for t in corr if not is_null_form(t["form"])], \
                             [t["form"] for t in fl if not is_null_form(t["form"])]
                    if len(wc) != len(wf) or sum(a != b for a, b in zip(wc, wf)) != changed:
                        raise SystemExit(f"{rid} {name}: the foil differs from the correct sentence in other words")
                    # positions among the words the model sees (NULL nodes skipped); the verb complex is the
                    # generator's R2 span (head and the subtrees of its lwg* / pof* dependents)
                    seen = sorted(pos[k] for k in by if not is_null_form(by[k]["form"]))
                    rank = {q: i for i, q in enumerate(seen)}
                    pv = min(rank[pos[k]] for k in span if pos[k] in rank)
                    ps, po = rank[pos[s_]], rank[pos[o_]]
                    # the object's words before the verb complex (an object can carry an extraposed complement
                    # clause after the verb: सफाई ... की कि ..., so its subtree straddles the verb complex)
                    obj_span = sorted(rank[pos[k]] for k in G.subtree(kids, o_) if pos[k] in rank and rank[pos[k]] < pv)
                    gap = pv - obj_span[-1] - 1
                    items.append({"ref_id": rid, "order_id": name, "clause_head": h, "is_reference": vr is None,
                                  "order_class": "OSV" if po < ps else "SOV",
                                  "object_adjacent": gap == 0, "object_verb_gap": gap,
                                  "agreeing_words": len(agreeing), "foil_forms": "|".join(foil[k] for k in agreeing),
                                  "correct": text(corr), "foil": text(fl)})
        d = pd.DataFrame(items)
        f = out / "agreement_items.csv"
        d.to_csv(f, index=False)
        log.output(str(f), "one row per order: correct and foil sentence, order class")
        log.table(["clauses", "count"], sorted(cnt.items()))
        log.table(["items", "count"], [["orders (items)", len(d)], ["references", d.ref_id.nunique()],
                                       ["OSV-type orders / SOV-type orders", f"{(d.order_class == 'OSV').sum()} / {(d.order_class == 'SOV').sum()}"],
                                       ["attested orders that are OSV-type", int((d.is_reference & (d.order_class == 'OSV')).sum())],
                                       ["references with both classes", int(d.groupby('ref_id').order_class.nunique().eq(2).sum())]])
        for r in d.head(3).itertuples():
            log.p(f"example ({r.order_class}): {r.correct}  ||  foil: {r.foil}")


def score(args, rc, out):
    tag, _, path = args.model.partition("=")
    with RunLog(args.tag or f"rq1_agreement_order_score_{tag}", __file__, args,
                purpose=f"Agreement items scored by {tag}.") as log:
        from pll_scorer import load_masked_lm, word_surprisals
        d = pd.read_csv(out / "agreement_items.csv")
        model, tok, device = load_masked_lm(path)
        if device != "cuda":
            raise SystemExit("no GPU visible; refusing to score on the CPU")
        rows = []
        for i, r in enumerate(d.itertuples(), 1):
            sc, _ = word_surprisals(model, tok, device, r.correct, metric="within_word_l2r", batch_size=args.batch_size)
            sf, _ = word_surprisals(model, tok, device, r.foil, metric="within_word_l2r", batch_size=args.batch_size)
            rows.append({"ref_id": r.ref_id, "order_id": r.order_id,
                         "sum_correct": None if sc is None else sum(sc), "sum_foil": None if sf is None else sum(sf)})
            if i % 500 == 0:
                print(f"    {i:,}/{len(d):,}", flush=True)
        s = pd.DataFrame(rows)
        f = out / f"agreement_scores_{tag}.csv"
        s.to_csv(f, index=False)
        log.kv("items scored / unscorable", f"{int(s.sum_correct.notna().sum()):,} / {int(s.sum_correct.isna().sum())}")
        log.output(str(f), "summed PLL of the correct and the foil sentence per item")


def analyse(args, rc, out):
    with RunLog(args.tag or "rq1_agreement_order", __file__, args,
                purpose="Whether the models' agreement survives the subject moving between object and verb.") as log:
        d = pd.read_csv(out / "agreement_items.csv")
        if d.duplicated(["ref_id", "order_id"]).any():
            raise SystemExit("item ids are not unique")
        summary = []
        for k_m, m in enumerate(args.models):
            rng = np.random.default_rng([args.seed, k_m])
            f = out / f"agreement_scores_{m}.csv"
            if not f.exists():
                log.kv(m, "not scored, skipped")
                continue
            sc = pd.read_csv(f)
            if sc.duplicated(["ref_id", "order_id"]).any():
                raise SystemExit(f"{m}: duplicate score rows")
            x = d.merge(sc, on=["ref_id", "order_id"], validate="one_to_one").dropna(subset=["sum_correct", "sum_foil"])
            x["A"] = x.sum_foil - x.sum_correct
            log.h2(f"model: {m}")
            rows = []
            for name, sel in (("all orders", x.A.notna()), ("attested order only", x.is_reference),
                              ("OSV-type orders", x.order_class == "OSV"), ("SOV-type orders", x.order_class == "SOV"),
                              ("object adjacent to the verb", x.object_adjacent),
                              ("object not adjacent", ~x.object_adjacent),
                              ("OSV-type, variants, object not adjacent",
                               (x.order_class == "OSV") & ~x.is_reference & ~x.object_adjacent),
                              ("SOV-type, variants, object not adjacent",
                               (x.order_class == "SOV") & ~x.is_reference & ~x.object_adjacent)):
                y = x[sel]
                rows.append([name, len(y), float((y.A > 0).mean()) if len(y) else None,
                             float(y.A.mean()) if len(y) else None, float(y.object_verb_gap.mean()) if len(y) else None])
            log.table(["items", "n", "correct agreement preferred (A > 0)", "mean A (bits)", "mean object-verb gap (words)"],
                      rows, floatfmt="{:.4f}")
            z = x[~x.is_reference & ~x.object_adjacent]

            def contrast(keys):
                g = z.groupby(keys + ["order_class"]).A.mean().unstack()
                if not {"OSV", "SOV"} <= set(g.columns):
                    return None
                g = g.dropna(subset=["OSV", "SOV"])
                cell = (g["OSV"] - g["SOV"]).groupby(level=["ref_id", "clause_head"]).mean()
                docs = [O.doc_of(r) for r, _ in cell.index]
                sums = cell.groupby(docs).sum().to_numpy()
                obs = sums.sum()
                null = np.array([(sums * rng.choice([-1.0, 1.0], len(sums))).sum() for _ in range(args.permutations)])
                return len(cell), float(cell.mean()), (1 + int((np.abs(null) >= abs(obs)).sum())) / (1 + args.permutations)
            res = {}
            for label, keys in (("gap-matched (primary)", ["ref_id", "clause_head", "object_verb_gap"]),
                                ("unmatched, object not adjacent", ["ref_id", "clause_head"])):
                r_ = contrast(keys)
                if r_:
                    res[label] = r_
                    log.kv(f"OSV-type minus SOV-type mean A, {label}: clauses / bits / document sign-flip p",
                           f"{r_[0]:,} / {r_[1]:+.4f} / {r_[2]:.4g}")
            if res:
                pm = res.get("gap-matched (primary)", (0, None, None))
                um = res.get("unmatched, object not adjacent", (0, None, None))
                summary.append([m, len(x), float((x.A > 0).mean()), pm[0], pm[1], pm[2], um[0], um[1], um[2]])
        log.h2("Summary")
        log.table(["model", "items", "correct agreement preferred", "clauses, gap-matched", "OSV minus SOV, gap-matched",
                   "sign-flip p", "clauses, unmatched", "OSV minus SOV, unmatched", "sign-flip p"], summary,
                  floatfmt="{:.4g}")
        log.p("The contrast uses only variant orders whose object is not adjacent to the verb complex, so on both "
              "sides something stands between object and verb: in OSV-type orders the ne-marked subject, in SOV-type "
              "orders another phrase. A nearest-noun heuristic predicts a negative difference; agreement that "
              "respects case predicts none.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--stage", required=True, choices=["build", "score", "analyse"])
    ap.add_argument("--model", help="tag=path_or_hub_id (score)")
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "xlmrlarge", "mbert"])
    ap.add_argument("--cap", type=int, default=30)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--permutations", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=707)
    ap.add_argument("--out-dir", default=str(rc / "agreement"))
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    {"build": build, "score": score, "analyse": analyse}[args.stage](args, rc, out)


if __name__ == "__main__":
    main()
