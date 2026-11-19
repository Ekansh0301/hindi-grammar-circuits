# rq1_lens_analysis_mbert_tuned

_At which layer does each model's preference for the reference appear, overall and by word class?_

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 16:10 |
| script | `rq1_lens_analysis.py` (sha256 `d4ab7ffa38a16972`) |
| host | gnode (Linux) |
| duration | 0.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"models": ["mbert_tuned"], "out": "<earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_mbert_tuned.csv", "tag": "rq1_lens_analysis_mbert_tuned", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_lens_analysis.py --models mbert_tuned --out <earlier-repo>/sets/set1/Results_Checks/rq1_lens_layers_mbert_tuned.csv --tag rq1_lens_analysis_mbert_tuned` |



## model: mbert_tuned

- **pairs**: 8,922
- **readability file**: <earlier-repo>/sets/set1/Results_Checks/lm_units/readability_mbert_tuned.csv

| words | pairs | final-layer share | first readable layer at 90% |
|---|---|---|---|
| all words | 8922 | 0.743 | 6 |
| verb complex | 8867 | 0.608 | 9 |
| postposition | 8644 | 0.658 | 6 |
| moved head | 8922 | 0.670 | 7 |
| moved other | 8268 | 0.631 | 6 |
| unmoved unit | 3471 | 0.622 | 8 |
| outside | 8918 | 0.560 | 3 |


| words | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all words | 0.61* | 0.61 | 0.62 | 0.66 | 0.69 | 0.72 | 0.74 | 0.75 | 0.76 | 0.77 | 0.77 | 0.76 | 0.74 |
| verb complex | 0.11* | 0.48 | 0.52 | 0.54 | 0.55 | 0.58 | 0.58 | 0.60 | 0.60 | 0.61 | 0.61 | 0.61 | 0.61 |
| postposition | 0.56* | 0.57 | 0.56 | 0.59 | 0.61 | 0.63 | 0.65 | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 | 0.66 |
| moved head | 0.54* | 0.57 | 0.57 | 0.61 | 0.62 | 0.63 | 0.65 | 0.66 | 0.67 | 0.67 | 0.69 | 0.68 | 0.67 |
| moved other | 0.54* | 0.56 | 0.56 | 0.58 | 0.59 | 0.61 | 0.63 | 0.64 | 0.65 | 0.65 | 0.64 | 0.64 | 0.63 |
| unmoved unit | 0.33* | 0.54 | 0.55 | 0.56 | 0.57 | 0.58 | 0.59 | 0.61 | 0.63 | 0.63 | 0.64 | 0.64 | 0.62 |
| outside | 0.23* | 0.50 | 0.50 | 0.56 | 0.57 | 0.57 | 0.54 | 0.55 | 0.58 | 0.58 | 0.58 | 0.57 | 0.56 |

Share of pairs in which the reference is preferred at each layer; * marks unreadable layers.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_lens_layers_mbert_tuned.csv` | 4,552 | `3c77f51ebfb13f28` | reference-preferred share per model, word class and layer |
