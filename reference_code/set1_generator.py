#!/usr/bin/env python3
"""Set 1 variant generation: complete preverbal constituents reordered, trees renumbered.

The rules are specified in SET1_CONSTRUCTION_PLAN.md (Sections 4 and 5); the rule names
below (R0 to R8) refer to that document. This module holds the logic only. The build
driver is build_set1.py, the unit tests are tests/test_set1_generator.py, and the
independent audit is audit_set1.py.

Input is HDTB IntraChunk CoNLL: word-level gold dependencies with Paninian labels.
A sentence is a list of token dicts with integer `idx` and `head`.
"""
import hashlib
import itertools
import random
import re
from collections import defaultdict

# R2: relations that belong to the verb complex and never move.
def is_verb_complex_rel(rel):
    return rel.startswith("lwg") or rel in ("pof", "pof__cn")

CONNECTIVE_RELS = {"sent-adv", "rad"}                       # R3
REL_MARKERS = {"जो", "जिस", "जिसे", "जिसने", "जिन", "जिन्हें", "जिन्होंने", "जहाँ", "जहां",
               "जब", "जैसे", "जितना", "जितने", "जितनी", "यदि", "अगर"}          # R5
CORRELATES = {"वह", "वो", "वे", "उस", "उसे", "उसने", "उन", "उन्हें", "उन्होंने", "वहाँ", "वहां",
              "तब", "तो", "वैसे", "उतना", "उतने", "उतनी"}
ENUMERATE_UP_TO = 7                                          # Section 5
SAMPLE_SIZE = 5039
SAMPLE_POOL = 20000


# Pronouns with the case marker fused into the word. HDTB often leaves their `vib` feature empty
# (e.g. किसने, WQ), so they would otherwise read as case-unmarked for R4.
FUSED_DATIVE_ACCUSATIVE = {"मुझे", "तुझे", "उसे", "इसे", "किसे", "जिसे", "हमें", "तुम्हें", "उन्हें",
                           "इन्हें", "किन्हें", "जिन्हें", "आपको"}


def fused_case_pronoun(tok):
    f = tok["form"]
    return tok.get("cpos") == "pn" and (f.endswith("ने") or f in FUSED_DATIVE_ACCUSATIVE)


def is_null(tok):
    return tok["form"].strip().upper() == "NULL"


def feats_dict(tok):
    return dict(kv.split("-", 1) for kv in tok.get("feats", "").split("|") if "-" in kv)


def children(tokens):
    kids = defaultdict(list)
    for t in tokens:
        kids[t["head"]].append(t["idx"])
    for k in kids:
        kids[k].sort()
    return kids


def subtree(kids, h):
    seen, stack = set(), [h]
    while stack:
        j = stack.pop()
        if j not in seen:
            seen.add(j)
            stack += kids.get(j, [])
    return sorted(seen)


def contiguous(ix):
    return bool(ix) and ix[-1] - ix[0] + 1 == len(ix)


def stable_seed(text, seed):
    return int(hashlib.sha256(f"{seed}:{text}".encode()).hexdigest()[:12], 16)


# ----------------------------------------------------------------------------- clauses
def clause_heads(tokens):
    """R0: [(clause_type, head idx)]. The root if it is a verb; otherwise each verbal
    conjunct of a coordinating root."""
    by = {t["idx"]: t for t in tokens}
    roots = [t for t in tokens if t["head"] == 0]
    if len(roots) != 1:
        return []
    root = roots[0]
    if root["cpos"] == "v":
        return [("main", root["idx"])]
    if root["cpos"] == "avy":
        kids = children(tokens)
        return [("conjunct", d) for d in kids.get(root["idx"], [])
                if by[d]["deprel"] == "ccof" and by[d]["cpos"] == "v"]
    return []


