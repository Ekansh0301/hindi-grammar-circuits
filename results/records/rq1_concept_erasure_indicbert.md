# rq1_concept_erasure_indicbert

_LEACE erasure of role against marker, and what it does to the order preference._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 00:56 |
| script | `rq1_concept_erasure.py` (sha256 `9d84adcba6422e0d`) |
| host | gnode (Linux) |
| duration | 332.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "conditions": ["none", "role", "marker", "control", "random"], "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "indicbert"}` |
| command | `scripts/rq1_concept_erasure.py --tag indicbert --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --batch-size 32` |


- **layer / fit units / fit references**: 7 / 5,976 / 2,000

## Linear probes on the fit units, before and after each eraser (out of fold, grouped by reference)


| eraser | probe for | accuracy | majority rate |
|---|---|---|---|
| (no erasure) | role | 0.8884 | 0.6292 |
| (no erasure) | marker | 0.8758 | 0.4098 |
| role | role | 0.5475 | 0.6292 |
| role | marker | 0.8576 | 0.4098 |
| marker | role | 0.7013 | 0.6292 |
| marker | marker | 0.2587 | 0.4098 |
| control | role | 0.8852 | 0.6292 |
| control | marker | 0.8767 | 0.4098 |
| random | role | 0.8899 | 0.6292 |
| random | marker | 0.8743 | 0.4098 |

- **rank removed: role / marker**: 2 / 7
- **covariance rank / dimensions**: 768 / 768

## Per condition


| condition | held-out nats per subtoken | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|
| none | 2.3137 | 0.7865 | 0.7843 | 0.7826 | 0.7928 |
| role | 2.4034 | 0.7932 | 0.7882 | 0.7979 | 0.7980 |
| marker | 2.5648 | 0.8001 | 0.7972 | 0.8036 | 0.7966 |
| control | 2.3832 | 0.7852 | 0.7832 | 0.7817 | 0.7919 |
| random | 2.3470 | 0.7871 | 0.7839 | 0.7769 | 0.7928 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | 0.01531 | 0.1772 |
| OSV->SOV | role | random | 2286 | 0.021 | 0.08889 |
| OSV->SOV | marker | none | 2286 | 0.021 | 0.0336 |
| OSV->SOV | marker | random | 2286 | 0.02668 | 0.0287 |
| OSV->SOV | control | none | 2286 | -0.0008749 | 0.9508 |
| OSV->SOV | control | random | 2286 | 0.004812 | 0.5507 |
| OSV->SOV | random | none | 2286 | -0.005687 | 0.4528 |
| RQ1 pairs | role | none | 8923 | 0.006724 | 0.0233 |
| RQ1 pairs | role | random | 8923 | 0.006164 | 0.0425 |
| RQ1 pairs | marker | none | 8923 | 0.01356 | 9.999e-05 |
| RQ1 pairs | marker | random | 8923 | 0.013 | 0.0005999 |
| RQ1 pairs | control | none | 8923 | -0.001345 | 0.5815 |
| RQ1 pairs | control | random | 8923 | -0.001905 | 0.5167 |
| RQ1 pairs | random | none | 8923 | 0.0005603 | 0.8501 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_indicberter0_s0.csv` | 1,207,926 | `51d44eea27b8225a` | RQ1 pairs, condition none |
| `osv_indicberter0.csv` | 649,832 | `8d1f8765b1389384` | OSV transition pairs, condition none |
| `t_indicberter1_s0.csv` | 1,207,603 | `1acc8b05f1596216` | RQ1 pairs, condition role |
| `osv_indicberter1.csv` | 647,945 | `ca03633fdd3a1974` | OSV transition pairs, condition role |
| `t_indicberter2_s0.csv` | 1,206,741 | `5931a037cf7c38a7` | RQ1 pairs, condition marker |
| `osv_indicberter2.csv` | 648,544 | `6dc49059f0e06d83` | OSV transition pairs, condition marker |
| `t_indicberter3_s0.csv` | 1,207,585 | `25114d7a813e6d37` | RQ1 pairs, condition control |
| `osv_indicberter3.csv` | 648,947 | `4faadbebf5c9782c` | OSV transition pairs, condition control |
| `t_indicberter4_s0.csv` | 1,207,518 | `3431742b01ad07c8` | RQ1 pairs, condition random |
| `osv_indicberter4.csv` | 648,323 | `426107837f0cc475` | OSV transition pairs, condition random |
