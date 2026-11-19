# mi_validate_wordorder_xlmrlarge

_Step 4 word order, stage validate, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 17:17 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 87.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate"}` |
| command | `scripts/mi_wordorder.py --stage validate --model xlmrlarge --max-rows 128 --chunk 8` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **half read**: heldout
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L9H2, L17H3, L17H7, L20H14, L17H15, L21H3, L6H15, L16H4, L16H1, L20H2
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.99e-05
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **pairs / skipped / with a gap above --min-gap**: 154 / 0 / 129

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.5348 | [0.482, 0.594] | 0.08285 | 0.2137 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.08588 | [0.038, 0.129] | 0.0138 | 0.04953 | 0.009901 | 0.0032 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 2.4256 | 0.0000 | yes |
| circuit ablated | 2.4755 | 0.0499 | yes |
| random set 0 | 2.4533 | 0.0277 | yes |
| random set 1 | 2.4279 | 0.0023 | yes |
| random set 2 | 2.4216 | -0.0040 | yes |
| random set 3 | 2.4459 | 0.0202 | yes |
| random set 4 | 2.4402 | 0.0146 | yes |
| random set 5 | 2.4742 | 0.0486 | yes |
| random set 6 | 2.4699 | 0.0443 | yes |
| random set 7 | 2.4543 | 0.0287 | yes |
| random set 8 | 2.4401 | 0.0145 | yes |
| random set 9 | 2.4843 | 0.0587 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L19MLP | 0.3845 | 0.3752 | [0.338, 0.417] |
| L20MLP | 0.3698 | 0.3067 | [0.278, 0.338] |
| L21MLP | 0.3255 | 0.2973 | [0.253, 0.339] |
| L18MLP | 0.3194 | 0.3207 | [0.277, 0.364] |
| L17MLP | 0.2208 | 0.2400 | [0.205, 0.272] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_wordorder_xlmrlarge.npz` | 186,035 | `1780a1960008b4b2` | held-out half: each set patched (faithfulness) and ablated in both runs (necessity); set 0 is the circuit |
