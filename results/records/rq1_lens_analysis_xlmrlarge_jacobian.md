# rq1_lens_analysis_xlmrlarge_jacobian

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 16:33 |
| script | `rq1_lens_analysis.py` (sha256 `9943dd76e4966e49`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"models": ["xlmrlarge_jacobian"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_xlmrlarge_jacobian.csv", "tag": "rq1_lens_analysis_xlmrlarge_jacobian", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models xlmrlarge_jacobian --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_xlmrlarge_jacobian.csv --tag rq1_lens_analysis_xlmrlarge_jacobian` |



## model: xlmrlarge_jacobian

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_xlmrlarge_jacobian.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.809 | 21 |
| verb complex | 8868 | 0.697 | 21 |
| postposition | 8645 | 0.670 | 21 |
| moved head | 8923 | 0.754 | 21 |
| moved other | 8269 | 0.685 | 21 |
| unmoved unit | 3472 | 0.670 | 21 |
| outside | 8919 | 0.536 | 24 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.49* | 0.52* | 0.60* | 0.62* | 0.63* | 0.64* | 0.65* | 0.66* | 0.68* | 0.70* | 0.71* | 0.74* | 0.75* | 0.75* | 0.76* | 0.80* | 0.82* | 0.84* | 0.86* | 0.87* | 0.85* | 0.83 | 0.81 | 0.80 | 0.81 |
| verb complex | 0.07* | 0.48* | 0.48* | 0.48* | 0.50* | 0.50* | 0.51* | 0.52* | 0.52* | 0.55* | 0.56* | 0.57* | 0.58* | 0.59* | 0.59* | 0.61* | 0.63* | 0.65* | 0.67* | 0.69* | 0.71* | 0.72 | 0.70 | 0.69 | 0.70 |
| postposition | 0.47* | 0.50* | 0.52* | 0.52* | 0.54* | 0.55* | 0.56* | 0.56* | 0.57* | 0.59* | 0.59* | 0.63* | 0.64* | 0.63* | 0.65* | 0.69* | 0.70* | 0.71* | 0.73* | 0.74* | 0.72* | 0.67 | 0.66 | 0.66 | 0.67 |
| moved head | 0.50* | 0.51* | 0.58* | 0.60* | 0.61* | 0.61* | 0.61* | 0.62* | 0.63* | 0.65* | 0.65* | 0.65* | 0.67* | 0.67* | 0.68* | 0.72* | 0.73* | 0.76* | 0.78* | 0.80* | 0.80* | 0.77 | 0.75 | 0.75 | 0.75 |
| moved other | 0.49* | 0.53* | 0.54* | 0.55* | 0.55* | 0.57* | 0.57* | 0.57* | 0.59* | 0.59* | 0.61* | 0.61* | 0.63* | 0.62* | 0.63* | 0.66* | 0.68* | 0.70* | 0.72* | 0.74* | 0.73* | 0.69 | 0.67 | 0.68 | 0.69 |
| unmoved unit | 0.34* | 0.50* | 0.58* | 0.59* | 0.59* | 0.60* | 0.60* | 0.60* | 0.60* | 0.60* | 0.61* | 0.62* | 0.63* | 0.63* | 0.64* | 0.67* | 0.68* | 0.70* | 0.71* | 0.72* | 0.71* | 0.69 | 0.67 | 0.66 | 0.67 |
| outside | 0.09* | 0.51* | 0.56* | 0.59* | 0.60* | 0.59* | 0.57* | 0.59* | 0.61* | 0.62* | 0.62* | 0.65* | 0.63* | 0.59* | 0.61* | 0.61* | 0.63* | 0.64* | 0.61* | 0.58* | 0.52* | 0.53 | 0.50 | 0.50 | 0.54 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_xlmrlarge_jacobian.csv` | 10,144 | `cb8f265d626deac7` | reference-preferred share per model, word class and layer |
