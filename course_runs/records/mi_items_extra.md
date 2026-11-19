# mi_items_extra

_Items for the follow-up experiments: the word-order pool, reordering sizes, case-marker deletions._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:00 |
| script | `mi_items_extra.py` (sha256 `c96eb35136d7cd86`) |
| host | gnode (Linux) |
| duration | 0.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"out_dir": null, "record_tag": "mi_items_extra"}` |
| command | `scripts/mi_items_extra.py` |



| tokenizer | pairs | pairs whose site counts differ from step 2 |
|---|---|---|
| muril | 1000 | 0 |
| xlmrlarge | 1000 | 0 |

- **check: the 300 pairs of step 4 rebuilt here, pairs that differ from wordorder_pairs.csv**: 0 of 300

| pool | pairs | documents | size 1 | size 2-3 | size 4-7 | size 8+ |
|---|---|---|---|---|---|---|
| selection | 146 | 124 | 73 | 46 | 21 | 6 |
| heldout | 154 | 124 | 77 | 47 | 23 | 7 |
| seen_doc | 229 | 132 | 93 | 85 | 35 | 16 |
| fresh | 471 | 334 | 209 | 152 | 78 | 32 |


| fresh pairs | with moved_psp words | psp words deleted (mean per pair) | entering experiment 2 |
|---|---|---|---|
| 471 | 420 | 2.2071 | 223 |


| size bin | fresh pairs | entering experiment 2 |
|---|---|---|
| 1 | 209 | 100 |
| 2-3 | 152 | 80 |
| 4-7 | 78 | 32 |
| 8+ | 32 | 11 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `wordorder_pool.csv` | 1,053,596 | `48f5fad28d6996a3` | step 2's 1,000 pairs with pool, reordering size and the case-marker deletions |
