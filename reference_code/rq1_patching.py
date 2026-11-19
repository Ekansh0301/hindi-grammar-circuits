#!/usr/bin/env python3
"""Where is the order preference computed? Interchange patching of the moved constituents (EXTENSION I1).

A reference and its variant contain the same words, so states can be moved between their runs word for word.
Declared before any run (2 Oct 2026):

  pairs       a fixed subsample of the RQ1 pairs (--n-pairs, seed 707)
  passes      the variant is scored as T is (within_word_l2r: for each subtoken position, that position and
              the later positions of its word masked); for every such pass the CLEAN run is the reference with
              the same word masked the same way, so the two runs differ only in order
  patch       at layer l (hidden-state index; 0 is the embedding output), the states of one SITE's subtokens in
              the variant run are replaced by the clean run's states of the same subtokens (aligned by word and
              subtoken), and the variant's masked position is then read out as usual
  sites       moved_heads    the head word (order_model.representative) of every unit whose position changes
              moved_psp      the postpositions of those units
              moved_other    every other word of those units (modifiers, dependents)
              verb           the clause's verb complex (head plus the subtrees of its lwg* / pof*
                             dependents, the generator's R2 span)
              unmoved        every word outside the moved units and the verb complex
              all            every word (layer 0 only: the built-in check)
  recovery    with S(x) the mean per-word surprisal of sentence x and S*(var) the patched variant's, the share of
              the gap closed: (S(var) - S*(var)) / (S(var) - S(ref)), aggregated as a ratio of sums over pairs
              whose gap exceeds --min-gap bits in either direction (signed, so a patch that widens the gap
              counts negative)
  check       'all' at layer 0 must recover 1 to within 1e-3: with learned absolute positions the patched
              states are the reference's states in another order, which attention cannot tell apart
  layers      --layers (default every other hidden-state index)
  direction   --direction denoising (the default, every earlier run): the variant is the BASE run and the reference
              the CLEAN one, so a patch restores the reference. --direction noising (added 4 Oct, the declared
              follow-up now that denoising was informative): the reference is the base and the variant the clean
              run, so a patch of the variant's states into the reference run asks whether that site is enough to
              carry the variant's dispreference in. Both use one formula, the share of the gap moved:
              (S*(base) - S(base)) / (S(clean) - S(base)), a ratio of sums over pairs with |gap| > --min-gap;
              for denoising it is the recovery defined above. The check is the same in both: 'all' at layer 0
              must move the whole gap, to within 1e-3, worst pair 5e-3 bits
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
import order_model as O
import set1_generator as G
from hutb_corpus import BASE, load_trees, set1_variants, text_of
from materialise_set1 import official_tokens
from pll_scorer import load_masked_lm
from runlog import RunLog

SITES = ["moved_heads", "moved_psp", "moved_other", "verb", "unmoved"]


def word_subtokens(tok, text):
    g = U.whitespace_groups(tok, text)
    if g is None:
        return None
    ids, groups, gw, nw = g
    by_word = [[] for _ in range(nw)]
    for k, pos in enumerate(groups):
        by_word[gw[k]].extend(pos)
    return ids, groups, gw, by_word


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--n-pairs", type=int, default=1000)
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-dir", default=str(rc / "patching"))
    ap.add_argument("--record-tag", default=None)
    ap.add_argument("--direction", default="denoising", choices=["denoising", "noising"])
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.direction == "denoising" else "_noising"
    with RunLog(args.record_tag or f"rq1_patching_{args.tag}{suffix}", __file__, args,
                purpose=("Interchange patching of reference states into the variant run" if args.direction == "denoising"
                         else "Interchange patching of variant states into the reference run (noising)")
                + ", by site and layer.") as log:
        model, tok, device = load_masked_lm(args.model)
        model.eval()
        n_hidden = model.config.num_hidden_layers + 1
        layers = args.layers if args.layers is not None else list(range(0, n_hidden, 2))
        conds = [("all", 0)] + [(s, l) for l in layers for s in SITES]
        log.kv("layers / conditions", f"{', '.join(map(str, layers))} / {len(conds)}")
        enc_layers = model.base_model.encoder.layer
        emb = model.base_model.embeddings

        refs, vars_ = load_trees()
        vt = set1_variants().set_index("var_id")
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]]
        pick = pairs.iloc[np.sort(np.random.default_rng(707).choice(len(pairs), size=min(args.n_pairs, len(pairs)), replace=False))]

        def module_for(layer):
            return emb if layer == 0 else enc_layers[layer - 1]

        rows, skipped = [], 0
        for n, r in enumerate(pick.itertuples(), 1):
            rt, vtr = refs[r.ref_id], vars_[r.var_id]
            v = vt.loc[r.var_id]
            rtext, vtext = text_of(rt, True), text_of(vtr, False)
            ridx, vidx = U.set1_surface_indices(rt, v.to_dict() | {"var_id": r.var_id}, vtr)
            A, B = word_subtokens(tok, rtext), word_subtokens(tok, vtext)
            if A is None or B is None or len(A[0]) > 256 or len(B[0]) > 256:
                skipped += 1
                continue
            # base run (patched) and clean run (source of the states): denoising patches the reference into the
            # variant, noising the variant into the reference
            if args.direction == "denoising":
                (c_ids, _, _, c_words), (v_ids, v_groups, v_gw, v_words) = A, B
                cidx, bidx = ridx, vidx
            else:
                (c_ids, _, _, c_words), (v_ids, v_groups, v_gw, v_words) = B, A
                cidx, bidx = vidx, ridx
            r_ids, r_words = c_ids, c_words
            r_pos_of = {t: k for k, t in enumerate(cidx)}
            # subtoken alignment base -> clean, word by word (same tree token, same word)
            align = {}
            ok = True
            for vk, t in enumerate(bidx):
                a, b = r_words[r_pos_of[t]], v_words[vk]
                if len(a) != len(b):
                    ok = False
                    break
                align.update(dict(zip(b, a)))
            if not ok:
                skipped += 1
                continue
            # sites, as sets of variant word positions
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
            site_words["unmoved"] = set(bidx) - moved_words - verb
            site_words["all"] = set(bidx)
            site_tok = {s: [p for vk, t in enumerate(bidx) if t in ws for p in v_words[vk]] for s, ws in site_words.items()}

            passes = U._l2r_passes(v_groups)
            r_base = torch.tensor([r_ids], device=device)
            v_base = torch.tensor([v_ids], device=device)

            # clean states: for each variant pass, the reference with the same word masked, every layer
            clean = []
            with torch.no_grad():
                for s0 in range(0, len(passes), args.batch_size):
                    chunk = passes[s0:s0 + args.batch_size]
                    x = r_base.repeat(len(chunk), 1)
                    for i, (mpos, _, _) in enumerate(chunk):
                        x[i, [align[p] for p in mpos]] = tok.mask_token_id
                    o = model(input_ids=x, attention_mask=torch.ones_like(x), output_hidden_states=True)
                    clean.append(torch.stack(o.hidden_states, 1))           # (batch, n_hidden, len, d)
                clean = torch.cat(clean, 0)

                def score_variant(site=None, layer=None):
                    per_word = np.zeros(len(v_words))
                    for s0 in range(0, len(passes), args.batch_size):
                        chunk = passes[s0:s0 + args.batch_size]
                        x = v_base.repeat(len(chunk), 1)
                        for i, (mpos, _, _) in enumerate(chunk):
                            x[i, mpos] = tok.mask_token_id
                        hook = None
                        if site is not None:
                            vpos = torch.tensor(site_tok[site], device=device, dtype=torch.long)
                            rpos = torch.tensor([align[p] for p in site_tok[site]], device=device, dtype=torch.long)
                            src = clean[s0:s0 + len(chunk), layer]

                            def f(mod, inp, outp, vpos=vpos, rpos=rpos, src=src):
                                h = outp[0] if isinstance(outp, tuple) else outp
                                h = h.clone()
                                h[:, vpos] = src[:, rpos].to(h.dtype)
                                return (h,) + tuple(outp[1:]) if isinstance(outp, tuple) else h
                            if len(site_tok[site]):
                                hook = module_for(layer).register_forward_hook(f)
                        try:
                            o = model(input_ids=x, attention_mask=torch.ones_like(x))
                        finally:
                            if hook is not None:
                                hook.remove()
                        rows_ = torch.arange(len(chunk), device=device)
                        pos = torch.tensor([p for _, p, _ in chunk], device=device)
                        tgt = torch.tensor([v_ids[p] for _, p, _ in chunk], device=device)
                        lp = torch.log_softmax(o.logits[rows_, pos].float(), -1)
                        vals = (-lp.gather(1, tgt[:, None])[:, 0] / np.log(2)).tolist()
                        for (_, _, k), val in zip(chunk, vals):
                            per_word[v_gw[k]] += val
                    return float(per_word.mean())
                s_base = score_variant()
                ra = U.score_words(model, tok, device, rtext if args.direction == "denoising" else vtext,
                                   args.batch_size, layers=False)
                s_clean = float(np.mean(ra[0]))
                s_ref, s_var = (s_clean, s_base) if args.direction == "denoising" else (s_base, s_clean)
                rec = {"ref_id": r.ref_id, "var_id": r.var_id, "s_ref": s_ref, "s_var": s_var,
                       "s_base": s_base, "s_clean": s_clean,
                       **{f"n_{s}": len(site_tok[s]) for s in SITES}}
                for site, layer in conds:
                    rec[f"{site}@{layer}"] = score_variant(site, layer) if site_tok[site] else s_base
            rows.append(rec)
            if n % 50 == 0:
                print(f"    {n:,}/{len(pick):,} ({skipped} skipped)", flush=True)
        d = pd.DataFrame(rows)
        f = out / f"patching_{args.tag}{suffix}.csv"
        d.to_csv(f, index=False)
        log.output(str(f), "per pair: reference, variant, base and clean runs, and the patched base run per condition")
        gap = d.s_clean - d.s_base
        keep = gap.abs() > args.min_gap
        log.kv("direction", args.direction)
        log.kv("pairs patched / skipped / with a gap above --min-gap", f"{len(d):,} / {skipped:,} / {int(keep.sum()):,}")
        dk, gk = d[keep], gap[keep]
        rec_all = float(((dk["all@0"] - dk.s_base)).sum() / gk.sum())
        per_pair = float((d["all@0"] - d.s_clean).abs().max())
        log.kv("check: 'all' at layer 0 moves the whole gap (ratio of sums) / largest per-pair departure from the clean run (bits)",
               f"{rec_all:.6f} / {per_pair:.2e}")
        if abs(rec_all - 1) > 1e-3 or per_pair > 5e-3:
            raise SystemExit("patching every token at layer 0 does not recover the reference: the alignment is wrong")
        tab = []
        for l in layers:
            tab.append([l] + [float((dk[f"{s}@{l}"] - dk.s_base).sum() / gk.sum()) for s in SITES])
        log.table(["layer"] + [f"{'recovered' if args.direction == 'denoising' else 'moved'} by {s}" for s in SITES],
                  tab, floatfmt="{:.4f}")
        log.p(("Recovery is the share of the variant-reference gap closed by patching reference states into the "
               "variant run" if args.direction == "denoising" else "The share of the reference-variant gap moved by "
               "patching the variant's states into the reference run, toward the variant's surprisal")
              + ", a ratio of sums over pairs; 1 moves the whole gap, 0 none, negative the other way. Site sizes per "
              "pair are in the CSV.")


if __name__ == "__main__":
    main()
