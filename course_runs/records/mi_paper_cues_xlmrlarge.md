# mi_paper_cues_xlmrlarge

_P5: cue strata of the word-order circuit (local, existing outputs)_

| provenance | |
|---|---|
| run (UTC) | 2026-11-17 23:06 |
| script | `mi_paper_cues.py` (sha256 `d07dd40d1a3c752e`) |
| host | TARDIS (Linux) |
| duration | 0.0 min |
| versions | python 3.14.4, pandas 2.3.3, numpy 2.3.5, sklearn 1.7.2, gpu NVIDIA GeForce GTX 1650 |
| args | `{"boot": 2000, "min_gap": 0.05, "min_stratum": 40, "model": "xlmrlarge"}` |
| command | `scripts/mi_paper_cues.py --model xlmrlarge` |



## Join

- **pairs joined**: 471 of 471, none duplicated
- **documents**: 334
- **pairs above the gap floor**: 402 (|gap| > 0.05 bits)
- **missing values**: d_kenlm_mean_filt 0, d_ngram2_mean_filt 0, d_dep_total 0, d_is_inv_norm 19, d_casemarker_mean 0

## Overall share restored (whole set, for plausibility against follow-up 1)

- **10 heads**: 0.486 [0.448, 0.524]
- **MLP 1**: 0.366 [0.341, 0.393]
- **MLP 2**: 0.306 [0.281, 0.331]
- **MLP 3**: 0.304 [0.274, 0.333]
- **MLP 4**: 0.300 [0.277, 0.324]
- **MLP 5**: 0.203 [0.183, 0.226]
- **5 MLPs jointly**: 0.788 [0.747, 0.827]

## Sign check (before any stratification)

Convention. The d_ features are reference minus variant (the thesis scripts define per-sentence differences as reference minus variant, e.g. rq1_late_ablation: d = ref_Mean - var_Mean; the surprisal-type cues d_kenlm and d_ngram2 are n-gram surprisal differences). Reference is the written sentence, so a NEGATIVE value of d_kenlm_mean_filt or d_ngram2_mean_filt means the written sentence is less surprising to the n-gram model, i.e. the cue favours the written order. The pair's gap is f_clean - f_corrupt, positive when the model prefers the written order. If the convention holds, the Spearman of these cues with the gap is NEGATIVE. The check below tests this on the data; the script aborts if the lexical cue shows the opposite sign.


| cue | n | Spearman with gap | p |
|---|---|---|---|
| d_kenlm_mean_filt | 471 | -0.4566 | 1.242e-25 |
| d_ngram2_mean_filt | 471 | -0.3531 | 2.803e-15 |
| d_dep_total | 471 | -0.02603 | 0.5731 |
| d_is_inv_norm | 452 | -0.01035 | 0.8263 |
| d_casemarker_mean | 471 | 0.04235 | 0.3591 |
| kendall | 471 | 0.3273 | 3.212e-13 |

Result: lexical cues are negatively related to the gap, consistent with reference minus variant surprisal. Direction used: d < 0 favours the written order (agrees), d > 0 favours the reordered one (disagrees). For d_dep_total (dependency distance, smaller is easier) and d_is_inv_norm, the same reference minus variant convention applies; their correlations with the gap are descriptive and signs are read from the table above, not used for strata.


## Strata by d_kenlm_mean_filt

- **excluded (cue 0 or missing)**: 1

| stratum | pairs | docs | above floor | prefers written | mean gap (bits) | 10 heads share | 5 MLPs share |
|---|---|---|---|---|---|---|---|
| agrees (cue favours written) | 410 | 303 | 353 | 83.2% | 0.540 | 0.473 [0.436, 0.511] | 0.779 [0.740, 0.819] |
| disagrees (cue favours reordered) | 60 | 56 | 48 | 61.7% | 0.173 | 0.794 [0.566, 1.829] | 0.977 [0.718, 1.697] |


| quantity | disagrees minus agrees | 95% doc-bootstrap interval |
|---|---|---|
| 10 heads | 0.321 | [0.090, 1.351] |
| 5 MLPs jointly | 0.197 | [-0.066, 0.943] |

**DECISION (PRIMARY, d_kenlm_mean_filt, xlmrlarge): CUE-DEPENDENT** (strata above floor: agrees 353, disagrees 48; band +-0.1)


## Strata by d_ngram2_mean_filt

- **excluded (cue 0 or missing)**: 1

| stratum | pairs | docs | above floor | prefers written | mean gap (bits) | 10 heads share | 5 MLPs share |
|---|---|---|---|---|---|---|---|
| agrees (cue favours written) | 375 | 287 | 322 | 82.4% | 0.533 | 0.474 [0.433, 0.515] | 0.769 [0.726, 0.808] |
| disagrees (cue favours reordered) | 95 | 89 | 79 | 72.6% | 0.339 | 0.571 [0.462, 0.728] | 0.906 [0.794, 1.055] |


| quantity | disagrees minus agrees | 95% doc-bootstrap interval |
|---|---|---|
| 10 heads | 0.097 | [-0.018, 0.264] |
| 5 MLPs jointly | 0.137 | [0.015, 0.291] |

**DECISION (second analysis, d_ngram2_mean_filt, xlmrlarge): CUE-DEPENDENT** (strata above floor: agrees 322, disagrees 79; band +-0.1)


## Descriptive: Spearman with the gap and with the 5 MLPs' joint effect (bits)


| cue | n | rho gap | p | rho MLP effect | p |
|---|---|---|---|---|---|
| d_kenlm_mean_filt | 471 | -0.4566 | 1.242e-25 | -0.4333 | 5.632e-23 |
| d_ngram2_mean_filt | 471 | -0.3531 | 2.803e-15 | -0.3149 | 2.657e-12 |
| d_dep_total | 471 | -0.02603 | 0.5731 | -0.0165 | 0.7209 |
| d_is_inv_norm | 452 | -0.01035 | 0.8263 | -0.02494 | 0.597 |
| d_casemarker_mean | 471 | 0.04235 | 0.3591 | 0.05721 | 0.2152 |
| kendall | 471 | 0.3273 | 3.212e-13 | 0.3492 | 5.968e-15 |


## Descriptive: OLS of the gap on standardised cue families (not a test)

- **pairs in the regression**: 452
- **R^2**: 0.273

| term | coefficient (bits per SD) |
|---|---|
| intercept | 0.479 |
| d_kenlm_mean_filt | -0.372 |
| d_dep_total | -0.013 |
| d_is_inv_norm | 0.007 |
| d_casemarker_mean | 0.077 |


> Descriptive only: the cues are correlated with each other and with reordering size, and the gap is not a response with a known noise model.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `cues_xlmrlarge.csv` | 166,060 | `0a8f3bbad1989411` | per-pair cues, gap, set effects (bits), stratum |
