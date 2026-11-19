# rq1_patching_mbert_noising

_Interchange patching of variant states into the reference run (noising), by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 10:03 |
| script | `rq1_patching.py` (sha256 `488ed6414a4ea7c3`) |
| host | gnode (Linux) |
| duration | 138.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "direction": "noising", "layers": null, "min_gap": 0.05, "model": "bert-base-multilingual-cased", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "mbert"}` |
| command | `scripts/rq1_patching.py --tag mbert --model bert-base-multilingual-cased --batch-size 24 --direction noising` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **direction**: noising
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 913
- **check: 'all' at layer 0 moves the whole gap (ratio of sums) / largest per-pair departure from the clean run (bits)**: 1.000000 / 2.08e-05

| layer | moved by moved_heads | moved by moved_psp | moved by moved_other | moved by verb | moved by unmoved |
|---|---|---|---|---|---|
| 0 | 9.4694 | 4.6174 | 8.2083 | 0.0000 | 1.7763 |
| 2 | 3.8055 | 2.2832 | 2.7491 | -0.0070 | 0.3828 |
| 4 | 1.9231 | 1.0067 | 1.3100 | -0.0192 | 0.0923 |
| 6 | 0.8832 | 0.4519 | 0.5901 | -0.0116 | 0.0137 |
| 8 | 0.3473 | 0.1584 | 0.1778 | 0.0373 | 0.0070 |
| 10 | 0.2764 | 0.1467 | 0.1551 | 0.0527 | 0.0389 |
| 12 | 0.3921 | 0.1852 | 0.2292 | 0.0993 | 0.0942 |

The share of the reference-variant gap moved by patching the variant's states into the reference run, toward the variant's surprisal, a ratio of sums over pairs; 1 moves the whole gap, 0 none, negative the other way. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_mbert_noising.csv` | 814,248 | `9d3eb0a7350d983f` | per pair: reference, variant, base and clean runs, and the patched base run per condition |
