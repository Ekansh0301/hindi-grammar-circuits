#!/usr/bin/env python3
"""Per-word hidden states: structural distance probe and representational similarity
(PREREGISTRATION_DRAFT.md 7.3 tier 2, 7.4; RQ1_WORK_PLAN.md F5, F6). Masked LMs; one GPU job per model.

Data: the 2,000 sample references of the unit-state extraction (seed 707) and their sample variants.
Word states are the mean of each whitespace word's subtoken states per layer, plus the same mean of the
pre-LayerNorm embedding sum (the layer-0 control of 7.1). States are held in memory only.

F5, structural distance probe (Hewitt and Manning 2019). For each layer, a rank-64 matrix B such that
||B(h_i − h_j)||² approximates the tree distance between words i and j of the reference (distances in the
full tree, NULL nodes included in paths; NULL words themselves excluded). L1 loss normalised by the
number of word pairs, Adam (lr 1e-3), 20 epochs, seed 707. Training on references of 80% of documents,
evaluation on the rest (document hash). Reported: mean Spearman correlation of predicted and gold
distances over held-out sentences of 5 to 50 words, and UUAS of the minimum spanning tree against the gold
undirected edges between surface words. Control: the same probe on the pre-LayerNorm input.

F6, similarity. For each layer, words of a reference and its variant are matched by reference tree index;
reported: linear CKA between the stacked matched word vectors (all pairs), and the mean cosine of matched
words, overall and separately for words of moved and unmoved units (classes of rq1_word_attribution.py).
"""
import argparse
import hashlib
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch

import lm_units as U
from hutb_corpus import BASE, load_trees, set1_variants, text_of
from materialise_set1 import official_tokens
from pll_scorer import load_masked_lm
from rq1_word_attribution import word_classes
from runlog import RunLog


def word_states(model, tok, device, text):
    ts = U.token_states(model, tok, device, text)
    if ts is None:
        return None
    hs, pre, word_of = ts
    nw = len(text.split(" "))
    groups = [[] for _ in range(nw)]
    for p, w in word_of.items():
        groups[w].append(p)
    if any(not g for g in groups):
        return None
    H = torch.stack([hs[:, g].mean(1) for g in groups], 1).half().numpy()      # layers x words x d
    P = torch.stack([pre[g].mean(0) for g in groups]).half().numpy()           # words x d
    return H, P


def tree_distances(ref_rows):
    toks = official_tokens(ref_rows)
    adj = {t["idx"]: set() for t in toks}
    for t in toks:
        if t["head"]:
            adj[t["idx"]].add(t["head"])
            adj[t["head"]].add(t["idx"])
    surface = [t["idx"] for t in toks if t["form"].strip().upper() != "NULL"]
    D = np.zeros((len(surface), len(surface)), dtype=np.float32)
    for a, s in enumerate(surface):
        dist = {s: 0}
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)
        D[a] = [dist[x] for x in surface]
    edges = {frozenset((a, b)) for a in range(len(surface)) for b in range(a + 1, len(surface)) if D[a, b] == 1}
    return D, edges


def mst_edges(pred):
    n = len(pred)
    inside, edges = {0}, set()
    best = pred[0].copy()
    parent = np.zeros(n, dtype=int)
    for _ in range(n - 1):
        cand = [(best[j], j) for j in range(n) if j not in inside]
        _, j = min(cand)
        edges.add(frozenset((parent[j], j)))
        inside.add(j)
        upd = pred[j] < best
        best = np.where(upd, pred[j], best)
        parent = np.where(upd, j, parent)
    return edges


def spearman(a, b):
    ra, rb = pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy()
    return float(np.corrcoef(ra, rb)[0, 1])


def linear_baseline(D_eval, E_eval):
    """Predicted distance |i - j| (surface order only): the Spearman and UUAS a probe must beat."""
    rhos, correct, total = [], 0, 0
    for D, E in zip(D_eval, E_eval):
        n = len(D)
        pred = np.abs(np.subtract.outer(np.arange(n), np.arange(n))).astype(float)
        if 5 <= n <= 50:
            iu = np.triu_indices(n, 1)
            rhos.append(spearman(pred[iu], D[iu]))
        correct += len({frozenset((i, i + 1)) for i in range(n - 1)} & E)
        total += len(E)
    return float(np.nanmean(rhos)), correct / max(total, 1)


