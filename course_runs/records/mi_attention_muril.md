# mi_attention_muril

_Step 4 agreement, stage attention, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 15:56 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 0.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "attention", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage attention --model muril --max-rows 256` |


- **metric**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **heads read (top 5 heads of the object task, exact stage)**: L10H6, L8H3, L11H1, L9H6, L11H2

| head | to | mean share | clauses | OSV minus SOV | sign-flip p |
|---|---|---|---|---|---|
| L10H6 | object | 0.6031 | 52 | -0.05076 | 0.011 |
| L10H6 | subject | 0.009543 | 52 | 0.00444 | 9.999e-05 |
| L10H6 | ne | 0.01462 | 52 | 0.01028 | 9.999e-05 |
| L8H3 | object | 0.5816 | 52 | -0.01475 | 0.4295 |
| L8H3 | subject | 0.03037 | 52 | 0.0113 | 9.999e-05 |
| L8H3 | ne | 0.1074 | 52 | 0.02504 | 0.0002 |
| L11H1 | object | 0.4177 | 52 | 0.004951 | 0.6506 |
| L11H1 | subject | 0.02367 | 52 | 0.01058 | 9.999e-05 |
| L11H1 | ne | 0.03214 | 52 | 0.01397 | 9.999e-05 |
| L9H6 | object | 0.3107 | 52 | 0.02234 | 0.1366 |
| L9H6 | subject | 0.0126 | 52 | 0.01471 | 9.999e-05 |
| L9H6 | ne | 0.01684 | 52 | 0.02272 | 9.999e-05 |
| L11H2 | object | 0.2794 | 52 | 0.02887 | 0.014 |
| L11H2 | subject | 0.02566 | 52 | 0.01429 | 9.999e-05 |
| L11H2 | ne | 0.0549 | 52 | 0.03973 | 9.999e-05 |
| all | object | 0.1235 | 52 | 0.005456 | 0.0142 |
| all | subject | 0.04853 | 52 | 0.0141 | 9.999e-05 |
| all | ne | 0.06349 | 52 | 0.02459 | 9.999e-05 |


> Descriptive: in an OSV-type order the subject is nearer the verb, so part of any shift toward it is distance.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `attention_muril.csv` | 180,935 | `2445bbcf0fd49cc7` | per order: attention share from the scored span to object, subject and ne, per head read |
