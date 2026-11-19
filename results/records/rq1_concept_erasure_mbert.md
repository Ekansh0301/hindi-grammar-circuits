# rq1_concept_erasure_mbert

_LEACE erasure of role against marker, and what it does to the order preference._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 13:11 |
| script | `rq1_concept_erasure.py` (sha256 `9d84adcba6422e0d`) |
| host | gnode (Linux) |
| duration | 625.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "conditions": ["none", "role", "marker", "control", "random"], "limit": null, "model": "bert-base-multilingual-cased", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "mbert"}` |
| command | `scripts/rq1_concept_erasure.py --tag mbert --model bert-base-multilingual-cased --batch-size 24` |


- **layer / fit units / fit references**: 8 / 5,976 / 2,000

## Linear probes on the fit units, before and after each eraser (out of fold, grouped by reference)


| eraser | probe for | accuracy | majority rate |
|---|---|---|---|
| (no erasure) | role | 0.8395 | 0.6292 |
| (no erasure) | marker | 0.8717 | 0.4098 |
| role | role | 0.5467 | 0.6292 |
| role | marker | 0.8467 | 0.4098 |
| marker | role | 0.6665 | 0.6292 |
| marker | marker | 0.2480 | 0.4098 |
| control | role | 0.8397 | 0.6292 |
| control | marker | 0.8723 | 0.4098 |
| random | role | 0.8412 | 0.6292 |
| random | marker | 0.8718 | 0.4098 |

- **rank removed: role / marker**: 2 / 7
- **covariance rank / dimensions**: 768 / 768

## Per condition


| condition | held-out nats per subtoken | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|
| none | 3.3467 | 0.7428 | 0.7447 | 0.5171 | 0.7190 |
| role | 3.3952 | 0.7346 | 0.7345 | 0.5153 | 0.7051 |
| marker | 3.4799 | 0.7468 | 0.7476 | 0.5262 | 0.7557 |
| control | 3.4047 | 0.7431 | 0.7446 | 0.5179 | 0.7274 |
| random | 3.3677 | 0.7455 | 0.7454 | 0.5249 | 0.7167 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | -0.00175 | 0.9571 |
| OSV->SOV | role | random | 2286 | -0.009624 | 0.8913 |
| OSV->SOV | marker | none | 2286 | 0.009186 | 0.8202 |
| OSV->SOV | marker | random | 2286 | 0.001312 | 0.9859 |
| OSV->SOV | control | none | 2286 | 0.0008749 | 0.9773 |
| OSV->SOV | control | random | 2286 | -0.006999 | 0.7192 |
| OSV->SOV | random | none | 2286 | 0.007874 | 0.6004 |
| RQ1 pairs | role | none | 8922 | -0.008182 | 0.005999 |
| RQ1 pairs | role | random | 8922 | -0.01087 | 0.0012 |
| RQ1 pairs | marker | none | 8922 | 0.004035 | 0.2426 |
| RQ1 pairs | marker | random | 8922 | 0.001345 | 0.719 |
| RQ1 pairs | control | none | 8922 | 0.0003362 | 0.9323 |
| RQ1 pairs | control | random | 8922 | -0.002354 | 0.4101 |
| RQ1 pairs | random | none | 8922 | 0.00269 | 0.2154 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_mberter0_s0.csv` | 1,200,356 | `25875a6ef4c7812a` | RQ1 pairs, condition none |
| `osv_mberter0.csv` | 646,633 | `186882520de1b727` | OSV transition pairs, condition none |
| `t_mberter1_s0.csv` | 1,200,561 | `a189993796ae5f07` | RQ1 pairs, condition role |
| `osv_mberter1.csv` | 647,096 | `9cb98816e2b33cd9` | OSV transition pairs, condition role |
| `t_mberter2_s0.csv` | 1,200,834 | `399726d7ca154c0d` | RQ1 pairs, condition marker |
| `osv_mberter2.csv` | 646,266 | `7d38714f68317881` | OSV transition pairs, condition marker |
| `t_mberter3_s0.csv` | 1,200,549 | `2b7257b49e18905a` | RQ1 pairs, condition control |
| `osv_mberter3.csv` | 645,369 | `98aa657c4192999c` | OSV transition pairs, condition control |
| `t_mberter4_s0.csv` | 1,200,430 | `864d83b41f2425c1` | RQ1 pairs, condition random |
| `osv_mberter4.csv` | 646,717 | `f03b2541aebd2baf` | OSV transition pairs, condition random |
