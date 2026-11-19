#!/usr/bin/env python3
"""Driver for lm_units.py on a Set 1 pair list (RQ1_WORK_PLAN.md D1, D3, D4; masked LMs).

--what words     per-word surprisal (final layer and logit lens per layer) for reference and variant:
                 words_<tag>_s<k>.csv.gz, one row per word: ref_id, var_id, side, pos (surface position),
                 tree_idx (REFERENCE tree index, also for the variant), form, n_subtokens, s, lens_0..lens_L
--what states    pooled hidden states: states_<tag>_s<k>_part<j>.npz with ref_id, var_id, diff
                 (reference minus variant, float16, pairs x layers x d), cos (pairs x layers), and
                 pre_ln_maxabs (max |difference| of the pooled pre-LayerNorm embedding sum, which must be
                 zero up to float error: the layer-0 identity check of PREREGISTRATION_DRAFT.md 7.1)
--what window    per-word surprisal with w words of context each side, for every --windows value:
                 window_<tag>_s<k>.csv.gz, one row per word and window

Every output is written in parts and a rerun skips pairs already written (4 h job limits).
--check-against compares each sentence's summed final-layer surprisal with the Sum feature of an
existing t_<tag>_within_word_l2r_s*.csv run; the largest difference is recorded.
"""
import argparse
import csv
import gzip
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

import lm_units as U
from hutb_corpus import BASE, load_trees, set1_variants, text_of
from pll_scorer import load_masked_lm
from runlog import RunLog


