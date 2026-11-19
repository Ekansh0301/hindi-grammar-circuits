#!/usr/bin/env python3
"""Items for the three follow-up experiments (docs/FOLLOWUP_EXPERIMENTS.md): the word-order pool with its reordering
sizes and the case-marker deletions. CPU only; runs on Ada against the thesis corpus (as mi_items.py). Declared
before any run (27 Oct 2026).

THE POOL. Step 2's 1,000 patched pairs, all of them, with sites built by mi_items.word_order_pairs (called with
n_wordorder = 1000, which draws the whole 1,000 in sorted order), checked against step 2's subtoken counts for both
tokenizers by mi_items.check_sites. Each pair is assigned to a pool:
  selection / heldout   the 300 pairs step 4 used (their halves from outputs/items/wordorder_pairs.csv)
  seen_doc              one of the other 700 whose document is among the 300's documents (either half)
  fresh                 the rest: documents step 4 never read. Only these are used by the follow-up experiments, so
                        nothing a follow-up reads was used to pick the circuit or to validate it.
CHECK: for the 300 pairs of step 4, the texts, the alignment and the sites rebuilt here are identical to
wordorder_pairs.csv.

REORDERING SIZE. `kendall` from data/word_order/pairs.csv: the number of phrase pairs whose order is swapped (1 = a
single swap), the size used by the proposal's second check. Bins: 1, 2-3, 4-7, 8+ (as the slide); the primary
grouping for the tests merges the last two (4+), because the 8+ bin of fresh pairs is small.

CASE-MARKER DELETION (experiment 2, word order). For every fresh pair:
  psp    delete every variant word whose site is moved_psp (the postpositions and case markers attached to the
         phrases that moved) from BOTH sentences (the same words, found through the alignment)
  ctl    delete the same number of words, drawn at random (seed 709, per pair) from the site `unmoved` (the
         sentence-final danda or full stop excluded), from both sentences. The control for 'any deletion'
A pair enters experiment 2 only if it has at least one moved_psp word and at least as many unmoved words as it
deletes. Kept per condition: the two texts, the alignment (variant word to reference word) and the sites, with the
words renumbered. CHECKS: every aligned variant word and reference word are the same string; the two texts of every edited pair still have the same number of words; the alignment is
still a permutation; the deleted reference words are exactly the images of the deleted variant words.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_items as I  # noqa: E402
from runlog import RunLog  # noqa: E402

ROOT = HERE.parent
SITE_PSP, SITE_UNMOVED = I.SITES.index("moved_psp"), I.SITES.index("unmoved")
BINS = [("1", lambda k: k == 1), ("2-3", lambda k: 2 <= k <= 3), ("4-7", lambda k: 4 <= k <= 7), ("8+", lambda k: k >= 8)]


def ints(s):
    return [int(x) for x in str(s).split("|")]


def bin_of(k):
    return next(n for n, f in BINS if f(k))


def delete_words(ref_text, var_text, v2r, site, drop):
    """Remove the variant words `drop` from the variant text and their images from the reference text; renumber."""
    vw, rw = var_text.split(" "), ref_text.split(" ")
    if len(vw) != len(v2r) or len(rw) != len(v2r):
        raise SystemExit(f"word counts differ from the alignment: {len(vw)} / {len(rw)} / {len(v2r)}")
    drop = set(drop)
    if any(vw[i] != rw[v2r[i]] for i in range(len(vw))):
        raise SystemExit("an aligned variant word and reference word are different strings")
    gone_ref = {v2r[i] for i in drop}
    if len(gone_ref) != len(drop):
        raise SystemExit("two deleted variant words map to one reference word")
    keep_v = [i for i in range(len(vw)) if i not in drop]
    keep_r = [j for j in range(len(rw)) if j not in gone_ref]
    new_r = {j: n for n, j in enumerate(keep_r)}
    out_v2r = [new_r[v2r[i]] for i in keep_v]
    if sorted(out_v2r) != list(range(len(keep_v))) or len(keep_r) != len(keep_v):
        raise SystemExit("the edited alignment is not a permutation")
    return (" ".join(rw[j] for j in keep_r), " ".join(vw[i] for i in keep_v), out_v2r, [site[i] for i in keep_v])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=None, help="default: course_runs/outputs/items_extra")
    ap.add_argument("--record-tag", default="mi_items_extra")
    args = ap.parse_args()
    out = Path(args.out_dir or ROOT / "course_runs" / "outputs" / "items_extra")
    out.mkdir(parents=True, exist_ok=True)
    with RunLog(args.record_tag, __file__, args, purpose="Items for the follow-up experiments: the word-order pool, "
                                                         "reordering sizes, case-marker deletions.") as log:
        ns = argparse.Namespace(n_wordorder=1000)
        wo = I.word_order_pairs(ns, log)
        if len(wo) != 1000:
            raise SystemExit(f"expected step 2's 1,000 pairs, built {len(wo)}")
        I.check_sites(wo, log)
        old = pd.read_csv(ROOT / "course_runs" / "outputs" / "items" / "wordorder_pairs.csv",
                          dtype={"var_to_ref": str, "var_site": str}).set_index(["ref_id", "var_id"])
        wo = wo.set_index(["ref_id", "var_id"])
        bad = 0
        for k, r in old.iterrows():
            n = wo.loc[k]
            bad += int(not (n.ref_text == r.ref_text and n.var_text == r.var_text and n.var_to_ref == r.var_to_ref
                            and n.var_site == r.var_site and n.doc == r.doc))
        log.kv("check: the 300 pairs of step 4 rebuilt here, pairs that differ from wordorder_pairs.csv", f"{bad} of {len(old)}")
        if bad:
            raise SystemExit("the rebuilt pairs differ from the ones step 4 used")
        wo["half"] = old.half.reindex(wo.index)
        docs_seen = set(old.doc)
        kend = pd.read_csv(ROOT / "data" / "word_order" / "pairs.csv").set_index(["ref_id", "var_id"]).kendall
        wo["kendall"] = kend.reindex(wo.index)
        if wo.kendall.isna().any():
            raise SystemExit("a pair has no reordering size in data/word_order/pairs.csv")
        wo["pool"] = [h if isinstance(h, str) else ("seen_doc" if d in docs_seen else "fresh")
                      for h, d in zip(wo.half, wo.doc)]
        wo["bin"] = [bin_of(int(k)) for k in wo.kendall]
        wo = wo.reset_index()
        log.table(["pool", "pairs", "documents"] + [f"size {n}" for n, _ in BINS],
                  [[p, int((wo.pool == p).sum()), wo[wo.pool == p].doc.nunique()] +
                   [int(((wo.pool == p) & (wo.bin == n)).sum()) for n, _ in BINS]
                   for p in ("selection", "heldout", "seen_doc", "fresh")])
        fresh = wo[wo.pool == "fresh"]
        if set(fresh.doc) & docs_seen:
            raise SystemExit("a fresh pair shares a document with step 4's pairs")

        rows = []
        for i, r in enumerate(wo.itertuples()):
            rec = {"n_psp": 0, "psp_ok": False}
            if r.pool == "fresh":
                v2r, site = ints(r.var_to_ref), ints(r.var_site)
                psp = [w for w, s in enumerate(site) if s == SITE_PSP]
                # the sentence-final danda is not a candidate for the control: deleting it is not like deleting a word
                unm = [w for w, s in enumerate(site) if s == SITE_UNMOVED and r.var_text.split(" ")[w] not in ("।", ".")]
                rec["n_psp"] = len(psp)
                if psp and len(unm) >= len(psp):
                    rng = np.random.default_rng([709, i])
                    ctl = sorted(rng.choice(unm, size=len(psp), replace=False).tolist())
                    for tag, drop in (("psp", psp), ("ctl", ctl)):
                        rt, vt, m, s = delete_words(r.ref_text, r.var_text, v2r, site, drop)
                        rec[f"ref_text_{tag}"], rec[f"var_text_{tag}"] = rt, vt
                        rec[f"var_to_ref_{tag}"] = I.pipe(m)
                        rec[f"var_site_{tag}"] = I.pipe(s)
                        rec[f"dropped_{tag}"] = I.pipe(drop)
                    rec["psp_ok"] = True
            rows.append(rec)
        wo = pd.concat([wo, pd.DataFrame(rows, index=wo.index)], axis=1)
        f = wo[wo.pool == "fresh"]
        log.table(["fresh pairs", "with moved_psp words", "psp words deleted (mean per pair)", "entering experiment 2"],
                  [[len(f), int((f.n_psp > 0).sum()), float(f.n_psp[f.n_psp > 0].mean()), int(f.psp_ok.sum())]])
        log.table(["size bin"] + ["fresh pairs", "entering experiment 2"],
                  [[n, int((f.bin == n).sum()), int(((f.bin == n) & f.psp_ok).sum())] for n, _ in BINS])
        path = out / "wordorder_pool.csv"
        wo.to_csv(path, index=False)
        log.output(str(path), "step 2's 1,000 pairs with pool, reordering size and the case-marker deletions")


if __name__ == "__main__":
    main()
