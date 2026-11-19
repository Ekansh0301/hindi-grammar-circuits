#!/usr/bin/env python3
"""Surprisal preference layer by layer (PREREGISTRATION_DRAFT.md 7.2; RQ1_WORK_PLAN.md F2).

From the logit-lens columns of words_<model>_s*_part*.csv.gz (lens_0 = embedding output, last =
final layer, which equals the model's surprisal): for every layer, the pair difference
D_layer = Σ_words [lens_var − lens_ref] and the share of pairs with D_layer > 0 (the reference is
preferred), overall and within each word class of rq1_word_attribution.py (share of pairs whose
class contribution is positive, among pairs where the class has words).

Layers are marked unreadable when readability_<model>.csv (rq1_lm_units.py --what readability) puts
them more than 2 nats per subtoken above the final layer; shares on unreadable layers are reported
but not read. A layer the readability file does not list, and every layer when the file is missing,
counts as unreadable: readability has to be shown, not assumed. Reported: the first readable layer at
which the share reaches 90% of its final-layer value (share − 0.5 scaled, so chance is 0 and the final
layer is 1).
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from hutb_corpus import BASE, FC, parse_conllu, set1_variants
from rq1_word_attribution import CLASSES, word_classes
from runlog import RunLog


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--words-dir", default=str(rc / "lm_units"))
    ap.add_argument("--out", default=str(rc / "rq1_lens_layers.csv"))
    ap.add_argument("--tag", default="rq1_lens_analysis")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args, purpose="At which layer does each model's preference for the reference "
                                                  "appear, overall and by word class?") as log:
        refs = parse_conllu(FC / "reference_trees.conllu", 8)
        V = set1_variants().set_index("var_id")
        allrows, cls_cache = [], {}
        for m in args.models:
            files = sorted(glob.glob(f"{args.words_dir}/words_{m}_s*_part*.csv.gz"))
            if not files:
                log.note(f"{m}: no word files")
                continue
            w = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
            lens = sorted([c for c in w.columns if c.startswith("lens_")], key=lambda c: int(c.split("_")[1]))
            if (w[lens[-1]] - w.s).abs().max() > 0.01:
                raise SystemExit(f"{m}: final lens layer does not reproduce the surprisal")
            rd = Path(args.words_dir) / f"readability_{m}.csv"
            # No file, or a layer it does not list: unreadable, never readable by default.
            readable = (pd.read_csv(rd).set_index("layer").readable == "yes").to_dict() if rd.exists() else {}
            for key in w[["ref_id", "var_id"]].drop_duplicates().itertuples(index=False):
                if key not in cls_cache:
                    cls_cache[key] = word_classes(refs[key.ref_id], V.loc[key.var_id])
            w["cls"] = [cls_cache[(r, v)][int(i)] for r, v, i in zip(w.ref_id, w.var_id, w.tree_idx)]
            sign = np.where(w.side == "var", 1.0, -1.0)
            for c in lens:
                w[c] = w[c] * sign
            per_pair = w.groupby(["ref_id", "var_id"])[lens].sum()
            per_cls = w.groupby(["ref_id", "var_id", "cls"])[lens].sum()
            log.h2(f"model: {m}")
            log.kv("pairs", f"{len(per_pair):,}")
            log.kv("readability file", str(rd) if rd.exists() else "missing: every layer reported, none read")
            groups = [("all words", per_pair)] + [(c, per_cls.xs(c, level="cls")) for c in CLASSES[:-1]
                                                  if c in per_cls.index.get_level_values("cls")]
            table, first = [], []
            for label, frame in groups:
                shares = (frame > 0).mean().to_numpy()
                final = shares[-1]
                scaled = (shares - 0.5) / (final - 0.5) if final != 0.5 else np.full_like(shares, np.nan)
                ok = [i for i in range(len(lens)) if readable.get(i, False) and scaled[i] >= 0.9]
                first.append([label, len(frame), final, ok[0] if ok else "none"])
                for i, sh in enumerate(shares):
                    allrows.append([m, label, i, sh, readable.get(i, False)])
                table.append([label] + [f"{x:.2f}{'' if readable.get(i, False) else '*'}" for i, x in enumerate(shares)])
            log.table(["words", "pairs", "final-layer share", "first readable layer at 90%"], first, floatfmt="{:.3f}")
            log.table(["words"] + [str(i) for i in range(len(lens))], table)
            log.p("Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.")
        pd.DataFrame(allrows, columns=["model", "words", "layer", "share", "readable"]).to_csv(args.out, index=False)
        log.output(args.out, "reference-preferred share per model, word class and layer")


if __name__ == "__main__":
    main()
