# mi_paper_setsize_wordorder_muril

_Paper experiments, stage setsize, task wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:53 |
| script | `mi_paper_sets.py` (sha256 `04bffbd9b44c3e7c`) |
| host | gnode (Linux) |
| duration | 208.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_nec": null, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "setsize", "task": "wordorder"}` |
| command | `scripts/mi_paper_sets.py --model muril --max-rows 256 --task wordorder --stage setsize` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.85e-05
- **fresh pairs: available / drawn / built / skipped**: 471 / 300 / 300 / 0
- **check: embedding output patched everywhere, fresh items: ratio of sums / worst pair (bits)**: 1.000001 / 5.72e-06
- **items / documents / with a gap above --min-gap / mean gap (bits)**: 300 / 241 / 258 / 0.606
- **ranking: top 10 equal to step 4's frozen 10 heads (asserted)**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3
- **ranking: heads ranked by exact share / by the screen alone (of all heads)**: 60 / 84

| rank | head | ranked by | share (exact; screened where ranked by the screen) |
|---|---|---|---|
| 1 | L3H11 | exact | 0.1133 |
| 2 | L1H4 | exact | 0.1043 |
| 3 | L1H3 | exact | 0.0974 |
| 4 | L6H6 | exact | 0.0893 |
| 5 | L6H4 | exact | 0.0889 |
| 6 | L9H6 | exact | 0.0869 |
| 7 | L9H10 | exact | 0.0812 |
| 8 | L8H11 | exact | 0.0809 |
| 9 | L2H11 | exact | 0.0789 |
| 10 | L9H3 | exact | 0.0737 |
| 11 | L6H10 | exact | 0.0731 |
| 12 | L9H4 | exact | 0.0722 |
| 13 | L7H2 | exact | 0.0710 |
| 14 | L6H9 | exact | 0.0704 |
| 15 | L10H4 | exact | 0.0701 |
| 16 | L2H10 | exact | 0.0698 |
| 17 | L9H9 | exact | 0.0662 |
| 18 | L8H10 | exact | 0.0614 |
| 19 | L10H10 | exact | 0.0607 |
| 20 | L7H9 | exact | 0.0602 |
| 21 | L5H2 | exact | 0.0600 |
| 22 | L4H4 | exact | 0.0592 |
| 23 | L7H4 | exact | 0.0583 |
| 24 | L8H5 | exact | 0.0574 |
| 25 | L10H6 | exact | 0.0569 |
| 26 | L8H6 | exact | 0.0547 |
| 27 | L7H8 | exact | 0.0547 |
| 28 | L9H11 | exact | 0.0538 |
| 29 | L4H10 | exact | 0.0520 |
| 30 | L7H3 | exact | 0.0515 |
| 31 | L3H1 | exact | 0.0509 |
| 32 | L4H11 | exact | 0.0506 |
| 33 | L2H9 | exact | 0.0500 |
| 34 | L10H9 | exact | 0.0485 |
| 35 | L8H0 | exact | 0.0448 |
| 36 | L10H5 | exact | 0.0424 |
| 37 | L6H11 | exact | 0.0409 |
| 38 | L8H8 | exact | 0.0364 |
| 39 | L8H3 | exact | 0.0346 |
| 40 | L9H5 | exact | 0.0344 |

- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477

## K = 5

- **heads of the set ranked by the screen alone**: 0 of 5
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 5 / 0 (of 5)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 31 of 139
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 500 / 0 / 0
- **set**: L3H11, L1H4, L1H3, L6H6, L6H4

## K = 10

- **heads of the set ranked by the screen alone**: 0 of 10
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 10 / 0 (of 10)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 62 of 134
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **set**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3

## K = 20

- **heads of the set ranked by the screen alone**: 0 of 20
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 20 / 0 (of 20)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 76 of 124
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 2000 / 0 / 0
- **set**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3, L6H10, L9H4, L7H2, L6H9, L10H4, L2H10, L9H9, L8H10, L10H10, L7H9

## K = 40

