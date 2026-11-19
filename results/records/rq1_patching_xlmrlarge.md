# rq1_patching_xlmrlarge

_Interchange patching of reference states into the variant run, by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 13:11 |
| script | `rq1_patching.py` (sha256 `2ec9064efd5d7399`) |
| host | gnode (Linux) |
| duration | 247.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "layers": null, "min_gap": 0.05, "model": "xlm-roberta-large", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "xlmrlarge"}` |
| command | `scripts/rq1_patching.py --tag xlmrlarge --model xlm-roberta-large --batch-size 16` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24 / 66
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 862
- **check: 'all' at layer 0 recovers (ratio of sums) / largest per-pair departure (bits)**: 1.000000 / 5.10e-05

| layer | recovered by moved_heads | recovered by moved_psp | recovered by moved_other | recovered by verb | recovered by unmoved |
|---|---|---|---|---|---|
| 0 | -5.4307 | -3.3272 | -5.1232 | 0.0000 | -0.8720 |
| 2 | -3.0621 | -1.9047 | -2.4818 | 0.0159 | -0.1390 |
| 4 | -2.2422 | -1.4246 | -1.9796 | 0.0323 | -0.0799 |
| 6 | -1.8561 | -1.2085 | -1.7650 | 0.0500 | -0.0569 |
| 8 | -1.2282 | -0.8087 | -1.2806 | 0.0701 | 0.0069 |
| 10 | -0.2415 | -0.2710 | -0.5658 | 0.0857 | 0.0670 |
| 12 | 0.2348 | -0.0172 | -0.1856 | 0.1136 | 0.0954 |
| 14 | 0.4279 | 0.0972 | 0.0140 | 0.1170 | 0.1247 |
| 16 | 0.5169 | 0.1514 | 0.1281 | 0.1377 | 0.1455 |
| 18 | 0.5689 | 0.1846 | 0.2054 | 0.1518 | 0.1607 |
| 20 | 0.5794 | 0.1715 | 0.2504 | 0.1616 | 0.1587 |
| 22 | 0.5040 | 0.1203 | 0.2285 | 0.1407 | 0.1246 |
| 24 | 0.4718 | 0.0909 | 0.2034 | 0.1220 | 0.1118 |

Recovery is the share of the variant-reference gap closed by the patch, a ratio of sums over pairs; 1 closes it, 0 leaves it, negative widens it. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_xlmrlarge.csv` | 1,333,656 | `2f0ed0a756ef6965` | per pair: reference, variant, and the patched variant per condition |
