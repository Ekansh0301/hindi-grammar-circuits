# mi_swap_exact_wordorder_xlmrlarge

_Follow-up 3, halves swapped: exact, wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:44 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 12.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task wordorder --stage exact` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **matched random 30 heads: layer-unmatched / type-unmatched replacements**: 0 / 0
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.79e-05
- **check: embedding output patched everywhere, ratio of sums / worst pair (bits)**: 1.000005 / 4.05e-06
- **pairs / with a gap above --min-gap**: 154 / 129
- **screen's top 30 heads against 30 heads matched by block: mean |effect| per pair (bits), document sign-flip p (one-sided; descriptive)**: 0.0442 vs 0.0202, p = 9.999e-05
- **heads: Spearman of screened and exact shares over the 60 / of the 10 largest exact shares, in the screen's top 30**: 0.969 / 10
The comparison is among the 60 heads patched exactly: a head the screen ranked outside its top 30 is patched only if drawn as a matched random head, so YES says the screen's top heads beat heads matched to them by block, not that no stronger head was missed.

- **DECISION (the screen ranks heads usefully for this model)**: YES

| component | drawn as | screened share | exact share | document bootstrap 95% |
|---|---|---|---|---|
| L19MLP | MLP (all) | 0.4467 | 0.3752 | [0.338, 0.417] |
| L18MLP | MLP (all) | 0.3767 | 0.3207 | [0.277, 0.364] |
| L20MLP | MLP (all) | 0.3731 | 0.3067 | [0.278, 0.338] |
| L21MLP | MLP (all) | 0.3742 | 0.2973 | [0.253, 0.339] |
| L17MLP | MLP (all) | 0.2714 | 0.2400 | [0.205, 0.272] |
| L11MLP | MLP (all) | 0.1955 | 0.2052 | [0.158, 0.255] |
| L16MLP | MLP (all) | 0.1967 | 0.1680 | [0.135, 0.202] |
| L22MLP | MLP (all) | 0.1926 | 0.1421 | [0.114, 0.173] |
| L9MLP | MLP (all) | 0.2198 | 0.1355 | [0.088, 0.184] |
| L12MLP | MLP (all) | 0.1543 | 0.1176 | [0.074, 0.165] |
| L8MLP | MLP (all) | 0.1399 | 0.1103 | [0.069, 0.159] |
| L14MLP | MLP (all) | 0.1273 | 0.0970 | [0.063, 0.131] |
| L15MLP | MLP (all) | 0.1132 | 0.0954 | [0.062, 0.125] |
| L10MLP | MLP (all) | 0.0910 | 0.0938 | [0.032, 0.152] |
| L9H2 | screen top 30 head | 0.0759 | 0.0884 | [0.069, 0.110] |
| L8H4 | screen top 30 head | 0.0536 | 0.0849 | [0.056, 0.115] |
| L7MLP | MLP (all) | 0.1024 | 0.0816 | [0.038, 0.130] |
| L17H3 | screen top 30 head | 0.0786 | 0.0801 | [0.065, 0.097] |
| L13MLP | MLP (all) | 0.1068 | 0.0789 | [0.036, 0.121] |
| L17H7 | screen top 30 head | 0.0809 | 0.0750 | [0.061, 0.091] |
| L9H3 | screen top 30 head | 0.0567 | 0.0736 | [0.047, 0.104] |
| L20H14 | screen top 30 head | 0.0714 | 0.0689 | [0.057, 0.083] |
| L16H4 | screen top 30 head | 0.0584 | 0.0659 | [0.048, 0.088] |
| L20H3 | screen top 30 head | 0.0679 | 0.0639 | [0.054, 0.075] |
| L19H8 | screen top 30 head | 0.0624 | 0.0611 | [0.051, 0.072] |
| L21H5 | screen top 30 head | 0.0639 | 0.0600 | [0.050, 0.072] |
| L17H15 | screen top 30 head | 0.0585 | 0.0588 | [0.048, 0.070] |
| L11H9 | screen top 30 head | 0.0530 | 0.0588 | [0.046, 0.073] |
| L16H1 | screen top 30 head | 0.0621 | 0.0586 | [0.046, 0.073] |
| L18H12 | screen top 30 head | 0.0572 | 0.0538 | [0.040, 0.069] |
| L12H4 | screen top 30 head | 0.0542 | 0.0527 | [0.038, 0.071] |
| L18H14 | screen top 30 head | 0.0522 | 0.0506 | [0.040, 0.062] |
| L21H0 | screen top 30 head | 0.0548 | 0.0504 | [0.041, 0.061] |
| L19H7 | screen top 30 head | 0.0507 | 0.0501 | [0.041, 0.061] |
| L20H2 | screen top 30 head | 0.0519 | 0.0498 | [0.044, 0.057] |
| L9H13 | matched random head | 0.0468 | 0.0479 | [0.032, 0.066] |
| L19H11 | screen top 30 head | 0.0510 | 0.0476 | [0.037, 0.059] |
| L21H3 | matched random head | 0.0497 | 0.0467 | [0.038, 0.056] |
| L11H10 | screen top 30 head | 0.0503 | 0.0445 | [0.027, 0.074] |
| L8H9 | screen top 30 head | 0.0559 | 0.0427 | [0.022, 0.070] |
| L18H3 | matched random head | 0.0433 | 0.0425 | [0.033, 0.054] |
| L8H15 | screen top 30 head | 0.0645 | 0.0393 | [0.017, 0.065] |
| L11H14 | matched random head | 0.0310 | 0.0392 | [0.007, 0.072] |
| L8H7 | matched random head | 0.0193 | 0.0389 | [0.024, 0.055] |
| L19H15 | matched random head | 0.0375 | 0.0364 | [0.029, 0.045] |
| L16H12 | matched random head | 0.0369 | 0.0364 | [0.024, 0.051] |
| L17H5 | matched random head | 0.0374 | 0.0359 | [0.027, 0.046] |
| L19H13 | matched random head | 0.0362 | 0.0339 | [0.026, 0.042] |
| L19H10 | matched random head | 0.0323 | 0.0313 | [0.025, 0.038] |
| L4MLP | MLP (all) | 0.0265 | 0.0309 | [0.012, 0.051] |
| L3MLP | MLP (all) | 0.0249 | 0.0284 | [0.010, 0.049] |
| L11H13 | matched random head | 0.0254 | 0.0262 | [0.015, 0.039] |
| L5MLP | MLP (all) | 0.0072 | 0.0256 | [0.006, 0.045] |
| L20H11 | matched random head | 0.0269 | 0.0254 | [0.020, 0.032] |
| L6MLP | MLP (all) | 0.0139 | 0.0239 | [-0.005, 0.061] |
| L16H15 | matched random head | 0.0213 | 0.0209 | [0.014, 0.028] |
| L1MLP | MLP (all) | 0.0010 | 0.0193 | [-0.003, 0.043] |
| L18H5 | matched random head | 0.0190 | 0.0185 | [0.012, 0.026] |
| L20H7 | matched random head | 0.0200 | 0.0183 | [0.012, 0.025] |
| L20H0 | matched random head | 0.0192 | 0.0180 | [0.009, 0.026] |
| L23MLP | MLP (all) | 0.0679 | 0.0178 | [-0.011, 0.048] |
| L17H2 | matched random head | 0.0171 | 0.0156 | [0.010, 0.022] |
| L11H15 | matched random head | 0.0155 | 0.0151 | [0.010, 0.021] |
| L2MLP | MLP (all) | 0.0209 | 0.0104 | [-0.011, 0.033] |
| L8H6 | matched random head | 0.0100 | 0.0096 | [-0.007, 0.024] |
| L17H12 | matched random head | 0.0054 | 0.0045 | [0.000, 0.009] |
| L21H11 | matched random head | 0.0158 | 0.0044 | [-0.005, 0.014] |
| L20H12 | matched random head | 0.0022 | 0.0017 | [-0.002, 0.005] |
| L16H0 | matched random head | 0.0003 | 0.0002 | [-0.001, 0.002] |
| L17H10 | matched random head | 0.0001 | -0.0002 | [-0.003, 0.003] |
| L9H14 | matched random head | -0.0014 | -0.0023 | [-0.006, 0.001] |
| L9H9 | matched random head | -0.0034 | -0.0045 | [-0.010, -0.000] |
| L18H4 | matched random head | -0.0058 | -0.0069 | [-0.012, -0.002] |
| L12H3 | matched random head | -0.0100 | -0.0111 | [-0.018, -0.006] |
| L21H8 | matched random head | -0.0121 | -0.0135 | [-0.019, -0.008] |
| L8H12 | matched random head | -0.0290 | -0.0231 | [-0.034, -0.013] |
| L9H6 | screen top 30 head | -0.0552 | -0.0484 | [-0.063, -0.036] |
| L0MLP | MLP (all) | -0.0119 | -0.0487 | [-0.107, -0.005] |
| L11H2 | screen top 30 head | -0.0667 | -0.0609 | [-0.081, -0.044] |
| L17H0 | screen top 30 head | -0.0679 | -0.0688 | [-0.083, -0.057] |
| L16H14 | screen top 30 head | -0.0697 | -0.0706 | [-0.092, -0.053] |
| L20H8 | screen top 30 head | -0.0953 | -0.0975 | [-0.110, -0.087] |
| L21H4 | screen top 30 head | -0.0958 | -0.0977 | [-0.110, -0.087] |
| L18H1 | screen top 30 head | -0.0961 | -0.0982 | [-0.118, -0.082] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_wordorder_xlmrlarge.npz` | 55,850 | `93dcb616e2f817f4` | exact patching, each component alone at every position: the screen's top 30 heads, every MLP, 30 matched random heads |
