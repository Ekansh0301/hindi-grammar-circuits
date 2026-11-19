# rq1_probe_selectivity

_Hewitt and Liang control task for the case probe: selectivity per layer, and a permutation floor for the pair probes._

| provenance | |
|---|---|
| run (UTC) | 2026-09-27 17:55 |
| script | `rq1_probe_selectivity.py` (sha256 `0e280f8cb825e008`) |
| host | gnode (Linux) |
| duration | 10.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "tag": "rq1_probe_selectivity", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_probe_selectivity.py` |



## model: muril, case probe against its control task

- **constituents / references / distinct head lemmas**: 5,976 / 2,000 / 2,014
- **units per head lemma (mean)**: 2.97
- **majority class: real task, control task**: 0.4098, 0.4011

| layer | real accuracy | control accuracy | selectivity | real macro-F1 | control macro-F1 |
|---|---|---|---|---|---|
| 0 | 0.4960 | 0.5673 | -0.0713 | 0.3428 | 0.5261 |
| 1 | 0.5330 | 0.5382 | -0.0052 | 0.3731 | 0.4932 |
| 2 | 0.8482 | 0.5099 | 0.3384 | 0.6789 | 0.4681 |
| 3 | 0.8737 | 0.4823 | 0.3914 | 0.7119 | 0.4385 |
| 4 | 0.8934 | 0.4598 | 0.4336 | 0.7365 | 0.4124 |
| 5 | 0.8839 | 0.4408 | 0.4431 | 0.7270 | 0.3925 |
| 6 | 0.8589 | 0.4224 | 0.4366 | 0.6919 | 0.3734 |
| 7 | 0.8685 | 0.4230 | 0.4454 | 0.6993 | 0.3718 |
| 8 | 0.8574 | 0.4304 | 0.4270 | 0.6875 | 0.3806 |
| 9 | 0.8486 | 0.4347 | 0.4138 | 0.6750 | 0.3832 |
| 10 | 0.8434 | 0.4391 | 0.4043 | 0.6708 | 0.3906 |
| 11 | 0.8608 | 0.4439 | 0.4168 | 0.6995 | 0.3957 |
| 12 | 0.8643 | 0.4592 | 0.4051 | 0.7040 | 0.4057 |

- **highest selectivity**: layer 7, +0.4454 (0.8685 against 0.4230)

## model: muril, pair probes against a permutation floor


| layer | R² d_syn_order | permuted | R² d_dep_mean | permuted |
|---|---|---|---|---|
| 0 | 0.0221 | -0.1433 | 0.2061 | -0.1152 |
| 6 | 0.3524 | -0.1377 | 0.7027 | -0.1380 |
| 12 | 0.2845 | -0.1405 | 0.6037 | -0.1470 |

Three layers only: first, middle, output. The permuted column is a floor check, not a control task, for the reason in this script's docstring.


## model: indicbert, case probe against its control task

- **constituents / references / distinct head lemmas**: 5,976 / 2,000 / 2,014
- **units per head lemma (mean)**: 2.97
- **majority class: real task, control task**: 0.4098, 0.4011

| layer | real accuracy | control accuracy | selectivity | real macro-F1 | control macro-F1 |
|---|---|---|---|---|---|
| 0 | 0.5115 | 0.5653 | -0.0537 | 0.3577 | 0.5258 |
| 1 | 0.8506 | 0.5392 | 0.3114 | 0.7027 | 0.4984 |
| 2 | 0.8909 | 0.5033 | 0.3876 | 0.7460 | 0.4643 |
| 3 | 0.8839 | 0.4869 | 0.3969 | 0.7327 | 0.4399 |
| 4 | 0.8973 | 0.4784 | 0.4188 | 0.7492 | 0.4318 |
| 5 | 0.8916 | 0.4610 | 0.4306 | 0.7364 | 0.4134 |
| 6 | 0.8899 | 0.4434 | 0.4465 | 0.7350 | 0.3973 |
| 7 | 0.8760 | 0.4277 | 0.4483 | 0.7181 | 0.3752 |
| 8 | 0.8641 | 0.4245 | 0.4396 | 0.6985 | 0.3748 |
| 9 | 0.8583 | 0.4337 | 0.4245 | 0.6965 | 0.3846 |
| 10 | 0.8389 | 0.4429 | 0.3959 | 0.6739 | 0.3872 |
| 11 | 0.7898 | 0.4239 | 0.3660 | 0.6270 | 0.3641 |
| 12 | 0.8064 | 0.4460 | 0.3604 | 0.6435 | 0.3949 |

- **highest selectivity**: layer 7, +0.4483 (0.8760 against 0.4277)

## model: indicbert, pair probes against a permutation floor


| layer | R² d_syn_order | permuted | R² d_dep_mean | permuted |
|---|---|---|---|---|
| 0 | -0.0351 | -0.1494 | 0.0480 | -0.1351 |
| 6 | 0.3590 | -0.1370 | 0.7157 | -0.1398 |
| 12 | 0.2399 | -0.1339 | 0.5366 | -0.1464 |

Three layers only: first, middle, output. The permuted column is a floor check, not a control task, for the reason in this script's docstring.


## model: mbert, case probe against its control task

- **constituents / references / distinct head lemmas**: 5,976 / 2,000 / 2,014
- **units per head lemma (mean)**: 2.97
- **majority class: real task, control task**: 0.4098, 0.4011

| layer | real accuracy | control accuracy | selectivity | real macro-F1 | control macro-F1 |
|---|---|---|---|---|---|
| 0 | 0.4885 | 0.5944 | -0.1059 | 0.3300 | 0.5529 |
| 1 | 0.5686 | 0.5535 | 0.0151 | 0.4128 | 0.5144 |
| 2 | 0.7123 | 0.5557 | 0.1566 | 0.5456 | 0.5107 |
| 3 | 0.7903 | 0.5360 | 0.2544 | 0.6266 | 0.4903 |
| 4 | 0.8332 | 0.5192 | 0.3139 | 0.6703 | 0.4763 |
| 5 | 0.8166 | 0.5032 | 0.3134 | 0.6489 | 0.4575 |
| 6 | 0.8934 | 0.4711 | 0.4224 | 0.7436 | 0.4221 |
| 7 | 0.8912 | 0.4553 | 0.4359 | 0.7426 | 0.4042 |
| 8 | 0.8715 | 0.4329 | 0.4386 | 0.7185 | 0.3782 |
| 9 | 0.8601 | 0.4252 | 0.4349 | 0.7071 | 0.3713 |
| 10 | 0.8496 | 0.4182 | 0.4314 | 0.6900 | 0.3596 |
| 11 | 0.8424 | 0.4113 | 0.4311 | 0.6826 | 0.3579 |
| 12 | 0.8042 | 0.4125 | 0.3917 | 0.6420 | 0.3572 |

- **highest selectivity**: layer 8, +0.4386 (0.8715 against 0.4329)

## model: mbert, pair probes against a permutation floor


| layer | R² d_syn_order | permuted | R² d_dep_mean | permuted |
|---|---|---|---|---|
| 0 | -0.0584 | -0.1376 | -0.0083 | -0.1354 |
| 6 | 0.2465 | -0.1323 | 0.5923 | -0.1242 |
| 12 | 0.2096 | -0.1348 | 0.5260 | -0.1321 |

Three layers only: first, middle, output. The permuted column is a floor check, not a control task, for the reason in this script's docstring.


## model: xlmrlarge, case probe against its control task

- **constituents / references / distinct head lemmas**: 5,976 / 2,000 / 2,014
- **units per head lemma (mean)**: 2.97
- **majority class: real task, control task**: 0.4098, 0.4011

| layer | real accuracy | control accuracy | selectivity | real macro-F1 | control macro-F1 |
|---|---|---|---|---|---|
| 0 | 0.4813 | 0.6046 | -0.1233 | 0.3300 | 0.5706 |
| 1 | 0.5495 | 0.5693 | -0.0197 | 0.4020 | 0.5314 |
| 2 | 0.7562 | 0.5505 | 0.2057 | 0.6017 | 0.5054 |
| 3 | 0.8029 | 0.5462 | 0.2567 | 0.6463 | 0.5088 |
| 4 | 0.8061 | 0.5318 | 0.2743 | 0.6534 | 0.4869 |
| 5 | 0.8189 | 0.5174 | 0.3015 | 0.6690 | 0.4724 |
| 6 | 0.8107 | 0.5104 | 0.3004 | 0.6538 | 0.4738 |
| 7 | 0.8333 | 0.4983 | 0.3350 | 0.6771 | 0.4578 |
| 8 | 0.8770 | 0.4988 | 0.3782 | 0.7184 | 0.4575 |
| 9 | 0.9041 | 0.4990 | 0.4051 | 0.7479 | 0.4598 |
| 10 | 0.9222 | 0.4915 | 0.4307 | 0.7740 | 0.4479 |
| 11 | 0.9003 | 0.4871 | 0.4132 | 0.7445 | 0.4444 |
| 12 | 0.9050 | 0.4657 | 0.4393 | 0.7594 | 0.4196 |
| 13 | 0.8936 | 0.4562 | 0.4374 | 0.7438 | 0.4096 |
| 14 | 0.8832 | 0.4523 | 0.4309 | 0.7296 | 0.4031 |
| 15 | 0.8681 | 0.4388 | 0.4294 | 0.7095 | 0.3850 |
| 16 | 0.8524 | 0.4235 | 0.4289 | 0.6857 | 0.3805 |
| 17 | 0.8526 | 0.4255 | 0.4270 | 0.6876 | 0.3802 |
| 18 | 0.8516 | 0.4137 | 0.4379 | 0.6829 | 0.3623 |
| 19 | 0.8452 | 0.4301 | 0.4152 | 0.6790 | 0.3766 |
| 20 | 0.8437 | 0.4352 | 0.4085 | 0.6751 | 0.3859 |
| 21 | 0.8325 | 0.4520 | 0.3805 | 0.6582 | 0.4055 |
| 22 | 0.8218 | 0.4526 | 0.3691 | 0.6494 | 0.4114 |
| 23 | 0.8174 | 0.4433 | 0.3742 | 0.6431 | 0.3990 |
| 24 | 0.8064 | 0.4526 | 0.3537 | 0.6310 | 0.4086 |

- **highest selectivity**: layer 12, +0.4393 (0.9050 against 0.4657)

## model: xlmrlarge, pair probes against a permutation floor


| layer | R² d_syn_order | permuted | R² d_dep_mean | permuted |
|---|---|---|---|---|
| 0 | -0.1739 | -0.1653 | -0.1895 | -0.1855 |
| 12 | 0.2922 | -0.1838 | 0.6556 | -0.1796 |
| 24 | 0.2158 | -0.2190 | 0.4598 | -0.2085 |

Three layers only: first, middle, output. The permuted column is a floor check, not a control task, for the reason in this script's docstring.


> Selectivity, not raw accuracy, is what says the states carry case. A probe that scores well on the control task has the capacity to memorise the head lemma, and its real accuracy then says as much about the probe as about the model.


> The control task is a function of the head LEMMA, so it is fixed per type and reproducible from the seed; it is not a per-constituent coin flip, which would be a random-label baseline and is a weaker check.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_probe_selectivity.csv` | 5,667 | `818f2af268b1dc5f` | per-layer real, control and selectivity |
