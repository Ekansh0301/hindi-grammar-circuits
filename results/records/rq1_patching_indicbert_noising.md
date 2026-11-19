# rq1_patching_indicbert_noising

_Interchange patching of variant states into the reference run (noising), by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 08:53 |
| script | `rq1_patching.py` (sha256 `488ed6414a4ea7c3`) |
| host | gnode (Linux) |
| duration | 77.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "direction": "noising", "layers": null, "min_gap": 0.05, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "indicbert"}` |
| command | `scripts/rq1_patching.py --tag indicbert --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --batch-size 32 --direction noising` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12 / 36
- **direction**: noising
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 878
- **check: 'all' at layer 0 moves the whole gap (ratio of sums) / largest per-pair departure from the clean run (bits)**: 1.000000 / 8.13e-06

| layer | moved by moved_heads | moved by moved_psp | moved by moved_other | moved by verb | moved by unmoved |
|---|---|---|---|---|---|
| 0 | 5.6176 | 2.8248 | 3.8338 | 0.0000 | 0.4238 |
| 2 | 2.5769 | 0.9125 | 1.5551 | -0.0048 | 0.0393 |
| 4 | 1.3258 | 0.3821 | 0.8399 | -0.0039 | -0.0058 |
| 6 | 0.7432 | 0.1797 | 0.4264 | -0.0054 | -0.0013 |
| 8 | 0.4459 | 0.0805 | 0.1954 | 0.0011 | 0.0080 |
| 10 | 0.3859 | 0.0696 | 0.1242 | 0.0327 | 0.0335 |
| 12 | 0.5379 | 0.1002 | 0.1843 | 0.1053 | 0.0723 |

The share of the reference-variant gap moved by patching the variant's states into the reference run, toward the variant's surprisal, a ratio of sums over pairs; 1 moves the whole gap, 0 none, negative the other way. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_indicbert_noising.csv` | 828,594 | `7c34fc50d5343b66` | per pair: reference, variant, base and clean runs, and the patched base run per condition |
