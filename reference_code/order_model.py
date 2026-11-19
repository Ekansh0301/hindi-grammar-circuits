#!/usr/bin/env python3
"""Constituent-level predictors for Set 1 pairs (PREREGISTRATION_DRAFT.md 6.2 and 6.3).

  E1   constituent-order surprisal: an interpolated Kneser-Ney trigram over the sequence of a
       clause's units, each unit written as relation:case-marker (`k7t:0 k1:ने k2:को END`)
  ACC  d_pron_inv (a full noun phrase before a pronominal unit) and d_bare_obj (an unmarked,
       noun-headed k2 that is not the last unit before the verb complex; d_bare_obj_nonspec
       additionally excludes nouns with a demonstrative, numeral or genitive dependent)
  strata  which kinds of units a variant moves: arguments only, adjuncts only, both

Units follow the Set 1 definition (rules R0 to R2, SET1_CONSTRUCTION_PLAN.md 4b). `clause_units`
re-derives them without the rules that only decide whether a clause is permuted (holds, number
of free units), so clauses with a single unit still train the order model; the build checks it
agrees with `set1_generator.analyse_clause` on every clause that function accepts.
"""
import hashlib
import math
from collections import Counter, defaultdict

import set1_generator as G

BOS, END = "<s>", "</s>"
ARG_BASE = ["k1", "k1s", "k2", "k2p", "k3", "k4", "k4a", "k5", "pk1", "mk1", "jk1"]
ARGUMENTS = set(ARG_BASE) | {"ras-" + r for r in ARG_BASE}
FULL_NP = {"NN", "NNP"}


# ----------------------------------------------------------------------------- units
def clause_units(tokens, head):
    """Unit head indices of a clause in surface order, or None if R1/R2 or adjacency fails."""
    by = {t["idx"]: t for t in tokens}
    kids = G.children(tokens)
    pre = [d for d in kids.get(head, []) if d < head]
    vc = [d for d in pre if G.is_verb_complex_rel(by[d]["deprel"])]
    units = [d for d in pre if d not in vc and by[d]["deprel"] != "rsym"]
    if not units:
        return None
    spans = {d: G.subtree(kids, d) for d in units}
    if not all(G.contiguous(s) for s in spans.values()):
        return None
    vc_span = sorted({i for d in vc for i in G.subtree(kids, d)} | {head})
    if not G.contiguous(vc_span):
        return None
    units.sort(key=lambda d: spans[d][0])
    for a, b in zip(units, units[1:]):
        if spans[a][-1] + 1 != spans[b][0]:
            return None
    if spans[units[-1]][-1] + 1 != vc_span[0]:
        return None
    return units


def has_surface(tokens, kids, d):
    by = {t["idx"]: t for t in tokens}
    return any(not G.is_null(by[i]) for i in G.subtree(kids, d))


def representative(by, kids, d):
    """The token that carries a unit's case and category. In HDTB a coordinated constituent is
    headed by the conjunction, and its postposition attaches to the LAST conjunct
    (मेरे भाई और मेरी मां ने: ने is a child of मां), so for coordination follow the last
    conjunct, recursively for nested coordination."""
    while True:
        conj = [c for c in kids.get(d, []) if by[c]["deprel"] == "ccof"]
        if not conj or any(by[c]["deprel"] == "lwg__psp" for c in kids.get(d, [])):
            return d
        d = max(conj)


def marker(by, kids, d):
    """The unit's case marker: postposition(s) on its head, or on the last conjunct of a
    coordination; else the fused case of a pronoun; else 0."""
    for h in (d, representative(by, kids, d)):
        psp = [by[c]["form"] for c in kids.get(h, []) if by[c]["deprel"] == "lwg__psp"]
        if psp:
            return "_".join(psp)
    rep = by[representative(by, kids, d)]
    if G.fused_case_pronoun(rep):
        return "ने" if rep["form"].endswith("ने") else "को"
    return "0"


def pronominal(tok):
    return tok["xpos"] == "PRP" or G.fused_case_pronoun(tok)


SPECIFIC_DEPENDENT_XPOS = {"DEM", "QC", "QO"}


def specific(by, kids, h):
    """A noun with a demonstrative, numeral or genitive dependent: specific, so outside
    pseudo-incorporation."""
    return any(by[c]["xpos"] in SPECIFIC_DEPENDENT_XPOS or by[c]["deprel"] == "r6" for c in kids.get(h, []))


