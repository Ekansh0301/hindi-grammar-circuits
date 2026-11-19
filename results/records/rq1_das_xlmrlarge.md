# rq1_das_xlmrlarge

_Distributed alignment search: is what the moved head words carry (I1) a low-rank subspace, and what does it encode?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 23:32 |
| script | `rq1_das.py` (sha256 `e40adf12347edf08`) |
| host | gnode (Linux) |
| duration | 569.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "epochs": 3, "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "i1_csv": null, "layer": null, "lr": 0.001, "min_gap": 0.05, "model": "xlm-roberta-large", "n_eval": 1000, "n_train": 2000, "n_val": 200, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/das", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "pairs_per_step": 8, "random_seeds": 3, "ranks": [1, 4, 16, 64], "record_tag": null, "tag": "xlmrlarge", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv", "verb_ranks": [1, 16]}` |
| command | `scripts/rq1_das.py --tag xlmrlarge --model xlm-roberta-large --batch-size 16` |


- **layer / hidden size**: 20 / 1024
- **pairs: evaluation (I1's) / validation / training**: 1,000 / 200 / 2,000
- **evaluation documents / training and validation documents**: 582 / 347 (disjoint)

### Checks against I1's per-pair output, before training (largest departure, bits)

- **S(base) vs I1 s_var**: 1.78e-15
- **S(clean) vs I1 s_ref**: 1.35e-05
- **full patch, moved heads, vs I1 moved_heads@20**: 1.78e-15
- **full patch, verb, vs I1 verb@20**: 1.78e-15
- **moved_heads: training / validation pairs with the site present**: 2,000 of 2,000 / 200 of 200
- **verb: training / validation pairs with the site present**: 1,994 of 2,000 / 200 of 200

### Training (validation pairs; epoch 0 is the random initialisation)


| site | rank | epoch | mean KL | validation recovery |
|---|---|---|---|---|
| moved_heads | 1 | 0 | nan | 0.0007 |
| moved_heads | 1 | 1 | 0.3543 | 0.1608 |
| moved_heads | 1 | 2 | 0.3471 | 0.1592 |
| moved_heads | 1 | 3 | 0.3471 | 0.1623 |
| moved_heads | 4 | 0 | nan | 0.0035 |
| moved_heads | 4 | 1 | 0.3322 | 0.2522 |
| moved_heads | 4 | 2 | 0.3084 | 0.2639 |
| moved_heads | 4 | 3 | 0.3074 | 0.2702 |
| moved_heads | 16 | 0 | nan | 0.0127 |
| moved_heads | 16 | 1 | 0.2958 | 0.3571 |
| moved_heads | 16 | 2 | 0.2629 | 0.3905 |
| moved_heads | 16 | 3 | 0.2583 | 0.3838 |
| moved_heads | 64 | 0 | nan | 0.0438 |
| moved_heads | 64 | 1 | 0.2634 | 0.4784 |
| moved_heads | 64 | 2 | 0.2185 | 0.4927 |
| moved_heads | 64 | 3 | 0.2090 | 0.5082 |
| verb | 1 | 0 | nan | 0.0002 |
| verb | 1 | 1 | 0.3914 | 0.0273 |
| verb | 1 | 2 | 0.3848 | 0.0329 |
| verb | 1 | 3 | 0.3833 | 0.0440 |
| verb | 16 | 0 | nan | 0.0007 |
| verb | 16 | 1 | 0.3625 | 0.1326 |
| verb | 16 | 2 | 0.3430 | 0.1500 |
| verb | 16 | 3 | 0.3386 | 0.1537 |

- **evaluation pairs with a gap above --min-gap**: 862 of 1,000

## Share of the gap recovered on I1's pairs


| site | rank | learned | random (mean) | full state (I1) | p, learned vs random | p, learned vs full |
|---|---|---|---|---|---|---|
| moved_heads | 1 | 0.1821 | 0.0008 | 0.5794 | 0.0001 | 0.0001 |
| moved_heads | 4 | 0.2969 | 0.0034 | 0.5794 | 0.0001 | 0.0001 |
| moved_heads | 16 | 0.4413 | 0.0129 | 0.5794 | 0.0001 | 0.0001 |
| moved_heads | 64 | 0.5596 | 0.0502 | 0.5794 | 0.0001 | 0.0430 |
| verb | 1 | 0.0567 | 0.0003 | 0.1616 | 0.0001 | 0.0001 |
| verb | 16 | 0.1707 | 0.0039 | 0.1616 | 0.0001 | 0.3022 |

A ratio of sums over evaluation pairs, I1's measure: 1 closes the variant's gap to the reference, 0 leaves it. p: document-level sign-flip permutation on the per-pair difference in the amount moved, two-sided, 10,000 permutations. The verb complex is the site control.

- **rank-1 direction's sign in dv (the npz holds the unflipped Q)**: -1

## What the rank-1 variable tracks (moved head words, unmasked runs)


| against | Spearman over pairs | Spearman over documents | p (documents) | documents |
|---|---|---|---|---|
| the model's preference d_T | 0.1119 | 0.1445 | 0.0006 | 582 |
| E1, d_syn_order | 0.0941 | 0.1041 | 0.0109 | 582 |
| trigram, d_kenlm_mean | 0.0952 | 0.0901 | 0.0260 | 582 |
| moved heads' position change, dpos | -0.6736 | -0.6585 | 0.0001 | 582 |

dv is the change in the learned direction's value at the moved head words, reference minus variant, signed so that it rises with the model's own preference. Over documents: per-document means, permutation p over documents, 10,000. Descriptive.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `das_xlmrlarge.npz` | 419,352 | `ce1d546dac061d97` | the learned subspaces (k x d, orthonormal rows), per site and rank |
| `das_xlmrlarge.csv` | 681,761 | `abdee59647d02b8a` | per evaluation pair: clean and base runs, the base run under every condition, and (rank 1) dv, dpos and the E1 and trigram differences |
