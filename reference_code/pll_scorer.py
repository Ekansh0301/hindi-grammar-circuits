#!/usr/bin/env python3
"""
Masked-LM pseudo-log-likelihood scoring, with the three metrics that matter
for this project kept side by side so they can be compared rather than
assumed equivalent.

WHY THIS MODULE EXISTS
----------------------
Section 6.2 of the proposal specifies `within_word_l2r` and explicitly
rejects simultaneous whole-word masking:

    "We do not use simultaneous whole-word masking because it violates the
    conditional independence assumptions required for joint probability
    estimation."

Earlier runs in this project used whole-word masking anyway, so every
masked-LM number produced before this module is provisional against it.
Rather than silently switch, all three metrics are implemented here and
`verify_masking_metric.py` measures how far apart they actually are.

THE THREE METRICS
-----------------
Let word k consist of subtokens t_1..t_m at positions p_1..p_m.

  original          (Salazar et al. 2020, and the metric the related paper
                     uses -- "by masking one token at a time")
                     score t_j with only p_j masked.

  within_word_l2r   (Kauf & Ivanova 2023; the proposal's choice)
                     score t_j with p_j..p_m masked -- that subtoken and
                     every later subtoken of the SAME word. Earlier
                     subtokens of the word stay visible; all other words
                     stay visible. Prevents the model reconstructing a word
                     from its own remaining pieces, which is what inflates
                     `original` on multi-subword words.

  whole_word        score every t_j with all of p_1..p_m masked, in ONE
                     forward pass. This is what the proposal rejects: the
                     m predictions are treated as independent when they are
                     not, so the "joint" probability it implies is not one.

For a word that is a single subtoken all three coincide exactly. The
metrics can therefore only differ to the extent that the tokenizer
fragments words -- which is why the verification script reports fertility
first.

Word-level surprisal is the SUM over the word's subtokens, in bits;
sentence-level features are computed from that per-word sequence.
"""
import math

import torch


def group_words(tok, text):
    """Subtoken positions grouped by word, plus the id sequence with special
    tokens attached.

    Grouping uses HF `word_ids()` rather than a "##" prefix test. "##" is
    WordPiece-specific: mBERT/MuRIL/IndicBERT use it, XLM-R is SentencePiece
    and marks word STARTS with a boundary marker instead, so a "##" test
    never fires there and every subpiece becomes its own "word". Measured on
    a 6-word Hindi sentence, "##"-grouping gave 6 words for mBERT (correct)
    and 8 for XLM-R (wrong); word_ids() gives 6 for both.
    """
    enc = tok(text, add_special_tokens=False)
    inner = enc["input_ids"]
    if not inner:
        return None, None
    ids = [tok.cls_token_id] + inner + [tok.sep_token_id]
    wids = enc.word_ids()
    groups, cur, prev = [], [], object()
    for i, w in enumerate(wids):
        if w is None:
            continue
        if w != prev and cur:
            groups.append(cur)
            cur = []
        cur.append(1 + i)          # +1 for the leading [CLS]
        prev = w
    if cur:
        groups.append(cur)
    return ids, groups


def mask_passes(groups, metric):
    """Forward passes required by a metric.

    Each pass is (mask_positions, [(scored_position, word_index), ...]).
    """
    passes = []
    for k, pos in enumerate(groups):
        if metric == "whole_word":
            passes.append((list(pos), [(p, k) for p in pos]))
        elif metric == "original":
            for p in pos:
                passes.append(([p], [(p, k)]))
        elif metric == "within_word_l2r":
            for j, p in enumerate(pos):
                passes.append((list(pos[j:]), [(p, k)]))
        else:
            raise ValueError(f"unknown metric {metric!r}")
    return passes


def group_words_with_context(tok, context, text, max_len):
    """Like group_words, but with a discourse context placed before the target.

    The context and target are tokenised SEPARATELY and concatenated, so the
    target's subtokens -- and therefore its word grouping -- are identical with
    and without context. A comparison of the two conditions then differs only in
    what the model can see, never in what is being scored. If the sequence would
    exceed the model's length, the context is cut from the LEFT (the sentence
    nearest the target is kept) and the cut is reported.
    Returns (ids, groups, n_context_tokens_dropped) or (None, None, 0).
    """
    enc = tok(text, add_special_tokens=False)
    inner = enc["input_ids"]
    if not inner:
        return None, None, 0
    ctx = tok(context, add_special_tokens=False)["input_ids"] if context else []
    room = max_len - 2 - len(inner)
    if room < 0:
        return None, None, 0
    dropped = max(0, len(ctx) - room)
    ctx = ctx[dropped:]
    ids = [tok.cls_token_id] + ctx + inner + [tok.sep_token_id]
    off = 1 + len(ctx)
    groups, cur, prev = [], [], object()
    for i, w in enumerate(enc.word_ids()):
        if w is None:
            continue
        if w != prev and cur:
            groups.append(cur)
            cur = []
        cur.append(off + i)
        prev = w
    if cur:
        groups.append(cur)
    return ids, groups, dropped