class Clause:
    """One clause of a reference: its units (generator order) and per-unit descriptors."""

    def __init__(self, tokens, head):
        self.units = clause_units(tokens, head)
        if self.units is None:
            return
        by = {t["idx"]: t for t in tokens}
        kids = G.children(tokens)
        self.surface = [has_surface(tokens, kids, d) for d in self.units]
        self.rel = [by[d]["deprel"] for d in self.units]
        self.mark = [marker(by, kids, d) for d in self.units]
        rep = [representative(by, kids, d) for d in self.units]
        self.pron = [pronominal(by[h]) for h in rep]
        self.full_np = [by[h]["xpos"] in FULL_NP for h in rep]
        self.specific = [specific(by, kids, h) for h in rep]
        self.pos = [by[h]["xpos"] for h in rep]
        self.size = [sum(1 for i in G.subtree(kids, d) if not G.is_null(by[i])) for d in self.units]

    def ok(self):
        return self.units is not None

    def symbols(self, order=None, with_marker=True):
        order = range(len(self.units)) if order is None else order
        return [f"{self.rel[u]}:{self.mark[u]}" if with_marker else self.rel[u]
                for u in order if self.surface[u]]

    def symbols_rich(self, order=None):
        """Each surface unit as a run of word-free attribute tokens: relation, case marker, the head's
        part of speech, its length in words (bucketed 1, 2, 3-4, 5-8, 9+), and whether it is specific
        (a demonstrative, numeral or genitive dependent). The richer-information axis of the structure
        model (RQ1_WORK_PLAN.md K1b): still no word identity, but what a constituent is, not only what
        role and case it has. A model over these tokens predicts each attribute given everything
        before it, so its probabilities stay exactly normalised for combinations never seen together."""
        order = range(len(self.units)) if order is None else order
        out = []
        for u in order:
            if not self.surface[u]:
                continue
            n = self.size[u]
            b = "1" if n == 1 else "2" if n == 2 else "3-4" if n <= 4 else "5-8" if n <= 8 else "9+"
            out += [f"R:{self.rel[u]}", f"C:{self.mark[u]}", f"P:{self.pos[u]}", f"L:{b}",
                    f"S:{int(self.specific[u])}"]
        return out

    def pron_inv(self, order=None):
        seq = [u for u in (range(len(self.units)) if order is None else order) if self.surface[u]]
        n = len(seq)
        if n < 2:
            return 0.0
        bad = sum(1 for i in range(n) for j in range(i + 1, n) if self.full_np[seq[i]] and self.pron[seq[j]])
        return bad / (n * (n - 1) / 2)

    def _bare(self, u, nonspecific):
        return (self.rel[u] == "k2" and self.mark[u] == "0" and self.full_np[u]
                and not (nonspecific and self.specific[u]))

    def bare_obj(self, order=None, nonspecific=False):
        """1 if an unmarked noun-headed k2 is not the last surface unit before the verb complex."""
        seq = [u for u in (range(len(self.units)) if order is None else order) if self.surface[u]]
        return int(any(self._bare(u, nonspecific) for u in seq[:-1]))

    def has_bare_obj(self, nonspecific=False):
        return any(self._bare(u, nonspecific) and self.surface[u] for u in range(len(self.units)))


def moved_stratum(clause, order):
    moved = [clause.rel[u] for slot, u in enumerate(order) if u != slot]
    kinds = {r in ARGUMENTS for r in moved}
    if kinds == {True}:
        return "arguments_only"
    if kinds == {False}:
        return "adjuncts_only"
    return "both"


def fold_of(doc, k=10):
    return int(hashlib.sha256(doc.encode()).hexdigest()[:8], 16) % k


def doc_of(ref_id):
    return ref_id.split("__")[0]


