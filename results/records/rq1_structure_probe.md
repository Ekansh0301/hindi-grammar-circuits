# rq1_structure_probe

_Is case marking decodable from a constituent without its marker, and are order expectation and dependency length decodable from the pair difference, layer by layer?_

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 14:31 |
| script | `rq1_structure_probe.py` (sha256 `3553621380e3a737`) |
| host | gnode (Linux) |
| duration | 71.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_structure_probe.csv", "tag": "rq1_structure_probe", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv"}` |
| command | `scripts/rq1_structure_probe.py` |



## model: muril, case probe

- **constituents / references**: 5,976 / 2,000
- **labels**: 0 2449, other 970, me 761, ne 653, ko 496, se 327, par 317, ka 3
- **majority-class accuracy**: 0.4098
- **control (pre-LayerNorm embedding sum): accuracy, macro-F1**: 0.4943, 0.3412

| layer | accuracy | macro-F1 | accuracy minus control |
|---|---|---|---|
| 0 | 0.4958 | 0.3425 | 0.0015 |
| 1 | 0.5331 | 0.3731 | 0.0388 |
| 2 | 0.8482 | 0.6794 | 0.3539 |
| 3 | 0.8738 | 0.7122 | 0.3795 |
| 4 | 0.8931 | 0.7360 | 0.3988 |
| 5 | 0.8849 | 0.7280 | 0.3906 |
| 6 | 0.8589 | 0.6918 | 0.3646 |
| 7 | 0.8685 | 0.6992 | 0.3742 |
| 8 | 0.8578 | 0.6879 | 0.3635 |
| 9 | 0.8484 | 0.6748 | 0.3541 |
| 10 | 0.8434 | 0.6708 | 0.3491 |
| 11 | 0.8608 | 0.6995 | 0.3665 |
| 12 | 0.8643 | 0.7040 | 0.3700 |


## model: muril, pair probes (out-of-fold R²)

- **pairs**: 8,923

| layer | R² d_syn_order | R² d_dep_mean |
|---|---|---|
| 0 | 0.0221 | 0.2061 |
| 1 | 0.0209 | 0.1827 |
| 2 | 0.1930 | 0.4170 |
| 3 | 0.2984 | 0.5941 |
| 4 | 0.3358 | 0.6413 |
| 5 | 0.3487 | 0.6682 |
| 6 | 0.3524 | 0.7027 |
| 7 | 0.3511 | 0.7073 |
| 8 | 0.3389 | 0.6850 |
| 9 | 0.3257 | 0.6575 |
| 10 | 0.3083 | 0.6339 |
| 11 | 0.2906 | 0.6054 |
| 12 | 0.2845 | 0.6037 |

Layer 0 is the control row.


## model: indicbert, case probe

- **constituents / references**: 5,976 / 2,000
- **labels**: 0 2449, other 970, me 761, ne 653, ko 496, se 327, par 317, ka 3
- **majority-class accuracy**: 0.4098
- **control (pre-LayerNorm embedding sum): accuracy, macro-F1**: 0.5085, 0.3536

| layer | accuracy | macro-F1 | accuracy minus control |
|---|---|---|---|
| 0 | 0.5119 | 0.3581 | 0.0033 |
| 1 | 0.8504 | 0.7024 | 0.3419 |
| 2 | 0.8906 | 0.7458 | 0.3820 |
| 3 | 0.8839 | 0.7327 | 0.3753 |
| 4 | 0.8973 | 0.7491 | 0.3887 |
| 5 | 0.8916 | 0.7364 | 0.3830 |
| 6 | 0.8899 | 0.7349 | 0.3814 |
| 7 | 0.8758 | 0.7179 | 0.3673 |
| 8 | 0.8641 | 0.6985 | 0.3556 |
| 9 | 0.8583 | 0.6965 | 0.3497 |
| 10 | 0.8395 | 0.6751 | 0.3310 |
| 11 | 0.7898 | 0.6263 | 0.2813 |
| 12 | 0.8067 | 0.6440 | 0.2982 |


## model: indicbert, pair probes (out-of-fold R²)

- **pairs**: 8,923

| layer | R² d_syn_order | R² d_dep_mean |
|---|---|---|
| 0 | -0.0351 | 0.0480 |
| 1 | 0.1237 | 0.3003 |
| 2 | 0.2415 | 0.4502 |
| 3 | 0.2645 | 0.5214 |
| 4 | 0.3207 | 0.6279 |
| 5 | 0.3421 | 0.6781 |
| 6 | 0.3590 | 0.7157 |
| 7 | 0.3570 | 0.7049 |
| 8 | 0.3267 | 0.6775 |
| 9 | 0.3141 | 0.6541 |
| 10 | 0.2843 | 0.6158 |
| 11 | 0.2380 | 0.5050 |
| 12 | 0.2399 | 0.5366 |

Layer 0 is the control row.


## model: mbert, case probe

- **constituents / references**: 5,976 / 2,000
- **labels**: 0 2449, other 970, me 761, ne 653, ko 496, se 327, par 317, ka 3
- **majority-class accuracy**: 0.4098
- **control (pre-LayerNorm embedding sum): accuracy, macro-F1**: 0.4890, 0.3304

| layer | accuracy | macro-F1 | accuracy minus control |
|---|---|---|---|
| 0 | 0.4886 | 0.3299 | -0.0003 |
| 1 | 0.5686 | 0.4128 | 0.0797 |
| 2 | 0.7118 | 0.5448 | 0.2229 |
| 3 | 0.7908 | 0.6273 | 0.3019 |
| 4 | 0.8342 | 0.6713 | 0.3452 |
| 5 | 0.8169 | 0.6496 | 0.3280 |
| 6 | 0.8932 | 0.7433 | 0.4043 |
| 7 | 0.8907 | 0.7413 | 0.4018 |
| 8 | 0.8717 | 0.7187 | 0.3827 |
| 9 | 0.8601 | 0.7071 | 0.3712 |
| 10 | 0.8499 | 0.6901 | 0.3609 |
| 11 | 0.8422 | 0.6824 | 0.3532 |
| 12 | 0.8042 | 0.6419 | 0.3153 |


## model: mbert, pair probes (out-of-fold R²)

- **pairs**: 8,923

| layer | R² d_syn_order | R² d_dep_mean |
|---|---|---|
| 0 | -0.0584 | -0.0084 |
| 1 | 0.0219 | 0.1530 |
| 2 | 0.0489 | 0.1628 |
| 3 | 0.1211 | 0.3429 |
| 4 | 0.1683 | 0.4282 |
| 5 | 0.2182 | 0.5460 |
| 6 | 0.2465 | 0.5923 |
| 7 | 0.2692 | 0.6099 |
| 8 | 0.2713 | 0.6035 |
| 9 | 0.2514 | 0.5855 |
| 10 | 0.2365 | 0.5653 |
| 11 | 0.2255 | 0.5520 |
| 12 | 0.2096 | 0.5260 |

Layer 0 is the control row.


## model: xlmrlarge, case probe

- **constituents / references**: 5,976 / 2,000
- **labels**: 0 2449, other 970, me 761, ne 653, ko 496, se 327, par 317, ka 3
- **majority-class accuracy**: 0.4098
- **control (pre-LayerNorm embedding sum): accuracy, macro-F1**: 0.4813, 0.3307

| layer | accuracy | macro-F1 | accuracy minus control |
|---|---|---|---|
| 0 | 0.4808 | 0.3296 | -0.0005 |
| 1 | 0.5505 | 0.4023 | 0.0693 |
| 2 | 0.7557 | 0.6016 | 0.2744 |
| 3 | 0.8035 | 0.6474 | 0.3223 |
| 4 | 0.8046 | 0.6516 | 0.3233 |
| 5 | 0.8191 | 0.6693 | 0.3379 |
| 6 | 0.8104 | 0.6535 | 0.3291 |
| 7 | 0.8333 | 0.6771 | 0.3521 |
| 8 | 0.8768 | 0.7181 | 0.3956 |
| 9 | 0.9041 | 0.7479 | 0.4229 |
| 10 | 0.9222 | 0.7740 | 0.4409 |
| 11 | 0.9003 | 0.7445 | 0.4190 |
| 12 | 0.9051 | 0.7594 | 0.4239 |
| 13 | 0.8937 | 0.7445 | 0.4125 |
| 14 | 0.8832 | 0.7294 | 0.4019 |
| 15 | 0.8681 | 0.7093 | 0.3869 |
| 16 | 0.8526 | 0.6862 | 0.3713 |
| 17 | 0.8522 | 0.6879 | 0.3710 |
| 18 | 0.8516 | 0.6829 | 0.3703 |
| 19 | 0.8452 | 0.6791 | 0.3640 |
| 20 | 0.8439 | 0.6754 | 0.3626 |
| 21 | 0.8320 | 0.6577 | 0.3507 |
| 22 | 0.8215 | 0.6486 | 0.3402 |
| 23 | 0.8183 | 0.6438 | 0.3370 |
| 24 | 0.8067 | 0.6307 | 0.3255 |


## model: xlmrlarge, pair probes (out-of-fold R²)

- **pairs**: 8,923

| layer | R² d_syn_order | R² d_dep_mean |
|---|---|---|
| 0 | -0.1739 | -0.1895 |
| 1 | -0.0654 | 0.1228 |
| 2 | 0.0102 | 0.2040 |
| 3 | 0.0772 | 0.2941 |
| 4 | 0.0997 | 0.3059 |
| 5 | 0.1045 | 0.3033 |
| 6 | 0.1273 | 0.3247 |
| 7 | 0.1605 | 0.4532 |
| 8 | 0.2208 | 0.5582 |
| 9 | 0.2491 | 0.6374 |
| 10 | 0.2573 | 0.6541 |
| 11 | 0.2837 | 0.6640 |
| 12 | 0.2922 | 0.6556 |
| 13 | 0.2973 | 0.6624 |
| 14 | 0.2872 | 0.6517 |
| 15 | 0.2910 | 0.6520 |
| 16 | 0.2829 | 0.6503 |
| 17 | 0.2930 | 0.6424 |
| 18 | 0.2767 | 0.6267 |
| 19 | 0.2733 | 0.6072 |
| 20 | 0.2628 | 0.5797 |
| 21 | 0.2593 | 0.5256 |
| 22 | 0.2318 | 0.5016 |
| 23 | 0.2170 | 0.4719 |
| 24 | 0.2158 | 0.4598 |

Layer 0 is the control row.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_structure_probe.csv` | 6,956 | `e391a8a417133278` | case probe: a = accuracy, b = macro-F1; pair probe: a = R² d_syn_order, b = R² d_dep_mean |
