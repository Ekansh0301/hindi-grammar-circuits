# lm_units_readability_xlmrlarge

_readability for xlmrlarge on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:15 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 2.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "check_against": null, "flush_every": 250, "limit": 500, "model": "xlm-roberta-large", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "shard": 0, "tag": "xlmrlarge", "what": "readability", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model xlm-roberta-large --tag xlmrlarge --what readability --limit 500 --batch-size 16 --sentences <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt` |


- **sentences (8 to 40 words, seed 707)**: 500
- **source**: <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt

| layer | nats per subtoken | minus final layer | readable |
|---|---|---|---|
| 0 | 22.336 | 20.096 | no |
| 1 | 25.645 | 23.405 | no |
| 2 | 26.550 | 24.311 | no |
| 3 | 27.943 | 25.704 | no |
| 4 | 26.074 | 23.835 | no |
| 5 | 24.705 | 22.466 | no |
| 6 | 22.523 | 20.284 | no |
| 7 | 21.068 | 18.829 | no |
| 8 | 19.772 | 17.533 | no |
| 9 | 18.148 | 15.909 | no |
| 10 | 16.192 | 13.953 | no |
| 11 | 13.286 | 11.047 | no |
| 12 | 12.196 | 9.957 | no |
| 13 | 11.436 | 9.197 | no |
| 14 | 11.281 | 9.042 | no |
| 15 | 10.523 | 8.284 | no |
| 16 | 9.377 | 7.137 | no |
| 17 | 8.687 | 6.448 | no |
| 18 | 6.550 | 4.311 | no |
| 19 | 5.511 | 3.271 | no |
| 20 | 4.801 | 2.562 | no |
| 21 | 3.817 | 1.578 | yes |
| 22 | 3.706 | 1.467 | yes |
| 23 | 3.306 | 1.067 | yes |
| 24 | 2.239 | 0.000 | yes |
