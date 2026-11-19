#!/usr/bin/env python3
"""Write Set 1 variant trees for the variants a stage needs (SET1_CONSTRUCTION_PLAN.md, P3).

Reads reference_trees.conllu and variants.tsv.gz from HUTB_CORPUS, re-derives each listed
variant's tree from its reference and its stored unit order, checks that the tree's words
equal the stored text, and writes/extends variant_trees.conllu in the 5-column format the
pipeline reads (id, form, xpos, head, deprel). Existing entries are kept, so several pair
lists can be materialised into the same file.
"""
import argparse
import csv
import gzip
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

import set1_generator as G
from hutb_corpus import FC, parse_conllu
from runlog import RunLog


def official_tokens(rows):
    """Reference rows as written by build_set1.py, back to generator tokens (coarse category
    restored from the `cat-` feature)."""
    out = []
    for r in rows:
        feats = r[5]
        cat = G.feats_dict({"feats": feats}).get("cat", "")
        out.append({"idx": int(r[0]), "form": r[1], "lemma": r[2], "cpos": cat, "xpos": r[4],
                    "feats": feats, "head": int(r[6]), "deprel": "main" if r[7] == "root" else r[7]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pairs", nargs="+", required=True, help="CSV files with a var_id column")
    ap.add_argument("--tag", default="materialise_set1")
    args = ap.parse_args()

    with RunLog(args.tag, __file__, args,
                purpose="Write Set 1 variant trees for the listed variants, checking each against "
                        "its stored text.") as log:
        want = set()
        for p in args.pairs:
            want |= set(pd.read_csv(p).var_id)
        target = FC / "variant_trees.conllu"
        have = set(parse_conllu(target, 5)) if target.exists() else set()
        todo = want - have
        log.kv("variants requested / already written / to write", f"{len(want):,} / {len(want & have):,} / {len(todo):,}")
        refs = parse_conllu(FC / "reference_trees.conllu", 8)
        written = 0
        with gzip.open(FC / "variants.tsv.gz", "rt", encoding="utf-8") as fh, \
                open(target, "a", encoding="utf-8") as out:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["var_id"] not in todo:
                    continue
                toks = official_tokens(refs[r["ref_id"]])
                clause, reason = G.analyse_clause(toks, int(r["clause_head"]))
                if clause is None:
                    raise SystemExit(f"{r['var_id']}: clause no longer analysable ({reason})")
                vt = G.variant_tokens(toks, clause, list(map(int, r["order"].split("|"))))
                text = " ".join(t["form"] for t in vt if not G.is_null(t))
                if text != r["text"]:
                    raise SystemExit(f"{r['var_id']}: tree text differs from stored text")
                out.write(f"# sent_id = {r['var_id']}\n")
                for t in vt:
                    out.write("\t".join([str(t["idx"]), t["form"], t["xpos"], str(t["head"]),
                                         "root" if t["head"] == 0 else t["deprel"]]) + "\n")
                out.write("\n")
                written += 1
        log.kv("written", f"{written:,}")
        if written != len(todo):
            raise SystemExit(f"{len(todo) - written} requested variants not found in variants.tsv.gz")
        log.output(target, "Set 1 variant trees (cumulative)")


if __name__ == "__main__":
    main()
