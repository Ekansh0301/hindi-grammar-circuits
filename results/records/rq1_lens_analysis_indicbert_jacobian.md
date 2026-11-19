# rq1_lens_analysis_indicbert_jacobian

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 12:21 |
| script | `rq1_lens_analysis.py` (sha256 `9943dd76e4966e49`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"models": ["indicbert_jacobian"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_indicbert_jacobian.csv", "tag": "rq1_lens_analysis_indicbert_jacobian", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models indicbert_jacobian --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_indicbert_jacobian.csv --tag rq1_lens_analysis_indicbert_jacobian` |



## model: indicbert_jacobian

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_indicbert_jacobian.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.787 | 10 |
| verb complex | 8868 | 0.702 | 10 |
| postposition | 8645 | 0.691 | 12 |
| moved head | 8923 | 0.739 | 10 |
| moved other | 8269 | 0.646 | 10 |
| unmoved unit | 3472 | 0.666 | 10 |
| outside | 8919 | 0.597 | 10 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.53* | 0.63* | 0.67* | 0.73* | 0.74* | 0.76* | 0.80* | 0.82* | 0.85* | 0.85* | 0.81 | 0.79 | 0.79 |
| verb complex | 0.06* | 0.55* | 0.60* | 0.61* | 0.63* | 0.65* | 0.67* | 0.69* | 0.69* | 0.72* | 0.72 | 0.70 | 0.70 |
| postposition | 0.51* | 0.57* | 0.60* | 0.58* | 0.61* | 0.62* | 0.66* | 0.69* | 0.72* | 0.72* | 0.67 | 0.66 | 0.69 |
| moved head | 0.51* | 0.62* | 0.65* | 0.70* | 0.71* | 0.72* | 0.75* | 0.78* | 0.81* | 0.81* | 0.77 | 0.75 | 0.74 |
| moved other | 0.52* | 0.55* | 0.57* | 0.61* | 0.63* | 0.65* | 0.67* | 0.69* | 0.69* | 0.69* | 0.65 | 0.65 | 0.65 |
| unmoved unit | 0.30* | 0.56* | 0.56* | 0.60* | 0.62* | 0.63* | 0.65* | 0.67* | 0.71* | 0.71* | 0.69 | 0.65 | 0.67 |
| outside | 0.09* | 0.54* | 0.63* | 0.60* | 0.59* | 0.57* | 0.59* | 0.54* | 0.54* | 0.60* | 0.59 | 0.60 | 0.60 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_indicbert_jacobian.csv` | 5,254 | `921b8b36c8e772ea` | reference-preferred share per model, word class and layer |
