# mi_path_xlmrlarge

_Step 4 agreement, stage path, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 16:36 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 8.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "path", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage path --model xlmrlarge --max-rows 128 --chunk 8` |


- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 387

| receiver head | through object | through subject | through ne | through all | through random other |
|---|---|---|---|---|---|
| L21H0 | 0.2317 | 0.0005 | 0.0000 | 0.3140 | -0.0001 |
| L20H0 | 0.2018 | 0.0012 | 0.0000 | 0.2338 | 0.0001 |
| L20H2 | 0.0699 | 0.0004 | -0.0010 | 0.0955 | 0.0005 |
| L22H6 | 0.0449 | -0.0004 | 0.0006 | 0.0712 | -0.0006 |
| L19H3 | 0.0404 | 0.0013 | -0.0004 | 0.0432 | -0.0008 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `path_xlmrlarge.npz` | 46,847 | `70bb5e6da8b11017` | per item x receiver head x sender set: metric with only that head's keys and values patched |
