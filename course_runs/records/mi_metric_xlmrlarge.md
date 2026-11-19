# mi_metric_xlmrlarge

_Step 4 agreement, stage metric, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 11:51 |
| script | `mi_agreement.py` (sha256 `ad41c1fb9a3f6c07`) |
| host | gnode (Linux) |
| duration | 17.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "metric", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage metric --model xlmrlarge --max-rows 128 --chunk 8` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: single-word spans against score_words, orders / worst difference (bits)**: 200 / 1.86e-04
- **check: multi-word spans against a one-pass-at-a-time computation through the full logits (independent of the runs, hooks and batching; it shares the tokenisation and the span definition), orders / worst (bits)**: 50 / 2.07e-04

| masked | orders | correct preferred (M > 0) | mean M (bits) | clauses | OSV minus SOV (bits) | sign-flip p |
|---|---|---|---|---|---|---|
| none | 5265 | 0.9519 | 6.941 | 102 | 0.1637 | 0.2597 |
| obj | 5265 | 0.5504 | 0.5799 | 102 | 0.2061 | 0.1621 |
| subj | 5265 | 0.9278 | 6.116 | 102 | -1.128 | 9.999e-05 |
| ne | 5265 | 0.9314 | 6.014 | 102 | -0.3339 | 0.06599 |

- **Pearson / Spearman of M (nothing masked) with the baseline's A, orders**: 0.550 / 0.547 (5,265)

| rule | met |
|---|---|
| single-word check on at least 20 orders | yes |
| multi-word check on at least 10 orders | yes |
| Spearman with A at least 0.5 | yes |
| M > 0 in at least 80% of orders | yes |

- **DECISION (metric used by the later stages)**: ACCEPTED

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `metric_xlmrlarge.csv` | 1,946,275 | `0f9bdf8420a541eb` | per order: M under each masking condition, and the baseline's whole-sentence A |
