# rq1_attention_mass_muril

_Attention mass arriving at the moved constituents, per layer, reference on reference sentences. Descriptive only._

| provenance | |
|---|---|
| run (UTC) | 2026-09-27 17:34 |
| script | `rq1_attention_mass.py` (sha256 `dcae432d2bed028d`) |
| host | gnode (Linux) |
| duration | 0.8 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"model": "<earlier-repo>/local_models/muril-base-cased", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_attention_mass_muril", "tag": "muril"}` |
| command | `scripts/rq1_attention_mass.py --model <earlier-repo>/local_models/muril-base-cased --tag muril --record-tag rq1_attention_mass_muril` |


- **references used / skipped**: 2,000 / 0
- **mean share of real subtokens that are moved words**: 0.4232

| layer | enrichment on the moved constituents | against uniform | share of attention on special tokens |
|---|---|---|---|
| 0 | 0.9966 | -0.0034 | 0.3937 |
| 1 | 0.9775 | -0.0225 | 0.5328 |
| 2 | 1.0365 | +0.0365 | 0.5854 |
| 3 | 1.0757 | +0.0757 | 0.6797 |
| 4 | 1.0565 | +0.0565 | 0.6132 |
| 5 | 1.0685 | +0.0685 | 0.6960 |
| 6 | 0.9748 | -0.0252 | 0.6435 |
| 7 | 1.0277 | +0.0277 | 0.6689 |
| 8 | 1.0133 | +0.0133 | 0.7257 |
| 9 | 1.0242 | +0.0242 | 0.7661 |
| 10 | 0.7886 | -0.2114 | 0.7706 |
| 11 | 0.8964 | -0.1036 | 0.6688 |

- **layer of highest enrichment**: 3 (1.0757)

> Enrichment is attention mass on the moved constituents divided by the share of subtokens they occupy, so 1.0 is what uniform attention gives and the number is comparable across sentences of different lengths.


> Descriptive only. Attention is not explanation: this can say whether the layers where the probes read most are also where attention concentrates on the moved material, and it cannot say that the attention causes the preference.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_attention_mass_muril.csv` | 517 | `5e1408c449bf250f` | per-layer attention enrichment on the moved constituents |
