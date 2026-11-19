# Scripts

Analysis code for the two Hindi judgements (word order, agreement) in MuRIL and XLM-R-large. Every script that produces
results describes its design and checks in its docstring, and keeps a record in `course_runs/records/` (script hash,
command, library versions, output checksums).

## Scripts

| file | what it does | needs |
|---|---|---|
| `baseline_check.py` | the baseline checks (written order preferred, correct verb preferred, intervening subject), recomputed from `data/` | CPU, pandas |
| `mi_lib.py` | shared machinery: runs and pairs, hooks on head slices, MLP outputs, keys, values and embeddings; exact and attribution patching; mean-ablation; matched random sets; document-level statistics | imported |
| `mi_items.py` | word positions of every agreement order, the contrast pairs, the document split, and the 300 word-order pairs with alignment and sites; checks everything against the stored items | CPU, treebank |
| `mi_agreement.py` | agreement stages `metric`, `screen`, `exact`, `attention`, `path`, `validate` | GPU |
| `mi_decompose.py` | splits the whole-sentence agreement margin by word class on the contrast orders | GPU |
| `mi_wordorder.py` | word-order stages `screen`, `exact`, `sites`, `validate` | GPU |
| `mi_items_extra.py` | items for the follow-ups: 1,000 word-order pairs with reordering sizes and case-marker deletions | CPU, treebank |
| `mi_followup.py` | follow-ups `size`, `case_wordorder`, `case_agreement` | GPU |
| `mi_swap.py`, `mi_swap_compare.py` | step 4 repeated with the two document halves exchanged, and the comparison | GPU, CPU |
| `mi_items_paper.py` | items for the paper experiments: ko and bhi insertion, role swap, marker control matched in kind | CPU, treebank |
| `mi_paper_edit.py` | stages `ko`, `role_swap`, `kind` (ko-insertion, role swap, marker control matched in kind) | GPU |
| `mi_paper_mask.py` | stage `swap_mask`: masks one slot at a time in the role-swapped sentences | GPU |
| `mi_paper_sets.py` | stages `setsize` (head sets of 5 to 40 against matched random sets) and `mlpsets` (the top 5 MLPs against other 5-subsets) | GPU |
| `mi_paper_cues.py`, `mi_paper_cues_gap.py` | word-order preference by n-gram cue, and the circuit's effect given the gap | CPU |
| `mi_figures.py`, `mi_figures_followup.py` | figures from the outputs | CPU, matplotlib |
| `mi_paper_numbers.py` | recomputes the paper's Results numbers from `course_runs/outputs` and writes `paper_numbers.json` | CPU, numpy |
| `mi_figures_paper.py` | paper figures 1 to 4 (`paper/figures/`) | CPU, matplotlib |

## Running

The GPU stages ran on 11 GB cards: `--max-rows 256` for MuRIL, `--max-rows 128 --chunk 8` for XLM-R-large. The scripts
load the models from the Hugging Face Hub.

```bash
python3 scripts/mi_agreement.py --stage metric --model muril --max-rows 256
python3 scripts/mi_agreement.py --stage exact --task object --model muril --max-rows 256
python3 scripts/mi_wordorder.py --stage validate --model muril --max-rows 256
```

Order: build the items (`mi_items.py`, `mi_items_extra.py`, `mi_items_paper.py`); `metric` before every other agreement
stage; `screen`, then `exact`, then `attention` and `path`; then the validation stages, which read the held-out half once;
then the follow-ups and the paper experiments, which take their components from the exact stages.

Environment variables: `MI_OUT` (outputs, default `course_runs/outputs`), `MI_ITEMS` and `MI_ITEMS_EXTRA` (item folders),
`HUTB_RESULTS_DIR` (records, set to `course_runs/records`), `HUTB_BASE` and `HUTB_CORPUS` (the treebank, for the item
builders), `MI_ALLOW_CPU=1` (small CPU test runs only).

## Built-in checks

- every GPU stage checks that a head's columns, keys and values are that head's;
- unpatched runs reproduce the earlier scores or margins (about 1e-3 bits or better);
- patching the embedding output at every position recovers the whole gap;
- `metric` checks the span margin against an independent computation, and later agreement stages refuse to run until it has
  written its decision file;
- `validate` checks language-modelling cost against held-out text (a 2-nat limit).

Results land in `course_runs/outputs/` and records in `course_runs/records/` (`mi_<stage>[_<task>]_<model>.md`). A rerun
under an existing record tag overwrites that record.
