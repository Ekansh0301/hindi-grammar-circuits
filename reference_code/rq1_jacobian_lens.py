#!/usr/bin/env python3
"""Jacobian lens for masked LMs (RQ1_WORK_PLAN.md M4), the arbiter between the logit and the tuned lens.

The Jacobian lens (Anthropic, July 2026) reads a layer's state h_l through the model's own average local
map to the output: J_l = E[d h_final / d h_l], and lens(h_l) = softmax(W_U norm(J_l h_l)). The logit lens
is the special case J_l = I. Unlike the tuned lens, nothing is trained to reproduce the output
distribution, so a layer cannot look good by having been fitted to the answer, which is the reason the
two lenses' disagreement over mBERT's layer 10 (REPORT.md 3.11) needs this one to settle it.

The published lens is defined for autoregressive models, averaging over source position t and every later
position t' >= t. A masked LM reads a word's surprisal at the masked position itself, so the masked
analogue used here is the SAME-position Jacobian at masked positions:

    J_l = mean over masked positions t of  d h_final[t] / d h_l[t]

estimated with within_word_l2r masking exactly as scoring masks, on IndicCorp sentences (HDTB removed)
from the tuned lens's own training pool, never the 500 held out for readability. The readout applies the
model's MLM head to J_l h_l, so "norm" and W_U are the head's own transform and decoder. One backward pass
per output dimension gives that row of the summed Jacobian for every layer at once.

The readout is the first-order expansion around the MEAN state, not around zero:

    h_final  ~  mu_final + J_l (h_l - mu_l)

with mu_l and mu_final the mean states at the same masked positions. The published lens is linear
(J_l h_l) because the models it was built for are pre-LayerNorm, where the output norm makes the scale of
J_l h_l irrelevant. These four encoders are post-LayerNorm, and their MLM head applies a dense layer, a
bias and a GELU BEFORE its LayerNorm, so J_l h_l, which is small, is read almost entirely as the head's
bias: in a 20-sentence smoke test on MuRIL the linear readout was flat across depth and far from the
final layer, while the expansion around the mean improved monotonically with depth. The choice was made
on that smoke test, before any full run, and it is not a tuning: the expansion around the mean is the
first-order approximation of the same map at the point the data sit, where the linear readout expands
around zero, which no post-LayerNorm state is near. It is still fitted to nothing (the means are
averages, not trained). The linear readout's readability is kept in every record beside it, so the
choice is shown, not asserted.

Written for rq1_lm_units.py --tuned-lens, which applies translators of the form h + W h + b: here
W = J_l - I and b = mu_final - J_l mu_l, so the translator is exactly h -> mu_final + J_l (h - mu_l). Then
readability on the 500 held-out sentences under the declared 2-nat rule, as for the other two lenses.

Checks: a split-half estimate (the mean over two disjoint halves of the positions) and its relative
difference per layer, so the average is shown to be stable rather than assumed; the translated final layer
is the identity by construction and is not estimated.
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
    ap.add_argument("--n-sentences", type=int, default=1000, help="estimation sentences, as in the published lens")
    ap.add_argument("--per-sentence", type=int, default=2, help="masked positions drawn per sentence")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-dir", default=str(BASE / "Results_Checks" / "lm_units"))
    args = ap.parse_args()
    out = Path(args.out_dir)
    with RunLog(f"rq1_jacobian_lens_{args.tag}", __file__, args,
                purpose="Jacobian-lens translators (masked analogue) and their readability.") as log:
        torch.manual_seed(707)
        model, tok, device = load_masked_lm(args.model)
        model.eval()                                     # dropout off; parameters keep requires_grad so a
        L = model.config.num_hidden_layers + 1           # graph is built through the hidden states
        d = model.config.hidden_size
        head = U.mlm_head(model)
        lines = [l.strip() for l in open(args.sentences, encoding="utf-8") if 8 <= len(l.split()) <= 40]
        rng = np.random.default_rng(707)
        held_idx = set(rng.choice(len(lines), size=min(500, len(lines)), replace=False).tolist())   # as in readability
        held = [lines[i] for i in sorted(held_idx)]
        pool = [l for i, l in enumerate(lines) if i not in held_idx]
        est = [pool[i] for i in np.random.default_rng(708).permutation(len(pool))[:args.n_sentences]]
        log.kv("estimation sentences / held-out sentences", f"{len(est):,} / {len(held):,}")

        # the masked positions: within_word_l2r passes, a few per sentence
        prng = np.random.default_rng(709)
        jobs = []
        for text in est:
            g = U.whitespace_groups(tok, text)
            if g is None or len(g[0]) > 256:
                continue
            ids, groups, _, _ = g
            passes = U._l2r_passes(groups)
            for j in prng.choice(len(passes), size=min(args.per_sentence, len(passes)), replace=False):
                mask_pos, p, _ = passes[j]
                jobs.append((ids, mask_pos, p))
        log.kv("masked positions", f"{len(jobs):,}")

        halves = [[torch.zeros(d, d, dtype=torch.float64) for _ in range(L - 1)] for _ in range(2)]
        mu = torch.zeros(L, d, dtype=torch.float64)      # summed states at the masked positions, every layer
        counts = [0, 0]
        for b0 in range(0, len(jobs), args.batch_size):
            chunk = jobs[b0:b0 + args.batch_size]
            n = max(len(c[0]) for c in chunk)
            pad = tok.pad_token_id if tok.pad_token_id is not None else 0
            x = torch.full((len(chunk), n), pad, dtype=torch.long)
            att = torch.zeros((len(chunk), n), dtype=torch.long)
            for r, (ids, mask_pos, _) in enumerate(chunk):
                x[r, :len(ids)] = torch.tensor(ids)
                att[r, :len(ids)] = 1
                x[r, mask_pos] = tok.mask_token_id
            x, att = x.to(device), att.to(device)
            pos = torch.tensor([c[2] for c in chunk], device=device)
            rows = torch.arange(len(chunk), device=device)
            with torch.enable_grad():
                o = model(input_ids=x, attention_mask=att, output_hidden_states=True)
                hs = o.hidden_states
                fin = hs[-1][rows, pos]                                  # (B, d)
                acc = [torch.zeros(d, d, dtype=torch.float64, device=device) for _ in range(L - 1)]
                for i in range(d):
                    g = torch.autograd.grad(fin[:, i].sum(), hs[:-1], retain_graph=i < d - 1)
                    for l in range(L - 1):
                        acc[l][i] += g[l][rows, pos].sum(0).double()     # row i: d fin_i / d h_l
            half = (b0 // args.batch_size) % 2
            for l in range(L - 1):
                halves[half][l] += acc[l].cpu()
            for l in range(L):
                mu[l] += hs[l][rows, pos].detach().double().sum(0).cpu()
            counts[half] += len(chunk)
            print(f"    {min(b0 + args.batch_size, len(jobs)):,}/{len(jobs):,} positions", flush=True)
            del o, hs, fin, acc

        J = [(halves[0][l] + halves[1][l]) / sum(counts) for l in range(L - 1)]
        rows_ = []
        eye = torch.eye(d, dtype=torch.float64)
        for l in range(L - 1):
            a, b = halves[0][l] / counts[0], halves[1][l] / counts[1]
            rows_.append([l, float(torch.linalg.norm(J[l] - eye) / torch.linalg.norm(eye)),
                          float(torch.linalg.norm(a - b) / torch.linalg.norm(J[l]))])
        log.h2("The averaged Jacobians")
        log.table(["layer", "‖J − I‖ / ‖I‖ (distance from the logit lens)", "split-half ‖J₁ − J₂‖ / ‖J‖"],
                  rows_, floatfmt="{:.4f}")
        log.p(f"Positions split into alternating batches, {counts[0]:,} and {counts[1]:,}. A split-half "
              "difference small against 1 means the average is a property of the layer, not of the sample.")

        mu = mu / sum(counts)

        def translators(affine):
            tr = torch.nn.ModuleList([U.Translator(d) for _ in range(L - 1)]).to(device)
            with torch.no_grad():
                for l in range(L - 1):
                    tr[l].lin.weight.copy_((J[l] - eye).float())         # h + (J - I) h = J h
                    b = (mu[-1] - J[l] @ mu[l]) if affine else torch.zeros(d, dtype=torch.float64)
                    tr[l].lin.bias.copy_(b.float())                      # + mu_final - J mu_l
            return tr.eval()
        tr, tr_lin = translators(True), translators(False)

        tot_j, tot_lin, tot_l, nsub = np.zeros(L), np.zeros(L), np.zeros(L), 0
        with torch.no_grad():
            for text in held:
                a = U.score_words(model, tok, device, text, args.batch_size, layers=True)
                b = U.score_words(model, tok, device, text, args.batch_size, layers=True, translators=tr)
                c = U.score_words(model, tok, device, text, args.batch_size, layers=True, translators=tr_lin)
                if a is None or b is None or c is None:
                    continue
                tot_l += np.array(a[2]).sum(0) * np.log(2)
                tot_j += np.array(b[2]).sum(0) * np.log(2)
                tot_lin += np.array(c[2]).sum(0) * np.log(2)
                nsub += sum(a[1])
        lo, ja, jl = tot_l / nsub, tot_j / nsub, tot_lin / nsub
        if abs(ja[-1] - lo[-1]) > 1e-6 or abs(jl[-1] - lo[-1]) > 1e-6:
            raise SystemExit("the final layer differs between the lenses; it must be untranslated")
        rr = [[l, lo[l], jl[l], ja[l], ja[l] - ja[-1], "yes" if ja[l] - ja[-1] <= 2 else "no"] for l in range(L)]
        log.h2("Readability on the 500 held-out sentences (declared rule: within 2 nats per subtoken of the final layer)")
        log.table(["layer", "logit lens nats/subtoken", "Jacobian, linear (diagnostic)",
                   "Jacobian lens, around the mean", "Jacobian minus final", "readable (Jacobian)"],
                  rr, floatfmt="{:.3f}")
        rpath = out / f"readability_{args.tag}_jacobian.csv"
        pd.DataFrame([[r[0], r[3], r[4], r[5]] for r in rr],
                     columns=["layer", "nats_per_subtoken", "minus_final", "readable"]).to_csv(rpath, index=False)
        path = out / f"jacobian_lens_{args.tag}.pt"
        torch.save(tr.state_dict(), path)
        log.output(str(rpath), "Jacobian-lens readability per layer")
        log.output(str(path), "translators h -> mu_final + J_l (h - mu_l), for rq1_lm_units.py --tuned-lens")


if __name__ == "__main__":
    main()
