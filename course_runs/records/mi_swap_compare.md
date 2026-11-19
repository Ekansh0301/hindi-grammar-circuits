# mi_swap_compare

_Follow-up 3: step 4 against the halves swapped._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 15:31 |
| script | `mi_swap_compare.py` (sha256 `98f9cffdffbc6fdd`) |
| host | gnode (Linux) |
| duration | 0.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"record_tag": "mi_swap_compare"}` |
| command | `scripts/mi_swap_compare.py` |



## object, muril


|  | step 4 (chosen on selection, validated on held-out) | swapped (chosen on held-out, validated on selection) |
|---|---|---|
| top 10 heads | L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10 | L8H3, L10H6, L11H1, L9H6, L11H2, L9H3, L10H10, L1H3, L9H8, L9H5 |
| top 5 MLPs | L11MLP, L10MLP, L9MLP, L8MLP, L0MLP | L11MLP, L10MLP, L8MLP, L9MLP, L0MLP |
| 10 heads validated (the circuit) | L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10 | L8H3, L10H6, L11H1, L9H6, L11H2, L9H3, L10H10, L1H3, L9H8, L9H5 |

- **heads in both of 10 / MLPs in both of 5 / Spearman of exact shares over the components both patched**: 8 / 5 / 0.514 (over 156 components)

| test | direction | circuit | document bootstrap 95% | random mean | random 95th percentile | rank p among random sets | document sign-flip p |
|---|---|---|---|---|---|---|---|
| faithfulness | step 4 | 0.8979 | [0.860, 0.931] | 0.004569 | 0.05961 | 0.009901 | 9.999e-05 |
| faithfulness | swapped | 0.8311 | [0.772, 0.893] | 0.003312 | 0.05934 | 0.009901 | 9.999e-05 |
| necessity | step 4 | 0.9652 | [0.887, 1.045] | 0.004642 | 0.05035 | 0.009901 | 9.999e-05 |
| necessity | swapped | 0.9437 | [0.837, 1.089] | 0.0002567 | 0.05488 | 0.009901 | 9.999e-05 |


| MLP of the validation direction | share on its validation half |
|---|---|
| step 4: L11MLP | 0.4629 |
| step 4: L10MLP | 0.3690 |
| step 4: L9MLP | 0.1613 |
| step 4: L8MLP | 0.2698 |
| step 4: L0MLP | 0.0996 |
| swapped: L11MLP | 0.4488 |
| swapped: L10MLP | 0.3168 |
| swapped: L8MLP | 0.1940 |
| swapped: L9MLP | 0.2060 |
| swapped: L0MLP | 0.0814 |


## object, xlmrlarge


|  | step 4 (chosen on selection, validated on held-out) | swapped (chosen on held-out, validated on selection) |
|---|---|---|
| top 10 heads | L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13 | L20H0, L21H0, L20H2, L19H3, L22H6, L12H6, L8H9, L10H9, L23H7, L8H6 |
| top 5 MLPs | L21MLP, L20MLP, L22MLP, L19MLP, L23MLP | L21MLP, L20MLP, L22MLP, L23MLP, L19MLP |
| 10 heads validated (the circuit) | L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13 | L20H0, L21H0, L20H2, L19H3, L22H6, L12H6, L8H9, L10H9, L23H7, L8H6 |

- **heads in both of 10 / MLPs in both of 5 / Spearman of exact shares over the components both patched**: 7 / 5 / 0.305 (over 408 components)

| test | direction | circuit | document bootstrap 95% | random mean | random 95th percentile | rank p among random sets | document sign-flip p |
|---|---|---|---|---|---|---|---|
| faithfulness | step 4 | 0.7799 | [0.711, 0.848] | -0.002935 | 0.01881 | 0.009901 | 9.999e-05 |
| faithfulness | swapped | 0.7448 | [0.686, 0.830] | 0.001439 | 0.02203 | 0.009901 | 9.999e-05 |
| necessity | step 4 | 1.08 | [0.943, 1.247] | 0.004691 | 0.05887 | 0.009901 | 9.999e-05 |
| necessity | swapped | 1.01 | [0.880, 1.189] | 0.001956 | 0.04924 | 0.009901 | 9.999e-05 |


| MLP of the validation direction | share on its validation half |
|---|---|
| step 4: L21MLP | 0.3412 |
| step 4: L20MLP | 0.2162 |
| step 4: L22MLP | 0.1283 |
| step 4: L19MLP | 0.0616 |
| step 4: L23MLP | 0.1199 |
| swapped: L21MLP | 0.3685 |
| swapped: L20MLP | 0.2237 |
| swapped: L22MLP | 0.1315 |
| swapped: L23MLP | 0.0795 |
| swapped: L19MLP | 0.0882 |


## wordorder, muril


|  | step 4 (chosen on selection, validated on held-out) | swapped (chosen on held-out, validated on selection) |
|---|---|---|
| top 10 heads | L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3 | L1H3, L3H11, L9H10, L1H4, L8H11, L6H4, L9H3, L6H10, L10H4, L7H2 |
| top 5 MLPs | L10MLP, L9MLP, L8MLP, L7MLP, L6MLP | L10MLP, L9MLP, L8MLP, L7MLP, L6MLP |
| 10 heads validated (the circuit) | L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3 | L1H3, L3H11, L9H10, L1H4, L8H11, L6H4, L9H3, L6H10, L10H4, L7H2 |

- **heads in both of 10 / MLPs in both of 5 / Spearman of exact shares over the components both patched**: 7 / 5 / 0.933 (over 53 components)

| test | direction | circuit | document bootstrap 95% | random mean | random 95th percentile | rank p among random sets | document sign-flip p |
|---|---|---|---|---|---|---|---|
| faithfulness | step 4 | 0.7788 | [0.717, 0.839] | 0.1601 | 0.2648 | 0.009901 | 9.999e-05 |
| faithfulness | swapped | 0.7793 | [0.712, 0.850] | 0.2001 | 0.3439 | 0.009901 | 9.999e-05 |
| necessity | step 4 | 0.0598 | [-0.001, 0.112] | 0.007719 | 0.06725 | 0.07921 | 0.05559 |
| necessity | swapped | 0.07467 | [0.004, 0.145] | 0.01437 | 0.07332 | 0.05941 | 0.07079 |


| MLP of the validation direction | share on its validation half |
|---|---|
| step 4: L10MLP | 0.5627 |
| step 4: L9MLP | 0.4950 |
| step 4: L8MLP | 0.4532 |
| step 4: L7MLP | 0.3770 |
| step 4: L6MLP | 0.2433 |
| swapped: L10MLP | 0.5585 |
| swapped: L9MLP | 0.4929 |
| swapped: L8MLP | 0.4863 |
| swapped: L7MLP | 0.4245 |
| swapped: L6MLP | 0.2992 |


## wordorder, xlmrlarge


|  | step 4 (chosen on selection, validated on held-out) | swapped (chosen on held-out, validated on selection) |
|---|---|---|
| top 10 heads | L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2 | L9H2, L8H4, L17H3, L17H7, L9H3, L20H14, L16H4, L20H3, L19H8, L21H5 |
| top 5 MLPs | L19MLP, L20MLP, L21MLP, L18MLP, L17MLP | L19MLP, L18MLP, L20MLP, L21MLP, L17MLP |
| 10 heads validated (the circuit) | L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2 | L9H2, L8H4, L17H3, L17H7, L9H3, L20H14, L16H4, L20H3, L19H8, L21H5 |

- **heads in both of 10 / MLPs in both of 5 / Spearman of exact shares over the components both patched**: 5 / 5 / 0.973 (over 58 components)

| test | direction | circuit | document bootstrap 95% | random mean | random 95th percentile | rank p among random sets | document sign-flip p |
|---|---|---|---|---|---|---|---|
| faithfulness | step 4 | 0.5348 | [0.482, 0.594] | 0.08285 | 0.2137 | 0.009901 | 9.999e-05 |
| faithfulness | swapped | 0.532 | [0.471, 0.626] | 0.1166 | 0.2453 | 0.009901 | 9.999e-05 |
| necessity | step 4 | 0.08588 | [0.038, 0.129] | 0.0138 | 0.04953 | 0.009901 | 0.0032 |
| necessity | swapped | 0.01899 | [-0.033, 0.067] | 0.01663 | 0.05541 | 0.4455 | 0.9339 |


| MLP of the validation direction | share on its validation half |
|---|---|
| step 4: L19MLP | 0.3752 |
| step 4: L20MLP | 0.3067 |
| step 4: L21MLP | 0.2973 |
| step 4: L18MLP | 0.3207 |
| step 4: L17MLP | 0.2400 |
| swapped: L19MLP | 0.3845 |
| swapped: L18MLP | 0.3194 |
| swapped: L20MLP | 0.3698 |
| swapped: L21MLP | 0.3255 |
| swapped: L17MLP | 0.2208 |


## Declared reading


| task | model | stable | faithfulness differs by | swapped rank p | heads shared of 10 | MLPs shared of 5 |
|---|---|---|---|---|---|---|
| object | muril | yes | 0.06688 | 0.009901 | 8 | 5 |
| object | xlmrlarge | yes | 0.03516 | 0.009901 | 7 | 5 |
| wordorder | muril | yes | 0.0004609 | 0.009901 | 7 | 5 |
| wordorder | xlmrlarge | NO | 0.002759 | 0.009901 | 5 | 5 |

- **DECISION (declared: within 0.10, ranks first, at least 6 heads and 3 MLPs shared, in every task and model)**: not in every case: wordorder/xlmrlarge