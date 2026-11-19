# mi_paper_cues_gap_xlmrlarge

_P5 POST HOC: circuit effect regressed on gap and stratum (added after P5 was read)_

| provenance | |
|---|---|
| run (UTC) | 2026-11-17 23:29 |
| script | `mi_paper_cues_gap.py` (sha256 `00b2b4f15cb15245`) |
| host | TARDIS (Linux) |
| duration | 0.0 min |
| versions | python 3.14.4, pandas 2.3.3, numpy 2.3.5, sklearn 1.7.2, gpu NVIDIA GeForce GTX 1650 |
| args | `{"boot": 1000, "min_gap": 0.05, "model": "xlmrlarge"}` |
| command | `scripts/mi_paper_cues_gap.py --model xlmrlarge` |


**POST HOC.** This analysis was added after P5 was run and read, to interpret its outcome. It is not part of P5's declared rule; P5's labels stand as run.

- **pairs / above the gap floor / documents**: 471 / 402 / 334

## Strata by d_kenlm_mean_filt (agrees = 0: d < 0; disagrees = 1: d > 0), pairs above the floor

- **pairs agrees / disagrees (documents)**: 353 / 48 (269 / 46)

| circuit part | intercept b0 (bits) | gap slope b1 | stratum coefficient b2 (bits) | document bootstrap 95% (1,000 draws, seed 707) | draws dropped | reading |
|---|---|---|---|---|---|---|
| 10 heads | 0.099 | 0.315 | 0.004 | [-0.049, 0.057] | 0 | within +-0.1 bit |
| 5 MLPs jointly | 0.050 | 0.700 | 0.010 | [-0.061, 0.077] | 0 | within +-0.1 bit |


| circuit part | stratum | pairs | mean gap | mean effect (bits) | intercept (bits) | slope on gap | ratio of sums (share) |
|---|---|---|---|---|---|---|---|
| 10 heads | agrees | 353 | 0.627 | 0.296 | 0.104 | 0.307 | 0.473 |
| 10 heads | disagrees | 48 | 0.215 | 0.171 | 0.079 | 0.425 | 0.794 |
| 5 MLPs jointly | agrees | 353 | 0.627 | 0.488 | 0.052 | 0.696 | 0.779 |
| 5 MLPs jointly | disagrees | 48 | 0.215 | 0.210 | 0.049 | 0.751 | 0.977 |


## Strata by d_ngram2_mean_filt (agrees = 0: d < 0; disagrees = 1: d > 0), pairs above the floor

- **pairs agrees / disagrees (documents)**: 322 / 79 (253 / 77)

| circuit part | intercept b0 (bits) | gap slope b1 | stratum coefficient b2 (bits) | document bootstrap 95% (1,000 draws, seed 707) | draws dropped | reading |
|---|---|---|---|---|---|---|
| 10 heads | 0.098 | 0.315 | 0.006 | [-0.035, 0.047] | 0 | within +-0.1 bit |
| 5 MLPs jointly | 0.042 | 0.702 | 0.041 | [-0.009, 0.091] | 0 | within +-0.1 bit |


| circuit part | stratum | pairs | mean gap | mean effect (bits) | intercept (bits) | slope on gap | ratio of sums (share) |
|---|---|---|---|---|---|---|---|
| 10 heads | agrees | 322 | 0.619 | 0.294 | 0.101 | 0.312 | 0.474 |
| 10 heads | disagrees | 79 | 0.406 | 0.232 | 0.095 | 0.337 | 0.571 |
| 5 MLPs jointly | agrees | 322 | 0.619 | 0.476 | 0.048 | 0.691 | 0.769 |
| 5 MLPs jointly | disagrees | 79 | 0.406 | 0.368 | 0.059 | 0.760 | 0.906 |


> Post hoc and descriptive. A stratum coefficient near 0 with the share still higher in the disagrees stratum means the share difference follows from the smaller gaps (effect roughly constant in bits).
