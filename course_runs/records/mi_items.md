# mi_items

_Items, pairs and the document split for step 4._

| provenance | |
|---|---|
| run (UTC) | 2026-10-23 11:20 |
| script | `mi_items.py` (sha256 `76107c9e6bc93be1`) |
| host | gnode (Linux) |
| duration | 0.6 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"n_wordorder": 300, "out_dir": null, "record_tag": "mi_items"}` |
| command | `scripts/mi_items.py` |


- **orders rebuilt and checked**: 5,265 of 5,265

| contrast pairs | cells | clauses | documents |
|---|---|---|---|
| 670 | 207 | 102 | 91 |


| half | documents | clauses | contrast pairs | orders in pairs | OSV-type | SOV-type |
|---|---|---|---|---|---|---|
| selection | 46 | 52 | 356 | 388 | 198 | 190 |
| heldout | 45 | 50 | 314 | 351 | 181 | 170 |


| tokenizer | pairs | pairs whose site counts differ from step 2 |
|---|---|---|
| muril | 300 | 0 |
| xlmrlarge | 300 | 0 |


| word-order half | documents | pairs |
|---|---|---|
| selection | 124 | 146 |
| heldout | 124 | 154 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `agreement_positions.csv` | 4,510,716 | `ca574a0b98ab94b5` | every agreement order with word positions, document and half |
| `contrast_pairs.csv` | 117,008 | `e6280b2d0445d18f` | OSV-type / SOV-type pairs within clause and gap, with the half |
| `wordorder_pairs.csv` | 213,491 | `97b4a793263d48c7` | 300 of step 2's patched pairs: texts, word alignment, sites, half |
