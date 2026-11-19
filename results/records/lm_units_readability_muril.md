# lm_units_readability_muril

_readability for muril on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:34 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 25.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "check_against": null, "flush_every": 250, "limit": 500, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "shard": 0, "tag": "muril", "what": "readability", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --what readability --limit 500 --batch-size 32 --sentences <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt` |


- **sentences (8 to 40 words, seed 707)**: 500
- **source**: <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt

| layer | nats per subtoken | minus final layer | readable |
|---|---|---|---|
| 0 | 85.427 | 82.678 | no |
| 1 | 102.256 | 99.507 | no |
| 2 | 87.858 | 85.109 | no |
| 3 | 70.937 | 68.188 | no |
| 4 | 65.310 | 62.562 | no |
| 5 | 70.454 | 67.706 | no |
| 6 | 88.053 | 85.304 | no |
| 7 | 96.631 | 93.882 | no |
| 8 | 92.265 | 89.517 | no |
| 9 | 96.294 | 93.545 | no |
| 10 | 100.432 | 97.683 | no |
| 11 | 114.889 | 112.140 | no |
| 12 | 2.749 | 0.000 | yes |
