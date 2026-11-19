# rq1_agreement_order

_Whether the models' agreement survives the subject moving between object and verb._

| provenance | |
|---|---|
| run (UTC) | 2026-10-03 23:39 |
| script | `rq1_agreement_order.py` (sha256 `2c391d0c3174fe24`) |
| host | gnode (Linux) |
| duration | 0.0 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"batch_size": 32, "cap": 30, "model": null, "models": ["muril", "indicbert", "xlmrlarge", "mbert"], "out_dir": "<earlier-repo>/sets/set1/Results_Checks/agreement", "permutations": 10000, "seed": 707, "stage": "analyse", "tag": null}` |
| command | `scripts/rq1_agreement_order.py --stage analyse` |



## model: muril


| items | n | correct agreement preferred (A > 0) | mean A (bits) | mean object-verb gap (words) |
|---|---|---|---|---|
| all orders | 5265 | 0.9364 | 11.4979 | 7.7274 |
| attested order only | 459 | 0.9695 | 12.2583 | 0.7865 |
| OSV-type orders | 2525 | 0.9113 | 10.3918 | 12.0768 |
| SOV-type orders | 2740 | 0.9595 | 12.5173 | 3.7193 |
| object adjacent to the verb | 1403 | 0.9708 | 12.3491 | 0.0000 |
| object not adjacent | 3862 | 0.9239 | 11.1887 | 10.5347 |
| OSV-type, variants, object not adjacent | 2504 | 0.9109 | 10.3800 | 12.1090 |
| SOV-type, variants, object not adjacent | 1294 | 0.9459 | 12.7327 | 7.7303 |

- **OSV-type minus SOV-type mean A, gap-matched (primary): clauses / bits / document sign-flip p**: 102 / -1.7468 / 9.999e-05
- **OSV-type minus SOV-type mean A, unmatched, object not adjacent: clauses / bits / document sign-flip p**: 269 / -1.8332 / 9.999e-05

## model: indicbert


| items | n | correct agreement preferred (A > 0) | mean A (bits) | mean object-verb gap (words) |
|---|---|---|---|---|
| all orders | 5265 | 0.9628 | 10.9300 | 7.7274 |
| attested order only | 459 | 0.9739 | 11.7201 | 0.7865 |
| OSV-type orders | 2525 | 0.9450 | 9.8881 | 12.0768 |
| SOV-type orders | 2740 | 0.9792 | 11.8902 | 3.7193 |
| object adjacent to the verb | 1403 | 0.9800 | 12.2659 | 0.0000 |
| object not adjacent | 3862 | 0.9565 | 10.4447 | 10.5347 |
| OSV-type, variants, object not adjacent | 2504 | 0.9449 | 9.8860 | 12.1090 |
| SOV-type, variants, object not adjacent | 1294 | 0.9776 | 11.5825 | 7.7303 |

- **OSV-type minus SOV-type mean A, gap-matched (primary): clauses / bits / document sign-flip p**: 102 / -0.3775 / 0.191
- **OSV-type minus SOV-type mean A, unmatched, object not adjacent: clauses / bits / document sign-flip p**: 269 / -1.2487 / 9.999e-05

## model: xlmrlarge


| items | n | correct agreement preferred (A > 0) | mean A (bits) | mean object-verb gap (words) |
|---|---|---|---|---|
| all orders | 5265 | 0.9493 | 9.7858 | 7.7274 |
| attested order only | 459 | 0.9673 | 9.6893 | 0.7865 |
| OSV-type orders | 2525 | 0.9394 | 9.5216 | 12.0768 |
| SOV-type orders | 2740 | 0.9584 | 10.0293 | 3.7193 |
| object adjacent to the verb | 1403 | 0.9672 | 9.9750 | 0.0000 |
| object not adjacent | 3862 | 0.9428 | 9.7171 | 10.5347 |
| OSV-type, variants, object not adjacent | 2504 | 0.9389 | 9.5255 | 12.1090 |
| SOV-type, variants, object not adjacent | 1294 | 0.9474 | 10.0985 | 7.7303 |

- **OSV-type minus SOV-type mean A, gap-matched (primary): clauses / bits / document sign-flip p**: 102 / -0.2120 / 0.5796
- **OSV-type minus SOV-type mean A, unmatched, object not adjacent: clauses / bits / document sign-flip p**: 269 / -0.0667 / 0.7295

## model: mbert


| items | n | correct agreement preferred (A > 0) | mean A (bits) | mean object-verb gap (words) |
|---|---|---|---|---|
| all orders | 5265 | 0.6414 | 2.1326 | 7.7274 |
| attested order only | 459 | 0.7342 | 3.4677 | 0.7865 |
| OSV-type orders | 2525 | 0.5881 | 1.3084 | 12.0768 |
| SOV-type orders | 2740 | 0.6905 | 2.8921 | 3.7193 |
| object adjacent to the verb | 1403 | 0.7491 | 3.9206 | 0.0000 |
| object not adjacent | 3862 | 0.6023 | 1.4830 | 10.5347 |
| OSV-type, variants, object not adjacent | 2504 | 0.5879 | 1.2981 | 12.1090 |
| SOV-type, variants, object not adjacent | 1294 | 0.6291 | 1.8024 | 7.7303 |

- **OSV-type minus SOV-type mean A, gap-matched (primary): clauses / bits / document sign-flip p**: 102 / -0.1101 / 0.7219
- **OSV-type minus SOV-type mean A, unmatched, object not adjacent: clauses / bits / document sign-flip p**: 269 / -0.3836 / 0.0162

## Summary


| model | items | correct agreement preferred | clauses, gap-matched | OSV minus SOV, gap-matched | sign-flip p | clauses, unmatched | OSV minus SOV, unmatched | sign-flip p |
|---|---|---|---|---|---|---|---|---|
| muril | 5265 | 0.9364 | 102 | -1.747 | 9.999e-05 | 269 | -1.833 | 9.999e-05 |
| indicbert | 5265 | 0.9628 | 102 | -0.3775 | 0.191 | 269 | -1.249 | 9.999e-05 |
| xlmrlarge | 5265 | 0.9493 | 102 | -0.212 | 0.5796 | 269 | -0.06671 | 0.7295 |
| mbert | 5265 | 0.6414 | 102 | -0.1101 | 0.7219 | 269 | -0.3836 | 0.0162 |

The contrast uses only variant orders whose object is not adjacent to the verb complex, so on both sides something stands between object and verb: in OSV-type orders the ne-marked subject, in SOV-type orders another phrase. A nearest-noun heuristic predicts a negative difference; agreement that respects case predicts none.
