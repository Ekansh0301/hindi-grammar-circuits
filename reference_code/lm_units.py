#!/usr/bin/env python3
"""Word-level and layer-level quantities from masked LMs (RQ1_WORK_PLAN.md D1; PREREGISTRATION_DRAFT.md 6.2, 7).

Everything is keyed to WHITESPACE words of the sentence text, which are the tree tokens (NULL
removed), so a word's value can be tied to its reference tree index. Surprisal itself is computed
exactly as pll_scorer.word_surprisals does (within_word_l2r over the tokenizer's own words, which
can split a tree token such as ९.३० into several); those values are then summed into whitespace
words, so the per-word values add up to the existing sentence scores.

  score_words      per whitespace word: surprisal at the final layer and, through the model's own
                   MLM head applied to every hidden layer, at each layer (logit lens)
  pooled_states    mean of each layer's hidden states over the sentence's subtokens, and the mean
                   of the embedding sum before the embedding LayerNorm (the layer-0 identity input)
  window_words     per whitespace word: surprisal with only w words of context on each side, the
                   other words removed from the input
"""
import bisect
import math

import torch


def mlm_head(model):
    return model.cls if hasattr(model, "cls") else model.lm_head


def whitespace_groups(tok, text):
    """(ids with specials, HF-word subtoken groups, whitespace word of each group, n words).

    Groups follow the tokenizer's `word_ids()`, as in pll_scorer.group_words. Each group is assigned
    to the whitespace word containing its first non-empty character span."""
    words = text.split(" ")
    starts, c = [], 0
    for w in words:
        starts.append(c)
        c += len(w) + 1
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    inner = enc["input_ids"]
    if not inner:
        return None
    ids = [tok.cls_token_id] + inner + [tok.sep_token_id]
    groups, gw, cur, prev = [], [], [], object()
    offs = enc["offset_mapping"]
    for i, w in enumerate(enc.word_ids()):
        if w is None:
            continue
        if w != prev and cur:
            groups.append(cur)
            cur = []
        cur.append(1 + i)
        prev = w
    if cur:
        groups.append(cur)
    for g in groups:
        spans = [offs[p - 1] for p in g if offs[p - 1][1] > offs[p - 1][0]]
        ch = spans[0][0] if spans else offs[g[0] - 1][0]
        gw.append(bisect.bisect_right(starts, ch) - 1)
    return ids, groups, gw, len(words)


def _l2r_passes(groups, only=None):
    out = []
    for k, pos in enumerate(groups):
        if only is not None and k not in only:
            continue
        for j, p in enumerate(pos):
            out.append((list(pos[j:]), p, k))
    return out


@torch.inference_mode()
def score_words(model, tok, device, text, batch_size=32, layers=True, max_subtokens=256, translators=None,
                hide_words=None):
    """Per whitespace word: final-layer surprisal (bits), subtoken count, and a
    [n_layers + 1] list of logit-lens surprisals (None if layers=False).
    Returns None for empty or over-long input.

    `hide_words` (whitespace word indices) are masked in every pass and not scored: the model knows
    something stands there and how many subtokens long it is, but not what (rq1_verb_blind.py). Their
    surprisal entries stay 0 and their subtoken counts are returned as 0, so a per-subtoken mean over
    the result counts only scored words. With None, the passes are exactly those of before."""
    g = whitespace_groups(tok, text)
    if g is None or len(g[0]) > max_subtokens:
        return None
    ids, groups, gw, nw = g
    hidden = set(hide_words or ())
    passes = _l2r_passes(groups, only={k for k in range(len(groups)) if gw[k] not in hidden} if hidden else None)
    if hidden:
        ids = list(ids)
        for k, pos in enumerate(groups):
            if gw[k] in hidden:
                for q in pos:
                    ids[q] = tok.mask_token_id
    head = mlm_head(model)
    n_layers = model.config.num_hidden_layers + 1
    final = [0.0] * nw
    lens = [[0.0] * n_layers for _ in range(nw)] if layers else None
    nsub = [0] * nw
    for k, pos in enumerate(groups):
        if gw[k] not in hidden:
            nsub[gw[k]] += len(pos)
    vocab = model.config.vocab_size
    per_row = vocab * (n_layers if layers else 1)
    bs = max(1, min(batch_size, int(2.0e9 / (4 * per_row)) or 1))
    base = torch.tensor([ids], device=device)
    s = 0
    while s < len(passes):
        chunk = passes[s:s + bs]
        batch = base.repeat(len(chunk), 1)
        for r, (mask_pos, _, _) in enumerate(chunk):
            batch[r, mask_pos] = tok.mask_token_id
        try:
            out = model(input_ids=batch, attention_mask=torch.ones_like(batch), output_hidden_states=layers)
        except torch.OutOfMemoryError:
            del batch
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
            continue
        rows = torch.arange(len(chunk), device=device)
        pos = torch.tensor([p for _, p, _ in chunk], device=device)
        tgt = torch.tensor([ids[p] for _, p, _ in chunk], device=device)
        lp = torch.log_softmax(out.logits[rows, pos].float(), -1)
        vals = (-lp.gather(1, tgt[:, None])[:, 0] / math.log(2)).tolist()
        for (_, _, k), v in zip(chunk, vals):
            final[gw[k]] += v
        if layers:
            for li, hs in enumerate(out.hidden_states):
                h = hs[rows, pos]
                if translators is not None and li < len(translators):
                    h = translators[li](h)
                lpl = torch.log_softmax(head(h).float(), -1)
                vl = (-lpl.gather(1, tgt[:, None])[:, 0] / math.log(2)).tolist()
                for (_, _, k), v in zip(chunk, vl):
                    lens[gw[k]][li] += v
        s += len(chunk)
    return final, nsub, lens


