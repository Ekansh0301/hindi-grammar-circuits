# lm_units_words_indicbert_s1

_words for indicbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 09:43 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 12.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "check_against": "sets/set1/Results_Checks/t_indicbert_within_word_l2r_s1.csv", "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_shards": 2, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "shard": 1, "tag": "indicbert", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --what words --batch-size 32 --shard 1 --n-shards 2 --check-against sets/set1/Results_Checks/t_indicbert_within_word_l2r_s1.csv` |


- **pairs in shard / already written / to do**: 4,461 / 0 / 4,461
- **device**: cuda
- **layers (including embeddings)**: 13
- **pairs written this run**: 4,461
- **skipped (too long or empty)**: 0
- **pairs compared with the existing sentence scores**: 4,461
- **largest |summed word surprisal − existing Sum| (bits)**: 0.0006719