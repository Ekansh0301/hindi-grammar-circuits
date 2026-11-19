# rq1_word_state_probes_muril

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 13:24 |
| script | `rq1_word_state_probes.py` (sha256 `36af65baffb5a95d`) |
| host | gnode (Linux) |
| duration | 27.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 20, "model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "muril"}` |
| command | `scripts/rq1_word_state_probes.py --model <earlier-repo>/local_models/muril-base-cased --tag muril` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)


| layer | mean Spearman (5-50 words) | UUAS |
|---|---|---|
| control (pre-LayerNorm input) | 0.575 | 0.501 |
| 0 | 0.440 | 0.357 |
| 1 | 0.460 | 0.371 |
| 2 | 0.597 | 0.490 |
| 3 | 0.659 | 0.529 |
| 4 | 0.710 | 0.596 |
| 5 | 0.697 | 0.602 |
| 6 | 0.698 | 0.610 |
| 7 | 0.705 | 0.616 |
| 8 | 0.708 | 0.617 |
| 9 | 0.668 | 0.578 |
| 10 | 0.660 | 0.572 |
| 11 | 0.659 | 0.565 |
| 12 | 0.722 | 0.666 |


## F6: similarity of matched words, reference vs variant


| layer | linear CKA | mean cosine | cosine, moved words | cosine, other words |
|---|---|---|---|---|
| 0 | 0.9102 | 0.9501 | 0.9188 | 0.9692 |
| 1 | 0.8959 | 0.9547 | 0.9242 | 0.9734 |
| 2 | 0.8784 | 0.9430 | 0.9067 | 0.9652 |
| 3 | 0.8662 | 0.9400 | 0.9065 | 0.9606 |
| 4 | 0.8495 | 0.9358 | 0.9016 | 0.9568 |
| 5 | 0.8644 | 0.9359 | 0.9059 | 0.9543 |
| 6 | 0.8550 | 0.9289 | 0.8960 | 0.9490 |
| 7 | 0.8379 | 0.9243 | 0.8894 | 0.9457 |
| 8 | 0.8858 | 0.9284 | 0.8972 | 0.9475 |
| 9 | 0.9081 | 0.9368 | 0.9100 | 0.9532 |
| 10 | 0.9129 | 0.9452 | 0.9205 | 0.9603 |
| 11 | 0.9034 | 0.9556 | 0.9343 | 0.9687 |
| 12 | 0.9484 | 0.9976 | 0.9969 | 0.9981 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_muril.csv` | 1,484 | `4f0d2dfbe9757484` | distance: a = Spearman, b = UUAS; similarity: a = CKA, b = mean cosine |