# ----------------------------------------------------------------------------- model
class KNTrigram:
    """Interpolated Kneser-Ney trigram (Chen and Goodman 1999) with one absolute discount D at
    every order. Lower orders use continuation counts; the unigram level interpolates with the
    uniform distribution over the prediction vocabulary, so every distribution sums to 1."""

    def __init__(self, vocab, discount=0.75):
        self.V = sorted(set(vocab) | {END})
        self.D = discount

    def fit(self, sequences):
        c3 = Counter()
        for seq in sequences:
            s = [BOS, BOS] + list(seq) + [END]
            for i in range(2, len(s)):
                c3[(s[i - 2], s[i - 1], s[i])] += 1
        self.c3 = c3
        self.c_uv, self.n_uv = Counter(), Counter()
        cont2_pairs = defaultdict(set)
        for (u, v, w), c in c3.items():
            self.c_uv[(u, v)] += c
            self.n_uv[(u, v)] += 1
            cont2_pairs[(v, w)].add(u)
        self.cont2 = {vw: len(us) for vw, us in cont2_pairs.items()}
        self.cont2_v, self.types2_v = Counter(), Counter()
        cont1_sets = defaultdict(set)
        for (v, w), n in self.cont2.items():
            self.cont2_v[v] += n
            self.types2_v[v] += 1
            cont1_sets[w].add(v)
        self.cont1 = {w: len(vs) for w, vs in cont1_sets.items()}
        self.total1 = sum(self.cont1.values())
        self.types1 = len(self.cont1)
        unknown = set(self.cont1) - set(self.V)
        if unknown:
            raise ValueError(f"symbols outside the vocabulary: {sorted(unknown)[:5]}")
        return self

    def p1(self, w):
        return (max(self.cont1.get(w, 0) - self.D, 0) / self.total1
                + self.D * self.types1 / self.total1 / len(self.V))

    def p2(self, w, v):
        n = self.cont2_v.get(v, 0)
        if n == 0:
            return self.p1(w)
        return (max(self.cont2.get((v, w), 0) - self.D, 0) / n
                + self.D * self.types2_v[v] / n * self.p1(w))

    def p3(self, w, u, v):
        n = self.c_uv.get((u, v), 0)
        if n == 0:
            return self.p2(w, v)
        return (max(self.c3.get((u, v, w), 0) - self.D, 0) / n
                + self.D * self.n_uv[(u, v)] / n * self.p2(w, v))

    def surprisal(self, seq):
        """Total surprisal in bits of the sequence followed by END."""
        s = [BOS, BOS] + list(seq) + [END]
        return -sum(math.log2(self.p3(s[i], s[i - 2], s[i - 1])) for i in range(2, len(s)))


class KNGram:
    """Interpolated Kneser-Ney of any order n >= 1, same discount at every level.

    The trigram above is the proposal's E1 and is left exactly as it is; this one exists for the
    capacity curve (RQ2_RQ3_WORK_PLAN.md / RQ1_WORK_PLAN.md K1), which asks how the absorbed share moves
    as the structure-only model is made stronger or weaker. At n = 3 it must reproduce `KNTrigram`
    surprisal for surprisal, which `tests/test_order_model.py` checks on the real unit sequences: a
    capacity curve whose middle point disagreed with the published E1 would compare nothing.

    Counts: the top level uses raw counts; every lower level uses continuation counts (the number of
    distinct left contexts a sequence appears in), which is what makes it Kneser-Ney rather than
    interpolated absolute discounting. The unigram level interpolates with the uniform distribution over
    the prediction vocabulary, so every distribution sums to 1.
    """

    def __init__(self, vocab, order=3, discount=0.75):
        if order < 1:
            raise ValueError("order must be at least 1")
        self.V = sorted(set(vocab) | {END})
        self.n = order
        self.D = discount

    def fit(self, sequences):
        # level k holds k-grams: counts at the top level, continuation counts below it
        self.cnt = [Counter() for _ in range(self.n + 1)]      # cnt[k][k-gram] -> count
        self.tot = [Counter() for _ in range(self.n + 1)]      # tot[k][history] -> sum over w
        self.typ = [Counter() for _ in range(self.n + 1)]      # typ[k][history] -> distinct w
        top = Counter()
        for seq in sequences:
            s = [BOS] * (self.n - 1) + list(seq) + [END]
            for i in range(self.n - 1, len(s)):
                top[tuple(s[i - self.n + 1:i + 1])] += 1
        self.cnt[self.n] = top
        for g, c in top.items():
            self.tot[self.n][g[:-1]] += c
            self.typ[self.n][g[:-1]] += 1
        for k in range(self.n - 1, 0, -1):
            cont = defaultdict(set)                            # k-gram -> distinct left symbols
            for g in self.cnt[k + 1]:
                cont[g[1:]].add(g[0])
            self.cnt[k] = Counter({g: len(v) for g, v in cont.items()})
            for g, c in self.cnt[k].items():
                self.tot[k][g[:-1]] += c
                self.typ[k][g[:-1]] += 1
        self.total1 = sum(self.cnt[1].values())
        unknown = {g[0] for g in self.cnt[1]} - set(self.V)
        if unknown:
            raise ValueError(f"symbols outside the vocabulary: {sorted(unknown)[:5]}")
        return self

    def p(self, w, hist):
        """P(w | hist), hist a tuple of at most n-1 symbols, most recent last."""
        k = len(hist) + 1
        if k == 1:
            return (max(self.cnt[1].get((w,), 0) - self.D, 0) / self.total1
                    + self.D * len(self.cnt[1]) / self.total1 / len(self.V))
        n_h = self.tot[k].get(hist, 0)
        if n_h == 0:
            return self.p(w, hist[1:])
        return (max(self.cnt[k].get(hist + (w,), 0) - self.D, 0) / n_h
                + self.D * self.typ[k][hist] / n_h * self.p(w, hist[1:]))

    def surprisal(self, seq):
        """Total surprisal in bits of the sequence followed by END."""
        s = [BOS] * (self.n - 1) + list(seq) + [END]
        return -sum(math.log2(self.p(s[i], tuple(s[i - self.n + 1:i])))
                    for i in range(self.n - 1, len(s)))