@torch.inference_mode()
def pooled_states(model, tok, device, text, max_subtokens=512):
    """(per-layer mean hidden state [n_layers+1, d], mean pre-LayerNorm embedding sum [d]) over the
    sentence's subtokens, special tokens excluded; None if empty or too long."""
    g = whitespace_groups(tok, text)
    if g is None or len(g[0]) > max_subtokens:
        return None
    ids = torch.tensor([g[0]], device=device)
    captured = {}
    ln = model.base_model.embeddings.LayerNorm
    h = ln.register_forward_pre_hook(lambda m, inp: captured.__setitem__("x", inp[0].detach()))
    try:
        out = model.base_model(input_ids=ids, attention_mask=torch.ones_like(ids), output_hidden_states=True)
    finally:
        h.remove()
    hs = torch.stack([x[0, 1:-1].float().mean(0) for x in out.hidden_states])
    pre = captured["x"][0, 1:-1].float().mean(0)
    return hs.cpu(), pre.cpu()


@torch.inference_mode()
def window_words(model, tok, device, text, w, batch_size=64, max_subtokens=256):
    """Per whitespace word: surprisal (bits) with only the w words on each side visible."""
    words = text.split(" ")
    rows = []                                        # (ids, mask positions, scored position, word)
    for k in range(len(words)):
        lo = max(0, k - w)
        g = whitespace_groups(tok, " ".join(words[lo:k + w + 1]))
        if g is None or len(g[0]) > max_subtokens:
            return None
        ids, groups, gw, _ = g
        target = {i for i, x in enumerate(gw) if x == k - lo}
        for mask_pos, p, _ in _l2r_passes(groups, only=target):
            rows.append((ids, mask_pos, p, k))
    out = [0.0] * len(words)
    pad = tok.pad_token_id
    for s in range(0, len(rows), batch_size):
        chunk = rows[s:s + batch_size]
        L = max(len(r[0]) for r in chunk)
        batch = torch.full((len(chunk), L), pad, device=device)
        att = torch.zeros((len(chunk), L), dtype=torch.long, device=device)
        for i, (ids, mask_pos, _, _) in enumerate(chunk):
            batch[i, :len(ids)] = torch.tensor(ids, device=device)
            att[i, :len(ids)] = 1
            batch[i, mask_pos] = tok.mask_token_id
        logits = model(input_ids=batch, attention_mask=att).logits
        ri = torch.arange(len(chunk), device=device)
        pos = torch.tensor([r[2] for r in chunk], device=device)
        tgt = torch.tensor([r[0][r[2]] for r in chunk], device=device)
        lp = torch.log_softmax(logits[ri, pos].float(), -1)
        for (_, _, _, k), v in zip(chunk, (-lp.gather(1, tgt[:, None])[:, 0] / math.log(2)).tolist()):
            out[k] += v
    return out


def set1_surface_indices(ref_rows, var_row, var_rows):
    """Reference tree index of every surface (non-NULL) word of the reference and of the variant.

    The variant's indices come from inverting the generator's renumbering for the stored unit
    order, and are checked word by word against the reference forms."""
    import set1_generator as G
    from materialise_set1 import official_tokens
    toks = official_tokens(ref_rows)
    by = {t["idx"]: t for t in toks}
    ref_idx = [t["idx"] for t in toks if not G.is_null(t)]
    clause, _ = G.analyse_clause(toks, int(var_row["clause_head"]))
    m = G.renumber(toks, clause, [int(x) for x in var_row["order"].split("|")])
    inv = {new: old for old, new in m.items()}
    var_idx = [inv[int(r[0])] for r in var_rows if r[1].strip().upper() != "NULL"]
    forms = [r[1] for r in var_rows if r[1].strip().upper() != "NULL"]
    if [by[i]["form"] for i in var_idx] != forms:
        raise ValueError(f"{var_row['var_id']}: variant words do not map onto the reference")
    return ref_idx, var_idx


