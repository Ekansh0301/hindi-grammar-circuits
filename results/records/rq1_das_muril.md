# rq1_das_muril

_Distributed alignment search: is what the moved head words carry (I1) a low-rank subspace, and what does it encode?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 18:47 |
| script | `rq1_das.py` (sha256 `e40adf12347edf08`) |
| host | gnode (Linux) |
| duration | 295.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "epochs": 3, "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "i1_csv": null, "layer": null, "lr": 0.001, "min_gap": 0.05, "model": "<earlier-repo>/local_models/muril-base-cased", "n_eval": 1000, "n_train": 2000, "n_val": 200, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/das", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "pairs_per_step": 8, "random_seeds": 3, "ranks": [1, 4, 16, 64], "record_tag": null, "tag": "muril", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv", "verb_ranks": [1, 16]}` |
| command | `scripts/rq1_das.py --tag muril --model <earlier-repo>/local_models/muril-base-cased --batch-size 32` |


- **layer / hidden size**: 8 / 768
- **pairs: evaluation (I1's) / validation / training**: 1,000 / 200 / 2,000
- **evaluation documents / training and validation documents**: 582 / 347 (disjoint)

### Checks against I1's per-pair output, before training (largest departure, bits)

- **S(base) vs I1 s_var**: 1.78e-15
- **S(clean) vs I1 s_ref**: 4.73e-06
- **full patch, moved heads, vs I1 moved_heads@8**: 1.78e-15
- **full patch, verb, vs I1 verb@8**: 1.78e-15
- **moved_heads: training / validation pairs with the site present**: 2,000 of 2,000 / 200 of 200
- **verb: training / validation pairs with the site present**: 1,994 of 2,000 / 200 of 200

### Training (validation pairs; epoch 0 is the random initialisation)


| site | rank | epoch | mean KL | validation recovery |
|---|---|---|---|---|
| moved_heads | 1 | 0 | nan | 0.0019 |
| moved_heads | 1 | 1 | 0.4467 | 0.2059 |
| moved_heads | 1 | 2 | 0.4229 | 0.2083 |
| moved_heads | 1 | 3 | 0.4230 | 0.2085 |
| moved_heads | 4 | 0 | nan | 0.0046 |
| moved_heads | 4 | 1 | 0.4064 | 0.3337 |
| moved_heads | 4 | 2 | 0.3707 | 0.3559 |
| moved_heads | 4 | 3 | 0.3674 | 0.3578 |
| moved_heads | 16 | 0 | nan | 0.0147 |
| moved_heads | 16 | 1 | 0.3525 | 0.5055 |
| moved_heads | 16 | 2 | 0.3060 | 0.5336 |
| moved_heads | 16 | 3 | 0.2984 | 0.5372 |
| moved_heads | 64 | 0 | nan | 0.0663 |
| moved_heads | 64 | 1 | 0.3089 | 0.6083 |
| moved_heads | 64 | 2 | 0.2506 | 0.6422 |
| moved_heads | 64 | 3 | 0.2368 | 0.6408 |
| verb | 1 | 0 | nan | 0.0001 |
| verb | 1 | 1 | 0.5045 | 0.0216 |
| verb | 1 | 2 | 0.4997 | 0.0230 |
| verb | 1 | 3 | 0.4994 | 0.0246 |
| verb | 16 | 0 | nan | 0.0034 |
| verb | 16 | 1 | 0.4771 | 0.1029 |
| verb | 16 | 2 | 0.4569 | 0.1153 |
| verb | 16 | 3 | 0.4531 | 0.1179 |

- **evaluation pairs with a gap above --min-gap**: 875 of 1,000

## Share of the gap recovered on I1's pairs


| site | rank | learned | random (mean) | full state (I1) | p, learned vs random | p, learned vs full |
|---|---|---|---|---|---|---|
| moved_heads | 1 | 0.2592 | 0.0006 | 0.6030 | 0.0001 | 0.0001 |
| moved_heads | 4 | 0.4005 | 0.0036 | 0.6030 | 0.0001 | 0.0001 |
| moved_heads | 16 | 0.5555 | 0.0135 | 0.6030 | 0.0001 | 0.0001 |
| moved_heads | 64 | 0.6485 | 0.0683 | 0.6030 | 0.0001 | 0.0001 |
| verb | 1 | 0.0367 | 0.0001 | 0.1057 | 0.0001 | 0.0001 |
| verb | 16 | 0.1472 | 0.0025 | 0.1057 | 0.0001 | 0.0001 |

A ratio of sums over evaluation pairs, I1's measure: 1 closes the variant's gap to the reference, 0 leaves it. p: document-level sign-flip permutation on the per-pair difference in the amount moved, two-sided, 10,000 permutations. The verb complex is the site control.

- **rank-1 direction's sign in dv (the npz holds the unflipped Q)**: +1

## What the rank-1 variable tracks (moved head words, unmasked runs)


| against | Spearman over pairs | Spearman over documents | p (documents) | documents |
|---|---|---|---|---|
| the model's preference d_T | 0.1951 | 0.1916 | 0.0001 | 582 |
| E1, d_syn_order | 0.1325 | 0.1041 | 0.0103 | 582 |
| trigram, d_kenlm_mean | 0.1335 | 0.1252 | 0.0024 | 582 |
| moved heads' position change, dpos | -0.8214 | -0.8286 | 0.0001 | 582 |

dv is the change in the learned direction's value at the moved head words, reference minus variant, signed so that it rises with the model's own preference. Over documents: per-document means, permutation p over documents, 10,000. Descriptive.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `das_muril.npz` | 314,904 | `4d9599ef2692742f` | the learned subspaces (k x d, orthonormal rows), per site and rank |
| `das_muril.csv` | 683,050 | `945f93f109232682` | per evaluation pair: clean and base runs, the base run under every condition, and (rank 1) dv, dpos and the E1 and trigram differences |
