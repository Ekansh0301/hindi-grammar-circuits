# mi_paper_mlpsets_object_muril

_Paper experiments, stage mlpsets, task object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 11:13 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 26.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_nec": null, "n_random": null, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "mlpsets", "task": "object"}` |
| command | `scripts/mi_paper_sets.py --model muril --max-rows 256 --task object --stage mlpsets` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against the metric stage's M_none and M_obj, orders / worst (bits)**: 400 / 1.78e-15
- **fresh variant orders with the object not adjacent: available / drawn / built / skipped**: 1470 / 400 / 400 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000000 / 0.00e+00
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 400 / 112 / 395 / 6.263
- **frozen top 5 MLPs (step 4 selection half)**: L11MLP, L10MLP, L9MLP, L8MLP, L0MLP
- **sets tested (frozen set + others) / design**: 792 (791 others) / declared
- **number of sets by overlap with the frozen five (0 / 1 / 2 / 3 / 4)**: 21 / 175 / 350 / 210 / 35
- **necessity sample (random, stratified by overlap; frozen set always included): size / by overlap 0 to 4**: 100 / 3 / 22 / 44 / 27 / 4
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **timing: seconds per item per set (faithfulness, 792 sets / necessity, 101 sets)**: 0.0043 / 0.0034

## Frozen top 5 MLPs against the other sets (descriptive: rank among all others, difference from their mean)


| measure | frozen set | document bootstrap 95% | others, mean | others, 95th pct | rank among others (1 = best) | sign-flip p, two-sided | sign-flip p, one-sided |
|---|---|---|---|---|---|---|---|
| faithfulness (all sets) | 0.7633 | [0.707, 0.806] | 0.5547 | 0.7478 | 11 of 792 | 9.999e-05 | 9.999e-05 |
| necessity (sample) | 0.982 | [0.825, 1.182] | 0.9614 | 1.017 | 42 of 101 | 0.7682 | 0.3747 |


## Sets by the number of the frozen five they contain


| frozen MLPs contained | sets | mean faithfulness | best faithfulness | sets with necessity | mean necessity |
|---|---|---|---|---|---|
| 0 | 21 | 0.3112 | 0.4278 | 3 | 0.9843 |
| 1 | 175 | 0.447 | 0.6614 | 22 | 0.9613 |
| 2 | 350 | 0.5563 | 0.7452 | 44 | 0.9599 |
| 3 | 210 | 0.6407 | 0.7657 | 27 | 0.9589 |
| 4 | 35 | 0.7076 | 0.7763 | 4 | 0.9795 |
| 5 | 1 | 0.7633 | 0.7633 | 1 | 0.982 |


> The row for 5 is the frozen set itself.

- **Spearman of the overlap count with faithfulness over the other sets: rho / p (two-sided)**: 0.649 / 8.828e-96

## Declared reading (P4, third addendum)

- **best set sharing at most three of the frozen MLPs: set / overlap / faithfulness**: L2MLP, L6MLP, L9MLP, L10MLP, L11MLP / 3 / 0.7657
- **frozen set faithfulness minus best (margin 0.02 declared) / document bootstrap 95% (descriptive) / one-sided sign-flip p**: -0.0024 / [-0.019, 0.014] / 0.6057
- **descriptive: best set sharing four of the frozen five: set / faithfulness / frozen minus it**: L0MLP, L1MLP, L9MLP, L10MLP, L11MLP / 0.7763 / -0.0129
- **descriptive: other sets within 0.02 of the frozen set (ties, either side) / above it by more than 0.02 / of all others**: 50 (6.3%) / 0 / 791

| overlap | sets | within 0.02 of the frozen set | above it by more than 0.02 |
|---|---|---|---|
| 0 | 21 | 0 | 0 |
| 1 | 175 | 0 | 0 |
| 2 | 350 | 1 | 0 |
| 3 | 210 | 29 | 0 |
| 4 | 35 | 20 | 0 |


| term | coefficient | document bootstrap 95% (1,000 draws, seed 707) |
|---|---|---|
| intercept | 0.2644 | [0.1646, 0.3631] |
| mean block index (per block) | 0.02295 | [0.0107, 0.0355] |
| overlap count | 0.07889 | [0.0687, 0.0892] |

- **SPECIFIC (margin >= 0.02 and p < 0.05) / DEPTH (block-index coefficient > 0, interval excludes 0)**: no / yes

## Language-modelling check (held-out nats per subtoken; frozen set and 10 sets drawn across overlap classes)

- **unablated**: 3.0697

| model | overlap | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|---|
| frozen top 5 MLPs ablated | 5 | 8.0782 | 5.0085 | no |
| set L1MLP, L2MLP, L4MLP, L5MLP, L6MLP | 0 | 4.8394 | 1.7698 | yes |
| set L1MLP, L3MLP, L4MLP, L5MLP, L6MLP | 0 | 4.4447 | 1.3750 | yes |
| set L1MLP, L2MLP, L4MLP, L5MLP, L10MLP | 1 | 4.7991 | 1.7294 | yes |
| set L3MLP, L5MLP, L6MLP, L7MLP, L10MLP | 1 | 4.1855 | 1.1158 | yes |
| set L2MLP, L5MLP, L6MLP, L9MLP, L10MLP | 2 | 4.3316 | 1.2619 | yes |
| set L2MLP, L6MLP, L7MLP, L9MLP, L11MLP | 2 | 4.5210 | 1.4513 | yes |
| set L0MLP, L1MLP, L2MLP, L8MLP, L11MLP | 3 | 7.2757 | 4.2061 | no |
| set L0MLP, L2MLP, L3MLP, L9MLP, L10MLP | 3 | 6.8941 | 3.8244 | no |
| set L0MLP, L4MLP, L9MLP, L10MLP, L11MLP | 4 | 7.5493 | 4.4797 | no |
| set L1MLP, L8MLP, L9MLP, L10MLP, L11MLP | 4 | 5.3409 | 2.2712 | no |

- **DECISION mlpsets object muril**: DEPTH (frozen MLPs of blocks 11, 10, 9, 8, 0); necessity not read (the frozen set's language-modelling cost is 5.01 nats > 2)

> Selecting the best of many sets on the same data favours the other sets, so SPECIFIC is the conservative reading; the regression includes the frozen set (overlap 5).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `mlpsets_object_muril.npz` | 1,611,104 | `f51a708aedcfa070` | per item and set: faithfulness (all sets) and ablated metrics (nec_idx = the frozen set and the necessity sample); set 0 is the frozen top 5 MLPs; overlap = frozen MLPs contained |
