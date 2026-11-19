# mi_swap_validate_object_muril

_Follow-up 3, halves swapped: validate, object, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:27 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 5.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "selection", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "object"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task object --stage validate` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: selection
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **exact-stage input**: exact_object_muril.npz (sha256 0873b5d3176cf284)
- **half read**: selection
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L8H3, L10H6, L11H1, L9H6, L11H2, L9H3, L10H10, L1H3, L9H8, L9H5
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 385

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.8311 | [0.772, 0.893] | 0.003312 | 0.05934 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.9437 | [0.837, 1.089] | 0.0002567 | 0.05488 | 0.009901 | 9.999e-05 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 3.0697 | 0.0000 | yes |
| circuit ablated | 3.2026 | 0.1329 | yes |
| random set 0 | 3.0981 | 0.0284 | yes |
| random set 1 | 3.1388 | 0.0691 | yes |
| random set 2 | 3.1256 | 0.0560 | yes |
| random set 3 | 3.1148 | 0.0451 | yes |
| random set 4 | 3.1237 | 0.0541 | yes |
| random set 5 | 3.1017 | 0.0320 | yes |
| random set 6 | 3.1451 | 0.0755 | yes |
| random set 7 | 3.1575 | 0.0879 | yes |
| random set 8 | 3.1231 | 0.0535 | yes |
| random set 9 | 3.0922 | 0.0225 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L11MLP | 0.4629 | 0.4488 | [0.400, 0.504] |
| L10MLP | 0.3690 | 0.3168 | [0.290, 0.346] |
| L8MLP | 0.2698 | 0.1940 | [0.154, 0.238] |
| L9MLP | 0.1613 | 0.2060 | [0.161, 0.257] |
| L0MLP | 0.0996 | 0.0814 | [0.041, 0.125] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_object_muril.npz` | 367,955 | `7e36624d3996144f` | held-out half: metric with each set patched (faithfulness) and ablated (necessity); set 0 is the circuit |
