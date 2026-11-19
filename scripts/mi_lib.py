#!/usr/bin/env python3
"""Shared machinery for the step 4 experiments (REMAINING_EXPERIMENTS.md): runs, hooks, patching, attribution
patching, mean-ablation, and the document-level statistics.

THE OBJECTS
  Run    one tokenised sentence and the masked passes it is scored with: input ids (R x T, each row one pass
         with its masks applied), the scored position and target id of each row, a weight per row, and a
         position class per position. The metric of a run is sum_r w_r * log2 p_r. Every metric in step 4 is
         a sum of such runs:
           agreement margin M     = log2 P(correct agreeing words) - log2 P(wrong ones), so the rows of the
                                    correct sentence weigh +1 and those of the wrong one -1
           word-order base metric = -(mean per-word surprisal of the sentence), so every row weighs +1/n_words
                                    (log2 p is minus a surprisal)
  Pair   a corrupted list of runs and a clean list of runs with the same pass structure (row r of one is row r
         of the other), and for each run an alignment from corrupted positions to clean positions (identity
         when only masks differ; by word when the two runs are two orders of the same words). A patch copies
         clean activations into the corrupted run at aligned positions.

COMPONENTS
  ("head", l, h)  attention head h of block l (0-based): its slice of the input to attention.output.dense,
                  the concatenated head outputs before the output projection, so patching one slice changes
                  that head's contribution and nothing else
  ("mlp", l)      the MLP output of block l (output.dense), before the residual addition and LayerNorm
  ("emb",)        the embedding layer's output (used only in the built-in checks)
  Key and value patches (path patching) act on attention.self.key / .value outputs, one head's slice.

SCORING never materialises the full logits: the last hidden state is gathered at the scored positions and only
those rows go through the MLM head (a 250k vocabulary times every position of every row would not fit).
"""
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "reference_code"))

import lm_units as U  # noqa: E402  (whitespace_groups, mlm_head)

LN2 = math.log(2)
MODELS = {  # tag: (path or hub id, batch size used in the thesis runs)
    "muril": ("google/muril-base-cased", 32),
    "xlmrlarge": ("xlm-roberta-large", 16),
}
# outputs go to course_runs/outputs unless MI_OUT says otherwise (smoke tests point it elsewhere); the items built
# by mi_items.py are read from MI_ITEMS, by default course_runs/outputs/items, in both cases
DEVICE = "cuda"   # set by load(); "cpu" only under MI_ALLOW_CPU=1
OUT = Path(os.environ.get("MI_OUT", ROOT / "course_runs" / "outputs"))
ITEMS = Path(os.environ.get("MI_ITEMS", ROOT / "course_runs" / "outputs" / "items"))


# ----------------------------------------------------------------------------------------------- model

def load(tag, eager=True):
    """Model and tokenizer on the GPU, parameters frozen. Refuses the CPU (every run is on a GPU). Eager
    attention by default, so every stage can check the head layout (check_head_layout) on the model it uses."""
    from transformers import AutoModelForMaskedLM, AutoTokenizer
    path = MODELS[tag][0]
    global DEVICE
    if torch.cuda.is_available():
        DEVICE = "cuda"
    elif os.environ.get("MI_ALLOW_CPU") == "1":
        DEVICE = "cpu"      # CPU smoke tests only: the real models, a handful of items
        torch.set_num_threads(int(os.environ.get("SLURM_CPUS_PER_TASK", "4")))
    else:
        raise SystemExit("no GPU visible; refusing to run on the CPU (MI_ALLOW_CPU=1 is for smoke tests only)")
    tok = AutoTokenizer.from_pretrained(path)
    kw = {"attn_implementation": "eager"} if eager else {}
    model = AutoModelForMaskedLM.from_pretrained(path, **kw).to(DEVICE).eval()
    for p in model.parameters():
        p.requires_grad_(False)
    return model, tok


