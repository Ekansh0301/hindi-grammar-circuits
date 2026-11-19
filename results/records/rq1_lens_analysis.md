# rq1_lens_analysis

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 11:16 |
| script | `rq1_lens_analysis.py` (sha256 `d4ab7ffa38a16972`) |
| host | gnode (Linux) |
| duration | 0.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"models": ["muril", "indicbert", "mbert", "xlmrlarge"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers.csv", "tag": "rq1_lens_analysis", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py` |



## model: muril

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_muril.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.820 | 12 |
| verb complex | 8868 | 0.697 | 12 |
| postposition | 8645 | 0.710 | 12 |
| moved head | 8923 | 0.769 | 12 |
| moved other | 8269 | 0.705 | 12 |
| unmoved unit | 3472 | 0.681 | 12 |
| outside | 8919 | 0.618 | 12 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.52* | 0.52* | 0.53* | 0.59* | 0.57* | 0.62* | 0.64* | 0.64* | 0.57* | 0.50* | 0.46* | 0.42* | 0.82 |
| verb complex | 0.04* | 0.51* | 0.57* | 0.58* | 0.52* | 0.59* | 0.61* | 0.53* | 0.51* | 0.47* | 0.47* | 0.45* | 0.70 |
| postposition | 0.50* | 0.52* | 0.54* | 0.58* | 0.57* | 0.57* | 0.53* | 0.58* | 0.52* | 0.44* | 0.43* | 0.39* | 0.71 |
| moved head | 0.50* | 0.49* | 0.48* | 0.52* | 0.54* | 0.58* | 0.59* | 0.58* | 0.54* | 0.51* | 0.46* | 0.46* | 0.77 |
| moved other | 0.50* | 0.51* | 0.50* | 0.52* | 0.54* | 0.56* | 0.55* | 0.56* | 0.55* | 0.53* | 0.50* | 0.45* | 0.71 |
| unmoved unit | 0.32* | 0.47* | 0.45* | 0.49* | 0.51* | 0.53* | 0.54* | 0.55* | 0.53* | 0.52* | 0.50* | 0.45* | 0.68 |
| outside | 0.12* | 0.51* | 0.58* | 0.46* | 0.43* | 0.53* | 0.63* | 0.60* | 0.55* | 0.53* | 0.56* | 0.52* | 0.62 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## model: indicbert

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_indicbert.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.787 | 10 |
| verb complex | 8868 | 0.702 | 12 |
| postposition | 8645 | 0.691 | 12 |
| moved head | 8923 | 0.739 | 10 |
| moved other | 8269 | 0.646 | 11 |
| unmoved unit | 3472 | 0.666 | 12 |
| outside | 8919 | 0.597 | 10 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.54* | 0.59* | 0.66* | 0.68* | 0.70* | 0.73* | 0.75* | 0.74* | 0.75* | 0.77* | 0.77 | 0.77 | 0.79 |
| verb complex | 0.04* | 0.60* | 0.60* | 0.59* | 0.59* | 0.58* | 0.61* | 0.59* | 0.62* | 0.64* | 0.67 | 0.67 | 0.70 |
| postposition | 0.49* | 0.51* | 0.55* | 0.57* | 0.56* | 0.60* | 0.62* | 0.60* | 0.62* | 0.61* | 0.62 | 0.61 | 0.69 |
| moved head | 0.52* | 0.58* | 0.64* | 0.66* | 0.67* | 0.68* | 0.68* | 0.71* | 0.72* | 0.72* | 0.73 | 0.73 | 0.74 |
| moved other | 0.52* | 0.53* | 0.56* | 0.56* | 0.57* | 0.58* | 0.58* | 0.59* | 0.60* | 0.61* | 0.62 | 0.64 | 0.65 |
| unmoved unit | 0.30* | 0.50* | 0.52* | 0.55* | 0.56* | 0.57* | 0.60* | 0.61* | 0.63* | 0.62* | 0.63 | 0.62 | 0.67 |
| outside | 0.21* | 0.52* | 0.52* | 0.49* | 0.53* | 0.54* | 0.56* | 0.58* | 0.62* | 0.65* | 0.63 | 0.61 | 0.60 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## model: mbert

- **pairs**: 8,922
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_mbert.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8922 | 0.743 | 12 |
| verb complex | 8867 | 0.608 | 12 |
| postposition | 8644 | 0.658 | 12 |
| moved head | 8922 | 0.670 | 12 |
| moved other | 8268 | 0.631 | 12 |
| unmoved unit | 3471 | 0.622 | 12 |
| outside | 8918 | 0.560 | 12 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.52* | 0.53* | 0.54* | 0.61* | 0.63* | 0.64* | 0.64* | 0.59* | 0.59* | 0.65* | 0.68* | 0.70* | 0.74 |
| verb complex | 0.09* | 0.47* | 0.46* | 0.45* | 0.48* | 0.50* | 0.47* | 0.59* | 0.64* | 0.68* | 0.67* | 0.67* | 0.61 |
| postposition | 0.52* | 0.55* | 0.56* | 0.59* | 0.61* | 0.62* | 0.63* | 0.60* | 0.61* | 0.64* | 0.65* | 0.68* | 0.66 |
| moved head | 0.49* | 0.49* | 0.49* | 0.52* | 0.52* | 0.53* | 0.57* | 0.57* | 0.56* | 0.59* | 0.63* | 0.64* | 0.67 |
| moved other | 0.50* | 0.51* | 0.53* | 0.55* | 0.55* | 0.57* | 0.60* | 0.54* | 0.52* | 0.53* | 0.56* | 0.59* | 0.63 |
| unmoved unit | 0.34* | 0.48* | 0.48* | 0.49* | 0.50* | 0.53* | 0.56* | 0.51* | 0.49* | 0.47* | 0.53* | 0.57* | 0.62 |
| outside | 0.20* | 0.50* | 0.49* | 0.47* | 0.47* | 0.43* | 0.40* | 0.43* | 0.45* | 0.54* | 0.54* | 0.60* | 0.56 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## model: xlmrlarge

- **pairs**: 8,923
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_xlmrlarge.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8923 | 0.809 | 23 |
| verb complex | 8868 | 0.697 | 24 |
| postposition | 8645 | 0.670 | 24 |
| moved head | 8923 | 0.754 | 24 |
| moved other | 8269 | 0.685 | 24 |
| unmoved unit | 3472 | 0.670 | 24 |
| outside | 8919 | 0.536 | 22 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.51* | 0.53* | 0.57* | 0.59* | 0.58* | 0.61* | 0.62* | 0.63* | 0.64* | 0.66* | 0.63* | 0.69* | 0.73* | 0.71* | 0.71* | 0.72* | 0.75* | 0.77* | 0.80* | 0.78* | 0.78* | 0.77 | 0.77 | 0.78 | 0.81 |
| verb complex | 0.07* | 0.51* | 0.48* | 0.44* | 0.47* | 0.47* | 0.53* | 0.52* | 0.53* | 0.56* | 0.56* | 0.59* | 0.64* | 0.59* | 0.60* | 0.60* | 0.65* | 0.67* | 0.66* | 0.67* | 0.70* | 0.67 | 0.67 | 0.67 | 0.70 |
| postposition | 0.51* | 0.52* | 0.53* | 0.50* | 0.50* | 0.51* | 0.53* | 0.53* | 0.55* | 0.57* | 0.59* | 0.64* | 0.64* | 0.65* | 0.64* | 0.66* | 0.69* | 0.69* | 0.71* | 0.66* | 0.65* | 0.62 | 0.64 | 0.64 | 0.67 |
| moved head | 0.50* | 0.52* | 0.55* | 0.58* | 0.58* | 0.59* | 0.59* | 0.61* | 0.62* | 0.63* | 0.60* | 0.63* | 0.64* | 0.63* | 0.64* | 0.65* | 0.67* | 0.69* | 0.72* | 0.71* | 0.71* | 0.71 | 0.71 | 0.71 | 0.75 |
| moved other | 0.49* | 0.50* | 0.52* | 0.54* | 0.54* | 0.56* | 0.56* | 0.57* | 0.58* | 0.58* | 0.57* | 0.58* | 0.60* | 0.62* | 0.60* | 0.60* | 0.61* | 0.63* | 0.65* | 0.63* | 0.63* | 0.63 | 0.63 | 0.64 | 0.69 |
| unmoved unit | 0.34* | 0.51* | 0.52* | 0.54* | 0.55* | 0.57* | 0.56* | 0.57* | 0.56* | 0.56* | 0.53* | 0.58* | 0.58* | 0.61* | 0.60* | 0.62* | 0.61* | 0.63* | 0.65* | 0.62* | 0.61* | 0.61 | 0.61 | 0.62 | 0.67 |
| outside | 0.19* | 0.51* | 0.48* | 0.40* | 0.41* | 0.40* | 0.43* | 0.44* | 0.42* | 0.43* | 0.46* | 0.43* | 0.46* | 0.46* | 0.47* | 0.44* | 0.52* | 0.53* | 0.56* | 0.52* | 0.49* | 0.51 | 0.55 | 0.59 | 0.54 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers.csv` | 21,103 | `9a7da3d701f7c6c7` | reference-preferred share per model, word class and layer |
