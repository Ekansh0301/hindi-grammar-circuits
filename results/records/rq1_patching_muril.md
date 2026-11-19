# rq1_patching_muril

_Interchange patching of reference states into the variant run, by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 17:21 |
| script | `rq1_patching.py` (sha256 `2ec9064efd5d7399`) |
| host | gnode (Linux) |
| duration | 76.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "layers": null, "min_gap": 0.05, "model": "<earlier-repo>/local_models/muril-base-cased", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "muril"}` |
| command | `scripts/rq1_patching.py --tag muril --model <earlier-repo>/local_models/muril-base-cased --batch-size 32` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 875
- **check: 'all' at layer 0 recovers (ratio of sums) / largest per-pair departure (bits)**: 1.000000 / 3.69e-05

| layer | recovered by moved_heads | recovered by moved_psp | recovered by moved_other | recovered by verb | recovered by unmoved |
|---|---|---|---|---|---|
| 0 | -3.6524 | -2.2856 | -3.4696 | 0.0000 | -0.4054 |
| 2 | -2.0540 | -1.0991 | -1.8512 | 0.0163 | -0.0351 |
| 4 | -0.4546 | -0.3219 | -0.7369 | 0.0347 | 0.0632 |
| 6 | 0.3353 | 0.0313 | -0.1103 | 0.0369 | 0.1127 |
| 8 | 0.6030 | 0.2081 | 0.1923 | 0.1057 | 0.1533 |
| 10 | 0.5359 | 0.1579 | 0.2060 | 0.1280 | 0.1240 |
| 12 | 0.4858 | 0.1121 | 0.1881 | 0.1109 | 0.1032 |

Recovery is the share of the variant-reference gap closed by the patch, a ratio of sums over pairs; 1 closes it, 0 leaves it, negative widens it. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_muril.csv` | 786,386 | `c95944ecb85c080a` | per pair: reference, variant, and the patched variant per condition |
