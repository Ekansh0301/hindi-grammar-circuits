#!/usr/bin/env python3
"""Items for the paper experiments P1, P2 and P6 (docs/PAPER_EXPERIMENTS.md). CPU only; runs on Ada against the
thesis corpus (as mi_items.py). Declared before any run (18 Nov 2026). Words are separated by one space in every
text; every index list is a pipe-separated list of indices into text.split(" "), as agreement_positions.csv.

FRESH AGREEMENT ORDERS: rows of outputs/items/agreement_positions.csv with in_contrast False and no half (the
documents outside the contrast pairs; step 4 never read them), as mi_followup.stage_case_agreement.

P2 ROLE SWAP (agreement_swap.csv). Versions orig (the stored order, unchanged) and swap. In swap the subject phrase
(subj_words, which excludes ne) and the object phrase (obj_words) exchange places; ne and every other word keep their
order; indices are renumbered. A pair of phrases enters only if each is one contiguous run of word indices (skips are
counted by reason). The swapped CORRECT sentence is the swap applied to the old FOIL sentence (the verb forms agree
with the ex-subject, which is now the bare noun in the object slot), the swapped FOIL sentence the swap applied to the
old CORRECT sentence. In swap, obj_words are the positions of the words in the object slot (the ex-subject words),
subj_words those in the subject slot (the ex-object words), ne_word is ne's new index. Also kept: equal_len (the two
phrases have the same number of words), len_subj and len_obj (their numbers of words), the tree features subj_gen,
subj_num, obj_gen, obj_num of the clause's two arguments, and the booleans swapcorrect_default (the subject is
masculine singular, so the swapped sentence's correct form is the default form) and origcorrect_default (the object
is masculine singular).

P1 KO INSERTION (agreement_ko.csv). Orders whose subject head is masculine singular in the reference tree (so the
subject-agreeing foil verb is exactly the default form), computed once per (ref_id, clause_head), and whose object
phrase is one contiguous run. Second-addendum rules (18 Nov): an order is skipped (reason counted) if the object
phrase's last word, or the word after it, is in the closed list CLOSED = {भी, ही, तक, को, से, में, पर, का, की, के}
(the insertions would double a particle), or if its foil agreeing words are not all default forms (a word ending in
ा, or है). Columns obj_gen, obj_num (tree, as subj_gen, subj_num) are kept for the stratification by object number. Versions: none (the stored order); ko (the word को inserted as a new word right after
the object phrase's last word, in both sentences; correct = old FOIL with ko, the default form; foil = old CORRECT
with ko); bhi (the word भी inserted at the same place; correct = old correct with bhi, foil = old foil with bhi, the
control). All index lists renumbered; the object words stay the old object words (the inserted word is not one).

P6 MARKER CONTROL MATCHED IN KIND (wordorder_kind.csv). Fresh pairs of outputs/items_extra/wordorder_pool.csv with
n_psp >= 1. Count the unmoved words (site unmoved, the danda and full stop excluded) whose string is in the closed
list {ने, को, से, में, पर, का, की, के, तक}. The pair enters (kind_ok) if that count >= n_psp. For entering pairs,
n_psp of those words are drawn at random (rng [711, i], i the pair's row in the pool csv) and deleted from both
sentences with mi_items_extra.delete_words (columns *_ctlk).

CHECKS (any failure stops the run): (a) the orig/none version equals the stored order (correct, foil and every index
list); (b) in every version the correct and foil sentences have the same number of words and differ exactly at
agree_words; (c) the swapped sentence has the same multiset of words as the original; (d) ko and bhi differ from none
by one inserted word only; (e) object, subject, verb words and ne are pairwise disjoint in every version and every
index is below the sentence length; (f) agree_words is a subset of verb_words; (g) kind: every deleted word is in the
listed set and (inside delete_words) the alignment is still a permutation; (h) ko and bhi: the inserted word is not
doubled (the words next to it differ from it) and, for ko, the correct agreeing words are all default forms; (i) ctls:
the deleted words are unmoved, distinct, disjoint from the moved markers, their strings equal the markers' strings
(as multisets), their number equals n_psp, and the alignment is a permutation (inside delete_words). Check (a) compares
the orig/none version's correct and foil sentences with data/agreement/agreement_items.csv.

P6 SECONDARY CONTROL ctls (second addendum). For each moved marker (the words the psp version deletes, taken in
word order) an unmoved word (danda and full stop excluded) with the same string, nearest in word distance to any
moved head word (site moved_heads; ties go to the lower index), not already drawn for an earlier marker. A pair is
ctls_ok only if every marker has one (columns ref_text_ctls, var_text_ctls, var_to_ref_ctls, var_site_ctls,
dropped_ctls). Per pair: dist_psp, dist_ctlk, dist_ctls (mean over the deleted words of the word distance to the
nearest moved head word). The record prints, for the markers and for each control, the mean and median distance, the
composition by string and the genitive (का, की, के) share against the other words. kind_ok and the ctlk columns keep
their meaning.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_items as I  # noqa: E402
import mi_items_extra as X  # noqa: E402
import set1_generator as G  # noqa: E402
from hutb_corpus import FC, parse_conllu  # noqa: E402
from materialise_set1 import official_tokens  # noqa: E402
from runlog import RunLog  # noqa: E402

ROOT = HERE.parent
LISTED = ["ने", "को", "से", "में", "पर", "का", "की", "के", "तक"]
CLOSED = ["भी", "ही", "तक", "को", "से", "में", "पर", "का", "की", "के"]
GENITIVE = ["का", "की", "के"]
SITE_HEADS = I.SITES.index("moved_heads")
LISTS = ["tok_order", "agree_words", "verb_words", "obj_words", "subj_words"]
FIELDS = ["correct", "foil", "agree_words", "verb_words", "obj_words", "subj_words", "ne_word"]
IDC = ["order_id", "ref_id", "doc", "order_class", "is_reference", "object_adjacent", "object_verb_gap"]


def ints(s):
    s = str(s)
    return [int(x) for x in s.split("|")] if s and s != "nan" else []


def contiguous(ix):
    ix = sorted(ix)
    return len(ix) > 0 and ix == list(range(ix[0], ix[0] + len(ix)))


def version_ok(v, tag):
    """checks (b), (e), (f) on one version (a dict with the FIELDS)."""
    cw, fw = v["correct"].split(" "), v["foil"].split(" ")
    n = len(cw)
    if len(fw) != n:
        raise SystemExit(f"{tag}: correct and foil differ in length")
    agree = ints(v["agree_words"])
    if [i for i in range(n) if cw[i] != fw[i]] != sorted(agree):
        raise SystemExit(f"{tag}: correct and foil do not differ exactly at agree_words")
    sets = [set(ints(v["obj_words"])), set(ints(v["subj_words"])), set(ints(v["verb_words"])), {int(v["ne_word"])}]
    for a in range(4):
        for b in range(a + 1, 4):
            if sets[a] & sets[b]:
                raise SystemExit(f"{tag}: object, subject, verb words and ne overlap")
    if any(i < 0 or i >= n for s in sets for i in s) or any(i >= n for i in agree):
        raise SystemExit(f"{tag}: an index is outside the sentence")
    if not set(agree) <= sets[2]:
        raise SystemExit(f"{tag}: agree_words are not inside verb_words")


def as_text(v):
    return f"correct: {v['correct']} || foil: {v['foil']} || obj {v['obj_words']} subj {v['subj_words']} ne {v['ne_word']} agree {v['agree_words']}"


def rebuild(w, perm):
    return " ".join(w[i] for i in perm)


def swap_version(o):
    """Swap subject and object phrases. Returns (version dict, equal_len) or a skip reason string."""
    S, O = sorted(ints(o.subj_words)), sorted(ints(o.obj_words))
    if not contiguous(S):
        return "subject phrase not contiguous"
    if not contiguous(O):
        return "object phrase not contiguous"
    n = len(o.correct.split(" "))
    (a0, a1), (b0, b1) = sorted([(S[0], S[-1]), (O[0], O[-1])])
    if a1 >= b0:
        return "phrases overlap"
    # new order of old indices: the later phrase goes first, the earlier phrase takes the later slot
    perm = list(range(a0)) + list(range(b0, b1 + 1)) + list(range(a1 + 1, b0)) + list(range(a0, a1 + 1)) + list(range(b1 + 1, n))
    if sorted(perm) != list(range(n)):
        raise SystemExit(f"{o.order_id}: swap permutation is broken")
    new = {old: k for k, old in enumerate(perm)}
    cw, fw = o.correct.split(" "), o.foil.split(" ")
    mp = lambda s: "|".join(str(new[i]) for i in sorted(ints(s), key=lambda x: new[x]))
    v = {"correct": rebuild(fw, perm), "foil": rebuild(cw, perm), "agree_words": mp(o.agree_words),
         "verb_words": mp(o.verb_words), "obj_words": "|".join(str(new[i]) for i in sorted(S, key=lambda x: new[x])),
         "subj_words": "|".join(str(new[i]) for i in sorted(O, key=lambda x: new[x])), "ne_word": new[int(o.ne_word)]}
    # (c) same multiset of words, both sentences
    if Counter(v["correct"].split(" ")) != Counter(fw) or Counter(v["foil"].split(" ")) != Counter(cw):
        raise SystemExit(f"{o.order_id}: the swapped sentence does not hold the same words")
    return v, len(S) == len(O)


def insert_version(o, word, kind):
    """Insert `word` right after the object phrase's last word. kind 'ko': swap the roles of correct and foil."""
    O = sorted(ints(o.obj_words))
    at = O[-1] + 1
    cw, fw = o.correct.split(" "), o.foil.split(" ")
    ins = lambda w: w[:at] + [word] + w[at:]
    sh = lambda i: i if i < at else i + 1
    mp = lambda s: "|".join(str(sh(i)) for i in ints(s))
    c, f = (fw, cw) if kind == "ko" else (cw, fw)
    return {"correct": " ".join(ins(c)), "foil": " ".join(ins(f)), "agree_words": mp(o.agree_words),
            "verb_words": mp(o.verb_words), "obj_words": mp(o.obj_words), "subj_words": mp(o.subj_words),
            "ne_word": sh(int(o.ne_word))}, at


