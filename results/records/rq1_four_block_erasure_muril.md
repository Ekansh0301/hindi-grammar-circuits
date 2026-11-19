# rq1_four_block_erasure_muril

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 22:53 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 8.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler3_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler4_s0.csv"], "tag": "rq1_four_block_erasure_muril", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler3_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure/t_muriler4_s0.csv --tag rq1_four_block_erasure_muril` |


- **pairs with L, S and unit features**: 8,923

## model: muriler0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_muriler0_Mean
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
| L | 0.2940 | 0.6594 | 0.3199 | 0.1322 | 0.0644 |
| S | 0.0147 | 0.0460 | 0.0072 | 0.0033 | 0.0022 |
| E | 0.2054 | 0.5144 | 0.2137 | 0.0630 | 0.0305 |
| T | 0.2695 | 0.6197 | 0.2900 | 0.1126 | 0.0557 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7836 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0867 | 0.0790 | 0.0971 |
| ΔR²(T | L, S, E) | 0.0557 | 0.0492 | 0.0644 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3570 | 0.3122 | 0.3998 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9544 | 0.02508 | 0.0221 | 0.02823 | 0.0005 | 0.8559 | 0.8869 | 0.03105 | 490 | 222 | 4.122e-24 |
| T over L+S+E | 0.9464 | 0.9621 | 0.0157 | 0.01349 | 0.01807 | 0.0005 | 0.8778 | 0.8947 | 0.01692 | 322 | 176 | 5.995e-11 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: muriler1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_muriler1_Mean
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
| L+E+T | 5 | 2.0 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.2891 | 0.6594 | 0.3142 | 0.1246 | 0.0584 |
| S | 0.0147 | 0.0460 | 0.0072 | 0.0033 | 0.0024 |
| E | 0.2035 | 0.5144 | 0.2100 | 0.0593 | 0.0303 |
| T | 0.2771 | 0.6377 | 0.2985 | 0.1155 | 0.0566 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7844 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0877 | 0.0785 | 0.0977 |
| ΔR²(T | L, S, E) | 0.0566 | 0.0485 | 0.0651 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3550 | 0.3129 | 0.3980 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9548 | 0.02548 | 0.02253 | 0.02863 | 0.0005 | 0.8559 | 0.8864 | 0.03059 | 493 | 229 | 4.145e-23 |
| T over L+S+E | 0.9464 | 0.9624 | 0.01602 | 0.01371 | 0.01836 | 0.0005 | 0.8778 | 0.8954 | 0.01761 | 330 | 178 | 1.485e-11 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: muriler2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_muriler2_Mean
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
| L+T | 4 | 1.9 |
| S+E | 4 | 4.4 |
| S+T | 4 | 4.4 |
| E+T | 2 | 1.4 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 2.1 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.2838 | 0.6594 | 0.3084 | 0.1163 | 0.0510 |
| S | 0.0147 | 0.0460 | 0.0071 | 0.0033 | 0.0023 |
| E | 0.2005 | 0.5144 | 0.2058 | 0.0542 | 0.0275 |
| T | 0.2920 | 0.6646 | 0.3152 | 0.1254 | 0.0631 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7909 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0970 | 0.0879 | 0.1089 |
| ΔR²(T | L, S, E) | 0.0631 | 0.0558 | 0.0725 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3497 | 0.3072 | 0.3892 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9572 | 0.02789 | 0.02464 | 0.03136 | 0.0005 | 0.8559 | 0.8885 | 0.03268 | 518 | 236 | 3.888e-25 |
| T over L+S+E | 0.9464 | 0.9639 | 0.01753 | 0.01516 | 0.02009 | 0.0005 | 0.8778 | 0.8972 | 0.01947 | 356 | 188 | 5.308e-13 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: muriler3

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_muriler3_Mean
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
| L | 0.2937 | 0.6594 | 0.3196 | 0.1318 | 0.0640 |
| S | 0.0149 | 0.0460 | 0.0074 | 0.0035 | 0.0025 |
| E | 0.2054 | 0.5144 | 0.2135 | 0.0629 | 0.0306 |
| T | 0.2667 | 0.6172 | 0.2871 | 0.1096 | 0.0527 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7806 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0836 | 0.0754 | 0.0937 |
| ΔR²(T | L, S, E) | 0.0527 | 0.0462 | 0.0609 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3689 | 0.3235 | 0.4108 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9536 | 0.02432 | 0.02143 | 0.02741 | 0.0005 | 0.8559 | 0.8853 | 0.02943 | 470 | 216 | 1.462e-22 |
| T over L+S+E | 0.9464 | 0.9612 | 0.01478 | 0.01261 | 0.01701 | 0.0005 | 0.8778 | 0.8952 | 0.0175 | 322 | 171 | 9.868e-12 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: muriler4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_muriler4_Mean
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
| L | 0.2957 | 0.6594 | 0.3216 | 0.1347 | 0.0670 |
| S | 0.0147 | 0.0460 | 0.0073 | 0.0033 | 0.0023 |
| E | 0.2061 | 0.5144 | 0.2148 | 0.0643 | 0.0310 |
| T | 0.2658 | 0.6127 | 0.2858 | 0.1103 | 0.0544 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7823 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0848 | 0.0763 | 0.0951 |
| ΔR²(T | L, S, E) | 0.0544 | 0.0482 | 0.0629 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3583 | 0.3168 | 0.4031 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9538 | 0.02447 | 0.0216 | 0.02754 | 0.0005 | 0.8559 | 0.8851 | 0.0292 | 475 | 223 | 7.485e-22 |
| T over L+S+E | 0.9464 | 0.9618 | 0.01536 | 0.0132 | 0.01765 | 0.0005 | 0.8778 | 0.8959 | 0.01819 | 325 | 168 | 1.385e-12 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| muriler0 | 8630 | 0.6664 | 0.0614 | 0.0867 | 0.0557 | 0.3570 | 0.3122 | 0.3998 | 0.0171 | 0.0157 |
| muriler1 | 8630 | 0.6664 | 0.0614 | 0.0877 | 0.0566 | 0.3550 | 0.3129 | 0.3980 | 0.0171 | 0.0160 |
| muriler2 | 8630 | 0.6664 | 0.0614 | 0.0970 | 0.0631 | 0.3497 | 0.3072 | 0.3892 | 0.0171 | 0.0175 |
| muriler3 | 8630 | 0.6664 | 0.0614 | 0.0836 | 0.0527 | 0.3689 | 0.3235 | 0.4108 | 0.0171 | 0.0148 |
| muriler4 | 8630 | 0.6664 | 0.0614 | 0.0848 | 0.0544 | 0.3583 | 0.3168 | 0.4031 | 0.0171 | 0.0154 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| muriler0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler0: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| muriler0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler0: T over L+S (McNemar) | 4.122e-24 | 6.183e-23 | yes |
| muriler0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| muriler0: T over L+S+E (McNemar) | 5.995e-11 | 1.199e-10 | yes |
| muriler1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler1: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| muriler1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler1: T over L+S (McNemar) | 4.145e-23 | 4.145e-22 | yes |
| muriler1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| muriler1: T over L+S+E (McNemar) | 1.485e-11 | 3.182e-11 | yes |
| muriler2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler2: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| muriler2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler2: T over L+S (McNemar) | 3.888e-25 | 1.166e-23 | yes |
| muriler2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| muriler2: T over L+S+E (McNemar) | 5.308e-13 | 1.448e-12 | yes |
| muriler3: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler3: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| muriler3: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler3: T over L+S (McNemar) | 1.462e-22 | 1.096e-21 | yes |
| muriler3: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| muriler3: T over L+S+E (McNemar) | 9.868e-12 | 2.277e-11 | yes |
| muriler4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler4: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| muriler4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| muriler4: T over L+S (McNemar) | 7.485e-22 | 4.491e-21 | yes |
| muriler4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| muriler4: T over L+S+E (McNemar) | 1.385e-12 | 3.463e-12 | yes |
