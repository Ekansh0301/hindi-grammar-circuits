# lm_units_states_mbert_s0

_states for mbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:04 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 1.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 24, "check_against": null, "flush_every": 250, "limit": null, "model": "bert-base-multilingual-cased", "n_refs": 2000, "n_shards": 2, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "mbert", "what": "states", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model bert-base-multilingual-cased --tag mbert --what states --batch-size 24 --shard 0 --n-shards 2` |


- **pairs in shard / already written / to do**: 4,462 / 0 / 4,462
- **device**: cuda
- **layers (including embeddings)**: 13
- **pairs written this run**: 4,462
- **skipped (too long or empty)**: 0
- **largest |pooled pre-LayerNorm difference| (identity check, must be ~0)**: 1.19e-07