# rq1_agreement_order_score_mbert

_Agreement items scored by mbert._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 23:27 |
| script | `rq1_agreement_order.py` (sha256 `2c391d0c3174fe24`) |
| host | gnode (Linux) |
| duration | 53.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "cap": 30, "model": "mbert=bert-base-multilingual-cased", "models": ["muril", "indicbert", "xlmrlarge", "mbert"], "out_dir": "<earlier-repo>/sets/set1/Results_Checks/agreement", "permutations": 10000, "seed": 707, "stage": "score", "tag": null}` |
| command | `scripts/rq1_agreement_order.py --stage score --model mbert=bert-base-multilingual-cased --batch-size 24` |


- **items scored / unscorable**: 5,265 / 0

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `agreement_scores_mbert.csv` | 607,347 | `330d7b3ebda5bfd8` | summed PLL of the correct and the foil sentence per item |
