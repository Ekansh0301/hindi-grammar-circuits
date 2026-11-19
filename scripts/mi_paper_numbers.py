#!/usr/bin/env python3
"""Numbers and per-condition summaries behind the paper's Results, recomputed from course_runs/outputs with numpy only.

The estimators are those of the validation stages (mi_lib.doc_bootstrap_ratio, ratio of sums over items whose gap exceeds
0.05 bits), so a value here equals the value in the run record it came from. `python3 scripts/mi_paper_numbers.py`
prints the numbers the Results quotes and writes them to course_runs/outputs/paper_numbers.json.
"""
import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "course_runs" / "outputs"
MODELS = ("muril", "xlmrlarge")
TASKS = ("object", "wordorder")
FLOOR = 0.05


# ---------------------------------------------------------------------------------------------- statistics (as mi_lib)

def boot_ratio(num, den, docs, B=2000, seed=707):
    """95% percentile interval of a ratio of sums, resampling documents."""
    num, den, d = np.asarray(num, float), np.asarray(den, float), np.asarray(docs)
    u = sorted(set(d.tolist()))
    idx = {k: i for i, k in enumerate(u)}
    ns, ds = np.zeros(len(u)), np.zeros(len(u))
    np.add.at(ns, [idx[x] for x in d], num)
    np.add.at(ds, [idx[x] for x in d], den)
    pick = np.random.default_rng(seed).integers(0, len(u), size=(B, len(u)))
    r = ns[pick].sum(1) / ds[pick].sum(1)
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def boot_mean(values, docs, B=2000, seed=707):
    """Mean of per-item values and its 95% document-bootstrap interval."""
    v, d = np.asarray(values, float), np.asarray(docs)
    ok = ~np.isnan(v)
    v, d = v[ok], d[ok]
    lo, hi = boot_ratio(v, np.ones_like(v), d, B, seed)
    return float(v.mean()), lo, hi


def signflip(values, docs, B=10000, seed=707):
    """Two-sided sign-flip permutation p of the sum of per-item values, flipping whole documents."""
    v, d = np.asarray(values, float), np.asarray(docs)
    u = {k: i for i, k in enumerate(sorted(set(d.tolist())))}
    sums = np.zeros(len(u))
    np.add.at(sums, [u[x] for x in d], v)
    null = (np.random.default_rng(seed).choice([-1.0, 1.0], size=(B, len(sums))) * sums).sum(1)
    return (1 + int((np.abs(null) >= abs(sums.sum())).sum())) / (1 + B)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows


def col(rows, name, cast=float):
    return np.array([cast(r[name]) if r[name] not in ("", "nan") else np.nan for r in rows])


# ---------------------------------------------------------------------------------------------- sets of components

def share_stats(effect, gap, docs):
    """effect (items, sets); set 0 is the set under test, the rest its comparators. Share, interval, comparators."""
    keep = np.abs(gap) > FLOOR
    sh = effect[keep].sum(0) / gap[keep].sum()
    lo, hi = boot_ratio(effect[keep, 0], gap[keep], docs[keep])
    rand = sh[1:]
    return {"share": float(sh[0]), "ci": [lo, hi], "rand_mean": float(rand.mean()) if len(rand) else None,
            "rand_p95": float(np.percentile(rand, 95)) if len(rand) else None,
            "rank": 1 + int((rand > sh[0]).sum()), "n_rand": int(len(rand)), "all": sh.tolist()}


def effects(z, task, faith="faith", nec_c="nec_clean", nec_x="nec_corrupt"):
    """Per-item faithfulness and necessity effects of every set, as the validation stages define them."""
    fc, fx = z["f_clean"], z["f_corrupt"]
    gap = fc - fx
    f_eff = z[faith] - fx[:, None]
    n_eff = (fc[:, None] - z[nec_c]) if task == "object" else (gap[:, None] - (z[nec_c] - z[nec_x]))
    return gap, f_eff, n_eff, z["docs"]


def validate(task, model):
    z = np.load(OUT / f"validate_{task}_{model}.npz", allow_pickle=True)
    gap, f_eff, n_eff, docs = effects(z, task)
    return {"faithfulness": share_stats(f_eff, gap, docs), "necessity": share_stats(n_eff, gap, docs)}


def setsize(task, model):
    z = np.load(OUT / f"setsize_{task}_{model}.npz", allow_pickle=True)
    fc, fx = z["f_clean"], z["f_corrupt"]
    gap = fc - fx
    out = {}
    for K in (int(k) for k in z["Ks"]):
        sub = {"faith": z[f"faith_K{K}"], "nec_clean": z[f"nec_clean_K{K}"], "nec_corrupt": z[f"nec_corrupt_K{K}"],
               "f_clean": fc, "f_corrupt": fx, "docs": z["docs"]}
        g, fe, ne, docs = effects(sub, task)
        out[K] = {"faithfulness": share_stats(fe, g, docs), "necessity": share_stats(ne, g, docs)}
        if f"zero_clean_K{K}" in z.files:
            zz = dict(sub, nec_clean=z[f"zero_clean_K{K}"], nec_corrupt=z[f"zero_corrupt_K{K}"])
            _, _, nz, _ = effects(zz, task)
            out[K]["necessity_zero"] = share_stats(nz, g, docs)
    return out


