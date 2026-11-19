# mi_paper_role_swap_muril

_Paper experiments, stage role_swap, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:47 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 8.4 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "role_swap"}` |
| command | `scripts/mi_paper_edit.py --model muril --max-rows 256 --stage role_swap` |


- **metric decision**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
Signs: M_<v> is the margin toward the version's correct form. For swap that is the form that agrees with the swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the verb follows the bare noun. The bare noun's slot is the version's obj_words, the ne-marked noun's slot its subj_words. Attention is read on the correct-form run of each version (for the first scored row of a span, which masks the whole span, the two forms are identical; later rows differ only in multi-subtoken spans).

- **check: unedited version (orig) against the metric stage's M_none and M_obj, orders / worst (bits)**: 2132 / 3.55e-15
- **check: embedding output patched everywhere recovers the clean margin, first five items of every version, worst (bits)**: 0.00e+00
- **orders read / entering (every version built) / skipped**: 2132 / 2132 / 0
- **timing (loop only): minutes in total / minutes per order (all versions)**: 8.29 / 0.0039

## Per order class and version


| class | version | orders | documents | mean M (bits) | M > 0 | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the bare noun's slot | to the ne-marked noun's slot | to ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 1142 | 233 | 8.69 | 0.9694 | 7.884 | 1140 | 0.819 [0.793, 0.848] | 0.5616 | 0.01824 | 0.04288 |
| SOV | swap | 1142 | 233 | -0.7983 | 0.4597 | 1.216 | 1123 | 0.868 [0.646, 1.167] | 0.283 | 0.1329 | 0.08499 |
| OSV | orig | 990 | 146 | 6.787 | 0.9081 | 6.012 | 979 | 0.845 [0.807, 0.886] | 0.4338 | 0.03366 | 0.06389 |
| OSV | swap | 990 | 146 | -2.987 | 0.2828 | 0.6189 | 946 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.07554 | 0.2569 | 0.1445 |
| all | orig | 2132 | 235 | 7.807 | 0.9409 | 7.014 | 2119 | 0.829 [0.799, 0.863] | 0.5023 | 0.0254 | 0.05263 |
| all | swap | 2132 | 235 | -1.814 | 0.3776 | 0.939 | 2069 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.1867 | 0.1905 | 0.1126 |


## [all orders] Primary (behaviour): M_swap by order class (two-sided document sign-flip)


| class | orders | mean M_swap (bits) | document bootstrap 95% | two-sided document sign-flip p | descriptive: mean M_swap / mean M_orig |
|---|---|---|---|---|---|
| SOV | 1142 | -0.7983 | [-1.668, -0.022] | 0.06559 | -0.09186 |
| OSV | 990 | -2.987 | [-3.861, -2.161] | 9.999e-05 | -0.44 |

- **DECISION (behaviour, all orders; declared: follows case if M_swap > 0, p < 0.05 in both classes; plausibility if < 0 in both; position if > 0 in SOV and < 0 in OSV; else mixed)**: mixed
- **orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents**: 1197 / 127

## [swap-correct form is not the default form] Primary (behaviour): M_swap by order class (two-sided document sign-flip)


| class | orders | mean M_swap (bits) | document bootstrap 95% | two-sided document sign-flip p | descriptive: mean M_swap / mean M_orig |
|---|---|---|---|---|---|
| SOV | 640 | -1.979 | [-3.086, -0.829] | 0.0012 | -0.21 |
| OSV | 557 | -4.789 | [-5.835, -3.816] | 9.999e-05 | -0.614 |

- **DECISION (behaviour, stratum where the swap-correct form is not the default form)**: follows plausibility
- **DECISION (P2 behaviour verdict; second addendum: the stratum's verdict if it differs from the overall one)**: follows plausibility (all orders: mixed; stratum: follows plausibility)

## [all orders] Primary (component): the top 5 heads' attention, bare noun's slot minus ne-marked noun's slot, swap version


| class | orders | mean difference (bare minus ne-marked slot) | document bootstrap 95% | one-sided p (bare higher) | one-sided p (ne-marked higher) |
|---|---|---|---|---|---|
| SOV | 1142 | 0.1501 | [0.109, 0.191] | 9.999e-05 | 1 |
| OSV | 990 | -0.1814 | [-0.220, -0.145] | 1 | 9.999e-05 |

- **DECISION (heads; declared: follow the slot if attention is higher on the bare noun's slot in both classes, p < 0.05; follow position if higher on the bare noun's slot in SOV and on the ne-marked noun's slot in OSV, both p < 0.05; else do not follow the slot)**: follow position

## [swap-correct form is not the default form] Primary (component): the top 5 heads' attention, bare noun's slot minus ne-marked noun's slot, swap version


| class | orders | mean difference (bare minus ne-marked slot) | document bootstrap 95% | one-sided p (bare higher) | one-sided p (ne-marked higher) |
|---|---|---|---|---|---|
| SOV | 640 | 0.1629 | [0.116, 0.212] | 9.999e-05 | 1 |
| OSV | 557 | -0.1703 | [-0.212, -0.132] | 1 | 9.999e-05 |

- **descriptive: heads reading in the stratum where the swap-correct form is not the default form**: follow position

## Attention by head and version: bare noun's slot / ne-marked noun's slot (mean share of the verb's attention)


| head | orig: bare | orig: ne-marked | swap: bare | swap: ne-marked |
|---|---|---|---|---|
| L10H6 | 0.6185 | 0.01381 | 0.2506 | 0.1754 |
| L8H3 | 0.6091 | 0.03611 | 0.2349 | 0.2291 |
| L11H1 | 0.4845 | 0.03153 | 0.1332 | 0.2675 |
| L9H6 | 0.45 | 0.01582 | 0.1712 | 0.1316 |
| L11H2 | 0.3492 | 0.02973 | 0.1434 | 0.1488 |


## The 10 heads' faithfulness, swap against orig (the orders above the gap floor in both versions)


| orders above the floor in both versions | mean gap on them: orig / swap (bits) | orig | swap | swap minus orig |
|---|---|---|---|---|
| 2057 | 7.091 / 0.968 | 0.830 [0.799, 0.863] | NOT ESTIMABLE (mean gap < 1.0 bit) | nan |

- **DECISION (faithfulness, first addendum: same if within 0.10 of orig on the same orders, lower if more than 0.10 below, higher if more than 0.10 above, not estimable if either version's mean gap on those orders is under 1.0 bit)**: not estimable

## Descriptive: M_swap by the swap-correct form being the default form, by class


| swap-correct form is the default | class | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|---|
| False | SOV | 640 | 125 | -1.979 | 0.3359 |
| False | OSV | 557 | 78 | -4.789 | 0.1149 |
| True | SOV | 502 | 120 | 0.7068 | 0.6175 |
| True | OSV | 433 | 74 | -0.668 | 0.4988 |


## Descriptive: M_swap by whether the two phrases have equal length


| equal length | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|
| True | 418 | 50 | -1.31 | 0.3636 |
| False | 1714 | 198 | -1.938 | 0.381 |


## Descriptive: M_swap by the number of words in the longer phrase


| words in the longer phrase | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|
| 1 | 300 | 23 | -1.624 | 0.3267 |
| 2 | 373 | 73 | -1.531 | 0.4397 |
| 3-4 | 502 | 62 | -1.545 | 0.3625 |
| 5-8 | 595 | 76 | -2.962 | 0.3126 |
| 9+ | 362 | 38 | -0.7518 | 0.4834 |

Note: in SOV-type orders the swap yields a canonical order (ne-marked noun first, bare noun next to the verb) and in OSV-type orders a non-canonical one, so the class split separates canonical from non-canonical order as well as position.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `role_swap_muril.csv` | 2,288,924 | `de208aba3f25316c` | per fresh order and version (orig, swap): margins, object-masked margins, the 10 heads' patch, attention to the bare noun's slot, the ne-marked noun's slot and ne |
