# mi_paper_kind_xlmrlarge

_Paper experiments, stage kind, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:32 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 12.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "kind"}` |
| command | `scripts/mi_paper_edit.py --model xlmrlarge --max-rows 128 --stage kind` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **pairs built per version (none / psp / ctlk / ctls)**: 133 / 133 / 131 / 17
- **pairs entering the primary test (kind_ok, built in none, psp, ctlk) / the secondary test (ctls_ok, built in none, psp, ctls)**: 131 / 17
- **frozen circuit (step 4 selection half): 10 heads**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2
- **frozen circuit: top 5 MLPs**: L19MLP, L20MLP, L21MLP, L18MLP, L17MLP
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 2.67e-05
- **check: embedding output patched everywhere, version none: ratio of sums / worst pair (bits)**: 1.000004 / 7.63e-06
- **check: embedding output patched everywhere, version psp: ratio of sums / worst pair (bits)**: 1.000006 / 2.15e-06
- **check: embedding output patched everywhere, version ctlk: ratio of sums / worst pair (bits)**: 1.000010 / 2.10e-05
- **check: embedding output patched everywhere, version ctls: ratio of sums / worst pair (bits)**: 0.999997 / 1.10e-05
- **timing: minutes in total / minutes per pair (all versions)**: 11.82 / 0.0889
Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every word's weight by n/(n-k): 'retained' is compared between psp and a control (equal counts); its level against the unedited gap carries that factor.


## Primary (ctlk): per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 131 | 0.2883 | 1 | 0.1588 | 0.537 [0.453, 0.634] | 0.2349 | 0.819 [0.745, 0.918] |
| psp | 131 | 0.3092 | 1.072 | 0.2295 | 0.731 [0.600, 0.968] | 0.4008 | 1.249 [1.085, 1.557] |
| ctlk | 131 | 0.2818 | 0.9773 | 0.173 | 0.597 [0.504, 0.740] | 0.2766 | 0.942 [0.837, 1.118] |


## Primary (ctlk): gap kept after deleting the control words (ctlk) minus gap kept after deleting the moved markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctlk |
|---|---|---|---|
| -0.02744 | [-0.114, 0.062] | 0.725 | 1.072 / 0.977 |

- **DECISION (Primary (ctlk); declared: supported if p < 0.05 and the gap retained under psp is lower than under ctlk; inconclusive if fewer than 100 pairs enter and p >= 0.05; not supported otherwise; pairs entering: 131). 'Supported' reads: deleting the moved phrases' markers costs more than deleting as many distant listed postpositions**: not supported
- **Primary (ctlk): descriptive: the 5 MLPs' joint effect (bits), ctlk minus psp, mean and document bootstrap 95%**: -0.124 [-0.192, -0.055]
- **Primary (ctlk): descriptive: the 10 heads' effect (bits), ctlk minus psp, mean and document bootstrap 95%**: -0.056 [-0.096, -0.019]

## Secondary (ctls): per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 17 | 0.36 | 1 | 0.2171 | 0.602 [0.422, 1.110] | 0.3563 | 0.994 [0.795, 1.595] |
| psp | 17 | 0.1758 | 0.4884 | 0.1845 | 1.066 [-10.139, 9.853] | 0.3778 | 2.147 [-17.532, 17.834] |
| ctls | 17 | 0.1946 | 0.5406 | 0.1277 | 0.657 [-2.711, 4.145] | 0.2909 | 1.545 [-5.174, 8.400] |


## Secondary (ctls): gap kept after deleting the control words (ctls) minus gap kept after deleting the moved markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctls |
|---|---|---|---|
| 0.0188 | [-0.165, 0.233] | 0.4369 | 0.488 / 0.541 |

- **DECISION (Secondary (ctls); declared: supported if p < 0.05 and the gap retained under psp is lower than under ctls; inconclusive if fewer than 100 pairs enter and p >= 0.05; not supported otherwise; pairs entering: 17). 'Supported' reads: deleting the moved phrases' markers costs more than deleting as many unmoved words of the same strings nearest to a moved head**: inconclusive
- **Secondary (ctls): descriptive: the 5 MLPs' joint effect (bits), ctls minus psp, mean and document bootstrap 95%**: -0.087 [-0.231, 0.068]
- **Secondary (ctls): descriptive: the 10 heads' effect (bits), ctls minus psp, mean and document bootstrap 95%**: -0.057 [-0.151, 0.019]
- **DECISION (P6 quoted verdict; second addendum: the secondary test's if it has at least 60 pairs, else the primary's; the paper states both)**: not supported (primary ctlk: not supported, 131 pairs; secondary ctls: inconclusive, 17 pairs; quoted from the primary)
- **item record, primary test: mean distance to the nearest moved head word (per-pair means): markers / control**: 1.09 / 8.88
- **item record, primary test: genitive (का, की, के) share: markers / control**: 13/211 (6%) / 97/211 (46%)
- **item record, secondary test: mean distance to the nearest moved head word (per-pair means): markers / control**: 1.09 / 10.26
- **item record, secondary test: genitive (का, की, के) share: markers / control**: 1/19 (5%) / 1/19 (5%)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `kind_xlmrlarge.npz` | 31,332 | `a925c0e663fcda1a` | per pair and version (none, psp, ctlk, ctls; each version's own pair list ids_<version>): clean and corrupted metrics, the circuit's patches |
