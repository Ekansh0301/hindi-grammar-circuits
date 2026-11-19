# lm_units_words_indicbert_jacobian

_words for indicbert_jacobian on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 12:21 |
| script | `rq1_lm_units.py` (sha256 `0eefa4b57fe97a67`) |
| host | gnode (Linux) |
| duration | 77.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "indicbert_jacobian", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_indicbert.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert_jacobian --what words --batch-size 32 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_indicbert.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_indicbert.pt
- **layers (including embeddings)**: 13
- **pairs written this run**: 8,923
- **skipped (too long or empty; causal states: token multisets differ)**: 0

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `words_indicbert_jacobian_s0_part0000.csv.gz` | 760,566 | `bd34c32e3e6b1296` | words, part 0 (written this run) |
| `words_indicbert_jacobian_s0_part0001.csv.gz` | 547,336 | `7f428e05b297404a` | words, part 1 (written this run) |
| `words_indicbert_jacobian_s0_part0002.csv.gz` | 673,875 | `4ae7069ee8370f00` | words, part 2 (written this run) |
| `words_indicbert_jacobian_s0_part0003.csv.gz` | 717,461 | `eea87f83efd0a45b` | words, part 3 (written this run) |
| `words_indicbert_jacobian_s0_part0004.csv.gz` | 654,137 | `8f0e5003d05d535b` | words, part 4 (written this run) |
| `words_indicbert_jacobian_s0_part0005.csv.gz` | 552,096 | `795db3f8f62d11d6` | words, part 5 (written this run) |
| `words_indicbert_jacobian_s0_part0006.csv.gz` | 575,902 | `aa68f7c995dfde77` | words, part 6 (written this run) |
| `words_indicbert_jacobian_s0_part0007.csv.gz` | 637,525 | `960d833391ba6192` | words, part 7 (written this run) |
| `words_indicbert_jacobian_s0_part0008.csv.gz` | 808,264 | `ee637e3e1af0e5ab` | words, part 8 (written this run) |
| `words_indicbert_jacobian_s0_part0009.csv.gz` | 626,672 | `0f6acf76d584e900` | words, part 9 (written this run) |
| `words_indicbert_jacobian_s0_part0010.csv.gz` | 467,561 | `8df25587441711be` | words, part 10 (written this run) |
| `words_indicbert_jacobian_s0_part0011.csv.gz` | 465,155 | `717ad8951bc63d29` | words, part 11 (written this run) |
| `words_indicbert_jacobian_s0_part0012.csv.gz` | 456,050 | `eab0a325e9d4b79d` | words, part 12 (written this run) |
| `words_indicbert_jacobian_s0_part0013.csv.gz` | 497,431 | `f0edd179bd236919` | words, part 13 (written this run) |
| `words_indicbert_jacobian_s0_part0014.csv.gz` | 528,902 | `537d5a13f311061d` | words, part 14 (written this run) |
| `words_indicbert_jacobian_s0_part0015.csv.gz` | 772,627 | `025506ba57e482cf` | words, part 15 (written this run) |
| `words_indicbert_jacobian_s0_part0016.csv.gz` | 812,028 | `9ed2dadb52db40b0` | words, part 16 (written this run) |
| `words_indicbert_jacobian_s0_part0017.csv.gz` | 776,335 | `6359b0f13da638fd` | words, part 17 (written this run) |
| `words_indicbert_jacobian_s0_part0018.csv.gz` | 584,253 | `2f5c37568ee2716b` | words, part 18 (written this run) |
| `words_indicbert_jacobian_s0_part0019.csv.gz` | 539,824 | `502e30fc1d14c0ec` | words, part 19 (written this run) |
| `words_indicbert_jacobian_s0_part0020.csv.gz` | 477,229 | `c28e261a4a6ed04a` | words, part 20 (written this run) |
| `words_indicbert_jacobian_s0_part0021.csv.gz` | 433,041 | `0e2d6243bb63ba8e` | words, part 21 (written this run) |
| `words_indicbert_jacobian_s0_part0022.csv.gz` | 447,841 | `f5d313d199631296` | words, part 22 (written this run) |
| `words_indicbert_jacobian_s0_part0023.csv.gz` | 454,777 | `694599af018bd776` | words, part 23 (written this run) |
| `words_indicbert_jacobian_s0_part0024.csv.gz` | 455,096 | `a66f7b38ecc1eb9a` | words, part 24 (written this run) |
| `words_indicbert_jacobian_s0_part0025.csv.gz` | 462,530 | `e63870b0dfa83040` | words, part 25 (written this run) |
| `words_indicbert_jacobian_s0_part0026.csv.gz` | 440,501 | `9e256890063ebb31` | words, part 26 (written this run) |
| `words_indicbert_jacobian_s0_part0027.csv.gz` | 487,446 | `6cf1e3f48913ed57` | words, part 27 (written this run) |
| `words_indicbert_jacobian_s0_part0028.csv.gz` | 460,628 | `d4de931e1098e912` | words, part 28 (written this run) |
| `words_indicbert_jacobian_s0_part0029.csv.gz` | 458,694 | `c38671d3d18140a2` | words, part 29 (written this run) |
| `words_indicbert_jacobian_s0_part0030.csv.gz` | 431,793 | `f81bb584896f987c` | words, part 30 (written this run) |
| `words_indicbert_jacobian_s0_part0031.csv.gz` | 454,002 | `cdd0bc3ea028bebf` | words, part 31 (written this run) |
| `words_indicbert_jacobian_s0_part0032.csv.gz` | 413,877 | `11faffe2371fcba8` | words, part 32 (written this run) |
| `words_indicbert_jacobian_s0_part0033.csv.gz` | 423,901 | `df1ef039d1a21406` | words, part 33 (written this run) |
| `words_indicbert_jacobian_s0_part0034.csv.gz` | 441,455 | `7377c6c29e6ab791` | words, part 34 (written this run) |
| `words_indicbert_jacobian_s0_part0035.csv.gz` | 297,611 | `053a3c66030fe9a4` | words, part 35 (written this run) |