def mlpsets(task, model):
    z = np.load(OUT / f"mlpsets_{task}_{model}.npz", allow_pickle=True)
    fc, fx = z["f_clean"], z["f_corrupt"]
    gap = fc - fx
    docs = z["docs"]
    keep = np.abs(gap) > FLOOR
    f_eff = z["faith"] - fx[:, None]
    f_sh = f_eff[keep].sum(0) / gap[keep].sum()
    lo, hi = boot_ratio(f_eff[keep, 0], gap[keep], docs[keep])
    idx = z["nec_idx"]
    nec = (fc[:, None] - z["nec_clean"]) if task == "object" else (gap[:, None] - (z["nec_clean"] - z["nec_corrupt"]))
    n_sh = nec[keep].sum(0) / gap[keep].sum()
    nlo, nhi = boot_ratio(nec[keep, 0], gap[keep], docs[keep])
    ov = z["overlap"]
    return {"faith": {"share": float(f_sh[0]), "ci": [lo, hi], "others_mean": float(f_sh[1:].mean()),
                      "others_p95": float(np.percentile(f_sh[1:], 95)), "rank": 1 + int((f_sh[1:] > f_sh[0]).sum()),
                      "n_others": int(len(f_sh) - 1), "within_0.02": int((np.abs(f_sh[1:] - f_sh[0]) <= 0.02).sum()),
                      "by_overlap": {int(o): float(f_sh[1:][ov[1:] == o].mean()) for o in sorted(set(ov[1:].tolist()))}},
            "necessity": {"share": float(n_sh[0]), "ci": [nlo, nhi], "others_mean": float(n_sh[1:].mean()),
                          "others_p95": float(np.percentile(n_sh[1:], 95)), "rank": 1 + int((n_sh[1:] > n_sh[0]).sum()),
                          "n_others": int(len(n_sh) - 1)}}


# ---------------------------------------------------------------------------------------------- agreement reading tests

def ko(model):
    rows = read_csv(OUT / f"ko_{model}.csv")
    docs = np.array([r["doc"] for r in rows])
    res = {"orders": len(rows)}
    for v in ("none", "bhi", "ko"):
        m = col(rows, f"Magree_{v}")
        res[v] = {"magree": list(boot_mean(m, docs)), "prefers_object_form": float((m > 0).mean()),
                  "att_object": float(np.nanmean(col(rows, f"attobject5_{v}")))}
    res["ko"]["prefers_default"] = float((col(rows, "Magree_ko") < 0).mean())
    return res


def role_swap(model):
    rows = read_csv(OUT / f"role_swap_{model}.csv")
    res = {}
    for stratum, sel in (("all", lambda r: True), ("not_default", lambda r: r["swapcorrect_default"] == "False")):
        rr = [r for r in rows if sel(r)]
        docs = np.array([r["doc"] for r in rr])
        for cls in ("SOV", "OSV"):
            c = [i for i, r in enumerate(rr) if r["order_class"] == cls]
            d = docs[c]
            ms = col([rr[i] for i in c], "M_swap")
            mo = col([rr[i] for i in c], "M_orig")
            res[f"{stratum}_{cls}"] = {"n": len(c), "swap": list(boot_mean(ms, d)), "orig": list(boot_mean(mo, d)),
                                       "p": signflip(ms, d), "swap_positive": float((ms > 0).mean())}
    return res


def swap_mask(model):
    rows = read_csv(OUT / f"swap_mask_{model}.csv")
    res = {}
    for stratum, sel in (("all", lambda r: True), ("not_default", lambda r: r["swapcorrect_default"] == "False")):
        rr = [r for r in rows if sel(r)]
        docs = np.array([r["doc"] for r in rr])
        for cls in ("SOV", "OSV"):
            c = [i for i, r in enumerate(rr) if r["order_class"] == cls]
            d, sub = docs[c], [rr[i] for i in c]
            cell = {"n": len(c)}
            for cond in ("none", "obj", "subj", "ne"):
                cell[cond] = list(boot_mean(col(sub, f"M_swap_{cond}"), d))
            for cond in ("obj", "subj", "ne"):
                cell[f"R_{cond}"] = list(boot_mean(col(sub, f"M_swap_{cond}") - col(sub, "M_swap_none"), d))
            res[f"{stratum}_{cls}"] = cell
    return res


def main():
    out = {"validate": {t: {m: validate(t, m) for m in MODELS} for t in TASKS},
           "setsize": {t: {m: setsize(t, m) for m in MODELS} for t in TASKS},
           "mlpsets": {t: {m: mlpsets(t, m) for m in MODELS} for t in TASKS},
           "ko": {m: ko(m) for m in MODELS}, "role_swap": {m: role_swap(m) for m in MODELS},
           "swap_mask": {m: swap_mask(m) for m in MODELS}}
    p = OUT / "paper_numbers.json"
    p.write_text(json.dumps(out, indent=1))
    for t in TASKS:
        for m in MODELS:
            v = out["validate"][t][m]
            print(f"validate {t:9s} {m:9s} faith {v['faithfulness']['share']:.3f} {v['faithfulness']['ci'][0]:.3f},"
                  f"{v['faithfulness']['ci'][1]:.3f} rand {v['faithfulness']['rand_mean']:.3f} | nec {v['necessity']['share']:.3f}"
                  f" {v['necessity']['ci'][0]:.3f},{v['necessity']['ci'][1]:.3f} rand {v['necessity']['rand_mean']:.3f}")
    print("wrote", p)


if __name__ == "__main__":
    main()
