#!/usr/bin/env python3
"""Tuned lens for masked LMs (PREREGISTRATION_DRAFT.md 7.2, tier 2; RQ1_WORK_PLAN.md F4).

Training data: readability_sentences.txt (IndicCorp sample, HDTB removed), sentences of 8 to 40 words,
EXCLUDING the 500 drawn (seed 707) for the logit-lens readability check; up to --n-train of the rest.
Passes follow within_word_l2r exactly as scoring does. For every layer except the last, a translator
h + W h + b (zero-initialised) is trained to minimise KL(final distribution || MLM head applied to the
translated state) at the scored positions; Adam, lr 1e-4, --epochs passes over the data, seed 707; each
layer's translator is trained independently.

Then: tuned-lens readability on the same 500 held-out sentences (nats per subtoken, readable within 2
nats of the final layer), written as readability_<tag>_tuned.csv, and the translators saved to
tuned_lens_<tag>.pt for rq1_lm_units.py --what words --tuned-lens.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
from hutb_corpus import BASE
from pll_scorer import load_masked_lm
from runlog import RunLog


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--sentences", default="data/heldout_text/readability_sentences.txt")
    ap.add_argument("--n-train", type=int, default=3000)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-dir", default=str(BASE / "Results_Checks" / "lm_units"))
    args = ap.parse_args()
    out = Path(args.out_dir)
    with RunLog(f"rq1_tuned_lens_{args.tag}", __file__, args, purpose="Tuned-lens translators and their readability.") as log:
        torch.manual_seed(707)
        model, tok, device = load_masked_lm(args.model)
        for p in model.parameters():
            p.requires_grad_(False)
        L = model.config.num_hidden_layers + 1
        d = model.config.hidden_size
        head = U.mlm_head(model)
        lines = [l.strip() for l in open(args.sentences, encoding="utf-8") if 8 <= len(l.split()) <= 40]
        rng = np.random.default_rng(707)
        held_idx = set(rng.choice(len(lines), size=min(500, len(lines)), replace=False).tolist())   # as in readability
        held = [lines[i] for i in sorted(held_idx)]
        pool = [l for i, l in enumerate(lines) if i not in held_idx]
        train = [pool[i] for i in np.random.default_rng(708).permutation(len(pool))[:args.n_train]]
        log.kv("training sentences / held-out sentences", f"{len(train):,} / {len(held):,}")

        tr = torch.nn.ModuleList([U.Translator(d) for _ in range(L - 1)]).to(device)
        opt = torch.optim.Adam(tr.parameters(), lr=1e-4)

        def batches(texts):
            for text in texts:
                g = U.whitespace_groups(tok, text)
                if g is None or len(g[0]) > 256:
                    continue
                ids, groups, _, _ = g
                passes = U._l2r_passes(groups)
                for s in range(0, len(passes), args.batch_size):
                    chunk = passes[s:s + args.batch_size]
                    x = torch.tensor([ids], device=device).repeat(len(chunk), 1)
                    for r, (mask_pos, _, _) in enumerate(chunk):
                        x[r, mask_pos] = tok.mask_token_id
                    yield x, torch.tensor([p for _, p, _ in chunk], device=device), \
                        torch.tensor([ids[p] for _, p, _ in chunk], device=device)

        losses = []
        for ep in range(args.epochs):
            tot, n = np.zeros(L - 1), 0
            for x, pos, _ in batches(train):
                with torch.no_grad():
                    o = model(input_ids=x, attention_mask=torch.ones_like(x), output_hidden_states=True)
                    rows = torch.arange(len(pos), device=device)
                    target = torch.log_softmax(o.logits[rows, pos].float(), -1)
                    hs = [h[rows, pos].float() for h in o.hidden_states[:-1]]
                opt.zero_grad()
                for li in range(L - 1):
                    lp = torch.log_softmax(head(tr[li](hs[li])).float(), -1)
                    kl = torch.nn.functional.kl_div(lp, target, log_target=True, reduction="batchmean")
                    kl.backward()
                    tot[li] += kl.item()
                opt.step()
                n += 1
            losses.append(tot / max(n, 1))
            print(f"    epoch {ep}: mean KL by layer {np.round(tot / max(n, 1), 3).tolist()}", flush=True)
        log.table(["epoch"] + [str(i) for i in range(L - 1)], [[e] + list(l) for e, l in enumerate(losses)], floatfmt="{:.3f}")

        tot_t, tot_l, nsub = np.zeros(L), np.zeros(L), 0
        tr.eval()
        with torch.no_grad():
            for text in held:
                a = U.score_words(model, tok, device, text, args.batch_size, layers=True)
                b = U.score_words(model, tok, device, text, args.batch_size, layers=True, translators=tr)
                if a is None or b is None:
                    continue
                tot_l += np.array(a[2]).sum(0) * np.log(2)
                tot_t += np.array(b[2]).sum(0) * np.log(2)
                nsub += sum(a[1])
        lo, tu = tot_l / nsub, tot_t / nsub
        rows = [[l, lo[l], tu[l], tu[l] - tu[-1], "yes" if tu[l] - tu[-1] <= 2 else "no"] for l in range(L)]
        log.table(["layer", "logit lens nats/subtoken", "tuned lens nats/subtoken", "tuned minus final", "readable (tuned)"],
                  rows, floatfmt="{:.3f}")
        pd.DataFrame([[r[0], r[2], r[3], r[4]] for r in rows], columns=["layer", "nats_per_subtoken", "minus_final", "readable"]).to_csv(
            out / f"readability_{args.tag}_tuned.csv", index=False)
        path = out / f"tuned_lens_{args.tag}.pt"
        torch.save(tr.state_dict(), path)
        log.output(str(path), "translator weights")


if __name__ == "__main__":
    main()
