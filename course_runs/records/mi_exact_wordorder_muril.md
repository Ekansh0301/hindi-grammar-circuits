# mi_exact_wordorder_muril

_Step 4 word order, stage exact, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:00 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 2.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact"}` |
| command | `scripts/mi_wordorder.py --stage exact --model muril --max-rows 256` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **matched random 30 heads: layer-unmatched / type-unmatched replacements**: 0 / 0
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.66e-05
- **check: embedding output patched everywhere, ratio of sums / worst pair (bits)**: 0.999999 / 7.39e-06
- **pairs / with a gap above --min-gap**: 146 / 124
- **screen's top 30 heads against 30 heads matched by block: mean |effect| per pair (bits), document sign-flip p (one-sided; descriptive)**: 0.0503 vs 0.0251, p = 9.999e-05
- **heads: Spearman of screened and exact shares over the 60 / of the 10 largest exact shares, in the screen's top 30**: 0.977 / 10
The comparison is among the 60 heads patched exactly: a head the screen ranked outside its top 30 is patched only if drawn as a matched random head, so YES says the screen's top heads beat heads matched to them by block, not that no stronger head was missed.

- **DECISION (the screen ranks heads usefully for this model)**: YES

| component | drawn as | screened share | exact share | document bootstrap 95% |
|---|---|---|---|---|
| L10MLP | MLP (all) | 0.7228 | 0.5585 | [0.502, 0.634] |
| L9MLP | MLP (all) | 0.5951 | 0.4929 | [0.452, 0.543] |
| L8MLP | MLP (all) | 0.5724 | 0.4863 | [0.437, 0.552] |
| L7MLP | MLP (all) | 0.5079 | 0.4245 | [0.373, 0.483] |
| L6MLP | MLP (all) | 0.3194 | 0.2992 | [0.250, 0.365] |
| L5MLP | MLP (all) | 0.2576 | 0.2247 | [0.178, 0.279] |
| L2MLP | MLP (all) | 0.2421 | 0.2147 | [0.171, 0.274] |
| L4MLP | MLP (all) | 0.2288 | 0.1945 | [0.148, 0.252] |
| L1MLP | MLP (all) | 0.1632 | 0.1849 | [0.133, 0.239] |
| L3MLP | MLP (all) | 0.2300 | 0.1534 | [0.101, 0.219] |
| L11MLP | MLP (all) | 0.2855 | 0.1329 | [0.079, 0.184] |
| L3H11 | screen top 30 head | 0.0972 | 0.1133 | [0.086, 0.146] |
| L1H4 | screen top 30 head | 0.0710 | 0.1043 | [0.075, 0.138] |
| L1H3 | screen top 30 head | 0.0626 | 0.0974 | [0.066, 0.129] |
| L6H6 | screen top 30 head | 0.0944 | 0.0893 | [0.071, 0.112] |
| L6H4 | screen top 30 head | 0.0834 | 0.0889 | [0.071, 0.110] |
| L9H6 | screen top 30 head | 0.0888 | 0.0869 | [0.073, 0.104] |
| L9H10 | screen top 30 head | 0.0876 | 0.0812 | [0.068, 0.098] |
| L8H11 | screen top 30 head | 0.0793 | 0.0809 | [0.067, 0.099] |
| L2H11 | screen top 30 head | 0.0751 | 0.0789 | [0.057, 0.105] |
| L9H3 | screen top 30 head | 0.0785 | 0.0737 | [0.054, 0.096] |
| L6H10 | screen top 30 head | 0.0685 | 0.0731 | [0.057, 0.093] |
| L9H4 | screen top 30 head | 0.0805 | 0.0722 | [0.057, 0.092] |
| L7H2 | screen top 30 head | 0.0605 | 0.0710 | [0.058, 0.088] |
| L6H9 | screen top 30 head | 0.0655 | 0.0704 | [0.056, 0.088] |
| L10H4 | screen top 30 head | 0.0770 | 0.0701 | [0.058, 0.085] |
| L2H10 | screen top 30 head | 0.0690 | 0.0698 | [0.053, 0.089] |
| L9H9 | screen top 30 head | 0.0688 | 0.0662 | [0.055, 0.083] |
| L8H10 | screen top 30 head | 0.0666 | 0.0614 | [0.051, 0.075] |
| L10H10 | screen top 30 head | 0.0637 | 0.0607 | [0.051, 0.073] |
| L7H9 | screen top 30 head | 0.0594 | 0.0602 | [0.047, 0.075] |
| L5H2 | screen top 30 head | 0.0646 | 0.0600 | [0.040, 0.086] |
| L4H4 | screen top 30 head | 0.0613 | 0.0592 | [0.041, 0.082] |
| L7H4 | screen top 30 head | 0.0581 | 0.0583 | [0.044, 0.073] |
| L8H5 | screen top 30 head | 0.0605 | 0.0574 | [0.044, 0.073] |
| L10H6 | screen top 30 head | 0.0591 | 0.0569 | [0.050, 0.065] |
| L8H6 | screen top 30 head | 0.0609 | 0.0547 | [0.042, 0.073] |
| L7H8 | matched random head | 0.0514 | 0.0547 | [0.042, 0.075] |
| L0MLP | MLP (all) | 0.0620 | 0.0541 | [-0.048, 0.128] |
| L9H11 | matched random head | 0.0533 | 0.0538 | [0.044, 0.065] |
| L4H10 | screen top 30 head | 0.0544 | 0.0520 | [0.034, 0.073] |
| L7H3 | matched random head | 0.0511 | 0.0515 | [0.027, 0.072] |
| L3H1 | screen top 30 head | 0.0600 | 0.0509 | [0.031, 0.072] |
| L4H11 | matched random head | 0.0529 | 0.0506 | [0.039, 0.065] |
| L2H9 | matched random head | 0.0349 | 0.0500 | [0.037, 0.065] |
| L10H9 | matched random head | 0.0511 | 0.0485 | [0.036, 0.063] |
| L8H0 | matched random head | 0.0457 | 0.0448 | [0.034, 0.058] |
| L10H5 | matched random head | 0.0478 | 0.0424 | [0.029, 0.058] |
| L6H11 | matched random head | 0.0422 | 0.0409 | [0.028, 0.061] |
| L8H8 | matched random head | 0.0370 | 0.0364 | [0.028, 0.049] |
| L8H3 | matched random head | 0.0382 | 0.0346 | [0.019, 0.049] |
| L9H5 | matched random head | 0.0349 | 0.0344 | [0.028, 0.042] |
| L9H0 | matched random head | 0.0382 | 0.0334 | [0.026, 0.043] |
| L6H3 | matched random head | 0.0300 | 0.0285 | [0.012, 0.045] |
| L9H8 | matched random head | 0.0321 | 0.0281 | [0.020, 0.038] |
| L7H1 | matched random head | 0.0284 | 0.0271 | [0.020, 0.035] |
| L1H5 | matched random head | 0.0230 | 0.0250 | [0.017, 0.034] |
| L6H2 | matched random head | 0.0217 | 0.0218 | [0.015, 0.030] |
| L9H2 | matched random head | 0.0132 | 0.0109 | [-0.000, 0.028] |
| L10H2 | matched random head | 0.0107 | 0.0098 | [0.005, 0.015] |
| L9H7 | matched random head | 0.0074 | 0.0072 | [0.005, 0.010] |
| L6H8 | matched random head | 0.0057 | 0.0046 | [-0.001, 0.010] |
| L3H10 | matched random head | 0.0026 | 0.0031 | [-0.002, 0.012] |
| L2H7 | matched random head | 0.0010 | 0.0010 | [-0.004, 0.009] |
| L1H6 | matched random head | 0.0004 | 0.0003 | [-0.001, 0.002] |
| L4H9 | matched random head | -0.0003 | -0.0016 | [-0.009, 0.005] |
| L3H4 | matched random head | 0.0002 | -0.0020 | [-0.011, 0.004] |
| L6H5 | matched random head | -0.0149 | -0.0186 | [-0.035, -0.003] |
| L8H1 | matched random head | -0.0209 | -0.0262 | [-0.040, -0.015] |
| L5H4 | matched random head | -0.0530 | -0.0557 | [-0.078, -0.039] |
| L6H7 | screen top 30 head | -0.0749 | -0.0749 | [-0.095, -0.060] |
| L9H1 | screen top 30 head | -0.0785 | -0.0840 | [-0.104, -0.069] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_wordorder_muril.npz` | 46,367 | `bb2bbee27156d9d5` | exact patching, each component alone at every position: the screen's top 30 heads, every MLP, 30 matched random heads |