@torch.inference_mode()
def word_surprisals(model, tok, device, text, metric="within_word_l2r",
                    batch_size=32, max_subtokens=256, context=None, return_dropped=False):
    """Per-word surprisal in bits, plus the subtoken count of each word.

    Returns (surprisals, fertilities) or (None, None) for empty input.
    Batched explicitly: one masked copy per pass, and a single unbatched
    batch of (n_passes x seq_len x vocab) logits OOMs on longer sentences.
    """
    dropped = 0
    if context is None:
        ids, groups = group_words(tok, text)
        if groups and len(ids) > max_subtokens:  # guard, not a silent truncation
            groups = None
    else:
        ids, groups, dropped = group_words_with_context(tok, context, text, max_subtokens)
    if not groups:
        return (None, None, dropped) if return_dropped else (None, None)
    passes = mask_passes(groups, metric)
    base = torch.tensor([ids], device=device)
    per_word = [0.0] * len(groups)
    # The model materialises FULL logits (batch x sequence x vocabulary) before any
    # position can be selected, so a fixed batch size is only safe for short inputs.
    # With a 512-token context and MuRIL's 197k vocabulary, batch 32 needs ~12.6 GB
    # and killed an RQ3 shard. Batches are therefore sized by tokens, scaled to the
    # vocabulary, keeping the logits under ~2.5 GB; an OOM still halves and retries.
    vocab = getattr(getattr(model, "config", None), "vocab_size", 120000)
    token_budget = max(len(ids), int(2.5e9 / (4 * vocab)))
    bs = max(1, min(batch_size, token_budget // len(ids)))
    s = 0
    while s < len(passes):
        chunk = passes[s:s + bs]
        batch = base.repeat(len(chunk), 1)
        for r, (mask_pos, _) in enumerate(chunk):
            for p in mask_pos:
                batch[r, p] = tok.mask_token_id
        try:
            logits = model(input_ids=batch,
                           attention_mask=torch.ones_like(batch)).logits
        except torch.OutOfMemoryError:
            del batch
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
            continue
        # Gather only the positions actually scored BEFORE the softmax. Taking
        # log_softmax over the full (batch x seq x vocab) tensor materialises a
        # second float32 copy of it -- ~3 GB for MuRIL's 197k vocab at batch 32
        # -- and OOMs an 11 GB card on long sentences for no reason, since at
        # most one position per row is read.
        rows_i, pos_i, word_i = [], [], []
        for r, (_, scored) in enumerate(chunk):
            for p, k in scored:
                rows_i.append(r)
                pos_i.append(p)
                word_i.append(k)
        sel = logits[torch.tensor(rows_i, device=device),
                     torch.tensor(pos_i, device=device)].float()
        lp = torch.log_softmax(sel, dim=-1)
        tgt = torch.tensor([ids[p] for p in pos_i], device=device)
        vals = -lp.gather(1, tgt.unsqueeze(1)).squeeze(1) / math.log(2)
        for k, v in zip(word_i, vals.tolist()):
            per_word[k] += v
        s += len(chunk)
    fert = [len(g) for g in groups]
    return (per_word, fert, dropped) if return_dropped else (per_word, fert)


# ---------------------------------------------------------------------------
# Sentence-level features.
#
# The nine features follow the related paper's Section 3.3 definitions
# verbatim, so our numbers are directly comparable to its Table 1:
#   Aggregate Load     : Sum, Mean, Mean_Q1 (mean of the TOP quartile of S)
#   Peak Difficulty    : Max, Max_2, Max_3 (three largest entries of S),
#                        Max_Norm_Score (max_i s_i / c_i, c_i = subtoken count,
#                        so long multi-subword words cannot dominate the peak)
#   Sequential         : Max_Adj_Sum (max_i s_i + s_{i+1})
#   Dispersion         : Std_Dev
#
# Mean_Q1 is the mean of the top quartile BY VALUE, not the first quarter of
# the sentence by position -- the paper's wording is "the mean of the top
# quartile of S". Getting this wrong would silently produce an incomparable
# feature.
#
# The proposal's own analysis uses Mean only; the other eight are a declared
# extension and are reported separately.
# ---------------------------------------------------------------------------
FEATURES = ["Sum", "Mean", "Mean_Q1", "Max", "Max_2", "Max_3",
            "Max_Norm_Score", "Max_Adj_Sum", "Std_Dev"]


def sentence_features(s, fert):
    if not s:
        return None
    n = len(s)
    srt = sorted(s, reverse=True)
    q = max(1, round(n / 4))
    mean = sum(s) / n
    var = sum((x - mean) ** 2 for x in s) / n
    return {
        "Sum": sum(s),
        "Mean": mean,
        "Mean_Q1": sum(srt[:q]) / q,
        "Max": srt[0],
        "Max_2": srt[1] if n > 1 else srt[0],
        "Max_3": srt[2] if n > 2 else srt[-1],
        "Max_Norm_Score": max(x / c for x, c in zip(s, fert)),
        "Max_Adj_Sum": max((s[i] + s[i + 1] for i in range(n - 1)), default=s[0]),
        "Std_Dev": math.sqrt(var),
    }


def load_masked_lm(model_name, device=None):
    from transformers import AutoModelForMaskedLM, AutoTokenizer
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name).to(device).eval()
    return model, tok, device
