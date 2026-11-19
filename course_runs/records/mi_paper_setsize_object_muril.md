# mi_paper_setsize_object_muril

_Paper experiments, stage setsize, task object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 10:25 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 36.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_nec": null, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "setsize", "task": "object"}` |
| command | `scripts/mi_paper_sets.py --model muril --max-rows 256 --task object --stage setsize` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against the metric stage's M_none and M_obj, orders / worst (bits)**: 400 / 1.78e-15
- **fresh variant orders with the object not adjacent: available / drawn / built / skipped**: 1470 / 400 / 400 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000000 / 0.00e+00
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 400 / 112 / 395 / 6.263
- **ranking: top 10 equal to step 4's frozen 10 heads (asserted)**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
- **ranking: heads ranked by exact share / by the screen alone (of all heads)**: 144 / 0

| rank | head | ranked by | share (exact; screened where ranked by the screen) |
|---|---|---|---|
| 1 | L10H6 | exact | 0.3225 |
| 2 | L8H3 | exact | 0.3053 |
| 3 | L11H1 | exact | 0.1479 |
| 4 | L9H6 | exact | 0.0852 |
| 5 | L11H2 | exact | 0.0591 |
| 6 | L9H3 | exact | 0.0432 |
| 7 | L10H3 | exact | 0.0393 |
| 8 | L10H10 | exact | 0.0369 |
| 9 | L9H8 | exact | 0.0313 |
| 10 | L11H10 | exact | 0.0255 |
| 11 | L9H5 | exact | 0.0239 |
| 12 | L9H10 | exact | 0.0177 |
| 13 | L5H7 | exact | 0.0150 |
| 14 | L1H3 | exact | 0.0120 |
| 15 | L8H5 | exact | 0.0110 |
| 16 | L10H7 | exact | 0.0088 |
| 17 | L2H3 | exact | 0.0078 |
| 18 | L9H0 | exact | 0.0074 |
| 19 | L11H0 | exact | 0.0073 |
| 20 | L3H4 | exact | 0.0071 |
| 21 | L4H1 | exact | 0.0066 |
| 22 | L2H0 | exact | 0.0064 |
| 23 | L10H4 | exact | 0.0061 |
| 24 | L10H9 | exact | 0.0049 |
| 25 | L4H11 | exact | 0.0045 |
| 26 | L1H10 | exact | 0.0041 |
| 27 | L10H1 | exact | 0.0040 |
| 28 | L7H3 | exact | 0.0038 |
| 29 | L7H6 | exact | 0.0036 |
| 30 | L0H11 | exact | 0.0035 |
| 31 | L3H3 | exact | 0.0034 |
| 32 | L9H4 | exact | 0.0034 |
| 33 | L1H2 | exact | 0.0033 |
| 34 | L10H8 | exact | 0.0029 |
| 35 | L4H2 | exact | 0.0029 |
| 36 | L10H5 | exact | 0.0026 |
| 37 | L4H10 | exact | 0.0026 |
| 38 | L1H1 | exact | 0.0025 |
| 39 | L3H11 | exact | 0.0024 |
| 40 | L6H5 | exact | 0.0023 |

- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477

## K = 5

- **heads of the set ranked by the screen alone**: 0 of 5
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 43 of 139
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 500 / 0 / 0
- **set**: L10H6, L8H3, L11H1, L9H6, L11H2

## K = 10

- **heads of the set ranked by the screen alone**: 0 of 10
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 38 of 134
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **set**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10

## K = 20

- **heads of the set ranked by the screen alone**: 0 of 20
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 76 of 124
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 2000 / 0 / 0
- **set**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10, L9H5, L9H10, L5H7, L1H3, L8H5, L10H7, L2H3, L9H0, L11H0, L3H4

## K = 40

- **heads of the set ranked by the screen alone**: 0 of 40
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 104 of 104
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 50 of 50 / 2000 / 400 / 0
- **set**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10, L9H5, L9H10, L5H7, L1H3, L8H5, L10H7, L2H3, L9H0, L11H0, L3H4, L4H1, L2H0, L10H4, L10H9, L4H11, L1H10, L10H1, L7H3, L7H6, L0H11, L3H3, L9H4, L1H2, L10H8, L4H2, L10H5, L4H10, L1H1, L3H11, L6H5
- **items / with a gap above --min-gap / documents**: 400 / 395 / 112
- **timing: seconds per item per set (faithfulness, over all K) / per item per ablated set (necessity, mean and zero; word order ablates both runs)**: 0.0074 (354 sets) / 0.0046 (506 ablated sets)

## Faithfulness (patch the set into the corrupted run)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.7441 | [0.697, 0.791] | 0.02783 | 0.07003 | 1 of 101 | 0.7162 | 9.999e-05 | 100 | 43 | - |
| 10 | top 10 | 0 | 0.8507 | [0.813, 0.891] | 0.02035 | 0.0667 | 1 of 101 | 0.8303 | 9.999e-05 | 100 | 38 | - |
| 20 | top 20 | 0 | 0.9385 | [0.916, 0.960] | -0.03267 | -0.004578 | 1 of 101 | 0.9712 | 9.999e-05 | 100 | 76 | - |
| 40 | top 40 | 0 | 0.9725 | [0.960, 0.985] | -0.03708 | 0.004525 | 1 of 51 | 1.01 | 9.999e-05 | 50 | 104 | - |


