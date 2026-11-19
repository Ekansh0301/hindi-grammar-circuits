# mi_swap_validate_wordorder_xlmrlarge

_Follow-up 3, halves swapped: validate, wordorder, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 15:30 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 46.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": "selection", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model xlmrlarge --max-rows 128 --chunk 8 --task wordorder --stage validate` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: selection
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **half read**: selection
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L9H2, L8H4, L17H3, L17H7, L9H3, L20H14, L16H4, L20H3, L19H8, L21H5
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 1.56e-04
- **mean-estimation positions: special / masked / other**: 600 / 376 / 6,541
- **pairs / skipped / with a gap above --min-gap**: 146 / 0 / 127

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.532 | [0.471, 0.626] | 0.1166 | 0.2453 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.01899 | [-0.033, 0.067] | 0.01663 | 0.05541 | 0.4455 | 0.9339 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 2.4256 | 0.0000 | yes |
| circuit ablated | 2.4812 | 0.0556 | yes |
| random set 0 | 2.4297 | 0.0040 | yes |
| random set 1 | 2.4522 | 0.0266 | yes |
| random set 2 | 2.4517 | 0.0261 | yes |
| random set 3 | 2.4580 | 0.0324 | yes |
| random set 4 | 2.4279 | 0.0023 | yes |
| random set 5 | 2.5067 | 0.0811 | yes |
| random set 6 | 2.4456 | 0.0200 | yes |
| random set 7 | 2.4297 | 0.0041 | yes |
| random set 8 | 2.4372 | 0.0116 | yes |
| random set 9 | 2.4584 | 0.0328 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L19MLP | 0.3752 | 0.3845 | [0.339, 0.440] |
| L18MLP | 0.3207 | 0.3194 | [0.275, 0.381] |
| L20MLP | 0.3067 | 0.3698 | [0.319, 0.441] |
| L21MLP | 0.2973 | 0.3255 | [0.290, 0.370] |
| L17MLP | 0.2400 | 0.2208 | [0.186, 0.265] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_wordorder_xlmrlarge.npz` | 176,089 | `24418dca1cbafe4f` | held-out half: each set patched (faithfulness) and ablated in both runs (necessity); set 0 is the circuit |
