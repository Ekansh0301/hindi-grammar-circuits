# lm_units_words_mbert_jacobian

_words for mbert_jacobian on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 13:18 |
| script | `rq1_lm_units.py` (sha256 `0eefa4b57fe97a67`) |
| host | gnode (Linux) |
| duration | 106.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "bert-base-multilingual-cased", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "mbert_jacobian", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_mbert.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model bert-base-multilingual-cased --tag mbert_jacobian --what words --batch-size 24 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_mbert.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_mbert.pt
- **layers (including embeddings)**: 13
- **pairs written this run**: 8,922
- **skipped (too long or empty; causal states: token multisets differ)**: 1

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `words_mbert_jacobian_s0_part0000.csv.gz` | 786,604 | `01ee9993182e03e3` | words, part 0 (written this run) |
| `words_mbert_jacobian_s0_part0001.csv.gz` | 564,320 | `b06bee25f50c4f81` | words, part 1 (written this run) |
| `words_mbert_jacobian_s0_part0002.csv.gz` | 697,232 | `a8f72944e826ebad` | words, part 2 (written this run) |
| `words_mbert_jacobian_s0_part0003.csv.gz` | 743,194 | `1bff1622a4134b8d` | words, part 3 (written this run) |
| `words_mbert_jacobian_s0_part0004.csv.gz` | 676,165 | `125427f8486ed2cb` | words, part 4 (written this run) |
| `words_mbert_jacobian_s0_part0005.csv.gz` | 570,446 | `a9488c2a7dfb03ec` | words, part 5 (written this run) |
| `words_mbert_jacobian_s0_part0006.csv.gz` | 596,767 | `82748370eda1481f` | words, part 6 (written this run) |
| `words_mbert_jacobian_s0_part0007.csv.gz` | 658,998 | `115a6af6230d7c37` | words, part 7 (written this run) |
| `words_mbert_jacobian_s0_part0008.csv.gz` | 836,709 | `364259ea150711d0` | words, part 8 (written this run) |
| `words_mbert_jacobian_s0_part0009.csv.gz` | 645,024 | `f0fb7a0f18c8c906` | words, part 9 (written this run) |
| `words_mbert_jacobian_s0_part0010.csv.gz` | 483,110 | `18bf5320aaf4332b` | words, part 10 (written this run) |
| `words_mbert_jacobian_s0_part0011.csv.gz` | 481,030 | `bf7fcf5c8bd4c973` | words, part 11 (written this run) |
| `words_mbert_jacobian_s0_part0012.csv.gz` | 471,690 | `0556f18d1f6e9952` | words, part 12 (written this run) |
| `words_mbert_jacobian_s0_part0013.csv.gz` | 513,497 | `91046bf791e6f707` | words, part 13 (written this run) |
| `words_mbert_jacobian_s0_part0014.csv.gz` | 546,071 | `0506f56b5526ff8a` | words, part 14 (written this run) |
| `words_mbert_jacobian_s0_part0015.csv.gz` | 798,478 | `bbd4d9e323ac40af` | words, part 15 (written this run) |
| `words_mbert_jacobian_s0_part0016.csv.gz` | 840,027 | `d5df56237769afdf` | words, part 16 (written this run) |
| `words_mbert_jacobian_s0_part0017.csv.gz` | 803,267 | `84f3faef16f57b93` | words, part 17 (written this run) |
| `words_mbert_jacobian_s0_part0018.csv.gz` | 601,646 | `9a1f7bc73edf46db` | words, part 18 (written this run) |
| `words_mbert_jacobian_s0_part0019.csv.gz` | 555,271 | `8af55470470cd950` | words, part 19 (written this run) |
| `words_mbert_jacobian_s0_part0020.csv.gz` | 492,849 | `7461e97c60b24f13` | words, part 20 (written this run) |
| `words_mbert_jacobian_s0_part0021.csv.gz` | 446,181 | `4791de138461eca6` | words, part 21 (written this run) |
| `words_mbert_jacobian_s0_part0022.csv.gz` | 462,507 | `0335fc74dacd621d` | words, part 22 (written this run) |
| `words_mbert_jacobian_s0_part0023.csv.gz` | 468,998 | `b48c86fc3d8bde51` | words, part 23 (written this run) |
| `words_mbert_jacobian_s0_part0024.csv.gz` | 469,123 | `c8d4d057c8fdf51d` | words, part 24 (written this run) |
| `words_mbert_jacobian_s0_part0025.csv.gz` | 477,221 | `6554b16cc6d8391b` | words, part 25 (written this run) |
| `words_mbert_jacobian_s0_part0026.csv.gz` | 453,548 | `1a4121b31cbe532f` | words, part 26 (written this run) |
| `words_mbert_jacobian_s0_part0027.csv.gz` | 503,487 | `5f62d04edc06ffa0` | words, part 27 (written this run) |
| `words_mbert_jacobian_s0_part0028.csv.gz` | 475,106 | `344b2feb4c12ae73` | words, part 28 (written this run) |
| `words_mbert_jacobian_s0_part0029.csv.gz` | 472,978 | `889293fd56548141` | words, part 29 (written this run) |
| `words_mbert_jacobian_s0_part0030.csv.gz` | 445,270 | `3f704afa7792b12c` | words, part 30 (written this run) |
| `words_mbert_jacobian_s0_part0031.csv.gz` | 456,466 | `d57525928884b9cc` | words, part 31 (written this run) |
| `words_mbert_jacobian_s0_part0032.csv.gz` | 427,406 | `6feb4b2b95c1b638` | words, part 32 (written this run) |
| `words_mbert_jacobian_s0_part0033.csv.gz` | 437,286 | `2ab28ccee294db4c` | words, part 33 (written this run) |
| `words_mbert_jacobian_s0_part0034.csv.gz` | 455,667 | `d60c341edf55c2df` | words, part 34 (written this run) |
| `words_mbert_jacobian_s0_part0035.csv.gz` | 303,134 | `290ed1a7f853c7d5` | words, part 35 (written this run) |
