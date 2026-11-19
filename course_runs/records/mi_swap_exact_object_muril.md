# mi_swap_exact_object_muril

_Follow-up 3, halves swapped: exact, object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:22 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 4.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "object"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task object --stage exact` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: embedding output patched everywhere, ratio of sums / worst item (bits)**: 1.000000 / 0.00e+00
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 348

| component | share of the gap restored | document bootstrap 95% | at special only | at agree only | at verb only | at object only | at subject only | at ne only | at other only |
|---|---|---|---|---|---|---|---|---|---|
| L11MLP | 0.4629 | [0.427, 0.500] | -0.0000 | 0.4629 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L8H3 | 0.3790 | [0.308, 0.448] | -0.0002 | 0.2228 | 0.1278 | 0.0230 | 0.0004 | 0.0007 | 0.0021 |
| L10MLP | 0.3690 | [0.334, 0.404] | 0.0000 | 0.3433 | 0.0230 | 0.0019 | -0.0002 | -0.0000 | 0.0030 |
| L10H6 | 0.3101 | [0.279, 0.341] | 0.0000 | 0.2909 | 0.0148 | 0.0033 | 0.0003 | 0.0003 | 0.0018 |
| L8MLP | 0.2698 | [0.212, 0.327] | -0.0001 | 0.1108 | 0.0879 | 0.0586 | -0.0001 | -0.0003 | 0.0079 |
| L9MLP | 0.1613 | [0.126, 0.198] | -0.0002 | 0.0790 | 0.0123 | 0.0554 | 0.0005 | 0.0002 | -0.0020 |
| L11H1 | 0.1522 | [0.138, 0.167] | -0.0000 | 0.1522 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L0MLP | 0.0996 | [0.052, 0.153] | 0.0010 | -0.0049 | -0.0043 | 0.1233 | -0.0003 | -0.0006 | -0.0039 |
| L9H6 | 0.0884 | [0.076, 0.100] | -0.0000 | 0.0661 | 0.0128 | 0.0079 | 0.0001 | 0.0001 | 0.0004 |
| L3MLP | 0.0775 | [0.046, 0.112] | 0.0001 | -0.0056 | 0.0010 | 0.0871 | 0.0027 | -0.0003 | -0.0041 |
| L11H2 | 0.0651 | [0.057, 0.073] | -0.0000 | 0.0651 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L6MLP | 0.0641 | [0.035, 0.094] | -0.0003 | 0.0001 | -0.0012 | 0.0631 | 0.0000 | -0.0029 | 0.0074 |
| L9H3 | 0.0458 | [0.036, 0.056] | -0.0000 | 0.0463 | 0.0021 | -0.0037 | 0.0002 | 0.0007 | -0.0007 |
| L2MLP | 0.0398 | [0.009, 0.069] | -0.0008 | -0.0032 | -0.0039 | 0.0368 | 0.0014 | -0.0011 | 0.0024 |
| L10H10 | 0.0377 | [0.029, 0.048] | 0.0000 | 0.0359 | 0.0014 | 0.0003 | 0.0000 | -0.0001 | 0.0000 |
| L1H3 | 0.0350 | [0.017, 0.059] | 0.0000 | -0.0001 | 0.0001 | 0.0319 | 0.0000 | -0.0001 | 0.0017 |
| L9H8 | 0.0350 | [0.024, 0.046] | -0.0001 | 0.0285 | 0.0048 | 0.0014 | 0.0000 | -0.0000 | 0.0005 |
| L1MLP | 0.0345 | [0.007, 0.062] | -0.0004 | -0.0074 | -0.0031 | 0.0372 | -0.0001 | -0.0006 | 0.0010 |
| L9H5 | 0.0311 | [0.021, 0.042] | -0.0001 | 0.0042 | 0.0059 | 0.0206 | 0.0000 | -0.0000 | 0.0005 |
| L7MLP | 0.0282 | [-0.000, 0.056] | -0.0001 | -0.0073 | -0.0114 | 0.0430 | 0.0002 | -0.0017 | 0.0016 |


| top K patched jointly | share restored |
|---|---|
| 1 | 0.4629 |
| 2 | 0.6554 |
| 5 | 0.8788 |
| 10 | 0.9417 |
| 20 | 0.9702 |

- **screen against exact: Spearman over components / top-20 overlap**: 0.922 / 18 of 20
- **screen input**: screen_object_muril.npz (sha256 cb55e955ee6214ea)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_object_muril.npz` | 416,975 | `0873b5d3176cf284` | exact patching: every component alone; the top 20 per position class; the top K jointly |
