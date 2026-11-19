# rq1_das_mbert

_Distributed alignment search: is what the moved head words carry (I1) a low-rank subspace, and what does it encode?_

| provenance | |
|---|---|
| run (UTC) | 2026-10-04 22:58 |
| script | `rq1_das.py` (sha256 `e40adf12347edf08`) |
| host | gnode (Linux) |
| duration | 542.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "epochs": 3, "features": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_all.csv", "i1_csv": null, "layer": null, "lr": 0.001, "min_gap": 0.05, "model": "bert-base-multilingual-cased", "n_eval": 1000, "n_train": 2000, "n_val": 200, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/das", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "pairs_per_step": 8, "random_seeds": 3, "ranks": [1, 4, 16, 64], "record_tag": null, "tag": "mbert", "units": "<earlier-repo>/sets/set1/Results_Checks/rq1_features_units.csv", "verb_ranks": [1, 16]}` |
| command | `scripts/rq1_das.py --tag mbert --model bert-base-multilingual-cased --batch-size 24` |


- **layer / hidden size**: 10 / 768
- **pairs: evaluation (I1's) / validation / training**: 1,000 / 200 / 2,000
- **evaluation documents / training and validation documents**: 582 / 347 (disjoint)

### Checks against I1's per-pair output, before training (largest departure, bits)

- **S(base) vs I1 s_var**: 1.78e-15
- **S(clean) vs I1 s_ref**: 3.98e-06
- **full patch, moved heads, vs I1 moved_heads@10**: 1.78e-15
- **full patch, verb, vs I1 verb@10**: 1.78e-15
- **moved_heads: training / validation pairs with the site present**: 2,000 of 2,000 / 200 of 200
- **verb: training / validation pairs with the site present**: 1,994 of 2,000 / 200 of 200

### Training (validation pairs; epoch 0 is the random initialisation)


| site | rank | epoch | mean KL | validation recovery |
|---|---|---|---|---|
| moved_heads | 1 | 0 | nan | 0.0017 |
| moved_heads | 1 | 1 | 0.3430 | 0.1288 |
| moved_heads | 1 | 2 | 0.3390 | 0.1229 |
| moved_heads | 1 | 3 | 0.3389 | 0.1222 |
| moved_heads | 4 | 0 | nan | 0.0017 |
| moved_heads | 4 | 1 | 0.3190 | 0.2755 |
| moved_heads | 4 | 2 | 0.3088 | 0.2788 |
| moved_heads | 4 | 3 | 0.3083 | 0.2826 |
| moved_heads | 16 | 0 | nan | 0.0209 |
| moved_heads | 16 | 1 | 0.3003 | 0.3888 |
| moved_heads | 16 | 2 | 0.2797 | 0.4219 |
| moved_heads | 16 | 3 | 0.2766 | 0.4172 |
| moved_heads | 64 | 0 | nan | 0.0754 |
| moved_heads | 64 | 1 | 0.2801 | 0.4886 |
| moved_heads | 64 | 2 | 0.2551 | 0.4833 |
| moved_heads | 64 | 3 | 0.2494 | 0.4943 |
| verb | 1 | 0 | nan | 0.0006 |
| verb | 1 | 1 | 0.3532 | 0.0039 |
| verb | 1 | 2 | 0.3494 | 0.0096 |
| verb | 1 | 3 | 0.3490 | 0.0108 |
| verb | 16 | 0 | nan | 0.0070 |
| verb | 16 | 1 | 0.3345 | 0.1206 |
| verb | 16 | 2 | 0.3247 | 0.1203 |
| verb | 16 | 3 | 0.3230 | 0.1337 |

- **evaluation pairs with a gap above --min-gap**: 913 of 1,000

## Share of the gap recovered on I1's pairs


| site | rank | learned | random (mean) | full state (I1) | p, learned vs random | p, learned vs full |
|---|---|---|---|---|---|---|
| moved_heads | 1 | 0.1154 | 0.0017 | 0.4964 | 0.0001 | 0.0001 |
| moved_heads | 4 | 0.2840 | 0.0065 | 0.4964 | 0.0001 | 0.0001 |
| moved_heads | 16 | 0.4212 | 0.0180 | 0.4964 | 0.0001 | 0.0001 |
| moved_heads | 64 | 0.4920 | 0.0708 | 0.4964 | 0.0001 | 0.7692 |
| verb | 1 | 0.0064 | 0.0005 | 0.1463 | 0.0766 | 0.0001 |
| verb | 16 | 0.1169 | 0.0050 | 0.1463 | 0.0001 | 0.0003 |

A ratio of sums over evaluation pairs, I1's measure: 1 closes the variant's gap to the reference, 0 leaves it. p: document-level sign-flip permutation on the per-pair difference in the amount moved, two-sided, 10,000 permutations. The verb complex is the site control.

- **rank-1 direction's sign in dv (the npz holds the unflipped Q)**: -1

## What the rank-1 variable tracks (moved head words, unmasked runs)


| against | Spearman over pairs | Spearman over documents | p (documents) | documents |
|---|---|---|---|---|
| the model's preference d_T | 0.0258 | 0.0247 | 0.5490 | 582 |
| E1, d_syn_order | -0.0139 | 0.0153 | 0.7107 | 582 |
| trigram, d_kenlm_mean | 0.0276 | 0.0206 | 0.6260 | 582 |
| moved heads' position change, dpos | 0.3873 | 0.3868 | 0.0001 | 582 |

dv is the change in the learned direction's value at the moved head words, reference minus variant, signed so that it rises with the model's own preference. Over documents: per-document means, permutation p over documents, 10,000. Descriptive.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `das_mbert.npz` | 314,904 | `7bc6600580226a32` | the learned subspaces (k x d, orthonormal rows), per site and rank |
| `das_mbert.csv` | 675,628 | `36e63c2edf358e33` | per evaluation pair: clean and base runs, the base run under every condition, and (rank 1) dv, dpos and the E1 and trigram differences |
