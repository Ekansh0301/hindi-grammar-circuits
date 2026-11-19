# rq1_four_block_erasure_units_xlmrlarge

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 14:31 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 6.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu4_s0.csv"], "tag": "rq1_four_block_erasure_units_xlmrlarge", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_xlmrlargeeu4_s0.csv --tag rq1_four_block_erasure_units_xlmrlarge` |


- **pairs with L, S and unit features**: 8,923

## model: xlmrlargeeu0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeeu0_Mean
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


## model: xlmrlargeeu1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeeu1_Mean
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
| E+T | 2 | 1.3 |
| L+S+E | 7 | 4.4 |
| L+S+T | 7 | 4.4 |
| L+E+T | 5 | 1.9 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.4 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3189 | 0.6594 | 0.3477 | 0.1706 | 0.0980 |
| S | 0.0164 | 0.0460 | 0.0094 | 0.0056 | 0.0045 |
| E | 0.2182 | 0.5144 | 0.2332 | 0.0852 | 0.0401 |
| T | 0.2077 | 0.5013 | 0.2210 | 0.0751 | 0.0334 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7612 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0547 | 0.0476 | 0.0638 |
| ΔR²(T | L, S, E) | 0.0334 | 0.0281 | 0.0396 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3893 | 0.3397 | 0.4433 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9456 | 0.01624 | 0.01357 | 0.01892 | 0.0005 | 0.8559 | 0.8754 | 0.01958 | 372 | 203 | 1.708e-12 |
| T over L+S+E | 0.9464 | 0.9559 | 0.009474 | 0.007568 | 0.01136 | 0.0005 | 0.8778 | 0.8866 | 0.008806 | 247 | 171 | 0.0002355 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeeu2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeeu2_Mean
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
| L | 0.3002 | 0.6594 | 0.3262 | 0.1416 | 0.0738 |
| S | 0.0150 | 0.0460 | 0.0077 | 0.0038 | 0.0027 |
| E | 0.2084 | 0.5144 | 0.2178 | 0.0681 | 0.0335 |
| T | 0.2471 | 0.5845 | 0.2655 | 0.0956 | 0.0430 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7709 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0709 | 0.0626 | 0.0817 |
| ΔR²(T | L, S, E) | 0.0430 | 0.0366 | 0.0509 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3936 | 0.3482 | 0.4419 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9506 | 0.02127 | 0.01836 | 0.02435 | 0.0005 | 0.8559 | 0.8816 | 0.02572 | 433 | 211 | 1.408e-18 |
| T over L+S+E | 0.9464 | 0.9588 | 0.01236 | 0.01029 | 0.01442 | 0.0005 | 0.8778 | 0.8898 | 0.01205 | 289 | 185 | 2.044e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: xlmrlargeeu4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_xlmrlargeeu4_Mean
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
| L | 0.3030 | 0.6594 | 0.3296 | 0.1460 | 0.0771 |
| S | 0.0151 | 0.0460 | 0.0079 | 0.0038 | 0.0025 |
| E | 0.2088 | 0.5144 | 0.2195 | 0.0691 | 0.0321 |
| T | 0.2538 | 0.5856 | 0.2720 | 0.1048 | 0.0528 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7806 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0821 | 0.0751 | 0.0922 |
| ΔR²(T | L, S, E) | 0.0528 | 0.0471 | 0.0620 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3573 | 0.3109 | 0.4001 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9536 | 0.02431 | 0.02133 | 0.02751 | 0.0005 | 0.8559 | 0.8832 | 0.02735 | 467 | 231 | 2.673e-19 |
| T over L+S+E | 0.9464 | 0.9616 | 0.01522 | 0.01302 | 0.01754 | 0.0005 | 0.8778 | 0.8936 | 0.01587 | 334 | 197 | 2.956e-09 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| xlmrlargeeu0 | 8630 | 0.6664 | 0.0614 | 0.0838 | 0.0539 | 0.3561 | 0.3103 | 0.3962 | 0.0171 | 0.0154 |
| xlmrlargeeu1 | 8630 | 0.6664 | 0.0614 | 0.0547 | 0.0334 | 0.3893 | 0.3397 | 0.4433 | 0.0171 | 0.0095 |
| xlmrlargeeu2 | 8630 | 0.6664 | 0.0614 | 0.0709 | 0.0430 | 0.3936 | 0.3482 | 0.4419 | 0.0171 | 0.0124 |
| xlmrlargeeu4 | 8630 | 0.6664 | 0.0614 | 0.0821 | 0.0528 | 0.3573 | 0.3109 | 0.4001 | 0.0171 | 0.0152 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| xlmrlargeeu0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu0: E over L+S (McNemar) | 7.46e-14 | 2.558e-13 | yes |
| xlmrlargeeu0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu0: T over L+S (McNemar) | 7.813e-21 | 1.875e-19 | yes |
| xlmrlargeeu0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu0: T over L+S+E (McNemar) | 1.839e-10 | 4.905e-10 | yes |
| xlmrlargeeu1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu1: E over L+S (McNemar) | 7.46e-14 | 2.558e-13 | yes |
| xlmrlargeeu1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu1: T over L+S (McNemar) | 1.708e-12 | 5.123e-12 | yes |
| xlmrlargeeu1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu1: T over L+S+E (McNemar) | 0.0002355 | 0.0004709 | yes |
| xlmrlargeeu2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu2: E over L+S (McNemar) | 7.46e-14 | 2.558e-13 | yes |
| xlmrlargeeu2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu2: T over L+S (McNemar) | 1.408e-18 | 1.127e-17 | yes |
| xlmrlargeeu2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu2: T over L+S+E (McNemar) | 2.044e-06 | 4.459e-06 | yes |
| xlmrlargeeu4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu4: E over L+S (McNemar) | 7.46e-14 | 2.558e-13 | yes |
| xlmrlargeeu4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu4: T over L+S (McNemar) | 2.673e-19 | 3.207e-18 | yes |
| xlmrlargeeu4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| xlmrlargeeu4: T over L+S+E (McNemar) | 2.956e-09 | 7.095e-09 | yes |
