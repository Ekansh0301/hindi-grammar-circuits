# mi_sites_wordorder_xlmrlarge

_Step 4 word order, stage sites, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:29 |
| script | `mi_wordorder.py` (sha256 `d1fa24d1efb7b069`) |
| host | gnode (Linux) |
| duration | 18.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "sites"}` |
| command | `scripts/mi_wordorder.py --stage sites --model xlmrlarge --max-rows 128 --chunk 8` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 3.60e-05

| component | at special only | at moved_heads only | at moved_psp only | at moved_other only | at verb only | at unmoved only |
|---|---|---|---|---|---|---|
| L9H2 | -0.0005 | 0.0414 | 0.0179 | 0.0115 | -0.0013 | 0.0089 |
| L17H3 | 0.0000 | 0.0313 | 0.0149 | 0.0188 | 0.0045 | 0.0062 |
| L17H7 | -0.0005 | 0.0260 | 0.0142 | 0.0198 | 0.0107 | 0.0077 |
| L20H14 | 0.0000 | 0.0208 | 0.0133 | 0.0135 | 0.0119 | 0.0140 |
| L17H15 | -0.0004 | 0.0268 | 0.0127 | 0.0141 | 0.0085 | 0.0080 |
| L19MLP | -0.0005 | 0.1403 | 0.0916 | 0.0741 | 0.0383 | 0.0531 |
| L20MLP | -0.0002 | 0.1377 | 0.0721 | 0.0866 | 0.0346 | 0.0444 |
| L21MLP | -0.0001 | 0.1300 | 0.0618 | 0.0667 | 0.0340 | 0.0340 |
| L18MLP | 0.0000 | 0.1260 | 0.0706 | 0.0765 | 0.0283 | 0.0341 |
| L17MLP | -0.0008 | 0.0862 | 0.0458 | 0.0576 | 0.0188 | 0.0182 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `sites_wordorder_xlmrlarge.npz` | 32,055 | `a1075841de6d1ff6` | the exact stage's top 10, each patched at one site class at a time |
