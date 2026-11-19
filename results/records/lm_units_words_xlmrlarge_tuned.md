# lm_units_words_xlmrlarge_tuned

_words for xlmrlarge_tuned on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 19:26 |
| script | `rq1_lm_units.py` (sha256 `d15a374e912f6e52`) |
| host | gnode (Linux) |
| duration | 153.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "xlm-roberta-large", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "xlmrlarge_tuned", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_xlmrlarge.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model xlm-roberta-large --tag xlmrlarge_tuned --what words --batch-size 16 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_xlmrlarge.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/tuned_lens_xlmrlarge.pt
- **layers (including embeddings)**: 25
- **pairs written this run**: 8,923
- **skipped (too long or empty; causal states: token multisets differ)**: 0