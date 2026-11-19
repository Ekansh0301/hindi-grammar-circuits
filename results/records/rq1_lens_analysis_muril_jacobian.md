# rq1_lens_analysis_muril_jacobian

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 12:12 |
| script | `rq1_lens_analysis.py` (sha256 `9943dd76e4966e49`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"models": ["muril_jacobian"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_muril_jacobian.csv", "tag": "rq1_lens_analysis_muril_jacobian", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models muril_jacobian --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_muril_jacobian.csv --tag rq1_lens_analysis_muril_jacobian` |



## model: muril_jacobian

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_muril_jacobian.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.820 | 10 |
| verb complex | 8868 | 0.697 | 10 |
| postposition | 8645 | 0.710 | 10 |
| moved head | 8923 | 0.769 | 10 |
| moved other | 8269 | 0.705 | 10 |
| unmoved unit | 3472 | 0.681 | 10 |
| outside | 8919 | 0.618 | 10 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.56* | 0.57* | 0.68* | 0.72* | 0.76* | 0.77* | 0.82* | 0.86* | 0.87* | 0.86* | 0.84 | 0.82 | 0.82 |
| verb complex | 0.07* | 0.54* | 0.55* | 0.58* | 0.62* | 0.62* | 0.66* | 0.70* | 0.70* | 0.71* | 0.71 | 0.69 | 0.70 |
| postposition | 0.57* | 0.57* | 0.58* | 0.62* | 0.63* | 0.64* | 0.67* | 0.72* | 0.74* | 0.71* | 0.71 | 0.69 | 0.71 |
| moved head | 0.52* | 0.53* | 0.62* | 0.65* | 0.68* | 0.69* | 0.73* | 0.78* | 0.80* | 0.80* | 0.80 | 0.77 | 0.77 |
| moved other | 0.54* | 0.53* | 0.58* | 0.59* | 0.61* | 0.63* | 0.67* | 0.70* | 0.72* | 0.72* | 0.71 | 0.69 | 0.71 |
| unmoved unit | 0.32* | 0.49* | 0.56* | 0.58* | 0.60* | 0.60* | 0.64* | 0.69* | 0.70* | 0.70* | 0.70 | 0.67 | 0.68 |
| outside | 0.10* | 0.49* | 0.59* | 0.49* | 0.64* | 0.59* | 0.63* | 0.65* | 0.64* | 0.63* | 0.61 | 0.60 | 0.62 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_muril_jacobian.csv` | 4,886 | `17612c3099b65da0` | reference-preferred share per model, word class and layer |