def analyse_clause(tokens, head):
    """Movable units of one clause and the constraints on them, or (None, reason)."""
    by = {t["idx"]: t for t in tokens}
    kids = children(tokens)
    pre = [d for d in kids.get(head, []) if d < head]
    vc = [d for d in pre if is_verb_complex_rel(by[d]["deprel"])]
    units = [d for d in pre if d not in vc and by[d]["deprel"] != "rsym"]
    if len(units) < 2:
        return None, "fewer than two units"
    spans = {d: subtree(kids, d) for d in units}
    if not all(contiguous(s) for s in spans.values()):
        return None, "R1 non-contiguous unit"
    vc_span = sorted(set(itertools.chain.from_iterable(subtree(kids, d) for d in vc)) | {head})
    if not contiguous(vc_span):
        return None, "R2 verb complex interrupted"
    units.sort(key=lambda d: spans[d][0])
    for a, b in zip(units, units[1:]):
        if spans[a][-1] + 1 != spans[b][0]:
            return None, "material between units"
    if spans[units[-1]][-1] + 1 != vc_span[0]:
        return None, "material between the last unit and the verb complex"

    surface = {d: [by[i]["form"] for i in spans[d] if not is_null(by[i])] for d in units}
    fixed = set()
    for i, d in enumerate(units):
        if not surface[d]:
            fixed.add(i)                                              # R6
        elif by[d]["deprel"] in CONNECTIVE_RELS or by[d]["cpos"] == "avy":
            fixed.add(i)                                              # R3

    holds = []
    # P6: agreement features of the verb complex, read from the rightmost verbal token that
    # specifies each feature (the finite auxiliary in periphrastic forms: खाता है has
    # gender on खाता and person on है).
    agr = {}
    for i in reversed(vc_span):
        if by[i]["xpos"] in ("VM", "VAUX"):
            for k, v in feats_dict(by[i]).items():
                if k in ("gen", "num", "pers") and v not in ("", "any") and k not in agr:
                    agr[k] = v

    def marked(d):
        vib = feats_dict(by[d]).get("vib", "")
        return (any(by[c]["deprel"] == "lwg__psp" for c in kids.get(d, [])) or vib not in ("", "0")
                or fused_case_pronoun(by[d]))

    def compatible(d):
        f = feats_dict(by[d])
        return all(f.get(k, "") in ("", "any") or agr.get(k, "") in ("", "any") or f[k] == agr[k]
                   for k in ("gen", "num", "pers"))
    k1 = [i for i, d in enumerate(units) if by[d]["deprel"] == "k1"]
    k2 = [i for i, d in enumerate(units) if by[d]["deprel"] == "k2"]
    for a in k1:
        for b in k2:
            da, db = units[a], units[b]
            if not marked(da) and not marked(db) and compatible(da) and compatible(db):
                holds.append(("R4", min(a, b), max(a, b)))            # R4
    rel = [i for i, d in enumerate(units) if surface[d] and surface[d][0] in REL_MARKERS]
    cor = [i for i, d in enumerate(units) if surface[d] and surface[d][0] in CORRELATES]
    for a in rel:
        for b in cor:
            if a != b:
                holds.append(("R5", min(a, b), max(a, b)))            # R5

    free = [i for i in range(len(units)) if i not in fixed]
    if len(free) < 2:
        return None, "fewer than two free units"
    markers = {d: tuple(by[c]["form"] for c in kids.get(d, []) if by[c]["deprel"] == "lwg__psp")
               for d in units}
    return {"head": head, "units": units, "spans": spans, "surface": surface,
            "fixed": fixed, "free": free, "holds": holds, "vc_span": vc_span,
            "region": (spans[units[0]][0], spans[units[-1]][-1]), "markers": markers,
            "rels": [by[d]["deprel"] for d in units]}, "ok"


# ----------------------------------------------------------------------------- orders
def renumber(tokens, clause, order):
    """Old idx -> new idx for a unit order (order[slot] = unit index)."""
    start, end = clause["region"]
    new_seq = []
    for slot in range(len(order)):
        new_seq += clause["spans"][clause["units"][order[slot]]]
    mapping = {t["idx"]: t["idx"] for t in tokens}
    for pos, old in enumerate(new_seq, start=start):
        mapping[old] = pos
    return mapping


