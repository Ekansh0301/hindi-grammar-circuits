# rq1_concept_erasure_units_indicbert

_LEACE erasure of role or marker at every layer, at the constituents' own words only._

| provenance | |
|---|---|
| run (UTC) | 2026-10-05 09:50 |
| script | `rq1_concept_erasure_units.py` (sha256 `ed7db8580e9a68c5`) |
| host | gnode (Linux) |
| duration | 310.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "conditions": ["none", "role", "marker", "random"], "erasers": "<earlier-repo>/logs/i2u_smoke/indicbert/erasers_indicbert.npz", "fit_limit": null, "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "tag": "indicbert"}` |
| command | `scripts/rq1_concept_erasure_units.py --tag indicbert --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --batch-size 32 --erasers <earlier-repo>/logs/i2u_smoke/indicbert/erasers_indicbert.npz` |


- **fit references / units / encoder blocks**: 2,000 / 5,976 / 12
- **check 1: recomputed unerased unit states against the stored (float16) ones: largest absolute / largest relative departure / elements outside tolerance**: 0.0020 / 4.05e-03 / 0
- **role: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/indicbert/erasers_indicbert.npz
- **marker: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/indicbert/erasers_indicbert.npz
- **random: erasers loaded from**: <earlier-repo>/logs/i2u_smoke/indicbert/erasers_indicbert.npz

## Check: every block's eraser active


| eraser | layer | cross-covariance with role, share of unerased | with marker, share of unerased |
|---|---|---|---|
| role | 1 | 4.84e-08 | 8.98e-01 |
| role | 2 | 3.01e-07 | 8.92e-01 |
| role | 3 | 3.17e-08 | 8.88e-01 |
| role | 4 | 3.76e-08 | 8.73e-01 |
| role | 5 | 3.53e-08 | 8.70e-01 |
| role | 6 | 2.59e-08 | 8.70e-01 |
| role | 7 | 2.63e-08 | 8.69e-01 |
| role | 8 | 2.71e-08 | 8.77e-01 |
| role | 9 | 2.60e-08 | 9.03e-01 |
| role | 10 | 2.68e-08 | 9.17e-01 |
| role | 11 | 2.93e-08 | 9.14e-01 |
| role | 12 | 3.29e-08 | 8.74e-01 |
| marker | 1 | 6.63e-01 | 4.91e-08 |
| marker | 2 | 6.37e-01 | 2.94e-07 |
| marker | 3 | 6.34e-01 | 4.08e-08 |
| marker | 4 | 6.17e-01 | 3.51e-08 |
| marker | 5 | 6.10e-01 | 3.51e-08 |
| marker | 6 | 5.97e-01 | 3.33e-08 |
| marker | 7 | 5.80e-01 | 3.38e-08 |
| marker | 8 | 5.86e-01 | 3.16e-08 |
| marker | 9 | 6.02e-01 | 2.87e-08 |
| marker | 10 | 6.30e-01 | 2.79e-08 |
| marker | 11 | 6.27e-01 | 3.43e-08 |
| marker | 12 | 5.07e-01 | 3.18e-08 |
| random | 1 | 9.99e-01 | 1.00e+00 |
| random | 2 | 9.99e-01 | 9.97e-01 |
| random | 3 | 9.89e-01 | 9.94e-01 |
| random | 4 | 9.89e-01 | 9.95e-01 |
| random | 5 | 9.91e-01 | 9.95e-01 |
| random | 6 | 9.91e-01 | 9.95e-01 |
| random | 7 | 9.92e-01 | 9.97e-01 |
| random | 8 | 9.96e-01 | 9.98e-01 |
| random | 9 | 9.98e-01 | 9.99e-01 |
| random | 10 | 1.00e+00 | 1.00e+00 |
| random | 11 | 1.00e+00 | 1.00e+00 |
| random | 12 | 9.98e-01 | 9.97e-01 |


| eraser | layer | role probe | role majority | marker probe | marker majority |
|---|---|---|---|---|---|
| role | 1 | 0.5326 | 0.6292 | 0.8248 | 0.4098 |
| role | 6 | 0.5534 | 0.6292 | 0.8646 | 0.4098 |
| role | 7 | 0.5475 | 0.6292 | 0.8566 | 0.4098 |
| role | 12 | 0.5487 | 0.6292 | 0.7656 | 0.4098 |
| marker | 1 | 0.6427 | 0.6292 | 0.2701 | 0.4098 |
| marker | 6 | 0.6894 | 0.6292 | 0.2604 | 0.4098 |
| marker | 7 | 0.6944 | 0.6292 | 0.2624 | 0.4098 |
| marker | 12 | 0.6509 | 0.6292 | 0.2428 | 0.4098 |
| random | 1 | 0.7863 | 0.6292 | 0.8497 | 0.4098 |
| random | 6 | 0.8879 | 0.6292 | 0.8886 | 0.4098 |
| random | 7 | 0.8872 | 0.6292 | 0.8783 | 0.4098 |
| random | 12 | 0.8159 | 0.6292 | 0.8054 | 0.4098 |

- **readability references (not fit references)**: 500

## Per condition


| condition | held-out nats per subtoken | READ (both within 2 nats of none) | units' subtokens | other subtokens | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|---|---|---|
| none | 1.6624 | yes | 2.2628 | 0.9410 | 0.7865 | 0.7843 | 0.7826 | 0.7928 |
| role | 1.7407 | yes | 2.3760 | 0.9774 | 0.7960 | 0.7959 | 0.7979 | 0.7970 |
| marker | 1.7337 | yes | 2.3761 | 0.9620 | 0.8071 | 0.8077 | 0.7883 | 0.7980 |
| random | 1.6730 | yes | 2.2807 | 0.9429 | 0.7853 | 0.7825 | 0.7804 | 0.7896 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | 0.01531 | 0.3135 |
| RQ1 pairs | role | none | 8923 | 0.009526 | 0.006999 |
| OSV->SOV | role | random | 2286 | 0.0175 | 0.2486 |
| RQ1 pairs | role | random | 8923 | 0.01076 | 0.0025 |
| OSV->SOV | marker | none | 2286 | 0.005687 | 0.814 |
| RQ1 pairs | marker | none | 8923 | 0.02062 | 9.999e-05 |
| OSV->SOV | marker | random | 2286 | 0.007874 | 0.6628 |
| RQ1 pairs | marker | random | 8923 | 0.02185 | 9.999e-05 |
| OSV->SOV | random | none | 2286 | -0.002187 | 0.7465 |
| RQ1 pairs | random | none | 8923 | -0.001233 | 0.5529 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_indicberteu0_s0.csv` | 1,207,925 | `957fbf41acc2814c` | RQ1 pairs, condition none |
| `osv_indicberteu0.csv` | 649,832 | `8d1f8765b1389384` | OSV transition pairs, condition none |
| `t_indicberteu1_s0.csv` | 1,206,894 | `ffa71d522e8ef566` | RQ1 pairs, condition role |
| `osv_indicberteu1.csv` | 648,580 | `b1309b543c07412f` | OSV transition pairs, condition role |
| `t_indicberteu2_s0.csv` | 1,207,410 | `28df182a9e1fc80f` | RQ1 pairs, condition marker |
| `osv_indicberteu2.csv` | 647,702 | `d7969788425861f9` | OSV transition pairs, condition marker |
| `t_indicberteu4_s0.csv` | 1,207,947 | `eb9cc413c8da37e0` | RQ1 pairs, condition random |
| `osv_indicberteu4.csv` | 649,617 | `f7c93ce08c12fbd0` | OSV transition pairs, condition random |
