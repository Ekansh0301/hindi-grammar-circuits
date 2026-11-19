# mi_followup_case_agreement_xlmrlarge

_Follow-up, stage case_agreement, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 15:30 |
| script | `mi_followup.py` (sha256 `69a9975e7a85601e`) |
| host | gnode (Linux) |
| duration | 22.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "case_agreement"}` |
| command | `scripts/mi_followup.py --model xlmrlarge --max-rows 128 --stage case_agreement` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
- **frozen circuit: the 5 MLPs**: L21MLP, L20MLP, L22MLP, L19MLP, L23MLP
- **check: unedited version against the metric stage's M_none and M_obj, orders / worst (bits)**: 2137 / 3.55e-15
- **check: embedding output patched everywhere recovers the clean margin, first items**: 5 items, within 5e-3 bits
- **fresh orders read / entering (all three versions built) / skipped**: 2179 / 2137 / 42

## Per version


| version | orders | correct preferred (M > 0) | mean M (bits) | mean M, object masked | mean gap (bits) | 10 heads: share of the gap restored | 5 MLPs jointly: share | mean attention to the object, top 5 heads |
|---|---|---|---|---|---|---|---|---|
| none | 2137 | 0.9518 | 6.961 | 0.3853 | 6.576 | 0.724 [0.687, 0.760] | 0.647 [0.613, 0.688] | 0.5164 |
| ne | 2137 | 0.7534 | 3.033 | -0.7287 | 3.762 | 0.750 [0.692, 0.816] | 0.607 [0.564, 0.653] | 0.3606 |
| ctl | 2137 | 0.9345 | 6.443 | 0.2919 | 6.151 | 0.725 [0.689, 0.762] | 0.646 [0.612, 0.684] | 0.4945 |

Step 4's circuit was found on variant orders with the object not adjacent to the verb. The table below is the same, restricted to those orders (the fresh set also holds the attested orders and adjacent objects).


## Per version, variant orders with the object not adjacent only


| version | orders | mean M (bits) | mean gap (bits) | 10 heads: share | 5 MLPs jointly: share | mean attention to the object, top 5 heads |
|---|---|---|---|---|---|---|
| none | 1452 | 6.485 | 6.217 | 0.706 [0.666, 0.748] | 0.655 [0.614, 0.696] | 0.4783 |
| ne | 1452 | 2.899 | 3.749 | 0.745 [0.682, 0.815] | 0.622 [0.578, 0.668] | 0.3314 |
| ctl | 1452 | 5.864 | 5.671 | 0.711 [0.673, 0.754] | 0.654 [0.614, 0.693] | 0.4481 |


## Primary: clean margin after deleting an unrelated word minus after deleting ne (paired per order)


| mean difference (bits) | document bootstrap 95% | one-sided document sign-flip p | mean M: ne / ctl |
|---|---|---|---|
| 3.41 | [2.930, 3.912] | 9.999e-05 | 3.033 / 6.443 |

- **DECISION (declared: supported if p < 0.05 and the mean margin under ne is lower than under ctl)**: supported

## Attention to the object by head and version (mean share of the verb's attention)


| head | none | ne | ctl |
|---|---|---|---|
| L21H0 | 0.606 | 0.4636 | 0.5881 |
| L20H0 | 0.7392 | 0.6086 | 0.7083 |
| L20H2 | 0.5333 | 0.2575 | 0.5026 |
| L22H6 | 0.2993 | 0.2233 | 0.2909 |
| L19H3 | 0.4043 | 0.2501 | 0.3825 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `case_agreement_xlmrlarge.csv` | 1,360,499 | `fbf6e75fe2e5c41b` | per fresh order and version: the clean and object-masked margins, the circuit's patches, attention to the object |
