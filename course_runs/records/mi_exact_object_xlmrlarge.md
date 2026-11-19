# mi_exact_object_xlmrlarge

_Step 4 agreement, stage exact, task object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 16:27 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 38.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage exact --task object --model xlmrlarge --max-rows 128 --chunk 8` |


- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: embedding output patched everywhere, ratio of sums / worst item (bits)**: 1.000000 / 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 387

| component | share of the gap restored | document bootstrap 95% | at special only | at agree only | at verb only | at object only | at subject only | at ne only | at other only |
|---|---|---|---|---|---|---|---|---|---|
| L21MLP | 0.3685 | [0.325, 0.428] | 0.0002 | 0.3558 | 0.0050 | 0.0060 | -0.0000 | -0.0009 | 0.0040 |
| L21H0 | 0.2878 | [0.249, 0.340] | 0.0000 | 0.2826 | 0.0029 | 0.0009 | 0.0000 | 0.0007 | 0.0007 |
| L20H0 | 0.2498 | [0.212, 0.295] | -0.0000 | 0.2354 | 0.0105 | 0.0034 | 0.0001 | 0.0001 | 0.0003 |
| L20MLP | 0.2237 | [0.190, 0.262] | 0.0002 | 0.1641 | 0.0234 | 0.0234 | -0.0009 | 0.0004 | -0.0031 |
| L22MLP | 0.1315 | [0.088, 0.183] | -0.0003 | 0.1370 | -0.0026 | 0.0019 | -0.0011 | 0.0007 | -0.0024 |
| L20H2 | 0.1086 | [0.088, 0.136] | -0.0001 | 0.0976 | 0.0083 | 0.0022 | -0.0002 | 0.0000 | -0.0004 |
| L19MLP | 0.0882 | [0.054, 0.125] | 0.0004 | 0.0340 | 0.0125 | 0.0483 | 0.0004 | -0.0004 | -0.0102 |
| L23MLP | 0.0795 | [0.048, 0.115] | -0.0000 | 0.0795 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L22H6 | 0.0771 | [0.063, 0.092] | 0.0001 | 0.0767 | 0.0002 | 0.0002 | -0.0001 | 0.0000 | 0.0000 |
| L19H3 | 0.0599 | [0.045, 0.074] | 0.0002 | 0.0325 | 0.0105 | 0.0156 | -0.0000 | -0.0001 | -0.0004 |
| L17MLP | 0.0443 | [0.020, 0.064] | 0.0000 | -0.0001 | -0.0065 | 0.0535 | 0.0034 | -0.0010 | -0.0053 |
| L10MLP | 0.0368 | [0.004, 0.061] | -0.0001 | -0.0049 | 0.0042 | 0.0273 | 0.0025 | -0.0005 | 0.0048 |
| L9MLP | 0.0275 | [0.003, 0.051] | 0.0032 | -0.0041 | -0.0011 | 0.0171 | -0.0001 | 0.0011 | 0.0074 |
| L7MLP | 0.0245 | [0.007, 0.043] | 0.0032 | -0.0033 | -0.0005 | 0.0301 | -0.0021 | -0.0017 | -0.0011 |
| L23H15 | 0.0152 | [0.003, 0.030] | -0.0000 | 0.0152 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L11MLP | 0.0143 | [-0.007, 0.035] | 0.0002 | -0.0010 | -0.0003 | 0.0386 | -0.0029 | -0.0042 | -0.0109 |
| L5MLP | 0.0137 | [0.003, 0.026] | 0.0020 | 0.0013 | 0.0001 | 0.0129 | 0.0006 | 0.0002 | -0.0011 |
| L12H6 | 0.0115 | [0.002, 0.021] | 0.0001 | 0.0003 | -0.0002 | 0.0119 | -0.0001 | -0.0000 | -0.0003 |
| L23H7 | 0.0107 | [0.005, 0.017] | -0.0000 | 0.0107 | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| L17H7 | 0.0094 | [-0.008, 0.028] | -0.0007 | 0.0049 | -0.0017 | 0.0064 | 0.0001 | -0.0004 | 0.0000 |


| top K patched jointly | share restored |
|---|---|
| 1 | 0.3685 |
| 2 | 0.5401 |
| 5 | 0.8286 |
| 10 | 0.9360 |
| 20 | 0.9293 |

- **screen against exact: Spearman over components / top-20 overlap**: 0.802 / 16 of 20
- **screen input**: screen_object_xlmrlarge.npz (sha256 a254e18167143f56)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_object_xlmrlarge.npz` | 810,350 | `ca14575fa4257472` | exact patching: every component alone; the top 20 per position class; the top K jointly |
