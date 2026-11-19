# rq1_attention_mass_mbert

_Attention mass arriving at the moved constituents, per layer, reference on reference sentences. Descriptive only._

| provenance | |
|---|---|
| run (UTC) | 2026-09-27 17:35 |
| script | `rq1_attention_mass.py` (sha256 `dcae432d2bed028d`) |
| host | gnode (Linux) |
| duration | 0.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"model": "bert-base-multilingual-cased", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_attention_mass_mbert", "tag": "mbert"}` |
| command | `scripts/rq1_attention_mass.py --model bert-base-multilingual-cased --tag mbert --record-tag rq1_attention_mass_mbert` |


- **references used / skipped**: 2,000 / 0
- **mean share of real subtokens that are moved words**: 0.4967

| layer | enrichment on the moved constituents | against uniform | share of attention on special tokens |
|---|---|---|---|
| 0 | 0.9447 | -0.0553 | 0.1652 |
| 1 | 0.8854 | -0.1146 | 0.5663 |
| 2 | 0.9613 | -0.0387 | 0.5461 |
| 3 | 0.9588 | -0.0412 | 0.4263 |
| 4 | 1.0082 | +0.0082 | 0.4836 |
| 5 | 0.9504 | -0.0496 | 0.1491 |
| 6 | 0.9500 | -0.0500 | 0.1826 |
| 7 | 0.9945 | -0.0055 | 0.1941 |
| 8 | 0.9837 | -0.0163 | 0.2429 |
| 9 | 0.9973 | -0.0027 | 0.2365 |
| 10 | 1.0171 | +0.0171 | 0.1930 |
| 11 | 0.9623 | -0.0377 | 0.1611 |

- **layer of highest enrichment**: 10 (1.0171)

> Enrichment is attention mass on the moved constituents divided by the share of subtokens they occupy, so 1.0 is what uniform attention gives and the number is comparable across sentences of different lengths.


> Descriptive only. Attention is not explanation: this can say whether the layers where the probes read most are also where attention concentrates on the moved material, and it cannot say that the attention causes the preference.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_attention_mass_mbert.csv` | 524 | `31912d50e06bc884` | per-layer attention enrichment on the moved constituents |
