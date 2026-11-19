# mi_decompose_xlmrlarge

_Where the baseline's intervening-subject effect lies, by word class, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:02 |
| script | `mi_decompose.py` (sha256 `34ed62f02606e6ee`) |
| host | gnode (Linux) |
| duration | 3.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"limit": null, "model": "xlmrlarge", "record_tag": null}` |
| command | `scripts/mi_decompose.py --model xlmrlarge` |


- **orders**: 739 of 739
- **check: classes sum to A, worst order (bits)**: 0.00e+00
- **check: A against the stored baseline sums, worst order (bits)**: 1.24e-03
- **check: the stored baseline margin's contrast on these orders, clauses / bits / p**: 102 / -0.2120 / 0.5796

| part of A | mean over orders (bits) | clauses | OSV minus SOV, gap-matched (bits) | sign-flip p |
|---|---|---|---|---|
| A | 9.051 | 102 | -0.212 | 0.5796 |
| A_agree | 5.509 | 102 | 0.08754 | 0.4299 |
| A_verb | 0.3879 | 102 | -0.09258 | 0.407 |
| A_object | 1.725 | 102 | -0.11 | 0.4308 |
| A_subject | 0.1119 | 102 | 0.7514 | 9.999e-05 |
| A_ne | -0.03216 | 102 | -0.03311 | 0.7971 |
| A_other | 1.35 | 102 | -0.8152 | 9.999e-05 |

A's row reproduces the baseline contrast (seed [707, model index], as baseline_check.py); the class rows add up to it within each clause. A class whose contrast carries the effect is where the intervening subject changes the scores; agree is the verb's own forms.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `decompose_xlmrlarge.csv` | 193,592 | `2f75aca045f2e0a5` | per order: the whole-sentence margin A, the stored baseline margin, and A's parts by word class |
