# mi_paper_cues_muril

_P5: cue strata of the word-order circuit (local, existing outputs)_

| provenance | |
|---|---|
| run (UTC) | 2026-11-17 23:06 |
| script | `mi_paper_cues.py` (sha256 `d07dd40d1a3c752e`) |
| host | TARDIS (Linux) |
| duration | 0.0 min |
| versions | python 3.14.4, pandas 2.3.3, numpy 2.3.5, sklearn 1.7.2, gpu NVIDIA GeForce GTX 1650 |
| args | `{"boot": 2000, "min_gap": 0.05, "min_stratum": 40, "model": "muril"}` |
| command | `scripts/mi_paper_cues.py --model muril` |



## Join

- **pairs joined**: 471 of 471, none duplicated
- **documents**: 334
- **pairs above the gap floor**: 409 (|gap| > 0.05 bits)
- **missing values**: d_kenlm_mean_filt 0, d_ngram2_mean_filt 0, d_dep_total 0, d_is_inv_norm 19, d_casemarker_mean 0

## Overall share restored (whole set, for plausibility against follow-up 1)

- **10 heads**: 0.710 [0.669, 0.750]
- **MLP 1**: 0.567 [0.544, 0.594]
- **MLP 2**: 0.482 [0.458, 0.508]
- **MLP 3**: 0.440 [0.414, 0.469]
- **MLP 4**: 0.362 [0.334, 0.394]
- **MLP 5**: 0.232 [0.206, 0.261]
- **5 MLPs jointly**: 0.965 [0.939, 0.992]

## Sign check (before any stratification)

Convention. The d_ features are reference minus variant (the thesis scripts define per-sentence differences as reference minus variant, e.g. rq1_late_ablation: d = ref_Mean - var_Mean; the surprisal-type cues d_kenlm and d_ngram2 are n-gram surprisal differences). Reference is the written sentence, so a NEGATIVE value of d_kenlm_mean_filt or d_ngram2_mean_filt means the written sentence is less surprising to the n-gram model, i.e. the cue favours the written order. The pair's gap is f_clean - f_corrupt, positive when the model prefers the written order. If the convention holds, the Spearman of these cues with the gap is NEGATIVE. The check below tests this on the data; the script aborts if the lexical cue shows the opposite sign.


| cue | n | Spearman with gap | p |
|---|---|---|---|
| d_kenlm_mean_filt | 471 | -0.4989 | 5.148e-31 |
| d_ngram2_mean_filt | 471 | -0.3399 | 3.342e-14 |
| d_dep_total | 471 | -0.1115 | 0.01544 |
| d_is_inv_norm | 452 | -0.04224 | 0.3703 |
| d_casemarker_mean | 471 | 0.04745 | 0.3041 |
| kendall | 471 | 0.3516 | 3.756e-15 |

Result: lexical cues are negatively related to the gap, consistent with reference minus variant surprisal. Direction used: d < 0 favours the written order (agrees), d > 0 favours the reordered one (disagrees). For d_dep_total (dependency distance, smaller is easier) and d_is_inv_norm, the same reference minus variant convention applies; their correlations with the gap are descriptive and signs are read from the table above, not used for strata.


## Strata by d_kenlm_mean_filt

- **excluded (cue 0 or missing)**: 1

| stratum | pairs | docs | above floor | prefers written | mean gap (bits) | 10 heads share | 5 MLPs share |
|---|---|---|---|---|---|---|---|
| agrees (cue favours written) | 410 | 303 | 358 | 82.7% | 0.683 | 0.704 [0.667, 0.744] | 0.957 [0.931, 0.983] |
| disagrees (cue favours reordered) | 60 | 56 | 50 | 61.7% | 0.160 | 0.904 [0.536, 2.469] | 1.177 [0.956, 2.360] |


| quantity | disagrees minus agrees | 95% doc-bootstrap interval |
|---|---|---|
| 10 heads | 0.200 | [-0.170, 1.759] |
| 5 MLPs jointly | 0.219 | [-0.003, 1.416] |

**DECISION (PRIMARY, d_kenlm_mean_filt, muril): INCONCLUSIVE** (strata above floor: agrees 358, disagrees 50; band +-0.1)


## Strata by d_ngram2_mean_filt

- **excluded (cue 0 or missing)**: 1

| stratum | pairs | docs | above floor | prefers written | mean gap (bits) | 10 heads share | 5 MLPs share |
|---|---|---|---|---|---|---|---|
| agrees (cue favours written) | 375 | 287 | 335 | 81.3% | 0.672 | 0.702 [0.662, 0.746] | 0.950 [0.922, 0.980] |
| disagrees (cue favours reordered) | 95 | 89 | 73 | 74.7% | 0.397 | 0.765 [0.655, 0.885] | 1.061 [0.974, 1.176] |


| quantity | disagrees minus agrees | 95% doc-bootstrap interval |
|---|---|---|
| 10 heads | 0.062 | [-0.059, 0.192] |
| 5 MLPs jointly | 0.111 | [0.017, 0.231] |

**DECISION (second analysis, d_ngram2_mean_filt, muril): CUE-DEPENDENT** (strata above floor: agrees 335, disagrees 73; band +-0.1)


## Descriptive: Spearman with the gap and with the 5 MLPs' joint effect (bits)


| cue | n | rho gap | p | rho MLP effect | p |
|---|---|---|---|---|---|
| d_kenlm_mean_filt | 471 | -0.4989 | 5.148e-31 | -0.4786 | 2.482e-28 |
| d_ngram2_mean_filt | 471 | -0.3399 | 3.342e-14 | -0.3201 | 1.11e-12 |
| d_dep_total | 471 | -0.1115 | 0.01544 | -0.1014 | 0.02771 |
| d_is_inv_norm | 452 | -0.04224 | 0.3703 | -0.04171 | 0.3763 |
| d_casemarker_mean | 471 | 0.04745 | 0.3041 | 0.05022 | 0.2768 |
| kendall | 471 | 0.3516 | 3.756e-15 | 0.3761 | 2.833e-17 |


## Descriptive: OLS of the gap on standardised cue families (not a test)

- **pairs in the regression**: 452
- **R^2**: 0.329

| term | coefficient (bits per SD) |
|---|---|
| intercept | 0.598 |
| d_kenlm_mean_filt | -0.525 |
| d_dep_total | -0.073 |
| d_is_inv_norm | -0.040 |
| d_casemarker_mean | 0.076 |


> Descriptive only: the cues are correlated with each other and with reordering size, and the gap is not a response with a known noise model.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `cues_muril.csv` | 165,345 | `ed4600d1c196adb2` | per-pair cues, gap, set effects (bits), stratum |
