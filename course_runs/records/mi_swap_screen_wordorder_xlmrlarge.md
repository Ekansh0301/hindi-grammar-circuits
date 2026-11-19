# mi_swap_screen_wordorder_xlmrlarge

_Follow-up 3, halves swapped: screen, wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:31 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 1.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task wordorder --stage screen` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.79e-05
- **pairs / skipped / with a gap above --min-gap**: 154 / 0 / 129

| component | screened share | via special | via moved_heads | via moved_psp | via moved_other | via verb | via unmoved |
|---|---|---|---|---|---|---|---|
| L19MLP | 0.4467 | -0.0001 | 0.1666 | 0.0640 | 0.1037 | 0.0487 | 0.0639 |
| L18MLP | 0.3767 | 0.0000 | 0.1509 | 0.0542 | 0.0887 | 0.0351 | 0.0477 |
| L21MLP | 0.3742 | 0.0002 | 0.1605 | 0.0457 | 0.0798 | 0.0345 | 0.0533 |
| L20MLP | 0.3731 | 0.0001 | 0.1445 | 0.0471 | 0.0830 | 0.0444 | 0.0540 |
| L17MLP | 0.2714 | -0.0008 | 0.1145 | 0.0285 | 0.0685 | 0.0270 | 0.0337 |
| L9MLP | 0.2198 | -0.0023 | 0.0872 | 0.0244 | 0.0393 | 0.0532 | 0.0181 |
| L16MLP | 0.1967 | -0.0004 | 0.0740 | 0.0309 | 0.0450 | 0.0214 | 0.0257 |
| L11MLP | 0.1955 | 0.0012 | 0.0801 | 0.0222 | 0.0334 | 0.0460 | 0.0127 |
| L22MLP | 0.1926 | 0.0003 | 0.0803 | 0.0121 | 0.0491 | 0.0283 | 0.0225 |
| L12MLP | 0.1543 | 0.0002 | 0.0527 | 0.0230 | 0.0430 | 0.0193 | 0.0161 |
| L8MLP | 0.1399 | -0.0009 | 0.0760 | 0.0139 | 0.0404 | 0.0361 | -0.0257 |
| L14MLP | 0.1273 | -0.0012 | 0.0364 | 0.0297 | 0.0319 | 0.0195 | 0.0109 |
| L15MLP | 0.1132 | 0.0001 | 0.0257 | 0.0178 | 0.0301 | 0.0177 | 0.0217 |
| L13MLP | 0.1068 | 0.0008 | 0.0396 | 0.0222 | 0.0299 | 0.0100 | 0.0043 |
| L7MLP | 0.1024 | 0.0017 | 0.0682 | 0.0194 | 0.0247 | 0.0170 | -0.0287 |
| L18H1 | -0.0961 | 0.0002 | -0.0395 | -0.0119 | -0.0236 | -0.0077 | -0.0136 |
| L21H4 | -0.0958 | 0.0001 | -0.0383 | -0.0073 | -0.0239 | -0.0110 | -0.0154 |
| L20H8 | -0.0953 | -0.0001 | -0.0343 | -0.0107 | -0.0246 | -0.0130 | -0.0126 |
| L10MLP | 0.0910 | 0.0005 | 0.0518 | 0.0088 | 0.0332 | -0.0130 | 0.0098 |
| L17H7 | 0.0809 | 0.0002 | 0.0284 | 0.0089 | 0.0216 | 0.0120 | 0.0097 |
| L17H3 | 0.0786 | -0.0000 | 0.0358 | 0.0122 | 0.0164 | 0.0036 | 0.0105 |
| L9H2 | 0.0759 | -0.0003 | 0.0366 | 0.0215 | 0.0038 | -0.0014 | 0.0157 |
| L20H14 | 0.0714 | 0.0002 | 0.0220 | 0.0094 | 0.0180 | 0.0102 | 0.0117 |
| L16H14 | -0.0697 | -0.0001 | -0.0293 | -0.0113 | -0.0182 | -0.0028 | -0.0080 |
| L20H3 | 0.0679 | -0.0001 | 0.0252 | 0.0023 | 0.0237 | 0.0039 | 0.0129 |
| L23MLP | 0.0679 | 0.0000 | 0.0503 | 0.0011 | 0.0075 | 0.0094 | -0.0004 |
| L17H0 | -0.0679 | -0.0000 | -0.0256 | -0.0095 | -0.0175 | -0.0073 | -0.0080 |
| L11H2 | -0.0667 | 0.0002 | -0.0319 | -0.0109 | -0.0156 | -0.0050 | -0.0035 |
| L8H15 | 0.0645 | 0.0003 | 0.0139 | -0.0001 | 0.0013 | 0.0561 | -0.0070 |
| L21H5 | 0.0639 | 0.0000 | 0.0364 | 0.0030 | 0.0082 | 0.0040 | 0.0123 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_wordorder_xlmrlarge.npz` | 2,797,893 | `8fef2e4cd8b0c98c` | attribution per pair x component x site class |
