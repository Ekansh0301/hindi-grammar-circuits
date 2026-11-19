#!/usr/bin/env python3
"""Why does a model's output lose what a late layer has? Mean-ablation of the last blocks (EXTENSION_RESEARCH I3).

M4 found that mBERT's layer 10 predicts the attested order better than its output, under both the tuned and
the Jacobian lens (rq1_layer_vs_output.md). A lens reads; this intervenes. Declared before any run (2 Oct 2026):

  ablation     mean-ablation (Zhang and Nanda 2024: closer to the data distribution than zeroing): a sublayer's
               output, the attention block's output projection (attention.output.dense) or the MLP's
               (output.dense), is replaced at every position by its mean over every position of --n-mean
               IndicCorp sentences read unmasked (the tuned and Jacobian lenses' pool, never the 500
               readability sentences), before the residual addition and LayerNorm
  conditions   none; for each block in --blocks (1-based, e.g. 11 12): its attention alone, its MLP alone, the
               whole block; and all listed blocks together
  rescoring    every RQ1 pair through the model's real MLM head, within_word_l2r, as T is scored; written as
               t_<tag>ab<k>_s<shard>.csv with t_<tag>ab<k>_Mean, for rq1_four_block.py; k indexes the
               conditions, listed in the record
  readability  each ablated model's mean surprisal per subtoken on the 500 held-out sentences (seed 707, as
               every lens's readability); a condition is READ only if it is within 2 nats of the unablated
               model, the declared rule, so that a model degraded into fitting better is not counted
  check        the unablated condition must reproduce the published sums (ref_Sum, var_Sum) to 0.01 bits
               (float noise on this path reaches 3.4e-3 for XLM-R-large, rq1_verb_blind; raised from 1e-3 on
               review, 2 Oct; the mBERT run in progress passed at 5.7e-14)
  measure      mean surprisal over whitespace words, the same in every condition; the published T averages
               over tokenizer words, so the unablated condition, not the published T, is the baseline
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
from hutb_corpus import BASE, load_trees, text_of
from pll_scorer import load_masked_lm
from runlog import RunLog


def encoder_layers(model):
    base = model.base_model
    return base.encoder.layer


def sublayers(model, block):
    layer = encoder_layers(model)[block - 1]
    return {"attn": layer.attention.output.dense, "mlp": layer.output.dense}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True, help="no underscore")
    ap.add_argument("--blocks", nargs="+", type=int, required=True, help="1-based encoder blocks, e.g. 11 12")
    ap.add_argument("--conditions", nargs="+", type=int, default=None, help="indices to run (default all)")
    ap.add_argument("--sentences", default="data/heldout_text/readability_sentences.txt")
    ap.add_argument("--n-mean", type=int, default=300)
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--batch-size", type=int, default=24)
    ap.add_argument("--out-dir", default=str(rc / "late_ablation"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if "_" in args.tag:
        raise SystemExit("the tag must not contain an underscore")
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tag = args.record_tag or f"rq1_late_ablation_{args.tag}"
    with RunLog(tag, __file__, args, purpose="Mean-ablation of late sublayers, rescored and gated by readability.") as log:
        model, tok, device = load_masked_lm(args.model)
        model.eval()
        conds = [("none", [])]
        for b in args.blocks:
            conds += [(f"block {b} attention", [(b, "attn")]), (f"block {b} MLP", [(b, "mlp")]),
                      (f"block {b} whole", [(b, "attn"), (b, "mlp")])]
        if len(args.blocks) > 1:
            conds.append(("all listed blocks", [(b, s) for b in args.blocks for s in ("attn", "mlp")]))
        log.table(["k", "condition"], [[k, c[0]] for k, c in enumerate(conds)])
        run = args.conditions if args.conditions is not None else list(range(len(conds)))

        lines = [l.strip() for l in open(args.sentences, encoding="utf-8") if 8 <= len(l.split()) <= 40]
        rng = np.random.default_rng(707)
        held_idx = set(rng.choice(len(lines), size=min(500, len(lines)), replace=False).tolist())
        held = [lines[i] for i in sorted(held_idx)]
        pool = [l for i, l in enumerate(lines) if i not in held_idx]
        est = [pool[i] for i in np.random.default_rng(708).permutation(len(pool))[:args.n_mean]]

        # means of every sublayer output that any condition ablates, over all positions of the estimation set
        targets = sorted({x for _, c in conds for x in c})
        sums = {t: None for t in targets}
        count = 0
        hooks = []

        def collector(t):
            def f(mod, inp, outp):
                nonlocal count
                v = outp.detach().double().sum(dim=(0, 1)).cpu()
                sums[t] = v if sums[t] is None else sums[t] + v
            return f
        for t in targets:
            hooks.append(sublayers(model, t[0])[t[1]].register_forward_hook(collector(t)))
        with torch.no_grad():
            for text in est:
                ids = tok(text, return_tensors="pt", truncation=True, max_length=256)["input_ids"].to(device)
                model(input_ids=ids)
                count += ids.shape[1]
        for h in hooks:
            h.remove()
        means = {t: (sums[t] / count).float().to(device) for t in targets}
        log.kv("mean-estimation sentences / positions", f"{len(est):,} / {count:,}")

        def ablate(spec):
            hs = []
            for t in spec:
                m = means[t]
                hs.append(sublayers(model, t[0])[t[1]].register_forward_hook(lambda mod, inp, outp, m=m: m.expand_as(outp)))
            return hs

        def readability():
            tot, nsub = 0.0, 0
            for text in held:
                a = U.score_words(model, tok, device, text, args.batch_size, layers=False)
                if a is None:
                    continue
                tot += float(np.sum(a[0])) * np.log(2)
                nsub += sum(a[1])
            return tot / nsub

        refs, vars_ = load_trees()
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]]
        if args.limit:
            pairs = pairs.head(args.limit)
        pub = pd.concat(pd.read_csv(f) for f in glob.glob(str(rc / f"t_{args.tag}_within_word_l2r_s*.csv")))
        pub = pub.set_index(["ref_id", "var_id"])[["ref_Sum", "var_Sum"]]
        base_read = None
        summary = []
        for k in run:
            name, spec = conds[k]
            hs = ablate(spec)
            try:
                with torch.no_grad():
                    rd = readability()
                    rows, dev = [], 0.0
                    for r in pairs.itertuples():
                        rt, vt = text_of(refs[r.ref_id], True), text_of(vars_[r.var_id], False)
                        a = U.score_words(model, tok, device, rt, args.batch_size, layers=False)
                        b = U.score_words(model, tok, device, vt, args.batch_size, layers=False)
                        if a is None or b is None:
                            continue
                        rs, vs = float(np.sum(a[0])), float(np.sum(b[0]))
                        if k == 0 and (r.ref_id, r.var_id) in pub.index:
                            p = pub.loc[(r.ref_id, r.var_id)]
                            dev = max(dev, abs(rs - p.ref_Sum), abs(vs - p.var_Sum))
                        rows.append({"ref_id": r.ref_id, "var_id": r.var_id, "ref_Mean": float(np.mean(a[0])),
                                     "var_Mean": float(np.mean(b[0]))})
            finally:
                for h in hs:
                    h.remove()
            if k == 0:
                base_read = rd
                log.kv("unablated: largest departure from the published sums (bits)", f"{dev:.2e}")
                if dev > 1e-2:
                    raise SystemExit("the unablated model does not reproduce the published sums")
            d = pd.DataFrame(rows)
            col = f"t_{args.tag}ab{k}_Mean"
            d[col] = d.ref_Mean - d.var_Mean
            f = out / f"t_{args.tag}ab{k}_s0.csv"
            d[["ref_id", "var_id", "ref_Mean", "var_Mean", col]].to_csv(f, index=False)
            log.output(str(f), f"condition {k}: {name}")
            summary.append([k, name, rd, len(d), float((d[col] < 0).mean())])
            print(f"    condition {k} ({name}) done", flush=True)
        if base_read is not None:
            for row in summary:
                row.insert(3, row[2] - base_read)
                row.insert(4, "yes" if row[3] <= 2 else "no")
            log.table(["k", "condition", "held-out nats per subtoken", "minus unablated", "READ (within 2 nats)",
                       "pairs", "reference preferred"], summary, floatfmt="{:.4f}")
        else:
            log.table(["k", "condition", "held-out nats per subtoken", "pairs", "reference preferred"], summary,
                      floatfmt="{:.4f}")
            log.p("The unablated condition is not in this run, so the readability rule is applied when the runs are joined.")


if __name__ == "__main__":
    main()
