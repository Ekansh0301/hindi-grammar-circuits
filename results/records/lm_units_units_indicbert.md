# lm_units_units_indicbert

_units for indicbert on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 10:11 |
| script | `rq1_lm_units.py` (sha256 `891df88594c94166`) |
| host | gnode (Linux) |
| duration | 0.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "check_against": null, "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "indicbert", "what": "units", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --what units --n-refs 2000` |


- **references / units / skipped references**: 2,000 / 5,976 / 0

| case label | units |
|---|---|
| 0 | 2449 |
| other | 970 |
| me | 761 |
| ne | 653 |
| ko | 496 |
| se | 327 |
| par | 317 |
| ka | 3 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `units_indicbert.npz` | 129,919,718 | `0d1cce35d9020635` | unit states, every layer |
