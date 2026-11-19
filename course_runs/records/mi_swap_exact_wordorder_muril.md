# mi_swap_exact_wordorder_muril

_Follow-up 3, halves swapped: exact, wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:19 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 2.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "exact", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task wordorder --stage exact` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **matched random 30 heads: layer-unmatched / type-unmatched replacements**: 0 / 0
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 2.95e-05
- **check: embedding output patched everywhere, ratio of sums / worst pair (bits)**: 0.999994 / 6.68e-06
- **pairs / with a gap above --min-gap**: 154 / 135
- **screen's top 30 heads against 30 heads matched by block: mean |effect| per pair (bits), document sign-flip p (one-sided; descriptive)**: 0.0548 vs 0.0275, p = 9.999e-05
- **heads: Spearman of screened and exact shares over the 60 / of the 10 largest exact shares, in the screen's top 30**: 0.978 / 10
The comparison is among the 60 heads patched exactly: a head the screen ranked outside its top 30 is patched only if drawn as a matched random head, so YES says the screen's top heads beat heads matched to them by block, not that no stronger head was missed.

- **DECISION (the screen ranks heads usefully for this model)**: YES

| component | drawn as | screened share | exact share | document bootstrap 95% |
|---|---|---|---|---|
| L10MLP | MLP (all) | 0.7169 | 0.5627 | [0.523, 0.606] |
| L9MLP | MLP (all) | 0.5854 | 0.4950 | [0.453, 0.537] |
| L8MLP | MLP (all) | 0.5286 | 0.4532 | [0.401, 0.512] |
| L7MLP | MLP (all) | 0.4508 | 0.3770 | [0.327, 0.430] |
| L6MLP | MLP (all) | 0.3022 | 0.2433 | [0.190, 0.297] |
| L4MLP | MLP (all) | 0.2349 | 0.1890 | [0.151, 0.227] |
| L5MLP | MLP (all) | 0.2263 | 0.1816 | [0.139, 0.225] |
| L1MLP | MLP (all) | 0.1526 | 0.1769 | [0.136, 0.218] |
| L11MLP | MLP (all) | 0.2997 | 0.1578 | [0.105, 0.212] |
| L2MLP | MLP (all) | 0.1762 | 0.1558 | [0.124, 0.190] |
| L3MLP | MLP (all) | 0.1881 | 0.1347 | [0.092, 0.181] |
| L1H3 | screen top 30 head | 0.0822 | 0.1147 | [0.090, 0.141] |
| L3H11 | screen top 30 head | 0.0974 | 0.1140 | [0.090, 0.141] |
| L9H10 | screen top 30 head | 0.1083 | 0.1039 | [0.088, 0.121] |
| L1H4 | screen top 30 head | 0.0643 | 0.0958 | [0.077, 0.115] |
| L8H11 | screen top 30 head | 0.0826 | 0.0857 | [0.074, 0.099] |
| L0MLP | MLP (all) | 0.0760 | 0.0772 | [0.023, 0.127] |
| L6H4 | screen top 30 head | 0.0734 | 0.0766 | [0.061, 0.093] |
| L9H3 | screen top 30 head | 0.0737 | 0.0745 | [0.059, 0.092] |
| L6H10 | screen top 30 head | 0.0676 | 0.0741 | [0.060, 0.089] |
| L10H4 | screen top 30 head | 0.0793 | 0.0738 | [0.063, 0.086] |
| L7H2 | screen top 30 head | 0.0672 | 0.0727 | [0.059, 0.088] |
| L4H4 | screen top 30 head | 0.0702 | 0.0721 | [0.058, 0.087] |
| L9H11 | screen top 30 head | 0.0700 | 0.0709 | [0.059, 0.086] |
| L10H6 | screen top 30 head | 0.0711 | 0.0675 | [0.057, 0.080] |
| L9H6 | screen top 30 head | 0.0677 | 0.0672 | [0.056, 0.078] |
| L8H5 | screen top 30 head | 0.0689 | 0.0663 | [0.052, 0.081] |
| L2H11 | screen top 30 head | 0.0582 | 0.0639 | [0.041, 0.088] |
| L7H0 | screen top 30 head | 0.0585 | 0.0619 | [0.051, 0.073] |
| L9H9 | screen top 30 head | 0.0620 | 0.0614 | [0.050, 0.075] |
| L6H6 | screen top 30 head | 0.0699 | 0.0609 | [0.040, 0.083] |
| L7H9 | screen top 30 head | 0.0600 | 0.0606 | [0.049, 0.073] |
| L7H4 | screen top 30 head | 0.0618 | 0.0600 | [0.046, 0.075] |
| L6H9 | matched random head | 0.0524 | 0.0585 | [0.044, 0.074] |
| L2H6 | screen top 30 head | 0.0608 | 0.0573 | [0.043, 0.074] |
| L8H6 | screen top 30 head | 0.0634 | 0.0570 | [0.043, 0.073] |
| L10H1 | screen top 30 head | 0.0580 | 0.0565 | [0.047, 0.068] |
| L5H11 | screen top 30 head | 0.0568 | 0.0551 | [0.039, 0.074] |
| L10H10 | screen top 30 head | 0.0579 | 0.0544 | [0.045, 0.065] |
| L10H9 | screen top 30 head | 0.0576 | 0.0542 | [0.043, 0.068] |
| L8H10 | screen top 30 head | 0.0563 | 0.0539 | [0.042, 0.065] |
| L9H4 | matched random head | 0.0547 | 0.0485 | [0.037, 0.060] |
| L10H5 | matched random head | 0.0466 | 0.0422 | [0.027, 0.058] |
| L8H9 | matched random head | 0.0403 | 0.0396 | [0.030, 0.050] |
| L8H8 | matched random head | 0.0392 | 0.0391 | [0.026, 0.060] |
| L2H9 | matched random head | 0.0185 | 0.0384 | [0.023, 0.055] |
| L8H3 | matched random head | 0.0409 | 0.0383 | [0.024, 0.053] |
| L8H7 | matched random head | 0.0384 | 0.0378 | [0.033, 0.044] |
| L7H6 | matched random head | 0.0359 | 0.0368 | [0.029, 0.045] |
| L7H3 | matched random head | 0.0407 | 0.0360 | [0.018, 0.054] |
| L9H5 | matched random head | 0.0330 | 0.0327 | [0.027, 0.040] |
| L6H11 | matched random head | 0.0332 | 0.0322 | [0.026, 0.040] |
| L9H0 | matched random head | 0.0360 | 0.0310 | [0.022, 0.040] |
| L9H8 | matched random head | 0.0335 | 0.0306 | [0.023, 0.040] |
| L5H7 | matched random head | 0.0355 | 0.0300 | [0.012, 0.048] |
| L4H3 | matched random head | 0.0215 | 0.0180 | [0.008, 0.029] |
| L1H2 | matched random head | 0.0176 | 0.0172 | [0.008, 0.026] |
| L10H2 | matched random head | 0.0172 | 0.0161 | [0.007, 0.033] |
| L7H7 | matched random head | 0.0216 | 0.0136 | [0.001, 0.026] |
| L10H8 | matched random head | 0.0121 | 0.0117 | [0.009, 0.015] |
| L9H2 | matched random head | 0.0140 | 0.0102 | [0.004, 0.017] |
| L3H6 | matched random head | 0.0109 | 0.0101 | [0.000, 0.023] |
| L9H7 | matched random head | 0.0092 | 0.0089 | [0.004, 0.017] |
| L10H11 | matched random head | 0.0054 | 0.0047 | [0.002, 0.008] |
| L6H0 | matched random head | 0.0015 | 0.0014 | [-0.001, 0.003] |
| L1H7 | matched random head | 0.0008 | 0.0008 | [-0.001, 0.002] |
| L2H8 | matched random head | -0.0068 | -0.0050 | [-0.010, -0.001] |
| L6H5 | matched random head | -0.0054 | -0.0099 | [-0.024, 0.005] |
| L10H0 | matched random head | -0.0205 | -0.0237 | [-0.034, -0.012] |
| L7H5 | matched random head | -0.0491 | -0.0495 | [-0.060, -0.040] |
| L6H7 | screen top 30 head | -0.0653 | -0.0659 | [-0.082, -0.053] |
| L9H1 | screen top 30 head | -0.0704 | -0.0735 | [-0.089, -0.060] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `exact_wordorder_muril.npz` | 48,935 | `ba09d8768e3f9dce` | exact patching, each component alone at every position: the screen's top 30 heads, every MLP, 30 matched random heads |
