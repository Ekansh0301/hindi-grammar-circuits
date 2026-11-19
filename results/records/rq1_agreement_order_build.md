# rq1_agreement_order_build

_Agreement items: ergative clauses with a bare object, correct and subject-agreeing foil verbs._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 13:12 |
| script | `rq1_agreement_order.py` (sha256 `2c391d0c3174fe24`) |
| host | gnode (Linux) |
| duration | 0.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"batch_size": 32, "cap": 30, "model": null, "models": ["muril", "indicbert", "xlmrlarge", "mbert"], "out_dir": "<earlier-repo>/sets/set1/Results_Checks/agreement", "permutations": 10000, "seed": 707, "stage": "build", "tag": null}` |
| command | `scripts/rq1_agreement_order.py --stage build` |



| clauses | count |
|---|---|
| a. ergative clauses with a bare noun object (Training news) | 1064 |
| b. left out: the verb complex does not show the object's gender and number | 53 |
| c. left out: the subject's gender or number is not explicit | 91 |
| d. left out: subject and object agree in gender and number (no foil) | 333 |
| e. left out: no attested foil form for some agreeing word | 127 |
| f. left out: the foil forms equal the attested ones (syncretism) | 1 |
| g. items: clauses with a foil | 459 |


| items | count |
|---|---|
| orders (items) | 5265 |
| references | 457 |
| OSV-type orders / SOV-type orders | 2525 / 2740 |
| attested orders that are OSV-type | 21 |
| references with both classes | 322 |

example (SOV): अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखी ।  ||  foil: अलाउद्दीन खिलजी ने चित्‍तौड़ पर आक्रमण करने के बाद एक शर्त रखा ।

example (SOV): अलाउद्दीन खिलजी ने एक शर्त चित्‍तौड़ पर आक्रमण करने के बाद रखी ।  ||  foil: अलाउद्दीन खिलजी ने एक शर्त चित्‍तौड़ पर आक्रमण करने के बाद रखा ।

example (SOV): चित्‍तौड़ पर आक्रमण करने के बाद अलाउद्दीन खिलजी ने एक शर्त रखी ।  ||  foil: चित्‍तौड़ पर आक्रमण करने के बाद अलाउद्दीन खिलजी ने एक शर्त रखा ।


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `agreement_items.csv` | 3,863,167 | `350d0f0c29e0b639` | one row per order: correct and foil sentence, order class |
