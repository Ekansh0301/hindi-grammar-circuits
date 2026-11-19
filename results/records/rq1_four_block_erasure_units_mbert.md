# rq1_four_block_erasure_units_mbert

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 14:07 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 7.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu4_s0.csv"], "tag": "rq1_four_block_erasure_units_mbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_mberteu4_s0.csv --tag rq1_four_block_erasure_units_mbert` |


- **pairs with L, S and unit features**: 8,923

## model: mberteu0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberteu0_Mean
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


## model: mberteu1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberteu1_Mean
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
| L+T | 4 | 1.4 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.3 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.6 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3662 | 0.6594 | 0.4072 | 0.2450 | 0.1532 |
| S | 0.0179 | 0.0460 | 0.0141 | 0.0069 | 0.0048 |
| E | 0.2434 | 0.5144 | 0.2775 | 0.1298 | 0.0519 |
| T | 0.1085 | 0.2852 | 0.1133 | 0.0274 | 0.0082 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7361 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0177 | 0.0139 | 0.0219 |
| ΔR²(T | L, S, E) | 0.0082 | 0.0059 | 0.0109 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.5366 | 0.4599 | 0.6100 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9338 | 0.004655 | 0.002998 | 0.006224 | 0.0005 | 0.8553 | 0.8626 | 0.007301 | 247 | 184 | 0.00278 |
| T over L+S+E | 0.9464 | 0.9485 | 0.002118 | 0.001176 | 0.003059 | 0.0005 | 0.8772 | 0.879 | 0.001854 | 129 | 113 | 0.3349 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mberteu2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberteu2_Mean
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
| L | 0.3515 | 0.6594 | 0.3861 | 0.2208 | 0.1399 |
| S | 0.0173 | 0.0460 | 0.0122 | 0.0063 | 0.0046 |
| E | 0.2345 | 0.5144 | 0.2603 | 0.1134 | 0.0500 |
| T | 0.1332 | 0.3516 | 0.1395 | 0.0331 | 0.0087 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7366 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0201 | 0.0154 | 0.0253 |
| ΔR²(T | L, S, E) | 0.0087 | 0.0061 | 0.0121 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.5662 | 0.4996 | 0.6391 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9345 | 0.005368 | 0.003733 | 0.007138 | 0.0005 | 0.8553 | 0.8631 | 0.00788 | 255 | 187 | 0.001411 |
| T over L+S+E | 0.9464 | 0.9487 | 0.002309 | 0.00136 | 0.003249 | 0.0005 | 0.8772 | 0.8779 | 0.0006953 | 124 | 118 | 0.748 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mberteu4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberteu4_Mean
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
| L+E+T | 5 | 1.7 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3401 | 0.6594 | 0.3708 | 0.2024 | 0.1278 |
| S | 0.0166 | 0.0460 | 0.0107 | 0.0056 | 0.0040 |
| E | 0.2271 | 0.5144 | 0.2478 | 0.1004 | 0.0458 |
| T | 0.1608 | 0.4105 | 0.1692 | 0.0467 | 0.0166 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7445 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0323 | 0.0259 | 0.0392 |
| ΔR²(T | L, S, E) | 0.0166 | 0.0122 | 0.0208 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4849 | 0.4300 | 0.5426 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9377 | 0.008508 | 0.006315 | 0.01056 | 0.0005 | 0.8553 | 0.8622 | 0.006953 | 293 | 233 | 0.01003 |
| T over L+S+E | 0.9464 | 0.9508 | 0.004397 | 0.003038 | 0.005738 | 0.0005 | 0.8772 | 0.8811 | 0.00394 | 174 | 140 | 0.06239 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| mberteu0 | 8629 | 0.6665 | 0.0614 | 0.0318 | 0.0162 | 0.4904 | 0.4319 | 0.5460 | 0.0172 | 0.0042 |
| mberteu1 | 8629 | 0.6665 | 0.0614 | 0.0177 | 0.0082 | 0.5366 | 0.4599 | 0.6100 | 0.0172 | 0.0021 |
| mberteu2 | 8629 | 0.6665 | 0.0614 | 0.0201 | 0.0087 | 0.5662 | 0.4996 | 0.6391 | 0.0172 | 0.0023 |
| mberteu4 | 8629 | 0.6665 | 0.0614 | 0.0323 | 0.0166 | 0.4849 | 0.4300 | 0.5426 | 0.0172 | 0.0044 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| mberteu0: E over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu0: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberteu0: T over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu0: T over L+S (McNemar) | 1.113e-05 | 5.342e-05 | yes |
| mberteu0: T over L+S+E (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu0: T over L+S+E (McNemar) | 0.09492 | 0.1035 | no |
| mberteu1: E over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu1: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberteu1: T over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu1: T over L+S (McNemar) | 0.00278 | 0.003512 | yes |
| mberteu1: T over L+S+E (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu1: T over L+S+E (McNemar) | 0.3349 | 0.3495 | no |
| mberteu2: E over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu2: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberteu2: T over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu2: T over L+S (McNemar) | 0.001411 | 0.001881 | yes |
| mberteu2: T over L+S+E (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu2: T over L+S+E (McNemar) | 0.748 | 0.748 | no |
| mberteu4: E over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu4: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberteu4: T over L+S (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu4: T over L+S (McNemar) | 0.01003 | 0.01204 | yes |
| mberteu4: T over L+S+E (AUC) | 0.0005 | 0.0007059 | yes |
| mberteu4: T over L+S+E (McNemar) | 0.06239 | 0.0713 | no |
