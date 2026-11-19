#!/usr/bin/env python3
"""Does surprisal read from a middle layer carry more structure than the model's own surprisal?

The layer analysis (F1, F3, F5) shows that order and structure are most decodable in the upper-middle
layers and fade towards the output, while the behaviour — surprisal — is read only at the output. Those
two facts are in different currencies, so "the representation has it and the behaviour does not" has been
an inference rather than a measurement.

Following Kuribayashi et al. (TACL 2025), this puts both in the same currency. The logit lens gives a
surprisal at every layer; each layer's surprisal is entered as T in the four-block decomposition, exactly
as the model's own surprisal is. Then for every layer we can read:

  ΔR²(T_layer | L,S)     how much that layer's surprisal adds to word statistics and memory cost
  absorbed share          how much of that a structure-only order model also supplies
  ΔAUC over L+S+E1        what is left

If middle-layer surprisal adds more than the final layer's, or if its absorbed share differs, the
dissociation is measured in behavioural terms rather than inferred from a probe. Layers are marked
unreadable by the declared 2-nat rule (`readability_<model>.csv`) and reported but not read, as in F2.

Input: the per-word lens columns already written by `rq1_lm_units.py --what words` (`lens_0` … `lens_N`);
no rescoring, CPU only. `--lens tuned` reads the tuned-lens columns instead, which is the version that can
be read: under the declared 2-nat rule the logit lens leaves **only the final layer readable** for MuRIL
and mBERT, while the tuned lens opens layers 8-12 and 1-12 respectively.

**A caveat that belongs with any tuned-lens result.** Anthropic's Jacobian lens paper (July 2026) argues
that the tuned lens, being optimised for correlational fit with the output distribution, tends to "skip
ahead" to the output rather than surface what an intermediate layer itself carries. If that is right, a
tuned-lens curve that rises smoothly with depth partly reflects the translator's fit rather than the
layer. The J-lens is the principled correction and is on the future plan (RQ1_WORK_PLAN.md M); until it is
run, layer-wise surprisal is reported as lens-dependent and the two lenses are reported side by side.
"""
import argparse
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from dominance_analysis import fit_subset, nagelkerke_r2
from hutb_corpus import BASE
from rq1_dominance import SPEC_L, SPEC_S, auc_fast, cluster_bootstrap_auc_diff, cv_predict
from runlog import RunLog


def expand(d, cols):
    X = d[cols].to_numpy(float)
    g = d.ref_id.to_numpy()
    return np.vstack([X, -X]), np.r_[np.ones(len(d)), np.zeros(len(d))], np.r_[g, g]


def r2(d, cols):
    e = pd.DataFrame(np.vstack([d[cols].to_numpy(float), -d[cols].to_numpy(float)]), columns=cols)
    e["y"] = np.r_[np.ones(len(d)), np.zeros(len(d))]
    llnull, _ = fit_subset(e, "y", [])
    return nagelkerke_r2(fit_subset(e, "y", cols)[0], llnull, len(e))


