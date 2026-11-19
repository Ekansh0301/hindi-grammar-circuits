# mi_swap_validate_wordorder_muril

_Follow-up 3, halves swapped: validate, wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:29 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 10.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "selection", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task wordorder --stage validate` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: selection
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **half read**: selection
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L1H3, L3H11, L9H10, L1H4, L8H11, L6H4, L9H3, L6H10, L10H4, L7H2
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.66e-05
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **pairs / skipped / with a gap above --min-gap**: 146 / 0 / 124

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.7793 | [0.712, 0.850] | 0.2001 | 0.3439 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.07467 | [0.004, 0.145] | 0.01437 | 0.07332 | 0.05941 | 0.07079 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 3.0697 | 0.0000 | yes |
| circuit ablated | 3.1843 | 0.1146 | yes |
| random set 0 | 3.1051 | 0.0355 | yes |
| random set 1 | 3.0712 | 0.0015 | yes |
| random set 2 | 3.1205 | 0.0508 | yes |
| random set 3 | 3.0762 | 0.0066 | yes |
| random set 4 | 3.1004 | 0.0307 | yes |
| random set 5 | 3.0887 | 0.0191 | yes |
| random set 6 | 3.0872 | 0.0176 | yes |
| random set 7 | 3.0905 | 0.0209 | yes |
| random set 8 | 3.0664 | -0.0032 | yes |
| random set 9 | 3.0979 | 0.0283 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L10MLP | 0.5627 | 0.5585 | [0.502, 0.634] |
| L9MLP | 0.4950 | 0.4929 | [0.452, 0.543] |
| L8MLP | 0.4532 | 0.4863 | [0.437, 0.552] |
| L7MLP | 0.3770 | 0.4245 | [0.373, 0.483] |
| L6MLP | 0.2433 | 0.2992 | [0.250, 0.365] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_wordorder_muril.npz` | 179,319 | `3f3e8764e2d8e511` | held-out half: each set patched (faithfulness) and ablated in both runs (necessity); set 0 is the circuit |
