#!/usr/bin/env python3
"""Where in the sentence is the baseline's intervening-subject effect? (A0 follow-up, 23 Oct 2026, declared before
it was run.) GPU, per model.

Why. The baseline margin is whole-sentence: A = sum over every word w of S_wrong(w) - S_correct(w), each word scored
within_word_l2r in its own sentence (data/agreement/agreement_scores_<model>.csv). MuRIL's gap-matched
intervening-subject contrast on A is -1.75 bits (p 1e-4). A0 found that the margin of the agreeing words alone,
scored as one chain, shows no such effect for MuRIL (-0.05 bits, p 0.80). So the -1.75 is carried by how some other
words are scored next to the two verb forms. This says which.

What. For every order in the contrast pairs (both halves: the stage chooses nothing), the per-word surprisals of
the correct and the wrong sentence (lm_units.score_words, the scorer of steps 1 to 3), and A split by word class:
agree (the agreeing words that differ), verb (the rest of the verb complex), object (the object phrase's words
before the verb complex, as mi_items defines it; an object word after the verb counts as other), subject (the
subject phrase without ne), ne, other. Then the baseline's gap-matched contrast (mi_agreement.contrast_test,
the same seed as the baseline) for A and for each class.
CHECKS (hardened on review, 23 Oct, before the full run): both sentences have one score per whitespace word and the
same word count; every class index is inside the sentence; the words where the two sentences differ are exactly
the agree class; every score is finite; A reproduces the stored baseline sums to 1e-2 bits (the scorer's float
noise; rq1_late_ablation.py's tolerance); on a full run every order is scored and the stored margin's contrast
reproduces the baseline (102 clauses, MuRIL -1.7468, XLM-R-large -0.2120 bits) before anything is written.
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
import mi_agreement as AG  # noqa: E402
import lm_units as U  # noqa: E402
from runlog import RunLog  # noqa: E402

CLASSES = ["agree", "verb", "object", "subject", "ne", "other"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    M.OUT.mkdir(parents=True, exist_ok=True)
    bs = M.MODELS[args.model][1]
    with RunLog(args.record_tag or f"mi_decompose_{args.model}", __file__, args,
                purpose=f"Where the baseline's intervening-subject effect lies, by word class, {args.model}.") as log:
        model, tok = M.load(args.model)
        pos = AG.read_positions()
        o = pos[pos.in_contrast]
        if args.limit:
            o = o.head(args.limit)
        base = pd.read_csv(M.ROOT / "data" / "agreement" / f"agreement_scores_{args.model}.csv").set_index(["ref_id", "order_id"])
        rows, worst_sum, worst_base = [], 0.0, 0.0
        for i, r in enumerate(o.itertuples(), 1):
            c = U.score_words(model, tok, M.DEVICE, r.correct, bs, layers=False)
            f = U.score_words(model, tok, M.DEVICE, r.foil, bs, layers=False)
            if c is None or f is None:
                continue
            wc_words, wf_words = r.correct.split(" "), r.foil.split(" ")
            n = len(wc_words)
            if not (len(c[0]) == len(f[0]) == n == len(wf_words)):
                raise SystemExit(f"{r.order_id}: word counts differ between the sentences and their scores")
            idx = AG.ints(r.agree_words) + AG.ints(r.verb_words) + AG.ints(r.obj_words) + AG.ints(r.subj_words) + [int(r.ne_word)]
            if max(idx) >= n or min(idx) < 0:
                raise SystemExit(f"{r.order_id}: a class index falls outside the sentence")
            if [w for w in range(n) if wc_words[w] != wf_words[w]] != AG.ints(r.agree_words):
                raise SystemExit(f"{r.order_id}: the sentences differ outside the agree class")
            if not (np.all(np.isfinite(c[0])) and np.all(np.isfinite(f[0]))):
                raise SystemExit(f"{r.order_id}: a non-finite surprisal")
            wc = AG.word_class(r)
            parts = dict.fromkeys(CLASSES, 0.0)
            for w, (sc, sf) in enumerate(zip(c[0], f[0])):
                parts[CLASSES[wc(w) - 1]] += sf - sc
            A = float(np.sum(f[0]) - np.sum(c[0]))
            worst_sum = max(worst_sum, abs(sum(parts.values()) - A))
            b = base.loc[(r.ref_id, r.order_id)]
            A_base = float(b.sum_foil - b.sum_correct)
            if not np.isfinite(A_base):
                raise SystemExit(f"{r.order_id}: the stored baseline margin is not finite")
            worst_base = max(worst_base, abs(A - A_base))
            rows.append({"ref_id": r.ref_id, "order_id": r.order_id, "clause_head": r.clause_head,
                         "object_verb_gap": r.object_verb_gap, "order_class": r.order_class,
                         "is_reference": r.is_reference, "object_adjacent": r.object_adjacent, "half": r.half,
                         "A": A, "A_base": A_base, **{f"A_{k}": v for k, v in parts.items()}})
            if i % 200 == 0:
                print(f"    {i}/{len(o)}", flush=True)
        d = pd.DataFrame(rows)
        k = AG.MODEL_INDEX[args.model]
        log.kv("orders", f"{len(d):,} of {len(o):,}")
        log.kv("check: classes sum to A, worst order (bits)", f"{worst_sum:.2e}")
        log.kv("check: A against the stored baseline sums, worst order (bits)", f"{worst_base:.2e}")
        if worst_sum > 1e-3 or worst_base > 1e-2:
            raise SystemExit("the split does not add up to the baseline's margin")
        nb, eb, pb = AG.contrast_test(d, "A_base", [707, k])
        log.kv("check: the stored baseline margin's contrast on these orders, clauses / bits / p", f"{nb} / {eb:+.4f} / {pb:.4g}")
        if not args.limit:
            want = {"muril": -1.7468, "xlmrlarge": -0.2120}[args.model]
            if len(d) != len(o):
                raise SystemExit("some orders could not be scored: the cells would differ from the baseline's")
            if nb != 102 or abs(eb - want) > 1e-3:
                raise SystemExit("the stored margin's contrast does not reproduce the baseline on these orders")
        out = M.OUT / f"decompose_{args.model}.csv"
        d.to_csv(out, index=False)
        log.output(str(out), "per order: the whole-sentence margin A, the stored baseline margin, and A's parts by word class")
        tab = []
        for col in ["A"] + [f"A_{c}" for c in CLASSES]:
            n, eff, p = AG.contrast_test(d, col, [707, k])
            tab.append([col, float(d[col].mean()), n, eff, p])
        log.table(["part of A", "mean over orders (bits)", "clauses", "OSV minus SOV, gap-matched (bits)",
                   "sign-flip p"], tab, floatfmt="{:.4g}")
        log.p("A's row reproduces the baseline contrast (seed [707, model index], as baseline_check.py); the class rows "
              "add up to it within each clause. A class whose contrast carries the effect is where the intervening "
              "subject changes the scores; agree is the verb's own forms.")


if __name__ == "__main__":
    main()