- **heads of the set ranked by the screen alone**: 0 of 40
- **heads of the set drawn by the exact stage as the screen's top 30 / as the 30 matched random heads**: 28 / 12 (of 40)
- **distinct heads used by the random sets (of the heads outside the top-K set)**: 80 of 104
- **random sets: distinct of asked / replacements / layer-unmatched / type-unmatched**: 50 of 50 / 2000 / 209 / 0
- **set**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3, L6H10, L9H4, L7H2, L6H9, L10H4, L2H10, L9H9, L8H10, L10H10, L7H9, L5H2, L4H4, L7H4, L8H5, L10H6, L8H6, L7H8, L9H11, L4H10, L7H3, L3H1, L4H11, L2H9, L10H9, L8H0, L10H5, L6H11, L8H8, L8H3, L9H5
- **items / with a gap above --min-gap / documents**: 300 / 258 / 215
- **timing: seconds per item per set (faithfulness, over all K) / per item per ablated set (necessity, mean and zero; word order ablates both runs)**: 0.0313 (354 sets) / 0.0592 (506 ablated sets)

## Faithfulness (patch the set into the corrupted run)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.4719 | [0.423, 0.527] | 0.03994 | 0.1259 | 1 of 101 | 0.432 | 9.999e-05 | 100 | 31 | 5 / 0 |
| 10 | top 10 | 0 | 0.7104 | [0.657, 0.772] | 0.1494 | 0.2601 | 1 of 101 | 0.561 | 9.999e-05 | 100 | 62 | 10 / 0 |
| 20 | top 20 | 0 | 0.9825 | [0.949, 1.021] | 0.2356 | 0.3931 | 1 of 101 | 0.7469 | 9.999e-05 | 100 | 76 | 20 / 0 |
| 40 | top 40 | 0 | 1.014 | [0.996, 1.035] | 0.2876 | 0.4055 | 1 of 51 | 0.7269 | 9.999e-05 | 50 | 80 | 28 / 12 |


## Necessity, mean ablation (share lost when the set is ablated)


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | top 5 | 0 | 0.07164 | [0.033, 0.106] | 0.001717 | 0.04536 | 3 of 101 | 0.06992 | 0.0015 | 100 | 31 | 5 / 0 |
| 10 | top 10 | 0 | 0.09255 | [0.043, 0.132] | 0.01393 | 0.07776 | 1 of 101 | 0.07862 | 0.0017 | 100 | 62 | 10 / 0 |
| 20 | top 20 | 0 | 0.103 | [0.012, 0.178] | 0.01075 | 0.06022 | 1 of 101 | 0.0923 | 0.0277 | 100 | 76 | 20 / 0 |
| 40 | top 40 | 0 | 0.1872 | [0.055, 0.291] | -0.01185 | 0.04427 | 1 of 51 | 0.199 | 0.0006999 | 50 | 80 | 28 / 12 |


## Necessity, zero ablation


| K | set | from screen alone | share (restored by patching, or lost by ablating) | document bootstrap 95% | random sets, mean | random sets, 95th pct | rank among random (1 = best) | top-K minus random-K | sign-flip p (set minus random mean) | random sets distinct | distinct heads in random sets | top-K heads: screen top 30 / matched random (word order) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | top 10 | 0 | 0.0258 | [-0.017, 0.062] | 0.0009972 | 0.03099 | 11 of 101 | 0.0248 | 0.1937 | 100 | 62 | 10 / 0 |
| 40 | top 40 | 0 | 0.02911 | [-0.098, 0.134] | -0.06558 | 0.01787 | 2 of 51 | 0.0947 | 0.119 | 50 | 80 | 28 / 12 |


## Language-modelling check (held-out nats per subtoken; the 2-nat rule)

- **unablated**: 3.0697

| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| K=5 top set, mean ablation | 3.0911 | 0.0214 | yes |
| K=5 random set 0, mean ablation | 3.0665 | -0.0032 | yes |
| K=5 random set 1, mean ablation | 3.0655 | -0.0041 | yes |
| K=5 random set 2, mean ablation | 3.0779 | 0.0082 | yes |
| K=5 random set 3, mean ablation | 3.0520 | -0.0177 | yes |
| K=5 random set 4, mean ablation | 3.0723 | 0.0026 | yes |
| K=5 random set 5, mean ablation | 3.0714 | 0.0018 | yes |
| K=5 random set 6, mean ablation | 3.0516 | -0.0180 | yes |
| K=5 random set 7, mean ablation | 3.0530 | -0.0166 | yes |
| K=5 random set 8, mean ablation | 3.0435 | -0.0262 | yes |
| K=5 random set 9, mean ablation | 3.0596 | -0.0101 | yes |
| K=10 top set, mean ablation | 3.1454 | 0.0758 | yes |
| K=10 random set 0, mean ablation | 3.0915 | 0.0218 | yes |
| K=10 random set 1, mean ablation | 3.0862 | 0.0165 | yes |
| K=10 random set 2, mean ablation | 3.0713 | 0.0016 | yes |
| K=10 random set 3, mean ablation | 3.0816 | 0.0119 | yes |
| K=10 random set 4, mean ablation | 3.0848 | 0.0151 | yes |
| K=10 random set 5, mean ablation | 3.0784 | 0.0087 | yes |
| K=10 random set 6, mean ablation | 3.0742 | 0.0045 | yes |
| K=10 random set 7, mean ablation | 3.0687 | -0.0009 | yes |
| K=10 random set 8, mean ablation | 3.0553 | -0.0143 | yes |
| K=10 random set 9, mean ablation | 3.0861 | 0.0164 | yes |
| K=10 top set, zero ablation | 3.1277 | 0.0580 | yes |
| K=20 top set, mean ablation | 3.4837 | 0.4141 | yes |
| K=20 random set 0, mean ablation | 3.1409 | 0.0712 | yes |
| K=20 random set 1, mean ablation | 3.1706 | 0.1010 | yes |
| K=20 random set 2, mean ablation | 3.1090 | 0.0393 | yes |
| K=20 random set 3, mean ablation | 3.1574 | 0.0877 | yes |
| K=20 random set 4, mean ablation | 3.1761 | 0.1064 | yes |
| K=20 random set 5, mean ablation | 3.1072 | 0.0375 | yes |
| K=20 random set 6, mean ablation | 3.1293 | 0.0597 | yes |
| K=20 random set 7, mean ablation | 3.1431 | 0.0735 | yes |
| K=20 random set 8, mean ablation | 3.0995 | 0.0299 | yes |
| K=20 random set 9, mean ablation | 3.1794 | 0.1098 | yes |
| K=40 top set, mean ablation | 4.6796 | 1.6099 | yes |
| K=40 random set 0, mean ablation | 3.3849 | 0.3153 | yes |
| K=40 random set 1, mean ablation | 3.2606 | 0.1909 | yes |
| K=40 random set 2, mean ablation | 3.3508 | 0.2811 | yes |
| K=40 random set 3, mean ablation | 3.3237 | 0.2540 | yes |
| K=40 random set 4, mean ablation | 3.3233 | 0.2536 | yes |
| K=40 random set 5, mean ablation | 3.3832 | 0.3136 | yes |
| K=40 random set 6, mean ablation | 3.3107 | 0.2410 | yes |
| K=40 random set 7, mean ablation | 3.3602 | 0.2906 | yes |
| K=40 random set 8, mean ablation | 3.3570 | 0.2874 | yes |
| K=40 random set 9, mean ablation | 3.4119 | 0.3422 | yes |
| K=40 top set, zero ablation | 3.9262 | 0.8566 | yes |


## Declared reading (P3): necessity at K = 40 minus at K = 10


| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| mean | 0.09255 | 0.1872 | 0.09463 | [-0.015, 0.184] | yes | 0.08 / 1.61 | HEADS NOT NECESSARY EVEN JOINTLY |

- **DECISION setsize wordorder muril (mean ablation)**: HEADS NOT NECESSARY EVEN JOINTLY

| ablation | necessity K=10 | necessity K=40 | K=40 minus K=10 | document bootstrap 95% | top-40 ranks first among random (necessity) | LM cost K=10 / K=40 (nats) | verdict |
|---|---|---|---|---|---|---|---|
| zero | 0.0258 | 0.02911 | 0.003319 | [-0.106, 0.099] | no | 0.06 / 0.86 | HEADS NOT NECESSARY EVEN JOINTLY |

- **DECISION setsize wordorder muril (zero ablation)**: HEADS NOT NECESSARY EVEN JOINTLY
- **DECISION setsize wordorder muril**: HEADS NOT NECESSARY EVEN JOINTLY (mean ablation); the same under zero ablation

> Word order: the exact stage patched only 60 heads (the screen's top 30 and 30 matched heads), so every top-K set up to K = 40 is drawn from those 60 and no K here reaches a head the screen ranked low; word-order sets are the best of a pre-selected pool.


> The K = 40 comparison is: the top 40 of a 60-head pool against the rest of the same layers. About a third of the top 40 are heads the exact stage drew as matched random heads (counts per K in the first table).


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `setsize_wordorder_muril.npz` | 1,603,915 | `dabb439dcb6d5bcd` | per item and set: faithfulness and ablated metrics (set 0 of each K is the top-K set); zero ablation for K = 10, 40 |
