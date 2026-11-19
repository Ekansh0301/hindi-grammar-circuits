# mi_validate_object_muril

_Step 4 agreement, stage validate, task object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 18:46 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 7.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage validate --task object --model muril --max-rows 256` |


- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **exact-stage input**: exact_object_muril.npz (sha256 8e4ed1d349941829)
- **half read**: heldout
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 348

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.8979 | [0.860, 0.931] | 0.004569 | 0.05961 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.9652 | [0.887, 1.045] | 0.004642 | 0.05035 | 0.009901 | 9.999e-05 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 3.0697 | 0.0000 | yes |
| circuit ablated | 3.2802 | 0.2106 | yes |
| random set 0 | 3.1132 | 0.0436 | yes |
| random set 1 | 3.1008 | 0.0312 | yes |
| random set 2 | 3.1767 | 0.1071 | yes |
| random set 3 | 3.1432 | 0.0735 | yes |
| random set 4 | 3.1946 | 0.1249 | yes |
| random set 5 | 3.1295 | 0.0598 | yes |
| random set 6 | 3.1165 | 0.0468 | yes |
| random set 7 | 3.1321 | 0.0624 | yes |
| random set 8 | 3.1516 | 0.0819 | yes |
| random set 9 | 3.1098 | 0.0401 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L11MLP | 0.4488 | 0.4629 | [0.427, 0.500] |
| L10MLP | 0.3168 | 0.3690 | [0.334, 0.404] |
| L9MLP | 0.2060 | 0.1613 | [0.126, 0.198] |
| L8MLP | 0.1940 | 0.2698 | [0.212, 0.327] |
| L0MLP | 0.0814 | 0.0996 | [0.052, 0.153] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_object_muril.npz` | 336,565 | `b04c89099df85689` | held-out half: metric with each set patched (faithfulness) and ablated (necessity); set 0 is the circuit |