class NeuralOrderModel:
    """A one-layer GRU over the same constituent-order symbols, with the same interface as KNGram.

    The capacity curve (RQ1_WORK_PLAN.md K1) varies the n-gram order and the training data and finds the
    absorbed share saturating near a third. That is evidence about one model family. This is a different
    family -- a recurrent net with a learned embedding, no Markov horizon and no discount -- fitted to the
    same cross-fitted folds, so the question "would a better structure model absorb more of T?" is asked
    of something that is not an n-gram at all.

    Deliberately small: the sequences are a handful of symbols long and the vocabulary is under a
    thousand, so anything larger would fit the training folds rather than the language. A slice of each
    training fold is held out to stop training, and the stopping epoch is reported.
    """

    def __init__(self, vocab, hidden=128, emb=64, epochs=40, lr=2e-3, patience=3, seed=707, device=None):
        self.V = sorted(set(vocab) | {END, BOS})
        self.ix = {w: i for i, w in enumerate(self.V)}
        self.hidden, self.emb, self.epochs, self.lr, self.patience = hidden, emb, epochs, lr, patience
        self.seed, self.device = seed, device
        self.stopped_at = None

    def _batch(self, seqs, torch):
        """(input ids, target ids, mask) with BOS prepended and END appended, padded."""
        rows = [[self.ix[BOS]] + [self.ix[w] for w in s] + [self.ix[END]] for s in seqs]
        n = max(len(r) for r in rows)
        x = torch.zeros(len(rows), n - 1, dtype=torch.long)
        y = torch.zeros(len(rows), n - 1, dtype=torch.long)
        m = torch.zeros(len(rows), n - 1, dtype=torch.bool)
        for i, r in enumerate(rows):
            x[i, :len(r) - 1] = torch.tensor(r[:-1])
            y[i, :len(r) - 1] = torch.tensor(r[1:])
            m[i, :len(r) - 1] = True
        return x, y, m

    def fit(self, sequences):
        import torch
        from torch import nn
        torch.manual_seed(self.seed)
        dev = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = dev
        g = torch.Generator().manual_seed(self.seed)
        perm = torch.randperm(len(sequences), generator=g).tolist()
        cut = max(1, int(0.1 * len(sequences)))
        dev_seqs = [sequences[i] for i in perm[:cut]]
        tr_seqs = [sequences[i] for i in perm[cut:]]

        self.net = self._make_net(len(self.V)).to(dev)
        opt = torch.optim.Adam(self.net.parameters(), lr=self.lr)
        lossf = nn.CrossEntropyLoss(reduction="none")
        xd, yd, md = [t.to(dev) for t in self._batch(dev_seqs, torch)]
        best, bad, state = float("inf"), 0, None
        bs = 256
        for ep in range(1, self.epochs + 1):
            self.net.train()
            order = torch.randperm(len(tr_seqs), generator=g).tolist()
            for i in range(0, len(order), bs):
                chunk = [tr_seqs[j] for j in order[i:i + bs]]
                x, y, m = [t.to(dev) for t in self._batch(chunk, torch)]
                loss = (lossf(self.net(x).transpose(1, 2), y) * m).sum() / m.sum()
                opt.zero_grad()
                loss.backward()
                opt.step()
            self.net.eval()
            with torch.no_grad():
                dl = float(((lossf(self.net(xd).transpose(1, 2), yd) * md).sum() / md.sum()).item())
            if dl < best - 1e-4:
                best, bad = dl, 0
                state = {k: v.detach().clone() for k, v in self.net.state_dict().items()}
            else:
                bad += 1
                if bad >= self.patience:
                    break
            self.stopped_at = ep
        if state is not None:
            self.net.load_state_dict(state)
        self.net.eval()
        return self

    def _make_net(self, V):
        """The network: an embedding, a one-layer GRU and an output layer. A subclass replaces this
        and nothing else, so every order model is fitted, stopped and scored the same way."""
        from torch import nn

        class Net(nn.Module):
            def __init__(self, V, emb, hidden):
                super().__init__()
                self.e = nn.Embedding(V, emb)
                self.r = nn.GRU(emb, hidden, batch_first=True)
                self.o = nn.Linear(hidden, V)

            def forward(self, x):
                return self.o(self.r(self.e(x))[0])

        return Net(V, self.emb, self.hidden)

    def surprisal(self, seq):
        """Total surprisal in bits of the sequence followed by END."""
        import torch
        x, y, m = [t.to(self.device) for t in self._batch([list(seq)], torch)]
        with torch.no_grad():
            lp = torch.log_softmax(self.net(x), dim=-1)[0]
        idx = torch.arange(lp.shape[0], device=self.device)
        bits = -lp[idx, y[0]] / math.log(2)
        return float((bits * m[0]).sum().item())

    def check_normalised(self, contexts):
        """Max |1 - Σ_w p(w | context)| over some contexts: a surprisal is only a surprisal if this is 0."""
        import torch
        worst = 0.0
        for c in contexts:
            x, _, _ = self._batch([list(c)], torch)
            with torch.no_grad():
                p = torch.softmax(self.net(x.to(self.device)), dim=-1)[0, -1]
            worst = max(worst, abs(float(p.sum().item()) - 1.0))
        return worst


