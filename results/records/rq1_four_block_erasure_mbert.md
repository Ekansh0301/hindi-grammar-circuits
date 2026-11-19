# rq1_four_block_erasure_mbert

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 13:19 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 8.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter3_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter4_s0.csv"], "tag": "rq1_four_block_erasure_mbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter3_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_mberter4_s0.csv --tag rq1_four_block_erasure_mbert` |


- **pairs with L, S and unit features**: 8,923

## model: mberter0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberter0_Mean
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


## model: mberter1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberter1_Mean
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
| L | 0.3461 | 0.6594 | 0.3791 | 0.2123 | 0.1338 |
| S | 0.0169 | 0.0460 | 0.0114 | 0.0059 | 0.0043 |
| E | 0.2311 | 0.5144 | 0.2547 | 0.1076 | 0.0478 |
| T | 0.1462 | 0.3790 | 0.1535 | 0.0398 | 0.0125 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7404 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0261 | 0.0201 | 0.0320 |
| ΔR²(T | L, S, E) | 0.0125 | 0.0089 | 0.0163 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.5213 | 0.4616 | 0.5811 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9359 | 0.006696 | 0.004769 | 0.008583 | 0.0005 | 0.8553 | 0.8614 | 0.006142 | 265 | 212 | 0.01718 |
| T over L+S+E | 0.9464 | 0.9494 | 0.003041 | 0.00189 | 0.004243 | 0.0005 | 0.8772 | 0.8799 | 0.002781 | 158 | 134 | 0.1782 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mberter2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberter2_Mean
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
| L | 0.3424 | 0.6594 | 0.3738 | 0.2061 | 0.1304 |
| S | 0.0167 | 0.0460 | 0.0111 | 0.0057 | 0.0041 |
| E | 0.2285 | 0.5144 | 0.2501 | 0.1028 | 0.0465 |
| T | 0.1557 | 0.3993 | 0.1636 | 0.0443 | 0.0154 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7433 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0303 | 0.0243 | 0.0369 |
| ΔR²(T | L, S, E) | 0.0154 | 0.0116 | 0.0192 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4931 | 0.4368 | 0.5521 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9373 | 0.008166 | 0.006115 | 0.01028 | 0.0005 | 0.8553 | 0.8657 | 0.01043 | 303 | 213 | 8.595e-05 |
| T over L+S+E | 0.9464 | 0.9504 | 0.004048 | 0.002778 | 0.005358 | 0.0005 | 0.8772 | 0.8795 | 0.002318 | 171 | 151 | 0.2897 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mberter3

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberter3_Mean
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
| L | 0.3427 | 0.6594 | 0.3742 | 0.2067 | 0.1306 |
| S | 0.0166 | 0.0460 | 0.0108 | 0.0056 | 0.0039 |
| E | 0.2287 | 0.5144 | 0.2504 | 0.1032 | 0.0465 |
| T | 0.1554 | 0.3985 | 0.1633 | 0.0444 | 0.0155 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7434 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0304 | 0.0238 | 0.0365 |
| ΔR²(T | L, S, E) | 0.0155 | 0.0117 | 0.0192 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4898 | 0.4328 | 0.5470 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9371 | 0.007903 | 0.005809 | 0.009977 | 0.0005 | 0.8553 | 0.8633 | 0.007996 | 283 | 214 | 0.002254 |
| T over L+S+E | 0.9464 | 0.9504 | 0.003995 | 0.002646 | 0.005291 | 0.0005 | 0.8772 | 0.8811 | 0.00394 | 173 | 139 | 0.06155 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: mberter4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_mberter4_Mean
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
| L | 0.3406 | 0.6594 | 0.3716 | 0.2034 | 0.1281 |
| S | 0.0165 | 0.0460 | 0.0107 | 0.0055 | 0.0039 |
| E | 0.2274 | 0.5144 | 0.2484 | 0.1010 | 0.0455 |
| T | 0.1600 | 0.4083 | 0.1684 | 0.0467 | 0.0166 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7445 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0537 | 0.0690 |
| ΔR²(T | L, S) | 0.0325 | 0.0253 | 0.0391 |
| ΔR²(T | L, S, E) | 0.0166 | 0.0122 | 0.0207 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.4896 | 0.4304 | 0.5463 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9292 | 0.9464 | 0.01721 | 0.01455 | 0.02011 | 0.0005 | 0.8553 | 0.8772 | 0.0219 | 417 | 228 | 8.947e-14 |
| T over L+S | 0.9292 | 0.9379 | 0.008723 | 0.006519 | 0.01086 | 0.0005 | 0.8553 | 0.8651 | 0.009851 | 308 | 223 | 0.0002598 |
| T over L+S+E | 0.9464 | 0.9508 | 0.004375 | 0.003042 | 0.005756 | 0.0005 | 0.8772 | 0.8796 | 0.002434 | 177 | 156 | 0.2731 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| mberter0 | 8629 | 0.6665 | 0.0614 | 0.0318 | 0.0162 | 0.4904 | 0.4319 | 0.5460 | 0.0172 | 0.0042 |
| mberter1 | 8629 | 0.6665 | 0.0614 | 0.0261 | 0.0125 | 0.5213 | 0.4616 | 0.5811 | 0.0172 | 0.0030 |
| mberter2 | 8629 | 0.6665 | 0.0614 | 0.0303 | 0.0154 | 0.4931 | 0.4368 | 0.5521 | 0.0172 | 0.0040 |
| mberter3 | 8629 | 0.6665 | 0.0614 | 0.0304 | 0.0155 | 0.4898 | 0.4328 | 0.5470 | 0.0172 | 0.0040 |
| mberter4 | 8629 | 0.6665 | 0.0614 | 0.0325 | 0.0166 | 0.4896 | 0.4304 | 0.5463 | 0.0172 | 0.0044 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| mberter0: E over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter0: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberter0: T over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter0: T over L+S (McNemar) | 1.113e-05 | 5.564e-05 | yes |
| mberter0: T over L+S+E (AUC) | 0.0005 | 0.0006522 | yes |
| mberter0: T over L+S+E (McNemar) | 0.09492 | 0.1055 | no |
| mberter1: E over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter1: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberter1: T over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter1: T over L+S (McNemar) | 0.01718 | 0.02061 | yes |
| mberter1: T over L+S+E (AUC) | 0.0005 | 0.0006522 | yes |
| mberter1: T over L+S+E (McNemar) | 0.1782 | 0.1909 | no |
| mberter2: E over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter2: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberter2: T over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter2: T over L+S (McNemar) | 8.595e-05 | 0.0003683 | yes |
| mberter2: T over L+S+E (AUC) | 0.0005 | 0.0006522 | yes |
| mberter2: T over L+S+E (McNemar) | 0.2897 | 0.2897 | no |
| mberter3: E over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter3: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberter3: T over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter3: T over L+S (McNemar) | 0.002254 | 0.002818 | yes |
| mberter3: T over L+S+E (AUC) | 0.0005 | 0.0006522 | yes |
| mberter3: T over L+S+E (McNemar) | 0.06155 | 0.07102 | no |
| mberter4: E over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter4: E over L+S (McNemar) | 8.947e-14 | 5.368e-13 | yes |
| mberter4: T over L+S (AUC) | 0.0005 | 0.0006522 | yes |
| mberter4: T over L+S (McNemar) | 0.0002598 | 0.0006522 | yes |
| mberter4: T over L+S+E (AUC) | 0.0005 | 0.0006522 | yes |
| mberter4: T over L+S+E (McNemar) | 0.2731 | 0.2825 | no |
