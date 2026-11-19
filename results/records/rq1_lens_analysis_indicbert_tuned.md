# rq1_lens_analysis_indicbert_tuned

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 15:14 |
| script | `rq1_lens_analysis.py` (sha256 `d4ab7ffa38a16972`) |
| host | gnode (Linux) |
| duration | 0.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"models": ["indicbert_tuned"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_indicbert_tuned.csv", "tag": "rq1_lens_analysis_indicbert_tuned", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models indicbert_tuned --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_indicbert_tuned.csv --tag rq1_lens_analysis_indicbert_tuned` |



## model: indicbert_tuned

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_indicbert_tuned.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.787 | 5 |
| verb complex | 8868 | 0.702 | 5 |
| postposition | 8645 | 0.691 | 5 |
| moved head | 8923 | 0.739 | 6 |
| moved other | 8269 | 0.646 | 6 |
| unmoved unit | 3472 | 0.666 | 6 |
| outside | 8919 | 0.597 | 9 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.64* | 0.70* | 0.74* | 0.76* | 0.77* | 0.79 | 0.79 | 0.80 | 0.80 | 0.81 | 0.79 | 0.79 | 0.79 |
| verb complex | 0.08* | 0.57* | 0.65* | 0.67* | 0.68* | 0.69 | 0.68 | 0.69 | 0.68 | 0.69 | 0.70 | 0.70 | 0.70 |
| postposition | 0.57* | 0.60* | 0.61* | 0.62* | 0.65* | 0.68 | 0.68 | 0.68 | 0.67 | 0.67 | 0.67 | 0.68 | 0.69 |
| moved head | 0.59* | 0.65* | 0.68* | 0.70* | 0.71* | 0.71 | 0.72 | 0.73 | 0.75 | 0.75 | 0.75 | 0.75 | 0.74 |
| moved other | 0.59* | 0.58* | 0.60* | 0.62* | 0.62* | 0.63 | 0.65 | 0.65 | 0.65 | 0.65 | 0.64 | 0.64 | 0.65 |
| unmoved unit | 0.31* | 0.54* | 0.60* | 0.61* | 0.64* | 0.63 | 0.65 | 0.66 | 0.66 | 0.66 | 0.66 | 0.65 | 0.67 |
| outside | 0.20* | 0.49* | 0.55* | 0.54* | 0.56* | 0.54 | 0.57 | 0.57 | 0.57 | 0.60 | 0.59 | 0.57 | 0.60 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_indicbert_tuned.csv` | 4,943 | `3b7187dd45271a1a` | reference-preferred share per model, word class and layer |