## Necessity, mean ablation (share lost when the set is ablated)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.7452 | [0.674, 0.824] | 0.01909 | 0.04489 | 1 of 101 | 0.7261 | 9.999e-05 | 100 | 43 | - |
| 10 | top 10 | 0 | 0.9431 | [0.875, 1.015] | 0.02682 | 0.06669 | 1 of 101 | 0.9163 | 9.999e-05 | 100 | 38 | - |
| 20 | top 20 | 0 | 1.001 | [0.932, 1.076] | 0.00368 | 0.03897 | 1 of 101 | 0.9975 | 9.999e-05 | 100 | 76 | - |
| 40 | top 40 | 0 | 1.025 | [0.945, 1.112] | 0.09073 | 0.1381 | 1 of 51 | 0.9345 | 9.999e-05 | 50 | 104 | - |


## Necessity, zero ablation


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | top 10 | 0 | 0.908 | [0.840, 0.979] | -0.01451 | 0.04794 | 1 of 101 | 0.9225 | 9.999e-05 | 100 | 38 | - |
| 40 | top 40 | 0 | 1.025 | [0.948, 1.113] | 0.09482 | 0.1625 | 1 of 51 | 0.9303 | 9.999e-05 | 50 | 104 | - |


## Language-modelling check (held-out nats per subtoken; the 2-nat rule)

- **unablated**: 3.0697

| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| K=5 top set, mean ablation | 3.1272 | 0.0576 | yes |
| K=5 random set 0, mean ablation | 3.0806 | 0.0109 | yes |
| K=5 random set 1, mean ablation | 3.0831 | 0.0134 | yes |
| K=5 random set 2, mean ablation | 3.0776 | 0.0080 | yes |
| K=5 random set 3, mean ablation | 3.0731 | 0.0034 | yes |
| K=5 random set 4, mean ablation | 3.1039 | 0.0342 | yes |
| K=5 random set 5, mean ablation | 3.0753 | 0.0056 | yes |
| K=5 random set 6, mean ablation | 3.0791 | 0.0094 | yes |
| K=5 random set 7, mean ablation | 3.0798 | 0.0102 | yes |
| K=5 random set 8, mean ablation | 3.0730 | 0.0034 | yes |
| K=5 random set 9, mean ablation | 3.0876 | 0.0179 | yes |
| K=10 top set, mean ablation | 3.2802 | 0.2106 | yes |
| K=10 random set 0, mean ablation | 3.1132 | 0.0436 | yes |
| K=10 random set 1, mean ablation | 3.1008 | 0.0312 | yes |
| K=10 random set 2, mean ablation | 3.1767 | 0.1071 | yes |
| K=10 random set 3, mean ablation | 3.1432 | 0.0735 | yes |
| K=10 random set 4, mean ablation | 3.1946 | 0.1249 | yes |
| K=10 random set 5, mean ablation | 3.1295 | 0.0598 | yes |
| K=10 random set 6, mean ablation | 3.1165 | 0.0468 | yes |
| K=10 random set 7, mean ablation | 3.1321 | 0.0624 | yes |
| K=10 random set 8, mean ablation | 3.1516 | 0.0819 | yes |
| K=10 random set 9, mean ablation | 3.1098 | 0.0401 | yes |
| K=10 top set, zero ablation | 3.2197 | 0.1500 | yes |
| K=20 top set, mean ablation | 3.4618 | 0.3922 | yes |
| K=20 random set 0, mean ablation | 3.2251 | 0.1555 | yes |
| K=20 random set 1, mean ablation | 3.2028 | 0.1331 | yes |
| K=20 random set 2, mean ablation | 3.1293 | 0.0597 | yes |
| K=20 random set 3, mean ablation | 3.1796 | 0.1100 | yes |
| K=20 random set 4, mean ablation | 3.2226 | 0.1529 | yes |
| K=20 random set 5, mean ablation | 3.1585 | 0.0888 | yes |
| K=20 random set 6, mean ablation | 3.1831 | 0.1134 | yes |
| K=20 random set 7, mean ablation | 3.1461 | 0.0764 | yes |
| K=20 random set 8, mean ablation | 3.2104 | 0.1408 | yes |
| K=20 random set 9, mean ablation | 3.1511 | 0.0814 | yes |
| K=40 top set, mean ablation | 3.9157 | 0.8460 | yes |
| K=40 random set 0, mean ablation | 3.2231 | 0.1534 | yes |
| K=40 random set 1, mean ablation | 3.1818 | 0.1121 | yes |
| K=40 random set 2, mean ablation | 3.2594 | 0.1897 | yes |
| K=40 random set 3, mean ablation | 3.2927 | 0.2230 | yes |
| K=40 random set 4, mean ablation | 3.2130 | 0.1433 | yes |
| K=40 random set 5, mean ablation | 3.2110 | 0.1414 | yes |
| K=40 random set 6, mean ablation | 3.2969 | 0.2272 | yes |
| K=40 random set 7, mean ablation | 3.2918 | 0.2222 | yes |
| K=40 random set 8, mean ablation | 3.2317 | 0.1621 | yes |
| K=40 random set 9, mean ablation | 3.2155 | 0.1458 | yes |
| K=40 top set, zero ablation | 3.7595 | 0.6898 | yes |


## Declared reading (P3): necessity at K = 40 minus at K = 10


| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| mean | 0.9431 | 1.025 | 0.08216 | [0.044, 0.120] | yes | 0.21 / 0.85 | COMPACT |

- **DECISION setsize object muril (mean ablation)**: COMPACT

| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| zero | 0.908 | 1.025 | 0.1171 | [0.072, 0.158] | yes | 0.15 / 0.69 | COMPACT |

- **DECISION setsize object muril (zero ablation)**: COMPACT
- **DECISION setsize object muril**: COMPACT (mean ablation); the same under zero ablation

> Agreement: every head was patched exactly, so the ranking is exact for all K.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `setsize_object_muril.npz` | 1,601,269 | `56b1189ff1dd9849` | per item and set: faithfulness and ablated metrics (set 0 of each K is the top-K set); zero ablation for K = 10, 40 |
