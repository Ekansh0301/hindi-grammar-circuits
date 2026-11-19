#!/usr/bin/env python3
"""Is what the moved head words carry a low-dimensional variable? Distributed alignment search (EXTENSION I4).

I1 (rq1_patching.py) found that putting the reference's states of the moved constituents' head words into the
variant's run recovers 0.50 to 0.60 of the variant's surprisal gap at each model's peak layer, more than any other
site. DAS (Geiger et al. 2024) asks whether that is carried by a low-rank subspace of those states, and if so what
the subspace encodes. Declared before any run (4 Oct 2026):

  layer       I1's peak for the moved head words, as a hidden-state index (0 is the embeddings): MuRIL 8,
              IndicBERT-v2 8, mBERT 10, XLM-R-large 20
  passes      exactly I1's denoising setup: the variant is the BASE run, scored within_word_l2r; for each of its
              passes the CLEAN run is the reference with the same word masked the same way; sites, alignment and
              pair selection are I1's code, copied, and checked against I1's own per-pair output (below)
  intervention at the layer, on the site's subtokens in every base pass: h <- h + (h_clean - h) Q^T Q, with Q a
              k x d matrix of orthonormal rows (torch's orthogonal parametrisation; pyvene's low-rank rotated-space
              intervention is the same map and is not used). k = d is I1's full-state patch
  training    Q is fitted on TRAINING pairs to make the patched base run's output distribution at every masked
              position match the clean run's: the loss is KL(clean || patched) averaged over passes, Adam, --lr,
              --epochs, --pairs-per-step pairs per step, the model frozen. --lr 1e-3 and --epochs 3 were chosen
              on VALIDATION pairs only, by a 300-pair MuRIL pilot of 1e-3 against 1e-2 (logs/das_smoke, 4 Oct): at
              1e-3 rank 1 was still rising after two epochs (0.08, 0.15) where at 1e-2 it had stalled (0.131,
              0.137); rank 16 ended at 0.35 and 0.39; a full run has seven times the steps per epoch. Ranks --ranks (1, 4, 16, 64) at the moved
              head words; ranks --verb-ranks (1, 16) at the verb complex, I1's weakest site (0.11 to 0.16), as the
              site control: a method that finds a strong subspace where the full state carries little is finding
              an interpretability illusion (Makelov et al. 2024), not a variable. After each epoch the share
              recovered on --n-val VALIDATION pairs is computed and the best epoch's Q kept
  pairs       EVALUATION: I1's own 1,000 pairs (same file, same seed 707 draw), so every number compares with I1's.
              TRAINING and VALIDATION: drawn (seed 708) from the remaining sample pairs whose DOCUMENT has no
              evaluation pair, so no document is on both sides
  measure     the share of the gap recovered, I1's: (S(base) - S*(base)) / (S(base) - S(clean)) as a ratio of sums
              over evaluation pairs with |gap| > --min-gap bits; S is mean surprisal per whitespace word
  controls    a random k-dimensional subspace (--random-seeds draws, uniform on the Stiefel manifold) at the same
              site and rank, and the full-state patch (I1's number)
  tests       per site and rank, learned against random (mean over draws), and learned against the full patch: the
              per-pair difference in the amount moved, summed per document, document-level sign-flip permutation
              p (10,000); two-sided
  reading     for rank 1 at the moved head words: the projection v = Q h of each moved head word's state at the
              layer in an UNMASKED run of each sentence, and per pair dv = mean over moved heads of v(reference) -
              v(variant), each head's v the mean over its subtokens. Spearman correlation of dv, over documents (per-document means, permutation p over
              documents, 10,000), with: the model's own preference d_T = S(reference) - S(variant); E1's order-model
              difference d_syn_order; the trigram's d_kenlm_mean; and dpos, the mean change in the moved heads'
              word index (a variable that is only the word's position would track dpos). Q's sign is fixed so that
              dv correlates positively with d_T over pairs. Descriptive: the variable is named only if one of these
              stands out
  checks      (1) S(base) and S(clean) of every evaluation pair equal I1's s_var and s_ref within 5e-3 bits;
              (2) the full-state patch at the moved head words and at the verb equals I1's moved_heads@L and verb@L
              per pair within 5e-3 bits, both before any training (so a setup defect costs minutes) and again in the
              evaluation; (3) every Q has orthonormal rows within 1e-4. Any failure stops the run. Pairs whose site has
              no surface word (the verb site of 55 sample pairs, a NULL clause head) are left out of training and
              validation for that site, and count as unmoved in the evaluation, as in I1
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch
from scipy.stats import spearmanr

import lm_units as U
import order_model as O
import set1_generator as G
from hutb_corpus import BASE, load_trees, set1_variants, text_of
from materialise_set1 import official_tokens
from pll_scorer import load_masked_lm
from runlog import RunLog

LAYER = {"muril": 8, "indicbert": 8, "mbert": 10, "xlmrlarge": 20}
SITES = ["moved_heads", "verb"]
LN2 = float(np.log(2))


def word_subtokens(tok, text):
    g = U.whitespace_groups(tok, text)
    if g is None:
        return None
    ids, groups, gw, nw = g
    by_word = [[] for _ in range(nw)]
    for k, pos in enumerate(groups):
        by_word[gw[k]].extend(pos)
    return ids, groups, gw, by_word


def prepare(r, refs, vars_, vt, tok):
    """I1's denoising setup for one pair (rq1_patching.py, copied): None if it cannot be aligned."""
    rt, vtr = refs[r.ref_id], vars_[r.var_id]
    v = vt.loc[r.var_id]
    rtext, vtext = text_of(rt, True), text_of(vtr, False)
    ridx, vidx = U.set1_surface_indices(rt, v.to_dict() | {"var_id": r.var_id}, vtr)
    A, B = word_subtokens(tok, rtext), word_subtokens(tok, vtext)
    if A is None or B is None or len(A[0]) > 256 or len(B[0]) > 256:
        return None
    (c_ids, _, _, c_words), (v_ids, v_groups, v_gw, v_words) = A, B
    r_pos_of = {t: k for k, t in enumerate(ridx)}
    align = {}
    for vk, t in enumerate(vidx):
        a, b = c_words[r_pos_of[t]], v_words[vk]
        if len(a) != len(b):
            return None
        align.update(dict(zip(b, a)))
    toks = official_tokens(rt)
    by = {t_["idx"]: t_ for t_ in toks}
    kids = G.children(toks)
    head = int(v.clause_head)
    c = O.Clause(toks, head)
    order = [int(x) for x in str(v.order).split("|")]
    moved_units = [c.units[u] for k, u in enumerate(order) if u != k and c.surface[u]]
    moved_heads = {O.representative(by, kids, d) for d in moved_units}
    verb = {head} | {i for k_ in kids.get(head, []) if G.is_verb_complex_rel(by[k_]["deprel"])
                     for i in G.subtree(kids, k_)}
    site_words = {"moved_heads": moved_heads, "verb": verb}
    site_tok = {s: [p for vk, t in enumerate(vidx) if t in ws for p in v_words[vk]] for s, ws in site_words.items()}
    heads_ref = [r_pos_of[t] for t in sorted(moved_heads) if t in r_pos_of]
    v_pos_of = {t: k for k, t in enumerate(vidx)}
    heads_var = [v_pos_of[t] for t in sorted(moved_heads) if t in v_pos_of]
    return {"ref_id": r.ref_id, "var_id": r.var_id, "c_ids": c_ids, "v_ids": v_ids, "v_gw": v_gw,
            "n_words": len(v_words), "align": align, "passes": U._l2r_passes(v_groups), "site_tok": site_tok,
            "c_words": c_words, "v_words": v_words, "heads_ref": heads_ref, "heads_var": heads_var}


