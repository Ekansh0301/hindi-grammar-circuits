#!/usr/bin/env python3
"""
Shared corpus access for the HUTB filtered corpus: one parser, one text
builder, one id convention, imported by every experiment script so the
scorer, the sampler and the feature builders cannot silently disagree about
what a sentence is.

TWO FILE FORMATS. reference_trees.conllu is 10-column CoNLL
(id, form, lemma, cpos, xpos, feats, head, deprel, _, _); variant_trees.conllu
is 5-column (id, form, xpos, head, deprel). An earlier version of the variant
parser assumed the reference layout and discarded the POS column.

NULL TOKENS ARE DROPPED FROM SURFACE TEXT. NULL marks an elided element in
the annotation -- a speaker never utters it, so feeding it to a language
model was a real contamination bug (~7% of variants affected). It is kept in
the token list, because the dependency structure refers to it, and removed
only from the string handed to a model.
"""
import os
from pathlib import Path

BASE = Path(os.environ.get("HUTB_BASE", "/home/ekansh-the-great/Music/HUTB"))
FC = Path(os.environ.get("HUTB_CORPUS", BASE / "HUTB_Filtered_Corpus"))


def is_null_form(form):
    """HDTB's placeholder for an elided element. Written `NULL` 2,124 times and `null` 17 times
    in HDTB v0.05, so the test is case-insensitive (an exact `== "NULL"` fed `null` to the
    language models in 18 shipped reference lines and 21 variant lines)."""
    return form.strip().upper() == "NULL"


def is_set1():
    """True when HUTB_CORPUS is a Set 1 corpus (built by build_set1.py). Set 1 trees are
    correct by construction, so there is no repaired file and no repair status."""
    return (FC / "set1_manifest.json").exists()


def set1_variants():
    """Every Set 1 variant with its order, severity, filter flags and text."""
    import pandas as _pd
    return _pd.read_csv(FC / "variants.tsv.gz", sep="\t", keep_default_na=False,
                        dtype={"var_id": str, "ref_id": str, "holds": str})

REF_COLS = {"idx": 0, "form": 1, "lemma": 2, "cpos": 3, "xpos": 4,
            "feats": 5, "head": 6, "deprel": 7}
VAR_COLS = {"idx": 0, "form": 1, "xpos": 2, "head": 3, "deprel": 4}


def _token_row(line, ncols_min, path, lineno):
    """A token line split into columns. A line narrower than `ncols_min` aborts: reading the 5-column
    variant file at the reference width used to skip every row silently, which left every variant
    empty and once produced a figure reporting 100% tokenisation contamination."""
    parts = line.split("\t")
    if len(parts) < ncols_min:
        raise ValueError(f"{path}:{lineno}: token line has {len(parts)} columns, fewer than the {ncols_min} "
                         "asked for. variant_trees.conllu is 5-column and reference_trees.conllu 10-column: "
                         "is this file being read at the other one's width?")
    return parts


def parse_conllu(path, ncols_min):
    sents, cur_id, cur = {}, None, []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if line.startswith("# sent_id"):
                if cur_id is not None:
                    sents[cur_id] = cur
                cur_id, cur = line.split("=", 1)[1].strip(), []
                continue
            if not line.strip() or line.startswith("#"):
                continue
            cur.append(_token_row(line, ncols_min, path, lineno))
        if cur_id is not None:
            sents[cur_id] = cur
    return sents


def iter_conllu(path, ncols_min):
    """Stream (sent_id, rows) instead of building a dict of the whole file.

    variant_trees.conllu holds 382k sentences; holding two or three copies of
    it in memory at once is what makes a 15 GB machine start swapping, and the
    OOM killer takes whichever job is largest -- not necessarily this one. Use
    this whenever a pass only needs one sentence at a time.
    """
    cur_id, cur = None, []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if line.startswith("# sent_id"):
                if cur_id is not None:
                    yield cur_id, cur
                cur_id, cur = line.split("=", 1)[1].strip(), []
                continue
            if not line.strip() or line.startswith("#"):
                continue
            cur.append(_token_row(line, ncols_min, path, lineno))
    if cur_id is not None:
        yield cur_id, cur


