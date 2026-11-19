# rq1_layer_vs_output

_Readable layers against the output, by a document-level sign-flip test._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 18:20 |
| script | `rq1_layer_vs_output.py` (sha256 `d1a4c9e12262fb1a`) |
| host | gnode (Linux) |
| duration | 0.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"flips": 10000, "lenses": ["logit", "tuned", "jacobian"], "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "seed": 707, "tag": "rq1_layer_vs_output", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_layer_vs_output.py --tag rq1_layer_vs_output` |



## logit lens, muril

- **pairs / readable layers before the output**: 8,630 / none

## logit lens, indicbert

- **pairs / readable layers before the output**: 8,630 / 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 10 | -0.006976 | 0.0008999 | 0.0018 | -0.002214 | -0.005098 | 0.06167 | 0.07275 |
| 11 | -0.004845 | 0.005099 | 0.005099 | -0.001322 | -0.0003476 | 0.06375 | 0.07275 |


## logit lens, mbert

- **pairs / readable layers before the output**: 8,629 / none

## logit lens, xlmrlarge

- **pairs / readable layers before the output**: 8,630 / 21, 22, 23
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 21 | -0.01511 | 9.999e-05 | 0.0003 | -0.004785 | -0.005446 | 0.05923 | 0.08375 |
| 22 | -0.0132 | 9.999e-05 | 0.0003 | -0.004183 | -0.005678 | 0.06168 | 0.08375 |
| 23 | -0.008426 | 9.999e-05 | 0.0003 | -0.002643 | -0.003824 | 0.0696 | 0.08375 |


## tuned lens, muril

- **pairs / readable layers before the output**: 8,630 / 8, 9, 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 8 | -0.01029 | 0.0007999 | 0.0032 | -0.003264 | -0.003476 | 0.07501 | 0.08666 |
| 9 | -0.008344 | 0.0039 | 0.007799 | -0.002482 | -0.002897 | 0.07656 | 0.08666 |
| 10 | -0.003262 | 0.1229 | 0.1229 | -0.001098 | -0.002665 | 0.08261 | 0.08666 |
| 11 | -0.005177 | 0.0023 | 0.006899 | -0.00132 | 0.0006952 | 0.07952 | 0.08666 |


## tuned lens, indicbert

- **pairs / readable layers before the output**: 8,630 / 5, 6, 7, 8, 9, 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 5 | -0.02936 | 9.999e-05 | 0.0006999 | -0.009035 | -0.007648 | 0.02937 | 0.07275 |
| 6 | -0.02474 | 9.999e-05 | 0.0006999 | -0.007396 | -0.008111 | 0.03886 | 0.07275 |
| 7 | -0.01654 | 9.999e-05 | 0.0006999 | -0.004863 | -0.005098 | 0.0524 | 0.07275 |
| 8 | -0.008244 | 0.0014 | 0.005599 | -0.002531 | -0.004403 | 0.0639 | 0.07275 |
| 9 | -0.000759 | 0.7329 | 0.9077 | -0.0002255 | -0.003244 | 0.07432 | 0.07275 |
| 10 | -0.001419 | 0.3642 | 0.9077 | -0.0005852 | -0.00394 | 0.07088 | 0.07275 |
| 11 | 0.001173 | 0.3026 | 0.9077 | 0.0004063 | 0.0002317 | 0.07414 | 0.07275 |


## tuned lens, mbert

- **pairs / readable layers before the output**: 8,629 / 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 1 | -0.01293 | 9.999e-05 | 0.0011 | -0.004119 | -0.004404 | 0.001712 | 0.03176 |
| 2 | -0.01335 | 9.999e-05 | 0.0011 | -0.004223 | -0.003708 | 0.001354 | 0.03176 |
| 3 | -0.0127 | 9.999e-05 | 0.0011 | -0.003985 | -0.003593 | 0.003451 | 0.03176 |
| 4 | -0.01174 | 9.999e-05 | 0.0011 | -0.003716 | -0.002318 | 0.00584 | 0.03176 |
| 5 | -0.01052 | 9.999e-05 | 0.0011 | -0.00324 | -0.001854 | 0.01011 | 0.03176 |
| 6 | -0.008426 | 9.999e-05 | 0.0011 | -0.002363 | -0.002318 | 0.01775 | 0.03176 |
| 7 | -0.00602 | 0.0009999 | 0.004 | -0.001506 | 0.0005794 | 0.02283 | 0.03176 |
| 8 | -0.001511 | 0.3709 | 0.3709 | -8.135e-05 | 0.001738 | 0.03279 | 0.03176 |
| 9 | 0.002761 | 0.06979 | 0.1396 | 0.001335 | 0.001391 | 0.04125 | 0.03176 |
| 10 | 0.005364 | 9.999e-05 | 0.0011 | 0.001988 | 0.001391 | 0.04309 | 0.03176 |
| 11 | 0.002865 | 0.0024 | 0.007199 | 0.001068 | 0.002434 | 0.0379 | 0.03176 |


