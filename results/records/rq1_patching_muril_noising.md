# rq1_patching_muril_noising

_Interchange patching of variant states into the reference run (noising), by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 07:45 |
| script | `rq1_patching.py` (sha256 `488ed6414a4ea7c3`) |
| host | gnode (Linux) |
| duration | 75.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "direction": "noising", "layers": null, "min_gap": 0.05, "model": "<earlier-repo>/local_models/muril-base-cased", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "muril"}` |
| command | `scripts/rq1_patching.py --tag muril --model <earlier-repo>/local_models/muril-base-cased --batch-size 32 --direction noising` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **direction**: noising
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 875
- **check: 'all' at layer 0 moves the whole gap (ratio of sums) / largest per-pair departure from the clean run (bits)**: 1.000000 / 4.37e-05

| layer | moved by moved_heads | moved by moved_psp | moved by moved_other | moved by verb | moved by unmoved |
|---|---|---|---|---|---|
| 0 | 5.0107 | 2.4605 | 3.5897 | 0.0000 | 0.4869 |
| 2 | 3.3678 | 1.3009 | 2.0363 | -0.0069 | 0.0983 |
| 4 | 1.7534 | 0.5732 | 1.0183 | -0.0089 | 0.0210 |
| 6 | 0.8853 | 0.2618 | 0.4278 | -0.0054 | 0.0055 |
| 8 | 0.4266 | 0.1009 | 0.1349 | 0.0057 | 0.0278 |
| 10 | 0.4330 | 0.0998 | 0.1612 | 0.0663 | 0.0753 |
| 12 | 0.4858 | 0.1121 | 0.1881 | 0.1109 | 0.1032 |

The share of the reference-variant gap moved by patching the variant's states into the reference run, toward the variant's surprisal, a ratio of sums over pairs; 1 moves the whole gap, 0 none, negative the other way. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_muril_noising.csv` | 824,571 | `d3d0b50328f89291` | per pair: reference, variant, base and clean runs, and the patched base run per condition |
