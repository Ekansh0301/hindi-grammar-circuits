# mi_followup_size_muril

_Follow-up, stage size, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:34 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 18.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "size"}` |
| command | `scripts/mi_followup.py --model muril --max-rows 256 --stage size` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.85e-05
- **check: embedding output patched everywhere, fresh pairs: ratio of sums / worst pair (bits)**: 1.000000 / 5.72e-06
- **frozen circuit (step 4 selection half): 10 heads**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3
- **frozen circuit: top 5 MLPs**: L10MLP, L9MLP, L8MLP, L7MLP, L6MLP
- **fresh pairs built / skipped / with a gap above --min-gap**: 471 / 0 / 409

## By reordering size: four size bins (as the slide)


| size | pairs | documents | mean words | mean gap (bits) | share: 10 heads | share: MLP 1 | share: 5 MLPs jointly |
|---|---|---|---|---|---|---|---|
| 1 | 209 | 178 | 19.1818 | 0.4122 | 0.705 [0.622, 0.797] | 0.560 [0.506, 0.634] | 0.943 [0.868, 1.045] |
| 2-3 | 152 | 133 | 20.3026 | 0.8752 | 0.691 [0.634, 0.754] | 0.556 [0.521, 0.599] | 0.953 [0.917, 0.993] |
| 4-7 | 78 | 72 | 24.0128 | 1.0052 | 0.729 [0.644, 0.818] | 0.578 [0.533, 0.632] | 1.007 [0.965, 1.059] |
| 8+ | 32 | 31 | 25.8750 | 0.8670 | 0.761 [0.671, 0.871] | 0.604 [0.551, 0.671] | 0.955 [0.904, 1.016] |


## By reordering size: three size groups (the tests)


| size | pairs | documents | mean words | mean gap (bits) | share: 10 heads | share: MLP 1 | share: 5 MLPs jointly |
|---|---|---|---|---|---|---|---|
| 1 | 209 | 178 | 19.1818 | 0.4122 | 0.705 [0.622, 0.797] | 0.560 [0.506, 0.634] | 0.943 [0.868, 1.045] |
| 2-3 | 152 | 133 | 20.3026 | 0.8752 | 0.691 [0.634, 0.754] | 0.556 [0.521, 0.599] | 0.953 [0.917, 0.993] |
| 4+ | 110 | 100 | 24.5545 | 0.9640 | 0.738 [0.670, 0.814] | 0.585 [0.548, 0.628] | 0.993 [0.959, 1.038] |


## Each MLP alone, by size group (ratio of sums)


| size | MLP 1 | MLP 2 | MLP 3 | MLP 4 | MLP 5 |
|---|---|---|---|---|---|
| 1 | 0.5603 | 0.4720 | 0.4410 | 0.3709 | 0.2727 |
| 2-3 | 0.5556 | 0.4842 | 0.4237 | 0.3422 | 0.2115 |
| 4+ | 0.5849 | 0.4857 | 0.4598 | 0.3804 | 0.2284 |


## Where the top 5 heads act: mean share of the gap restored when patched at one site class only


| size | special | moved_heads | moved_psp | moved_other | verb | unmoved |
|---|---|---|---|---|---|---|
| 1 | -0.0000 | 0.0476 | 0.0175 | 0.0217 | 0.0063 | 0.0051 |
| 2-3 | -0.0000 | 0.0325 | 0.0117 | 0.0080 | 0.0040 | 0.0106 |
| 4+ | 0.0000 | 0.0364 | 0.0243 | 0.0147 | 0.0019 | 0.0039 |


## Where the top 5 MLPs act: mean share of the gap restored when patched at one site class only


| size | special | moved_heads | moved_psp | moved_other | verb | unmoved |
|---|---|---|---|---|---|---|
| 1 | -0.0004 | 0.1816 | 0.0761 | 0.1242 | 0.0377 | 0.0205 |
| 2-3 | -0.0003 | 0.1711 | 0.0579 | 0.0726 | 0.0499 | 0.0617 |
| 4+ | -0.0003 | 0.1876 | 0.1031 | 0.0844 | 0.0296 | 0.0265 |


## Primary: the 4+ group minus single swaps


| quantity | 4+ minus single swaps | document bootstrap 95% | declared rule |
|---|---|---|---|
| 10 heads, faithfulness | 0.0330 | [-0.094, 0.148] | inconclusive |
| 5 MLPs jointly | 0.0499 | [-0.053, 0.144] | inconclusive |

- **DECISION (declared rule: both within +-0.10 = size-independent; otherwise either excludes 0 = size-dependent; else inconclusive)**: inconclusive
- **Spearman of reordering size with the per-pair gap (bits), fresh pairs above the floor**: 0.323

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `size_wordorder_muril.npz` | 130,347 | `2653a1eeb4a596d3` | per fresh pair: the circuit's patches (10 heads, 5 MLPs singly and jointly) and the top 10 components per site class |
