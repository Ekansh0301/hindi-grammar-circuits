# mi_decompose_muril

_Where the baseline's intervening-subject effect lies, by word class, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 12:01 |
| script | `mi_decompose.py` (sha256 `34ed62f02606e6ee`) |
| host | gnode (Linux) |
| duration | 3.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "model": "muril", "record_tag": null}` |
| command | `scripts/mi_decompose.py --model muril` |


- **orders**: 739 of 739
- **check: classes sum to A, worst order (bits)**: 0.00e+00
- **check: A against the stored baseline sums, worst order (bits)**: 7.99e-04
- **check: the stored baseline margin's contrast on these orders, clauses / bits / p**: 102 / -1.7468 / 9.999e-05

| part of A | mean over orders (bits) | clauses | OSV minus SOV, gap-matched (bits) | sign-flip p |
|---|---|---|---|---|
| A | 11.72 | 102 | -1.747 | 9.999e-05 |
| A_agree | 6.014 | 102 | -0.2294 | 0.1454 |
| A_verb | 0.6358 | 102 | 0.149 | 0.3199 |
| A_object | 2.937 | 102 | -0.4519 | 0.0181 |
| A_subject | 0.03211 | 102 | 0.4836 | 0.0002 |
| A_ne | 0.1262 | 102 | 0.1161 | 0.0442 |
| A_other | 1.979 | 102 | -1.814 | 9.999e-05 |

A's row reproduces the baseline contrast (seed [707, model index], as baseline_check.py); the class rows add up to it within each clause. A class whose contrast carries the effect is where the intervening subject changes the scores; agree is the verb's own forms.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `decompose_muril.csv` | 192,912 | `f0ef8ec9d70c33d0` | per order: the whole-sentence margin A, the stored baseline margin, and A's parts by word class |
