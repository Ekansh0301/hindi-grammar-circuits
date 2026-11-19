# mi_screen_object_xlmrlarge

_Step 4 agreement, stage screen, task object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 15:48 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 2.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage screen --task object --model xlmrlarge --max-rows 128 --chunk 8` |


- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 387
- **mean clean / corrupted metric (bits); total gap**: 7.506 / 2.053; 2115.98

| component | screened share of the gap | via special | via agree | via verb | via object | via subject | via ne | via other |
|---|---|---|---|---|---|---|---|---|
| L21MLP | 0.3651 | 0.0002 | 0.3491 | 0.0046 | 0.0052 | 0.0008 | -0.0003 | 0.0055 |
| L21H0 | 0.2672 | 0.0000 | 0.2621 | 0.0030 | 0.0008 | 0.0000 | 0.0007 | 0.0007 |
| L20H0 | 0.2499 | -0.0000 | 0.2364 | 0.0099 | 0.0031 | 0.0001 | 0.0001 | 0.0003 |
| L20MLP | 0.2188 | 0.0002 | 0.1627 | 0.0244 | 0.0271 | 0.0007 | 0.0008 | 0.0029 |
| L22MLP | 0.1337 | -0.0004 | 0.1398 | -0.0025 | 0.0021 | -0.0020 | 0.0011 | -0.0044 |
| L20H2 | 0.1051 | -0.0001 | 0.0949 | 0.0089 | 0.0021 | -0.0002 | -0.0000 | -0.0004 |
| L19MLP | 0.0990 | 0.0003 | 0.0318 | 0.0150 | 0.0602 | 0.0009 | 0.0005 | -0.0099 |
| L23MLP | 0.0812 | 0.0000 | 0.0812 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L22H6 | 0.0764 | 0.0001 | 0.0759 | 0.0002 | 0.0002 | -0.0001 | 0.0000 | 0.0000 |
| L19H3 | 0.0512 | 0.0002 | 0.0283 | 0.0099 | 0.0133 | -0.0000 | -0.0001 | -0.0004 |
| L17MLP | 0.0490 | 0.0001 | 0.0007 | -0.0037 | 0.0515 | 0.0041 | 0.0000 | -0.0038 |
| L21H4 | -0.0443 | -0.0000 | -0.0319 | -0.0048 | -0.0028 | -0.0001 | -0.0010 | -0.0036 |
| L7MLP | 0.0398 | 0.0064 | 0.0000 | -0.0006 | 0.0303 | 0.0030 | -0.0029 | 0.0037 |
| L11MLP | 0.0303 | 0.0003 | -0.0009 | -0.0012 | 0.0367 | -0.0015 | -0.0031 | -0.0001 |
| L10H7 | 0.0217 | 0.0004 | 0.0009 | -0.0156 | 0.0002 | -0.0155 | 0.0197 | 0.0316 |
| L0H7 | 0.0208 | 0.0002 | -0.0003 | -0.0002 | 0.0169 | 0.0001 | 0.0000 | 0.0040 |
| L1MLP | 0.0205 | 0.0028 | 0.0012 | -0.0001 | 0.0079 | 0.0039 | 0.0041 | 0.0007 |
| L9MLP | 0.0192 | 0.0083 | -0.0030 | -0.0003 | 0.0213 | -0.0028 | 0.0024 | -0.0068 |
| L5MLP | 0.0176 | 0.0026 | 0.0031 | -0.0001 | 0.0067 | 0.0070 | 0.0002 | -0.0019 |
| L10H3 | -0.0158 | -0.0002 | 0.0025 | -0.0009 | -0.0091 | 0.0000 | -0.0010 | -0.0071 |

Shares are first-order estimates (attribution patching): the exact stage checks them.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_object_xlmrlarge.npz` | 7,950,553 | `a254e18167143f56` | attribution per item x component x position class; clean and corrupted metrics |