def done_pairs(paths, cols=("ref_id", "var_id")):
    got = set()
    for p in paths:
        if p.suffix == ".npz":
            z = np.load(p, allow_pickle=False)
            got |= set(zip(z["ref_id"], z["var_id"]))
        else:
            with gzip.open(p, "rt", encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    got.add((r["ref_id"], r["var_id"]))
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--what", required=True, choices=["words", "states", "window", "readability", "units"])
    ap.add_argument("--n-refs", type=int, default=2000, help="--what units: references drawn (seed 707)")
    ap.add_argument("--sentences", default="/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt",
                    help="--what readability: plain sentences, one per line (IndicCorp sample, HDTB removed)")
    ap.add_argument("--pairs", default=str(BASE / "Results_Checks" / "rq1_sample_n12000.csv"))
    ap.add_argument("--windows", nargs="+", type=int, default=[1, 2, 3, 5])
    ap.add_argument("--no-lens", action="store_true")
    ap.add_argument("--tuned-lens", default=None, help="translators from rq1_tuned_lens.py; lens columns use them "
                                                         "(use a different --tag, e.g. muril_tuned)")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--flush-every", type=int, default=250)
    ap.add_argument("--limit", type=int, default=None, help="first N pairs of the shard (smoke tests)")
    ap.add_argument("--out-dir", default=str(BASE / "Results_Checks" / "lm_units"))
    ap.add_argument("--check-against", default=None, help="glob of t_<tag>_within_word_l2r_s*.csv")
    ap.add_argument("--record-tag", default=None)
    ap.add_argument("--dtype", default="auto", choices=["auto", "float32", "bfloat16", "float16"],
                    help="causal LMs only")
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_tag = (args.record_tag or f"lm_units_{args.what}_{args.tag}") + (f"_s{args.shard}" if args.n_shards > 1 else "")

    with RunLog(run_tag, __file__, args, purpose=f"{args.what} for {args.tag} on Set 1 pairs.") as log:
        if args.what == "readability":
            readability(args, log, out_dir)
            return
        if args.what == "units":
            unit_states(args, log, out_dir)
            return
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]].drop_duplicates().iloc[args.shard::args.n_shards]
        if args.limit:
            pairs = pairs.head(args.limit)
        stem = f"{args.what}_{args.tag}_s{args.shard}"
        parts = sorted(out_dir.glob(f"{stem}_part*"))
        done = done_pairs(parts)
        todo = [r for r in pairs.itertuples() if (r.ref_id, r.var_id) not in done]
        log.kv("pairs in shard / already written / to do", f"{len(pairs):,} / {len(done):,} / {len(todo):,}")

        refs, vars_ = load_trees()
        vt = set1_variants().set_index("var_id")
        from transformers import AutoConfig
        causal = any("CausalLM" in a for a in (AutoConfig.from_pretrained(args.model).architectures or []))
        model, tok, device = (U.load_causal_lm(args.model, dtype=args.dtype) if causal else load_masked_lm(args.model))
        log.kv("device", device)
        log.kv("model type", "causal (leading space, whitespace-corrected word surprisal)" if causal else "masked (within_word_l2r)")
        mismatched = 0
        translators = None
        if args.tuned_lens:
            import torch
            translators = torch.nn.ModuleList([U.Translator(model.config.hidden_size)
                                               for _ in range(model.config.num_hidden_layers)]).to(device)
            translators.load_state_dict(torch.load(args.tuned_lens, map_location=device))
            translators.eval()
            log.kv("tuned lens", args.tuned_lens)
        log.kv("layers (including embeddings)", model.config.num_hidden_layers + 1)

        skipped, part_no, buf = 0, len(parts), []
        n_written = 0

        def flush():
            nonlocal part_no, buf, n_written
            if not buf:
                return
            path = out_dir / f"{stem}_part{part_no:04d}{'.npz' if args.what == 'states' else '.csv.gz'}"
            tmp = path.with_name(path.name + ".tmp")
            if args.what == "states":
                with open(tmp, "wb") as fh:
                    np.savez(fh, ref_id=np.array([b[0] for b in buf]), var_id=np.array([b[1] for b in buf]),
                             diff=np.stack([b[2] for b in buf]).astype(np.float16),
                             cos=np.stack([b[3] for b in buf]).astype(np.float32),
                             pre_ln_maxabs=np.array([b[4] for b in buf], dtype=np.float32))
                n_written += len(buf)
            else:
                pd.DataFrame(buf).to_csv(tmp, index=False, compression="gzip", float_format="%.4f")
                n_written += len({(b["ref_id"], b["var_id"]) for b in buf})
            tmp.replace(path)
            log.output(path, f"{args.what}, part {part_no} (written this run)")
            part_no += 1
            buf = []

        pending = 0
        max_pre = 0.0
        for i, r in enumerate(todo, 1):
            rt, vtr = refs[r.ref_id], vars_[r.var_id]
            rtext, vtext = text_of(rt, True), text_of(vtr, False)
            try:
                ridx, vidx = U.set1_surface_indices(rt, vt.loc[r.var_id].to_dict() | {"var_id": r.var_id}, vtr)
            except ValueError as e:
                raise SystemExit(str(e))
            if causal:
                same = U.token_multiset(tok, rtext) == U.token_multiset(tok, vtext)
                mismatched += not same
            if args.what == "states":
                if causal and not same:
                    skipped += 1
                    continue
                pool = U.causal_pooled if causal else U.pooled_states
                a, b = pool(model, tok, device, rtext), pool(model, tok, device, vtext)
                if a is None or b is None:
                    skipped += 1
                    continue
                cos = torch_cos(a[0], b[0])
                pre = float((a[1] - b[1]).abs().max())
                max_pre = max(max_pre, pre)
                buf.append((r.ref_id, r.var_id, (a[0] - b[0]).numpy(), cos, pre))
            elif args.what == "words":
                if causal:
                    rs = U.causal_words(model, tok, device, rtext, layers=not args.no_lens)
                    vs = U.causal_words(model, tok, device, vtext, layers=not args.no_lens)
                else:
                    rs = U.score_words(model, tok, device, rtext, args.batch_size, layers=not args.no_lens, translators=translators)
                    vs = U.score_words(model, tok, device, vtext, args.batch_size, layers=not args.no_lens, translators=translators)
                if rs is None or vs is None:
                    skipped += 1
                    continue
                if causal:
                    raws = {"ref": rs[1], "var": vs[1]}
                    rs, vs = (rs[0], rs[2], rs[3]), (vs[0], vs[2], vs[3])
                for side, (fin, nsub, lens), idx, text in (("ref", rs, ridx, rtext), ("var", vs, vidx, vtext)):
                    forms = text.split(" ")
                    if len(forms) != len(idx):
                        raise SystemExit(f"{r.var_id}: {len(forms)} words but {len(idx)} tree indices ({side})")
                    for p, (f, n, s_, ti) in enumerate(zip(forms, nsub, fin, idx)):
                        row = {"ref_id": r.ref_id, "var_id": r.var_id, "side": side, "pos": p, "tree_idx": ti,
                               "form": f, "n_subtokens": n, "s": s_}
                        if causal:
                            row["s_raw"] = raws[side][p]
                            row["multiset_equal"] = same
                        if lens is not None:
                            row.update({f"lens_{l}": v for l, v in enumerate(lens[p])})
                        buf.append(row)
            else:
                win = U.causal_window if causal else U.window_words
                res = {w: [win(model, tok, device, t, w) for t in (rtext, vtext)] for w in args.windows}
                if any(x is None for ws in res.values() for x in ws):
                    skipped += 1
                    continue
                for w, ws in res.items():
                    for side, vals, idx, text in (("ref", ws[0], ridx, rtext), ("var", ws[1], vidx, vtext)):
                        for p, (f, s_, ti) in enumerate(zip(text.split(" "), vals, idx)):
                            buf.append({"ref_id": r.ref_id, "var_id": r.var_id, "side": side, "window": w,
                                        "pos": p, "tree_idx": ti, "form": f, "s": s_})
            pending += 1
            if pending >= args.flush_every:
                flush()
                pending = 0
                print(f"    {i}/{len(todo)} ({skipped} skipped)", flush=True)
        flush()
        log.kv("pairs written this run", f"{n_written:,}")
        log.kv("skipped (too long or empty; causal states: token multisets differ)", skipped)
        if causal:
            log.kv("pairs whose reference and variant token multisets differ", mismatched)
        if args.what == "states":
            log.kv("largest |pooled pre-LayerNorm difference| (identity check, must be ~0)", f"{max_pre:.3g}")
            if max_pre > 1e-3:
                raise SystemExit("layer-0 identity check failed: pooled pre-LayerNorm inputs differ")

        if args.check_against and args.what == "words":
            allp = sorted(out_dir.glob(f"{stem}_part*.csv.gz"))
            w = pd.concat(pd.read_csv(p, usecols=["ref_id", "var_id", "side", "s"]) for p in allp)
            sums = w.groupby(["ref_id", "var_id", "side"]).s.sum().unstack("side")
            t = pd.concat(pd.read_csv(p) for p in sorted(Path().glob(args.check_against)))
            j = sums.join(t.set_index(["ref_id", "var_id"])[["ref_Sum", "var_Sum"]], how="inner")
            d = np.maximum((j["ref"] - j["ref_Sum"]).abs(), (j["var"] - j["var_Sum"]).abs())
            log.kv("pairs compared with the existing sentence scores", f"{len(j):,}")
            log.kv("largest |summed word surprisal − existing Sum| (bits)", f"{d.max():.4g}")
            if len(j) and d.max() > 0.05:
                raise SystemExit("per-word surprisal does not add up to the existing sentence scores")


