# lm_units_words_xlmrlarge_jacobian

_words for xlmrlarge_jacobian on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 16:33 |
| script | `rq1_lm_units.py` (sha256 `0eefa4b57fe97a67`) |
| host | gnode (Linux) |
| duration | 154.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "xlm-roberta-large", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "xlmrlarge_jacobian", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_xlmrlarge.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model xlm-roberta-large --tag xlmrlarge_jacobian --what words --batch-size 16 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_xlmrlarge.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_xlmrlarge.pt
- **layers (including embeddings)**: 25
- **pairs written this run**: 8,923
- **skipped (too long or empty; causal states: token multisets differ)**: 0

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `words_xlmrlarge_jacobian_s0_part0000.csv.gz` | 1,330,750 | `5dd3839dbfe6d103` | words, part 0 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0001.csv.gz` | 954,648 | `e3f86cd198a9aa83` | words, part 1 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0002.csv.gz` | 1,173,495 | `70b7228778734ff6` | words, part 2 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0003.csv.gz` | 1,250,882 | `425a54307aafab55` | words, part 3 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0004.csv.gz` | 1,144,542 | `116003f8cb10af41` | words, part 4 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0005.csv.gz` | 963,866 | `4f7aa181be4efa68` | words, part 5 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0006.csv.gz` | 1,005,220 | `031d62aeb2e6faa4` | words, part 6 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0007.csv.gz` | 1,115,117 | `fb2d9cbc4b2186a5` | words, part 7 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0008.csv.gz` | 1,418,096 | `fc93de96fdfc5843` | words, part 8 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0009.csv.gz` | 1,097,033 | `0fab86107d9581c0` | words, part 9 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0010.csv.gz` | 814,795 | `32fbb31ab63da0dc` | words, part 10 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0011.csv.gz` | 812,425 | `b2a8ba7877ead6e5` | words, part 11 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0012.csv.gz` | 795,316 | `d293c5a8691a00da` | words, part 12 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0013.csv.gz` | 867,553 | `89e45d32415ce952` | words, part 13 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0014.csv.gz` | 921,982 | `4169e137395f73d4` | words, part 14 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0015.csv.gz` | 1,351,620 | `b2d60f00044b5d1c` | words, part 15 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0016.csv.gz` | 1,424,516 | `4fa4bbb876ba717e` | words, part 16 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0017.csv.gz` | 1,362,073 | `c3d3b60e8c4f79de` | words, part 17 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0018.csv.gz` | 1,022,464 | `9dd323e88c9a4f3c` | words, part 18 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0019.csv.gz` | 943,310 | `02da5e622facb0ec` | words, part 19 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0020.csv.gz` | 831,777 | `4076c338dc34c92b` | words, part 20 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0021.csv.gz` | 755,681 | `0f091d6a5930a843` | words, part 21 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0022.csv.gz` | 779,493 | `f70c265cd3398bc3` | words, part 22 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0023.csv.gz` | 791,806 | `ee0bc2b7eb6be778` | words, part 23 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0024.csv.gz` | 791,796 | `f4a0da815df9d0af` | words, part 24 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0025.csv.gz` | 806,771 | `ea5587d98133b1a8` | words, part 25 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0026.csv.gz` | 767,641 | `f6eef872f0453abf` | words, part 26 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0027.csv.gz` | 851,677 | `646134e967fe0031` | words, part 27 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0028.csv.gz` | 802,310 | `0f1fac9efc88262d` | words, part 28 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0029.csv.gz` | 799,675 | `4200319d913a4bb0` | words, part 29 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0030.csv.gz` | 753,760 | `26fbb01cbed6c913` | words, part 30 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0031.csv.gz` | 793,833 | `6f5e3e7969d52e67` | words, part 31 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0032.csv.gz` | 722,326 | `ae4030624a9e6b04` | words, part 32 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0033.csv.gz` | 739,348 | `d0f561bd70f8b9f3` | words, part 33 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0034.csv.gz` | 769,228 | `61a4d5aa2719e568` | words, part 34 (written this run) |
| `words_xlmrlarge_jacobian_s0_part0035.csv.gz` | 518,718 | `9d7979aa3ac0fd8c` | words, part 35 (written this run) |
