# rq1_lens_analysis_xlmrlarge_tuned

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 19:26 |
| script | `rq1_lens_analysis.py` (sha256 `d4ab7ffa38a16972`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"models": ["xlmrlarge_tuned"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_xlmrlarge_tuned.csv", "tag": "rq1_lens_analysis_xlmrlarge_tuned", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models xlmrlarge_tuned --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_xlmrlarge_tuned.csv --tag rq1_lens_analysis_xlmrlarge_tuned` |



## model: xlmrlarge_tuned

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_xlmrlarge_tuned.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.809 | 10 |
| verb complex | 8868 | 0.697 | 20 |
| postposition | 8645 | 0.670 | 12 |
| moved head | 8923 | 0.754 | 15 |
| moved other | 8269 | 0.685 | 15 |
| unmoved unit | 3472 | 0.670 | 14 |
| outside | 8919 | 0.536 | 10 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.63* | 0.63* | 0.68* | 0.71* | 0.72* | 0.73* | 0.73* | 0.75* | 0.76* | 0.77 | 0.78 | 0.79 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.81 | 0.81 | 0.80 | 0.80 | 0.81 |
| verb complex | 0.08* | 0.51* | 0.57* | 0.58* | 0.59* | 0.61* | 0.61* | 0.62* | 0.61* | 0.64 | 0.64 | 0.65 | 0.67 | 0.67 | 0.65 | 0.65 | 0.65 | 0.65 | 0.65 | 0.65 | 0.69 | 0.69 | 0.69 | 0.69 | 0.70 |
| postposition | 0.58* | 0.59* | 0.57* | 0.59* | 0.59* | 0.59* | 0.60* | 0.62* | 0.62* | 0.64 | 0.63 | 0.64 | 0.66 | 0.66 | 0.65 | 0.66 | 0.65 | 0.65 | 0.65 | 0.66 | 0.66 | 0.67 | 0.66 | 0.67 | 0.67 |
| moved head | 0.58* | 0.58* | 0.64* | 0.65* | 0.66* | 0.67* | 0.67* | 0.68* | 0.69* | 0.70 | 0.71 | 0.71 | 0.72 | 0.72 | 0.72 | 0.73 | 0.73 | 0.73 | 0.73 | 0.74 | 0.75 | 0.75 | 0.74 | 0.75 | 0.75 |
| moved other | 0.57* | 0.57* | 0.60* | 0.61* | 0.61* | 0.62* | 0.62* | 0.63* | 0.64* | 0.65 | 0.65 | 0.66 | 0.66 | 0.66 | 0.66 | 0.67 | 0.67 | 0.67 | 0.67 | 0.68 | 0.68 | 0.68 | 0.68 | 0.68 | 0.69 |
| unmoved unit | 0.33* | 0.50* | 0.57* | 0.58* | 0.59* | 0.59* | 0.58* | 0.60* | 0.60* | 0.62 | 0.62 | 0.64 | 0.64 | 0.65 | 0.65 | 0.65 | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 | 0.67 | 0.67 | 0.66 | 0.67 |
| outside | 0.09* | 0.52* | 0.55* | 0.58* | 0.57* | 0.55* | 0.53* | 0.54* | 0.53* | 0.51 | 0.54 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.51 | 0.52 | 0.52 | 0.51 | 0.51 | 0.51 | 0.52 | 0.54 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_xlmrlarge_tuned.csv` | 9,527 | `25c97298a97b839e` | reference-preferred share per model, word class and layer |