class Arch:
    def __init__(self, model):
        enc = model.base_model.encoder.layer
        cfg = model.config
        self.L, self.H, self.d = len(enc), cfg.num_attention_heads, cfg.hidden_size
        self.dh = self.d // self.H
        self.attn_in = [b.attention.output.dense for b in enc]
        self.mlp_out = [b.output.dense for b in enc]
        self.key = [b.attention.self.key for b in enc]
        self.value = [b.attention.self.value for b in enc]
        self.emb = model.base_model.embeddings
        self.base = model.base_model
        self.head = U.mlm_head(model)

    def components(self):
        out = []
        for l in range(self.L):
            out += [("head", l, h) for h in range(self.H)]
            out.append(("mlp", l))
        return out


def cname(c):
    return f"L{c[1]}H{c[2]}" if c[0] == "head" else (f"L{c[1]}MLP" if c[0] == "mlp" else "EMB")


def cparse(s):
    if s == "EMB":
        return ("emb",)
    l, rest = s[1:].split("H", 1) if "MLP" not in s else (s[1:].split("MLP")[0], None)
    return ("mlp", int(l)) if rest is None else ("head", int(l), int(rest))


# ----------------------------------------------------------------------------------------------- runs

@dataclass
class Run:
    ids: torch.Tensor      # (R, T) long, masks applied
    pos: torch.Tensor      # (R,) scored position
    tgt: torch.Tensor      # (R,) target id
    w: torch.Tensor        # (R,) float weight
    pclass: torch.Tensor   # (T,) long position class
    word_of: list          # (T,) whitespace word index of each position, -1 for special tokens
    off: list              # (T,) subtoken offset within its whitespace word, -1 for special tokens
    masked: torch.Tensor = None   # (R, T) bool: masked in that row


@dataclass
class Pair:
    corrupt: list
    clean: list
    align: list            # per run: (T,) long, clean position of each corrupted position
    meta: dict = field(default_factory=dict)


def tokenise(tok, text):
    """Ids with specials, and for every position its whitespace word and subtoken offset in that word."""
    g = U.whitespace_groups(tok, text)
    if g is None:
        return None
    ids, groups, gw, nw = g
    T = len(ids)
    word_of, off, seen = [-1] * T, [-1] * T, {}
    for k, pos in enumerate(groups):
        for p in pos:
            word_of[p] = gw[k]
            off[p] = seen.get(gw[k], 0)
            seen[gw[k]] = off[p] + 1
    return ids, groups, gw, nw, word_of, off


def _finish(tok, ids, passes, word_class, word_of, off, extra_mask, weights, device=None):
    """passes: list of (mask positions, scored position). extra_mask: positions masked in every row."""
    device = device or DEVICE
    R, T = len(passes), len(ids)
    x = torch.tensor([ids] * R, dtype=torch.long)
    m = torch.zeros(R, T, dtype=torch.bool)
    for r, (mp, _) in enumerate(passes):
        m[r, list(mp) + list(extra_mask)] = True
    x[m] = tok.mask_token_id
    pcl = torch.tensor([word_class(word_of[t]) if word_of[t] >= 0 else 0 for t in range(T)], dtype=torch.long)
    return Run(ids=x.to(device), pos=torch.tensor([p for _, p in passes], device=device),
               tgt=torch.tensor([ids[p] for _, p in passes], device=device),
               w=torch.tensor(weights, dtype=torch.float32, device=device), pclass=pcl.to(device),
               word_of=word_of, off=off, masked=m.to(device))


def span_run(tok, text, span_words, sign, mask_words=(), word_class=lambda w: 1):
    """Left-to-right chain over the subtokens of `span_words` (whitespace word indices, in sentence order):
    row i masks span subtoken i and every later span subtoken, and scores subtoken i, so the rows' log
    probabilities sum to log P(span | the rest of the sentence). `mask_words` are masked in every row (a
    corruption). Every row weighs `sign`."""
    t = tokenise(tok, text)
    if t is None:
        return None
    ids, groups, gw, nw, word_of, off = t
    span = [p for p in range(len(ids)) if word_of[p] in set(span_words)]
    if not span:
        return None
    passes = [(span[i:], span[i]) for i in range(len(span))]
    extra = [p for p in range(len(ids)) if word_of[p] in set(mask_words)]
    if set(extra) & set(span):
        raise ValueError("a masked word overlaps the scored span")
    return _finish(tok, ids, passes, word_class, word_of, off, extra, [float(sign)] * len(passes))


