# mi_paper_setsize_wordorder_xlmrlarge

_Paper experiments, stage setsize, task wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 22:26 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 785.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_nec": null, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "setsize", "task": "wordorder"}` |
| command | `scripts/mi_paper_sets.py --model xlmrlarge --max-rows 128 --task wordorder --stage setsize` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 9.04e-05
- **fresh pairs: available / drawn / built / skipped**: 471 / 300 / 300 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 0.999998 / 6.20e-06
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 300 / 241 / 259 / 0.503
- **ranking: top 10 equal to step 4's frozen 10 heads (asserted)**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2
- **ranking: heads ranked by exact share / by the screen alone (of all heads)**: 60 / 324

| rank | head | ranked by | share (exact; screened where ranked by the screen) |
|---|---|---|---|
| 1 | L9H2 | exact | 0.0769 |
| 2 | L17H3 | exact | 0.0755 |
| 3 | L17H7 | exact | 0.0754 |
| 4 | L20H14 | exact | 0.0734 |
| 5 | L17H15 | exact | 0.0697 |
| 6 | L21H3 | exact | 0.0671 |
| 7 | L6H15 | exact | 0.0655 |
| 8 | L16H4 | exact | 0.0647 |
| 9 | L16H1 | exact | 0.0639 |
| 10 | L20H2 | exact | 0.0625 |
| 11 | L21H5 | exact | 0.0610 |
| 12 | L20H6 | exact | 0.0600 |
| 13 | L20H3 | exact | 0.0593 |
| 14 | L19H7 | exact | 0.0582 |
| 15 | L19H11 | exact | 0.0565 |
| 16 | L18H12 | exact | 0.0548 |
| 17 | L18H9 | exact | 0.0503 |
| 18 | L19H3 | exact | 0.0498 |
| 19 | L19H8 | exact | 0.0497 |
| 20 | L10H9 | exact | 0.0490 |
| 21 | L15H12 | exact | 0.0475 |
| 22 | L20H10 | exact | 0.0470 |
| 23 | L18H13 | exact | 0.0468 |
| 24 | L16H5 | exact | 0.0452 |
| 25 | L12H4 | exact | 0.0447 |
| 26 | L21H0 | exact | 0.0436 |
| 27 | L19H15 | exact | 0.0356 |
| 28 | L20H15 | exact | 0.0355 |
| 29 | L19H6 | exact | 0.0333 |
| 30 | L19H2 | exact | 0.0301 |
| 31 | L17H4 | exact | 0.0295 |
| 32 | L20H11 | exact | 0.0276 |
| 33 | L18H5 | exact | 0.0265 |
| 34 | L20H0 | exact | 0.0224 |
| 35 | L21H13 | exact | 0.0221 |
| 36 | L10H13 | exact | 0.0175 |
| 37 | L17H6 | exact | 0.0146 |
| 38 | L16H8 | exact | 0.0142 |
| 39 | L11H15 | exact | 0.0127 |
| 40 | L21H12 | exact | 0.0109 |

- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541

## K = 5

- **heads of the set ranked by the screen alone**: 0 of 5
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 5 / 0 (of 5)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 43 of 379
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 500 / 0 / 0
- **set**: L9H2, L17H3, L17H7, L20H14, L17H15

## K = 10

- **heads of the set ranked by the screen alone**: 0 of 10
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 10 / 0 (of 10)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 86 of 374
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **set**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2

## K = 20

- **heads of the set ranked by the screen alone**: 0 of 20
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 20 / 0 (of 20)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 124 of 364
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 2000 / 0 / 0
- **set**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2, L21H5, L20H6, L20H3, L19H7, L19H11, L18H12, L18H9, L19H3, L19H8, L10H9

## K = 40

