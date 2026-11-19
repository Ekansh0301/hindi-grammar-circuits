# mi_paper_ko_muril

_Paper experiments, stage ko, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:38 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 5.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "ko"}` |
| command | `scripts/mi_paper_edit.py --model muril --max-rows 256 --stage ko` |


- **metric decision**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
Signs: M_<v> is the margin toward the version's own correct form (bits). Under ko the correct form is the DEFAULT form, so M_ko = D_ko, the margin toward the default form; Magree_<v> is the margin toward the object-agreeing form (equal to M_<v> except Magree_ko = -M_ko). Mobj_<v> is the object-masked margin with the sign of M_<v>. Attention is read on the sentence with the object-agreeing verb form in every version.

- **subtokens of को / भी in this model's tokenizer**: को: 1 (को) / भी: 1 (भी)
- **check: unedited version (none) against the metric stage's M_none and M_obj, orders / worst (bits)**: 956 / 1.78e-15
- **check: embedding output patched everywhere recovers the clean margin, first five items of every version, worst (bits)**: 0.00e+00
- **orders read / entering (every version built) / skipped**: 956 / 956 / 0
- **timing (loop only): minutes in total / minutes per order (all versions)**: 5.51 / 0.0058

## [all orders] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 956 | 0.9132 | 6.624 | 6.624 | -1.902 | 8.526 | 952 | 0.807 [0.775, 0.841] | 0.5303 |
| ko | 956 | 0.2531 | -3.245 | 3.245 | 4.794 | -1.549 | 943 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2183 |
| bhi | 956 | 0.9634 | 7.078 | 7.078 | -1.636 | 8.714 | 954 | 0.836 [0.807, 0.868] | 0.5195 |


## [all orders] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 643 | 5.775 | 8.179 | 639 | 0.821 [0.785, 0.862] | 0.4892 |
| ko | 643 | -3.179 | -1.376 | 634 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.1955 |
| bhi | 643 | 6.516 | 8.59 | 641 | 0.840 [0.809, 0.877] | 0.4985 |


## [all orders] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L10H6 | 0.6401 | 0.1491 | 0.6444 |
| L8H3 | 0.6203 | 0.1998 | 0.5702 |
| L11H1 | 0.4991 | 0.3357 | 0.5222 |
| L9H6 | 0.5117 | 0.1989 | 0.4982 |
| L11H2 | 0.3802 | 0.2077 | 0.3627 |

- **[all orders] clauses / distinct object head words / documents entering**: 130 / 87 / 118

## [all orders] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 7.078 | [6.353, 7.872] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 3.245 | [1.866, 4.595] | 9.999e-05 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 10.32 | [9.271, 11.443] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.4534 | - | nan |

- **[all orders] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.747 / 0.253
- **[all orders] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[all orders] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [all orders] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 3.245 | [1.866, 4.595] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 1.902 | [0.989, 2.898] |
| D_ko minus -Mobj_none (paired) | 1.343 | [-0.100, 2.693] |


## [all orders] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.3013 | [0.276, 0.325] | 9.999e-05 | 0.01076 | 0.530 / 0.520 / 0.218 |


## [all orders] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5195 | 0.06501 | 0.5845 |
| ko | 0.2183 | 0.2852 | 0.5034 |
| none | 0.5303 | - | - |

- **[all orders] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## [feminine singular object] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 728 | 0.9011 | 6.974 | 6.974 | -0.9587 | 7.933 | 724 | 0.812 [0.777, 0.850] | 0.5131 |
| ko | 728 | 0.2679 | -2.586 | 2.586 | 3.799 | -1.213 | 716 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2053 |
| bhi | 728 | 0.9602 | 7.47 | 7.47 | -0.9125 | 8.382 | 726 | 0.835 [0.803, 0.869] | 0.5106 |


## [feminine singular object] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 490 | 6.019 | 7.332 | 486 | 0.829 [0.792, 0.866] | 0.4656 |
| ko | 490 | -2.592 | -0.8828 | 482 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.1795 |
| bhi | 490 | 6.863 | 8.121 | 488 | 0.839 [0.806, 0.876] | 0.4864 |


## [feminine singular object] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L10H6 | 0.6017 | 0.1258 | 0.617 |
| L8H3 | 0.5996 | 0.1888 | 0.5584 |
| L11H1 | 0.4785 | 0.3216 | 0.5098 |
| L9H6 | 0.5092 | 0.1896 | 0.5041 |
| L11H2 | 0.3767 | 0.2009 | 0.3635 |

- **[feminine singular object] clauses / distinct object head words / documents entering**: 95 / 58 / 85

## [feminine singular object] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 7.47 | [6.615, 8.334] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 2.586 | [1.181, 3.978] | 0.0003 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 10.06 | [9.066, 11.172] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.4958 | - | nan |

- **[feminine singular object] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.732 / 0.268
- **[feminine singular object] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[feminine singular object] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [feminine singular object] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 2.586 | [1.181, 3.978] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 0.9587 | [0.144, 1.822] |
| D_ko minus -Mobj_none (paired) | 1.628 | [0.251, 2.977] |


## [feminine singular object] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.3052 | [0.280, 0.330] | 9.999e-05 | 0.00257 | 0.513 / 0.511 / 0.205 |


## [feminine singular object] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5106 | 0.06674 | 0.5773 |
| ko | 0.2053 | 0.2887 | 0.4941 |
| none | 0.5131 | - | - |

- **[feminine singular object] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## [plural object] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 228 | 0.9518 | 5.508 | 5.508 | -4.915 | 10.42 | 228 | 0.796 [0.734, 0.880] | 0.585 |
| ko | 228 | 0.2061 | -5.348 | 5.348 | 7.97 | -2.622 | 227 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2595 |
| bhi | 228 | 0.9737 | 5.826 | 5.826 | -3.946 | 9.772 | 228 | 0.839 [0.779, 0.914] | 0.5481 |


## [plural object] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 153 | 4.994 | 10.89 | 153 | 0.803 [0.736, 0.886] | 0.5648 |
| ko | 153 | -5.057 | -2.956 | 152 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2465 |
| bhi | 153 | 5.405 | 10.09 | 153 | 0.843 [0.777, 0.919] | 0.5371 |


## [plural object] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L10H6 | 0.7627 | 0.2232 | 0.7317 |
| L8H3 | 0.6863 | 0.2349 | 0.6077 |
| L11H1 | 0.5651 | 0.381 | 0.5614 |
| L9H6 | 0.5197 | 0.2287 | 0.4795 |
| L11H2 | 0.3914 | 0.2296 | 0.3603 |

- **[plural object] clauses / distinct object head words / documents entering**: 35 / 29 / 35

## [plural object] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 5.826 | [5.049, 6.539] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 5.348 | [2.251, 8.633] | 0.0018 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 11.17 | [8.389, 14.506] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.318 | - | nan |

- **[plural object] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.794 / 0.206
- **[plural object] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[plural object] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [plural object] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 5.348 | [2.251, 8.633] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 4.915 | [3.154, 6.548] |
| D_ko minus -Mobj_none (paired) | 0.4328 | [-3.840, 4.251] |


## [plural object] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.2886 | [0.227, 0.344] | 9.999e-05 | 0.03693 | 0.585 / 0.548 / 0.259 |


## [plural object] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5481 | 0.0595 | 0.6076 |
| ko | 0.2595 | 0.2739 | 0.5334 |
| none | 0.585 | - | - |

- **[plural object] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## P1 verdict

- **behaviour reading: all orders / feminine singular stratum / plural stratum**: respected / respected / respected
- **head-gating reading: all orders / feminine singular stratum / plural stratum**: gate on the marker / gate on the marker / gate on the marker
- **DECISION (P1 verdict; second addendum: the reading over all orders, replaced by the feminine singular stratum's if the readings differ)**: behaviour: respected; head gating: gate on the marker; taken from the reading over all orders (the readings agree)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `ko_muril.csv` | 792,594 | `80f3996a5b081495` | per fresh order and version (none, ko, bhi): margins (toward the version's correct form and toward the object-agreeing form), object-masked margins, the 10 heads' patch, attention to the object and to the inserted word |
