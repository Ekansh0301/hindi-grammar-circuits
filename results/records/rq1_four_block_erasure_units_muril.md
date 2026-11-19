# rq1_four_block_erasure_units_muril

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 09:46 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 6.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu4_s0.csv"], "tag": "rq1_four_block_erasure_units_muril", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_murileu4_s0.csv --tag rq1_four_block_erasure_units_muril` |


- **pairs with L, S and unit features**: 8,923

## model: murileu0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_murileu0_Mean
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


## model: murileu1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_murileu1_Mean
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
| L+E+T | 5 | 2.0 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.2932 | 0.6594 | 0.3191 | 0.1311 | 0.0632 |
| S | 0.0151 | 0.0460 | 0.0074 | 0.0039 | 0.0030 |
| E | 0.2066 | 0.5144 | 0.2142 | 0.0646 | 0.0331 |
| T | 0.2687 | 0.6187 | 0.2887 | 0.1118 | 0.0557 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7836 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0840 | 0.0752 | 0.0939 |
| ΔR²(T | L, S, E) | 0.0557 | 0.0479 | 0.0650 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3373 | 0.2904 | 0.3803 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9532 | 0.0239 | 0.02092 | 0.02701 | 0.0005 | 0.8559 | 0.882 | 0.02619 | 465 | 239 | 1.189e-17 |
| T over L+S+E | 0.9464 | 0.962 | 0.01558 | 0.01335 | 0.01797 | 0.0005 | 0.8778 | 0.8924 | 0.0146 | 323 | 197 | 3.636e-08 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: murileu2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_murileu2_Mean
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
| L+E+T | 5 | 2.0 |
| S+E+T | 5 | 4.4 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.2840 | 0.6594 | 0.3085 | 0.1166 | 0.0514 |
| S | 0.0148 | 0.0460 | 0.0072 | 0.0034 | 0.0026 |
| E | 0.1999 | 0.5144 | 0.2054 | 0.0535 | 0.0265 |
| T | 0.2905 | 0.6633 | 0.3137 | 0.1237 | 0.0614 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7892 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0962 | 0.0866 | 0.1061 |
| ΔR²(T | L, S, E) | 0.0614 | 0.0549 | 0.0690 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3625 | 0.3227 | 0.4053 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9567 | 0.02744 | 0.02428 | 0.03077 | 0.0005 | 0.8559 | 0.8852 | 0.02932 | 513 | 260 | 5.891e-20 |
| T over L+S+E | 0.9464 | 0.9636 | 0.0172 | 0.01481 | 0.01957 | 0.0005 | 0.8778 | 0.8943 | 0.01657 | 358 | 215 | 2.487e-09 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: murileu4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_murileu4_Mean
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
| L | 0.2933 | 0.6594 | 0.3192 | 0.1311 | 0.0635 |
| S | 0.0146 | 0.0460 | 0.0072 | 0.0031 | 0.0021 |
| E | 0.2050 | 0.5144 | 0.2133 | 0.0624 | 0.0302 |
| T | 0.2713 | 0.6231 | 0.2920 | 0.1137 | 0.0564 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7842 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0876 | 0.0796 | 0.0977 |
| ΔR²(T | L, S, E) | 0.0564 | 0.0497 | 0.0655 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3569 | 0.3150 | 0.4010 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9546 | 0.02534 | 0.02232 | 0.02847 | 0.0005 | 0.8559 | 0.887 | 0.03117 | 492 | 223 | 3.483e-24 |
| T over L+S+E | 0.9464 | 0.9623 | 0.01587 | 0.01356 | 0.01821 | 0.0005 | 0.8778 | 0.8966 | 0.01889 | 339 | 176 | 6.09e-13 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| murileu0 | 8630 | 0.6664 | 0.0614 | 0.0867 | 0.0557 | 0.3570 | 0.3122 | 0.3998 | 0.0171 | 0.0157 |
| murileu1 | 8630 | 0.6664 | 0.0614 | 0.0840 | 0.0557 | 0.3373 | 0.2904 | 0.3803 | 0.0171 | 0.0156 |
| murileu2 | 8630 | 0.6664 | 0.0614 | 0.0962 | 0.0614 | 0.3625 | 0.3227 | 0.4053 | 0.0171 | 0.0172 |
| murileu4 | 8630 | 0.6664 | 0.0614 | 0.0876 | 0.0564 | 0.3569 | 0.3150 | 0.4010 | 0.0171 | 0.0159 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| murileu0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu0: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| murileu0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu0: T over L+S (McNemar) | 4.122e-24 | 4.947e-23 | yes |
| murileu0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| murileu0: T over L+S+E (McNemar) | 5.995e-11 | 1.439e-10 | yes |
| murileu1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu1: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| murileu1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu1: T over L+S (McNemar) | 1.189e-17 | 7.137e-17 | yes |
| murileu1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| murileu1: T over L+S+E (McNemar) | 3.636e-08 | 7.272e-08 | yes |
| murileu2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu2: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| murileu2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu2: T over L+S (McNemar) | 5.891e-20 | 4.713e-19 | yes |
| murileu2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| murileu2: T over L+S+E (McNemar) | 2.487e-09 | 5.426e-09 | yes |
| murileu4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu4: E over L+S (McNemar) | 7.46e-14 | 2.238e-13 | yes |
| murileu4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| murileu4: T over L+S (McNemar) | 3.483e-24 | 4.947e-23 | yes |
| murileu4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| murileu4: T over L+S+E (McNemar) | 6.09e-13 | 1.624e-12 | yes |