class Runner:
    def __init__(self, model, tok, device, layer, batch_size):
        self.model, self.tok, self.device, self.bs = model, tok, device, batch_size
        self.mod = model.base_model.encoder.layer[layer - 1]

    def _inputs(self, P, chunk, clean):
        base = torch.tensor([P["c_ids"] if clean else P["v_ids"]], device=self.device)
        x = base.repeat(len(chunk), 1)
        for i, (mpos, _, _) in enumerate(chunk):
            x[i, [P["align"][p] for p in mpos] if clean else mpos] = self.tok.mask_token_id
        return x

    def _readout(self, P, chunk, logits, clean):
        rows = torch.arange(len(chunk), device=self.device)
        ids = P["c_ids"] if clean else P["v_ids"]
        pos = torch.tensor([P["align"][p] if clean else p for _, p, _ in chunk], device=self.device)
        tgt = torch.tensor([ids[P["align"][p]] if clean else ids[p] for _, p, _ in chunk], device=self.device)
        lp = torch.log_softmax(logits[rows, pos].float(), -1)
        return lp, -lp.gather(1, tgt[:, None])[:, 0] / LN2

    def clean_chunk(self, P, chunk, want_lp):
        """The clean run's layer states (whole sequence) and, if asked, its log-probabilities at the masked position."""
        got = {}

        def f(mod, inp, outp):
            got["h"] = (outp[0] if isinstance(outp, tuple) else outp).detach()
        hook = self.mod.register_forward_hook(f)
        try:
            with torch.no_grad():
                x = self._inputs(P, chunk, True)
                o = self.model(input_ids=x, attention_mask=torch.ones_like(x))
        finally:
            hook.remove()
        lp, s = self._readout(P, chunk, o.logits, True)
        return got["h"], (lp if want_lp else None), s

    def base_chunk(self, P, chunk, src, site, Q):
        """The base run with the site patched: Q None = no patch, Q 'full' = whole state, else a k x d tensor."""
        hook = None
        if Q is not None and P["site_tok"][site]:
            vpos = torch.tensor(P["site_tok"][site], device=self.device, dtype=torch.long)
            rpos = torch.tensor([P["align"][p] for p in P["site_tok"][site]], device=self.device, dtype=torch.long)
            s_ = src[:, rpos]

            def f(mod, inp, outp):
                h = outp[0] if isinstance(outp, tuple) else outp
                h = h.clone()
                if isinstance(Q, str):
                    h[:, vpos] = s_.to(h.dtype)
                else:
                    hv = h[:, vpos]
                    h[:, vpos] = hv + ((s_.to(hv.dtype) - hv) @ Q.T) @ Q
                return (h,) + tuple(outp[1:]) if isinstance(outp, tuple) else h
            hook = self.mod.register_forward_hook(f)
        try:
            x = self._inputs(P, chunk, False)
            o = self.model(input_ids=x, attention_mask=torch.ones_like(x))
        finally:
            if hook is not None:
                hook.remove()
        return self._readout(P, chunk, o.logits, False)

    def chunks(self, P):
        ps = P["passes"]
        return [ps[s0:s0 + self.bs] for s0 in range(0, len(ps), self.bs)]

    def mean_word(self, P, vals):
        per_word = np.zeros(P["n_words"])
        for (_, _, k), val in zip(P["passes"], vals):
            per_word[P["v_gw"][k]] += val
        return float(per_word.mean())

    @torch.no_grad()
    def score(self, P, conds):
        """S(clean), and S(base) under each condition: conds maps a name to (site, Q)."""
        out = {c: [] for c in conds}
        sc = []
        for chunk in self.chunks(P):
            src, _, s = self.clean_chunk(P, chunk, False)
            sc += s.tolist()
            for c, (site, Q) in conds.items():
                out[c] += self.base_chunk(P, chunk, src, site, Q)[1].tolist()
        return self.mean_word(P, sc), {c: self.mean_word(P, v) for c, v in out.items()}

    def kl_backward(self, P, site, Q, weight):
        """Backpropagate weight * mean over passes of KL(clean || patched); returns the pair's mean KL."""
        total, n = 0.0, len(P["passes"])
        for chunk in self.chunks(P):
            src, lp_c, _ = self.clean_chunk(P, chunk, True)
            lp_p, _ = self.base_chunk(P, chunk, src, site, Q())
            kl = (lp_c.exp() * (lp_c - lp_p)).sum(-1).sum()
            (kl * weight / n).backward()
            total += float(kl)
        return total / n

    @torch.no_grad()
    def head_states(self, ids, positions):
        """Layer states of an unmasked run at the given subtoken positions."""
        got = {}

        def f(mod, inp, outp):
            got["h"] = (outp[0] if isinstance(outp, tuple) else outp)[0].detach()
        hook = self.mod.register_forward_hook(f)
        try:
            x = torch.tensor([ids], device=self.device)
            self.model(input_ids=x, attention_mask=torch.ones_like(x))
        finally:
            hook.remove()
        return [got["h"][p].float() for p in positions]


