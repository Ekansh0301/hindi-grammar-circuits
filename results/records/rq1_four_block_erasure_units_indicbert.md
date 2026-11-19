# rq1_four_block_erasure_units_indicbert

_Four-block decomposition L, S, E, T: how much of transformer surprisal's unique contribution a structure-only order model also provides._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 09:57 |
| script | `rq1_four_block.py` (sha256 `3ed4353943d50c57`) |
| host | gnode (Linux) |
| duration | 6.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"acc": false, "bootstrap": 2000, "cluster": "reference", "e_cols": ["d_syn_order"], "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "keep": null, "l_trigram": "d_kenlm_mean_filt", "moved_stratum": null, "ngram": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_ngram.csv", "order_classes": null, "s_extra_cols": null, "s_extra_file": null, "sample": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "sev_q": null, "share_bootstrap": 200, "t_features": ["<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu0_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu1_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu2_s0.csv", "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu4_s0.csv"], "tag": "rq1_four_block_erasure_units_indicbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_four_block.py --t-features <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu0_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu1_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu2_s0.csv <earlier-repo>/sets/set1/Results_Checks/concept_erasure_units/t_indicberteu4_s0.csv --tag rq1_four_block_erasure_units_indicbert` |


- **pairs with L, S and unit features**: 8,923

## model: indicberteu0

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberteu0_Mean
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


## model: indicberteu1

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberteu1_Mean
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
| L | 0.3075 | 0.6594 | 0.3376 | 0.1544 | 0.0788 |
| S | 0.0162 | 0.0460 | 0.0091 | 0.0055 | 0.0044 |
| E | 0.2150 | 0.5144 | 0.2284 | 0.0798 | 0.0376 |
| T | 0.2433 | 0.5556 | 0.2600 | 0.1032 | 0.0542 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7821 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0780 | 0.0693 | 0.0866 |
| ΔR²(T | L, S, E) | 0.0542 | 0.0470 | 0.0609 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3052 | 0.2568 | 0.3550 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9519 | 0.02257 | 0.01938 | 0.02569 | 0.0005 | 0.8559 | 0.8846 | 0.02874 | 505 | 257 | 1.743e-19 |
| T over L+S+E | 0.9464 | 0.9614 | 0.01497 | 0.01272 | 0.01734 | 0.0005 | 0.8778 | 0.8946 | 0.0168 | 349 | 204 | 7.365e-10 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberteu2

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberteu2_Mean
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
| S+E+T | 5 | 4.5 |
| L+S+E+T | 8 | 4.5 |


### Dominance


| block | general dominance | R² alone | k=1 | k=2 | k=3 |
|---|---|---|---|---|---|
| L | 0.3034 | 0.6594 | 0.3307 | 0.1469 | 0.0765 |
| S | 0.0156 | 0.0460 | 0.0083 | 0.0046 | 0.0036 |
| E | 0.2108 | 0.5144 | 0.2216 | 0.0722 | 0.0348 |
| T | 0.2509 | 0.5785 | 0.2685 | 0.1037 | 0.0528 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7806 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0794 | 0.0716 | 0.0891 |
| ΔR²(T | L, S, E) | 0.0528 | 0.0459 | 0.0599 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3354 | 0.2884 | 0.3807 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9519 | 0.02258 | 0.01944 | 0.02566 | 0.0005 | 0.8559 | 0.8809 | 0.02503 | 492 | 276 | 5.744e-15 |
| T over L+S+E | 0.9464 | 0.9609 | 0.01445 | 0.01218 | 0.01674 | 0.0005 | 0.8778 | 0.8908 | 0.01309 | 352 | 239 | 3.83e-06 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## model: indicberteu4

- **L**: d_kenlm_mean_filt, d_semantic_sim, d_same_case_bigram
- **S**: d_dep_mean, d_dlt_mean, d_is_inv_norm
- **E**: d_syn_order
- **T**: t_indicberteu4_Mean
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
| L | 0.3154 | 0.6594 | 0.3448 | 0.1659 | 0.0915 |
| S | 0.0158 | 0.0460 | 0.0086 | 0.0049 | 0.0038 |
| E | 0.2163 | 0.5144 | 0.2313 | 0.0825 | 0.0369 |
| T | 0.2279 | 0.5287 | 0.2428 | 0.0927 | 0.0475 |


