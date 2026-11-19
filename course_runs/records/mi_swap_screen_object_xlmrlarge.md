# mi_swap_screen_object_xlmrlarge

_Follow-up 3, halves swapped: screen, object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:29 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 1.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "object"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task object --stage screen` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 351
- **mean clean / corrupted metric (bits); total gap**: 5.196 / -0.144; 1874.08

| component | screened share of the gap | via special | via agree | via verb | via object | via subject | via ne | via other |
|---|---|---|---|---|---|---|---|---|
| L20H0 | 0.3358 | -0.0000 | 0.3180 | 0.0151 | 0.0034 | -0.0000 | -0.0004 | -0.0002 |
| L21MLP | 0.3269 | 0.0003 | 0.3244 | 0.0021 | 0.0001 | -0.0001 | -0.0005 | 0.0006 |
| L21H0 | 0.2882 | 0.0000 | 0.2826 | 0.0035 | 0.0008 | -0.0000 | 0.0007 | 0.0006 |
| L20MLP | 0.2238 | 0.0000 | 0.2021 | 0.0218 | -0.0013 | 0.0002 | -0.0009 | 0.0019 |
| L20H2 | 0.1392 | 0.0000 | 0.1310 | 0.0088 | -0.0000 | -0.0000 | -0.0003 | -0.0003 |
| L22MLP | 0.1265 | 0.0012 | 0.1346 | -0.0011 | -0.0005 | -0.0002 | -0.0008 | -0.0067 |
| L23MLP | 0.1207 | 0.0000 | 0.1207 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L19MLP | 0.0809 | 0.0004 | 0.0068 | 0.0233 | 0.0490 | -0.0001 | 0.0003 | 0.0011 |
| L22H6 | 0.0724 | 0.0001 | 0.0720 | 0.0004 | -0.0001 | 0.0000 | 0.0000 | -0.0000 |
| L19H3 | 0.0678 | 0.0001 | 0.0411 | 0.0101 | 0.0167 | 0.0002 | 0.0001 | -0.0004 |
| L10H7 | -0.0658 | 0.0002 | 0.0017 | 0.0091 | 0.0022 | 0.0037 | -0.0057 | -0.0771 |
| L17MLP | 0.0340 | -0.0001 | -0.0044 | 0.0008 | 0.0476 | 0.0019 | -0.0010 | -0.0107 |
| L21H4 | -0.0323 | 0.0001 | -0.0280 | -0.0030 | -0.0011 | -0.0000 | -0.0000 | -0.0003 |
| L10H9 | 0.0199 | -0.0002 | 0.0047 | 0.0009 | 0.0072 | 0.0005 | -0.0001 | 0.0070 |
| L20H8 | -0.0192 | 0.0003 | -0.0025 | -0.0068 | -0.0073 | -0.0001 | 0.0005 | -0.0032 |
| L9H1 | -0.0187 | 0.0004 | -0.0002 | 0.0011 | -0.0003 | 0.0012 | -0.0003 | -0.0206 |
| L10H15 | 0.0186 | -0.0000 | 0.0164 | 0.0006 | 0.0006 | -0.0004 | 0.0000 | 0.0014 |
| L15MLP | 0.0185 | 0.0003 | -0.0027 | 0.0010 | 0.0279 | -0.0012 | 0.0001 | -0.0069 |
| L9H7 | 0.0182 | 0.0012 | -0.0012 | -0.0006 | 0.0018 | -0.0011 | 0.0007 | 0.0174 |
| L12MLP | -0.0172 | 0.0002 | 0.0034 | -0.0038 | -0.0062 | -0.0003 | -0.0010 | -0.0094 |

Shares are first-order estimates (attribution patching): the exact stage checks them.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_object_xlmrlarge.npz` | 7,209,643 | `30b5d1246a2b36d3` | attribution per item x component x position class; clean and corrupted metrics |