def train_probe(X_train, D_train, X_eval, D_eval, E_eval, device, rank=64, epochs=20, standardise=False, losses=None):
    torch.manual_seed(707)
    if standardise == "dims":
        allw = np.concatenate(X_train)
        mu, sd = allw.mean(0), allw.std(0) + 1e-6
        X_train = [(x - mu) / sd for x in X_train]
        X_eval = [(x - mu) / sd for x in X_eval]
    elif standardise == "norm":
        allw = np.concatenate(X_train)
        mu = allw.mean(0)
        scale = float(np.sqrt(((allw - mu) ** 2).sum(1).mean()))
        X_train = [(x - mu) / scale for x in X_train]
        X_eval = [(x - mu) / scale for x in X_eval]
    d = X_train[0].shape[1]
    B = torch.nn.Parameter(torch.randn(rank, d, device=device) * 0.01)
    opt = torch.optim.Adam([B], lr=1e-3)
    for ep in range(epochs):
        ep_loss = 0.0
        for i in np.random.default_rng(707).permutation(len(X_train)):
            h = torch.tensor(X_train[i], device=device, dtype=torch.float32) @ B.T
            diff = h[:, None, :] - h[None, :, :]
            pred = (diff ** 2).sum(-1)
            gold = torch.tensor(D_train[i], device=device)
            n = len(gold)
            loss = (pred - gold).abs().sum() / (n * n)
            opt.zero_grad()
            loss.backward()
            opt.step()
            ep_loss += loss.item()
        if losses is not None:
            losses.append(ep_loss / len(X_train))
    rhos, correct, total = [], 0, 0
    with torch.no_grad():
        for X, D, E in zip(X_eval, D_eval, E_eval):
            h = torch.tensor(X, device=device, dtype=torch.float32) @ B.T
            pred = ((h[:, None, :] - h[None, :, :]) ** 2).sum(-1).cpu().numpy()
            n = len(D)
            if 5 <= n <= 50:
                iu = np.triu_indices(n, 1)
                rhos.append(spearman(pred[iu], D[iu]))
            correct += len(mst_edges(pred) & E)
            total += len(E)
    return float(np.nanmean(rhos)), correct / max(total, 1)


