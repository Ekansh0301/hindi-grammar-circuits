# mi_paper_setsize_object_xlmrlarge

_Paper experiments, stage setsize, task object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 10:46 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 86.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_nec": null, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "setsize", "task": "object"}` |
| command | `scripts/mi_paper_sets.py --model xlmrlarge --max-rows 128 --task object --stage setsize` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against the metric stage's M_none and M_obj, orders / worst (bits)**: 400 / 1.56e-04
- **fresh variant orders with the object not adjacent: available / drawn / built / skipped**: 1470 / 400 / 400 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000000 / 0.00e+00
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 400 / 112 / 400 / 6.181
- **ranking: top 10 equal to step 4's frozen 10 heads (asserted)**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
- **ranking: heads ranked by exact share / by the screen alone (of all heads)**: 384 / 0

| rank | head | ranked by | share (exact; screened where ranked by the screen) |
|---|---|---|---|
| 1 | L21H0 | exact | 0.2878 |
| 2 | L20H0 | exact | 0.2498 |
| 3 | L20H2 | exact | 0.1086 |
| 4 | L22H6 | exact | 0.0771 |
| 5 | L19H3 | exact | 0.0599 |
| 6 | L23H15 | exact | 0.0152 |
| 7 | L12H6 | exact | 0.0115 |
| 8 | L23H7 | exact | 0.0107 |
| 9 | L17H7 | exact | 0.0094 |
| 10 | L9H13 | exact | 0.0087 |
| 11 | L10H2 | exact | 0.0084 |
| 12 | L1H3 | exact | 0.0082 |
| 13 | L13H4 | exact | 0.0082 |
| 14 | L10H9 | exact | 0.0080 |
| 15 | L21H10 | exact | 0.0080 |
| 16 | L22H1 | exact | 0.0080 |
| 17 | L22H7 | exact | 0.0076 |
| 18 | L17H8 | exact | 0.0074 |
| 19 | L21H7 | exact | 0.0074 |
| 20 | L20H9 | exact | 0.0071 |
| 21 | L0H7 | exact | 0.0069 |
| 22 | L4H2 | exact | 0.0065 |
| 23 | L21H6 | exact | 0.0064 |
| 24 | L18H5 | exact | 0.0063 |
| 25 | L14H5 | exact | 0.0061 |
| 26 | L18H3 | exact | 0.0061 |
| 27 | L23H2 | exact | 0.0056 |
| 28 | L21H3 | exact | 0.0055 |
| 29 | L20H13 | exact | 0.0055 |
| 30 | L0H3 | exact | 0.0054 |
| 31 | L15H6 | exact | 0.0053 |
| 32 | L11H15 | exact | 0.0053 |
| 33 | L23H13 | exact | 0.0051 |
| 34 | L1H12 | exact | 0.0051 |
| 35 | L11H4 | exact | 0.0051 |
| 36 | L2H0 | exact | 0.0050 |
| 37 | L22H15 | exact | 0.0049 |
| 38 | L16H10 | exact | 0.0048 |
| 39 | L8H4 | exact | 0.0048 |
| 40 | L20H6 | exact | 0.0047 |

- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541

## K = 5

- **heads of the set ranked by the screen alone**: 0 of 5
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 59 of 379
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 500 / 0 / 0
- **set**: L21H0, L20H0, L20H2, L22H6, L19H3

## K = 10

- **heads of the set ranked by the screen alone**: 0 of 10
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 118 of 374
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **set**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13

## K = 20

- **heads of the set ranked by the screen alone**: 0 of 20
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 156 of 364
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 2000 / 0 / 0
- **set**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13, L10H2, L1H3, L13H4, L10H9, L21H10, L22H1, L22H7, L17H8, L21H7, L20H9

## K = 40

