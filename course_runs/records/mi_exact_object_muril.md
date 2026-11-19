# mi_exact_object_muril

_Step 4 agreement, stage exact, task object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 15:56 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 8.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage exact --task object --model muril --max-rows 256` |


- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: embedding output patched everywhere, ratio of sums / worst item (bits)**: 1.000000 / 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 385

| component | share of the gap restored | document bootstrap 95% | at special only | at agree only | at verb only | at object only | at subject only | at ne only | at other only |
|---|---|---|---|---|---|---|---|---|---|
| L11MLP | 0.4488 | [0.400, 0.504] | 0.0000 | 0.4488 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L10H6 | 0.3225 | [0.286, 0.363] | -0.0000 | 0.2986 | 0.0167 | 0.0034 | 0.0002 | 0.0002 | 0.0025 |
| L10MLP | 0.3168 | [0.290, 0.346] | -0.0000 | 0.2990 | 0.0187 | 0.0056 | 0.0000 | -0.0002 | -0.0023 |
| L8H3 | 0.3053 | [0.245, 0.371] | -0.0002 | 0.1728 | 0.0958 | 0.0238 | 0.0002 | 0.0004 | 0.0026 |
| L9MLP | 0.2060 | [0.161, 0.257] | -0.0001 | 0.0968 | 0.0201 | 0.0732 | 0.0011 | -0.0008 | -0.0038 |
| L8MLP | 0.1940 | [0.154, 0.238] | -0.0003 | 0.0968 | 0.0504 | 0.0483 | -0.0015 | -0.0013 | -0.0037 |
| L11H1 | 0.1479 | [0.123, 0.177] | 0.0000 | 0.1479 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L9H6 | 0.0852 | [0.071, 0.100] | -0.0000 | 0.0663 | 0.0120 | 0.0059 | -0.0001 | 0.0001 | 0.0006 |
| L0MLP | 0.0814 | [0.041, 0.125] | 0.0007 | -0.0019 | -0.0009 | 0.0850 | 0.0018 | -0.0005 | 0.0053 |
| L11H2 | 0.0591 | [0.048, 0.071] | 0.0000 | 0.0591 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| L3MLP | 0.0579 | [0.029, 0.093] | -0.0002 | 0.0089 | -0.0001 | 0.0617 | 0.0009 | 0.0004 | -0.0026 |
| L9H3 | 0.0432 | [0.034, 0.055] | 0.0000 | 0.0413 | 0.0016 | -0.0027 | 0.0002 | 0.0004 | 0.0017 |
| L10H3 | 0.0393 | [0.026, 0.052] | 0.0000 | 0.0381 | 0.0010 | -0.0002 | -0.0000 | 0.0000 | 0.0004 |
| L2MLP | 0.0393 | [0.005, 0.085] | -0.0007 | 0.0087 | -0.0012 | 0.0401 | -0.0003 | -0.0005 | 0.0024 |
| L10H10 | 0.0369 | [0.030, 0.045] | 0.0000 | 0.0360 | 0.0007 | -0.0002 | -0.0000 | -0.0000 | 0.0004 |
| L1MLP | 0.0332 | [0.011, 0.058] | 0.0006 | 0.0037 | -0.0006 | 0.0295 | 0.0023 | -0.0007 | -0.0056 |
| L9H8 | 0.0313 | [0.020, 0.045] | -0.0001 | 0.0271 | 0.0041 | -0.0001 | 0.0001 | -0.0001 | 0.0004 |
| L6MLP | 0.0297 | [0.011, 0.050] | -0.0006 | -0.0031 | 0.0029 | 0.0330 | 0.0015 | -0.0003 | -0.0078 |
| L7MLP | 0.0281 | [-0.006, 0.060] | 0.0002 | 0.0113 | -0.0081 | 0.0213 | 0.0013 | 0.0009 | -0.0030 |
| L5MLP | 0.0277 | [-0.003, 0.063] | 0.0001 | 0.0069 | 0.0041 | 0.0231 | -0.0002 | -0.0009 | -0.0083 |


| top K patched jointly | share restored |
|---|---|
| 1 | 0.4488 |
| 2 | 0.6361 |
| 5 | 0.8230 |
| 10 | 0.9127 |
| 20 | 0.9496 |

- **screen against exact: Spearman over components / top-20 overlap**: 0.860 / 17 of 20
- **screen input**: screen_object_muril.npz (sha256 457413578c210356)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_object_muril.npz` | 446,899 | `8e4ed1d349941829` | exact patching: every component alone; the top 20 per position class; the top K jointly |
