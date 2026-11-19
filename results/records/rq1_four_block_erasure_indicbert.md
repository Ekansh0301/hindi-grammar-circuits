# rq1_four_block_erasure_indicbert

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 01:04 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 7.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter3_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter4_s0.csv"], "tag": "rq1_four_block_erasure_indicbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter3_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_indicberter4_s0.csv --tag rq1_four_block_erasure_indicbert` |


- **pairs with L, S and unit features**: 8,923

## model: indicberter0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberter0_Mean
- **pairs**: 8,630

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.7 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3151 | 0.6594 | 0.3444 | 0.1653 | 0.0912 |
| S | 0.0157 | 0.0460 | 0.0085 | 0.0047 | 0.0036 |
| E | 0.2161 | 0.5144 | 0.2310 | 0.0822 | 0.0368 |
| T | 0.2291 | 0.5308 | 0.2440 | 0.0935 | 0.0482 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7760 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0727 | 0.0646 | 0.0817 |
| ΔR²(T | L, S, E) | 0.0482 | 0.0417 | 0.0541 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3380 | 0.2912 | 0.3850 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9498 | 0.02053 | 0.01756 | 0.02353 | 0.0005 | 0.8559 | 0.8768 | 0.02097 | 452 | 271 | 1.71e-11 |
| T over L+S+E | 0.9464 | 0.9595 | 0.01307 | 0.01093 | 0.01534 | 0.0005 | 0.8778 | 0.8906 | 0.01286 | 330 | 219 | 2.478e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberter1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberter1_Mean
- **pairs**: 8,630

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.8 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.5 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3096 | 0.6594 | 0.3378 | 0.1566 | 0.0847 |
| S | 0.0157 | 0.0460 | 0.0085 | 0.0048 | 0.0036 |
| E | 0.2134 | 0.5144 | 0.2262 | 0.0771 | 0.0359 |
| T | 0.2395 | 0.5538 | 0.2557 | 0.0982 | 0.0504 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7783 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0760 | 0.0675 | 0.0855 |
| ΔR²(T | L, S, E) | 0.0504 | 0.0432 | 0.0570 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3365 | 0.2904 | 0.3848 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9506 | 0.02132 | 0.01834 | 0.02439 | 0.0005 | 0.8559 | 0.8793 | 0.02341 | 470 | 268 | 9.69e-14 |
| T over L+S+E | 0.9464 | 0.9601 | 0.01367 | 0.01137 | 0.01594 | 0.0005 | 0.8778 | 0.8911 | 0.01333 | 339 | 224 | 1.432e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberter2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberter2_Mean
- **pairs**: 8,630

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.8 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.5 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.5 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.5 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3048 | 0.6594 | 0.3337 | 0.1498 | 0.0765 |
| S | 0.0155 | 0.0460 | 0.0083 | 0.0044 | 0.0032 |
| E | 0.2133 | 0.5144 | 0.2253 | 0.0765 | 0.0369 |
| T | 0.2475 | 0.5682 | 0.2649 | 0.1036 | 0.0532 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7810 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0777 | 0.0693 | 0.0874 |
| ΔR²(T | L, S, E) | 0.0532 | 0.0457 | 0.0603 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3160 | 0.2696 | 0.3667 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9512 | 0.02188 | 0.01879 | 0.02508 | 0.0005 | 0.8559 | 0.8809 | 0.02503 | 499 | 283 | 1.015e-14 |
| T over L+S+E | 0.9464 | 0.961 | 0.01461 | 0.01233 | 0.01708 | 0.0005 | 0.8778 | 0.8924 | 0.0146 | 361 | 235 | 2.769e-07 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberter3

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberter3_Mean
- **pairs**: 8,630

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.7 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3134 | 0.6594 | 0.3426 | 0.1628 | 0.0890 |
| S | 0.0156 | 0.0460 | 0.0084 | 0.0046 | 0.0035 |
| E | 0.2157 | 0.5144 | 0.2301 | 0.0813 | 0.0370 |
| T | 0.2305 | 0.5354 | 0.2458 | 0.0935 | 0.0475 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7753 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0719 | 0.0630 | 0.0798 |
| ΔR²(T | L, S, E) | 0.0475 | 0.0412 | 0.0536 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3396 | 0.2918 | 0.3891 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9495 | 0.02024 | 0.01729 | 0.02322 | 0.0005 | 0.8559 | 0.876 | 0.02016 | 451 | 277 | 1.18e-10 |
| T over L+S+E | 0.9464 | 0.9593 | 0.01287 | 0.01081 | 0.01507 | 0.0005 | 0.8778 | 0.8898 | 0.01205 | 323 | 219 | 9.121e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberter4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberter4_Mean
- **pairs**: 8,630

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.7 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3142 | 0.6594 | 0.3432 | 0.1639 | 0.0901 |
| S | 0.0156 | 0.0460 | 0.0084 | 0.0047 | 0.0035 |
| E | 0.2156 | 0.5144 | 0.2302 | 0.0813 | 0.0366 |
| T | 0.2299 | 0.5339 | 0.2450 | 0.0933 | 0.0475 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7753 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0723 | 0.0645 | 0.0809 |
| ΔR²(T | L, S, E) | 0.0475 | 0.0402 | 0.0539 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3432 | 0.2988 | 0.3939 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9498 | 0.02046 | 0.01751 | 0.02351 | 0.0005 | 0.8559 | 0.8759 | 0.02005 | 445 | 272 | 1.088e-10 |
| T over L+S+E | 0.9464 | 0.9594 | 0.01298 | 0.0109 | 0.01519 | 0.0005 | 0.8778 | 0.891 | 0.01321 | 335 | 221 | 1.522e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| indicberter0 | 8630 | 0.6664 | 0.0614 | 0.0727 | 0.0482 | 0.3380 | 0.2912 | 0.3850 | 0.0171 | 0.0131 |
| indicberter1 | 8630 | 0.6664 | 0.0614 | 0.0760 | 0.0504 | 0.3365 | 0.2904 | 0.3848 | 0.0171 | 0.0137 |
| indicberter2 | 8630 | 0.6664 | 0.0614 | 0.0777 | 0.0532 | 0.3160 | 0.2696 | 0.3667 | 0.0171 | 0.0146 |
| indicberter3 | 8630 | 0.6664 | 0.0614 | 0.0719 | 0.0475 | 0.3396 | 0.2918 | 0.3891 | 0.0171 | 0.0129 |
| indicberter4 | 8630 | 0.6664 | 0.0614 | 0.0723 | 0.0475 | 0.3432 | 0.2988 | 0.3939 | 0.0171 | 0.0130 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| indicberter0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter0: E over L+S (McNemar) | 7.46e-14 | 3.73e-13 | yes |
| indicberter0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter0: T over L+S (McNemar) | 1.71e-11 | 6.412e-11 | yes |
| indicberter0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberter0: T over L+S+E (McNemar) | 2.478e-06 | 5.311e-06 | yes |
| indicberter1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter1: E over L+S (McNemar) | 7.46e-14 | 3.73e-13 | yes |
| indicberter1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter1: T over L+S (McNemar) | 9.69e-14 | 4.153e-13 | yes |
| indicberter1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberter1: T over L+S+E (McNemar) | 1.432e-06 | 3.513e-06 | yes |
| indicberter2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter2: E over L+S (McNemar) | 7.46e-14 | 3.73e-13 | yes |
| indicberter2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter2: T over L+S (McNemar) | 1.015e-14 | 3.045e-13 | yes |
| indicberter2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberter2: T over L+S+E (McNemar) | 2.769e-07 | 7.551e-07 | yes |
| indicberter3: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter3: E over L+S (McNemar) | 7.46e-14 | 3.73e-13 | yes |
| indicberter3: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter3: T over L+S (McNemar) | 1.18e-10 | 3.54e-10 | yes |
| indicberter3: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberter3: T over L+S+E (McNemar) | 9.121e-06 | 1.824e-05 | yes |
| indicberter4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter4: E over L+S (McNemar) | 7.46e-14 | 3.73e-13 | yes |
| indicberter4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberter4: T over L+S (McNemar) | 1.088e-10 | 3.54e-10 | yes |
| indicberter4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberter4: T over L+S+E (McNemar) | 1.522e-06 | 3.513e-06 | yes |
