# lm_units_readability_indicbert

_readability for indicbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:10 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 1.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "check_against": null, "flush_every": 250, "limit": 500, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "shard": 0, "tag": "indicbert", "what": "readability", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --what readability --limit 500 --batch-size 32 --sentences <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt` |


- **sentences (8 to 40 words, seed 707)**: 500
- **source**: <earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt

| layer | nats per subtoken | minus final layer | readable |
|---|---|---|---|
| 0 | 14.672 | 12.358 | no |
| 1 | 11.381 | 9.067 | no |
| 2 | 8.052 | 5.738 | no |
| 3 | 7.930 | 5.616 | no |
| 4 | 8.622 | 6.308 | no |
| 5 | 7.643 | 5.330 | no |
| 6 | 6.825 | 4.511 | no |
| 7 | 6.867 | 4.554 | no |
| 8 | 6.108 | 3.794 | no |
| 9 | 6.115 | 3.801 | no |
| 10 | 4.311 | 1.998 | yes |
| 11 | 3.336 | 1.023 | yes |
| 12 | 2.314 | 0.000 | yes |
