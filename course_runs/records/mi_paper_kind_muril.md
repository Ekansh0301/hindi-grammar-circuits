# mi_paper_kind_muril

_Paper experiments, stage kind, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:50 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 3.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "kind"}` |
| command | `scripts/mi_paper_edit.py --model muril --max-rows 256 --stage kind` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **pairs built per version (none / psp / ctlk / ctls)**: 133 / 133 / 131 / 17
- **pairs entering the primary test (kind_ok, built in none, psp, ctlk) / the secondary test (ctls_ok, built in none, psp, ctls)**: 131 / 17
- **frozen circuit (step 4 selection half): 10 heads**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3
- **frozen circuit: top 5 MLPs**: L10MLP, L9MLP, L8MLP, L7MLP, L6MLP
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 2.96e-05
- **check: embedding output patched everywhere, version none: ratio of sums / worst pair (bits)**: 1.000004 / 5.72e-06
- **check: embedding output patched everywhere, version psp: ratio of sums / worst pair (bits)**: 1.000032 / 1.10e-05
- **check: embedding output patched everywhere, version ctlk: ratio of sums / worst pair (bits)**: 1.000000 / 3.58e-06
- **check: embedding output patched everywhere, version ctls: ratio of sums / worst pair (bits)**: 1.000006 / 6.68e-06
- **timing: minutes in total / minutes per pair (all versions)**: 3.09 / 0.0232
Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every word's weight by n/(n-k): 'retained' is compared between psp and a control (equal counts); its level against the unedited gap carries that factor.


## Primary (ctlk): per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 131 | 0.3837 | 1 | 0.2943 | 0.754 [0.672, 0.855] | 0.3713 | 0.959 [0.906, 1.035] |
| psp | 131 | 0.4131 | 1.077 | 0.4512 | 1.078 [0.897, 1.396] | 0.5547 | 1.312 [1.136, 1.620] |
| ctlk | 131 | 0.4153 | 1.082 | 0.3251 | 0.768 [0.667, 0.894] | 0.4412 | 1.043 [0.957, 1.175] |


## Primary (ctlk): gap kept after deleting the control words (ctlk) minus gap kept after deleting the moved markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctlk |
|---|---|---|---|
| 0.002138 | [-0.116, 0.122] | 0.4951 | 1.077 / 1.082 |

- **DECISION (Primary (ctlk); declared: supported if p < 0.05 and the gap retained under psp is lower than under ctlk; inconclusive if fewer than 100 pairs enter and p >= 0.05; not supported otherwise; pairs entering: 131). 'Supported' reads: deleting the moved phrases' markers costs more than deleting as many distant listed postpositions**: not supported
- **Primary (ctlk): descriptive: the 5 MLPs' joint effect (bits), ctlk minus psp, mean and document bootstrap 95%**: -0.113 [-0.221, -0.010]
- **Primary (ctlk): descriptive: the 10 heads' effect (bits), ctlk minus psp, mean and document bootstrap 95%**: -0.126 [-0.209, -0.051]

## Secondary (ctls): per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 17 | 0.4403 | 1 | 0.3382 | 0.735 [0.538, 0.919] | 0.4326 | 0.965 [0.774, 1.148] |
| psp | 17 | 0.6028 | 1.369 | 0.4771 | 0.781 [0.602, 1.187] | 0.731 | 1.198 [0.992, 1.792] |
| ctls | 17 | 0.3903 | 0.8864 | 0.331 | 0.836 [0.678, 1.503] | 0.4159 | 1.038 [0.847, 1.184] |


## Secondary (ctls): gap kept after deleting the control words (ctls) minus gap kept after deleting the moved markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctls |
|---|---|---|---|
| -0.2126 | [-0.471, 0.013] | 0.9492 | 1.369 / 0.886 |

- **DECISION (Secondary (ctls); declared: supported if p < 0.05 and the gap retained under psp is lower than under ctls; inconclusive if fewer than 100 pairs enter and p >= 0.05; not supported otherwise; pairs entering: 17). 'Supported' reads: deleting the moved phrases' markers costs more than deleting as many unmoved words of the same strings nearest to a moved head**: inconclusive
- **Secondary (ctls): descriptive: the 5 MLPs' joint effect (bits), ctls minus psp, mean and document bootstrap 95%**: -0.315 [-0.582, -0.102]
- **Secondary (ctls): descriptive: the 10 heads' effect (bits), ctls minus psp, mean and document bootstrap 95%**: -0.146 [-0.321, 0.026]
- **DECISION (P6 quoted verdict; second addendum: the secondary test's if it has at least 60 pairs, else the primary's; the paper states both)**: not supported (primary ctlk: not supported, 131 pairs; secondary ctls: inconclusive, 17 pairs; quoted from the primary)
- **item record, primary test: mean distance to the nearest moved head word (per-pair means): markers / control**: 1.09 / 8.88
- **item record, primary test: genitive (का, की, के) share: markers / control**: 13/211 (6%) / 97/211 (46%)
- **item record, secondary test: mean distance to the nearest moved head word (per-pair means): markers / control**: 1.09 / 10.26
- **item record, secondary test: genitive (का, की, के) share: markers / control**: 1/19 (5%) / 1/19 (5%)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `kind_muril.npz` | 31,605 | `7896bc78d9072b6a` | per pair and version (none, psp, ctlk, ctls; each version's own pair list ids_<version>): clean and corrupted metrics, the circuit's patches |