def share(base, patched, clean, keep):
    return float((base[keep] - patched[keep]).sum() / (base[keep] - clean[keep]).sum())


def doc_signflip(diff, docs, n_perm=10000, seed=707):
    s = pd.Series(diff).groupby(docs).sum().to_numpy()
    obs = abs(s.sum())
    signs = np.random.default_rng(seed).choice([-1.0, 1.0], size=(n_perm, len(s)))
    return float((1 + (np.abs(signs @ s) >= obs - 1e-12).sum()) / (n_perm + 1))


def doc_spearman(x, y, docs, n_perm=10000, seed=707):
    d = pd.DataFrame({"x": x, "y": y, "doc": docs}).dropna().groupby("doc").mean()
    rho = spearmanr(d.x, d.y).statistic
    rng = np.random.default_rng(seed)
    null = np.array([spearmanr(rng.permutation(d.x.to_numpy()), d.y).statistic for _ in range(n_perm)])
    return float(rho), float((1 + (np.abs(null) >= abs(rho) - 1e-12).sum()) / (n_perm + 1)), len(d)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True, help="muril, indicbert, mbert or xlmrlarge (picks the layer and I1's CSV)")
    ap.add_argument("--layer", type=int, default=None)
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--units", default=str(rc / "rq1_features_units.csv"))
    ap.add_argument("--features", default=str(rc / "rq1_features_all.csv"))
    ap.add_argument("--i1-csv", default=None, help="I1's per-pair output (default patching/patching_<tag>.csv)")
    ap.add_argument("--n-eval", type=int, default=1000, help="the first n of I1's 1,000 pairs (fewer only for a smoke)")
    ap.add_argument("--n-train", type=int, default=2000)
    ap.add_argument("--n-val", type=int, default=200)
    ap.add_argument("--ranks", nargs="+", type=int, default=[1, 4, 16, 64])
    ap.add_argument("--verb-ranks", nargs="+", type=int, default=[1, 16])
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--pairs-per-step", type=int, default=8)
    ap.add_argument("--random-seeds", type=int, default=3)
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--out-dir", default=str(rc / "das"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    layer = args.layer if args.layer is not None else LAYER[args.tag]
    i1_csv = Path(args.i1_csv or rc / "patching" / f"patching_{args.tag}.csv")
    with RunLog(args.record_tag or f"rq1_das_{args.tag}", __file__, args,
                purpose="Distributed alignment search: is what the moved head words carry (I1) a low-rank subspace, "
                        "and what does it encode?") as log:
        torch.manual_seed(707)
        model, tok, device = load_masked_lm(args.model)
        model.eval()
        for p_ in model.parameters():
            p_.requires_grad_(False)
        d_model = model.config.hidden_size
        R = Runner(model, tok, device, layer, args.batch_size)
        log.kv("layer / hidden size", f"{layer} / {d_model}")

        refs, vars_ = load_trees()
        vt = set1_variants().set_index("var_id")
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]]
        pick_i = np.sort(np.random.default_rng(707).choice(len(pairs), size=min(1000, len(pairs)), replace=False))
        ev_pairs = pairs.iloc[pick_i]
        doc = lambda s: s.str.split("__").str[0]
        ev_docs = set(doc(ev_pairs.ref_id))
        pool = pairs.drop(index=pairs.index[pick_i])
        pool = pool[~doc(pool.ref_id).isin(ev_docs)]
        pool = pool.iloc[np.random.default_rng(708).permutation(len(pool))]

        def build(df, n):
            got = []
            for r in df.itertuples():
                if len(got) == n:
                    break
                P = prepare(r, refs, vars_, vt, tok)
                if P is not None:
                    got.append(P)
            return got
        EV = build(ev_pairs.iloc[:args.n_eval], args.n_eval)
        VA = build(pool.iloc[:args.n_val * 2], args.n_val)
        TR = build(pool.iloc[args.n_val * 2:], args.n_train)
        assert not ({doc(pd.Series([P["ref_id"]]))[0] for P in TR + VA} & ev_docs)
        log.kv("pairs: evaluation (I1's) / validation / training", f"{len(EV):,} / {len(VA):,} / {len(TR):,}")
        log.kv("evaluation documents / training and validation documents",
               f"{len({P['ref_id'].split('__')[0] for P in EV}):,} / "
               f"{len({P['ref_id'].split('__')[0] for P in TR + VA}):,} (disjoint)")

        def recovered(Ps, site, Q):
            b, pt, c = [], [], []
            for P in Ps:
                sc, s = R.score(P, {"b": (site, None), "p": (site, Q)})
                b.append(s["b"]), pt.append(s["p"]), c.append(sc)
            b, pt, c = map(np.array, (b, pt, c))
            return share(b, pt, c, np.abs(c - b) > args.min_gap)

        # ---- checks 1 and 2, before any training: this script must reproduce I1's setup ----------------------
        pre = {"base": ("moved_heads", None), "full_moved_heads": ("moved_heads", "full"), "full_verb": ("verb", "full")}
        chk = []
        for P in EV:
            sc, s = R.score(P, pre)
            chk.append({"ref_id": P["ref_id"], "var_id": P["var_id"], "s_clean": sc, **s})
        chk = pd.DataFrame(chk)
        i1 = pd.read_csv(i1_csv)[["ref_id", "var_id", "s_ref", "s_var", f"moved_heads@{layer}", f"verb@{layer}"]].merge(
            chk, on=["ref_id", "var_id"], how="inner")
        if len(i1) != len(chk):
            raise SystemExit(f"check failed: {len(chk) - len(i1)} evaluation pairs are not in I1's output")
        dev = {"S(base) vs I1 s_var": (i1.base - i1.s_var).abs().max(),
               "S(clean) vs I1 s_ref": (i1.s_clean - i1.s_ref).abs().max(),
               f"full patch, moved heads, vs I1 moved_heads@{layer}": (i1.full_moved_heads - i1[f"moved_heads@{layer}"]).abs().max(),
               f"full patch, verb, vs I1 verb@{layer}": (i1.full_verb - i1[f"verb@{layer}"]).abs().max()}
        log.h3("Checks against I1's per-pair output, before training (largest departure, bits)")
        for k_, v_ in dev.items():
            log.kv(k_, f"{v_:.2e}")
        if max(dev.values()) > 5e-3:
            raise SystemExit("checks 1 and 2 failed: this script does not reproduce I1's setup")

        # ---- training --------------------------------------------------------------------------------------
        learned, history = {}, []
        for site, ranks in (("moved_heads", args.ranks), ("verb", args.verb_ranks)):
            TRs, VAs = [P for P in TR if P["site_tok"][site]], [P for P in VA if P["site_tok"][site]]
            log.kv(f"{site}: training / validation pairs with the site present",
                   f"{len(TRs):,} of {len(TR):,} / {len(VAs):,} of {len(VA):,}")
            for k in ranks:
                torch.manual_seed(1000 + k + (0 if site == "moved_heads" else 500))
                lin = torch.nn.utils.parametrizations.orthogonal(
                    torch.nn.Linear(d_model, k, bias=False)).to(device)
                opt = torch.optim.Adam(lin.parameters(), lr=args.lr)
                best, best_rec = lin.weight.detach().clone(), recovered(VAs, site, lin.weight.detach())
                history.append([site, k, 0, float("nan"), best_rec])
                print(f"    {site} k={k}: validation recovery before training {best_rec:.4f}", flush=True)
                rng = np.random.default_rng(709 + k)
                for ep in range(1, args.epochs + 1):
                    order, kls = rng.permutation(len(TRs)), []
                    opt.zero_grad()
                    for j, i in enumerate(order, 1):
                        kls.append(R.kl_backward(TRs[i], site, lambda: lin.weight, 1.0 / args.pairs_per_step))
                        if j % args.pairs_per_step == 0 or j == len(order):
                            opt.step()
                            opt.zero_grad()
                        if j % 250 == 0:
                            print(f"      epoch {ep}: {j:,}/{len(TRs):,} pairs, mean KL {np.mean(kls[-250:]):.4f}", flush=True)
                    rec = recovered(VAs, site, lin.weight.detach())
                    history.append([site, k, ep, float(np.mean(kls)), rec])
                    print(f"    {site} k={k} epoch {ep}: mean KL {np.mean(kls):.4f}, validation recovery {rec:.4f}", flush=True)
                    if rec > best_rec:
                        best, best_rec = lin.weight.detach().clone(), rec
                ortho = float((best @ best.T - torch.eye(k, device=device)).abs().max())
                if ortho > 1e-4:
                    raise SystemExit(f"check 3 failed: Q for {site} k={k} is not orthonormal ({ortho:.2e})")
                learned[(site, k)] = best
        log.h3("Training (validation pairs; epoch 0 is the random initialisation)")
        log.table(["site", "rank", "epoch", "mean KL", "validation recovery"], history)
        np.savez(out / f"das_{args.tag}.npz", **{f"{s}_k{k}": Q.cpu().numpy() for (s, k), Q in learned.items()})
        log.output(str(out / f"das_{args.tag}.npz"), "the learned subspaces (k x d, orthonormal rows), per site and rank")

        # ---- evaluation ------------------------------------------------------------------------------------
        g = torch.Generator().manual_seed(710)
        conds = {"base": ("moved_heads", None), "full_moved_heads": ("moved_heads", "full"), "full_verb": ("verb", "full")}
        for (site, k), Q in learned.items():
            conds[f"das_{site}_k{k}"] = (site, Q)
            for sd in range(args.random_seeds):
                q, _ = torch.linalg.qr(torch.randn(d_model, k, generator=g))
                conds[f"rand{sd}_{site}_k{k}"] = (site, q.T.contiguous().to(device))
        rows = []
        for n, P in enumerate(EV, 1):
            sc, s = R.score(P, conds)
            rows.append({"ref_id": P["ref_id"], "var_id": P["var_id"], "s_clean": sc, **s,
                         **{f"n_{st}": len(P["site_tok"][st]) for st in SITES}})
            if n % 100 == 0:
                print(f"    evaluated {n:,}/{len(EV):,}", flush=True)
        d = pd.DataFrame(rows)

        # the evaluation must repeat the pre-training check's numbers (same code path, so exactly)
        again = chk.merge(d, on=["ref_id", "var_id"], suffixes=("", "_ev"))
        if len(again) != len(d) or max((again[c] - again[f"{c}_ev"]).abs().max()
                                       for c in ("s_clean", "base", "full_moved_heads", "full_verb")) > 5e-3:
            raise SystemExit("check failed: the evaluation does not repeat the pre-training check")

        f = out / f"das_{args.tag}.csv"
        keep = (d.s_clean - d.base).abs() > args.min_gap
        docs = doc(d.ref_id)
        log.kv("evaluation pairs with a gap above --min-gap", f"{int(keep.sum()):,} of {len(d):,}")

        tab = []
        for site, ranks in (("moved_heads", args.ranks), ("verb", args.verb_ranks)):
            full = share(d.base, d[f"full_{site}"], d.s_clean, keep)
            for k in ranks:
                das = share(d.base, d[f"das_{site}_k{k}"], d.s_clean, keep)
                rcols = [f"rand{sd}_{site}_k{k}" for sd in range(args.random_seeds)]
                rnd = float(np.mean([share(d.base, d[c], d.s_clean, keep) for c in rcols]))
                moved = (d.base - d[f"das_{site}_k{k}"])[keep]
                p_r = doc_signflip(moved - (d.base - d[rcols].mean(axis=1))[keep], docs[keep])
                p_f = doc_signflip(moved - (d.base - d[f"full_{site}"])[keep], docs[keep])
                tab.append([site, k, das, rnd, full, p_r, p_f])
        log.h2("Share of the gap recovered on I1's pairs")
        log.table(["site", "rank", "learned", "random (mean)", "full state (I1)", "p, learned vs random",
                   "p, learned vs full"], tab)
        log.p("A ratio of sums over evaluation pairs, I1's measure: 1 closes the variant's gap to the reference, 0 "
              "leaves it. p: document-level sign-flip permutation on the per-pair difference in the amount moved, "
              "two-sided, 10,000 permutations. The verb complex is the site control.")

        # ---- reading the rank-1 variable ----------------------------------------------------------------------
        if ("moved_heads", 1) in learned:
            q = learned[("moved_heads", 1)][0].float()
            dv, dpos = [], []
            for P in EV:
                def per_head(ids, words, heads):
                    vals = [float(torch.stack(R.head_states(ids, words[w])).mean(0) @ q) for w in heads if words[w]]
                    return float(np.mean(vals)) if vals else np.nan
                vr = per_head(P["c_ids"], P["c_words"], P["heads_ref"])
                vv = per_head(P["v_ids"], P["v_words"], P["heads_var"])
                dv.append(vr - vv)
                dpos.append(float(np.mean(P["heads_ref"]) - np.mean(P["heads_var"])) if P["heads_ref"] else np.nan)
            d["dv"], d["dpos"], d["d_T"] = dv, dpos, d.s_clean - d.base
            sgn = 1.0 if spearmanr(d.dv, d.d_T, nan_policy="omit").statistic >= 0 else -1.0
            d["dv"] *= sgn
            log.kv("rank-1 direction's sign in dv (the npz holds the unflipped Q)", f"{sgn:+.0f}")
            feats = pd.read_csv(args.units, usecols=["ref_id", "var_id", "d_syn_order"]).merge(
                pd.read_csv(args.features, usecols=["ref_id", "var_id", "d_kenlm_mean"]), on=["ref_id", "var_id"])
            m = d.merge(feats, on=["ref_id", "var_id"], how="left")
            tab = []
            for name, col in (("the model's preference d_T", "d_T"), ("E1, d_syn_order", "d_syn_order"),
                              ("trigram, d_kenlm_mean", "d_kenlm_mean"), ("moved heads' position change, dpos", "dpos")):
                rho_pair = float(spearmanr(m.dv, m[col], nan_policy="omit").statistic)
                rho, p, nd = doc_spearman(m.dv, m[col], doc(m.ref_id))
                tab.append([name, rho_pair, rho, p, nd])
            log.h2("What the rank-1 variable tracks (moved head words, unmasked runs)")
            log.table(["against", "Spearman over pairs", "Spearman over documents", "p (documents)", "documents"], tab)
            log.p("dv is the change in the learned direction's value at the moved head words, reference minus variant, "
                  "signed so that it rises with the model's own preference. Over documents: per-document means, "
                  "permutation p over documents, 10,000. Descriptive.")
            d = m
        d.to_csv(f, index=False)
        log.output(str(f), "per evaluation pair: clean and base runs, the base run under every condition, and (rank 1) "
                           "dv, dpos and the E1 and trigram differences")


if __name__ == "__main__":
    main()