def stored(o):
    return {"correct": o.correct, "foil": o.foil, "agree_words": o.agree_words, "verb_words": o.verb_words,
            "obj_words": o.obj_words, "subj_words": o.subj_words, "ne_word": int(o.ne_word)}


def check_against_items(o, items, tag):
    """(a): the stored order's correct and foil sentences equal data/agreement/agreement_items.csv's."""
    r = items.get((o.ref_id, o.order_id))
    if r is None or r[0] != o.correct or r[1] != o.foil:
        raise SystemExit(f"{tag} {o.order_id}: correct/foil differ from data/agreement/agreement_items.csv")


def is_default(w):
    return w.endswith("\u093e") or w == "\u0939\u0948"


def foil_all_default(o):
    fw = o.foil.split(" ")
    return all(is_default(fw[i]) for i in ints(o.agree_words))


def clause_features(fresh, log):
    """(subj_gen, subj_num, obj_gen, obj_num) per (ref_id, clause_head), from the reference tree: the k1 and the k2
    dependent of the clause head, as mi_items.agreement_positions finds them."""
    refs = parse_conllu(FC / "reference_trees.conllu", 10)
    out = {}
    for rid, h in sorted(set(zip(fresh.ref_id, fresh.clause_head.astype(int)))):
        toks = official_tokens(refs[rid])
        by = {t["idx"]: t for t in toks}
        kids = G.children(toks)
        res = []
        for rel in ("k1", "k2"):
            k = [x for x in kids.get(h, []) if by[x]["deprel"] == rel]
            if len(k) != 1:
                raise SystemExit(f"{rid} clause {h}: {len(k)} {rel} dependents")
            f = G.feats_dict({"feats": by[k[0]]["feats"]})
            res += [I.g_(f), I.n_(f)]
        out[(rid, h)] = tuple(res)
    log.kv("clauses whose subject and object features were read from the tree", len(out))
    return out


