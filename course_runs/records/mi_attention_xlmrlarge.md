# mi_attention_xlmrlarge

_Step 4 agreement, stage attention, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 16:27 |
| script | `mi_agreement.py` (sha256 `7f69a37e54e39b23`) |
| host | gnode (Linux) |
| duration | 0.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 16, "chunk": 8, "half": null, "k": 10, "k_mlp": 5, "limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "attention", "task": "object"}` |
| command | `scripts/mi_agreement.py --stage attention --model xlmrlarge --max-rows 128 --chunk 8` |


- **metric**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **heads read (top 5 heads of the object task, exact stage)**: L21H0, L20H0, L20H2, L22H6, L19H3

| head | to | mean share | clauses | OSV minus SOV | sign-flip p |
|---|---|---|---|---|---|
| L21H0 | object | 0.5215 | 52 | 0.02343 | 0.1106 |
| L21H0 | subject | 0.01035 | 52 | 0.000541 | 0.7048 |
| L21H0 | ne | 0.004849 | 52 | 0.001565 | 0.0207 |
| L20H0 | object | 0.7314 | 52 | 0.02931 | 0.07829 |
| L20H0 | subject | 0.01163 | 52 | -0.001282 | 0.1878 |
| L20H0 | ne | 0.006582 | 52 | -0.00329 | 9.999e-05 |
| L20H2 | object | 0.4452 | 52 | 0.0169 | 0.2536 |
| L20H2 | subject | 0.01361 | 52 | 0.002642 | 0.0138 |
| L20H2 | ne | 0.0706 | 52 | 0.02314 | 9.999e-05 |
| L22H6 | object | 0.264 | 52 | 0.02182 | 0.0186 |
| L22H6 | subject | 0.02459 | 52 | -0.0008293 | 0.7354 |
| L22H6 | ne | 0.08916 | 52 | 0.006852 | 0.05759 |
| L19H3 | object | 0.2583 | 52 | 0.0005784 | 0.9648 |
| L19H3 | subject | 0.03257 | 52 | 0.03705 | 9.999e-05 |
| L19H3 | ne | 0.07042 | 52 | 0.08152 | 9.999e-05 |
| all | object | 0.1023 | 52 | 0.001237 | 0.7882 |
| all | subject | 0.04981 | 52 | 0.006763 | 9.999e-05 |
| all | ne | 0.05383 | 52 | 0.01143 | 9.999e-05 |


> Descriptive: in an OSV-type order the subject is nearer the verb, so part of any shift toward it is distance.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `attention_xlmrlarge.csv` | 181,345 | `a76f1a3a39202487` | per order: attention share from the scored span to object, subject and ne, per head read |
