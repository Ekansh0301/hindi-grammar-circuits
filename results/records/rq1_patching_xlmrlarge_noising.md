# rq1_patching_xlmrlarge_noising

_Interchange patching of variant states into the reference run (noising), by site and layer._

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 13:00 |
| script | `rq1_patching.py` (sha256 `488ed6414a4ea7c3`) |
| host | gnode (Linux) |
| duration | 246.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "direction": "noising", "layers": null, "min_gap": 0.05, "model": "xlm-roberta-large", "n_pairs": 1000, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/patching", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "xlmrlarge"}` |
| command | `scripts/rq1_patching.py --tag xlmrlarge --model xlm-roberta-large --batch-size 16 --direction noising` |


- **layers / conditions**: 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24 / 66
- **direction**: noising
- **pairs patched / skipped / with a gap above --min-gap**: 1,000 / 0 / 862
- **check: 'all' at layer 0 moves the whole gap (ratio of sums) / largest per-pair departure from the clean run (bits)**: 1.000000 / 1.15e-04

| layer | moved by moved_heads | moved by moved_psp | moved by moved_other | moved by verb | moved by unmoved |
|---|---|---|---|---|---|
| 0 | 6.9299 | 3.3440 | 5.2045 | 0.0000 | 0.9017 |
| 2 | 4.3786 | 2.0367 | 2.6543 | -0.0014 | 0.1577 |
| 4 | 3.6007 | 1.5446 | 2.1781 | -0.0044 | 0.1085 |
| 6 | 3.2109 | 1.3207 | 1.9793 | -0.0059 | 0.0904 |
| 8 | 2.5496 | 0.9544 | 1.5460 | -0.0061 | 0.0500 |
| 10 | 1.4732 | 0.5271 | 0.9060 | 0.0039 | 0.0195 |
| 12 | 0.8822 | 0.2924 | 0.5565 | 0.0110 | 0.0098 |
| 14 | 0.6238 | 0.1835 | 0.3525 | 0.0143 | 0.0032 |
| 16 | 0.4794 | 0.1187 | 0.2413 | 0.0160 | -0.0003 |
| 18 | 0.3854 | 0.0842 | 0.1683 | 0.0136 | 0.0103 |
| 20 | 0.3513 | 0.0710 | 0.1365 | 0.0384 | 0.0500 |
| 22 | 0.4222 | 0.0861 | 0.1770 | 0.1000 | 0.0930 |
| 24 | 0.4718 | 0.0909 | 0.2034 | 0.1220 | 0.1118 |

The share of the reference-variant gap moved by patching the variant's states into the reference run, toward the variant's surprisal, a ratio of sums over pairs; 1 moves the whole gap, 0 none, negative the other way. Site sizes per pair are in the CSV.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `patching_xlmrlarge_noising.csv` | 1,372,569 | `f0c6dd3798b34f7f` | per pair: reference, variant, base and clean runs, and the patched base run per condition |
