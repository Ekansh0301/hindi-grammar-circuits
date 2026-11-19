# mi_metric_muril

_Step 4 agreement, stage metric, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 11:45 |
| script | `mi_agreement.py` (sha256 `ad41c1fb9a3f6c07`) |
| host | gnode (Linux) |
| duration | 10.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "metric", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage metric --model muril --max-rows 256` |


- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: single-word spans against score_words, orders / worst difference (bits)**: 200 / 1.15e-04
- **check: multi-word spans against a one-pass-at-a-time computation through the full logits (independent of the runs, hooks and batching; it shares the tokenisation and the span definition), orders / worst (bits)**: 50 / 1.13e-04

| masked | orders | correct preferred (M > 0) | mean M (bits) | clauses | OSV minus SOV (bits) | sign-flip p |
|---|---|---|---|---|---|---|
| none | 5265 | 0.9379 | 7.365 | 102 | -0.04576 | 0.795 |
| obj | 5265 | 0.5595 | 0.4983 | 102 | -0.03748 | 0.7481 |
| subj | 5265 | 0.913 | 6.652 | 102 | -1.244 | 9.999e-05 |
| ne | 5265 | 0.9221 | 6.43 | 102 | -0.54 | 0.009099 |

- **Pearson / Spearman of M (nothing masked) with the baseline's A, orders**: 0.571 / 0.545 (5,265)

| rule | met |
|---|---|
| single-word check on at least 20 orders | yes |
| multi-word check on at least 10 orders | yes |
| Spearman with A at least 0.5 | yes |
| M > 0 in at least 80% of orders | yes |
| intervening-subject contrast negative, p < 0.05 | NO |

- **DECISION (metric used by the later stages)**: REJECTED

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `metric_muril.csv` | 1,947,112 | `f00c439230487bec` | per order: M under each masking condition, and the baseline's whole-sentence A |