| quantity | estimate | 95% low | 95% high |
|---|---|---|---|
| full-model R² | 0.7754 | nan | nan |
| ΔR²(E | L, S) | 0.0614 | 0.0538 | 0.0691 |
| ΔR²(T | L, S) | 0.0721 | 0.0639 | 0.0810 |
| ΔR²(T | L, S, E) | 0.0475 | 0.0411 | 0.0537 |
| absorbed share 1 − ΔR²(T|L,S,E)/ΔR²(T|L,S) | 0.3406 | 0.2922 | 0.3898 |

Intervals: 200 bootstrap replicates over references.


### Out-of-fold AUC and per-pair accuracy (grouped 5-fold by reference)


| comparison | AUC without | AUC with | ΔAUC | 95% low | 95% high | bootstrap p | accuracy without | accuracy with | Δaccuracy | McNemar b | c | McNemar p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E over L+S | 0.9293 | 0.9464 | 0.01709 | 0.01431 | 0.01981 | 0.0005 | 0.8559 | 0.8778 | 0.0219 | 415 | 226 | 7.46e-14 |
| T over L+S | 0.9293 | 0.9496 | 0.02031 | 0.01735 | 0.02327 | 0.0005 | 0.8559 | 0.878 | 0.02213 | 455 | 264 | 1.024e-12 |
| T over L+S+E | 0.9464 | 0.9593 | 0.01286 | 0.01078 | 0.01508 | 0.0005 | 0.8778 | 0.8912 | 0.01344 | 326 | 210 | 6.169e-07 |

Accuracy is per pair -- is the reference scored above its own variant -- which is what the task asks and what McNemar tests. AUC is taken over every positive row against every negative row, including rows from different pairs, so it also rewards a predictor for having a consistent sign; read the two together, and see `rq1_null_calibration_permute.md` for how far apart they can be pushed.


## Summary


| model | pairs | R²(L+S) | ΔR²(E|L,S) | ΔR²(T|L,S) | ΔR²(T|L,S,E) | absorbed share | 95% low | 95% high | ΔAUC E over L+S | ΔAUC T over L+S+E |
|---|---|---|---|---|---|---|---|---|---|---|
| indicberteu0 | 8630 | 0.6664 | 0.0614 | 0.0727 | 0.0482 | 0.3380 | 0.2912 | 0.3850 | 0.0171 | 0.0131 |
| indicberteu1 | 8630 | 0.6664 | 0.0614 | 0.0780 | 0.0542 | 0.3052 | 0.2568 | 0.3550 | 0.0171 | 0.0150 |
| indicberteu2 | 8630 | 0.6664 | 0.0614 | 0.0794 | 0.0528 | 0.3354 | 0.2884 | 0.3807 | 0.0171 | 0.0145 |
| indicberteu4 | 8630 | 0.6664 | 0.0614 | 0.0721 | 0.0475 | 0.3406 | 0.2922 | 0.3898 | 0.0171 | 0.0129 |


## Benjamini-Hochberg across every test in this run


| test | raw p | BH p | significant at 0.05 |
|---|---|---|---|
| indicberteu0: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu0: E over L+S (McNemar) | 7.46e-14 | 2.984e-13 | yes |
| indicberteu0: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu0: T over L+S (McNemar) | 1.71e-11 | 5.13e-11 | yes |
| indicberteu0: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu0: T over L+S+E (McNemar) | 2.478e-06 | 5.407e-06 | yes |
| indicberteu1: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu1: E over L+S (McNemar) | 7.46e-14 | 2.984e-13 | yes |
| indicberteu1: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu1: T over L+S (McNemar) | 1.743e-19 | 4.184e-18 | yes |
| indicberteu1: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu1: T over L+S+E (McNemar) | 7.365e-10 | 1.964e-09 | yes |
| indicberteu2: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu2: E over L+S (McNemar) | 7.46e-14 | 2.984e-13 | yes |
| indicberteu2: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu2: T over L+S (McNemar) | 5.744e-15 | 6.893e-14 | yes |
| indicberteu2: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu2: T over L+S+E (McNemar) | 3.83e-06 | 7.661e-06 | yes |
| indicberteu4: E over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu4: E over L+S (McNemar) | 7.46e-14 | 2.984e-13 | yes |
| indicberteu4: T over L+S (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu4: T over L+S (McNemar) | 1.024e-12 | 3.51e-12 | yes |
| indicberteu4: T over L+S+E (AUC) | 0.0005 | 0.0005 | yes |
| indicberteu4: T over L+S+E (McNemar) | 6.169e-07 | 1.481e-06 | yes |
