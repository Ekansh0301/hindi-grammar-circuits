# rq1_patching_mbert

_Interchange patching of reference states into the variant run, by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 19:19 |
| script | `rq1_patching.py` (sha256 `2ec9064efd5d7399`) |
| host | gnode (Linux) |
| duration | 137.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "layers": null, "min_gap": 0.05, "model": "bert-base-multilingual-cased", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "mbert"}` |
| command | `scripts/rq1_patching.py --tag mbert --model bert-base-multilingual-cased --batch-size 24` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 913
- **check: 'all' at layer 0 recovers (ratio of sums) / largest per-pair departure (bits)**: 1.000000 / 1.49e-05

| layer | recovered by moved_heads | recovered by moved_psp | recovered by moved_other | recovered by verb | recovered by unmoved |
|---|---|---|---|---|---|
| 0 | -8.3583 | -4.2715 | -7.9153 | 0.0000 | -1.6127 |
| 2 | -2.8525 | -1.8717 | -2.3892 | 0.0116 | -0.2454 |
| 4 | -0.9316 | -0.6279 | -0.9702 | 0.0480 | 0.0343 |
| 6 | 0.0447 | -0.0572 | -0.1995 | 0.0844 | 0.1144 |
| 8 | 0.4801 | 0.2083 | 0.2253 | 0.1384 | 0.1720 |
| 10 | 0.4964 | 0.2270 | 0.2906 | 0.1463 | 0.1472 |
| 12 | 0.3921 | 0.1852 | 0.2292 | 0.0993 | 0.0942 |

Recovery is the share of the variant-reference gap closed by the patch, a ratio of sums over pairs; 1 closes it, 0 leaves it, negative widens it. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_mbert.csv` | 778,577 | `b920270dd9b0d9f5` | per pair: reference, variant, and the patched variant per condition |