def obj_kind(g, n):
    if n == "pl":
        return "plural"
    if n == "sg" and g == "f":
        return "feminine singular"
    if n == "sg" and g == "m":
        return "masculine singular"
    return "other"


def write_versions(row, versions):
    for vn, v in versions.items():
        for k in FIELDS:
            row[f"{vn}_{k}"] = v[k]


def agreement_items(log, out):
    pos = pd.read_csv(ROOT / "course_runs" / "outputs" / "items" / "agreement_positions.csv", dtype={c: str for c in LISTS})
    fresh = pos[(pos.in_contrast.astype(str) == "False") & pos.half.isna()].reset_index(drop=True)
    log.kv("fresh agreement orders read", f"{len(fresh):,} of {len(pos):,}")
    it = pd.read_csv(ROOT / "data" / "agreement" / "agreement_items.csv", dtype=str)
    items = {(r.ref_id, r.order_id): (r.correct, r.foil) for r in it.itertuples()}
    cf = clause_features(fresh, log)
    swap_rows, ko_rows, skips, ko_skips = [], [], Counter(), Counter()
    ex = {"swap": [], "ko feminine singular": [], "ko plural": [], "bhi": [], "skipped, object ends in or is followed by a particle": [],
          "skipped, foil not a default form": []}
    for o in fresh.itertuples():
        orig = stored(o)
        version_ok(orig, f"orig {o.order_id}")
        check_against_items(o, items, "orig")
        idc = {c: getattr(o, c) for c in IDC}
        sg, sn, og, on = cf[(o.ref_id, int(o.clause_head))]
        tree = {"subj_gen": sg, "subj_num": sn, "obj_gen": og, "obj_num": on}
        # P2
        s = swap_version(o)
        if isinstance(s, str):
            skips[s] += 1
        else:
            sw, eq = s
            version_ok(sw, f"swap {o.order_id}")
            row = dict(idc) | {"equal_len": eq, "len_subj": len(ints(o.subj_words)), "len_obj": len(ints(o.obj_words))} | tree | {
                "swapcorrect_default": sg == "m" and sn == "sg", "origcorrect_default": og == "m" and on == "sg"}
            write_versions(row, {"orig": orig, "swap": sw})
            swap_rows.append(row)
            if len(swap_rows) % 80 == 1 and len(ex["swap"]) < 3:
                ex["swap"].append((orig, sw))
        # P1
        cw = o.correct.split(" ")
        O = ints(o.obj_words)
        if not (sg == "m" and sn == "sg"):
            ko_skips["subject not masculine singular"] += 1
        elif not contiguous(O):
            ko_skips["object phrase not contiguous"] += 1
        elif cw[max(O)] in CLOSED:
            ko_skips["object phrase ends in a listed particle or postposition"] += 1
            if len(ex["skipped, object ends in or is followed by a particle"]) < 3:
                ex["skipped, object ends in or is followed by a particle"].append((orig, None))
        elif max(O) + 1 < len(cw) and cw[max(O) + 1] in CLOSED:
            ko_skips["object phrase is followed by a listed particle or postposition"] += 1
            if len(ex["skipped, object ends in or is followed by a particle"]) < 3:
                ex["skipped, object ends in or is followed by a particle"].append((orig, None))
        elif not foil_all_default(o):
            ko_skips["foil agreeing words not all default forms"] += 1
            if len(ex["skipped, foil not a default form"]) < 3:
                ex["skipped, foil not a default form"].append((orig, None))
        else:
            ko, at = insert_version(o, "को", "ko")
            bhi, at2 = insert_version(o, "भी", "bhi")
            for vn, v, wd in (("ko", ko, "को"), ("bhi", bhi, "भी")):
                version_ok(v, f"{vn} {o.order_id}")
                # (d): removing the inserted word recovers none (ko: with correct and foil exchanged)
                for k, sent in (("correct", o.foil if vn == "ko" else o.correct), ("foil", o.correct if vn == "ko" else o.foil)):
                    w = v[k].split(" ")
                    if w[at] != wd or " ".join(w[:at] + w[at + 1:]) != sent:
                        raise SystemExit(f"{vn} {o.order_id}: more than the inserted word differs from none")
                    # (h): the inserted word is not doubled
                    if w[at - 1] == wd or (at + 1 < len(w) and w[at + 1] == wd):
                        raise SystemExit(f"{vn} {o.order_id}: the inserted word {wd} is doubled")
                # the lists differ from none only by the renumbering around the insertion
                for k in ("agree_words", "verb_words", "obj_words", "subj_words"):
                    back = [i if i < at else i - 1 for i in ints(v[k])]
                    if back != ints(orig[k]):
                        raise SystemExit(f"{vn} {o.order_id}: {k} is not the renumbered stored list")
                if at in ints(v["obj_words"]) + ints(v["subj_words"]) + ints(v["verb_words"]) + [int(v["ne_word"])]:
                    raise SystemExit(f"{vn} {o.order_id}: the inserted word is in a word set")
            # (h): under ko the correct agreeing words are default forms
            kw = ko["correct"].split(" ")
            if not all(is_default(kw[i]) for i in ints(ko["agree_words"])):
                raise SystemExit(f"ko {o.order_id}: the correct agreeing words are not all default forms")
            row = dict(idc) | tree | {"clause_head": int(o.clause_head), "obj_head_word": cw[int(o.obj_head)]}
            write_versions(row, {"none": orig, "ko": ko, "bhi": bhi})
            ko_rows.append(row)
            kk = "ko plural" if on == "pl" else ("ko feminine singular" if (on == "sg" and og == "f") else None)
            if kk and len(ex[kk]) < 3 and len(ko_rows) % 7 == 1:
                ex[kk].append((orig, ko))
            if len(ko_rows) % 60 == 1 and len(ex["bhi"]) < 3:
                ex["bhi"].append((orig, bhi))
    sw = pd.DataFrame(swap_rows)
    ko = pd.DataFrame(ko_rows)
    cols = IDC + ["equal_len", "len_subj", "len_obj", "subj_gen", "subj_num", "obj_gen", "obj_num", "swapcorrect_default",
                  "origcorrect_default"] + [f"{v}_{k}" for v in ("orig", "swap") for k in FIELDS]
    sw[cols].to_csv(out / "agreement_swap.csv", index=False)
    cols = IDC + ["subj_gen", "subj_num", "obj_gen", "obj_num", "clause_head", "obj_head_word"] + [f"{v}_{k}" for v in ("none", "ko", "bhi") for k in FIELDS]
    ko[cols].to_csv(out / "agreement_ko.csv", index=False)
    log.output(str(out / "agreement_swap.csv"), "P2: fresh orders, orig and subject/object-swapped versions")
    log.output(str(out / "agreement_ko.csv"), "P1: fresh orders with a masculine singular subject, none / ko / bhi versions")
    log.table(["P2 swap", "count"], [["fresh orders read", len(fresh)], ["kept", len(sw)]] +
              [[f"skipped: {k}", v] for k, v in skips.items()] + [["equal-length phrases", int(sw.equal_len.sum())]])
    log.table(["P1 ko", "count"], [["fresh orders read", len(fresh)], ["entering", len(ko)]] +
              [[f"skipped: {k}", v] for k, v in ko_skips.items()] +
              [["clauses entering", len(set(zip(ko.ref_id, ko.clause_head)))],
               ["distinct object head words entering", int(ko.obj_head_word.nunique())],
               ["documents entering", int(ko.doc.nunique())]])
    ko["obj_kind"] = [obj_kind(g, n) for g, n in zip(ko.obj_gen, ko.obj_num)]
    log.table(["P1: entering orders by object number", "orders", "documents"],
              [[k, int((ko.obj_kind == k).sum()), int(ko[ko.obj_kind == k].doc.nunique())]
               for k in ("feminine singular", "masculine singular", "plural", "other")])
    sw["swapcorrect_default"] = sw.swapcorrect_default.astype(bool)
    sw["origcorrect_default"] = sw.origcorrect_default.astype(bool)
    log.table(["P2: swapcorrect_default (rows) by origcorrect_default (columns)", "origcorrect_default False", "origcorrect_default True"],
              [[f"swapcorrect_default {b}", int(((sw.swapcorrect_default == b) & ~sw.origcorrect_default).sum()),
                int(((sw.swapcorrect_default == b) & sw.origcorrect_default).sum())] for b in (False, True)])
    for name, d in (("swap", sw), ("ko", ko)):
        log.table([f"{name}: order class", "orders", "documents"],
                  [[c, int((d.order_class == c).sum()), d[d.order_class == c].doc.nunique()] for c in ("SOV", "OSV")] +
                  [["reference orders", int(d.is_reference.sum()), d.doc.nunique()]])
    if len(sw) == 0 or len(ko) == 0:
        raise SystemExit("no orders kept")
    log.h3("Examples (orig/none, then the edited version)")
    for name, lst in ex.items():
        for a, b in lst:
            log.bullet(f"{name} | before: {as_text(a)}")
            if b is not None:
                log.bullet(f"{name} | after:  {as_text(b)}")


