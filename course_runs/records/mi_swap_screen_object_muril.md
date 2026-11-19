# mi_swap_screen_object_muril

_Follow-up 3, halves swapped: screen, object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:17 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 1.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "object"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task object --stage screen` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 348
- **mean clean / corrupted metric (bits); total gap**: 6.026 / -1.364; 2593.99

| component | screened share of the gap | via special | via agree | via verb | via object | via subject | via ne | via other |
|---|---|---|---|---|---|---|---|---|
| L11MLP | 0.4339 | 0.0000 | 0.4339 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L10MLP | 0.3650 | 0.0000 | 0.3360 | 0.0233 | 0.0025 | -0.0001 | -0.0001 | 0.0033 |
| L10H6 | 0.2831 | 0.0000 | 0.2638 | 0.0143 | 0.0030 | 0.0003 | 0.0003 | 0.0015 |
| L8H3 | 0.2451 | -0.0002 | 0.1247 | 0.1010 | 0.0169 | 0.0004 | 0.0007 | 0.0016 |
| L8MLP | 0.2141 | -0.0001 | 0.0825 | 0.0646 | 0.0608 | -0.0003 | -0.0004 | 0.0071 |
| L11H1 | 0.1672 | 0.0000 | 0.1672 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L9MLP | 0.1591 | -0.0002 | 0.0734 | 0.0118 | 0.0751 | 0.0003 | 0.0002 | -0.0015 |
| L9H6 | 0.0814 | -0.0000 | 0.0611 | 0.0122 | 0.0078 | 0.0000 | 0.0001 | 0.0001 |
| L11H2 | 0.0647 | 0.0000 | 0.0647 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L3MLP | 0.0641 | 0.0002 | 0.0003 | -0.0000 | 0.0644 | 0.0037 | -0.0002 | -0.0042 |
| L9H1 | -0.0594 | -0.0000 | -0.0197 | -0.0141 | -0.0221 | 0.0001 | -0.0003 | -0.0033 |
| L6MLP | 0.0533 | -0.0004 | 0.0034 | -0.0014 | 0.0459 | 0.0001 | -0.0012 | 0.0068 |
| L9H3 | 0.0441 | -0.0000 | 0.0453 | 0.0020 | -0.0034 | 0.0002 | 0.0007 | -0.0008 |
| L10H10 | 0.0374 | 0.0000 | 0.0357 | 0.0013 | 0.0003 | 0.0000 | -0.0000 | 0.0001 |
| L2MLP | 0.0346 | -0.0006 | -0.0052 | -0.0036 | 0.0406 | 0.0023 | -0.0009 | 0.0020 |
| L9H5 | 0.0316 | -0.0001 | 0.0042 | 0.0061 | 0.0209 | 0.0000 | -0.0000 | 0.0004 |
| L9H8 | 0.0286 | -0.0001 | 0.0245 | 0.0040 | -0.0001 | -0.0000 | -0.0001 | 0.0003 |
| L11H10 | 0.0261 | 0.0000 | 0.0261 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L8H1 | -0.0252 | 0.0001 | -0.0004 | -0.0108 | -0.0085 | -0.0006 | -0.0009 | -0.0042 |
| L10H3 | 0.0242 | 0.0000 | 0.0237 | 0.0004 | 0.0001 | -0.0000 | -0.0000 | -0.0000 |

Shares are first-order estimates (attribution patching): the exact stage checks them.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_object_muril.npz` | 2,670,003 | `cb55e955ee6214ea` | attribution per item x component x position class; clean and corrupted metrics |
