# mi_followup_case_agreement_muril

_Follow-up, stage case_agreement, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:52 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 12.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "case_agreement"}` |
| command | `scripts/mi_followup.py --model muril --max-rows 256 --stage case_agreement` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
- **frozen circuit: the 5 MLPs**: L11MLP, L10MLP, L9MLP, L8MLP, L0MLP
- **check: unedited version against the metric stage's M_none and M_obj, orders / worst (bits)**: 2137 / 3.55e-15
- **check: embedding output patched everywhere recovers the clean margin, first items**: 5 items, within 5e-3 bits
- **fresh orders read / entering (all three versions built) / skipped**: 2179 / 2137 / 42

## Per version


| version | orders | correct preferred (M > 0) | mean M (bits) | mean M, object masked | mean gap (bits) | 10 heads: share of the gap restored | 5 MLPs jointly: share | mean attention to the object, top 5 heads |
|---|---|---|---|---|---|---|---|---|
| none | 2137 | 0.941 | 7.727 | 0.8122 | 6.914 | 0.832 [0.803, 0.865] | 0.775 [0.736, 0.807] | 0.4996 |
| ne | 2137 | 0.7085 | 3.011 | -0.5985 | 3.609 | 0.817 [0.768, 0.874] | 0.687 [0.619, 0.739] | 0.359 |
| ctl | 2137 | 0.9233 | 7.186 | 0.7708 | 6.415 | 0.833 [0.802, 0.870] | 0.772 [0.732, 0.803] | 0.4771 |

Step 4's circuit was found on variant orders with the object not adjacent to the verb. The table below is the same, restricted to those orders (the fresh set also holds the attested orders and adjacent objects).


## Per version, variant orders with the object not adjacent only


| version | orders | mean M (bits) | mean gap (bits) | 10 heads: share | 5 MLPs jointly: share | mean attention to the object, top 5 heads |
|---|---|---|---|---|---|---|
| none | 1452 | 6.992 | 6.141 | 0.848 [0.810, 0.889] | 0.763 [0.711, 0.802] | 0.4577 |
| ne | 1452 | 2.563 | 3.246 | 0.848 [0.789, 0.914] | 0.675 [0.591, 0.739] | 0.3192 |
| ctl | 1452 | 6.337 | 5.514 | 0.852 [0.811, 0.901] | 0.756 [0.703, 0.796] | 0.4268 |


## Primary: clean margin after deleting an unrelated word minus after deleting ne (paired per order)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | mean M: ne / ctl |
|---|---|---|---|
| 4.175 | [3.564, 4.787] | 9.999e-05 | 3.011 / 7.186 |

- **DECISION (declared: supported if p < 0.05 and the mean margin under ne is lower than under ctl)**: supported

## Attention to the object by head and version (mean share of the verb's attention)


| head | none | ne | ctl |
|---|---|---|---|
| L10H6 | 0.6178 | 0.3515 | 0.5879 |
| L8H3 | 0.6063 | 0.3973 | 0.5785 |
| L11H1 | 0.482 | 0.386 | 0.4677 |
| L9H6 | 0.4459 | 0.3556 | 0.419 |
| L11H2 | 0.346 | 0.3044 | 0.3325 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `case_agreement_muril.csv` | 1,361,169 | `8c74d7f69328167b` | per fresh order and version: the clean and object-masked margins, the circuit's patches, attention to the object |