class TransformerOrderModel(NeuralOrderModel):
    """A small causal transformer over the order symbols, the capacity axis's third family
    (RQ1_WORK_PLAN.md K1b). Same folds, same early stopping on a held-out slice of each training fold,
    same scoring as the GRU; only the network differs. Fixed before any result: model width 64, two
    layers, four heads, feed-forward 128, dropout 0.1, learned positions, Adam at 1e-3, at most 60
    epochs with patience 5."""

    def __init__(self, vocab, d=64, layers=2, heads=4, ff=128, dropout=0.1, max_len=160, epochs=60,
                 lr=1e-3, patience=5, seed=707, device=None):
        super().__init__(vocab, hidden=d, emb=d, epochs=epochs, lr=lr, patience=patience, seed=seed,
                         device=device)
        self.layers, self.heads, self.ff, self.dropout, self.max_len = layers, heads, ff, dropout, max_len

    def _make_net(self, V):
        import torch
        from torch import nn
        d, L, H, F, P, maxlen = self.emb, self.layers, self.heads, self.ff, self.dropout, self.max_len

        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.e = nn.Embedding(V, d)
                self.p = nn.Embedding(maxlen, d)
                layer = nn.TransformerEncoderLayer(d, H, F, P, batch_first=True)
                self.t = nn.TransformerEncoder(layer, L)
                self.o = nn.Linear(d, V)

            def forward(self, x):
                n = x.shape[1]
                if n > maxlen:
                    raise ValueError(f"sequence of {n} symbols is longer than max_len {maxlen}")
                pos = torch.arange(n, device=x.device)
                causal = torch.triu(torch.full((n, n), float("-inf"), device=x.device), diagonal=1)
                return self.o(self.t(self.e(x) + self.p(pos), mask=causal))

        return Net()


class UnigramBaseline:
    """Add-one unigram over the same vocabulary: the sanity floor the trigram must beat."""

    def __init__(self, vocab):
        self.V = sorted(set(vocab) | {END})

    def fit(self, sequences):
        self.c = Counter(w for seq in sequences for w in list(seq) + [END])
        self.n = sum(self.c.values())
        return self

    def surprisal(self, seq):
        return -sum(math.log2((self.c.get(w, 0) + 1) / (self.n + len(self.V))) for w in list(seq) + [END])
