# mi_followup_case_wordorder_xlmrlarge

_Follow-up, stage case_wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 15:07 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 9.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "case_wordorder"}` |
| command | `scripts/mi_followup.py --model xlmrlarge --max-rows 128 --stage case_wordorder` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **pairs entering (with moved_psp words, all three versions built)**: 223 of 223
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.36e-05
- **check: embedding output patched everywhere, version none: ratio of sums / worst pair (bits)**: 0.999998 / 8.82e-06
- **check: embedding output patched everywhere, version psp: ratio of sums / worst pair (bits)**: 1.000003 / 3.81e-06
- **check: embedding output patched everywhere, version ctl: ratio of sums / worst pair (bits)**: 1.000001 / 1.43e-06
Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every word's weight by n/(n-k): 'retained' is compared between psp and ctl (equal counts); its level against the unedited gap carries that factor.


## Per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 223 | 0.3312 | 1.0000 | 0.1891 | 0.557 [0.496, 0.639] | 0.2550 | 0.766 [0.720, 0.824] |
| psp | 223 | 0.3192 | 0.9638 | 0.2741 | 0.832 [0.694, 1.050] | 0.4749 | 1.440 [1.243, 1.771] |
| ctl | 223 | 0.3701 | 1.1173 | 0.2231 | 0.583 [0.508, 0.675] | 0.3318 | 0.874 [0.797, 0.961] |


## Primary: gap kept after deleting other words minus gap kept after deleting the case markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctl |
|---|---|---|---|
| 0.05087 | [-0.032, 0.143] | 0.1324 | 0.964 / 1.117 |

- **DECISION (declared: supported if p < 0.05 and the gap retained under psp is lower than under ctl)**: not supported
- **descriptive: the 5 MLPs' joint effect (bits), ctl minus psp, mean and document bootstrap 95%**: -0.143 [-0.221, -0.061]

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `case_wordorder_xlmrlarge.npz` | 33,068 | `4241003b6c05a440` | per pair and version: clean and corrupted metrics, the circuit's patches |
