# rq1_patching_indicbert

_Interchange patching of reference states into the variant run, by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 09:03 |
| script | `rq1_patching.py` (sha256 `2ec9064efd5d7399`) |
| host | gnode (Linux) |
| duration | 77.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "layers": null, "min_gap": 0.05, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "indicbert"}` |
| command | `scripts/rq1_patching.py --tag indicbert --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --batch-size 32` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 878
- **check: 'all' at layer 0 recovers (ratio of sums) / largest per-pair departure (bits)**: 1.000000 / 7.25e-06

| layer | recovered by moved_heads | recovered by moved_psp | recovered by moved_other | recovered by verb | recovered by unmoved |
|---|---|---|---|---|---|
| 0 | -4.2207 | -2.7517 | -3.7481 | 0.0000 | -0.4018 |
| 2 | -1.2253 | -0.7102 | -1.3054 | 0.0358 | 0.0212 |
| 4 | -0.0633 | -0.1271 | -0.5062 | 0.0485 | 0.0933 |
| 6 | 0.3991 | 0.1118 | -0.0701 | 0.0731 | 0.1092 |
| 8 | 0.5989 | 0.2156 | 0.1625 | 0.1366 | 0.1289 |
| 10 | 0.5915 | 0.1993 | 0.2409 | 0.1607 | 0.1231 |
| 12 | 0.5379 | 0.1002 | 0.1843 | 0.1053 | 0.0723 |

Recovery is the share of the variant-reference gap closed by the patch, a ratio of sums over pairs; 1 closes it, 0 leaves it, negative widens it. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_indicbert.csv` | 790,159 | `c8cdcafc92041681` | per pair: reference, variant, and the patched variant per condition |
