# rq1_lens_analysis_mbert_jacobian

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 13:19 |
| script | `rq1_lens_analysis.py` (sha256 `9943dd76e4966e49`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"models": ["mbert_jacobian"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_mbert_jacobian.csv", "tag": "rq1_lens_analysis_mbert_jacobian", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models mbert_jacobian --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_mbert_jacobian.csv --tag rq1_lens_analysis_mbert_jacobian` |



## model: mbert_jacobian

- **pairs**: 8,922
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_mbert_jacobian.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8922 | 0.743 | 8 |
| verb complex | 8867 | 0.608 | 9 |
| postposition | 8644 | 0.658 | 8 |
| moved head | 8922 | 0.670 | 9 |
| moved other | 8268 | 0.631 | 8 |
| unmoved unit | 3471 | 0.622 | 9 |
| outside | 8918 | 0.560 | 9 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.51* | 0.53* | 0.54* | 0.59* | 0.62* | 0.64* | 0.69* | 0.71* | 0.74 | 0.77 | 0.79 | 0.78 | 0.74 |
| verb complex | 0.09* | 0.46* | 0.47* | 0.52* | 0.51* | 0.52* | 0.54* | 0.56* | 0.58 | 0.61 | 0.62 | 0.62 | 0.61 |
| postposition | 0.50* | 0.52* | 0.51* | 0.54* | 0.56* | 0.59* | 0.60* | 0.62* | 0.65 | 0.67 | 0.67 | 0.66 | 0.66 |
| moved head | 0.50* | 0.52* | 0.53* | 0.55* | 0.57* | 0.58* | 0.61* | 0.62* | 0.64 | 0.68 | 0.70 | 0.69 | 0.67 |
| moved other | 0.50* | 0.50* | 0.52* | 0.54* | 0.57* | 0.58* | 0.61* | 0.61* | 0.63 | 0.64 | 0.66 | 0.66 | 0.63 |
| unmoved unit | 0.33* | 0.53* | 0.54* | 0.56* | 0.57* | 0.58* | 0.59* | 0.58* | 0.59 | 0.62 | 0.65 | 0.66 | 0.62 |
| outside | 0.10* | 0.51* | 0.52* | 0.59* | 0.49* | 0.48* | 0.53* | 0.51* | 0.55 | 0.59 | 0.61 | 0.61 | 0.56 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_mbert_jacobian.csv` | 4,880 | `0c62d700cf5e878c` | reference-preferred share per model, word class and layer |
