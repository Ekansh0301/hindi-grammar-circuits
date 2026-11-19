# rq1_attention_mass_xlmrlarge

_Attention mass arriving at the moved constituents, per layer, reference on reference sentences. Descriptive only._

| provenance | |
|---|---|
| run (UTC) | 2026-09-27 17:37 |
| script | `rq1_attention_mass.py` (sha256 `dcae432d2bed028d`) |
| host | gnode (Linux) |
| duration | 1.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"model": "xlm-roberta-large", "n_refs": 2000, "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": "rq1_attention_mass_xlmrlarge", "tag": "xlmrlarge"}` |
| command | `scripts/rq1_attention_mass.py --model xlm-roberta-large --tag xlmrlarge --record-tag rq1_attention_mass_xlmrlarge` |


- **references used / skipped**: 2,000 / 0
- **mean share of real subtokens that are moved words**: 0.4515

| layer | enrichment on the moved constituents | against uniform | share of attention on special tokens |
|---|---|---|---|
| 0 | 0.8611 | -0.1389 | 0.1868 |
| 1 | 0.8872 | -0.1128 | 0.4756 |
| 2 | 0.9132 | -0.0868 | 0.6860 |
| 3 | 0.7827 | -0.2173 | 0.3746 |
| 4 | 0.7996 | -0.2004 | 0.4305 |
| 5 | 0.7354 | -0.2646 | 0.3535 |
| 6 | 0.6316 | -0.3684 | 0.2464 |
| 7 | 0.5596 | -0.4404 | 0.1735 |
| 8 | 0.6866 | -0.3134 | 0.1640 |
| 9 | 0.6187 | -0.3813 | 0.1482 |
| 10 | 0.6987 | -0.3013 | 0.1497 |
| 11 | 0.6239 | -0.3761 | 0.1568 |
| 12 | 0.6148 | -0.3852 | 0.1567 |
| 13 | 0.5908 | -0.4092 | 0.1796 |
| 14 | 0.6489 | -0.3511 | 0.3036 |
| 15 | 0.5919 | -0.4081 | 0.1286 |
| 16 | 0.7765 | -0.2235 | 0.4758 |
| 17 | 0.8090 | -0.1910 | 0.5155 |
| 18 | 0.9186 | -0.0814 | 0.5241 |
| 19 | 0.8721 | -0.1279 | 0.6955 |
| 20 | 0.6930 | -0.3070 | 0.5984 |
| 21 | 0.7275 | -0.2725 | 0.6550 |
| 22 | 0.7730 | -0.2270 | 0.5808 |
| 23 | 0.7630 | -0.2370 | 0.2806 |

- **layer of highest enrichment**: 18 (0.9186)

> Enrichment is attention mass on the moved constituents divided by the share of subtokens they occupy, so 1.0 is what uniform attention gives and the number is comparable across sentences of different lengths.


> Descriptive only. Attention is not explanation: this can say whether the layers where the probes read most are also where attention concentrates on the moved material, and it cannot say that the attention causes the preference.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `rq1_attention_mass_xlmrlarge.csv` | 1,018 | `221afdf3919aa607` | per-layer attention enrichment on the moved constituents |