def variant_tokens(tokens, clause, order):
    m = renumber(tokens, clause, order)
    out = []
    for t in tokens:
        u = dict(t)
        u["idx"] = m[t["idx"]]
        u["head"] = m[t["head"]] if t["head"] else 0
        out.append(u)
    out.sort(key=lambda x: x["idx"])
    return out


def severity(tokens, mapping):
    """(severity_abs, severity_net, n_arcs), the definitions of build_stratified_sample.py."""
    tot_abs = tot_net = n = 0
    for t in tokens:
        if not t["head"]:
            continue
        d0 = abs(t["idx"] - t["head"])
        d1 = abs(mapping[t["idx"]] - mapping[t["head"]])
        tot_abs += abs(d1 - d0)
        tot_net += d1 - d0
        n += 1
    return (tot_abs / n, abs(tot_net) / n, n) if n else (0.0, 0.0, 0)


def adjacent_swap(order, free):
    """True when exactly two movable units exchange places and no other movable unit lies
    between them (held units may). Kendall distance 1 over all slots misses the case where a
    held unit sits between the two."""
    moved = [s for s, u in enumerate(order) if u != s]
    if len(moved) != 2:
        return False
    a, b = moved
    return a in free and b in free and not any(a < f < b for f in free)


def kendall(order):
    return sum(1 for i in range(len(order)) for j in range(i + 1, len(order)) if order[i] > order[j])


def respects_holds(order, holds):
    pos = {u: s for s, u in enumerate(order)}
    return all(pos[a] < pos[b] for _, a, b in holds)


def candidate_orders(clause, ref_id, seed):
    k = len(clause["units"])
    free = clause["free"]
    ident = list(range(k))

    def build(perm):
        order = list(ident)
        for slot, u in zip(free, perm):
            order[slot] = u
        return order

    assert len(free) <= ENUMERATE_UP_TO, "larger clauses go through sampled_orders"
    for perm in itertools.permutations(free):
        yield build(perm)


