#!/usr/bin/env python3
"""Where the attention goes, layer by layer, relative to the constituents that moved
(RQ1_WORK_PLAN.md O4).

Everything else in this project says WHERE the order information is: the probes find it in the
upper-middle layers, the lenses read a preference out of them, the decomposition scores what the output
does with it. Nothing says anything about the computation that puts it there, because the project has no
attention, patching or ablation analysis at all. This is the cheapest step in that direction and it is
deliberately the most modest one.

What it measures. For each sentence, every subtoken is assigned the word class of the word it belongs to
(`rq1_word_attribution.word_classes`), and for each layer the attention matrix is averaged over heads and
over query positions, giving the share of attention arriving at each key subtoken. The share landing on
the moved constituents is then divided by the share of subtokens those constituents occupy:

  enrichment = (attention mass on moved words) / (share of subtokens that are moved words)

with attention renormalised over real subtokens first. Special tokens are attention sinks in these
models, taking a large and layer-dependent share of every row, and they are not words: leaving them in
the denominator pushes every enrichment below 1 for a reason that has nothing to do with word order.
The share they take is reported beside the enrichment, because it is the diagnostic that says why.

1.0 is what uniform attention gives. Above 1.0 means attention concentrates on the material whose
position differs between the two orders.

**Reference sentences only, and the reason is an alignment trap rather than a choice.** A variant tree
renumbers its tokens 1..n in the new surface order, so the reference's tree indices do not carry over to
it and "the k-th word of the variant" is not "the k-th word of the reference". Recovering the mapping
means replaying the unit permutation in `var_row["order"]` against the clause spans, which is possible
and is exactly the kind of fiddly index arithmetic that has produced silent, plausible-looking figures in
this project before. The question O4 was added to answer, whether the layers where the probes read most
are also the layers where attention concentrates on the moved material, is answerable on the reference
alone, so that is what this measures.

**This is descriptive and must stay that way.** Attention is not explanation (Jain and Wallace 2019;
Wiegreffe and Pinter 2019): a layer can attend heavily to the moved words without that attention causing
the preference, and the converse. What the figure can support is a statement about whether the layers
where the probes read most are also the layers where attention reorganises. Anything causal needs
patching, which is O5 and a different paper.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
from hutb_corpus import BASE, is_null_form, load_trees, set1_variants, text_of
from pll_scorer import load_masked_lm
from rq1_word_attribution import word_classes
from runlog import RunLog

MOVED = {"moved head", "moved other"}


def tree_idx_of_word(rows):
    """whitespace word index -> reference tree index, matching text_of's NULL removal."""
    out, k = {}, 0
    for r in rows:
        if is_null_form(r[1]):
            continue
        out[k] = int(r[0])
        k += 1
    return out