def l2r_run(tok, text, word_class=lambda w: 1, mask_words=()):
    """within_word_l2r over every word (the scoring of steps 1 to 3): for each tokenizer word and each of its
    subtokens j, mask subtokens j.. of that word and score j. Rows weigh +1/n_words, so the metric
    sum w * log2 p is minus the mean per-word surprisal over whitespace words (as rq1_patching.py)."""
    t = tokenise(tok, text)
    if t is None:
        return None
    ids, groups, gw, nw, word_of, off = t
    hidden = set(mask_words)
    passes = [(pos[j:], pos[j]) for k, pos in enumerate(groups) if gw[k] not in hidden for j in range(len(pos))]
    extra = [p for p in range(len(ids)) if word_of[p] in hidden]
    n_scored = nw - len(hidden & set(range(nw)))
    return _finish(tok, ids, passes, word_class, word_of, off, extra, [1.0 / n_scored] * len(passes))


def mapped_run(tok, base, other_text, word_map, word_class=lambda w: 1):
    """The run of `other_text` whose rows mask and score the same words as `base`'s rows, found through
    word_map (base whitespace word -> other whitespace word) and subtoken offset. Used for the clean side of a
    pair whose two runs are two orders of the same words. Returns (run, alignment base position -> other)."""
    t = tokenise(tok, other_text)
    ids, groups, gw, nw, word_of, off = t
    where = {(word_of[p], off[p]): p for p in range(len(ids)) if word_of[p] >= 0}
    T = base.ids.shape[1]
    if len(ids) != T:
        raise ValueError("the two orders tokenise to different lengths")
    align = []
    for p in range(T):
        if base.word_of[p] < 0:
            align.append(0 if p == 0 else len(ids) - 1)
        else:
            align.append(where[(word_map[base.word_of[p]], base.off[p])])
    a = torch.tensor(align, device=base.ids.device)
    if sorted(align) != list(range(T)):
        raise ValueError("the alignment is not a permutation")
    x = torch.tensor([ids] * base.ids.shape[0], dtype=torch.long, device=base.ids.device)
    m = torch.zeros_like(base.masked)
    m[:, a] = base.masked
    x[m] = tok.mask_token_id
    pos = a[base.pos]
    tgt = torch.tensor(ids, device=base.ids.device)[pos]
    if not torch.equal(tgt, base.tgt):
        raise ValueError("aligned rows score different subtokens")
    pcl = torch.tensor([word_class(word_of[t_]) if word_of[t_] >= 0 else 0 for t_ in range(T)], device=base.ids.device)
    run = Run(ids=x, pos=pos, tgt=tgt, w=base.w.clone(), pclass=pcl, word_of=word_of, off=off, masked=m)
    return run, a


# ----------------------------------------------------------------------------------------------- hooks

