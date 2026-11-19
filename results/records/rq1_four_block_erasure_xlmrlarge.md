# rq1_four_block_erasure_xlmrlarge

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 14:47 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 8.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer3_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer4_s0.csv"], "tag": "rq1_four_block_erasure_xlmrlarge", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer3_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_xlmrlargeer4_s0.csv --tag rq1_four_block_erasure_xlmrlarge` |


- **pairs with L, S and unit features**: 8,923

## model: xlmrlargeer0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeer0_Mean
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
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3041 | 0.6594 | 0.3310 | 0.1477 | 0.0784 |
| S | 0.0151 | 0.0460 | 0.0080 | 0.0038 | 0.0025 |
| E | 0.2089 | 0.5144 | 0.2202 | 0.0696 | 0.0316 |
| T | 0.2537 | 0.5833 | 0.2717 | 0.1057 | 0.0539 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7818 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0838 | 0.0764 | 0.0938 |
| ΔR²(T | L, S, E) | 0.0539 | 0.0488 | 0.0627 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3561 | 0.3103 | 0.3962 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.954 | 0.02473 | 0.02169 | 0.02799 | 0.0005 | 0.8559 | 0.8845 | 0.02862 | 476 | 229 | 7.813e-21 |
| T over L+S+E | 0.9464 | 0.9618 | 0.01544 | 0.01324 | 0.01777 | 0.0005 | 0.8778 | 0.8946 | 0.0168 | 331 | 186 | 1.839e-10 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeer1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeer1_Mean
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
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3033 | 0.6594 | 0.3299 | 0.1464 | 0.0777 |
| S | 0.0151 | 0.0460 | 0.0080 | 0.0038 | 0.0025 |
| E | 0.2087 | 0.5144 | 0.2195 | 0.0690 | 0.0319 |
| T | 0.2540 | 0.5854 | 0.2722 | 0.1052 | 0.0533 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7812 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0828 | 0.0751 | 0.0929 |
| ΔR²(T | L, S, E) | 0.0533 | 0.0480 | 0.0618 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3562 | 0.3120 | 0.3974 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9536 | 0.02431 | 0.02125 | 0.0275 | 0.0005 | 0.8559 | 0.8846 | 0.02874 | 476 | 228 | 5.056e-21 |
| T over L+S+E | 0.9464 | 0.9617 | 0.01526 | 0.01306 | 0.01752 | 0.0005 | 0.8778 | 0.8948 | 0.01703 | 330 | 183 | 8.594e-11 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeer2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeer2_Mean
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
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.2996 | 0.6594 | 0.3266 | 0.1410 | 0.0714 |
| S | 0.0151 | 0.0460 | 0.0079 | 0.0038 | 0.0025 |
| E | 0.2082 | 0.5144 | 0.2183 | 0.0680 | 0.0320 |
| T | 0.2566 | 0.5935 | 0.2758 | 0.1055 | 0.0516 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7794 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0810 | 0.0736 | 0.0921 |
| ΔR²(T | L, S, E) | 0.0516 | 0.0465 | 0.0602 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3635 | 0.3175 | 0.4039 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9532 | 0.02391 | 0.0209 | 0.02704 | 0.0005 | 0.8559 | 0.8841 | 0.02827 | 469 | 225 | 1.145e-20 |
| T over L+S+E | 0.9464 | 0.9611 | 0.01466 | 0.01251 | 0.01692 | 0.0005 | 0.8778 | 0.8946 | 0.0168 | 335 | 190 | 2.546e-10 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeer3

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeer3_Mean
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
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3039 | 0.6594 | 0.3308 | 0.1474 | 0.0780 |
| S | 0.0151 | 0.0460 | 0.0079 | 0.0038 | 0.0025 |
| E | 0.2088 | 0.5144 | 0.2200 | 0.0694 | 0.0313 |
| T | 0.2537 | 0.5838 | 0.2719 | 0.1055 | 0.0536 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7814 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0837 | 0.0760 | 0.0945 |
| ΔR²(T | L, S, E) | 0.0536 | 0.0482 | 0.0622 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3602 | 0.3154 | 0.4000 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.954 | 0.02467 | 0.02165 | 0.02793 | 0.0005 | 0.8559 | 0.8841 | 0.02827 | 471 | 227 | 1.489e-20 |
| T over L+S+E | 0.9464 | 0.9617 | 0.01532 | 0.01313 | 0.01763 | 0.0005 | 0.8778 | 0.8939 | 0.01611 | 325 | 186 | 8.156e-10 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeer4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeer4_Mean
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
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3039 | 0.6594 | 0.3307 | 0.1474 | 0.0782 |
| S | 0.0151 | 0.0460 | 0.0080 | 0.0038 | 0.0025 |
| E | 0.2088 | 0.5144 | 0.2199 | 0.0693 | 0.0314 |
| T | 0.2541 | 0.5843 | 0.2722 | 0.1059 | 0.0540 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7819 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0840 | 0.0764 | 0.0943 |
| ΔR²(T | L, S, E) | 0.0540 | 0.0486 | 0.0630 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3571 | 0.3114 | 0.3963 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9541 | 0.02478 | 0.02177 | 0.02803 | 0.0005 | 0.8559 | 0.8852 | 0.02932 | 474 | 221 | 4.134e-22 |
| T over L+S+E | 0.9464 | 0.9619 | 0.01545 | 0.01325 | 0.01775 | 0.0005 | 0.8778 | 0.8941 | 0.01634 | 324 | 183 | 3.919e-10 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| xlmrlargeer0 | 8630 | 0.6664 | 0.0614 | 0.0838 | 0.0539 | 0.3561 | 0.3103 | 0.3962 | 0.0171 | 0.0154 |
| xlmrlargeer1 | 8630 | 0.6664 | 0.0614 | 0.0828 | 0.0533 | 0.3562 | 0.3120 | 0.3974 | 0.0171 | 0.0153 |
| xlmrlargeer2 | 8630 | 0.6664 | 0.0614 | 0.0810 | 0.0516 | 0.3635 | 0.3175 | 0.4039 | 0.0171 | 0.0147 |
| xlmrlargeer3 | 8630 | 0.6664 | 0.0614 | 0.0837 | 0.0536 | 0.3602 | 0.3154 | 0.4000 | 0.0171 | 0.0153 |
| xlmrlargeer4 | 8630 | 0.6664 | 0.0614 | 0.0840 | 0.0540 | 0.3571 | 0.3114 | 0.3963 | 0.0171 | 0.0155 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| xlmrlargeer0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer0: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| xlmrlargeer0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer0: T over L+S (McNemar) | 7.813e-21 | 7.813e-20 | yes |
| xlmrlargeer0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer0: T over L+S+E (McNemar) | 1.839e-10 | 4.598e-10 | yes |
| xlmrlargeer1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer1: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| xlmrlargeer1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer1: T over L+S (McNemar) | 5.056e-21 | 7.584e-20 | yes |
| xlmrlargeer1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer1: T over L+S+E (McNemar) | 8.594e-11 | 2.344e-10 | yes |
| xlmrlargeer2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer2: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| xlmrlargeer2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer2: T over L+S (McNemar) | 1.145e-20 | 8.589e-20 | yes |
| xlmrlargeer2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer2: T over L+S+E (McNemar) | 2.546e-10 | 5.876e-10 | yes |
| xlmrlargeer3: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer3: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| xlmrlargeer3: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer3: T over L+S (McNemar) | 1.489e-20 | 8.936e-20 | yes |
| xlmrlargeer3: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer3: T over L+S+E (McNemar) | 8.156e-10 | 1.631e-09 | yes |
| xlmrlargeer4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer4: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| xlmrlargeer4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer4: T over L+S (McNemar) | 4.134e-22 | 1.24e-20 | yes |
| xlmrlargeer4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeer4: T over L+S+E (McNemar) | 3.919e-10 | 8.399e-10 | yes |
