# rq1_late_ablation_mbert

_Mean-ablation of late sublayers, rescored and gated by readability._

| provenance | |
|---|---|
| run (UTC) | 2026-10-02 19:06 |
| script | `rq1_late_ablation.py` (sha256 `9e1ef673abdb62c3`) |
| host | gnode (Linux) |
| duration | 549.5 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"batch_size": 24, "blocks": [11, 12], "conditions": null, "limit": null, "model": "bert-base-multilingual-cased", "n_mean": 300, "out_dir": "<earlier-repo>/sets/set1/Results_Checks/late_ablation", "pairs": "<earlier-repo>/sets/set1/Results_Checks/rq1_sample_n12000.csv", "record_tag": null, "sentences": "<earlier-repo>/Results_Checks/indiccorp_sample/readability_sentences.txt", "tag": "mbert"}` |
| command | `scripts/rq1_late_ablation.py --tag mbert --model bert-base-multilingual-cased --batch-size 24 --blocks 11 12` |



| k | condition |
|---|---|
| 0 | none |
| 1 | block 11 attention |
| 2 | block 11 MLP |
| 3 | block 11 whole |
| 4 | block 12 attention |
| 5 | block 12 MLP |
| 6 | block 12 whole |
| 7 | all listed blocks |

- **mean-estimation sentences / positions**: 300 / 10,711
- **unablated: largest departure from the published sums (bits)**: 5.68e-14

| k | condition | held-out nats per subtoken | minus unablated | READ (within 2 nats) | pairs | reference preferred |
|---|---|---|---|---|---|---|
| 0 | none | 3.3467 | 0.0000 | yes | 8922 | 0.7428 |
| 1 | block 11 attention | 3.2958 | -0.0509 | yes | 8922 | 0.7761 |
| 2 | block 11 MLP | 3.4835 | 0.1368 | yes | 8922 | 0.7376 |
| 3 | block 11 whole | 3.3996 | 0.0529 | yes | 8922 | 0.7740 |
| 4 | block 12 attention | 3.2332 | -0.1135 | yes | 8922 | 0.7830 |
| 5 | block 12 MLP | 3.7118 | 0.3651 | yes | 8922 | 0.7217 |
| 6 | block 12 whole | 3.4584 | 0.1117 | yes | 8922 | 0.7689 |
| 7 | all listed blocks | 4.0199 | 0.6732 | yes | 8922 | 0.7749 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `t_mbertab0_s0.csv` | 1,200,356 | `834d7ac4e95f86dc` | condition 0: none |
| `t_mbertab1_s0.csv` | 1,200,783 | `3d22d21565ebfa92` | condition 1: block 11 attention |
| `t_mbertab2_s0.csv` | 1,200,819 | `29c5ce3595f770b7` | condition 2: block 11 MLP |
| `t_mbertab3_s0.csv` | 1,201,316 | `cbdb30628f58921b` | condition 3: block 11 whole |
| `t_mbertab4_s0.csv` | 1,200,767 | `8460612d48cf92d0` | condition 4: block 12 attention |
| `t_mbertab5_s0.csv` | 1,201,013 | `d487fab52e9437e2` | condition 5: block 12 MLP |
| `t_mbertab6_s0.csv` | 1,201,535 | `6aa5f17241dbd51a` | condition 6: block 12 whole |
| `t_mbertab7_s0.csv` | 1,205,825 | `54e60c82ec1511c3` | condition 7: all listed blocks |