- **heads of the set ranked by the screen alone**: 0 of 40
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 275 of 344
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 50 of 50 / 2000 / 0 / 0
- **set**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13, L10H2, L1H3, L13H4, L10H9, L21H10, L22H1, L22H7, L17H8, L21H7, L20H9, L0H7, L4H2, L21H6, L18H5, L14H5, L18H3, L23H2, L21H3, L20H13, L0H3, L15H6, L11H15, L23H13, L1H12, L11H4, L2H0, L22H15, L16H10, L8H4, L20H6
- **items / with a gap above --min-gap / documents**: 400 / 400 / 112
- **timing: seconds per item per set (faithfulness, over all K) / per item per ablated set (necessity, mean and zero; word order ablates both runs)**: 0.0154 (354 sets) / 0.0122 (506 ablated sets)

## Faithfulness (patch the set into the corrupted run)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.6624 | [0.612, 0.709] | -0.002346 | 0.01571 | 1 of 101 | 0.6648 | 9.999e-05 | 100 | 59 | - |
| 10 | top 10 | 0 | 0.693 | [0.654, 0.733] | 0.003775 | 0.02235 | 1 of 101 | 0.6893 | 9.999e-05 | 100 | 118 | - |
| 20 | top 20 | 0 | 0.7382 | [0.707, 0.771] | -0.001145 | 0.03329 | 1 of 101 | 0.7394 | 9.999e-05 | 100 | 156 | - |
| 40 | top 40 | 0 | 0.7978 | [0.770, 0.824] | -0.004701 | 0.04154 | 1 of 51 | 0.8025 | 9.999e-05 | 50 | 275 | - |


## Necessity, mean ablation (share lost when the set is ablated)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.8703 | [0.783, 0.956] | 0.005059 | 0.04313 | 1 of 101 | 0.8653 | 9.999e-05 | 100 | 59 | - |
| 10 | top 10 | 0 | 0.8905 | [0.806, 0.974] | 0.001983 | 0.04665 | 1 of 101 | 0.8885 | 9.999e-05 | 100 | 118 | - |
| 20 | top 20 | 0 | 0.926 | [0.843, 1.010] | 0.009106 | 0.07597 | 1 of 101 | 0.9169 | 9.999e-05 | 100 | 156 | - |
| 40 | top 40 | 0 | 0.9746 | [0.893, 1.055] | 0.01719 | 0.09542 | 1 of 51 | 0.9574 | 9.999e-05 | 50 | 275 | - |


## Necessity, zero ablation


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | top 10 | 0 | 0.7971 | [0.716, 0.884] | 0.01078 | 0.08627 | 1 of 101 | 0.7863 | 9.999e-05 | 100 | 118 | - |
| 40 | top 40 | 0 | 0.8742 | [0.792, 0.964] | 0.06171 | 0.1897 | 1 of 51 | 0.8125 | 9.999e-05 | 50 | 275 | - |


## Language-modelling check (held-out nats per subtoken; the 2-nat rule)

- **unablated**: 2.4256

| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| K=5 top set, mean ablation | 2.4574 | 0.0318 | yes |
| K=5 random set 0, mean ablation | 2.4424 | 0.0167 | yes |
| K=5 random set 1, mean ablation | 2.4451 | 0.0195 | yes |
| K=5 random set 2, mean ablation | 2.4777 | 0.0521 | yes |
| K=5 random set 3, mean ablation | 2.4344 | 0.0087 | yes |
| K=5 random set 4, mean ablation | 2.4386 | 0.0130 | yes |
| K=5 random set 5, mean ablation | 2.4369 | 0.0113 | yes |
| K=5 random set 6, mean ablation | 2.4517 | 0.0261 | yes |
| K=5 random set 7, mean ablation | 2.4356 | 0.0100 | yes |
| K=5 random set 8, mean ablation | 2.4411 | 0.0155 | yes |
| K=5 random set 9, mean ablation | 2.4444 | 0.0188 | yes |
| K=10 top set, mean ablation | 2.4832 | 0.0576 | yes |
| K=10 random set 0, mean ablation | 2.4600 | 0.0344 | yes |
| K=10 random set 1, mean ablation | 2.5418 | 0.1162 | yes |
| K=10 random set 2, mean ablation | 2.4401 | 0.0144 | yes |
| K=10 random set 3, mean ablation | 2.4525 | 0.0269 | yes |
| K=10 random set 4, mean ablation | 2.4466 | 0.0209 | yes |
| K=10 random set 5, mean ablation | 2.4405 | 0.0149 | yes |
| K=10 random set 6, mean ablation | 2.4449 | 0.0193 | yes |
| K=10 random set 7, mean ablation | 2.4634 | 0.0378 | yes |
| K=10 random set 8, mean ablation | 2.4577 | 0.0321 | yes |
| K=10 random set 9, mean ablation | 2.4469 | 0.0213 | yes |
| K=10 top set, zero ablation | 2.4889 | 0.0632 | yes |
| K=20 top set, mean ablation | 2.5564 | 0.1308 | yes |
| K=20 random set 0, mean ablation | 2.4666 | 0.0410 | yes |
| K=20 random set 1, mean ablation | 2.4746 | 0.0490 | yes |
| K=20 random set 2, mean ablation | 2.4693 | 0.0437 | yes |
| K=20 random set 3, mean ablation | 2.4564 | 0.0308 | yes |
| K=20 random set 4, mean ablation | 2.4973 | 0.0717 | yes |
| K=20 random set 5, mean ablation | 2.4665 | 0.0408 | yes |
| K=20 random set 6, mean ablation | 2.5077 | 0.0821 | yes |
| K=20 random set 7, mean ablation | 2.4805 | 0.0549 | yes |
| K=20 random set 8, mean ablation | 2.4625 | 0.0369 | yes |
| K=20 random set 9, mean ablation | 2.5023 | 0.0767 | yes |
| K=40 top set, mean ablation | 2.6922 | 0.2666 | yes |
| K=40 random set 0, mean ablation | 2.5629 | 0.1373 | yes |
| K=40 random set 1, mean ablation | 2.5571 | 0.1315 | yes |
| K=40 random set 2, mean ablation | 2.5945 | 0.1689 | yes |
| K=40 random set 3, mean ablation | 2.5618 | 0.1361 | yes |
| K=40 random set 4, mean ablation | 2.5579 | 0.1323 | yes |
| K=40 random set 5, mean ablation | 2.5793 | 0.1537 | yes |
| K=40 random set 6, mean ablation | 2.6113 | 0.1857 | yes |
| K=40 random set 7, mean ablation | 2.5724 | 0.1468 | yes |
| K=40 random set 8, mean ablation | 2.5989 | 0.1733 | yes |
| K=40 random set 9, mean ablation | 2.5361 | 0.1105 | yes |
| K=40 top set, zero ablation | 2.6628 | 0.2372 | yes |


## Declared reading (P3): necessity at K = 40 minus at K = 10


| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| mean | 0.8905 | 0.9746 | 0.08405 | [0.058, 0.110] | yes | 0.06 / 0.27 | NONE OF THE THREE |

- **DECISION setsize object xlmrlarge (mean ablation)**: NONE OF THE THREE

| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| zero | 0.7971 | 0.8742 | 0.07703 | [0.040, 0.114] | yes | 0.06 / 0.24 | NONE OF THE THREE |

- **DECISION setsize object xlmrlarge (zero ablation)**: NONE OF THE THREE
- **DECISION setsize object xlmrlarge**: NONE OF THE THREE (mean ablation); the same under zero ablation

> Agreement: every head was patched exactly, so the ranking is exact for all K.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `setsize_object_xlmrlarge.npz` | 1,602,506 | `77ee00145e57d0b9` | per item and set: faithfulness and ablated metrics (set 0 of each K is the top-K set); zero ablation for K = 10, 40 |