@torch.inference_mode()
def token_states(model, tok, device, text, max_subtokens=512):
    """(hidden states [n_layers+1, n_subtokens, d], pre-LayerNorm embedding sum [n_subtokens, d],
    {subtoken position: whitespace word}) for one sentence, special tokens included in the arrays."""
    g = whitespace_groups(tok, text)
    if g is None or len(g[0]) > max_subtokens:
        return None
    ids, groups, gw, _ = g
    word_of = {p: gw[k] for k, pos in enumerate(groups) for p in pos}
    x = torch.tensor([ids], device=device)
    captured = {}
    h = model.base_model.embeddings.LayerNorm.register_forward_pre_hook(
        lambda m, inp: captured.__setitem__("x", inp[0].detach()))
    try:
        out = model.base_model(input_ids=x, attention_mask=torch.ones_like(x), output_hidden_states=True)
    finally:
        h.remove()
    return torch.stack(out.hidden_states)[:, 0].float().cpu(), captured["x"][0].float().cpu(), word_of


CASE_LABELS = {"0": "0", "ने": "ne", "को": "ko", "से": "se", "में": "me", "पर": "par", "का": "ka", "के": "ka", "की": "ka"}


def unit_word_positions(ref_rows, clause_head):
    """For each unit of the clause: (head idx, relation, case label, surface word positions of the
    unit WITHOUT its own postpositions), skipping units headed by a fused case pronoun
    (PREREGISTRATION_DRAFT.md 7.3 clarification)."""
    import order_model as O
    import set1_generator as G
    from materialise_set1 import official_tokens
    toks = official_tokens(ref_rows)
    by = {t["idx"]: t for t in toks}
    kids = G.children(toks)
    surface = [t["idx"] for t in toks if not G.is_null(t)]
    pos_of = {i: p for p, i in enumerate(surface)}
    clause, _ = G.analyse_clause(toks, int(clause_head))
    out = []
    for d in clause["units"]:
        rep = O.representative(by, kids, d)
        if G.fused_case_pronoun(by[rep]):
            continue
        own = {c for h in {d, rep} for c in kids.get(h, []) if by[c]["deprel"] == "lwg__psp"}
        words = [pos_of[i] for i in clause["spans"][d] if i in pos_of and i not in own]
        if not words:
            continue
        m = O.marker(by, kids, d)
        out.append((d, by[d]["deprel"], CASE_LABELS.get(m, "other"), words))
    return out


# ============================================================================= causal LMs
# Byte-level BPE models (Qwen2.5, LLaMA-3, Airavata) attach the space to the START of a word's first token.
# Every sentence is given a leading space, so each word is tokenised as " word" wherever it stands and a
# reference and its variant contain the same token multiset (checked per pair). Word surprisal is the sum of
# the word's token surprisals ("raw"), plus the whitespace correction of Oh and Schuler (2024) / Pimentel and
# Meister (2024): s(w_k) = raw_k − log2 B_k + log2 B_{k−1}, where B_k is the probability that the token after
# word k begins a new word (a whitespace-initial token, or end of text after the last word) and B_0 the same
# probability before the first word.

def load_causal_lm(model_name, device=None, dtype="auto"):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(model_name)
    td = {"auto": (torch.bfloat16 if device == "cuda" else torch.float32), "float32": torch.float32,
          "bfloat16": torch.bfloat16, "float16": torch.float16}[dtype]
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=td).to(device).eval()
    return model, tok, device


def is_causal(model):
    return any("CausalLM" in a for a in (getattr(model.config, "architectures", None) or []))


def start_id(tok):
    return tok.bos_token_id if tok.bos_token_id is not None else tok.eos_token_id


_SPACE_IDS = {}


def space_initial_ids(tok):
    """Token ids whose surface form begins with whitespace, plus end of text."""
    key = id(tok)
    if key not in _SPACE_IDS:
        ids = []
        for t, i in tok.get_vocab().items():
            s = tok.convert_tokens_to_string([t])
            if s[:1].isspace():
                ids.append(i)
        if tok.eos_token_id is not None:
            ids.append(tok.eos_token_id)
        _SPACE_IDS[key] = torch.tensor(sorted(set(ids)))
    return _SPACE_IDS[key]


def causal_tokens(tok, text):
    """(ids with the start token, word index of each non-start token, n words); text gets a leading space."""
    words = text.split(" ")
    s = " " + text
    starts, c = [], 1
    for w in words:
        starts.append(c)
        c += len(w) + 1
    enc = tok(s, add_special_tokens=False, return_offsets_mapping=True)
    wi = []
    for a, b in enc["offset_mapping"]:
        while a < b and s[a].isspace():
            a += 1
        wi.append(max(0, bisect.bisect_right(starts, a) - 1))
    return [start_id(tok)] + enc["input_ids"], wi, len(words)