def linear_cka(X, Y):
    X = X - X.mean(0)
    Y = Y - Y.mean(0)
    return float(np.linalg.norm(Y.T @ X) ** 2 / (np.linalg.norm(X.T @ X) * np.linalg.norm(Y.T @ Y)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    rc = BASE / "Results_Checks"
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--pairs", default=str(rc / "rq1_sample_n12000.csv"))
    ap.add_argument("--n-refs", type=int, default=2000)
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--record-tag", default=None)
    ap.add_argument("--standardise", default="none", choices=["none", "dims", "norm"],
                    help="dims: z-score each dimension; norm: centre and divide by the mean vector norm (deviation 6.6.4)")
    ap.add_argument("--only-f5", action="store_true")
    ap.add_argument("--geometry", action="store_true",
                    help="diagnostic: per layer, the share of variance in the top 1 and top 5 dimensions")
    ap.add_argument("--drop-top-dims", type=int, default=0,
                    help="diagnostic: train F5 with the K highest-variance dimensions (from training "
                         "references) removed; reported as a diagnostic, never in place of the declared probe")
    ap.add_argument("--layers", type=int, nargs="+", default=None, help="F5 on these layers only")
    args = ap.parse_args()
    with RunLog(args.record_tag or f"rq1_word_state_probes_{args.tag}", __file__, args,
                purpose="Structural distance probe and reference-variant similarity per layer.") as log:
        pairs = pd.read_csv(args.pairs)[["ref_id", "var_id"]].drop_duplicates("ref_id")
        rng = np.random.default_rng(707)
        pick = pairs.iloc[np.sort(rng.choice(len(pairs), size=min(args.n_refs, len(pairs)), replace=False))]
        refs, vars_ = load_trees()
        V = set1_variants().set_index("var_id")
        model, tok, device = load_masked_lm(args.model)
        L = model.config.num_hidden_layers + 1
        data = []
        for r in pick.itertuples():
            rt, vtr = refs[r.ref_id], vars_[r.var_id]
            a = word_states(model, tok, device, text_of(rt, True))
            b = word_states(model, tok, device, text_of(vtr, False))
            if a is None or b is None:
                continue
            ridx, vidx = U.set1_surface_indices(rt, V.loc[r.var_id].to_dict() | {"var_id": r.var_id}, vtr)
            D, E = tree_distances(rt)
            cls = word_classes(rt, V.loc[r.var_id])
            doc = r.ref_id.split("__")[0]
            held = int(hashlib.sha256(doc.encode()).hexdigest()[:8], 16) % 5 == 0
            data.append(dict(ref=r.ref_id, a=a, b=b, ridx=ridx, vidx=vidx, D=D, E=E, cls=cls, held=held))
        log.kv("pairs with word states", f"{len(data):,}")
        log.kv("training / held-out references (by document)", f"{sum(not x['held'] for x in data):,} / {sum(x['held'] for x in data):,}")

        tr = [x for x in data if not x["held"]]
        if args.geometry:
            log.h2("Geometry of each layer's word states (training references)")
            grow = []
            for layer in range(L):
                X = np.concatenate([x["a"][0][layer].astype(np.float64) for x in tr[:400]])
                mu = X.mean(0)
                var = ((X - mu) ** 2).mean(0)
                top = np.sort(var)[::-1]
                norms = np.linalg.norm(X, axis=1)
                grow.append([layer, top[0] / top.sum(), top[:5].sum() / top.sum(), int(np.argmax(var)),
                             np.linalg.norm(mu) / norms.mean()])
            log.table(["layer", "variance share, top dimension", "top 5 dimensions", "top dimension index",
                       "|mean vector| / mean state norm"], grow, floatfmt="{:.3f}")
            log.p("A layer whose variance sits in one or a few dimensions presents a distance probe with "
                  "almost nothing else to read: any rescaling that keeps those dimensions keeps them "
                  "dominant. That is a fact about the layer's geometry, and it is why this is reported "
                  "next to the probe rather than folded into it.")

        log.h2("F5: structural distance probe (held-out references)")
        log.kv("input scaling / epochs", f"{args.standardise} / {args.epochs}")
        sdv = np.concatenate([x["a"][0][L // 2].astype(np.float32) for x in data[:300]]).std(0)
        log.kv(f"layer {L // 2}: dimensions with std < 1e-3 / smallest / largest std",
               f"{int((sdv < 1e-3).sum())} / {sdv.min():.2e} / {sdv.max():.2e}")
        standardise = None if args.standardise == "none" else args.standardise
        rows = []
        ev = [x for x in data if x["held"]]
        lb = linear_baseline([x["D"] for x in ev], [x["E"] for x in ev])
        rows.append(["baseline: surface distance |i - j|", lb[0], lb[1], np.nan, np.nan])
        cl = []
        ctrl = train_probe([x["a"][1].astype(np.float32) for x in tr], [x["D"] for x in tr],
                           [x["a"][1].astype(np.float32) for x in ev], [x["D"] for x in ev], [x["E"] for x in ev],
                           device, epochs=args.epochs, standardise=standardise, losses=cl)
        rows.append(["control (pre-LayerNorm input)", ctrl[0], ctrl[1], cl[0], cl[-1]])
        out = []
        if args.drop_top_dims:
            log.note(f"DIAGNOSTIC: the {args.drop_top_dims} highest-variance dimensions of each layer "
                     "(estimated on training references) are removed before the probe. Not the declared "
                     "probe; read beside rq1_word_state_probes_<model>_f5_norm.md, never instead of it.")
        for layer in (args.layers if args.layers is not None else range(L)):
            keep = slice(None)
            if args.drop_top_dims:
                Xtr = np.concatenate([x["a"][0][layer].astype(np.float64) for x in tr[:400]])
                var = Xtr.var(0)
                keep = np.sort(np.argsort(var)[::-1][args.drop_top_dims:])
            ls = []
            res = train_probe([x["a"][0][layer][:, keep].astype(np.float32) for x in tr], [x["D"] for x in tr],
                              [x["a"][0][layer][:, keep].astype(np.float32) for x in ev], [x["D"] for x in ev],
                              [x["E"] for x in ev], device, epochs=args.epochs, standardise=standardise, losses=ls)
            rows.append([layer, res[0], res[1], ls[0], ls[-1]])
            out.append([args.tag, "distance", layer, res[0], res[1]])
            print(f"    layer {layer}: spearman {res[0]:.3f} uuas {res[1]:.3f} loss {ls[0]:.3f}->{ls[-1]:.3f}", flush=True)
        log.table(["layer", "mean Spearman (5-50 words)", "UUAS", "training loss, first epoch", "last epoch"],
                  rows, floatfmt="{:.3f}")

        if args.only_f5:
            path = rc / f"rq1_word_state_probes_{args.record_tag or args.tag}.csv"
            pd.DataFrame(out, columns=["model", "analysis", "layer", "a", "b"]).to_csv(path, index=False)
            log.output(str(path), "distance: a = Spearman, b = UUAS")
            return
        log.h2("F6: similarity of matched words, reference vs variant")
        rows = []
        for layer in range(L):
            Xs, Ys, cos_all, cos_moved, cos_unmoved = [], [], [], [], []
            for x in data:
                pos_v = {t: p for p, t in enumerate(x["vidx"])}
                for p, t in enumerate(x["ridx"]):
                    u = x["a"][0][layer, p].astype(np.float32)
                    v = x["b"][0][layer, pos_v[t]].astype(np.float32)
                    Xs.append(u)
                    Ys.append(v)
                    c = float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))
                    cos_all.append(c)
                    (cos_moved if x["cls"][t] in ("moved head", "moved other") else cos_unmoved).append(c)
            X, Y = np.stack(Xs), np.stack(Ys)
            rows.append([layer, linear_cka(X, Y), np.mean(cos_all), np.mean(cos_moved), np.mean(cos_unmoved)])
            out.append([args.tag, "similarity", layer, rows[-1][1], rows[-1][2]])
        log.table(["layer", "linear CKA", "mean cosine", "cosine, moved words", "cosine, other words"], rows, floatfmt="{:.4f}")
        path = rc / f"rq1_word_state_probes_{args.tag}.csv"
        pd.DataFrame(out, columns=["model", "analysis", "layer", "a", "b"]).to_csv(path, index=False)
        log.output(str(path), "distance: a = Spearman, b = UUAS; similarity: a = CKA, b = mean cosine")


if __name__ == "__main__":
    main()