def readability(args, log, out_dir):
    """PREREGISTRATION_DRAFT.md 7.2: logit-lens surprisal per layer on held-out IndicCorp sentences, in nats
    per subtoken; a layer is readable if within 2 nats of the final layer."""
    model, tok, device = load_masked_lm(args.model)
    n_layers = model.config.num_hidden_layers + 1
    lines = [l.strip() for l in open(args.sentences, encoding="utf-8") if 8 <= len(l.split()) <= 40]
    rng = np.random.default_rng(707)
    pick = [lines[i] for i in sorted(rng.choice(len(lines), size=min(args.limit or 500, len(lines)), replace=False))]
    tot, nsub = np.zeros(n_layers), 0
    for text in pick:
        r = U.score_words(model, tok, device, text, args.batch_size, layers=True)
        if r is None:
            continue
        _, ns, lens = r
        tot += np.array(lens).sum(0) * np.log(2)
        nsub += sum(ns)
    per = tot / nsub
    rows = [[l, per[l], per[l] - per[-1], "yes" if per[l] - per[-1] <= 2 else "no"] for l in range(n_layers)]
    log.kv("sentences (8 to 40 words, seed 707)", len(pick))
    log.kv("source", args.sentences)
    log.table(["layer", "nats per subtoken", "minus final layer", "readable"], rows, floatfmt="{:.3f}")
    path = out_dir / f"readability_{args.tag}.csv"
    pd.DataFrame(rows, columns=["layer", "nats_per_subtoken", "minus_final", "readable"]).to_csv(path, index=False)
    log.output(path, "per-layer readability")


def unit_states(args, log, out_dir):
    """PREREGISTRATION_DRAFT.md 7.3: pooled states of each constituent of the clauses of --n-refs sample
    references, without the constituent's own postpositions; one npz with every layer."""
    pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]].drop_duplicates("ref_id")
    rng = np.random.default_rng(707)
    pick = pairs.iloc[np.sort(rng.choice(len(pairs), size=min(args.n_refs, len(pairs)), replace=False))]
    refs, _ = load_trees()
    vt = set1_variants().set_index("var_id")
    model, tok, device = load_masked_lm(args.model)
    rid, head, rel, lab, st, pre = [], [], [], [], [], []
    skipped = 0
    for r in pick.itertuples():
        rows = refs[r.ref_id]
        text = text_of(rows, True)
        ts = U.token_states(model, tok, device, text)
        if ts is None:
            skipped += 1
            continue
        hs, pr, word_of = ts
        for d, rl, lb, words in U.unit_word_positions(rows, vt.loc[r.var_id].clause_head):
            sub = [p for p, w in word_of.items() if w in set(words)]
            if not sub:
                continue
            rid.append(r.ref_id); head.append(d); rel.append(rl); lab.append(lb)
            st.append(hs[:, sub].mean(1).numpy().astype(np.float16))
            pre.append(pr[sub].mean(0).numpy().astype(np.float16))
    path = out_dir / f"units_{args.tag}.npz"
    np.savez(path, ref_id=np.array(rid), unit_head=np.array(head), rel=np.array(rel), label=np.array(lab),
             states=np.stack(st), pre=np.stack(pre))
    log.kv("references / units / skipped references", f"{len(pick):,} / {len(rid):,} / {skipped}")
    counts = pd.Series(lab).value_counts()
    log.table(["case label", "units"], [[k, int(v)] for k, v in counts.items()], floatfmt="{:.0f}")
    log.output(str(path), "unit states, every layer")


def torch_cos(a, b):
    import torch
    return torch.nn.functional.cosine_similarity(a, b, dim=-1).numpy()


if __name__ == "__main__":
    main()
