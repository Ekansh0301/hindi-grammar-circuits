# mi_paper_cues_gap_muril

_P5 POST HOC: circuit effect regressed on gap and stratum (added after P5 was read)_

| provenance | |
|---|---|
| run (UTC) | 2026-11-17 23:29 |
| script | `mi_paper_cues_gap.py` (sha256 `00b2b4f15cb15245`) |
| host | TARDIS (Linux) |
| duration | 0.0 min |
| versions | python 3.14.4, pandas 2.3.3, numpy 2.3.5, sklearn 1.7.2, gpu NVIDIA GeForce GTX 1650 |
| args | `{"boot": 1000, "min_gap": 0.05, "model": "muril"}` |
| command | `scripts/mi_paper_cues_gap.py --model muril` |


**POST HOC.** This analysis was added after P5 was run and read, to interpret its outcome. It is not part of P5's declared rule; P5's labels stand as run.

- **pairs / above the gap floor / documents**: 471 / 409 / 334

## Strata by d_kenlm_mean_filt (agrees = 0: d < 0; disagrees = 1: d > 0), pairs above the floor

- **pairs agrees / disagrees (documents)**: 358 / 50 (275 / 48)

| circuit part | intercept b0 (bits) | gap slope b1 | stratum coefficient b2 (bits) | document bootstrap 95% (1,000 draws, seed 707) | draws dropped | reading |
|---|---|---|---|---|---|---|
| 10 heads | 0.087 | 0.593 | -0.027 | [-0.105, 0.056] | 0 | NOT within +-0.1 bit |
| 5 MLPs jointly | 0.046 | 0.899 | 0.008 | [-0.035, 0.054] | 0 | within +-0.1 bit |


| circuit part | stratum | pairs | mean gap | mean effect (bits) | intercept (bits) | slope on gap | ratio of sums (share) |
|---|---|---|---|---|---|---|---|
| 10 heads | agrees | 358 | 0.781 | 0.550 | 0.082 | 0.599 | 0.704 |
| 10 heads | disagrees | 50 | 0.194 | 0.175 | 0.083 | 0.475 | 0.904 |
| 5 MLPs jointly | agrees | 358 | 0.781 | 0.748 | 0.044 | 0.901 | 0.957 |
| 5 MLPs jointly | disagrees | 50 | 0.194 | 0.228 | 0.064 | 0.844 | 1.177 |


## Strata by d_ngram2_mean_filt (agrees = 0: d < 0; disagrees = 1: d > 0), pairs above the floor

- **pairs agrees / disagrees (documents)**: 335 / 73 (266 / 71)

| circuit part | intercept b0 (bits) | gap slope b1 | stratum coefficient b2 (bits) | document bootstrap 95% (1,000 draws, seed 707) | draws dropped | reading |
|---|---|---|---|---|---|---|
| 10 heads | 0.081 | 0.595 | 0.006 | [-0.054, 0.066] | 0 | within +-0.1 bit |
| 5 MLPs jointly | 0.038 | 0.900 | 0.045 | [-0.008, 0.103] | 0 | NOT within +-0.1 bit |


| circuit part | stratum | pairs | mean gap | mean effect (bits) | intercept (bits) | slope on gap | ratio of sums (share) |
|---|---|---|---|---|---|---|---|
| 10 heads | agrees | 335 | 0.752 | 0.528 | 0.084 | 0.590 | 0.702 |
| 10 heads | disagrees | 73 | 0.514 | 0.393 | 0.068 | 0.633 | 0.765 |
| 5 MLPs jointly | agrees | 335 | 0.752 | 0.714 | 0.044 | 0.892 | 0.950 |
| 5 MLPs jointly | disagrees | 73 | 0.514 | 0.546 | 0.048 | 0.968 | 1.061 |


> Post hoc and descriptive. A stratum coefficient near 0 with the share still higher in the disagrees stratum means the share difference follows from the smaller gaps (effect roughly constant in bits).
