# rq1_word_state_probes_indicbert

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 13:44 |
| script | `rq1_word_state_probes.py` (sha256 `36af65baffb5a95d`) |
| host | gnode (Linux) |
| duration | 24.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 20, "model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "indicbert"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)


| layer | mean Spearman (5-50 words) | UUAS |
|---|---|---|
| control (pre-LayerNorm input) | 0.563 | 0.481 |
| 0 | 0.464 | 0.362 |
| 1 | 0.575 | 0.471 |
| 2 | 0.630 | 0.522 |
| 3 | 0.659 | 0.564 |
| 4 | 0.707 | 0.597 |
| 5 | 0.722 | 0.622 |
| 6 | 0.725 | 0.626 |
| 7 | 0.694 | 0.587 |
| 8 | 0.667 | 0.574 |
| 9 | 0.628 | 0.521 |
| 10 | 0.613 | 0.515 |
| 11 | 0.338 | 0.364 |
| 12 | 0.549 | 0.449 |


## F6: similarity of matched words, reference vs variant


| layer | linear CKA | mean cosine | cosine, moved words | cosine, other words |
|---|---|---|---|---|
| 0 | 0.8883 | 0.9374 | 0.8854 | 0.9693 |
| 1 | 0.8327 | 0.9325 | 0.8828 | 0.9629 |
| 2 | 0.8582 | 0.9523 | 0.9189 | 0.9729 |
| 3 | 0.8457 | 0.9441 | 0.9091 | 0.9656 |
| 4 | 0.8253 | 0.9360 | 0.8947 | 0.9613 |
| 5 | 0.8438 | 0.9373 | 0.8991 | 0.9608 |
| 6 | 0.8549 | 0.9352 | 0.8999 | 0.9569 |
| 7 | 0.8736 | 0.9282 | 0.8948 | 0.9487 |
| 8 | 0.8607 | 0.9265 | 0.8917 | 0.9479 |
| 9 | 0.8542 | 0.9198 | 0.8909 | 0.9375 |
| 10 | 0.8185 | 0.9104 | 0.8715 | 0.9343 |
| 11 | 0.8158 | 0.8643 | 0.8464 | 0.8753 |
| 12 | 0.7739 | 0.9300 | 0.9193 | 0.9366 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_indicbert.csv` | 1,588 | `ac48ae4ff6403fc8` | distance: a = Spearman, b = UUAS; similarity: a = CKA, b = mean cosine |
