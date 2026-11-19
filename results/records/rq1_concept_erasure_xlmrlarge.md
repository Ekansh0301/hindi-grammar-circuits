# rq1_concept_erasure_xlmrlarge

_LEACE erasure of role against marker, and what it does to the order preference._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 14:38 |
| script | `rq1_concept_erasure.py` (sha256 `9d84adcba6422e0d`) |
| host | gnode (Linux) |
| duration | 575.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "conditions": ["none", "role", "marker", "control", "random"], "limit": null, "model": "xlm-roberta-large", "osv_pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_osv_transition_pairs.csv", "out_dir": "<earlier-repo>/sets/set1/Results_Checks/concept_erasure", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "permutations": 10000, "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "xlmrlarge"}` |
| command | `scripts/rq1_concept_erasure.py --tag xlmrlarge --model xlm-roberta-large --batch-size 16` |


- **layer / fit units / fit references**: 12 / 5,976 / 2,000

## Linear probes on the fit units, before and after each eraser (out of fold, grouped by reference)


| eraser | probe for | accuracy | majority rate |
|---|---|---|---|
| (no erasure) | role | 0.8794 | 0.6292 |
| (no erasure) | marker | 0.9050 | 0.4098 |
| role | role | 0.4766 | 0.6292 |
| role | marker | 0.8844 | 0.4098 |
| marker | role | 0.6757 | 0.6292 |
| marker | marker | 0.1752 | 0.4098 |
| control | role | 0.8772 | 0.6292 |
| control | marker | 0.9060 | 0.4098 |
| random | role | 0.8785 | 0.6292 |
| random | marker | 0.9056 | 0.4098 |

- **rank removed: role / marker**: 2 / 7
- **covariance rank / dimensions**: 1024 / 1024

## Per condition


| condition | held-out nats per subtoken | reference preferred, all RQ1 pairs | same, references not used to fit | OSV defence (OSV->SOV) | OSV->OSV |
|---|---|---|---|---|---|
| none | 2.2392 | 0.8090 | 0.8093 | 0.8963 | 0.9090 |
| role | 2.2450 | 0.8075 | 0.8095 | 0.8976 | 0.9029 |
| marker | 2.2632 | 0.8108 | 0.8124 | 0.8880 | 0.9141 |
| control | 2.2430 | 0.8065 | 0.8075 | 0.8915 | 0.9034 |
| random | 2.2393 | 0.8079 | 0.8086 | 0.8963 | 0.9108 |


## Change in the OSV defence and in the RQ1 preference, against no erasure and against random


| pairs | eraser | against | n | change in reference-preferred rate | document sign-flip p |
|---|---|---|---|---|---|
| OSV->SOV | role | none | 2286 | 0.001312 | 0.9524 |
| OSV->SOV | role | random | 2286 | 0.001312 | 0.9209 |
| OSV->SOV | marker | none | 2286 | -0.008311 | 0.3607 |
| OSV->SOV | marker | random | 2286 | -0.008311 | 0.4898 |
| OSV->SOV | control | none | 2286 | -0.004812 | 0.4801 |
| OSV->SOV | control | random | 2286 | -0.004812 | 0.2902 |
| OSV->SOV | random | none | 2286 | 0 | 1 |
| RQ1 pairs | role | none | 8923 | -0.001569 | 0.5746 |
| RQ1 pairs | role | random | 8923 | -0.0004483 | 0.8943 |
| RQ1 pairs | marker | none | 8923 | 0.001793 | 0.5323 |
| RQ1 pairs | marker | random | 8923 | 0.002914 | 0.2762 |
| RQ1 pairs | control | none | 8923 | -0.002578 | 0.1766 |
| RQ1 pairs | control | random | 8923 | -0.001457 | 0.4715 |
| RQ1 pairs | random | none | 8923 | -0.001121 | 0.4553 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_xlmrlargeer0_s0.csv` | 1,205,851 | `cb756edef602ed27` | RQ1 pairs, condition none |
| `osv_xlmrlargeer0.csv` | 648,352 | `ccc105b71495e1d0` | OSV transition pairs, condition none |
| `t_xlmrlargeer1_s0.csv` | 1,205,799 | `62db838bcf8a4004` | RQ1 pairs, condition role |
| `osv_xlmrlargeer1.csv` | 647,700 | `cd7a1d149dbcf8e2` | OSV transition pairs, condition role |
| `t_xlmrlargeer2_s0.csv` | 1,205,437 | `a4aee2009a94a594` | RQ1 pairs, condition marker |
| `osv_xlmrlargeer2.csv` | 647,588 | `a585cfdfa53bddb9` | OSV transition pairs, condition marker |
| `t_xlmrlargeer3_s0.csv` | 1,205,621 | `f6b13d1069ae3d03` | RQ1 pairs, condition control |
| `osv_xlmrlargeer3.csv` | 647,239 | `6cc8ccddb85abdba` | OSV transition pairs, condition control |
| `t_xlmrlargeer4_s0.csv` | 1,205,769 | `3bbe430717b00c02` | RQ1 pairs, condition random |
| `osv_xlmrlargeer4.csv` | 648,735 | `a3b4a606f6b36e93` | OSV transition pairs, condition random |
