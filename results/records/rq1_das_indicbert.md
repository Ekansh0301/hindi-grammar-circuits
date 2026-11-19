# rq1_das_indicbert

_Distributed alignment search: is what the moved head words carry (I1) a low-rank subspace, and what does it encode?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 19:00 |
| script | `rq1_das.py` (sha256 `e40adf12347edf08`) |
| host | gnode (Linux) |
| duration | 308.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "epochs": 3, "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "i1_csv": null, "layer": null, "lr": 0.001, "min_gap": 0.05, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_eval": 1000, "n_train": 2000, "n_val": 200, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/das", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "pairs_per_step": 8, "random_seeds": 3, "ranks": [1, 4, 16, 64], "record_tag": null, "tag": "indicbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv", "verb_ranks": [1, 16]}` |
| command | `scripts/rq1_das.py --tag indicbert --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --batch-size 32` |


- **layer / hidden size**: 8 / 768
- **pairs: evaluation (I1's) / validation / training**: 1,000 / 200 / 2,000
- **evaluation documents / training and validation documents**: 582 / 347 (disjoint)

### Checks against I1's per-pair output, before training (largest departure, bits)

- **S(base) vs I1 s_var**: 1.78e-15
- **S(clean) vs I1 s_ref**: 2.83e-06
- **full patch, moved heads, vs I1 moved_heads@8**: 1.78e-15
- **full patch, verb, vs I1 verb@8**: 1.78e-15
- **moved_heads: training / validation pairs with the site present**: 2,000 of 2,000 / 200 of 200
- **verb: training / validation pairs with the site present**: 1,994 of 2,000 / 200 of 200

### Training (validation pairs; epoch 0 is the random initialisation)


| site | rank | epoch | mean KL | validation recovery |
|---|---|---|---|---|
| moved_heads | 1 | 0 | nan | 0.0011 |
| moved_heads | 1 | 1 | 0.5746 | 0.2394 |
| moved_heads | 1 | 2 | 0.5402 | 0.2547 |
| moved_heads | 1 | 3 | 0.5428 | 0.2420 |
| moved_heads | 4 | 0 | nan | 0.0032 |
| moved_heads | 4 | 1 | 0.5319 | 0.3817 |
| moved_heads | 4 | 2 | 0.4940 | 0.4222 |
| moved_heads | 4 | 3 | 0.4875 | 0.4404 |
| moved_heads | 16 | 0 | nan | 0.0122 |
| moved_heads | 16 | 1 | 0.4883 | 0.5385 |
| moved_heads | 16 | 2 | 0.4398 | 0.5946 |
| moved_heads | 16 | 3 | 0.4300 | 0.6226 |
| moved_heads | 64 | 0 | nan | 0.0694 |
| moved_heads | 64 | 1 | 0.4473 | 0.6541 |
| moved_heads | 64 | 2 | 0.3967 | 0.6956 |
| moved_heads | 64 | 3 | 0.3837 | 0.7065 |
| verb | 1 | 0 | nan | -0.0002 |
| verb | 1 | 1 | 0.7228 | 0.0679 |
| verb | 1 | 2 | 0.7184 | 0.0681 |
| verb | 1 | 3 | 0.7185 | 0.0696 |
| verb | 16 | 0 | nan | 0.0028 |
| verb | 16 | 1 | 0.6964 | 0.1634 |
| verb | 16 | 2 | 0.6780 | 0.1780 |
| verb | 16 | 3 | 0.6745 | 0.1819 |

- **evaluation pairs with a gap above --min-gap**: 878 of 1,000

## Share of the gap recovered on I1's pairs


| site | rank | learned | random (mean) | full state (I1) | p, learned vs random | p, learned vs full |
|---|---|---|---|---|---|---|
| moved_heads | 1 | 0.3458 | 0.0021 | 0.5989 | 0.0001 | 0.0001 |
| moved_heads | 4 | 0.4879 | 0.0061 | 0.5989 | 0.0001 | 0.0001 |
| moved_heads | 16 | 0.6274 | 0.0185 | 0.5989 | 0.0001 | 0.0700 |
| moved_heads | 64 | 0.7064 | 0.0741 | 0.5989 | 0.0001 | 0.0001 |
| verb | 1 | 0.0754 | 0.0003 | 0.1366 | 0.0001 | 0.0001 |
| verb | 16 | 0.2016 | 0.0036 | 0.1366 | 0.0001 | 0.0001 |

A ratio of sums over evaluation pairs, I1's measure: 1 closes the variant's gap to the reference, 0 leaves it. p: document-level sign-flip permutation on the per-pair difference in the amount moved, two-sided, 10,000 permutations. The verb complex is the site control.

- **rank-1 direction's sign in dv (the npz holds the unflipped Q)**: -1

## What the rank-1 variable tracks (moved head words, unmasked runs)


| against | Spearman over pairs | Spearman over documents | p (documents) | documents |
|---|---|---|---|---|
| the model's preference d_T | 0.0800 | 0.0875 | 0.0367 | 582 |
| E1, d_syn_order | 0.0343 | 0.0048 | 0.9089 | 582 |
| trigram, d_kenlm_mean | -0.0051 | -0.0270 | 0.5185 | 582 |
| moved heads' position change, dpos | -0.7116 | -0.6718 | 0.0001 | 582 |

dv is the change in the learned direction's value at the moved head words, reference minus variant, signed so that it rises with the model's own preference. Over documents: per-document means, permutation p over documents, 10,000. Descriptive.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `das_indicbert.npz` | 314,904 | `c991d0a474e714f7` | the learned subspaces (k x d, orthonormal rows), per site and rank |
| `das_indicbert.csv` | 685,697 | `2c9fc0f702f8647f` | per evaluation pair: clean and base runs, the base run under every condition, and (rank 1) dv, dpos and the E1 and trigram differences |