## tuned lens, xlmrlarge

- **pairs / readable layers before the output**: 8,630 / 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 9 | -0.04156 | 9.999e-05 | 0.0015 | -0.01372 | -0.01738 | 0.01819 | 0.08375 |
| 10 | -0.038 | 9.999e-05 | 0.0015 | -0.01247 | -0.01703 | 0.02597 | 0.08375 |
| 11 | -0.0333 | 9.999e-05 | 0.0015 | -0.01091 | -0.01194 | 0.03565 | 0.08375 |
| 12 | -0.028 | 9.999e-05 | 0.0015 | -0.009052 | -0.009965 | 0.04363 | 0.08375 |
| 13 | -0.02541 | 9.999e-05 | 0.0015 | -0.008127 | -0.008691 | 0.0477 | 0.08375 |
| 14 | -0.0238 | 9.999e-05 | 0.0015 | -0.007622 | -0.009618 | 0.05037 | 0.08375 |
| 15 | -0.02119 | 9.999e-05 | 0.0015 | -0.006576 | -0.0073 | 0.05491 | 0.08375 |
| 16 | -0.0207 | 9.999e-05 | 0.0015 | -0.006433 | -0.01124 | 0.05671 | 0.08375 |
| 17 | -0.01699 | 9.999e-05 | 0.0015 | -0.005232 | -0.00927 | 0.06168 | 0.08375 |
| 18 | -0.01399 | 9.999e-05 | 0.0015 | -0.004454 | -0.008575 | 0.06556 | 0.08375 |
| 19 | -0.008083 | 0.0024 | 0.012 | -0.002636 | -0.00533 | 0.07369 | 0.08375 |
| 20 | -0.003545 | 0.1072 | 0.2144 | -0.001386 | -0.002433 | 0.07992 | 0.08375 |
| 21 | -0.0014 | 0.4203 | 0.4203 | -0.0006929 | -0.001622 | 0.08222 | 0.08375 |
| 22 | -0.003185 | 0.0431 | 0.1293 | -0.001232 | -0.002086 | 0.07837 | 0.08375 |
| 23 | -0.003445 | 0.0047 | 0.0188 | -0.001198 | -0.001275 | 0.07902 | 0.08375 |


## jacobian lens, muril

- **pairs / readable layers before the output**: 8,630 / 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 10 | 0.00532 | 0.0243 | 0.0332 | 0.001554 | 0.004403 | 0.09737 | 0.08666 |
| 11 | -0.004145 | 0.0166 | 0.0332 | -0.001281 | 0 | 0.08161 | 0.08666 |


## jacobian lens, indicbert

- **pairs / readable layers before the output**: 8,630 / 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 10 | 0.0048 | 0.0244 | 0.0488 | 0.001175 | -0.002549 | 0.08261 | 0.07275 |
| 11 | 0.001877 | 0.2313 | 0.2313 | 0.0005441 | -0.002781 | 0.07525 | 0.07275 |


## jacobian lens, mbert

- **pairs / readable layers before the output**: 8,629 / 8, 9, 10, 11
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 8 | -0.005704 | 0.0007999 | 0.0016 | -0.001613 | 0.0003477 | 0.02118 | 0.03176 |
| 9 | 0.002192 | 0.1765 | 0.1765 | 0.000836 | 0.0002318 | 0.03876 | 0.03176 |
| 10 | 0.009034 | 9.999e-05 | 0.0004 | 0.002969 | 0.002318 | 0.05114 | 0.03176 |
| 11 | 0.005787 | 9.999e-05 | 0.0004 | 0.001998 | 0.002202 | 0.04418 | 0.03176 |


## jacobian lens, xlmrlarge

- **pairs / readable layers before the output**: 8,630 / 21, 22, 23
- **documents (the flip unit)**: 932

| layer | mean log-loss gain over the output (nats per pair) | permutation p | Holm p (this lens and model) | ΔAUC, layer minus output | Δaccuracy | ΔR²(T_layer | L,S) | ΔR²(T_output | L,S) |
|---|---|---|---|---|---|---|---|
| 21 | 0.009577 | 9.999e-05 | 0.0003 | 0.00263 | 0.006257 | 0.09768 | 0.08375 |
| 22 | -0.002806 | 0.1088 | 0.1088 | -0.001093 | -0.0005794 | 0.07911 | 0.08375 |
| 23 | -0.004047 | 0.0003 | 0.0005999 | -0.001375 | -0.0001159 | 0.07753 | 0.08375 |


