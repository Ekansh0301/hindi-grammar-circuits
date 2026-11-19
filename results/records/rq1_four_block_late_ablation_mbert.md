# rq1_four_block_late_ablation_mbert

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 19:23 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 16.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab3_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab4_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab5_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab6_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab7_s0.csv"], "tag": "rq1_four_block_late_ablation_mbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab0_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab1_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab2_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab3_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab4_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab5_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab6_s0.csv <earlier-repo>/sets/set1/Results_Checks/late_ablation/t_mbertab7_s0.csv --tag rq1_four_block_late_ablation_mbert` |


- **pairs with L, S and unit features**: 8,923

## model: mbertab0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab0_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.5 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.7 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3408 | 0.6594 | 0.3718 | 0.2035 | 0.1283 |
| S | 0.0166 | 0.0460 | 0.0109 | 0.0057 | 0.0040 |
| E | 0.2275 | 0.5144 | 0.2486 | 0.1012 | 0.0459 |
| T | 0.1592 | 0.4070 | 0.1675 | 0.0460 | 0.0162 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7441 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0318 | 0.0248 | 0.0381 |
| ΔR²(T | L, S, E) | 0.0162 | 0.0118 | 0.0204 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4904 | 0.4319 | 0.5460 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9375 | 0.008382 | 0.006164 | 0.01046 | 0.0005 | 0.8553 | 0.867 | 0.0117 | 311 | 210 | 1.113e-05 |
| T over L+S+E | 0.9464 | 0.9506 | 0.004195 | 0.002842 | 0.005524 | 0.0005 | 0.8772 | 0.8808 | 0.003593 | 177 | 146 | 0.09492 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab1_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.6 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.8 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3254 | 0.6594 | 0.3518 | 0.1788 | 0.1116 |
| S | 0.0161 | 0.0460 | 0.0097 | 0.0051 | 0.0037 |
| E | 0.2180 | 0.5144 | 0.2327 | 0.0843 | 0.0407 |
| T | 0.1901 | 0.4781 | 0.2016 | 0.0590 | 0.0218 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7497 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0425 | 0.0352 | 0.0495 |
| ΔR²(T | L, S, E) | 0.0218 | 0.0170 | 0.0262 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4878 | 0.4356 | 0.5405 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9412 | 0.01202 | 0.009551 | 0.0145 | 0.0005 | 0.8553 | 0.8708 | 0.01553 | 350 | 216 | 1.956e-08 |
| T over L+S+E | 0.9464 | 0.9523 | 0.005931 | 0.004372 | 0.007498 | 0.0005 | 0.8772 | 0.882 | 0.004867 | 195 | 153 | 0.02782 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab2_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.5 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.7 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3457 | 0.6594 | 0.3785 | 0.2116 | 0.1335 |
| S | 0.0169 | 0.0460 | 0.0115 | 0.0059 | 0.0041 |
| E | 0.2307 | 0.5144 | 0.2541 | 0.1068 | 0.0475 |
| T | 0.1501 | 0.3842 | 0.1575 | 0.0430 | 0.0155 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7434 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0294 | 0.0237 | 0.0356 |
| ΔR²(T | L, S, E) | 0.0155 | 0.0116 | 0.0195 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4739 | 0.4217 | 0.5384 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9368 | 0.007646 | 0.0055 | 0.009675 | 0.0005 | 0.8553 | 0.8663 | 0.01101 | 294 | 199 | 2.178e-05 |
| T over L+S+E | 0.9464 | 0.9504 | 0.003973 | 0.002658 | 0.005275 | 0.0005 | 0.8772 | 0.8816 | 0.004404 | 175 | 137 | 0.03603 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab3

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab3_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.6 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.8 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3253 | 0.6594 | 0.3521 | 0.1787 | 0.1111 |
| S | 0.0163 | 0.0460 | 0.0100 | 0.0053 | 0.0039 |
| E | 0.2184 | 0.5144 | 0.2332 | 0.0848 | 0.0411 |
| T | 0.1904 | 0.4774 | 0.2020 | 0.0597 | 0.0225 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7504 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0428 | 0.0355 | 0.0501 |
| ΔR²(T | L, S, E) | 0.0225 | 0.0179 | 0.0272 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4740 | 0.4269 | 0.5299 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9412 | 0.01201 | 0.009509 | 0.0145 | 0.0005 | 0.8553 | 0.8699 | 0.0146 | 354 | 228 | 1.983e-07 |
| T over L+S+E | 0.9464 | 0.9525 | 0.006127 | 0.004524 | 0.007717 | 0.0005 | 0.8772 | 0.8816 | 0.004404 | 208 | 170 | 0.05689 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab4_Mean
- **pairs**: 8,629

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
| L+E+T | 5 | 1.8 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3213 | 0.6594 | 0.3471 | 0.1724 | 0.1064 |
| S | 0.0161 | 0.0460 | 0.0096 | 0.0051 | 0.0037 |
| E | 0.2159 | 0.5144 | 0.2293 | 0.0805 | 0.0393 |
| T | 0.1982 | 0.4954 | 0.2107 | 0.0631 | 0.0237 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7516 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0458 | 0.0369 | 0.0535 |
| ΔR²(T | L, S, E) | 0.0237 | 0.0181 | 0.0286 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4833 | 0.4372 | 0.5297 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9422 | 0.01299 | 0.01039 | 0.01545 | 0.0005 | 0.8553 | 0.8717 | 0.01646 | 363 | 221 | 4.553e-09 |
| T over L+S+E | 0.9464 | 0.9529 | 0.006499 | 0.004898 | 0.008084 | 0.0005 | 0.8772 | 0.8843 | 0.007185 | 215 | 153 | 0.00144 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab5

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab5_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.5 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.3 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.7 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3517 | 0.6594 | 0.3862 | 0.2210 | 0.1403 |
| S | 0.0174 | 0.0460 | 0.0124 | 0.0065 | 0.0046 |
| E | 0.2335 | 0.5144 | 0.2596 | 0.1120 | 0.0480 |
| T | 0.1385 | 0.3576 | 0.1450 | 0.0381 | 0.0132 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7410 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0266 | 0.0211 | 0.0322 |
| ΔR²(T | L, S, E) | 0.0132 | 0.0095 | 0.0169 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.5050 | 0.4448 | 0.5681 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9359 | 0.006774 | 0.004848 | 0.00872 | 0.0005 | 0.8553 | 0.8627 | 0.007417 | 274 | 210 | 0.004141 |
| T over L+S+E | 0.9464 | 0.9496 | 0.003227 | 0.002025 | 0.004466 | 0.0005 | 0.8772 | 0.8795 | 0.002318 | 149 | 129 | 0.2544 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab6

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab6_Mean
- **pairs**: 8,629

### Condition index of each block combination (standardised pair differences)


| blocks | predictors | condition index |
|---|---|---|
| L | 3 | 1.1 |
| S | 3 | 4.3 |
| E | 1 | 1.0 |
| T | 1 | 1.0 |
| L+S | 6 | 4.4 |
| L+E | 4 | 1.4 |
| L+T | 4 | 1.6 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.8 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3279 | 0.6594 | 0.3551 | 0.1826 | 0.1144 |
| S | 0.0165 | 0.0460 | 0.0104 | 0.0056 | 0.0041 |
| E | 0.2195 | 0.5144 | 0.2352 | 0.0868 | 0.0415 |
| T | 0.1848 | 0.4658 | 0.1959 | 0.0567 | 0.0208 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7487 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0407 | 0.0325 | 0.0483 |
| ΔR²(T | L, S, E) | 0.0208 | 0.0157 | 0.0257 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4900 | 0.4386 | 0.5409 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9405 | 0.01132 | 0.008877 | 0.0136 | 0.0005 | 0.8553 | 0.8689 | 0.01367 | 349 | 231 | 1.093e-06 |
| T over L+S+E | 0.9464 | 0.9519 | 0.005544 | 0.004016 | 0.007034 | 0.0005 | 0.8772 | 0.8824 | 0.005215 | 197 | 152 | 0.01838 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mbertab7

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mbertab7_Mean
- **pairs**: 8,629

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
| L+E+T | 5 | 1.8 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3246 | 0.6594 | 0.3508 | 0.1771 | 0.1111 |
| S | 0.0168 | 0.0460 | 0.0108 | 0.0059 | 0.0044 |
| E | 0.2169 | 0.5144 | 0.2313 | 0.0821 | 0.0397 |
| T | 0.1920 | 0.4818 | 0.2040 | 0.0599 | 0.0224 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7503 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0441 | 0.0365 | 0.0514 |
| ΔR²(T | L, S, E) | 0.0224 | 0.0180 | 0.0269 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4918 | 0.4437 | 0.5437 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9414 | 0.01221 | 0.009765 | 0.01466 | 0.0005 | 0.8553 | 0.8699 | 0.0146 | 375 | 249 | 5.159e-07 |
| T over L+S+E | 0.9464 | 0.9524 | 0.005972 | 0.004397 | 0.007516 | 0.0005 | 0.8772 | 0.8834 | 0.006258 | 216 | 162 | 0.006335 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| mbertab0 | 8629 | 0.6665 | 0.0614 | 0.0318 | 0.0162 | 0.4904 | 0.4319 | 0.5460 | 0.0172 | 0.0042 |
| mbertab1 | 8629 | 0.6665 | 0.0614 | 0.0425 | 0.0218 | 0.4878 | 0.4356 | 0.5405 | 0.0172 | 0.0059 |
| mbertab2 | 8629 | 0.6665 | 0.0614 | 0.0294 | 0.0155 | 0.4739 | 0.4217 | 0.5384 | 0.0172 | 0.0040 |
| mbertab3 | 8629 | 0.6665 | 0.0614 | 0.0428 | 0.0225 | 0.4740 | 0.4269 | 0.5299 | 0.0172 | 0.0061 |
| mbertab4 | 8629 | 0.6665 | 0.0614 | 0.0458 | 0.0237 | 0.4833 | 0.4372 | 0.5297 | 0.0172 | 0.0065 |
| mbertab5 | 8629 | 0.6665 | 0.0614 | 0.0266 | 0.0132 | 0.5050 | 0.4448 | 0.5681 | 0.0172 | 0.0032 |
| mbertab6 | 8629 | 0.6665 | 0.0614 | 0.0407 | 0.0208 | 0.4900 | 0.4386 | 0.5409 | 0.0172 | 0.0055 |
| mbertab7 | 8629 | 0.6665 | 0.0614 | 0.0441 | 0.0224 | 0.4918 | 0.4437 | 0.5437 | 0.0172 | 0.0060 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| mbertab0: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab0: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab0: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab0: T over L+S (McNemar) | 1.113e-05 | 3.815e-05 | yes |
| mbertab0: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab0: T over L+S+E (McNemar) | 0.09492 | 0.09694 | no |
| mbertab1: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab1: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab1: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab1: T over L+S (McNemar) | 1.956e-08 | 9.39e-08 | yes |
| mbertab1: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab1: T over L+S+E (McNemar) | 0.02782 | 0.03035 | yes |
| mbertab2: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab2: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab2: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab2: T over L+S (McNemar) | 2.178e-05 | 6.969e-05 | yes |
| mbertab2: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab2: T over L+S+E (McNemar) | 0.03603 | 0.03843 | yes |
| mbertab3: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab3: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab3: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab3: T over L+S (McNemar) | 1.983e-07 | 8.653e-07 | yes |
| mbertab3: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab3: T over L+S+E (McNemar) | 0.05689 | 0.05936 | no |
| mbertab4: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab4: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab4: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab4: T over L+S (McNemar) | 4.553e-09 | 2.428e-08 | yes |
| mbertab4: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab4: T over L+S+E (McNemar) | 0.00144 | 0.001728 | yes |
| mbertab5: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab5: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab5: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab5: T over L+S (McNemar) | 0.004141 | 0.004848 | yes |
| mbertab5: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab5: T over L+S+E (McNemar) | 0.2544 | 0.2544 | no |
| mbertab6: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab6: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab6: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab6: T over L+S (McNemar) | 1.093e-06 | 4.034e-06 | yes |
| mbertab6: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab6: T over L+S+E (McNemar) | 0.01838 | 0.02052 | yes |
| mbertab7: E over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab7: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mbertab7: T over L+S (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab7: T over L+S (McNemar) | 5.159e-07 | 2.064e-06 | yes |
| mbertab7: T over L+S+E (AUC) | 0.0005 | 0.0006154 | yes |
| mbertab7: T over L+S+E (McNemar) | 0.006335 | 0.00724 | yes |
