# rq1_word_state_probes_mbert

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 13:52 |
| script | `rq1_word_state_probes.py` (sha256 `36af65baffb5a95d`) |
| host | gnode (Linux) |
| duration | 27.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 20, "model": "bert-base-multilingual-cased", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "mbert"}` |
| command | `scripts/rq1_word_state_probes.py --model bert-base-multilingual-cased --tag mbert` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)


| layer | mean Spearman (5-50 words) | UUAS |
|---|---|---|
| control (pre-LayerNorm input) | 0.555 | 0.478 |
| 0 | 0.286 | 0.227 |
| 1 | 0.269 | 0.224 |
| 2 | 0.354 | 0.271 |
| 3 | 0.426 | 0.322 |
| 4 | 0.483 | 0.362 |
| 5 | 0.515 | 0.370 |
| 6 | 0.537 | 0.422 |
| 7 | 0.523 | 0.436 |
| 8 | 0.519 | 0.426 |
| 9 | 0.506 | 0.417 |
| 10 | 0.514 | 0.445 |
| 11 | 0.512 | 0.417 |
| 12 | 0.525 | 0.417 |


## F6: similarity of matched words, reference vs variant


| layer | linear CKA | mean cosine | cosine, moved words | cosine, other words |
|---|---|---|---|---|
| 0 | 0.9724 | 0.9634 | 0.9351 | 0.9808 |
| 1 | 0.9683 | 0.9653 | 0.9383 | 0.9819 |
| 2 | 0.9487 | 0.9571 | 0.9236 | 0.9777 |
| 3 | 0.9470 | 0.9620 | 0.9339 | 0.9792 |
| 4 | 0.9360 | 0.9626 | 0.9358 | 0.9790 |
| 5 | 0.9298 | 0.9675 | 0.9473 | 0.9800 |
| 6 | 0.9113 | 0.9649 | 0.9456 | 0.9767 |
| 7 | 0.9059 | 0.9516 | 0.9300 | 0.9648 |
| 8 | 0.9021 | 0.9432 | 0.9213 | 0.9566 |
| 9 | 0.9144 | 0.9575 | 0.9421 | 0.9670 |
| 10 | 0.9184 | 0.9706 | 0.9611 | 0.9764 |
| 11 | 0.9143 | 0.9780 | 0.9720 | 0.9817 |
| 12 | 0.9153 | 0.9473 | 0.9343 | 0.9553 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_mbert.csv` | 1,490 | `223dbb9cce0930c7` | distance: a = Spearman, b = UUAS; similarity: a = CKA, b = mean cosine |