## Benjamini-Hochberg across every test in this run


| test | permutation p | BH p |
|---|---|---|
| logit indicbert layer 10 | 0.0008999 | 0.00159 |
| logit indicbert layer 11 | 0.005099 | 0.007112 |
| logit xlmrlarge layer 21 | 9.999e-05 | 0.0002038 |
| logit xlmrlarge layer 22 | 9.999e-05 | 0.0002038 |
| logit xlmrlarge layer 23 | 9.999e-05 | 0.0002038 |
| tuned muril layer 8 | 0.0007999 | 0.001462 |
| tuned muril layer 9 | 0.0039 | 0.005741 |
| tuned muril layer 10 | 0.1229 | 0.1416 |
| tuned muril layer 11 | 0.0023 | 0.003634 |
| tuned indicbert layer 5 | 9.999e-05 | 0.0002038 |
| tuned indicbert layer 6 | 9.999e-05 | 0.0002038 |
| tuned indicbert layer 7 | 9.999e-05 | 0.0002038 |
| tuned indicbert layer 8 | 0.0014 | 0.002319 |
| tuned indicbert layer 9 | 0.7329 | 0.7329 |
| tuned indicbert layer 10 | 0.3642 | 0.3854 |
| tuned indicbert layer 11 | 0.3026 | 0.3273 |
| tuned mbert layer 1 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 2 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 3 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 4 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 5 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 6 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 7 | 0.0009999 | 0.00171 |
| tuned mbert layer 8 | 0.3709 | 0.3854 |
| tuned mbert layer 9 | 0.06979 | 0.08602 |
| tuned mbert layer 10 | 9.999e-05 | 0.0002038 |
| tuned mbert layer 11 | 0.0024 | 0.003634 |
| tuned xlmrlarge layer 9 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 10 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 11 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 12 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 13 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 14 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 15 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 16 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 17 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 18 | 9.999e-05 | 0.0002038 |
| tuned xlmrlarge layer 19 | 0.0024 | 0.003634 |
| tuned xlmrlarge layer 20 | 0.1072 | 0.1281 |
| tuned xlmrlarge layer 21 | 0.4203 | 0.4283 |
| tuned xlmrlarge layer 22 | 0.0431 | 0.05438 |
| tuned xlmrlarge layer 23 | 0.0047 | 0.006732 |
| jacobian muril layer 10 | 0.0243 | 0.03154 |
| jacobian muril layer 11 | 0.0166 | 0.02256 |
| jacobian indicbert layer 10 | 0.0244 | 0.03154 |
| jacobian indicbert layer 11 | 0.2313 | 0.2554 |
| jacobian mbert layer 8 | 0.0007999 | 0.001462 |
| jacobian mbert layer 9 | 0.1765 | 0.199 |
| jacobian mbert layer 10 | 9.999e-05 | 0.0002038 |
| jacobian mbert layer 11 | 9.999e-05 | 0.0002038 |
| jacobian xlmrlarge layer 21 | 9.999e-05 | 0.0002038 |
| jacobian xlmrlarge layer 22 | 0.1088 | 0.1281 |
| jacobian xlmrlarge layer 23 | 0.0003 | 0.0005888 |


## Summary


| lens | model | readable layers tested | layer with the largest gain | its gain (nats) | its Holm p | layers better than the output (Holm p < 0.05) | layers worse than the output (Holm p < 0.05) |
|---|---|---|---|---|---|---|---|
| logit | indicbert | 2 | 11 | -0.004845 | 0.005099 | 0 | 2 |
| logit | xlmrlarge | 3 | 23 | -0.008426 | 0.0003 | 0 | 3 |
| tuned | muril | 4 | 10 | -0.003262 | 0.1229 | 0 | 3 |
| tuned | indicbert | 7 | 11 | 0.001173 | 0.9077 | 0 | 4 |
| tuned | mbert | 11 | 10 | 0.005364 | 0.0011 | 2 | 7 |
| tuned | xlmrlarge | 15 | 21 | -0.0014 | 0.4203 | 0 | 12 |
| jacobian | muril | 2 | 10 | 0.00532 | 0.0332 | 1 | 1 |
| jacobian | indicbert | 2 | 10 | 0.0048 | 0.0488 | 1 | 0 |
| jacobian | mbert | 4 | 10 | 0.009034 | 0.0004 | 2 | 1 |
| jacobian | xlmrlarge | 3 | 21 | 0.009577 | 0.0003 | 1 | 1 |

10,000 document-level sign flips per test, so no p is below 0.00010. A positive gain means the layer's surprisal predicts the attested order better than the output's, with L + S + E1 in both models.
