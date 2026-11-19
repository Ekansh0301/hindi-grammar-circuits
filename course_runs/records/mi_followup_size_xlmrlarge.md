# mi_followup_size_xlmrlarge

_Follow-up, stage size, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:58 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 39.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "size"}` |
| command | `scripts/mi_followup.py --model xlmrlarge --max-rows 128 --stage size` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 7.69e-05
- **check: embedding output patched everywhere, fresh pairs: ratio of sums / worst pair (bits)**: 0.999999 / 8.82e-06
- **frozen circuit (step 4 selection half): 10 heads**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2
- **frozen circuit: top 5 MLPs**: L19MLP, L20MLP, L21MLP, L18MLP, L17MLP
- **fresh pairs built / skipped / with a gap above --min-gap**: 471 / 0 / 402

## By reordering size: four size bins (as the slide)


| size | pairs | documents | mean words | mean gap (bits) | share: 10 heads | share: MLP 1 | share: 5 MLPs jointly |
|---|---|---|---|---|---|---|---|
| 1 | 209 | 178 | 19.1818 | 0.3475 | 0.488 [0.386, 0.605] | 0.380 [0.316, 0.469] | 0.723 [0.618, 0.839] |
| 2-3 | 152 | 133 | 20.3026 | 0.7480 | 0.468 [0.415, 0.535] | 0.346 [0.310, 0.387] | 0.808 [0.762, 0.858] |
| 4-7 | 78 | 72 | 24.0128 | 0.7510 | 0.478 [0.423, 0.539] | 0.369 [0.327, 0.417] | 0.808 [0.739, 0.878] |
| 8+ | 32 | 31 | 25.8750 | 0.6753 | 0.600 [0.509, 0.715] | 0.417 [0.356, 0.507] | 0.817 [0.740, 0.931] |


## By reordering size: three size groups (the tests)


| size | pairs | documents | mean words | mean gap (bits) | share: 10 heads | share: MLP 1 | share: 5 MLPs jointly |
|---|---|---|---|---|---|---|---|
| 1 | 209 | 178 | 19.1818 | 0.3475 | 0.488 [0.386, 0.605] | 0.380 [0.316, 0.469] | 0.723 [0.618, 0.839] |
| 2-3 | 152 | 133 | 20.3026 | 0.7480 | 0.468 [0.415, 0.535] | 0.346 [0.310, 0.387] | 0.808 [0.762, 0.858] |
| 4+ | 110 | 100 | 24.5545 | 0.7299 | 0.509 [0.459, 0.566] | 0.382 [0.345, 0.422] | 0.811 [0.756, 0.867] |


## Each MLP alone, by size group (ratio of sums)


| size | MLP 1 | MLP 2 | MLP 3 | MLP 4 | MLP 5 |
|---|---|---|---|---|---|
| 1 | 0.3799 | 0.2999 | 0.2750 | 0.3260 | 0.2296 |
| 2-3 | 0.3461 | 0.3066 | 0.3011 | 0.2913 | 0.1967 |
| 4+ | 0.3817 | 0.3093 | 0.3290 | 0.2917 | 0.1903 |


## Where the top 5 heads act: mean share of the gap restored when patched at one site class only


| size | special | moved_heads | moved_psp | moved_other | verb | unmoved |
|---|---|---|---|---|---|---|
| 1 | -0.0001 | 0.0252 | 0.0074 | 0.0257 | 0.0087 | 0.0026 |
| 2-3 | -0.0001 | 0.0247 | 0.0085 | 0.0127 | 0.0068 | 0.0104 |
| 4+ | -0.0004 | 0.0297 | 0.0176 | 0.0140 | 0.0061 | 0.0054 |


## Where the top 5 MLPs act: mean share of the gap restored when patched at one site class only


| size | special | moved_heads | moved_psp | moved_other | verb | unmoved |
|---|---|---|---|---|---|---|
| 1 | -0.0007 | 0.1142 | 0.0430 | 0.0985 | 0.0426 | 0.0180 |
| 2-3 | -0.0003 | 0.1157 | 0.0403 | 0.0513 | 0.0353 | 0.0483 |
| 4+ | 0.0002 | 0.1350 | 0.0632 | 0.0557 | 0.0359 | 0.0189 |


## Primary: the 4+ group minus single swaps


| quantity | 4+ minus single swaps | document bootstrap 95% | declared rule |
|---|---|---|---|
| 10 heads, faithfulness | 0.0212 | [-0.109, 0.134] | inconclusive |
| 5 MLPs jointly | 0.0874 | [-0.042, 0.214] | inconclusive |

- **DECISION (declared rule: both within +-0.10 = size-independent; otherwise either excludes 0 = size-dependent; else inconclusive)**: inconclusive
- **Spearman of reordering size with the per-pair gap (bits), fresh pairs above the floor**: 0.309

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `size_wordorder_xlmrlarge.npz` | 128,786 | `b3d9ab2c8f5e4b14` | per fresh pair: the circuit's patches (10 heads, 5 MLPs singly and jointly) and the top 10 components per site class |