def layer_differences(words_dir, model, lens="logit"):
    """Per pair, the reference-minus-variant mean per-word surprisal at every lens layer."""
    stem = model if lens == "logit" else f"{model}_{lens}"
    files = sorted(glob.glob(f"{words_dir}/words_{stem}_s*_part*.csv.gz"))
    if not files:
        raise SystemExit(f"no per-word files for {model}")
    head = pd.read_csv(files[0], nrows=1)
    lens = sorted((c for c in head.columns if c.startswith("lens_")), key=lambda c: int(c[5:]))
    keep = ["ref_id", "var_id", "side"] + lens
    d = pd.concat((pd.read_csv(f, usecols=keep) for f in files), ignore_index=True)
    g = d.groupby(["ref_id", "var_id", "side"])[lens].mean().reset_index()
    ref = g[g.side == "ref"].drop(columns="side")
    var = g[g.side == "var"].drop(columns="side")
    m = ref.merge(var, on=["ref_id", "var_id"], suffixes=("_ref", "_var"))
    out = m[["ref_id", "var_id"]].copy()
    for c in lens:
        out[c] = m[f"{c}_ref"] - m[f"{c}_var"]
    return out, lens


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--models", nargs="+", default=["muril", "indicbert", "mbert", "xlmrlarge"])
    ap.add_argument("--words-dir", default=str(rc / "lm_units"))
    ap.add_argument("--lens", default="logit", choices=["logit", "tuned", "jacobian"],
                    help="which lens's per-word columns to read. The logit lens leaves only the final "
                         "layer readable for MuRIL and mBERT; the tuned lens opens most of the depth but is "
                         "fitted to the output; the Jacobian lens (rq1_jacobian_lens.py, M4) reads each "
                         "layer through the model's own average map to the output, fitted to nothing")
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--tag", default="rq1_layerwise_decomposition")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="The four-block decomposition with surprisal read from every layer, not only "
                        "the output.") as log:
        feats = pd.read_csv(rc / "rq1_features_all.csv").merge(
            pd.read_csv(rc / "rq1_features_units.csv"), on=["ref_id", "var_id"])
        summary = []
        for m in args.models:
            diffs, lens = layer_differences(args.words_dir, m, args.lens)
            read = {}
            suffix = "" if args.lens == "logit" else f"_{args.lens}"
            rf = Path(args.words_dir) / f"readability_{m}{suffix}.csv"
            if rf.exists():
                r = pd.read_csv(rf)
                # readability_<model>.csv carries the declared 2-nat rule's verdict per layer
                read = {int(k): str(v).strip().lower() in ("yes", "true")
                        for k, v in zip(r.layer, r["readable"])}
            d = feats.merge(diffs, on=["ref_id", "var_id"])
            L = [c for c in SPEC_L if d[c].nunique() > 1]
            base = L + list(SPEC_S)
            withE = base + ["d_syn_order"]
            d = d.dropna(subset=withE + lens).reset_index(drop=True)
            n = len(d)
            log.h2(f"model: {m}")
            log.kv("pairs / lens layers / lens", f"{n:,} / {len(lens)} / {args.lens}")
            log.kv("readable layers", ", ".join(str(k) for k in sorted(read) if read[k]) or "final only")
            X0, y, g = expand(d, base)
            XE, _, _ = expand(d, withE)
            pE = cv_predict(XE, y, g)
            r_base, r_E = r2(d, base), r2(d, withE)
            rows = []
            for c in lens:
                k = int(c[5:])
                dT = r2(d, base + [c]) - r_base
                dTE = r2(d, withE + [c]) - r_E
                share = 1 - dTE / dT if dT > 1e-9 else float("nan")
                Xl, _, _ = expand(d, withE + [c])
                pl = cv_predict(Xl, y, g)
                dd, lo, hi, _ = cluster_bootstrap_auc_diff(y, pl, pE, n, B=args.bootstrap)
                rows.append([k, "yes" if read.get(k, k == len(lens) - 1) else "no",
                             dT, dTE, share, dd, lo, hi])
            log.table(["layer", "readable", "ΔR²(T_layer | L,S)", "ΔR²(T_layer | L,S,E1)",
                       "absorbed share", "ΔAUC over L+S+E1", "95% low", "95% high"], rows,
                      floatfmt="{:.4f}")
            fin = rows[-1]
            best = max(rows, key=lambda r: r[2])
            log.kv("final layer: ΔR²(T|L,S), absorbed share", f"{fin[2]:.4f}, {fin[4]:.3f}")
            log.kv("layer with the largest ΔR²(T|L,S)",
                   f"{best[0]} ({best[2]:.4f}, absorbed share {best[4]:.3f}, readable: {best[1]})")
            summary.append([m, fin[2], fin[4], best[0], best[2], best[4]])
        if summary:
            log.h2("Summary")
            log.table(["model", "final ΔR²(T|L,S)", "final absorbed share", "best layer",
                       "its ΔR²(T|L,S)", "its absorbed share"], summary, floatfmt="{:.4f}")
            log.p("The dissociation the layer probes suggest would show here as a middle layer whose "
                  "surprisal adds more than the output's, or whose absorbed share is lower — structure "
                  "present in the representation and spent by the time the model speaks. Read only the "
                  "layers marked readable; the rest are reported because hiding them would make the "
                  "readable ones look like a choice.")


if __name__ == "__main__":
    main()
