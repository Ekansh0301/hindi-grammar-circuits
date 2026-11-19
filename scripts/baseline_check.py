#!/usr/bin/env python3
"""Recompute the three preliminary checks of the proposal from the data in data/.

Needs only numpy and pandas. Run from the project folder:  python3 scripts/baseline_check.py

  1. word-order baseline: share of the 8,923 written-reordered pairs in which the model finds the written sentence less
     surprising (mean word-level pseudo-log-likelihood surprisal; data/word_order/)
  2. agreement baseline: share of the 5,265 orders in which the correct verb is more probable than the subject-agreeing
     one, margin A = sum_foil - sum_correct (bits; data/agreement/)
  3. intervening subject: within a clause and at the same object-verb distance, mean A of orders where the subject stands
     between object and verb (OSV-type) minus orders where it does not (SOV-type), over variant orders whose object is
     not adjacent to the verb; averaged per clause and tested with a document-level sign-flip permutation (10,000)

Expected output: 0.8204 / 0.8090; 0.9364 / 0.9493; 102 clauses, -1.7468 bits, p = 1e-4 / -0.2120 bits, p ~ 0.58.
"""
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent.parent / "data"
MODELS = {"muril": 0, "xlmrlarge": 2}   # the seed index each model had in the original four-model run


def word_order(m):
    pairs = pd.read_csv(D / "word_order" / "pairs.csv")[["ref_id", "var_id"]]
    t = pd.concat(pd.read_csv(D / "word_order" / f"t_{m}_within_word_l2r_s{s}.csv",
                              usecols=["ref_id", "var_id", "ref_Mean", "var_Mean"]) for s in (0, 1))
    x = pairs.merge(t.drop_duplicates(["ref_id", "var_id"]), on=["ref_id", "var_id"], validate="one_to_one")
    return len(x), float((x.ref_Mean < x.var_Mean).mean())


def agreement(m, k_m, permutations=10000, seed=707):
    d = pd.read_csv(D / "agreement" / "agreement_items.csv")
    sc = pd.read_csv(D / "agreement" / f"agreement_scores_{m}.csv")
    x = d.merge(sc, on=["ref_id", "order_id"], validate="one_to_one").dropna(subset=["sum_correct", "sum_foil"])
    x["A"] = x.sum_foil - x.sum_correct
    z = x[~x.is_reference & ~x.object_adjacent]
    g = z.groupby(["ref_id", "clause_head", "object_verb_gap", "order_class"]).A.mean().unstack().dropna(subset=["OSV", "SOV"])
    cell = (g["OSV"] - g["SOV"]).groupby(level=["ref_id", "clause_head"]).mean()
    sums = cell.groupby([r.split("__")[0] for r, _ in cell.index]).sum().to_numpy()
    rng = np.random.default_rng([seed, k_m])
    null = np.array([(sums * rng.choice([-1.0, 1.0], len(sums))).sum() for _ in range(permutations)])
    p = (1 + int((np.abs(null) >= abs(sums.sum())).sum())) / (1 + permutations)
    return len(x), float((x.A > 0).mean()), len(cell), float(cell.mean()), p


if __name__ == "__main__":
    for m, k in MODELS.items():
        n, wo = word_order(m)
        na, ag, nc, eff, p = agreement(m, k)
        print(f"{m:10s} word order {wo:.4f} ({n} pairs) | correct verb {ag:.4f} ({na} orders) | "
              f"intervening subject {eff:+.4f} bits over {nc} clauses, p = {p:.4g}")
