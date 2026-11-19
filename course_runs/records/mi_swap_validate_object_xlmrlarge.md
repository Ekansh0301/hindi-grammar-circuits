# mi_swap_validate_object_xlmrlarge

_Follow-up 3, halves swapped: validate, object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 15:02 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 11.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "selection", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "object"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task object --stage validate` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: selection
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **exact-stage input**: exact_object_xlmrlarge.npz (sha256 af22db456cf36236)
- **half read**: selection
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L20H0, L21H0, L20H2, L19H3, L22H6, L12H6, L8H9, L10H9, L23H7, L8H6
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 387

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.7448 | [0.686, 0.830] | 0.001439 | 0.02203 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 1.01 | [0.880, 1.189] | 0.001956 | 0.04924 | 0.009901 | 9.999e-05 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 2.4256 | 0.0000 | yes |
| circuit ablated | 2.4843 | 0.0587 | yes |
| random set 0 | 2.4409 | 0.0153 | yes |
| random set 1 | 2.4694 | 0.0438 | yes |
| random set 2 | 2.4404 | 0.0148 | yes |
| random set 3 | 2.4427 | 0.0171 | yes |
| random set 4 | 2.4758 | 0.0502 | yes |
| random set 5 | 2.5439 | 0.1182 | yes |
| random set 6 | 2.4490 | 0.0234 | yes |
| random set 7 | 2.4462 | 0.0205 | yes |
| random set 8 | 2.4732 | 0.0476 | yes |
| random set 9 | 2.5159 | 0.0903 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L21MLP | 0.3412 | 0.3685 | [0.325, 0.428] |
| L20MLP | 0.2162 | 0.2237 | [0.190, 0.262] |
| L22MLP | 0.1283 | 0.1315 | [0.088, 0.183] |
| L23MLP | 0.1199 | 0.0795 | [0.048, 0.115] |
| L19MLP | 0.0616 | 0.0882 | [0.054, 0.125] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_object_xlmrlarge.npz` | 362,013 | `a5ace65675cd3d60` | held-out half: metric with each set patched (faithfulness) and ablated (necessity); set 0 is the circuit |
