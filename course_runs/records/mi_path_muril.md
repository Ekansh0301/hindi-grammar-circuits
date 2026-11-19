# mi_path_muril

_Step 4 agreement, stage path, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 16:01 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 4.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "path", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage path --model muril --max-rows 256` |


- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **items / skipped / with a gap above --min-gap**: 388 / 0 / 385

| receiver head | through object | through subject | through ne | through all | through random other |
|---|---|---|---|---|---|
| L10H6 | 0.2254 | 0.0001 | -0.0000 | 0.2844 | 0.0010 |
| L8H3 | 0.2947 | 0.0006 | -0.0003 | 0.3199 | -0.0019 |
| L11H1 | 0.0887 | -0.0002 | -0.0001 | 0.1261 | 0.0009 |
| L9H6 | 0.0447 | 0.0001 | 0.0003 | 0.0784 | 0.0004 |
| L11H2 | 0.0278 | 0.0003 | 0.0009 | 0.0461 | 0.0009 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `path_muril.npz` | 47,323 | `03884b695a7a8fa4` | per item x receiver head x sender set: metric with only that head's keys and values patched |
