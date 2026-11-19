# mi_paper_mlpsets_wordorder_muril

_Paper experiments, stage mlpsets, task wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:42 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 149.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_nec": null, "n_random": null, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "mlpsets", "task": "wordorder"}` |
| command | `scripts/mi_paper_sets.py --model muril --max-rows 256 --task wordorder --stage mlpsets` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.85e-05
- **fresh pairs: available / drawn / built / skipped**: 471 / 300 / 300 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000001 / 5.72e-06
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 300 / 241 / 258 / 0.606
- **frozen top 5 MLPs (step 4 selection half)**: L10MLP, L9MLP, L8MLP, L7MLP, L6MLP
- **sets tested (frozen set + others) / design**: 792 (791 others) / declared
- **number of sets by overlap with the frozen five (0 / 1 / 2 / 3 / 4)**: 21 / 175 / 350 / 210 / 35
- **necessity sample (random, stratified by overlap; frozen set always included): size / by overlap 0 to 4**: 100 / 3 / 22 / 44 / 27 / 4
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **timing: seconds per item per set (faithfulness, 792 sets / necessity, 101 sets)**: 0.0298 / 0.0589

## Frozen top 5 MLPs against the other sets (descriptive: rank among all others, difference from their mean)


| measure | frozen set | document bootstrap 95% | others, mean | others, 95th pct | rank among others (1 = best) | sign-flip p, two-sided | sign-flip p, one-sided |
|---|---|---|---|---|---|---|---|
| faithfulness (all sets) | 0.9762 | [0.943, 1.014] | 0.8401 | 0.9517 | 3 of 792 | 9.999e-05 | 9.999e-05 |
| necessity (sample) | 0.3239 | [0.219, 0.408] | 0.4241 | 0.7539 | 52 of 101 | 9.999e-05 | 1 |


## Sets by the number of the frozen five they contain


| frozen MLPs contained | sets | mean faithfulness | best faithfulness | sets with necessity | mean necessity |
|---|---|---|---|---|---|
| 0 | 21 | 0.6245 | 0.7121 | 3 | 0.6419 |
| 1 | 175 | 0.7558 | 0.8797 | 22 | 0.548 |
| 2 | 350 | 0.845 | 0.9451 | 44 | 0.4266 |
| 3 | 210 | 0.9058 | 0.9664 | 27 | 0.2907 |
| 4 | 35 | 0.9477 | 0.9781 | 4 | 0.4518 |
| 5 | 1 | 0.9762 | 0.9762 | 1 | 0.3239 |


> The row for 5 is the frozen set itself.

- **Spearman of the overlap count with faithfulness over the other sets: rho / p (two-sided)**: 0.772 / 1.102e-157

## Declared reading (P4, third addendum)

- **best set sharing at most three of the frozen MLPs: set / overlap / faithfulness**: L1MLP, L2MLP, L8MLP, L9MLP, L10MLP / 3 / 0.9664
- **frozen set faithfulness minus best (margin 0.02 declared) / document bootstrap 95% (descriptive) / one-sided sign-flip p**: 0.0098 / [-0.011, 0.029] / 0.1773
- **descriptive: best set sharing four of the frozen five: set / faithfulness / frozen minus it**: L1MLP, L7MLP, L8MLP, L9MLP, L10MLP / 0.9781 / -0.0020
- **descriptive: other sets within 0.02 of the frozen set (ties, either side) / above it by more than 0.02 / of all others**: 30 (3.8%) / 0 / 791

| overlap | sets | within 0.02 of the frozen set | above it by more than 0.02 |
|---|---|---|---|
| 0 | 21 | 0 | 0 |
| 1 | 175 | 0 | 0 |
| 2 | 350 | 0 | 0 |
| 3 | 210 | 12 | 0 |
| 4 | 35 | 18 | 0 |


| term | coefficient | document bootstrap 95% (1,000 draws, seed 707) |
|---|---|---|
| intercept | 0.6645 | [0.5944, 0.7335] |
| mean block index (per block) | 0.005628 | [-0.0054, 0.0163] |
| overlap count | 0.06953 | [0.0571, 0.0852] |

- **SPECIFIC (margin >= 0.02 and p < 0.05) / DEPTH (block-index coefficient > 0, interval excludes 0)**: no / no

## Language-modelling check (held-out nats per subtoken; frozen set and 10 sets drawn across overlap classes)

- **unablated**: 3.0697

| model | overlap | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|---|
| frozen top 5 MLPs ablated | 5 | 4.6805 | 1.6109 | yes |
| set L0MLP, L1MLP, L3MLP, L4MLP, L5MLP | 0 | 7.0743 | 4.0046 | no |
| set L0MLP, L2MLP, L3MLP, L4MLP, L5MLP | 0 | 7.1050 | 4.0354 | no |
| set L0MLP, L2MLP, L3MLP, L4MLP, L9MLP | 1 | 6.9714 | 3.9017 | no |
| set L2MLP, L4MLP, L5MLP, L10MLP, L11MLP | 1 | 4.7234 | 1.6537 | yes |
| set L2MLP, L3MLP, L7MLP, L9MLP, L11MLP | 2 | 4.5070 | 1.4373 | yes |
| set L2MLP, L4MLP, L5MLP, L8MLP, L10MLP | 2 | 4.2719 | 1.2022 | yes |
| set L0MLP, L1MLP, L6MLP, L7MLP, L10MLP | 3 | 6.6277 | 3.5581 | no |
| set L0MLP, L4MLP, L8MLP, L9MLP, L10MLP | 3 | 6.9684 | 3.8987 | no |
| set L3MLP, L6MLP, L7MLP, L8MLP, L9MLP | 4 | 4.3267 | 1.2570 | yes |
| set L5MLP, L6MLP, L8MLP, L9MLP, L10MLP | 4 | 4.5032 | 1.4335 | yes |

- **DECISION mlpsets wordorder muril**: NEITHER (frozen MLPs of blocks 10, 9, 8, 7, 6)

> Selecting the best of many sets on the same data favours the other sets, so SPECIFIC is the conservative reading; the regression includes the frozen set (overlap 5).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `mlpsets_wordorder_muril.npz` | 1,125,690 | `b9c5ce5b18203b75` | per item and set: faithfulness (all sets) and ablated metrics (nec_idx = the frozen set and the necessity sample); set 0 is the frozen top 5 MLPs; overlap = frozen MLPs contained |
