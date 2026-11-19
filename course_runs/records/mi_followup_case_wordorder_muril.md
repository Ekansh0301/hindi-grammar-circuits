# mi_followup_case_wordorder_muril

_Follow-up, stage case_wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:39 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 4.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "case_wordorder"}` |
| command | `scripts/mi_followup.py --model muril --max-rows 256 --stage case_wordorder` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **pairs entering (with moved_psp words, all three versions built)**: 223 of 223
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.14e-05
- **check: embedding output patched everywhere, version none: ratio of sums / worst pair (bits)**: 1.000000 / 5.72e-06
- **check: embedding output patched everywhere, version psp: ratio of sums / worst pair (bits)**: 1.000010 / 1.10e-05
- **check: embedding output patched everywhere, version ctl: ratio of sums / worst pair (bits)**: 0.999994 / 1.24e-05
Each version's metric is minus the mean surprisal over the words left, so deleting k words rescales every word's weight by n/(n-k): 'retained' is compared between psp and ctl (equal counts); its level against the unedited gap carries that factor.


## Per version


| version | pairs | mean gap (bits) | gap retained (share of the unedited gap) | 10 heads: mean effect (bits) | 10 heads: share of that version's gap | 5 MLPs jointly: mean effect (bits) | 5 MLPs jointly: share of that version's gap |
|---|---|---|---|---|---|---|---|
| none | 223 | 0.4306 | 1.0000 | 0.3245 | 0.745 [0.684, 0.822] | 0.4090 | 0.941 [0.903, 0.985] |
| psp | 223 | 0.4063 | 0.9435 | 0.4641 | 1.130 [0.965, 1.390] | 0.5925 | 1.423 [1.258, 1.686] |
| ctl | 223 | 0.4511 | 1.0476 | 0.3653 | 0.801 [0.724, 0.900] | 0.4624 | 1.014 [0.955, 1.088] |


## Primary: gap kept after deleting other words minus gap kept after deleting the case markers (paired per pair)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | retained psp / ctl |
|---|---|---|---|
| 0.04483 | [-0.051, 0.145] | 0.1875 | 0.944 / 1.048 |

- **DECISION (declared: supported if p < 0.05 and the gap retained under psp is lower than under ctl)**: not supported
- **descriptive: the 5 MLPs' joint effect (bits), ctl minus psp, mean and document bootstrap 95%**: -0.130 [-0.213, -0.044]

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `case_wordorder_muril.npz` | 33,413 | `c05b0813f9edf0b2` | per pair and version: clean and corrupted metrics, the circuit's patches |
