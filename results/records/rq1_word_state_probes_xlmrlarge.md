# rq1_word_state_probes_xlmrlarge

_Structural distance probe and reference-variant similarity per layer._

| provenance | |
|---|---|
| run (UTC) | 2026-09-17 14:31 |
| script | `rq1_word_state_probes.py` (sha256 `2789b7829b1e6a4c`) |
| host | gnode (Linux) |
| duration | 46.1 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"epochs": 20, "model": "xlm-roberta-large", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "tag": "xlmrlarge"}` |
| command | `scripts/rq1_word_state_probes.py --model xlm-roberta-large --tag xlmrlarge` |


- **pairs with word states**: 2,000
- **training / held-out references (by document)**: 1,623 / 377

## F5: structural distance probe (held-out references)


| layer | mean Spearman (5-50 words) | UUAS |
|---|---|---|
| control (pre-LayerNorm input) | 0.505 | 0.419 |
| 0 | 0.176 | 0.202 |
| 1 | 0.235 | 0.210 |
| 2 | 0.295 | 0.249 |
| 3 | 0.356 | 0.259 |
| 4 | 0.371 | 0.263 |
| 5 | 0.384 | 0.294 |
| 6 | 0.410 | 0.304 |
| 7 | 0.433 | 0.301 |
| 8 | 0.487 | 0.350 |
| 9 | 0.518 | 0.389 |
| 10 | 0.543 | 0.410 |
| 11 | 0.545 | 0.429 |
| 12 | 0.441 | 0.376 |
| 13 | 0.368 | 0.375 |
| 14 | 0.391 | 0.385 |
| 15 | 0.364 | 0.357 |
| 16 | 0.338 | 0.366 |
| 17 | 0.334 | 0.376 |
| 18 | 0.340 | 0.379 |
| 19 | 0.342 | 0.361 |
| 20 | 0.364 | 0.349 |
| 21 | 0.381 | 0.345 |
| 22 | 0.422 | 0.351 |
| 23 | 0.427 | 0.316 |
| 24 | 0.538 | 0.427 |


## F6: similarity of matched words, reference vs variant


| layer | linear CKA | mean cosine | cosine, moved words | cosine, other words |
|---|---|---|---|---|
| 0 | 0.9583 | 0.9680 | 0.9490 | 0.9797 |
| 1 | 0.9661 | 0.9816 | 0.9681 | 0.9898 |
| 2 | 0.9396 | 0.9796 | 0.9646 | 0.9889 |
| 3 | 0.9563 | 0.9808 | 0.9674 | 0.9890 |
| 4 | 0.9577 | 0.9839 | 0.9739 | 0.9901 |
| 5 | 0.9537 | 0.9845 | 0.9748 | 0.9905 |
| 6 | 0.9496 | 0.9866 | 0.9780 | 0.9919 |
| 7 | 0.9487 | 0.9865 | 0.9780 | 0.9918 |
| 8 | 0.9376 | 0.9866 | 0.9780 | 0.9919 |
| 9 | 0.9189 | 0.9852 | 0.9767 | 0.9904 |
| 10 | 0.9122 | 0.9834 | 0.9736 | 0.9894 |
| 11 | 0.9045 | 0.9831 | 0.9741 | 0.9886 |
| 12 | 0.7962 | 0.9773 | 0.9718 | 0.9806 |
| 13 | 0.7442 | 0.9721 | 0.9701 | 0.9734 |
| 14 | 0.7348 | 0.9719 | 0.9701 | 0.9730 |
| 15 | 0.7275 | 0.9713 | 0.9706 | 0.9718 |
| 16 | 0.7260 | 0.9728 | 0.9714 | 0.9737 |
| 17 | 0.7283 | 0.9740 | 0.9722 | 0.9751 |
| 18 | 0.7299 | 0.9751 | 0.9732 | 0.9763 |
| 19 | 0.7251 | 0.9746 | 0.9735 | 0.9754 |
| 20 | 0.7478 | 0.9797 | 0.9793 | 0.9799 |
| 21 | 0.7403 | 0.9832 | 0.9835 | 0.9830 |
| 22 | 0.6938 | 0.9807 | 0.9834 | 0.9790 |
| 23 | 0.6788 | 0.9785 | 0.9829 | 0.9758 |
| 24 | 0.7239 | 0.9974 | 0.9981 | 0.9970 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_word_state_probes_xlmrlarge.csv` | 3,069 | `707de476a856edf2` | distance: a = Spearman, b = UUAS; similarity: a = CKA, b = mean cosine |