- **heads of the set ranked by the screen alone**: 0 of 40
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 23 / 17 (of 40)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 152 of 344
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 50 of 50 / 2000 / 0 / 0
- **set**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2, L21H5, L20H6, L20H3, L19H7, L19H11, L18H12, L18H9, L19H3, L19H8, L10H9, L15H12, L20H10, L18H13, L16H5, L12H4, L21H0, L19H15, L20H15, L19H6, L19H2, L17H4, L20H11, L18H5, L20H0, L21H13, L10H13, L17H6, L16H8, L11H15, L21H12
- **items / with a gap above --min-gap / documents**: 300 / 259 / 217
- **timing: seconds per item per set (faithfulness, over all K) / per item per ablated set (necessity, mean and zero; word order ablates both runs)**: 0.1154 (354 sets) / 0.2260 (506 ablated sets)

## Faithfulness (patch the set into the corrupted run)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.2958 | [0.262, 0.334] | 0.03172 | 0.1215 | 1 of 101 | 0.2641 | 9.999e-05 | 100 | 43 | 5 / 0 |
| 10 | top 10 | 0 | 0.4834 | [0.433, 0.543] | 0.08163 | 0.2046 | 1 of 101 | 0.4018 | 9.999e-05 | 100 | 86 | 10 / 0 |
| 20 | top 20 | 0 | 0.7002 | [0.642, 0.768] | 0.2344 | 0.3597 | 1 of 101 | 0.4658 | 9.999e-05 | 100 | 124 | 20 / 0 |
| 40 | top 40 | 0 | 0.8405 | [0.780, 0.906] | 0.3348 | 0.4838 | 1 of 51 | 0.5057 | 9.999e-05 | 50 | 152 | 23 / 17 |


## Necessity, mean ablation (share lost when the set is ablated)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.05656 | [0.026, 0.083] | 0.01452 | 0.03929 | 2 of 101 | 0.04205 | 0.006199 | 100 | 43 | 5 / 0 |
| 10 | top 10 | 0 | 0.0774 | [0.040, 0.109] | 0.01625 | 0.05292 | 1 of 101 | 0.06115 | 0.0005 | 100 | 86 | 10 / 0 |
| 20 | top 20 | 0 | 0.09364 | [0.035, 0.142] | 0.02532 | 0.06296 | 3 of 101 | 0.06832 | 0.004 | 100 | 124 | 20 / 0 |
| 40 | top 40 | 0 | 0.06788 | [-0.009, 0.134] | 0.02229 | 0.05918 | 3 of 51 | 0.04558 | 0.1383 | 50 | 152 | 23 / 17 |


## Necessity, zero ablation


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | top 10 | 0 | -0.01294 | [-0.051, 0.023] | 0.009142 | 0.04459 | 90 of 101 | -0.02208 | 0.2033 | 100 | 86 | 10 / 0 |
| 40 | top 40 | 0 | -0.03512 | [-0.117, 0.039] | -0.04111 | 0.01066 | 28 of 51 | 0.005993 | 0.8598 | 50 | 152 | 23 / 17 |


## Language-modelling check (held-out nats per subtoken; the 2-nat rule)

- **unablated**: 2.4256

| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| K=5 top set, mean ablation | 2.4366 | 0.0110 | yes |
| K=5 random set 0, mean ablation | 2.4520 | 0.0264 | yes |
| K=5 random set 1, mean ablation | 2.4401 | 0.0144 | yes |
| K=5 random set 2, mean ablation | 2.4294 | 0.0038 | yes |
| K=5 random set 3, mean ablation | 2.4155 | -0.0101 | yes |
| K=5 random set 4, mean ablation | 2.4274 | 0.0018 | yes |
| K=5 random set 5, mean ablation | 2.4293 | 0.0037 | yes |
| K=5 random set 6, mean ablation | 2.4269 | 0.0013 | yes |
| K=5 random set 7, mean ablation | 2.4571 | 0.0315 | yes |
| K=5 random set 8, mean ablation | 2.4313 | 0.0056 | yes |
| K=5 random set 9, mean ablation | 2.4423 | 0.0167 | yes |
| K=10 top set, mean ablation | 2.4755 | 0.0499 | yes |
| K=10 random set 0, mean ablation | 2.4533 | 0.0277 | yes |
| K=10 random set 1, mean ablation | 2.4279 | 0.0023 | yes |
| K=10 random set 2, mean ablation | 2.4216 | -0.0040 | yes |
| K=10 random set 3, mean ablation | 2.4459 | 0.0202 | yes |
| K=10 random set 4, mean ablation | 2.4402 | 0.0146 | yes |
| K=10 random set 5, mean ablation | 2.4742 | 0.0486 | yes |
| K=10 random set 6, mean ablation | 2.4699 | 0.0443 | yes |
| K=10 random set 7, mean ablation | 2.4543 | 0.0287 | yes |
| K=10 random set 8, mean ablation | 2.4401 | 0.0145 | yes |
| K=10 random set 9, mean ablation | 2.4843 | 0.0587 | yes |
| K=10 top set, zero ablation | 2.4733 | 0.0477 | yes |
| K=20 top set, mean ablation | 2.6000 | 0.1744 | yes |
| K=20 random set 0, mean ablation | 2.5320 | 0.1064 | yes |
| K=20 random set 1, mean ablation | 2.4442 | 0.0186 | yes |
| K=20 random set 2, mean ablation | 2.4528 | 0.0272 | yes |
| K=20 random set 3, mean ablation | 2.4912 | 0.0656 | yes |
| K=20 random set 4, mean ablation | 2.5014 | 0.0758 | yes |
| K=20 random set 5, mean ablation | 2.4609 | 0.0353 | yes |
| K=20 random set 6, mean ablation | 2.4836 | 0.0580 | yes |
| K=20 random set 7, mean ablation | 2.4902 | 0.0646 | yes |
| K=20 random set 8, mean ablation | 2.4835 | 0.0579 | yes |
| K=20 random set 9, mean ablation | 2.4813 | 0.0557 | yes |
| K=40 top set, mean ablation | 2.8517 | 0.4261 | yes |
| K=40 random set 0, mean ablation | 2.6807 | 0.2551 | yes |
| K=40 random set 1, mean ablation | 2.6127 | 0.1871 | yes |
| K=40 random set 2, mean ablation | 2.6504 | 0.2248 | yes |
| K=40 random set 3, mean ablation | 2.5888 | 0.1632 | yes |
| K=40 random set 4, mean ablation | 2.5771 | 0.1515 | yes |
| K=40 random set 5, mean ablation | 2.6023 | 0.1766 | yes |
| K=40 random set 6, mean ablation | 2.6020 | 0.1764 | yes |
| K=40 random set 7, mean ablation | 2.6231 | 0.1975 | yes |
| K=40 random set 8, mean ablation | 2.6099 | 0.1843 | yes |
| K=40 random set 9, mean ablation | 2.6544 | 0.2288 | yes |
| K=40 top set, zero ablation | 2.7341 | 0.3085 | yes |


## Declared reading (P3): necessity at K = 40 minus at K = 10


| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| mean | 0.0774 | 0.06788 | -0.00952 | [-0.066, 0.039] | no | 0.05 / 0.43 | HEADS NOT NECESSARY EVEN JOINTLY |

- **DECISION setsize wordorder xlmrlarge (mean ablation)**: HEADS NOT NECESSARY EVEN JOINTLY

| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| zero | -0.01294 | -0.03512 | -0.02219 | [-0.091, 0.042] | no | 0.05 / 0.31 | HEADS NOT NECESSARY EVEN JOINTLY |

- **DECISION setsize wordorder xlmrlarge (zero ablation)**: HEADS NOT NECESSARY EVEN JOINTLY
- **DECISION setsize wordorder xlmrlarge**: HEADS NOT NECESSARY EVEN JOINTLY (mean ablation); the same under zero ablation

> Word order: the exact stage patched only 60 heads (the screen's top 30 and 30 matched heads), so every top-K set up to K = 40 is drawn from those 60 and no K here reaches a head the screen ranked low; word-order sets are the best of a pre-selected pool.


> The K = 40 comparison is: the top 40 of a 60-head pool against the rest of the same layers. About a third of the top 40 are heads the exact stage drew as matched random heads (counts per K in the first table).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `setsize_wordorder_xlmrlarge.npz` | 1,580,499 | `5f98841af47e5352` | per item and set: faithfulness and ablated metrics (set 0 of each K is the top-K set); zero ablation for K = 10, 40 |
