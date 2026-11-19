# rq1_attention_mass_indicbert

_Attention mass arriving at the moved constituents, per layer, reference on reference sentences. Descriptive only._

| provenance | |
|---|---|
| run (UTC) | 2026-09-27 17:35 |
| script | `rq1_attention_mass.py` (sha256 `dcae432d2bed028d`) |
| host | gnode (Linux) |
| duration | 0.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"model": "<earlier-repo>/local_models/IndicBERTv2-MLM-only", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_attention_mass_indicbert", "tag": "indicbert"}` |
| command | `scripts/rq1_attention_mass.py --model <earlier-repo>/local_models/IndicBERTv2-MLM-only --tag indicbert --record-tag rq1_attention_mass_indicbert` |


- **references used / skipped**: 2,000 / 0
- **mean share of real subtokens that are moved words**: 0.4185

| layer | enrichment on the moved constituents | against uniform | share of attention on special tokens |
|---|---|---|---|
| 0 | 1.0566 | +0.0566 | 0.5942 |
| 1 | 1.0687 | +0.0687 | 0.7101 |
| 2 | 1.0120 | +0.0120 | 0.8011 |
| 3 | 1.0700 | +0.0700 | 0.7721 |
| 4 | 0.7145 | -0.2855 | 0.5959 |
| 5 | 0.5343 | -0.4657 | 0.5402 |
| 6 | 0.5477 | -0.4523 | 0.5118 |
| 7 | 0.5905 | -0.4095 | 0.5082 |
| 8 | 0.5646 | -0.4354 | 0.5319 |
| 9 | 0.5266 | -0.4734 | 0.5649 |
| 10 | 0.5482 | -0.4518 | 0.5596 |
| 11 | 0.5094 | -0.4906 | 0.0255 |

- **layer of highest enrichment**: 3 (1.0700)

> Enrichment is attention mass on the moved constituents divided by the share of subtokens they occupy, so 1.0 is what uniform attention gives and the number is comparable across sentences of different lengths.


> Descriptive only. Attention is not explanation: this can say whether the layers where the probes read most are also where attention concentrates on the moved material, and it cannot say that the attention causes the preference.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_attention_mass_indicbert.csv` | 515 | `4dbd2fdeb429b962` | per-layer attention enrichment on the moved constituents |
