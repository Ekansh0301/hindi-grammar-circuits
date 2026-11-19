#!/usr/bin/env python3
"""Follow-up experiment 3, the comparison (docs/FOLLOWUP_EXPERIMENTS.md): step 4 as run (components chosen on the
selection half, validated on the held-out half) against the same stages with the halves swapped (mi_swap.py:
chosen on the held-out half, validated on the selection half). CPU; reads outputs only; runs on Ada (needs mi_lib,
hence torch) or anywhere torch is installed. Declared before any run (27 Oct 2026).

Per task (object agreement, word order) and model:
  CIRCUITS  the top 10 heads and the top 5 MLPs of the exact stage in each direction, the overlap (heads in both
            of 10; MLPs in both of 5; every one of them listed), the Spearman correlation of the exact shares over
            the components patched in both directions (object task: every component; word order: the components
            both exact stages patched, which are every MLP and the heads either chose or drew)
  VALIDATION  faithfulness and necessity of the 10 heads on the half not used for choosing them, in each direction,
            beside 100 random head sets matched by block: circuit share, document-bootstrap 95% interval, random
            mean and 95th percentile, rank among random sets, document sign-flip p; computed exactly as the stages
            compute them from the saved arrays
  The top 5 MLPs' shares on the validation half, in each direction.
DECLARED READING (before the runs): the circuits are 'stable under the swap' if, in both tasks and both models, the
swapped validation's faithfulness is within 0.10 of step 4's and ranks first among the random sets, and at least 6
of the 10 heads and 3 of the 5 MLPs are shared. Otherwise the record lists which part failed and the report says
so: a circuit that depends on the split is a finding, not a defect to hide.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_lib as M  # noqa: E402
from runlog import RunLog  # noqa: E402

MODELS = ("muril", "xlmrlarge")
TASKS = ("object", "wordorder")


def exact_shares(path, min_gap=0.05):
    e = np.load(path)
    keep = np.abs(e["f_clean"] - e["f_corrupt"]) > min_gap
    share = (e["exact"] - e["f_corrupt"][:, None])[keep].sum(0) / (e["f_clean"] - e["f_corrupt"])[keep].sum()
    names = list(e["comps"])
    if "idx" in e.files:                       # word order: a subset of the components, by index into comps
        return {names[i]: float(s) for i, s in zip(e["idx"], share)}
    return {n: float(s) for n, s in zip(names, share)}


def top(shares, kind, k):
    ranked = sorted(shares, key=lambda n: -shares[n])
    return [n for n in ranked if (("MLP" in n) == (kind == "mlp"))][:k]


def validation(path, task, min_gap=0.05):
    v = np.load(path)
    fc, fx, docs = v["f_clean"], v["f_corrupt"], v["docs"]
    gap = fc - fx
    keep = np.abs(gap) > min_gap
    faith = v["faith"]
    if task == "object":
        lost = fc[:, None] - v["nec_clean"]
    else:
        lost = gap[:, None] - (v["nec_clean"] - v["nec_corrupt"])
    out = {}
    for name, per_item in (("faithfulness", faith - fx[:, None]), ("necessity", lost)):
        sh = per_item[keep].sum(0) / gap[keep].sum()
        rank_p = (1 + int((sh[1:] >= sh[0]).sum())) / (1 + len(sh) - 1)
        diff = (per_item[:, 0] - per_item[:, 1:].mean(1))[keep]
        lo, hi = M.doc_bootstrap_ratio(per_item[keep, 0], gap[keep], docs[keep])
        out[name] = (float(sh[0]), (lo, hi), float(sh[1:].mean()), float(np.percentile(sh[1:], 95)), rank_p,
                     M.doc_signflip(diff, docs[keep]))
    mlp = {str(n): float((v["mlp_heldout"][:, i] - fx)[keep].sum() / gap[keep].sum()) for i, n in enumerate(v["mlp_names"])}
    return out, mlp, str(v["sets"][0]).split("|"), int(keep.sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--record-tag", default="mi_swap_compare")
    args = ap.parse_args()
    out4 = M.ROOT / "course_runs" / "outputs"
    outs = out4 / "swap"
    with RunLog(args.record_tag, __file__, args, purpose="Follow-up 3: step 4 against the halves swapped.") as log:
        stable = {}
        for task in TASKS:
            for m in MODELS:
                a = exact_shares(out4 / f"exact_{task}_{m}.npz")
                b = exact_shares(outs / f"exact_{task}_{m}.npz")
                common = sorted(set(a) & set(b))
                from scipy.stats import spearmanr
                rho = float(spearmanr([a[n] for n in common], [b[n] for n in common]).correlation)
                h4, h5 = top(a, "head", 10), top(b, "head", 10)
                m4, m5 = top(a, "mlp", 5), top(b, "mlp", 5)
                vo, mo, circ_o, n_o = validation(out4 / f"validate_{task}_{m}.npz", task)
                vs, ms, circ_s, n_s = validation(outs / f"validate_{task}_{m}.npz", task)
                log.h2(f"{task}, {m}")
                log.table(["", "step 4 (chosen on selection, validated on held-out)", "swapped (chosen on held-out, validated on selection)"],
                          [["top 10 heads", ", ".join(h4), ", ".join(h5)], ["top 5 MLPs", ", ".join(m4), ", ".join(m5)],
                           ["10 heads validated (the circuit)", ", ".join(circ_o), ", ".join(circ_s)]])
                shared_h, shared_m = len(set(h4) & set(h5)), len(set(m4) & set(m5))
                log.kv("heads in both of 10 / MLPs in both of 5 / Spearman of exact shares over the components both patched",
                       f"{shared_h} / {shared_m} / {rho:.3f} (over {len(common)} components)")
                rows = []
                for q in ("faithfulness", "necessity"):
                    for lab, v in (("step 4", vo), ("swapped", vs)):
                        s, ci, rm, r95, rp, sp = v[q]
                        rows.append([q, lab, s, f"[{ci[0]:.3f}, {ci[1]:.3f}]", rm, r95, rp, sp])
                log.table(["test", "direction", "circuit", "document bootstrap 95%", "random mean", "random 95th percentile",
                           "rank p among random sets", "document sign-flip p"], rows, floatfmt="{:.4g}")
                log.table(["MLP of the validation direction", "share on its validation half"],
                          [[f"step 4: {n}", s] for n, s in mo.items()] + [[f"swapped: {n}", s] for n, s in ms.items()])
                f_o, f_s = vo["faithfulness"], vs["faithfulness"]
                ok = abs(f_o[0] - f_s[0]) <= 0.10 and f_s[4] <= 1.5 / 101 and shared_h >= 6 and shared_m >= 3
                stable[(task, m)] = (ok, abs(f_o[0] - f_s[0]), f_s[4], shared_h, shared_m)
        log.h2("Declared reading")
        log.table(["task", "model", "stable", "faithfulness differs by", "swapped rank p", "heads shared of 10", "MLPs shared of 5"],
                  [[t, m, "yes" if v[0] else "NO", v[1], v[2], v[3], v[4]] for (t, m), v in stable.items()], floatfmt="{:.4g}")
        log.kv("DECISION (declared: within 0.10, ranks first, at least 6 heads and 3 MLPs shared, in every task and model)",
               "stable under the swap" if all(v[0] for v in stable.values()) else
               "not in every case: " + ", ".join(f"{t}/{m}" for (t, m), v in stable.items() if not v[0]))


if __name__ == "__main__":
    main()
