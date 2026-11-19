# lm_units_words_muril_tuned

_words for muril_tuned on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 15:32 |
| script | `rq1_lm_units.py` (sha256 `d15a374e912f6e52`) |
| host | gnode (Linux) |
| duration | 70.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "muril_tuned", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_muril.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/muril-base-cased --tag muril_tuned --what words --batch-size 32 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_muril.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_muril.pt
- **layers (including embeddings)**: 13
- **pairs written this run**: 8,923
- **skipped (too long or empty; causal states: token multisets differ)**: 0