# lm_units_window_indicbert_s1

_window for indicbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-22 20:34 |
| script | `rq1_lm_units.py` (sha256 `d15a374e912f6e52`) |
| host | gnode (Linux) |
| duration | 15.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti | NVIDIA GeForce RTX 4070 |
| args | `{"batch_size": 32, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "n_shards": 2, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 1, "tag": "indicbert", "tuned_lens": null, "what": "window", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --what window --batch-size 32 --shard 1 --n-shards 2` |


- **pairs in shard / already written / to do**: 4,461 / 0 / 4,461
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **layers (including embeddings)**: 13
- **pairs written this run**: 4,461
- **skipped (too long or empty; causal states: token multisets differ)**: 0