def load_trees(repaired=True):
    """Reference and variant trees.

    `repaired=True` (the default) uses variant_trees_repaired.conllu. The
    shipped variant_trees.conllu silently reattaches to the root every arc
    whose head token the generator's surface alignment failed to match: 90.5%
    of variant trees are affected and they carry on average 3 arcs fewer than
    the reference they permute. See Results/rq1_variant_tree_repair.md. Pass
    repaired=False only to reproduce a pre-repair result deliberately.
    """
    if is_set1():
        var = FC / "variant_trees.conllu"
        if not var.exists():
            raise FileNotFoundError(f"{var} missing: run scripts/materialise_set1.py for the pairs this stage needs")
        return (parse_conllu(FC / "reference_trees.conllu", 8), parse_conllu(var, 5))
    var = FC / ("variant_trees_repaired.conllu" if repaired else "variant_trees.conllu")
    if repaired and not var.exists():
        raise FileNotFoundError(
            f"{var} missing — run scripts/repair_variant_trees.py first")
    return (parse_conllu(FC / "reference_trees.conllu", 8), parse_conllu(var, 5))


def clean_variant_ids():
    """Variant ids whose repaired tree is guaranteed correct (the alignment was
    forced at every step). Synthetic recovery is 99.44% on these against 52.63%
    where a tie occurred, so the flag is doing real work, not decoration."""
    import pandas as _pd
    if is_set1():
        return set(set1_variants().var_id)
    st = _pd.read_csv(BASE / "Results_Checks" / "variant_repair_status.csv")
    return set(st[st.repair_status == "clean"].var_id)


def tokens_of(rows, is_ref):
    """Token dicts of one sentence's rows. A row that cannot be read at the layout `is_ref` names
    raises: it used to be skipped, so variant rows passed as a reference (is_ref=True) came back as
    an empty sentence. No row of the reference or variant files has a non-integer id or head."""
    cols = REF_COLS if is_ref else VAR_COLS
    out = []
    for r in rows:
        try:
            out.append({
                "idx": int(r[cols["idx"]]),
                "form": r[cols["form"]],
                "xpos": r[cols["xpos"]],
                "head": int(r[cols["head"]]),
                "deprel": r[cols["deprel"]],
                "lemma": r[cols["lemma"]] if is_ref else r[cols["form"]],
                # References carry both a coarse and a fine POS column; the
                # canonical word-order detector reads the COARSE one, so it is
                # exposed separately rather than collapsed into xpos. Variants
                # have one POS column, which serves as both.
                "cpos": r[cols["cpos"]] if is_ref else r[cols["xpos"]],
            })
        except (ValueError, IndexError) as e:
            raise ValueError(f"row {r!r} does not read as a {'reference (10-column)' if is_ref else 'variant (5-column)'} "
                             f"token ({type(e).__name__}: {e}); is is_ref right for these rows?") from e
    return out


def text_of(rows, is_ref=True):
    """Surface string, NULL placeholders removed (see module docstring)."""
    cols = REF_COLS if is_ref else VAR_COLS
    return " ".join(r[cols["form"]] for r in rows
                    if len(r) > cols["form"] and not is_null_form(r[cols["form"]]))


def base_ref_id(sent_id):
    """'doc__11.3' -> 'doc__11.0', the reference a variant was derived from."""
    if "__" not in sent_id:
        return None
    prefix, rhs = sent_id.split("__", 1)
    return f"{prefix}__{rhs.split('.', 1)[0]}.0"


def variants_by_reference(vars_, refs, keep=None):
    """reference id -> [variant ids], optionally restricted to `keep`."""
    by_ref = {}
    for vid in vars_:
        rid = base_ref_id(vid)
        if rid is None or rid not in refs:
            continue
        if keep is not None and rid not in keep:
            continue
        by_ref.setdefault(rid, []).append(vid)
    for r in by_ref:
        by_ref[r].sort()
    return by_ref


def base_deprel(d):
    d = (d or "").split("__")[0]
    for pre in ("ras-", "ras_"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d.split("-")[0]