def attention_shares(model, tok, device, text):
    """(mean attention received by each subtoken per layer [n_layers, n_sub], {subtoken: word})."""
    g = U.whitespace_groups(tok, text)
    if g is None or len(g[0]) > 512:
        return None, None
    ids, groups, gw, _ = g
    word_of = {p: gw[k] for k, pos in enumerate(groups) for p in pos}
    x = torch.tensor([ids], device=device)
    with torch.no_grad():
        out = model.base_model(input_ids=x, attention_mask=torch.ones_like(x),
                               output_attentions=True)
    # [layer, head, query, key] -> mean over heads and queries = share arriving at each key
    att = torch.stack(out.attentions)[:, 0].float()
    return att.mean(1).mean(1).cpu().numpy(), word_of


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--n-refs", type=int, default=2000)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()

    with RunLog(args.record_tag or args.tag, __file__, args,
                purpose="Attention mass arriving at the moved constituents, per layer, reference "
                        "on reference sentences. Descriptive only.") as log:
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]].drop_duplicates("ref_id")
        rng = np.random.default_rng(707)                  # the sample F5 and F6 use, for comparability
        pick = pairs.iloc[np.sort(rng.choice(len(pairs), size=min(args.n_refs, len(pairs)),
                                             replace=False))]
        refs, _ = load_trees()
        vt = set1_variants().set_index("var_id")
        model, tok, device = load_masked_lm(args.model)
        model.eval()

        acc = {}                                          # side -> [layer] running sums
        n_ok, skipped = 0, 0
        for r in pick.itertuples():
            rows = refs[r.ref_id]
            vrow = vt.loc[r.var_id]
            try:
                cls = word_classes(rows, vrow)
            except Exception:
                skipped += 1
                continue
            idx_of = tree_idx_of_word(rows)
            if not any(cls.get(i) in MOVED for i in idx_of.values()):
                skipped += 1                              # nothing moved: the ratio is undefined
                continue
            share, word_of = attention_shares(model, tok, device, text_of(rows, True))
            if share is None:
                skipped += 1
                continue
            mask = np.zeros(share.shape[1], dtype=bool)
            for p, w in word_of.items():
                ti = idx_of.get(w)
                if ti is not None and cls.get(ti) in MOVED:
                    mask[p] = True
            if not mask.any():
                skipped += 1
                continue
            # Special tokens are attention sinks in BERT-family models: a large, layer-dependent
            # share of every row lands on [CLS] and [SEP], which are not words at all. Leaving them in
            # divides the numerator by a quantity that has nothing to do with word order and pushes
            # every enrichment below 1 mechanically. Renormalise over REAL subtokens, numerator and
            # denominator alike, so the question is the one being asked: among the words, does
            # attention concentrate on the ones that moved?
            real = np.zeros(share.shape[1], dtype=bool)
            for p in word_of:
                real[p] = True
            sink = 1.0 - share[:, real].sum(1)
            share = share[:, real] / share[:, real].sum(1, keepdims=True)
            mask = mask[real]
            occupancy = mask.sum() / len(mask)
            acc.setdefault("sink", np.zeros(share.shape[0]))
            acc["sink"] += sink
            acc.setdefault("reference", np.zeros(share.shape[0]))
            acc["reference"] += share[:, mask].sum(1) / occupancy
            acc.setdefault("occupancy", 0.0)
            acc["occupancy"] += occupancy
            acc.setdefault("n", 0)
            acc["n"] += 1
            n_ok += 1
            if n_ok % 200 == 0:
                print(f"    {n_ok} pairs", flush=True)

        n = acc.pop("n")
        log.kv("references used / skipped", f"{n:,} / {skipped:,}")
        log.kv("mean share of real subtokens that are moved words", f"{acc.pop('occupancy') / n:.4f}")
        ref_e, sink = acc["reference"] / n, acc.pop("sink") / n
        table = [[i, f"{ref_e[i]:.4f}", f"{ref_e[i] - 1:+.4f}", f"{sink[i]:.4f}"]
                 for i in range(len(ref_e))]
        log.table(["layer", "enrichment on the moved constituents", "against uniform",
                   "share of attention on special tokens"], table)
        peak = int(np.argmax(ref_e))
        log.kv("layer of highest enrichment", f"{peak} ({ref_e[peak]:.4f})")
        log.note("Enrichment is attention mass on the moved constituents divided by the share of "
                 "subtokens they occupy, so 1.0 is what uniform attention gives and the number is "
                 "comparable across sentences of different lengths.")
        log.note("Descriptive only. Attention is not explanation: this can say whether the layers "
                 "where the probes read most are also where attention concentrates on the moved "
                 "material, and it cannot say that the attention causes the preference.")
        out = rc / f"{args.record_tag or args.tag}.csv"
        pd.DataFrame({"layer": np.arange(len(ref_e)), "enrichment": ref_e,
                      "special_token_share": sink}).to_csv(out, index=False)
        log.output(str(out), "per-layer attention enrichment on the moved constituents")


if __name__ == "__main__":
    main()
