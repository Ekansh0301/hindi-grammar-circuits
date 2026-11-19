# mi_validate_wordorder_muril

_Step 4 word order, stage validate, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 16:13 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 24.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "validate"}` |
| command | `scripts/mi_wordorder.py --stage validate --model muril --max-rows 256` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **half read**: heldout
- **random sets: distinct (as sets) of asked / replacements / layer-unmatched / type-unmatched**: 100 of 100 / 1000 / 0 / 0
- **circuit (the top K heads of the exact stage, selection half)**: L3H11, L1H4, L1H3, L6H6, L6H4, L9H6, L9H10, L8H11, L2H11, L9H3
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.60e-05
- **mean-estimation positions: special / masked / other**: 600 / 326 / 5,477
- **pairs / skipped / with a gap above --min-gap**: 154 / 0 / 135

| test | circuit | document bootstrap 95% | random sets, mean | random sets, 95th percentile | rank p among random sets | document sign-flip p, circuit minus random mean |
|---|---|---|---|---|---|---|
| faithfulness (share restored by patching only the set) | 0.7788 | [0.717, 0.839] | 0.1601 | 0.2648 | 0.009901 | 9.999e-05 |
| necessity (share of the gap lost by ablating the set) | 0.0598 | [-0.001, 0.112] | 0.007719 | 0.06725 | 0.07921 | 0.05559 |


| model | held-out nats per subtoken | minus unablated | within 2 nats |
|---|---|---|---|
| unablated | 3.0697 | 0.0000 | yes |
| circuit ablated | 3.1454 | 0.0758 | yes |
| random set 0 | 3.0915 | 0.0218 | yes |
| random set 1 | 3.0862 | 0.0165 | yes |
| random set 2 | 3.0713 | 0.0016 | yes |
| random set 3 | 3.0816 | 0.0119 | yes |
| random set 4 | 3.0848 | 0.0151 | yes |
| random set 5 | 3.0784 | 0.0087 | yes |
| random set 6 | 3.0742 | 0.0045 | yes |
| random set 7 | 3.0687 | -0.0009 | yes |
| random set 8 | 3.0553 | -0.0143 | yes |
| random set 9 | 3.0861 | 0.0164 | yes |


| MLP (top by the exact stage) | share, selection half | share, held-out half | document bootstrap 95% |
|---|---|---|---|
| L10MLP | 0.5585 | 0.5627 | [0.523, 0.606] |
| L9MLP | 0.4929 | 0.4950 | [0.453, 0.537] |
| L8MLP | 0.4863 | 0.4532 | [0.401, 0.512] |
| L7MLP | 0.4245 | 0.3770 | [0.327, 0.430] |
| L6MLP | 0.2992 | 0.2433 | [0.190, 0.297] |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `validate_wordorder_muril.npz` | 188,795 | `1f4ac31936170bed` | held-out half: each set patched (faithfulness) and ablated in both runs (necessity); set 0 is the circuit |
