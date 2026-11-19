# mi_paper_mlpsets_wordorder_xlmrlarge

_Paper experiments, stage mlpsets, task wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 12:54 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 213.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_nec": null, "n_random": null, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "mlpsets", "task": "wordorder"}` |
| command | `scripts/mi_paper_sets.py --model xlmrlarge --max-rows 128 --task wordorder --stage mlpsets` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 9.04e-05
- **fresh pairs: available / drawn / built / skipped**: 471 / 300 / 300 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 0.999998 / 6.20e-06
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 300 / 241 / 259 / 0.503
- **frozen top 5 MLPs (step 4 selection half)**: L19MLP, L20MLP, L21MLP, L18MLP, L17MLP
- **sets tested (frozen set + others) / design**: 256 (255 others) / declared
- **number of sets by overlap with the frozen five (0 / 1 / 2 / 3 / 4)**: 30 / 30 / 40 / 60 / 95
- **necessity sample (random, stratified by overlap; frozen set always included): size / by overlap 0 to 4**: 60 / 7 / 7 / 10 / 14 / 22
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **timing: seconds per item per set (faithfulness, 256 sets / necessity, 61 sets)**: 0.1114 / 0.2213

## Frozen top 5 MLPs against the other sets (descriptive: rank among all others, difference from their mean)


| measure | frozen set | document bootstrap 95% | others, mean | others, 95th pct | rank among others (1 = best) | sign-flip p, two-sided | sign-flip p, one-sided |
|---|---|---|---|---|---|---|---|
| faithfulness (all sets) | 0.7921 | [0.740, 0.845] | 0.6345 | 0.7939 | 15 of 256 | 9.999e-05 | 9.999e-05 |
| necessity (sample) | 0.157 | [0.077, 0.228] | -0.01113 | 0.1413 | 3 of 61 | 9.999e-05 | 9.999e-05 |


## Sets by the number of the frozen five they contain


| frozen MLPs contained | sets | mean faithfulness | best faithfulness | sets with necessity | mean necessity |
|---|---|---|---|---|---|
| 0 | 30 | 0.2693 | 0.3773 | 7 | -0.2168 |
| 1 | 30 | 0.4858 | 0.6334 | 7 | -0.1669 |
| 2 | 40 | 0.5926 | 0.7083 | 10 | -0.05788 |
| 3 | 60 | 0.7095 | 0.8226 | 14 | 0.01883 |
| 4 | 95 | 0.7671 | 0.8399 | 22 | 0.106 |
| 5 | 1 | 0.7921 | 0.7921 | 1 | 0.157 |


> The row for 5 is the frozen set itself.

- **Spearman of the overlap count with faithfulness over the other sets: rho / p (two-sided)**: 0.915 / 1.369e-101

## Declared reading (P4, third addendum)

- **best set sharing at most three of the frozen MLPs: set / overlap / faithfulness**: L10MLP, L16MLP, L19MLP, L20MLP, L21MLP / 3 / 0.8226
- **frozen set faithfulness minus best (margin 0.02 declared) / document bootstrap 95% (descriptive) / one-sided sign-flip p**: -0.0304 / [-0.064, -0.001] / 0.9724
- **descriptive: best set sharing four of the frozen five: set / faithfulness / frozen minus it**: L10MLP, L18MLP, L19MLP, L20MLP, L21MLP / 0.8399 / -0.0478
- **descriptive: other sets within 0.02 of the frozen set (ties, either side) / above it by more than 0.02 / of all others**: 34 (13.3%) / 7 / 255

| overlap | sets | within 0.02 of the frozen set | above it by more than 0.02 |
|---|---|---|---|
| 0 | 30 | 0 | 0 |
| 1 | 30 | 0 | 0 |
| 2 | 40 | 0 | 0 |
| 3 | 60 | 3 | 1 |
| 4 | 95 | 31 | 6 |


| term | coefficient | document bootstrap 95% (1,000 draws, seed 707) |
|---|---|---|
| intercept | 0.2328 | [0.1803, 0.2894] |
| mean block index (per block) | 0.0104 | [0.0067, 0.0134] |
| overlap count | 0.09521 | [0.0849, 0.1067] |

- **SPECIFIC (margin >= 0.02 and p < 0.05) / DEPTH (block-index coefficient > 0, interval excludes 0)**: no / yes

## Language-modelling check (held-out nats per subtoken; frozen set and 10 sets drawn across overlap classes)

- **unablated**: 2.4256

| model | overlap | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|---|
| frozen top 5 MLPs ablated | 5 | 3.6267 | 1.2011 | yes |
| set L3MLP, L17MLP, L18MLP, L20MLP, L21MLP | 4 | 3.2159 | 0.7903 | yes |
| set L2MLP, L18MLP, L19MLP, L20MLP, L21MLP | 4 | 3.5874 | 1.1618 | yes |
| set L0MLP, L1MLP, L17MLP, L19MLP, L20MLP | 3 | 3.1060 | 0.6804 | yes |
| set L1MLP, L18MLP, L19MLP, L20MLP, L22MLP | 3 | 3.2576 | 0.8320 | yes |
| set L6MLP, L8MLP, L9MLP, L18MLP, L21MLP | 2 | 3.0140 | 0.5884 | yes |
| set L6MLP, L8MLP, L12MLP, L17MLP, L21MLP | 2 | 2.8770 | 0.4514 | yes |
| set L1MLP, L9MLP, L11MLP, L16MLP, L20MLP | 1 | 2.9139 | 0.4883 | yes |
| set L10MLP, L14MLP, L15MLP, L16MLP, L19MLP | 1 | 3.0599 | 0.6343 | yes |
| set L1MLP, L3MLP, L7MLP, L15MLP, L16MLP | 0 | 2.7118 | 0.2862 | yes |
| set L2MLP, L4MLP, L8MLP, L10MLP, L13MLP | 0 | 3.4697 | 1.0440 | yes |

- **DECISION mlpsets wordorder xlmrlarge**: DEPTH (frozen MLPs of blocks 21, 20, 19, 18, 17)

> Selecting the best of many sets on the same data favours the other sets, so SPECIFIC is the conservative reading; the regression includes the frozen set (overlap 5).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `mlpsets_wordorder_xlmrlarge.npz` | 444,567 | `9623d0ffbfcc47c7` | per item and set: faithfulness (all sets) and ablated metrics (nec_idx = the frozen set and the necessity sample); set 0 is the frozen top 5 MLPs; overlap = frozen MLPs contained |
