# mi_paper_mlpsets_object_xlmrlarge

_Paper experiments, stage mlpsets, task object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 09:49 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 28.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_nec": null, "n_random": null, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "mlpsets", "task": "object"}` |
| command | `scripts/mi_paper_sets.py --model xlmrlarge --max-rows 128 --task object --stage mlpsets` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against the metric stage's M_none and M_obj, orders / worst (bits)**: 400 / 1.56e-04
- **fresh variant orders with the object not adjacent: available / drawn / built / skipped**: 1470 / 400 / 400 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000000 / 0.00e+00
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 400 / 112 / 400 / 6.181
- **frozen top 5 MLPs (step 4 selection half)**: L21MLP, L20MLP, L22MLP, L19MLP, L23MLP
- **sets tested (frozen set + others) / design**: 256 (255 others) / declared
- **number of sets by overlap with the frozen five (0 / 1 / 2 / 3 / 4)**: 30 / 30 / 40 / 60 / 95
- **necessity sample (random, stratified by overlap; frozen set always included): size / by overlap 0 to 4**: 60 / 7 / 7 / 10 / 14 / 22
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **timing: seconds per item per set (faithfulness, 256 sets / necessity, 61 sets)**: 0.0121 / 0.0115

## Frozen top 5 MLPs against the other sets (descriptive: rank among all others, difference from their mean)


| measure | frozen set | document bootstrap 95% | others, mean | others, 95th pct | rank among others (1 = best) | sign-flip p, two-sided | sign-flip p, one-sided |
|---|---|---|---|---|---|---|---|
| faithfulness (all sets) | 0.644 | [0.603, 0.687] | 0.4166 | 0.6233 | 1 of 256 | 9.999e-05 | 9.999e-05 |
| necessity (sample) | 0.8264 | [0.752, 0.909] | 0.6516 | 0.8172 | 3 of 61 | 9.999e-05 | 9.999e-05 |


## Sets by the number of the frozen five they contain


| frozen MLPs contained | sets | mean faithfulness | best faithfulness | sets with necessity | mean necessity |
|---|---|---|---|---|---|
| 0 | 30 | 0.07521 | 0.1364 | 7 | 0.4908 |
| 1 | 30 | 0.2189 | 0.3803 | 7 | 0.518 |
| 2 | 40 | 0.3543 | 0.511 | 10 | 0.6198 |
| 3 | 60 | 0.4881 | 0.5802 | 14 | 0.661 |
| 4 | 95 | 0.5679 | 0.6391 | 22 | 0.7538 |
| 5 | 1 | 0.644 | 0.644 | 1 | 0.8264 |


> The row for 5 is the frozen set itself.

- **Spearman of the overlap count with faithfulness over the other sets: rho / p (two-sided)**: 0.886 / 3.158e-86

## Declared reading (P4, third addendum)

- **best set sharing at most three of the frozen MLPs: set / overlap / faithfulness**: L10MLP, L16MLP, L20MLP, L21MLP, L22MLP / 3 / 0.5802
- **frozen set faithfulness minus best (margin 0.02 declared) / document bootstrap 95% (descriptive) / one-sided sign-flip p**: 0.0638 / [0.036, 0.092] / 9.999e-05
- **descriptive: best set sharing four of the frozen five: set / faithfulness / frozen minus it**: L10MLP, L20MLP, L21MLP, L22MLP, L23MLP / 0.6391 / 0.0050
- **descriptive: other sets within 0.02 of the frozen set (ties, either side) / above it by more than 0.02 / of all others**: 12 (4.7%) / 0 / 255

| overlap | sets | within 0.02 of the frozen set | above it by more than 0.02 |
|---|---|---|---|
| 0 | 30 | 0 | 0 |
| 1 | 30 | 0 | 0 |
| 2 | 40 | 0 | 0 |
| 3 | 60 | 0 | 0 |
| 4 | 95 | 12 | 0 |


| term | coefficient | document bootstrap 95% (1,000 draws, seed 707) |
|---|---|---|
| intercept | 0.01381 | [-0.0192, 0.0505] |
| mean block index (per block) | 0.009128 | [0.0071, 0.0112] |
| overlap count | 0.09997 | [0.0852, 0.1150] |

- **SPECIFIC (margin >= 0.02 and p < 0.05) / DEPTH (block-index coefficient > 0, interval excludes 0)**: yes / no

## Language-modelling check (held-out nats per subtoken; frozen set and 10 sets drawn across overlap classes)

- **unablated**: 2.4256

| model | overlap | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|---|
| frozen top 5 MLPs ablated | 5 | 3.6002 | 1.1746 | yes |
| set L3MLP, L19MLP, L20MLP, L22MLP, L23MLP | 4 | 3.1376 | 0.7120 | yes |
| set L2MLP, L20MLP, L21MLP, L22MLP, L23MLP | 4 | 3.3457 | 0.9201 | yes |
| set L0MLP, L1MLP, L19MLP, L21MLP, L22MLP | 3 | 3.1381 | 0.7125 | yes |
| set L1MLP, L17MLP, L20MLP, L21MLP, L22MLP | 3 | 3.1582 | 0.7326 | yes |
| set L6MLP, L8MLP, L9MLP, L20MLP, L23MLP | 2 | 3.0273 | 0.6017 | yes |
| set L6MLP, L8MLP, L12MLP, L19MLP, L23MLP | 2 | 2.9446 | 0.5190 | yes |
| set L1MLP, L9MLP, L11MLP, L16MLP, L22MLP | 1 | 2.7957 | 0.3701 | yes |
| set L10MLP, L14MLP, L15MLP, L16MLP, L21MLP | 1 | 3.0226 | 0.5970 | yes |
| set L1MLP, L3MLP, L7MLP, L15MLP, L16MLP | 0 | 2.7118 | 0.2862 | yes |
| set L2MLP, L4MLP, L8MLP, L10MLP, L13MLP | 0 | 3.4697 | 1.0440 | yes |

- **DECISION mlpsets object xlmrlarge**: SPECIFIC (frozen MLPs of blocks 23, 22, 21, 20, 19)

> Selecting the best of many sets on the same data favours the other sets, so SPECIFIC is the conservative reading; the regression includes the frozen set (overlap 5).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `mlpsets_object_xlmrlarge.npz` | 580,733 | `9d801d73e0a88cc6` | per item and set: faithfulness (all sets) and ablated metrics (nec_idx = the frozen set and the necessity sample); set 0 is the frozen top 5 MLPs; overlap = frozen MLPs contained |
