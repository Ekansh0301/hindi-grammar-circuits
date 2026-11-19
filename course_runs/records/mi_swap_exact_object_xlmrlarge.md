# mi_swap_exact_object_xlmrlarge

_Follow-up 3, halves swapped: exact, object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:51 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 21.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "object"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task object --stage exact` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: embedding output patched everywhere, ratio of sums / worst item (bits)**: 1.000000 / 0.00e+00
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 351

| component | share of the gap restored | document bootstrap 95% | at special only | at agree only | at verb only | at object only | at subject only | at ne only | at other only |
|---|---|---|---|---|---|---|---|---|---|
| L21MLP | 0.3412 | [0.293, 0.390] | 0.0003 | 0.3408 | 0.0020 | 0.0002 | -0.0006 | -0.0007 | -0.0023 |
| L20H0 | 0.3086 | [0.251, 0.371] | -0.0000 | 0.2918 | 0.0156 | 0.0035 | -0.0000 | -0.0004 | -0.0003 |
| L21H0 | 0.3024 | [0.269, 0.344] | 0.0000 | 0.2967 | 0.0034 | 0.0012 | -0.0000 | 0.0007 | 0.0006 |
| L20MLP | 0.2162 | [0.178, 0.250] | 0.0000 | 0.1876 | 0.0216 | -0.0047 | 0.0000 | -0.0011 | -0.0043 |
| L20H2 | 0.1388 | [0.113, 0.167] | 0.0000 | 0.1298 | 0.0087 | -0.0002 | -0.0000 | -0.0003 | -0.0003 |
| L22MLP | 0.1283 | [0.079, 0.180] | 0.0012 | 0.1352 | -0.0012 | -0.0009 | -0.0001 | -0.0007 | -0.0050 |
| L23MLP | 0.1199 | [0.086, 0.160] | 0.0000 | 0.1199 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L19H3 | 0.0759 | [0.059, 0.094] | 0.0001 | 0.0452 | 0.0111 | 0.0192 | 0.0002 | 0.0001 | -0.0005 |
| L22H6 | 0.0742 | [0.055, 0.097] | 0.0001 | 0.0737 | 0.0004 | -0.0001 | 0.0000 | 0.0000 | -0.0000 |
| L19MLP | 0.0616 | [0.013, 0.097] | 0.0005 | 0.0052 | 0.0231 | 0.0360 | -0.0004 | -0.0003 | -0.0045 |
| L17MLP | 0.0292 | [-0.003, 0.057] | -0.0001 | -0.0082 | -0.0011 | 0.0499 | 0.0014 | -0.0021 | -0.0126 |
| L10MLP | 0.0290 | [-0.003, 0.064] | -0.0020 | 0.0060 | -0.0075 | 0.0365 | -0.0008 | -0.0053 | -0.0052 |
| L6MLP | 0.0191 | [0.005, 0.035] | -0.0064 | 0.0066 | -0.0003 | 0.0160 | 0.0004 | -0.0002 | -0.0023 |
| L12H6 | 0.0178 | [0.006, 0.029] | 0.0001 | 0.0026 | 0.0017 | 0.0125 | 0.0000 | 0.0003 | 0.0007 |
| L8H9 | 0.0145 | [0.001, 0.035] | -0.0005 | 0.0104 | -0.0013 | -0.0011 | -0.0004 | -0.0008 | 0.0037 |
| L5MLP | 0.0134 | [0.003, 0.032] | -0.0034 | 0.0027 | 0.0019 | 0.0095 | -0.0006 | 0.0003 | 0.0021 |
| L10H9 | 0.0120 | [0.000, 0.024] | -0.0002 | 0.0036 | -0.0008 | 0.0070 | 0.0007 | -0.0014 | 0.0022 |
| L23H7 | 0.0116 | [0.004, 0.021] | 0.0000 | 0.0116 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L8H6 | 0.0098 | [0.003, 0.018] | -0.0003 | 0.0022 | -0.0015 | 0.0086 | -0.0002 | 0.0003 | -0.0003 |
| L11H9 | 0.0097 | [0.000, 0.026] | 0.0005 | 0.0061 | 0.0004 | 0.0007 | 0.0008 | 0.0004 | 0.0008 |


| top K patched jointly | share restored |
|---|---|
| 1 | 0.3412 |
| 2 | 0.5306 |
| 5 | 0.8452 |
| 10 | 0.9891 |
| 20 | 0.9889 |

- **screen against exact: Spearman over components / top-20 overlap**: 0.846 / 15 of 20
- **screen input**: screen_object_xlmrlarge.npz (sha256 30b5d1246a2b36d3)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_object_xlmrlarge.npz` | 747,344 | `af22db456cf36236` | exact patching: every component alone; the top 20 per position class; the top K jointly |
