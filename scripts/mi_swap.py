#!/usr/bin/env python3
"""Follow-up experiment 3 (docs/FOLLOWUP_EXPERIMENTS.md): step 4 with the two halves swapped. GPU, per model and
task. Declared before any run (27 Oct 2026).

QUESTION. Step 4 chose its components on the selection half and read the held-out half once. Are the circuits an
accident of which documents fell where? Here the roles are exchanged: components are chosen on the held-out half
(screen, exact) and validated, once, on the selection half (validate). Nothing else changes: the stage functions are
mi_agreement's and mi_wordorder's, called unchanged, with their `half` argument set to the other half; the metric,
the items, the random-set seeds, the language-modelling check and every threshold are as in step 4.
WHAT IS DIFFERENT. The selection-half documents were read many times in step 4 (screens, exact stages, path,
attention). Here they are the validation half, so their read is no longer 'once'; what is read once is the
validation of THESE circuits, which were chosen without them. The held-out half, which step 4 read once, is now read
by the screen and the exact stage. State both in any use.
TASKS AND STAGES: --task object (agreement, the object corruption) or wordorder; --stage screen, exact, validate.
Outputs go to outputs/swap/ and records to mi_swap_<stage>_<task>_<model>.md; step 4's files are never written. The
metric decision and override are read from step 4's (copied into outputs/swap/ at the start).
Not repeated: path patching, attention and the site stage (descriptive stages that choose nothing the validation
needs). mi_swap_compare.py reads both directions and compares them.
"""
import argparse
import shutil
import sys
from pathlib import Path

import pandas as pd
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import mi_agreement as A  # noqa: E402
import mi_lib as M  # noqa: E402
import mi_wordorder as W  # noqa: E402
from runlog import RunLog  # noqa: E402

SENT = str(M.ROOT / "data" / "heldout_text" / "readability_sentences.txt")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--task", required=True, choices=["object", "wordorder"])
    ap.add_argument("--stage", required=True, choices=["screen", "exact", "validate"])
    ap.add_argument("--model", required=True, choices=list(M.MODELS))
    ap.add_argument("--limit", type=int, default=None, help="first N items only (smoke tests)")
    ap.add_argument("--min-gap", type=float, default=0.05)
    ap.add_argument("--chunk", type=int, default=16)
    ap.add_argument("--max-rows", type=int, default=256)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--k-mlp", type=int, default=5)
    ap.add_argument("--n-random", type=int, default=100)
    ap.add_argument("--n-mean", type=int, default=300)
    ap.add_argument("--n-read", type=int, default=100)
    ap.add_argument("--sentences", default=SENT)
    ap.add_argument("--record-tag", default=None)
    args = ap.parse_args()
    if not torch.cuda.is_available() and M.os.environ.get("MI_ALLOW_CPU") != "1":
        raise SystemExit("no GPU visible; refusing to run on the CPU")
    # the roles: screen and exact read the held-out half, validate reads the selection half
    args.half = "selection" if args.stage == "validate" else "heldout"
    args.batch_size = M.MODELS[args.model][1]
    step4_out = M.OUT
    swap_out = M.OUT / "swap"
    swap_out.mkdir(parents=True, exist_ok=True)
    for ext in ("decision", "override"):
        f = step4_out / f"metric_{args.model}.{ext}"
        if f.exists():
            shutil.copy(f, swap_out / f.name)
    M.OUT = swap_out
    tag = args.record_tag or f"mi_swap_{args.stage}_{args.task}_{args.model}"
    if args.task == "object":
        status = A.require_metric(args)
    with RunLog(tag, __file__, args, purpose=f"Follow-up 3, halves swapped: {args.stage}, {args.task}, {args.model}.") as log:
        log.kv("roles", "components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)")
        log.kv("half this stage reads", args.half)
        log.p("Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean "
              "the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are "
              "validated on, here the selection half.")
        if args.task == "object":
            log.kv("metric", status)
        model, tok = M.load(args.model)
        sess = M.Session(model)
        try:
            text = A.read_positions().correct.iloc[0] if args.task == "object" else \
                pd.read_csv(M.ITEMS / "wordorder_pairs.csv").ref_text.iloc[0]
            lay = M.check_head_layout(sess, tok, text)
            log.kv("check: head layout (attention x value slice h against attention input slice h), worst (abs)", f"{lay:.2e}")
            if lay > 1e-3:
                raise SystemExit("column block h is not head h: the head slices are wrong for this model")
            if args.task == "object":
                {"screen": A.stage_screen, "exact": A.stage_exact, "validate": A.stage_validate}[args.stage](args, log, model, tok, sess)
            else:
                {"screen": W.stage_screen, "exact": W.stage_exact, "validate": W.stage_validate}[args.stage](args, log, sess, tok)
        finally:
            sess.close()


if __name__ == "__main__":
    main()
