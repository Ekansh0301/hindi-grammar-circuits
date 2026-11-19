# lm_units_words_muril_jacobian

_words for muril_jacobian on Set 1 pairs._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 12:12 |
| script | `rq1_lm_units.py` (sha256 `0eefa4b57fe97a67`) |
| host | gnode (Linux) |
| duration | 69.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "check_against": null, "dtype": "auto", "flush_every": 250, "limit": null, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "n_shards": 1, "no_lens": false, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "/scratch/eg_hutb/indiccorp/extracted/hi-2_10.txt", "shard": 0, "tag": "muril_jacobian", "tuned_lens": "<earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_muril.pt", "what": "words", "windows": [1, 2, 3, 5]}` |
| command | `scripts/rq1_lm_units.py --model <earlier-repo>/local_models/muril-base-cased --tag muril_jacobian --what words --batch-size 32 --tuned-lens <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_muril.pt` |


- **pairs in shard / already written / to do**: 8,923 / 0 / 8,923
- **device**: cuda
- **model type**: masked (within_word_l2r)
- **tuned lens**: <earlier-repo>/sets/set1/Results_Checks/lm_units/jacobian_lens_muril.pt
- **layers (including embeddings)**: 13
- **pairs written this run**: 8,923
- **skipped (too long or empty; causal states: token multisets differ)**: 0

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `words_muril_jacobian_s0_part0000.csv.gz` | 770,600 | `5582ca318674f540` | words, part 0 (written this run) |
| `words_muril_jacobian_s0_part0001.csv.gz` | 553,830 | `32df0b7df5f655fd` | words, part 1 (written this run) |
| `words_muril_jacobian_s0_part0002.csv.gz` | 681,221 | `ead18d57a236dd39` | words, part 2 (written this run) |
| `words_muril_jacobian_s0_part0003.csv.gz` | 725,989 | `6e307d633b603033` | words, part 3 (written this run) |
| `words_muril_jacobian_s0_part0004.csv.gz` | 661,996 | `9d7d1364b4754a2f` | words, part 4 (written this run) |
| `words_muril_jacobian_s0_part0005.csv.gz` | 558,646 | `05afa2718c887543` | words, part 5 (written this run) |
| `words_muril_jacobian_s0_part0006.csv.gz` | 582,885 | `24a766e8b8396a22` | words, part 6 (written this run) |
| `words_muril_jacobian_s0_part0007.csv.gz` | 644,835 | `c8efe12ec5d5a3fe` | words, part 7 (written this run) |
| `words_muril_jacobian_s0_part0008.csv.gz` | 817,485 | `2a27ee4c210b5d10` | words, part 8 (written this run) |
| `words_muril_jacobian_s0_part0009.csv.gz` | 633,611 | `ec35672e372faf77` | words, part 9 (written this run) |
| `words_muril_jacobian_s0_part0010.csv.gz` | 473,172 | `e7c12d6452f91ece` | words, part 10 (written this run) |
| `words_muril_jacobian_s0_part0011.csv.gz` | 470,405 | `99fc58b0f5ad7f9f` | words, part 11 (written this run) |
| `words_muril_jacobian_s0_part0012.csv.gz` | 461,353 | `c97f74b68d390016` | words, part 12 (written this run) |
| `words_muril_jacobian_s0_part0013.csv.gz` | 502,884 | `fecae0cbe7a87159` | words, part 13 (written this run) |
| `words_muril_jacobian_s0_part0014.csv.gz` | 533,703 | `8873cd51c5fdcd77` | words, part 14 (written this run) |
| `words_muril_jacobian_s0_part0015.csv.gz` | 780,757 | `3ddb156720481e4c` | words, part 15 (written this run) |
| `words_muril_jacobian_s0_part0016.csv.gz` | 821,202 | `afc89d86f88c5ea8` | words, part 16 (written this run) |
| `words_muril_jacobian_s0_part0017.csv.gz` | 784,356 | `ee00190692daa79a` | words, part 17 (written this run) |
| `words_muril_jacobian_s0_part0018.csv.gz` | 591,170 | `46c8d7c692b5a996` | words, part 18 (written this run) |
| `words_muril_jacobian_s0_part0019.csv.gz` | 546,209 | `893b112a51a40d78` | words, part 19 (written this run) |
| `words_muril_jacobian_s0_part0020.csv.gz` | 482,411 | `25d04e504aa50b94` | words, part 20 (written this run) |
| `words_muril_jacobian_s0_part0021.csv.gz` | 437,600 | `168e95a71789c1ef` | words, part 21 (written this run) |
| `words_muril_jacobian_s0_part0022.csv.gz` | 452,576 | `19f8ca061f8fe356` | words, part 22 (written this run) |
| `words_muril_jacobian_s0_part0023.csv.gz` | 459,578 | `7d723e16b31412eb` | words, part 23 (written this run) |
| `words_muril_jacobian_s0_part0024.csv.gz` | 460,113 | `af75a193328956c2` | words, part 24 (written this run) |
| `words_muril_jacobian_s0_part0025.csv.gz` | 466,692 | `12aab6a411b93827` | words, part 25 (written this run) |
| `words_muril_jacobian_s0_part0026.csv.gz` | 444,646 | `efa59d486cbdc5de` | words, part 26 (written this run) |
| `words_muril_jacobian_s0_part0027.csv.gz` | 492,783 | `5ec549eb1986fbea` | words, part 27 (written this run) |
| `words_muril_jacobian_s0_part0028.csv.gz` | 465,656 | `8d6037e705b20c40` | words, part 28 (written this run) |
| `words_muril_jacobian_s0_part0029.csv.gz` | 463,518 | `42ecbd76cdaf993a` | words, part 29 (written this run) |
| `words_muril_jacobian_s0_part0030.csv.gz` | 436,080 | `cbedbceefa60be47` | words, part 30 (written this run) |
| `words_muril_jacobian_s0_part0031.csv.gz` | 458,538 | `bf5c40be3dca2b35` | words, part 31 (written this run) |
| `words_muril_jacobian_s0_part0032.csv.gz` | 418,050 | `69021ab6e3a97b8e` | words, part 32 (written this run) |
| `words_muril_jacobian_s0_part0033.csv.gz` | 428,440 | `2a8033af15caa4b6` | words, part 33 (written this run) |
| `words_muril_jacobian_s0_part0034.csv.gz` | 445,898 | `85157273d239f0fb` | words, part 34 (written this run) |
| `words_muril_jacobian_s0_part0035.csv.gz` | 300,418 | `d90c566616a05c3f` | words, part 35 (written this run) |
