# mi_validate_object_xlmrlarge

_Step 4 agreement, stage validate, task object, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 18:57 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 17.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage validate --task object --model xlmrlarge --max-rows 128 --chunk 8` |


- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **exact-stage input**: exact_object_xlmrlarge.npz (sha256 ca14575fa4257472)
- **half read**: heldout
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **items / skipped / with a gap above --min-gap**: 351 / 0 / 351

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.7799 | [0.711, 0.848] | -0.002935 | 0.01881 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 1.08 | [0.943, 1.247] | 0.004691 | 0.05887 | 0.009901 | 9.999e-05 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 2.4256 | 0.0000 | yes |
| circuit ablated | 2.4832 | 0.0576 | yes |
| random set 0 | 2.4600 | 0.0344 | yes |
| random set 1 | 2.5418 | 0.1162 | yes |
| random set 2 | 2.4401 | 0.0144 | yes |
| random set 3 | 2.4525 | 0.0269 | yes |
| random set 4 | 2.4466 | 0.0209 | yes |
| random set 5 | 2.4405 | 0.0149 | yes |
| random set 6 | 2.4449 | 0.0193 | yes |
| random set 7 | 2.4634 | 0.0378 | yes |
| random set 8 | 2.4577 | 0.0321 | yes |
| random set 9 | 2.4469 | 0.0213 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L21MLP | 0.3685 | 0.3412 | [0.293, 0.390] |
| L20MLP | 0.2237 | 0.2162 | [0.178, 0.250] |
| L22MLP | 0.1315 | 0.1283 | [0.079, 0.180] |
| L19MLP | 0.0882 | 0.0616 | [0.013, 0.097] |
| L23MLP | 0.0795 | 0.1199 | [0.086, 0.160] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_object_xlmrlarge.npz` | 331,096 | `150b5a99fc83be34` | held-out half: metric with each set patched (faithfulness) and ablated (necessity); set 0 is the circuit |