class Session:
    """Batched forwards with optional patches, gradient capture and caching, all through hooks that are
    installed once and read a per-forward plan."""

    def __init__(self, model):
        self.model = model
        self.A = Arch(model)
        self.plan = None
        hs = [self.A.emb.register_forward_hook(self._emb_hook)]
        for l in range(self.A.L):
            hs.append(self.A.attn_in[l].register_forward_pre_hook(self._attn_hook(l)))
            hs.append(self.A.mlp_out[l].register_forward_hook(self._mlp_hook(l)))
            hs.append(self.A.key[l].register_forward_hook(self._kv_hook("k", l)))
            hs.append(self.A.value[l].register_forward_hook(self._kv_hook("v", l)))
        self.handles = hs

    def close(self):
        for h in self.handles:
            h.remove()

    # each hook: apply patches for its site, then capture if asked
    def _apply(self, key, x, width_of):
        p = self.plan
        if p is None:
            return x
        specs = p["patches"].get(key)
        if specs:
            x = x.clone()
            for rows, pos, col, val in specs:
                c0, c1 = width_of(col)
                x[rows[:, None], pos, c0:c1] = val.to(x.dtype)
        if p["grad"] and key[0] in ("attn", "mlp"):
            x.retain_grad()
        if p["capture"] and key[0] in p["capture"]:
            p["store"][key] = x
        return x

    def _emb_hook(self, mod, inp, out):
        x = self._apply(("emb",), out, lambda c: (0, self.A.d))
        if self.plan is not None and self.plan["grad"]:
            x = x.detach().requires_grad_(True) if not x.requires_grad else x
            if self.plan["capture"] and "emb" in self.plan["capture"]:
                self.plan["store"][("emb",)] = x
        return x

    def _attn_hook(self, l):
        def f(mod, inp):
            return (self._apply(("attn", l), inp[0], self._head_cols),) + tuple(inp[1:])
        return f

    def _mlp_hook(self, l):
        def f(mod, inp, out):
            return self._apply(("mlp", l), out, lambda c: (0, self.A.d))
        return f

    def _kv_hook(self, kind, l):
        def f(mod, inp, out):
            return self._apply((kind, l), out, self._head_cols)
        return f

    def _head_cols(self, h):
        if h is None:
            return 0, self.A.d
        return h * self.A.dh, (h + 1) * self.A.dh

    def forward(self, ids, pos, tgt, patches=None, capture=(), grad=False):
        """log2 p of tgt at pos for every row. patches: {site key: [(rows, pos, head or None, value)]} with
        rows (r,), pos (r, p) and value (r, p, width). capture: the site kinds to keep ("attn", "mlp", "emb",
        "k", "v"). Returns (log2 p (R,), store of captured tensors)."""
        self.plan = {"patches": patches or {}, "capture": set(capture), "grad": grad, "store": {}}
        try:
            ctx = torch.enable_grad() if grad else torch.no_grad()
            with ctx:
                h = self.A.base(input_ids=ids, attention_mask=torch.ones_like(ids)).last_hidden_state
                sel = h[torch.arange(len(ids), device=ids.device), pos]
                lp = torch.log_softmax(self.A.head(sel).float(), -1).gather(1, tgt[:, None])[:, 0] / LN2
            return lp, self.plan["store"]
        finally:
            self.plan = None


def metric(sess, runs, chunk=64):
    """sum over runs and rows of w * log2 p, with no intervention."""
    tot = 0.0
    for run in runs:
        for s in range(0, len(run.ids), chunk):
            lp, _ = sess.forward(run.ids[s:s + chunk], run.pos[s:s + chunk], run.tgt[s:s + chunk])
            tot += float((run.w[s:s + chunk] * lp).sum())
    return tot


def cache(sess, run, rows=None, kinds=("attn", "mlp", "emb")):
    """Activations of the given site kinds (attention input, MLP output, embeddings; "k" and "v" on request)
    for the given rows."""
    sl = slice(None) if rows is None else rows
    _, st = sess.forward(run.ids[sl], run.pos[sl], run.tgt[sl], capture=kinds)
    return {k: v.detach() for k, v in st.items()}


def site_of(c):
    return ("emb",) if c[0] == "emb" else (("attn", c[1]) if c[0] == "head" else ("mlp", c[1]))


def col_of(c):
    return c[2] if c[0] == "head" else None


# ----------------------------------------------------------------------------------------------- patching

def patch_value(sess, c, act, rows_src, pos_src):
    """The clean activation of component c at rows_src (r,) and positions pos_src (r, p)."""
    a = act[site_of(c)]
    c0, c1 = sess._head_cols(col_of(c))
    return a[rows_src[:, None], pos_src, c0:c1]


