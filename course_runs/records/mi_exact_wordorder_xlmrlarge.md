# mi_exact_wordorder_xlmrlarge

_Step 4 word order, stage exact, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:11 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 12.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact"}` |
| command | `scripts/mi_wordorder.py --stage exact --model xlmrlarge --max-rows 128 --chunk 8` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **matched random 30 heads: layer-unmatched / type-unmatched replacements**: 0 / 0
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 1.56e-04
- **check: embedding output patched everywhere, ratio of sums / worst pair (bits)**: 1.000005 / 2.77e-05
- **pairs / with a gap above --min-gap**: 146 / 127
- **screen's top 30 heads against 30 heads matched by block: mean |effect| per pair (bits), document sign-flip p (one-sided; descriptive)**: 0.0372 vs 0.0138, p = 9.999e-05
- **heads: Spearman of screened and exact shares over the 60 / of the 10 largest exact shares, in the screen's top 30**: 0.990 / 10
The comparison is among the 60 heads patched exactly: a head the screen ranked outside its top 30 is patched only if drawn as a matched random head, so YES says the screen's top heads beat heads matched to them by block, not that no stronger head was missed.

- **DECISION (the screen ranks heads usefully for this model)**: YES

| component | drawn as | screened share | exact share | document bootstrap 95% |
|---|---|---|---|---|
| L19MLP | MLP (all) | 0.4804 | 0.3845 | [0.339, 0.440] |
| L20MLP | MLP (all) | 0.4533 | 0.3698 | [0.319, 0.441] |
| L21MLP | MLP (all) | 0.4330 | 0.3255 | [0.290, 0.370] |
| L18MLP | MLP (all) | 0.3860 | 0.3194 | [0.275, 0.381] |
| L17MLP | MLP (all) | 0.2501 | 0.2208 | [0.186, 0.265] |
| L11MLP | MLP (all) | 0.1991 | 0.1793 | [0.127, 0.242] |
| L16MLP | MLP (all) | 0.1807 | 0.1573 | [0.127, 0.197] |
| L10MLP | MLP (all) | 0.1504 | 0.1283 | [0.062, 0.189] |
| L12MLP | MLP (all) | 0.1518 | 0.1276 | [0.092, 0.159] |
| L22MLP | MLP (all) | 0.1887 | 0.1262 | [0.085, 0.179] |
| L9MLP | MLP (all) | 0.2152 | 0.1174 | [0.079, 0.161] |
| L13MLP | MLP (all) | 0.1332 | 0.1018 | [0.071, 0.133] |
| L8MLP | MLP (all) | 0.1624 | 0.0944 | [0.061, 0.125] |
| L14MLP | MLP (all) | 0.1212 | 0.0908 | [0.048, 0.129] |
| L15MLP | MLP (all) | 0.1319 | 0.0904 | [0.050, 0.136] |
| L9H2 | screen top 30 head | 0.0649 | 0.0769 | [0.055, 0.102] |
| L17H3 | screen top 30 head | 0.0759 | 0.0755 | [0.062, 0.093] |
| L17H7 | screen top 30 head | 0.0823 | 0.0754 | [0.060, 0.095] |
| L20H14 | screen top 30 head | 0.0748 | 0.0734 | [0.061, 0.089] |
| L17H15 | screen top 30 head | 0.0691 | 0.0697 | [0.055, 0.093] |
| L21H3 | screen top 30 head | 0.0710 | 0.0671 | [0.057, 0.080] |
| L6H15 | screen top 30 head | 0.0545 | 0.0655 | [0.040, 0.092] |
| L16H4 | screen top 30 head | 0.0661 | 0.0647 | [0.051, 0.082] |
| L16H1 | screen top 30 head | 0.0697 | 0.0639 | [0.047, 0.085] |
| L20H2 | screen top 30 head | 0.0643 | 0.0625 | [0.054, 0.074] |
| L21H5 | screen top 30 head | 0.0644 | 0.0610 | [0.050, 0.079] |
| L20H6 | screen top 30 head | 0.0640 | 0.0600 | [0.048, 0.072] |
| L20H3 | screen top 30 head | 0.0643 | 0.0593 | [0.048, 0.073] |
| L19H7 | screen top 30 head | 0.0577 | 0.0582 | [0.048, 0.071] |
| L7MLP | MLP (all) | 0.0875 | 0.0569 | [0.023, 0.087] |
| L19H11 | screen top 30 head | 0.0659 | 0.0565 | [0.041, 0.076] |
| L18H12 | screen top 30 head | 0.0560 | 0.0548 | [0.042, 0.071] |
| L18H9 | screen top 30 head | 0.0534 | 0.0503 | [0.040, 0.065] |
| L19H3 | screen top 30 head | 0.0531 | 0.0498 | [0.040, 0.062] |
| L19H8 | screen top 30 head | 0.0530 | 0.0497 | [0.040, 0.064] |
| L10H9 | screen top 30 head | 0.0573 | 0.0490 | [0.035, 0.064] |
| L15H12 | screen top 30 head | 0.0501 | 0.0475 | [0.036, 0.063] |
| L20H10 | screen top 30 head | 0.0500 | 0.0470 | [0.038, 0.060] |
| L18H13 | matched random head | 0.0493 | 0.0468 | [0.035, 0.061] |
| L16H5 | matched random head | 0.0455 | 0.0452 | [0.034, 0.060] |
| L12H4 | screen top 30 head | 0.0501 | 0.0447 | [0.029, 0.060] |
| L21H0 | matched random head | 0.0469 | 0.0436 | [0.034, 0.055] |
| L19H15 | matched random head | 0.0372 | 0.0356 | [0.024, 0.053] |
| L20H15 | matched random head | 0.0381 | 0.0355 | [0.026, 0.047] |
| L19H6 | matched random head | 0.0334 | 0.0333 | [0.025, 0.044] |
| L3MLP | MLP (all) | 0.0391 | 0.0304 | [0.013, 0.049] |
| L19H2 | matched random head | 0.0321 | 0.0301 | [0.023, 0.039] |
| L17H4 | matched random head | 0.0317 | 0.0295 | [0.022, 0.040] |
| L20H11 | matched random head | 0.0297 | 0.0276 | [0.016, 0.048] |
| L18H5 | matched random head | 0.0279 | 0.0265 | [0.019, 0.036] |
| L2MLP | MLP (all) | 0.0374 | 0.0259 | [0.006, 0.049] |
| L20H0 | matched random head | 0.0248 | 0.0224 | [0.016, 0.029] |
| L21H13 | matched random head | 0.0231 | 0.0221 | [0.018, 0.027] |
| L5MLP | MLP (all) | 0.0328 | 0.0218 | [-0.001, 0.042] |
| L10H13 | matched random head | 0.0242 | 0.0175 | [0.006, 0.029] |
| L6MLP | MLP (all) | 0.0535 | 0.0173 | [-0.004, 0.039] |
| L4MLP | MLP (all) | 0.0276 | 0.0166 | [-0.008, 0.039] |
| L17H6 | matched random head | 0.0146 | 0.0146 | [0.009, 0.022] |
| L16H8 | matched random head | 0.0145 | 0.0142 | [0.010, 0.019] |
| L11H15 | matched random head | 0.0127 | 0.0127 | [0.005, 0.021] |
| L21H12 | matched random head | 0.0111 | 0.0109 | [0.006, 0.017] |
| L1MLP | MLP (all) | 0.0107 | 0.0097 | [-0.016, 0.032] |
| L20H13 | matched random head | 0.0109 | 0.0097 | [0.005, 0.015] |
| L9H12 | matched random head | 0.0154 | 0.0089 | [0.001, 0.018] |
| L17H12 | matched random head | 0.0071 | 0.0062 | [0.002, 0.010] |
| L12H8 | matched random head | 0.0054 | 0.0051 | [-0.000, 0.011] |
| L20H4 | matched random head | 0.0058 | 0.0049 | [0.002, 0.008] |
| L19H5 | matched random head | 0.0052 | 0.0045 | [0.002, 0.008] |
| L20H12 | matched random head | 0.0025 | 0.0018 | [-0.002, 0.006] |
| L15H10 | matched random head | 0.0015 | 0.0018 | [-0.004, 0.008] |
| L9H14 | matched random head | -0.0012 | -0.0016 | [-0.006, 0.004] |
| L18H4 | matched random head | -0.0001 | -0.0018 | [-0.008, 0.006] |
| L17H10 | matched random head | -0.0016 | -0.0018 | [-0.006, 0.001] |
| L6H3 | matched random head | 0.0009 | -0.0030 | [-0.008, 0.001] |
| L16H11 | matched random head | -0.0176 | -0.0180 | [-0.026, -0.012] |
| L23MLP | MLP (all) | 0.0368 | -0.0229 | [-0.069, 0.017] |
| L9H6 | screen top 30 head | -0.0499 | -0.0392 | [-0.056, -0.022] |
| L16H14 | screen top 30 head | -0.0642 | -0.0627 | [-0.082, -0.047] |
| L11H2 | screen top 30 head | -0.0678 | -0.0629 | [-0.084, -0.046] |
| L17H0 | screen top 30 head | -0.0809 | -0.0819 | [-0.105, -0.065] |
| L21H4 | screen top 30 head | -0.0885 | -0.0914 | [-0.110, -0.078] |
| L0MLP | MLP (all) | 0.0032 | -0.0916 | [-0.176, -0.022] |
| L20H8 | screen top 30 head | -0.0955 | -0.0987 | [-0.114, -0.086] |
| L18H1 | screen top 30 head | -0.0993 | -0.1004 | [-0.127, -0.083] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_wordorder_xlmrlarge.npz` | 52,481 | `1c76c6cd35cba6e7` | exact patching, each component alone at every position: the screen's top 30 heads, every MLP, 30 matched random heads |
