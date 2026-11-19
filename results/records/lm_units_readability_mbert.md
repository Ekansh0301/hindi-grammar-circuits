# lm_units_readability_mbert

_readability for mbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:12 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 1.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 24, "check_against": null, "flush_every": 250, "limit": 500, "model": "bert-base-multilingual-cased", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "shard": 0, "tag": "mbert", "what": "readability", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model bert-base-multilingual-cased --tag mbert --what readability --limit 500 --batch-size 24 --sentences <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt` |


- **sentences (8 to 40 words, seed 707)**: 500
- **source**: <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt

| layer | nats per subtoken | minus final layer | readable |
|---|---|---|---|
| 0 | 18.357 | 15.010 | no |
| 1 | 18.288 | 14.942 | no |
| 2 | 15.865 | 12.518 | no |
| 3 | 14.334 | 10.987 | no |
| 4 | 13.005 | 9.658 | no |
| 5 | 11.552 | 8.205 | no |
| 6 | 11.227 | 7.881 | no |
| 7 | 12.388 | 9.041 | no |
| 8 | 12.737 | 9.390 | no |
| 9 | 13.278 | 9.931 | no |
| 10 | 13.329 | 9.983 | no |
| 11 | 12.945 | 9.599 | no |
| 12 | 3.347 | 0.000 | yes |