def sampled_orders(tokens, clause, ref_id, seed):
    """Severity-stratified sample for clauses with more than ENUMERATE_UP_TO free units."""
    rng = random.Random(stable_seed(ref_id + f"@{clause['head']}", seed))
    k = len(clause["units"])
    free = clause["free"]
    seen, pool = set(), []
    tries = 0
    while len(pool) < SAMPLE_POOL and tries < SAMPLE_POOL * 5:
        tries += 1
        perm = rng.sample(free, len(free))
        order = list(range(k))
        for slot, u in zip(free, perm):
            order[slot] = u
        key = tuple(order)
        if key in seen:
            continue
        seen.add(key)
        sa, _, _ = severity(tokens, renumber(tokens, clause, order))
        pool.append((sa, key))
    pool.sort()
    bins = [pool[i * len(pool) // 5:(i + 1) * len(pool) // 5] for i in range(5)]
    per = SAMPLE_SIZE // 5
    chosen = []
    for b in bins:
        chosen += rng.sample(b, min(per, len(b)))
    return [list(key) for _, key in sorted(chosen, key=lambda x: x[1])]


def generate(tokens, ref_id, seed=707, attested=None):
    """All Set 1 variants of one sentence: list of dicts, in deterministic order, plus a
    per-clause status list."""
    by = {t["idx"]: t for t in tokens}
    ref_surface = tuple(t["form"] for t in tokens if not is_null(t))
    out, status = [], []
    seen = {ref_surface}
    for ctype, head in clause_heads(tokens):
        clause, reason = analyse_clause(tokens, head)
        if clause is None:
            status.append({"clause_type": ctype, "clause_head": head, "status": reason,
                           "n_units": 0, "n_free": 0, "n_variants": 0})
            continue
        if len(clause["free"]) <= ENUMERATE_UP_TO:
            orders = candidate_orders(clause, ref_id, seed)
        else:
            orders = sampled_orders(tokens, clause, ref_id, seed)
        n = 0
        ident = list(range(len(clause["units"])))
        for order in orders:
            if order == ident or not respects_holds(order, clause["holds"]):
                continue
            m = renumber(tokens, clause, order)
            new = sorted(tokens, key=lambda t: m[t["idx"]])
            surface = tuple(t["form"] for t in new if not is_null(t))
            if surface in seen:
                continue                                              # R8
            seen.add(surface)
            sa, sn, na = severity(tokens, m)
            seq = [clause["rels"][u] for u in order if clause["surface"][clause["units"][u]]] + ["V"]
            bigram_ok = None if attested is None else all(b in attested for b in zip(seq, seq[1:]))
            mk = [clause["markers"][clause["units"][u]] for u in order
                  if clause["surface"][clause["units"][u]]]
            case_adj = any(a and a == b for a, b in zip(mk, mk[1:]))
            out.append({"ref_id": ref_id, "clause_type": ctype, "clause_head": head,
                        "order": "|".join(map(str, order)), "n_units": len(order),
                        "n_free": len(clause["free"]), "kendall": kendall(order),
                        "adjacent_swap": adjacent_swap(order, clause["free"]),
                        "severity_abs": sa, "severity_net": sn, "n_arcs": na,
                        "bigram_ok": bigram_ok, "case_adjacent": case_adj,
                        "held_R3_R6": len(clause["fixed"]),
                        "holds": ";".join(f"{r}:{a}-{b}" for r, a, b in clause["holds"]),
                        "text": " ".join(surface)})
            n += 1
        status.append({"clause_type": ctype, "clause_head": head, "status": "ok",
                       "n_units": len(clause["units"]), "n_free": len(clause["free"]),
                       "n_variants": n})
    return out, status


def reference_bigrams(tokens):
    """Adjacent unit-relation bigrams of every analysable clause in a reference."""
    grams = set()
    for _, head in clause_heads(tokens):
        clause, _ = analyse_clause(tokens, head)
        if clause is None:
            continue
        seq = [r for r, u in zip(clause["rels"], clause["units"]) if clause["surface"][u]] + ["V"]
        grams.update(zip(seq, seq[1:]))
    return grams


# ----------------------------------------------------------------------------- reading HDTB
def read_conll_blocks(path):
    blocks = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        rows = [l.split("\t") for l in block.strip().split("\n") if l and not l.startswith("#")]
        rows = [r for r in rows if len(r) >= 8]
        if rows:
            blocks.append([{"idx": int(r[0]), "form": r[1], "lemma": r[2], "cpos": r[3],
                            "xpos": r[4], "feats": r[5], "head": int(r[6]), "deprel": r[7]}
                           for r in rows])
    return blocks


SSF_SENT = re.compile(r"<Sentence id=['\"]?([^'\">]+)['\"]?>(.*?)</Sentence>", re.S)


def read_ssf_sentences(path):
    out = []
    for m in SSF_SENT.finditer(path.read_text(encoding="utf-8")):
        words = [l.split("\t")[1] for l in m.group(2).split("\n")
                 if l.count("\t") >= 2 and l.split("\t")[1] not in ("((", "))")]
        out.append((m.group(1), " ".join(words)))
    return out


def assign_ids(blocks, ssf):
    """P1: SSF sentence id for each CoNLL block, by text within the document.
    Returns (ids, n_ambiguous); raises if any block has no match."""
    by_text = defaultdict(list)
    for sid, text in ssf:
        by_text[text].append(sid)
    used, ids, ambiguous = defaultdict(int), [], 0
    for b in blocks:
        text = " ".join(t["form"] for t in b)
        cands = by_text.get(text)
        if not cands or used[text] >= len(cands):
            raise ValueError(f"no SSF sentence for CoNLL block: {text[:60]}")
        if len(cands) > 1:
            ambiguous += 1
        ids.append(cands[used[text]])
        used[text] += 1
    # HDTB itself repeats an SSF id attribute for two different sentences in one document
    # (fullnews_id_2617899_date_23_7_2004, id 16). Later occurrences get "_2", "_3", ...
    seen = defaultdict(int)
    for i, sid in enumerate(ids):
        seen[sid] += 1
        if seen[sid] > 1:
            ids[i] = f"{sid}_{seen[sid]}"
    return ids, ambiguous
