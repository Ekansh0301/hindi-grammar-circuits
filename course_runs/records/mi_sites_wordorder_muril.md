# mi_sites_wordorder_muril

_Step 4 word order, stage sites, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:07 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 4.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "sites"}` |
| command | `scripts/mi_wordorder.py --stage sites --model muril --max-rows 256` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 4.13e-05

| component | at special only | at moved_heads only | at moved_psp only | at moved_other only | at verb only | at unmoved only |
|---|---|---|---|---|---|---|
| L3H11 | 0.0000 | 0.0488 | 0.0318 | 0.0135 | 0.0022 | 0.0103 |
| L1H4 | -0.0002 | 0.0498 | 0.0245 | 0.0103 | 0.0001 | 0.0121 |
| L1H3 | 0.0000 | 0.0297 | 0.0117 | 0.0268 | 0.0127 | 0.0119 |
| L6H6 | 0.0001 | 0.0249 | 0.0218 | 0.0166 | 0.0105 | 0.0181 |
| L6H4 | 0.0000 | 0.0352 | 0.0292 | 0.0116 | 0.0017 | 0.0116 |
| L10MLP | 0.0000 | 0.2380 | 0.0856 | 0.1115 | 0.0657 | 0.0605 |
| L9MLP | -0.0002 | 0.2086 | 0.0878 | 0.0942 | 0.0499 | 0.0642 |
| L8MLP | -0.0007 | 0.1939 | 0.0987 | 0.1136 | 0.0377 | 0.0580 |
| L7MLP | -0.0008 | 0.1566 | 0.1217 | 0.0795 | 0.0170 | 0.0758 |
| L6MLP | -0.0003 | 0.1287 | 0.0754 | 0.0582 | 0.0071 | 0.0351 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `sites_wordorder_muril.npz` | 32,415 | `66cb0b358dc87d0c` | the exact stage's top 10, each patched at one site class at a time |