def token_multiset(tok, text):
    ids, _, _ = causal_tokens(tok, text)
    return sorted(ids[1:])


def final_norm(model):
    base = model.base_model
    return getattr(base, "norm", None) or getattr(base, "final_layernorm", None)


@torch.inference_mode()
def causal_words(model, tok, device, text, layers=True, max_tokens=512):
    """Per whitespace word: corrected surprisal, raw surprisal (bits), token count, logit-lens raw surprisal
    per layer (None if layers=False). None if the input is too long."""
    ids, wi, nw = causal_tokens(tok, text)
    if len(ids) > max_tokens:
        return None
    x = torch.tensor([ids], device=device)
    out = model(input_ids=x, output_hidden_states=layers)
    logp = torch.log_softmax(out.logits[0].float(), -1)                    # position t predicts token t+1
    tgt = x[0, 1:]
    tok_s = (-logp[:-1].gather(1, tgt[:, None])[:, 0] / math.log(2)).tolist()
    sp = space_initial_ids(tok).to(device)
    bow = (torch.logsumexp(logp[:, sp], -1) / math.log(2)).tolist()        # log2 P(next token starts a word)
    raw = [0.0] * nw
    nsub = [0] * nw
    last = [0] * nw                                                       # position of each word's last token
    for j, (w, s_) in enumerate(zip(wi, tok_s)):
        raw[w] += s_
        nsub[w] += 1
        last[w] = j + 1
    first_pos = 0                                                         # the start token predicts word 1
    corr = []
    prev = bow[first_pos]
    for k in range(nw):
        b_k = bow[last[k]]
        corr.append(raw[k] - b_k + prev)
        prev = b_k
    lens = None
    if layers:
        norm, head = final_norm(model), model.get_output_embeddings()
        lens = [[0.0] * len(out.hidden_states) for _ in range(nw)]
        for li, hs in enumerate(out.hidden_states):
            h = hs[0, :-1]
            if li < len(out.hidden_states) - 1 and norm is not None:
                h = norm(h)
            lp = torch.log_softmax(head(h).float(), -1)
            vals = (-lp.gather(1, tgt[:, None])[:, 0] / math.log(2)).tolist()
            for w, v in zip(wi, vals):
                lens[w][li] += v
    return corr, raw, nsub, lens


@torch.inference_mode()
def causal_pooled(model, tok, device, text, max_tokens=512):
    """(per-layer mean hidden state over the sentence's tokens, start token excluded; mean input embedding)."""
    ids, _, _ = causal_tokens(tok, text)
    if len(ids) > max_tokens:
        return None
    x = torch.tensor([ids], device=device)
    out = model(input_ids=x, output_hidden_states=True)
    hs = torch.stack([h[0, 1:].float().mean(0) for h in out.hidden_states])
    emb = model.get_input_embeddings()(x)[0, 1:].float().mean(0)
    return hs.cpu(), emb.cpu()


@torch.inference_mode()
def causal_window(model, tok, device, text, w, batch_size=64):
    """Per whitespace word: raw surprisal (bits) with only the w preceding words as context."""
    words = text.split(" ")
    rows = []
    for k in range(len(words)):
        ids, wi, _ = causal_tokens(tok, " ".join(words[max(0, k - w):k + 1]))
        tgt_word = k - max(0, k - w)
        rows.append((ids, [j + 1 for j, x in enumerate(wi) if x == tgt_word], k))
    out = [0.0] * len(words)
    pad = tok.pad_token_id if tok.pad_token_id is not None else start_id(tok)
    for s in range(0, len(rows), batch_size):
        chunk = rows[s:s + batch_size]
        L = max(len(r[0]) for r in chunk)
        batch = torch.full((len(chunk), L), pad, device=device)
        att = torch.zeros((len(chunk), L), dtype=torch.long, device=device)
        for i, (ids, _, _) in enumerate(chunk):
            batch[i, :len(ids)] = torch.tensor(ids, device=device)
            att[i, :len(ids)] = 1
        logp = torch.log_softmax(model(input_ids=batch, attention_mask=att).logits.float(), -1)
        for i, (ids, pos, k) in enumerate(chunk):
            for p in pos:
                out[k] += float(-logp[i, p - 1, ids[p]] / math.log(2))
    return out


class Translator(torch.nn.Module):
    """Tuned-lens translator for one layer: h + W h + b, initialised to the identity (Belrose et al. 2023)."""

    def __init__(self, d):
        super().__init__()
        self.lin = torch.nn.Linear(d, d)
        torch.nn.init.zeros_(self.lin.weight)
        torch.nn.init.zeros_(self.lin.bias)

    def forward(self, h):
        return h + self.lin(h.to(self.lin.weight.dtype)).to(h.dtype)