def word_dist(idx, heads):
    """word distance of each index to the nearest word of `heads`."""
    return [min(abs(i - h) for h in heads) for i in idx]


def secondary_control(words, site, markers, heads):
    """ctls: for each marker (in word order) an unmoved word with the same string, nearest to a moved head word and not
    already drawn. Returns the list of indices, or None if some marker has none."""
    if not heads:
        return None
    taken, drop = set(), []
    for m in markers:
        cand = [w for w, s in enumerate(site) if s == X.SITE_UNMOVED and words[w] == words[m] and words[w] not in ("।", ".")
                and w not in taken]
        if not cand:
            return None
        best = min(cand, key=lambda w: (min(abs(w - h) for h in heads), w))
        taken.add(best)
        drop.append(best)
    return sorted(drop)


def kind_items(log, out):
    pool = pd.read_csv(ROOT / "course_runs" / "outputs" / "items_extra" / "wordorder_pool.csv",
                       dtype={"var_to_ref": str, "var_site": str})
    rows, n_in, n_s, ex = [], 0, 0, []
    stats = {"markers (kind_ok pairs)": [], "ctlk": [], "markers (ctls_ok pairs)": [], "ctls": []}   # (word, distance)
    for i, r in enumerate(pool.itertuples()):
        if r.pool != "fresh" or int(r.n_psp) < 1:
            continue
        v2r, site = X.ints(r.var_to_ref), X.ints(r.var_site)
        words = r.var_text.split(" ")
        listed = [w for w, s in enumerate(site) if s == X.SITE_UNMOVED and words[w] in LISTED and words[w] not in ("।", ".")]
        markers = [w for w, s in enumerate(site) if s == X.SITE_PSP]
        heads = [w for w, s in enumerate(site) if s == SITE_HEADS]
        if len(markers) != int(r.n_psp):
            raise SystemExit(f"pair {i}: n_psp differs from the number of moved_psp words")
        dm = word_dist(markers, heads) if heads else []
        rec = {"ref_id": r.ref_id, "var_id": r.var_id, "doc": r.doc, "kendall": r.kendall, "n_psp": int(r.n_psp),
               "n_listed_unmoved": len(listed), "kind_ok": len(listed) >= int(r.n_psp),
               "dist_psp": float(np.mean(dm)) if dm else float("nan"), "ctls_ok": False}
        if rec["kind_ok"]:
            drop = sorted(np.random.default_rng([711, i]).choice(listed, size=int(r.n_psp), replace=False).tolist())
            if any(words[d] not in LISTED for d in drop) or any(site[d] != X.SITE_UNMOVED for d in drop):
                raise SystemExit(f"pair {i}: a deleted word is not an unmoved listed word")
            rt, vt, m, s = X.delete_words(r.ref_text, r.var_text, v2r, site, drop)
            dk = word_dist(drop, heads) if heads else []
            rec.update({"ref_text_ctlk": rt, "var_text_ctlk": vt, "var_to_ref_ctlk": I.pipe(m),
                        "var_site_ctlk": I.pipe(s), "dropped_ctlk": I.pipe(drop),
                        "dist_ctlk": float(np.mean(dk)) if dk else float("nan")})
            n_in += 1
            stats["markers (kind_ok pairs)"] += [(words[w], d) for w, d in zip(markers, dm)]
            stats["ctlk"] += [(words[w], d) for w, d in zip(drop, dk)]
        sec = secondary_control(words, site, markers, heads)
        if sec is not None:
            # (i): unmoved, distinct, disjoint from the markers, the same strings as the markers, the same number
            if (len(sec) != len(markers) or len(set(sec)) != len(sec) or set(sec) & set(markers)
                    or any(site[w] != X.SITE_UNMOVED for w in sec)
                    or Counter(words[w] for w in sec) != Counter(words[w] for w in markers)):
                raise SystemExit(f"pair {i}: the secondary control does not match the markers")
            rt, vt, m, s = X.delete_words(r.ref_text, r.var_text, v2r, site, sec)
            ds = word_dist(sec, heads)
            rec.update({"ref_text_ctls": rt, "var_text_ctls": vt, "var_to_ref_ctls": I.pipe(m), "var_site_ctls": I.pipe(s),
                        "dropped_ctls": I.pipe(sec), "dist_ctls": float(np.mean(ds)), "ctls_ok": True})
            n_s += 1
            stats["markers (ctls_ok pairs)"] += [(words[w], d) for w, d in zip(markers, dm)]
            stats["ctls"] += [(words[w], d) for w, d in zip(sec, ds)]
            if len(ex) < 3 and n_s % 20 == 1:
                ex.append((r, markers, sec, rt, vt))
        rows.append(rec)
    d = pd.DataFrame(rows)
    cols = ["ref_id", "var_id", "doc", "kendall", "n_psp", "n_listed_unmoved", "kind_ok", "ref_text_ctlk", "var_text_ctlk",
            "var_to_ref_ctlk", "var_site_ctlk", "dropped_ctlk", "ctls_ok", "ref_text_ctls", "var_text_ctls", "var_to_ref_ctls",
            "var_site_ctls", "dropped_ctls", "dist_psp", "dist_ctlk", "dist_ctls"]
    d[cols].to_csv(out / "wordorder_kind.csv", index=False)
    log.output(str(out / "wordorder_kind.csv"), "P6: fresh pairs with moved markers, the controls matched in kind (ctlk) and in kind and place (ctls)")
    log.table(["P6 kind", "count"], [["fresh pairs with n_psp >= 1", len(d)], ["entering primary test (kind_ok)", n_in],
                                      ["entering secondary test (ctls_ok)", n_s],
                                      ["entering both", int((d.kind_ok & d.ctls_ok).sum())],
                                      ["documents entering the primary test", d[d.kind_ok].doc.nunique()],
                                      ["documents entering the secondary test", d[d.ctls_ok].doc.nunique()],
                                      ["markers deleted per kind_ok pair (mean)", float(d[d.kind_ok].n_psp.mean())]])
    if n_in == 0:
        raise SystemExit("no word-order pair enters P6")
    crow = []
    for k, v in stats.items():
        dist = np.array([x[1] for x in v], float)
        gen = sum(1 for x in v if x[0] in GENITIVE)
        crow.append([k, len(v), float(dist.mean()) if len(v) else float("nan"), float(np.median(dist)) if len(v) else float("nan"),
                     f"{gen} of {len(v)} ({100 * gen / max(1, len(v)):.0f}%)",
                     f"{len(v) - gen} of {len(v)} ({100 * (len(v) - gen) / max(1, len(v)):.0f}%)"])
    log.h2("P6: word distance of the deleted words to the nearest moved head word, and genitive share")
    log.table(["set of deleted words", "words", "mean distance", "median distance", "genitive (का, की, के)", "other"], crow,
              floatfmt="{:.3g}")
    allw = sorted({w for v in stats.values() for w, _ in v}, key=lambda w: -sum(1 for x in stats["markers (kind_ok pairs)"] if x[0] == w))
    log.table(["string"] + list(stats), [[w] + [sum(1 for x in v if x[0] == w) for v in stats.values()] for w in allw])
    log.table(["per pair: mean of the pair's mean distances", "dist_psp", "dist_ctlk", "dist_ctls"],
              [["kind_ok pairs", float(d[d.kind_ok].dist_psp.mean()), float(d[d.kind_ok].dist_ctlk.mean()), "-"],
               ["ctls_ok pairs", float(d[d.ctls_ok].dist_psp.mean()), "-", float(d[d.ctls_ok].dist_ctls.mean())]], floatfmt="{:.3g}")
    log.h3("Examples (reference text, then the same pair with the listed words deleted)")
    for _, r in d[d.kind_ok].iloc[[0, len(d[d.kind_ok]) // 2, -1]].iterrows():
        pr = pool[(pool.ref_id == r.ref_id) & (pool.var_id == r.var_id)].iloc[0]
        log.bullet(f"ctlk | before: ref {pr.ref_text} || var {pr.var_text}")
        log.bullet(f"ctlk | after (dropped variant words {r.dropped_ctlk}): ref {r.ref_text_ctlk} || var {r.var_text_ctlk}")
    for r, markers, sec, rt, vt in ex:
        log.bullet(f"ctls | before: ref {r.ref_text} || var {r.var_text}")
        log.bullet(f"ctls | markers (variant words) {markers}: {[r.var_text.split(' ')[w] for w in markers]}; "
                   f"controls {sec}: {[r.var_text.split(' ')[w] for w in sec]}")
        log.bullet(f"ctls | after: ref {rt} || var {vt}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=None, help="default: course_runs/outputs/items_paper")
    ap.add_argument("--record-tag", default="mi_items_paper")
    args = ap.parse_args()
    out = Path(args.out_dir or ROOT / "course_runs" / "outputs" / "items_paper")
    out.mkdir(parents=True, exist_ok=True)
    with RunLog(args.record_tag, __file__, args, purpose="Items for the paper experiments P1 (ko insertion), P2 (role swap) "
                                                         "and P6 (marker control matched in kind). Rerun under the same tag: the first "
                                                         "run is superseded by the fixes after the independent review (particle "
                                                         "skips, default-form test, object features, secondary control ctls).") as log:
        agreement_items(log, out)
        kind_items(log, out)


if __name__ == "__main__":
    main()
