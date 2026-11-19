# mi_screen_object_muril

_Step 4 agreement, stage screen, task object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 15:47 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 1.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage screen --task object --model muril --max-rows 256` |


- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 385
- **mean clean / corrupted metric (bits); total gap**: 7.652 / 1.691; 2312.83

| component | screened share of the gap | via special | via agree | via verb | via object | via subject | via ne | via other |
|---|---|---|---|---|---|---|---|---|
| L11MLP | 0.4345 | 0.0000 | 0.4345 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L10MLP | 0.3276 | -0.0000 | 0.3051 | 0.0176 | 0.0070 | 0.0001 | -0.0002 | -0.0020 |
| L10H6 | 0.2834 | -0.0000 | 0.2613 | 0.0161 | 0.0030 | 0.0002 | 0.0002 | 0.0026 |
| L8H3 | 0.2114 | -0.0002 | 0.1066 | 0.0835 | 0.0182 | 0.0002 | 0.0005 | 0.0026 |
| L8MLP | 0.1617 | -0.0003 | 0.0763 | 0.0397 | 0.0488 | -0.0014 | -0.0014 | 0.0002 |
| L9MLP | 0.1606 | -0.0001 | 0.0769 | 0.0176 | 0.0687 | 0.0013 | -0.0009 | -0.0030 |
| L11H1 | 0.1516 | 0.0000 | 0.1516 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L9H6 | 0.0789 | -0.0000 | 0.0615 | 0.0117 | 0.0052 | -0.0001 | 0.0001 | 0.0005 |
| L11H2 | 0.0587 | 0.0000 | 0.0587 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L9H1 | -0.0503 | 0.0000 | -0.0164 | -0.0120 | -0.0181 | -0.0003 | -0.0002 | -0.0033 |
| L9H3 | 0.0425 | 0.0000 | 0.0409 | 0.0017 | -0.0023 | 0.0002 | 0.0005 | 0.0015 |
| L10H10 | 0.0376 | 0.0000 | 0.0367 | 0.0008 | -0.0002 | -0.0000 | -0.0000 | 0.0004 |
| L10H3 | 0.0368 | 0.0000 | 0.0355 | 0.0010 | -0.0002 | -0.0000 | 0.0000 | 0.0004 |
| L2MLP | -0.0301 | -0.0025 | -0.0220 | -0.0018 | -0.0064 | 0.0005 | -0.0007 | 0.0028 |
| L9H8 | 0.0267 | -0.0001 | 0.0242 | 0.0031 | -0.0005 | 0.0001 | -0.0002 | 0.0001 |
| L11H10 | 0.0257 | 0.0000 | 0.0257 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L7MLP | 0.0247 | 0.0003 | 0.0121 | -0.0063 | 0.0177 | 0.0012 | 0.0008 | -0.0009 |
| L3MLP | 0.0244 | -0.0005 | -0.0135 | -0.0020 | 0.0392 | 0.0005 | 0.0005 | 0.0002 |
| L9H5 | 0.0237 | -0.0001 | 0.0031 | 0.0042 | 0.0157 | 0.0002 | -0.0001 | 0.0007 |
| L9H10 | 0.0181 | -0.0000 | 0.0040 | 0.0019 | 0.0119 | 0.0001 | -0.0001 | 0.0002 |

Shares are first-order estimates (attribution patching): the exact stage checks them.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_object_muril.npz` | 2,944,062 | `457413578c210356` | attribution per item x component x position class; clean and corrupted metrics |
