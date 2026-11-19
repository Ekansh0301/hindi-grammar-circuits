#!/usr/bin/env python3
"""Erasing role or case at every layer, at the positions the erasers were fitted on (EXTENSION I2, its caveat, 5 Oct).

rq1_concept_erasure_all.py fitted each block's LEACE eraser on the constituents' pooled states (their words without
their own postpositions) but applied it to EVERY token's state, verbs, postpositions and punctuation included, where
LEACE's affine correction is off its fitted distribution; compounded over every block, that made MuRIL, IndicBERT-v2
and mBERT unreadable (IndicBERT-v2 even under the random eraser), so the caveat stayed open for them. This script
applies each eraser only where it was fitted. Declared before any run (5 Oct 2026); everything not stated here is as
in rq1_concept_erasure_all.py, whose code this copies:

  positions    in every sentence scored, the eraser acts only on the subtokens of the words of the clause's units,
               without their own postpositions (lm_units.unit_word_positions on the reference; for a variant the same
               words, mapped by lm_units.set1_surface_indices), and only where the token is not [MASK]: in a
               within_word_l2r pass the scored subtoken and the rest of its word are masked, and a [MASK] state is
               not in the population the erasers were fitted on (unmasked full-sentence states), so it is left alone
               (revised on review, 5 Oct, before any run of this script was read). So the eraser acts exactly on the
               population it is fitted on.
               Postpositions, the verb complex and every other word are left alone. Because LEACE is affine and
               affine maps commute with averaging, erasing every subtoken of a unit erases the unit's pooled state
               exactly, which is what the fit, check 2 and the probes read; a single subtoken's deviation from its
               unit's mean is not erased. Units headed by a fused case pronoun are not units here (as in the fit)
  fitting      sequential, as before, with the earlier blocks' erasers acting at these positions
  readability  on 500 sample references NOT among the 2,000 fit references (seed 707), each with its clause's units
               erased (raw IndicCorp text, used before, has no trees to say where the units are); held-out nats per
               subtoken over all subtokens, and separately over the units' subtokens and over the rest. READ only
               if BOTH the all-subtoken and the units'-subtoken figures are within 2 nats of no erasure (revised on
               review: the units are about half the words, so the all-subtoken mean alone would be looser than I3's
               rule). These figures are on treebank text, not comparable with rq1_concept_erasure_all.py's
  files        t_<tag>eu<k>_s0.csv, osv_<tag>eu<k>.csv, erasers_<tag>.npz in concept_erasure_units/ (eu: erased at the
               units, every layer); record rq1_concept_erasure_units_<tag>
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
from hutb_corpus import BASE, load_trees, set1_variants, text_of
from pll_scorer import load_masked_lm
from rq1_concept_erasure import LAYER, leace, probe_acc, random_eraser
from runlog import RunLog

# the same indices as rq1_concept_erasure.py (file eu<k> pairs with er<k>); 'control' is not run here
CONDITIONS = ["none", "role", "marker", "control", "random"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--conditions", nargs="+", default=["none", "role", "marker", "random"],
                    choices=["none", "role", "marker", "random"])
    ap.add_argument("--erasers", default=None, help="npz of fitted erasers to reuse (written by an earlier run); "
                    "the checks still run")
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--osv-pairs", default=str(rc / "rq1_osv_transition_pairs.csv"))
    ap.add_argument("--limit", type=int, default=None, help="score only this many pairs (smoke)")
    ap.add_argument("--fit-limit", type=int, default=None, help="fit on only this many references (smoke)")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--permutations", type=int, default=10000)
    ap.add_argument("--out-dir", default=str(rc / "concept_erasure_units"))
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with RunLog(args.record_tag or f"rq1_concept_erasure_units_{args.tag}", __file__, args,
                purpose="LEACE erasure of role or marker at every layer, at the constituents' own words only.") as log:
        z = np.load(rc / "lm_units" / f"units_{args.tag}.npz", allow_pickle=True)
        rid_all, head_all = z["ref_id"].astype(str), z["unit_head"].astype(int)
        rel, lab = z["rel"].astype(str), z["label"].astype(str)
        role = np.where(np.isin(rel, ["k1", "k2"]), rel, "other")
        fit_refs = list(dict.fromkeys(rid_all))
        if args.fit_limit:
            fit_refs = fit_refs[:args.fit_limit]
        keep_units = np.isin(rid_all, fit_refs)
        rid_all, head_all, role, lab = rid_all[keep_units], head_all[keep_units], role[keep_units], lab[keep_units]
        stored = z["states"][keep_units].astype(np.float32)
        groups = pd.factorize(rid_all)[0]
        onehot = lambda y: pd.get_dummies(pd.Series(y)).to_numpy(float)

        model, tok, device = load_masked_lm(args.model)
        model.eval()
        blocks = model.base_model.encoder.layer
        N = len(blocks)
        refs, vars_ = load_trees()
        vt = set1_variants().set_index("var_id")
        var_of = dict(pd.read_csv(args.pairs)[["ref_id", "var_id"]].drop_duplicates("ref_id").itertuples(index=False))
        active = {"pos": None, "ids": None}          # unit subtoken positions (set per sentence); the batch's input ids
        mask_id = tok.mask_token_id

        def grab_ids(mod, inp):
            active["ids"] = inp[0]
        model.base_model.embeddings.word_embeddings.register_forward_pre_hook(grab_ids)

        def subtokens(text, words):
            g = U.whitespace_groups(tok, text)
            if g is None:
                return []
            _, grp, gw, _ = g
            ws = set(words)
            return sorted(p for k, pos in enumerate(grp) if gw[k] in ws for p in pos)

        def unit_words(ref_id, clause_head):
            return [w for _, _, _, words in U.unit_word_positions(refs[ref_id], clause_head) for w in words]

        def var_words(ref_id, var_id, words):
            ridx, vidx = U.set1_surface_indices(refs[ref_id], vt.loc[var_id].to_dict() | {"var_id": var_id}, vars_[var_id])
            at = {t: k for k, t in enumerate(vidx)}
            return [at[ridx[w]] for w in words]

        def set_positions(text, words):
            p = subtokens(text, words)
            active["pos"] = torch.tensor(p, dtype=torch.long, device=device) if p else None

        def unit_states():
            """[units, N+1, d] pooled states of the fit units with whatever hooks are active, in the stored order."""
            rows_out = []
            for r in fit_refs:
                rows = refs[r]
                set_positions(text_of(rows, True), unit_words(r, vt.loc[var_of[r]].clause_head))
                ts = U.token_states(model, tok, device, text_of(rows, True))
                if ts is None:
                    raise SystemExit(f"{r}: a fit reference no longer scores")
                hs, _, word_of = ts
                for d, rl, lb, words in U.unit_word_positions(rows, vt.loc[var_of[r]].clause_head):
                    sub = [p for p, w in word_of.items() if w in set(words)]
                    if sub:
                        rows_out.append((r, d, hs[:, sub].mean(1).numpy()))
            got = [(r, d) for r, d, _ in rows_out]
            if got != list(zip(rid_all, head_all)):
                raise SystemExit("recomputed units differ from the stored ones in identity or order")
            return np.stack([x for _, _, x in rows_out])

        def hook_for(A_, b_):
            At = torch.tensor(A_.T, dtype=torch.float32, device=device)
            bt = torch.tensor(b_, dtype=torch.float32, device=device)

            def f(mod, inp, outp, At=At, bt=bt):
                pos = active["pos"]
                if pos is None:
                    return outp
                h = outp[0] if isinstance(outp, tuple) else outp
                ids = active["ids"]
                if ids.shape != h.shape[:2]:
                    raise SystemExit("the captured input ids do not match the block's states")
                sel = torch.zeros(ids.shape, dtype=torch.bool, device=h.device)
                sel[:, pos] = True
                sel &= ids != mask_id                    # never a [MASK] state: not in the fitted population
                h2 = h.clone()
                h2[sel] = (h[sel].float() @ At + bt).to(h.dtype)
                return (h2,) + tuple(outp[1:]) if isinstance(outp, tuple) else h2
            return f

        with torch.no_grad():
            S0 = unit_states()
        diff = np.abs(S0 - stored)
        bad = int((diff > 2e-3 * np.abs(stored) + 0.01).sum())
        log.kv("fit references / units / encoder blocks", f"{len(fit_refs):,} / {len(rid_all):,} / {N}")
        log.kv("check 1: recomputed unerased unit states against the stored (float16) ones: largest absolute / "
               "largest relative departure / elements outside tolerance",
               f"{float(diff.max()):.4f} / {float((diff / (np.abs(stored) + 1e-3)).max()):.2e} / {bad}")
        if bad:
            raise SystemExit("the recomputed fit units do not reproduce the stored states")

        # sequential fitting: erasers[concept][l] for block l = 1..N, fitted with blocks < l erased
        erasers = {}
        ranks = {}
        saved = np.load(args.erasers) if args.erasers else None
        for concept in ("role", "marker", "random"):
            if concept not in args.conditions:
                continue
            if saved is not None:
                erasers[concept] = {l: (saved[f"{concept}_A_{l}"], saved[f"{concept}_b_{l}"]) for l in range(1, N + 1)}
                log.kv(f"{concept}: erasers loaded from", args.erasers)
                continue
            erasers[concept], ranks[concept] = {}, []
            handles = []
            try:
                for l in range(1, N + 1):
                    with torch.no_grad():
                        X = S0[:, l] if l == 1 else unit_states()[:, l]
                    X = X.astype(np.float64)
                    if concept == "role":
                        A_, b_, rk, _ = leace(X, onehot(role))
                    elif concept == "marker":
                        A_, b_, rk, _ = leace(X, onehot(lab))
                    else:
                        _, _, rk, white = leace(X, onehot(role))
                        A_, b_ = random_eraser(white, rk, X.shape[1], seed=707 + l)
                    erasers[concept][l] = (A_, b_)
                    ranks[concept].append(rk)
                    handles.append(blocks[l - 1].register_forward_hook(hook_for(A_, b_)))
                    print(f"    {concept}: block {l} fitted (rank {rk})", flush=True)
            finally:
                for h in handles:
                    h.remove()
            log.kv(f"{concept}: rank removed per block", " ".join(map(str, ranks[concept])))
        if saved is None and erasers:
            ef = out / f"erasers_{args.tag}.npz"
            np.savez(ef, **{f"{c}_{x}_{l}": v for c, d_ in erasers.items() for l, (A_, b_) in d_.items()
                            for x, v in (("A", A_), ("b", b_))})
            log.output(str(ef), "the fitted erasers, every block, for reuse")

        # check 2: every block's eraser active, probe each concept at every layer
        def all_hooks(concept):
            return [blocks[l - 1].register_forward_hook(hook_for(*erasers[concept][l])) for l in range(1, N + 1)]
        log.h2("Check: every block's eraser active")

        def xcov(X, Z):
            Xc, Zc = X - X.mean(0), Z - Z.mean(0)
            return float(np.linalg.norm(Xc.T @ Zc / len(X)))
        probe_layers = sorted({1, LAYER[args.tag], N // 2, N})
        rows_cov, rows_ck = [], []
        Zr, Zm = onehot(role), onehot(lab)
        for concept in [c for c in ("role", "marker", "random") if c in erasers]:
            hs_ = all_hooks(concept)
            try:
                with torch.no_grad():
                    Se = unit_states()
            finally:
                for h in hs_:
                    h.remove()
            for l in range(1, N + 1):
                rows_cov.append([concept, l, xcov(Se[:, l], Zr) / xcov(S0[:, l], Zr), xcov(Se[:, l], Zm) / xcov(S0[:, l], Zm)])
            for l in probe_layers:
                ar, mr = probe_acc(Se[:, l], role, groups)
                am, mm = probe_acc(Se[:, l], lab, groups)
                rows_ck.append([concept, l, ar, mr, am, mm])
                print(f"    {concept}: probes at layer {l} done", flush=True)
        log.table(["eraser", "layer", "cross-covariance with role, share of unerased",
                   "with marker, share of unerased"], rows_cov, floatfmt="{:.2e}")
        log.table(["eraser", "layer", "role probe", "role majority", "marker probe", "marker majority"], rows_ck,
                  floatfmt="{:.4f}")
        for concept, l, cr, cm in rows_cov:
            if (concept == "role" and cr > 0.01) or (concept == "marker" and cm > 0.01):
                raise SystemExit(f"{concept}: cross-covariance at layer {l} is {max(cr, cm):.3g} of the unerased")
        for concept, l, ar, mr, am, mm in rows_ck:
            if concept == "role" and ar > mr + 0.02:
                raise SystemExit(f"role stays decodable at layer {l} under all-layer erasure ({ar:.3f} against {mr:.3f})")
            if concept == "marker" and am > mm + 0.02:
                raise SystemExit(f"the marker stays decodable at layer {l} under all-layer erasure ({am:.3f} against {mm:.3f})")

        # scoring
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]]
        osv = pd.read_csv(args.osv_pairs)
        osv = osv[osv.transition.isin(["OSV->SOV", "OSV->OSV"])][["ref_id", "var_id", "transition"]]
        if args.limit:
            pairs, osv = pairs.head(args.limit), osv.head(args.limit)
        fit_set = set(fit_refs)
        cand = [r for r in pd.read_csv(args.pairs).ref_id.drop_duplicates() if r not in fit_set and r in var_of]
        held_idx = np.random.default_rng(707).choice(len(cand), size=min(500, len(cand)), replace=False)
        held = [(cand[i], unit_words(cand[i], vt.loc[var_of[cand[i]]].clause_head)) for i in sorted(held_idx)]
        log.kv("readability references (not fit references)", f"{len(held):,}")
        summary = []
        for cond in args.conditions:
            hs_ = [] if cond == "none" else all_hooks(cond)
            try:
                with torch.no_grad():
                    tot, nsub, tu, nu = 0.0, 0, 0.0, 0
                    for r_, words in held:
                        text = text_of(refs[r_], True)
                        set_positions(text, words)
                        a = U.score_words(model, tok, device, text, args.batch_size, layers=False)
                        if a is not None:
                            tot += float(np.sum(a[0])) * np.log(2)
                            nsub += sum(a[1])
                            tu += float(sum(a[0][w] for w in words)) * np.log(2)
                            nu += sum(a[1][w] for w in words)
                    readability = tot / nsub
                    read_units, read_rest = tu / nu, (tot - tu) / (nsub - nu)

                    def score(df):
                        res = []
                        for r in df.itertuples():
                            words = unit_words(r.ref_id, vt.loc[r.var_id].clause_head)
                            rtext, vtext = text_of(refs[r.ref_id], True), text_of(vars_[r.var_id], False)
                            set_positions(rtext, words)
                            a = U.score_words(model, tok, device, rtext, args.batch_size, layers=False)
                            set_positions(vtext, var_words(r.ref_id, r.var_id, words))
                            v = U.score_words(model, tok, device, vtext, args.batch_size, layers=False)
                            if a is not None and v is not None:
                                res.append({"ref_id": r.ref_id, "var_id": r.var_id, "ref_Mean": float(np.mean(a[0])),
                                            "var_Mean": float(np.mean(v[0]))})
                        return pd.DataFrame(res)
                    t = score(pairs)
                    o = score(osv).merge(osv, on=["ref_id", "var_id"])
            finally:
                for h in hs_:
                    h.remove()
            active["pos"] = None
            k = CONDITIONS.index(cond)
            col = f"t_{args.tag}eu{k}_Mean"
            t[col] = t.ref_Mean - t.var_Mean
            o["d"] = o.ref_Mean - o.var_Mean
            tf, of = out / f"t_{args.tag}eu{k}_s0.csv", out / f"osv_{args.tag}eu{k}.csv"
            t.to_csv(tf, index=False)
            o.to_csv(of, index=False)
            log.output(str(tf), f"RQ1 pairs, condition {cond}")
            log.output(str(of), f"OSV transition pairs, condition {cond}")
            unseen = t[~t.ref_id.isin(set(fit_refs))]
            summary.append([cond, readability, read_units, read_rest, float((t[col] < 0).mean()), float((unseen[col] < 0).mean()),
                            float((o[o.transition == "OSV->SOV"].d < 0).mean()),
                            float((o[o.transition == "OSV->OSV"].d < 0).mean())])
            print(f"    condition {cond} done", flush=True)
        log.h2("Per condition")
        base_read = next((r[1] for r in summary if r[0] == "none"), None)
        base_units = next((r[2] for r in summary if r[0] == "none"), None)
        for r in summary:
            r.insert(2, "" if base_read is None else ("yes" if r[1] - base_read <= 2.0 and r[2] - base_units <= 2.0 else "NO"))
        log.table(["condition", "held-out nats per subtoken", "READ (both within 2 nats of none)", "units' subtokens",
                   "other subtokens",
                   "reference preferred, all RQ1 pairs", "same, references not used to fit", "OSV defence (OSV->SOV)",
                   "OSV->OSV"], summary, floatfmt="{:.4f}")
        unread = [r[0] for r in summary if r[2] == "NO"]
        if unread:
            log.note(f"Not readable (more than 2 nats worse than no erasure on held-out text, over all subtokens or the units'): {', '.join(unread)}. "
                     "Their preference numbers below are reported, not interpreted.")

        if "none" in args.conditions:
            log.h2("Change in the OSV defence and in the RQ1 preference, against no erasure and against random")

            def load(cond, kind):
                k = CONDITIONS.index(cond)
                return pd.read_csv(out / (f"osv_{args.tag}eu{k}.csv" if kind == "osv" else f"t_{args.tag}eu{k}_s0.csv"))
            res = []
            for k_c, cond in enumerate([c for c in args.conditions if c != "none"]):
                for against in [x for x in ("none", "random") if x in args.conditions and x != cond]:
                    rng = np.random.default_rng([707, k_c, ("none", "random").index(against)])
                    for kind in ("osv", "rq1"):
                        a, b = load(cond, kind), load(against, kind)
                        if kind == "osv":
                            m = a.merge(b[["ref_id", "var_id", "d"]], on=["ref_id", "var_id"], suffixes=("", "_b"))
                            m = m[m.transition == "OSV->SOV"]
                            ca, cb = "d", "d_b"
                        else:
                            ca = f"t_{args.tag}eu{CONDITIONS.index(cond)}_Mean"
                            cb = f"t_{args.tag}eu{CONDITIONS.index(against)}_Mean"
                            m = a[["ref_id", "var_id", ca]].merge(b[["ref_id", "var_id", cb]], on=["ref_id", "var_id"])
                        delta = (m[ca] < 0).astype(float) - (m[cb] < 0).astype(float)
                        doc = m.ref_id.str.split("__").str[0]
                        sums = delta.groupby(doc).sum().to_numpy()
                        obs = sums.sum() / len(m)
                        null = (rng.choice([-1.0, 1.0], size=(args.permutations, len(sums))) @ sums) / len(m)
                        p = (1 + int((np.abs(null) >= abs(obs)).sum())) / (1 + args.permutations)
                        res.append(["OSV->SOV" if kind == "osv" else "RQ1 pairs", cond, against, len(m), obs, p])
            log.table(["pairs", "eraser", "against", "n", "change in reference-preferred rate", "document sign-flip p"],
                      res, floatfmt="{:.4g}")


if __name__ == "__main__":
    main()