def exact(sess, pair, comps, positions, max_rows=256, extra=None):
    """Metric of the corrupted runs with each component in `comps` patched from the clean runs, one component
    at a time, at `positions` (a function run index -> (corrupted position tensor)). Returns an array
    (len(comps),). `extra(c)` may return further patches to apply together with c (a set of components is
    passed as a tuple of components and patched jointly)."""
    out = np.zeros(len(comps))
    for ri, (cr, cl) in enumerate(zip(pair.corrupt, pair.clean)):
        R = len(cr.ids)
        act = cache(sess, cl)
        P = positions(ri)
        if P.numel() == 0:
            # nothing to patch in this run: every component leaves it as it is
            out += metric(sess, [cr])
            continue
        per = max(1, max_rows // R)
        for b0 in range(0, len(comps), per):
            block = comps[b0:b0 + per]
            n = len(block)
            ids = cr.ids.repeat(n, 1)
            patches = {}
            for bi, c in enumerate(block):
                rows = torch.arange(bi * R, (bi + 1) * R, device=ids.device)
                for cc in (c if isinstance(c, tuple) and isinstance(c[0], tuple) else (c,)):
                    src = torch.arange(R, device=ids.device)
                    val = patch_value(sess, cc, act, src, pair.align[ri][P][None, :].expand(R, -1))
                    patches.setdefault(site_of(cc), []).append((rows, P[None, :].expand(R, -1), col_of(cc), val))
            lp, _ = sess.forward(ids, cr.pos.repeat(n), cr.tgt.repeat(n), patches=patches)
            out[b0:b0 + n] += (cr.w.repeat(n) * lp).view(n, R).sum(1).cpu().numpy()
    return out


def atp(sess, pair, n_class, chunk=16):
    """Attribution patching (Syed et al. 2023): for every head and MLP and every position class,
    sum over rows and positions of (clean - corrupted activation, aligned) . d metric / d activation, the
    gradient taken in the corrupted run. Returns (array (n_components, n_class), components)."""
    comps = sess.A.components()
    H, L, dh = sess.A.H, sess.A.L, sess.A.dh
    res = torch.zeros(L, H + 1, n_class, dtype=torch.float64, device=DEVICE)
    for ri, (cr, cl) in enumerate(zip(pair.corrupt, pair.clean)):
        al = pair.align[ri]
        onehot = torch.nn.functional.one_hot(cr.pclass, n_class).double()   # (T, n_class)
        for s in range(0, len(cr.ids), chunk):
            rows = torch.arange(s, min(s + chunk, len(cr.ids)), device=DEVICE)
            clean = cache(sess, cl, rows)
            lp, st = sess.forward(cr.ids[rows], cr.pos[rows], cr.tgt[rows], capture=("attn", "mlp"), grad=True)
            (cr.w[rows] * lp).sum().backward()
            for l in range(L):
                a = st[("attn", l)]
                diff = (clean[("attn", l)][:, al] - a.detach()).double()
                prod = (diff * a.grad.double()).view(len(rows), -1, H, dh).sum(-1).sum(0)   # (T, H)
                res[l, :H] += prod.T @ onehot
                m = st[("mlp", l)]
                dm = (clean[("mlp", l)][:, al] - m.detach()).double()
                res[l, H] += (dm * m.grad.double()).sum(-1).sum(0) @ onehot
            del st, lp
    arr = res.cpu().numpy()
    out = np.zeros((len(comps), n_class))
    for i, c in enumerate(comps):
        out[i] = arr[c[1], c[2] if c[0] == "head" else H]
    return out, comps


# ----------------------------------------------------------------------------------------------- mean ablation

POP_SPECIAL, POP_MASK, POP_OTHER = 0, 1, 2


def populations(run):
    """(R, T) population of every position in every row: special token, masked, or other."""
    pop = torch.full(run.masked.shape, POP_OTHER, dtype=torch.long, device=run.ids.device)
    pop[run.masked] = POP_MASK
    pop[:, 0] = POP_SPECIAL
    pop[:, -1] = POP_SPECIAL
    return pop


def estimate_means(sess, tok, sentences, seed=708):
    """Mean output of every head slice and MLP, separately over special tokens, masked positions and other
    positions, from held-out sentences each scored with one randomly chosen word masked (its whole
    subtoken span, the first pass of within_word_l2r). Means taken where they will be used, so an ablation
    never feeds a [MASK] position the average of unmasked ones."""
    rng = np.random.default_rng(seed)
    A = sess.A
    sums = {k: torch.zeros(3, A.d, dtype=torch.float64, device=DEVICE) for l in range(A.L) for k in (("attn", l), ("mlp", l))}
    cnt = torch.zeros(3, dtype=torch.float64, device=DEVICE)
    for text in sentences:
        t = tokenise(tok, text)
        if t is None or len(t[0]) > 256:
            continue
        ids, groups, gw, nw, word_of, off = t
        g = groups[int(rng.integers(len(groups)))]
        run = _finish(tok, ids, [(g, g[0])], lambda w: 1, word_of, off, [], [1.0])
        _, st = sess.forward(run.ids, run.pos, run.tgt, capture=("attn", "mlp"))
        pop = populations(run)[0]
        oh = torch.nn.functional.one_hot(pop, 3).double()            # (T, 3)
        cnt += oh.sum(0)
        for k in sums:
            sums[k] += oh.T @ st[k][0].double()
    return {k: (v / cnt[:, None]).float() for k, v in sums.items()}, cnt.cpu().numpy()


def ablation_patches(sess, run, comps, means, rows_offset=0, n_blocks=1, block_comps=None):
    """Patches replacing each component's output by its population mean at every position of every row.
    With n_blocks > 1, block b ablates the components block_comps[b] (a tuple of components)."""
    pop = populations(run)                                   # (R, T)
    R, T = pop.shape
    P = torch.arange(T, device=run.ids.device)[None, :].expand(R, -1)
    patches = {}
    blocks = block_comps if block_comps is not None else [comps]
    for b, bc in enumerate(blocks):
        rows = torch.arange(b * R, (b + 1) * R, device=run.ids.device)
        for c in bc:
            k = site_of(c)
            c0, c1 = sess._head_cols(col_of(c))
            val = means[k][:, c0:c1][pop]                     # (R, T, width)
            patches.setdefault(k, []).append((rows, P, col_of(c), val))
    return patches


def ablated_metric(sess, runs, comp_sets, means, max_rows=256):
    """Metric of `runs` with each set in comp_sets (list of tuples of components) mean-ablated. (len(sets),)"""
    out = np.zeros(len(comp_sets))
    for run in runs:
        R = len(run.ids)
        per = max(1, max_rows // R)
        for b0 in range(0, len(comp_sets), per):
            block = comp_sets[b0:b0 + per]
            n = len(block)
            patches = ablation_patches(sess, run, None, means, n_blocks=n, block_comps=block)
            lp, _ = sess.forward(run.ids.repeat(n, 1), run.pos.repeat(n), run.tgt.repeat(n), patches=patches)
            out[b0:b0 + n] += (run.w.repeat(n) * lp).view(n, R).sum(1).cpu().numpy()
    return out


def readability(sess, tok, sentences, comp_set=None, means=None):
    """Mean surprisal per subtoken (nats) of held-out sentences, within_word_l2r, optionally with a component
    set mean-ablated (the 2-nat rule of the thesis runs)."""
    tot, n = 0.0, 0
    for text in sentences:
        run = l2r_run(tok, text)
        if run is None or run.ids.shape[1] > 256:
            continue
        for s in range(0, len(run.ids), 64):
            ids, pos, tgt = run.ids[s:s + 64], run.pos[s:s + 64], run.tgt[s:s + 64]
            sub = Run(ids=ids, pos=pos, tgt=tgt, w=run.w[s:s + 64], pclass=run.pclass, word_of=run.word_of,
                      off=run.off, masked=run.masked[s:s + 64])
            patches = ablation_patches(sess, sub, None, means, block_comps=[comp_set]) if comp_set else None
            lp, _ = sess.forward(ids, pos, tgt, patches=patches)
            tot += float(-lp.sum()) * LN2
            n += len(ids)
    return tot / n


def heldout_sentences(path, n_mean=300, n_read=100):
    """The thesis's held-out IndicCorp pool: 8 to 40 words; the 500 readability sentences drawn with seed 707
    are kept apart (the first --n-read of them are read here), and the means come from the rest (seed 708)."""
    lines = [l.strip() for l in open(path, encoding="utf-8") if 8 <= len(l.split()) <= 40]
    held_idx = set(np.random.default_rng(707).choice(len(lines), size=min(500, len(lines)), replace=False).tolist())
    held = [lines[i] for i in sorted(held_idx)]
    pool = [l for i, l in enumerate(lines) if i not in held_idx]
    est = [pool[i] for i in np.random.default_rng(708).permutation(len(pool))[:n_mean]]
    return est, held[:n_read]


# ----------------------------------------------------------------------------------------------- statistics

def ratio_of_sums(num, den, keep):
    return float(np.sum(np.asarray(num)[keep]) / np.sum(np.asarray(den)[keep]))


def doc_signflip(values, docs, B=10000, seed=707, one_sided=False):
    """Sign-flip permutation p of the sum of per-item values, flipping whole documents."""
    v = np.asarray(values, float)
    d = np.asarray(docs)
    u = {k: i for i, k in enumerate(sorted(set(d.tolist())))}
    sums = np.zeros(len(u))
    np.add.at(sums, [u[x] for x in d], v)
    rng = np.random.default_rng(seed)
    obs = sums.sum()
    null = (rng.choice([-1.0, 1.0], size=(B, len(sums))) * sums).sum(1)
    if one_sided:
        return (1 + int((null >= obs).sum())) / (1 + B)
    return (1 + int((np.abs(null) >= abs(obs)).sum())) / (1 + B)


def doc_bootstrap_ratio(num, den, docs, B=2000, seed=707):
    """Percentile interval (2.5, 97.5) of a ratio of sums, resampling documents. Descriptive, not a test."""
    num, den, d = np.asarray(num, float), np.asarray(den, float), np.asarray(docs)
    u = sorted(set(d.tolist()))
    idx = {k: i for i, k in enumerate(u)}
    ns, ds = np.zeros(len(u)), np.zeros(len(u))
    np.add.at(ns, [idx[x] for x in d], num)
    np.add.at(ds, [idx[x] for x in d], den)
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(u), size=(B, len(u)))
    r = ns[pick].sum(1) / ds[pick].sum(1)
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def matched_random_sets(comps, circuit, n_sets, seed, mlp_window=2):
    """Random component sets matched to `circuit` in type and, as far as possible, in layer. Returns (sets, stats).

    heads   each replaced by a random other head of the same block; if every head of its block is taken (by the
            circuit or by this set), of the nearest block that has one free (counted as layer-unmatched)
    MLPs    there is one per block, so each is replaced by an MLP drawn at random from the free blocks within
            --mlp-window blocks of it (so the control varies from set to set instead of always taking the nearest
            block); if none is free there, from every free MLP (layer-unmatched); and if no MLP
            outside the circuit is left at all (a circuit with more than half the blocks' MLPs), by a random free
            head of the same block (type-unmatched). Rule declared on the second review, 23 Oct, before any run.
    No set repeats a component or contains one of the circuit's, and no two sets have the same members (a draw
    that repeats an earlier set's members is discarded; at most 50 * n_sets draws, so a circuit that leaves few
    choices yields fewer sets, and stats["distinct"] says how many). stats also counts, over the sets kept, the
    replacements that are layer-unmatched and type-unmatched, for the record."""
    rng = np.random.default_rng(seed)
    heads_by_layer = {}
    for c in comps:
        if c[0] == "head":
            heads_by_layer.setdefault(c[1], []).append(c)
    mlps = {c[1]: c for c in comps if c[0] == "mlp"}
    cset = set(circuit)
    stats = {"replacements": 0, "layer-unmatched": 0, "type-unmatched": 0}

    def free(x, s):
        return x not in cset and x not in s

    def head_near(layer, s):
        for dist in range(0, len(heads_by_layer)):
            pool = [x for l in sorted({layer - dist, layer + dist}) for x in heads_by_layer.get(l, []) if free(x, s)]
            if pool:
                return pool, dist
        return [], None

    out, seen, tries = [], set(), 0
    while len(out) < n_sets and tries < 50 * n_sets:
        tries += 1
        s = []
        st = {"replacements": 0, "layer-unmatched": 0, "type-unmatched": 0}
        for c in circuit:
            st["replacements"] += 1
            if c[0] == "head":
                pool, dist = head_near(c[1], s)
                if dist:
                    st["layer-unmatched"] += 1
            else:
                pool = [mlps[l] for l in range(c[1] - mlp_window, c[1] + mlp_window + 1)
                        if l != c[1] and l in mlps and free(mlps[l], s)]
                if not pool:
                    pool = [m for m in mlps.values() if free(m, s)]
                    if pool:
                        st["layer-unmatched"] += 1
                if not pool:
                    pool, dist = head_near(c[1], s)
                    st["type-unmatched"] += 1
                    if dist:
                        st["layer-unmatched"] += 1
            if not pool:
                raise ValueError(f"no replacement left for {cname(c)}: the circuit uses nearly every component")
            s.append(pool[int(rng.integers(len(pool)))])
        key = frozenset(s)
        if key in seen:
            continue
        seen.add(key)
        out.append(tuple(s))
        for k_ in st:
            stats[k_] += st[k_]
    stats["distinct"] = len(out)
    return out, stats


def check_head_layout(sess, tok, text, rows=4):
    """That column block h of the attention input, of the keys and of the values is head h. Under eager attention,
    at every block and head: (a) the attention probabilities of head h times value slice h equal slice h of the
    attention output projection's input; (b) softmax(query slice h . key slice h / sqrt(dh)) equals those
    probabilities (no padding, so no mask term). Returns the largest absolute difference of either."""
    run = l2r_run(tok, text)
    ids = run.ids[:rows]
    qs = {}
    enc = sess.model.base_model.encoder.layer
    hq = [enc[l].attention.self.query.register_forward_hook(lambda m, i, o, l=l: qs.__setitem__(l, o.detach()))
          for l in range(sess.A.L)]
    sess.plan = {"patches": {}, "capture": {"attn", "k", "v"}, "grad": False, "store": {}}
    try:
        with torch.no_grad():
            out = sess.A.base(input_ids=ids, attention_mask=torch.ones_like(ids), output_attentions=True)
        st = sess.plan["store"]
    finally:
        sess.plan = None
        for h_ in hq:
            h_.remove()
    if out.attentions is None or out.attentions[0] is None:
        raise SystemExit("the model returned no attention probabilities: load it with eager attention")
    worst = 0.0
    for l in range(sess.A.L):
        att, k, v, ctx = (out.attentions[l].float(), st[("k", l)].float(), st[("v", l)].float(),
                          st[("attn", l)].float())
        q = qs[l].float()
        for h in range(sess.A.H):
            c0, c1 = sess._head_cols(h)
            worst = max(worst, float((att[:, h] @ v[..., c0:c1] - ctx[..., c0:c1]).abs().max()))
            p = torch.softmax(q[..., c0:c1] @ k[..., c0:c1].transpose(-1, -2) / math.sqrt(sess.A.dh), -1)
            worst = max(worst, float((p - att[:, h]).abs().max()))
    return worst
