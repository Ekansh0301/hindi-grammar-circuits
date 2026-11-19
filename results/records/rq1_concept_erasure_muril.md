# rq1_concept_erasure_muril

_LEACE erasure of role against marker, and what it does to the order preference._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 22:45 |
| script | `rq1_concept_erasure.py` (sha256 `9d84adcba6422e0d`) |
| host | gnode (Linux) |
| duration | 323.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "conditions": ["none", "role", "marker", "control", "random"], "limit": null, "model": "<earlier-repo>/local_models/muril-base-cased", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "muril"}` |
| command | `scripts/rq1_concept_erasure.py --tag muril --model <earlier-repo>/local_models/muril-base-cased --batch-size 32` |


- **layer / fit units / fit references**: 7 / 5,976 / 2,000

## Linear probes on the fit units, before and after each eraser (out of fold, grouped by reference)


| eraser | probe for | accuracy | majority rate |
|---|---|---|---|
| (no erasure) | role | 0.8757 | 0.6292 |
| (no erasure) | marker | 0.8690 | 0.4098 |
| role | role | 0.5443 | 0.6292 |
| role | marker | 0.8390 | 0.4098 |
| marker | role | 0.6841 | 0.6292 |
| marker | marker | 0.2478 | 0.4098 |
| control | role | 0.8698 | 0.6292 |
| control | marker | 0.8681 | 0.4098 |
| random | role | 0.8783 | 0.6292 |
| random | marker | 0.8688 | 0.4098 |

- **rank removed: role / marker**: 2 / 7
- **covariance rank / dimensions**: 768 / 768

## Per condition


| condition | held-out nats per subtoken | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|
| none | 2.7487 | 0.8204 | 0.8164 | 0.8272 | 0.8542 |
| role | 2.7932 | 0.8314 | 0.8290 | 0.8066 | 0.8481 |
| marker | 2.8379 | 0.8365 | 0.8356 | 0.8342 | 0.8634 |
| control | 2.7685 | 0.8228 | 0.8193 | 0.8250 | 0.8542 |
| random | 2.7749 | 0.8176 | 0.8145 | 0.8303 | 0.8518 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | -0.02056 | 0.05949 |
| OSV->SOV | role | random | 2286 | -0.02362 | 0.07069 |
| OSV->SOV | marker | none | 2286 | 0.006999 | 0.3834 |
| OSV->SOV | marker | random | 2286 | 0.003937 | 0.6706 |
| OSV->SOV | control | none | 2286 | -0.002187 | 0.7449 |
| OSV->SOV | control | random | 2286 | -0.005249 | 0.7706 |
| OSV->SOV | random | none | 2286 | 0.003062 | 0.7691 |
| RQ1 pairs | role | none | 8923 | 0.01109 | 0.0004 |
| RQ1 pairs | role | random | 8923 | 0.0139 | 9.999e-05 |
| RQ1 pairs | marker | none | 8923 | 0.01614 | 9.999e-05 |
| RQ1 pairs | marker | random | 8923 | 0.01894 | 9.999e-05 |
| RQ1 pairs | control | none | 8923 | 0.002466 | 0.3695 |
| RQ1 pairs | control | random | 8923 | 0.005267 | 0.07179 |
| RQ1 pairs | random | none | 8923 | -0.002802 | 0.1875 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_muriler0_s0.csv` | 1,206,350 | `65addeabe8e3c76b` | RQ1 pairs, condition none |
| `osv_muriler0.csv` | 648,229 | `853dd0750b609b26` | OSV transition pairs, condition none |
| `t_muriler1_s0.csv` | 1,206,026 | `c48b849963700fc4` | RQ1 pairs, condition role |
| `osv_muriler1.csv` | 647,224 | `5b5b45f7b8a6ec80` | OSV transition pairs, condition role |
| `t_muriler2_s0.csv` | 1,205,541 | `b2557254ff76a63d` | RQ1 pairs, condition marker |
| `osv_muriler2.csv` | 646,044 | `e83d8f77832b1758` | OSV transition pairs, condition marker |
| `t_muriler3_s0.csv` | 1,206,067 | `bc882a5406b26660` | RQ1 pairs, condition control |
| `osv_muriler3.csv` | 648,418 | `fe3fe5265defa6c3` | OSV transition pairs, condition control |
| `t_muriler4_s0.csv` | 1,206,303 | `7c2a046a686be84f` | RQ1 pairs, condition random |
| `osv_muriler4.csv` | 647,112 | `1df153aa1d81beae` | OSV transition pairs, condition random |
