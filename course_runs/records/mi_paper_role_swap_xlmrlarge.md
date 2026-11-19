# mi_paper_role_swap_xlmrlarge

_Paper experiments, stage role_swap, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:20 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 16.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "role_swap"}` |
| command | `scripts/mi_paper_edit.py --model xlmrlarge --max-rows 128 --stage role_swap` |


- **metric decision**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
Signs: M_<v> is the margin toward the version's correct form. For swap that is the form that agrees with the swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the verb follows the bare noun. The bare noun's slot is the version's obj_words, the ne-marked noun's slot its subj_words. Attention is read on the correct-form run of each version (for the first scored row of a span, which masks the whole span, the two forms are identical; later rows differ only in multi-subtoken spans).

- **check: unedited version (orig) against the metric stage's M_none and M_obj, orders / worst (bits)**: 2132 / 9.21e-04
- **check: embedding output patched everywhere recovers the clean margin, first five items of every version, worst (bits)**: 0.00e+00
- **orders read / entering (every version built) / skipped**: 2132 / 2132 / 0
- **timing (loop only): minutes in total / minutes per order (all versions)**: 15.96 / 0.0075

## Per order class and version


| class | version | orders | documents | mean M (bits) | M > 0 | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the bare noun's slot | to the ne-marked noun's slot | to ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 1142 | 233 | 7.475 | 0.9641 | 6.997 | 1141 | 0.733 [0.700, 0.763] | 0.5596 | 0.02209 | 0.04165 |
| SOV | swap | 1142 | 233 | -2.529 | 0.2776 | -0.255 | 1121 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.1991 | 0.2516 | 0.07355 |
| OSV | orig | 990 | 146 | 6.538 | 0.9444 | 6.256 | 989 | 0.706 [0.664, 0.750] | 0.4705 | 0.03693 | 0.06521 |
| OSV | swap | 990 | 146 | -4.022 | 0.1495 | 0.02796 | 956 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.042 | 0.3697 | 0.1164 |
| all | orig | 2132 | 235 | 7.04 | 0.955 | 6.653 | 2130 | 0.721 [0.685, 0.756] | 0.5182 | 0.02898 | 0.05259 |
| all | swap | 2132 | 235 | -3.223 | 0.2181 | -0.1236 | 2077 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.1262 | 0.3064 | 0.09346 |


## [all orders] Primary (behaviour): M_swap by order class (two-sided document sign-flip)


| class | orders | mean M_swap (bits) | document bootstrap 95% | two-sided document sign-flip p | descriptive: mean M_swap / mean M_orig |
|---|---|---|---|---|---|
| SOV | 1142 | -2.529 | [-3.363, -1.724] | 9.999e-05 | -0.3384 |
| OSV | 990 | -4.022 | [-4.878, -3.243] | 9.999e-05 | -0.6152 |

- **DECISION (behaviour, all orders; declared: follows case if M_swap > 0, p < 0.05 in both classes; plausibility if < 0 in both; position if > 0 in SOV and < 0 in OSV; else mixed)**: follows plausibility
- **orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents**: 1197 / 127

## [swap-correct form is not the default form] Primary (behaviour): M_swap by order class (two-sided document sign-flip)


| class | orders | mean M_swap (bits) | document bootstrap 95% | two-sided document sign-flip p | descriptive: mean M_swap / mean M_orig |
|---|---|---|---|---|---|
| SOV | 640 | -3.494 | [-4.729, -2.346] | 9.999e-05 | -0.4258 |
| OSV | 557 | -5.254 | [-6.486, -4.136] | 9.999e-05 | -0.7084 |

- **DECISION (behaviour, stratum where the swap-correct form is not the default form)**: follows plausibility
- **DECISION (P2 behaviour verdict; second addendum: the stratum's verdict if it differs from the overall one)**: follows plausibility (all orders: follows plausibility; stratum: follows plausibility)

## [all orders] Primary (component): the top 5 heads' attention, bare noun's slot minus ne-marked noun's slot, swap version


| class | orders | mean difference (bare minus ne-marked slot) | document bootstrap 95% | one-sided p (bare higher) | one-sided p (ne-marked higher) |
|---|---|---|---|---|---|
| SOV | 1142 | -0.05252 | [-0.099, -0.005] | 0.9868 | 0.0133 |
| OSV | 990 | -0.3277 | [-0.361, -0.295] | 1 | 9.999e-05 |

- **DECISION (heads; declared: follow the slot if attention is higher on the bare noun's slot in both classes, p < 0.05; follow position if higher on the bare noun's slot in SOV and on the ne-marked noun's slot in OSV, both p < 0.05; else do not follow the slot)**: do not follow the slot

## [swap-correct form is not the default form] Primary (component): the top 5 heads' attention, bare noun's slot minus ne-marked noun's slot, swap version


| class | orders | mean difference (bare minus ne-marked slot) | document bootstrap 95% | one-sided p (bare higher) | one-sided p (ne-marked higher) |
|---|---|---|---|---|---|
| SOV | 640 | -0.0626 | [-0.118, -0.006] | 0.9803 | 0.0198 |
| OSV | 557 | -0.3192 | [-0.357, -0.283] | 1 | 9.999e-05 |

- **descriptive: heads reading in the stratum where the swap-correct form is not the default form**: do not follow the slot

## Attention by head and version: bare noun's slot / ne-marked noun's slot (mean share of the verb's attention)


| head | orig: bare | orig: ne-marked | swap: bare | swap: ne-marked |
|---|---|---|---|---|
| L21H0 | 0.6096 | 0.02024 | 0.1036 | 0.4079 |
| L20H0 | 0.739 | 0.01947 | 0.0879 | 0.5268 |
| L20H2 | 0.5319 | 0.01914 | 0.1095 | 0.256 |
| L22H6 | 0.3015 | 0.0448 | 0.1324 | 0.1961 |
| L19H3 | 0.4091 | 0.04124 | 0.1973 | 0.1455 |


## The 10 heads' faithfulness, swap against orig (the orders above the gap floor in both versions)


| orders above the floor in both versions | mean gap on them: orig / swap (bits) | orig | swap | swap minus orig |
|---|---|---|---|---|
| 2075 | 6.679 / -0.129 | 0.720 [0.685, 0.755] | NOT ESTIMABLE (mean gap < 1.0 bit) | nan |

- **DECISION (faithfulness, first addendum: same if within 0.10 of orig on the same orders, lower if more than 0.10 below, higher if more than 0.10 above, not estimable if either version's mean gap on those orders is under 1.0 bit)**: not estimable

## Descriptive: M_swap by the swap-correct form being the default form, by class


| swap-correct form is the default | class | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|---|
| False | SOV | 640 | 125 | -3.494 | 0.2188 |
| False | OSV | 557 | 78 | -5.254 | 0.1041 |
| True | SOV | 502 | 120 | -1.3 | 0.3526 |
| True | OSV | 433 | 74 | -2.438 | 0.2079 |


## Descriptive: M_swap by whether the two phrases have equal length


| equal length | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|
| True | 418 | 50 | -2.431 | 0.2273 |
| False | 1714 | 198 | -3.416 | 0.2159 |


## Descriptive: M_swap by the number of words in the longer phrase


| words in the longer phrase | orders | documents | mean M_swap (bits) | M_swap > 0 |
|---|---|---|---|---|
| 1 | 300 | 23 | -2.609 | 0.1967 |
| 2 | 373 | 73 | -2.715 | 0.2976 |
| 3-4 | 502 | 62 | -2.462 | 0.2649 |
| 5-8 | 595 | 76 | -4.881 | 0.1109 |
| 9+ | 362 | 38 | -2.583 | 0.2652 |

Note: in SOV-type orders the swap yields a canonical order (ne-marked noun first, bare noun next to the verb) and in OSV-type orders a non-canonical one, so the class split separates canonical from non-canonical order as well as position.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `role_swap_xlmrlarge.csv` | 2,290,678 | `7e08ede8337d21e1` | per fresh order and version (orig, swap): margins, object-masked margins, the 10 heads' patch, attention to the bare noun's slot, the ne-marked noun's slot and ne |
