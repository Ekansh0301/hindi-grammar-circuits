# rq1_word_state_probes_indicbert_f5_geometry

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-18 02:10 |
| script | `rq1_word_state_probes.py` (sha256 `7bc016dce49db3e9`) |
| host | gnode (Linux) |
| duration | 15.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"drop_top_dims": 5, "epochs": 40, "geometry": true, "layers": [10, 11, 12], "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "only_f5": true, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_word_state_probes_indicbert_f5_geometry", "standardise": "norm", "tag": "indicbert"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --standardise norm --epochs 40 --only-f5 --geometry --drop-top-dims 5 --layers 10 11 12 --record-tag rq1_word_state_probes_indicbert_f5_geometry` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## Geometry of each layer's word states (training references)


| layer | variance share, top dimension | top 5 dimensions | top dimension index | |mean vector| / mean state norm |
|---|---|---|---|---|
| 0 | 0.004 | 0.015 | 489 | 0.261 |
| 1 | 0.009 | 0.024 | 543 | 0.452 |
| 2 | 0.023 | 0.067 | 543 | 0.649 |
| 3 | 0.024 | 0.065 | 543 | 0.583 |
| 4 | 0.019 | 0.063 | 543 | 0.537 |
| 5 | 0.018 | 0.066 | 236 | 0.564 |
| 6 | 0.019 | 0.069 | 543 | 0.572 |
| 7 | 0.012 | 0.045 | 543 | 0.500 |
| 8 | 0.011 | 0.045 | 543 | 0.515 |
| 9 | 0.007 | 0.033 | 229 | 0.436 |
| 10 | 0.014 | 0.045 | 330 | 0.429 |
| 11 | 0.080 | 0.131 | 236 | 0.430 |
| 12 | 0.257 | 0.283 | 236 | 0.468 |

A layer whose variance sits in one or a few dimensions presents a distance probe with almost nothing else to read: any rescaling that keeps those dimensions keeps them dominant. That is a fact about the layer's geometry, and it is why this is reported next to the probe rather than folded into it.


## F5: structural distance probe (held-out references)

- **input scaling / epochs**: norm / 40
- **layer 6: dimensions with std < 1e-3 / smallest / largest std**: 0 / 9.78e-02 / 1.09e+00

> DIAGNOSTIC: the 5 highest-variance dimensions of each layer (estimated on training references) are removed before the probe. Not the declared probe; read beside rq1_word_state_probes_<model>_f5_norm.md, never instead of it.


| layer | mean Spearman (5-50 words) | UUAS | training loss, first epoch | last epoch |
|---|---|---|---|---|
| baseline: surface distance |i - j| | 0.404 | 0.549 | nan | nan |
| control (pre-LayerNorm input) | 0.594 | 0.512 | 1.191 | 0.812 |
| 10 | 0.728 | 0.650 | 1.216 | 0.607 |
| 11 | 0.395 | 0.412 | 1.465 | 1.009 |
| 12 | 0.645 | 0.558 | 1.489 | 0.745 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_rq1_word_state_probes_indicbert_f5_geometry.csv` | 205 | `e842397c186c2a74` | distance: a = Spearman, b = UUAS |
