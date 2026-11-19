# mi_paper_ko_xlmrlarge

_Paper experiments, stage ko, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 13:04 |
| script | `mi_paper_edit.py` (sha256 `a1083eaba9430171`) |
| host | gnode (Linux) |
| duration | 10.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "ko"}` |
| command | `scripts/mi_paper_edit.py --model xlmrlarge --max-rows 128 --stage ko` |


- **metric decision**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
Signs: M_<v> is the margin toward the version's own correct form (bits). Under ko the correct form is the DEFAULT form, so M_ko = D_ko, the margin toward the default form; Magree_<v> is the margin toward the object-agreeing form (equal to M_<v> except Magree_ko = -M_ko). Mobj_<v> is the object-masked margin with the sign of M_<v>. Attention is read on the sentence with the object-agreeing verb form in every version.

- **subtokens of को / भी in this model's tokenizer**: को: 1 (▁को) / भी: 1 (▁भी)
- **check: unedited version (none) against the metric stage's M_none and M_obj, orders / worst (bits)**: 956 / 4.38e-04
- **check: embedding output patched everywhere recovers the clean margin, first five items of every version, worst (bits)**: 0.00e+00
- **orders read / entering (every version built) / skipped**: 956 / 956 / 0
- **timing (loop only): minutes in total / minutes per order (all versions)**: 10.02 / 0.0105

## [all orders] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 956 | 0.9603 | 5.876 | 5.876 | -2.06 | 7.936 | 956 | 0.705 [0.654, 0.756] | 0.5447 |
| ko | 956 | 0.319 | -2.487 | 2.487 | 4.365 | -1.878 | 950 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2259 |
| bhi | 956 | 0.9728 | 6.039 | 6.039 | -1.827 | 7.866 | 955 | 0.755 [0.715, 0.796] | 0.5137 |


## [all orders] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 643 | 5.291 | 7.714 | 643 | 0.687 [0.630, 0.744] | 0.5093 |
| ko | 643 | -2.236 | -1.757 | 639 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2214 |
| bhi | 643 | 5.632 | 7.802 | 642 | 0.746 [0.699, 0.793] | 0.4905 |


## [all orders] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L21H0 | 0.6447 | 0.3516 | 0.6073 |
| L20H0 | 0.75 | 0.2562 | 0.756 |
| L20H2 | 0.5608 | 0.1545 | 0.4921 |
| L22H6 | 0.3314 | 0.2014 | 0.2867 |
| L19H3 | 0.4364 | 0.166 | 0.4264 |

- **[all orders] clauses / distinct object head words / documents entering**: 130 / 87 / 118

## [all orders] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 6.039 | [5.355, 6.737] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 2.487 | [1.218, 3.666] | 9.999e-05 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 8.526 | [7.527, 9.555] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.1626 | - | nan |

- **[all orders] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.681 / 0.319
- **[all orders] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[all orders] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [all orders] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 2.487 | [1.218, 3.666] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 2.06 | [1.269, 2.873] |
| D_ko minus -Mobj_none (paired) | 0.4271 | [-0.869, 1.730] |


## [all orders] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.2878 | [0.258, 0.317] | 9.999e-05 | 0.03095 | 0.545 / 0.514 / 0.226 |


## [all orders] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5137 | 0.07853 | 0.5922 |
| ko | 0.2259 | 0.3191 | 0.545 |
| none | 0.5447 | - | - |

- **[all orders] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## [feminine singular object] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 728 | 0.9698 | 6.536 | 6.536 | -1.297 | 7.833 | 728 | 0.702 [0.648, 0.756] | 0.536 |
| ko | 728 | 0.342 | -2.139 | 2.139 | 3.652 | -1.513 | 723 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2128 |
| bhi | 728 | 0.9876 | 6.708 | 6.708 | -1.275 | 7.983 | 728 | 0.745 [0.698, 0.793] | 0.5093 |


## [feminine singular object] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 490 | 5.955 | 7.616 | 490 | 0.680 [0.620, 0.741] | 0.4952 |
| ko | 490 | -1.862 | -1.372 | 487 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2077 |
| bhi | 490 | 6.306 | 7.917 | 490 | 0.734 [0.681, 0.788] | 0.4834 |


## [feminine singular object] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L21H0 | 0.6353 | 0.3399 | 0.5966 |
| L20H0 | 0.7646 | 0.251 | 0.7788 |
| L20H2 | 0.5527 | 0.1414 | 0.4849 |
| L22H6 | 0.3083 | 0.1844 | 0.2715 |
| L19H3 | 0.4194 | 0.1473 | 0.4144 |

- **[feminine singular object] clauses / distinct object head words / documents entering**: 95 / 58 / 85

## [feminine singular object] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 6.708 | [5.977, 7.397] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 2.139 | [0.738, 3.550] | 0.0022 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 8.847 | [7.823, 9.932] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.1715 | - | nan |

- **[feminine singular object] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.658 / 0.342
- **[feminine singular object] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[feminine singular object] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [feminine singular object] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 2.139 | [0.738, 3.550] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 1.297 | [0.547, 2.080] |
| D_ko minus -Mobj_none (paired) | 0.8423 | [-0.562, 2.242] |


## [feminine singular object] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.2964 | [0.266, 0.328] | 9.999e-05 | 0.02679 | 0.536 / 0.509 / 0.213 |


## [feminine singular object] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5093 | 0.08374 | 0.593 |
| ko | 0.2128 | 0.3239 | 0.5367 |
| none | 0.536 | - | - |

- **[feminine singular object] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## [plural object] Per version


| version | orders | object-agreeing form preferred (Magree > 0) | mean Magree (bits) | mean M, toward the version's correct form | mean Mobj (same sign) | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|---|---|---|
| none | 228 | 0.9298 | 3.769 | 3.769 | -4.498 | 8.266 | 228 | 0.715 [0.588, 0.844] | 0.5721 |
| ko | 228 | 0.2456 | -3.599 | 3.599 | 6.643 | -3.044 | 227 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2678 |
| bhi | 228 | 0.9254 | 3.903 | 3.903 | -3.59 | 7.493 | 227 | 0.789 [0.704, 0.870] | 0.5279 |


## [plural object] Per version, variant orders with the object not adjacent only (the population the circuit was found on)


| version | orders | mean Magree (bits) | mean gap (bits) | orders above the gap floor | 10 heads: share | top 5 heads: attention to the object |
|---|---|---|---|---|---|---|
| none | 153 | 3.162 | 8.028 | 153 | 0.708 [0.559, 0.855] | 0.5546 |
| ko | 153 | -3.434 | -2.991 | 152 | NOT ESTIMABLE (mean gap < 1.0 bit) | 0.2654 |
| bhi | 153 | 3.472 | 7.434 | 152 | 0.788 [0.704, 0.865] | 0.5131 |


## [plural object] Attention to the object by head and version (mean share of the verb's attention)


| head | none | ko | bhi |
|---|---|---|---|
| L21H0 | 0.6747 | 0.3888 | 0.6415 |
| L20H0 | 0.7037 | 0.2727 | 0.6829 |
| L20H2 | 0.5868 | 0.1963 | 0.5151 |
| L22H6 | 0.4052 | 0.2557 | 0.3353 |
| L19H3 | 0.4905 | 0.2254 | 0.4648 |

- **[plural object] clauses / distinct object head words / documents entering**: 35 / 29 / 35

## [plural object] Primary (behaviour): control, then the rule


| quantity | mean (bits) | document bootstrap 95% | one-sided document sign-flip p |
|---|---|---|---|
| control: M_bhi (object-agreeing form under bhi) | 3.903 | [2.743, 5.004] | 9.999e-05 |
| D_ko = M_ko (default form under ko) | 3.599 | [1.600, 5.971] | 0.0005 |
| M_bhi - Magree_ko (fall of the object-agreeing preference under ko against bhi) | 7.502 | [5.510, 9.863] | 9.999e-05 |
| descriptive: M_bhi - M_none | 0.1343 | - | nan |

- **[plural object] share of orders preferring the default form under ko (D_ko > 0) / the object-agreeing form under ko (Magree_ko > 0)**: 0.754 / 0.246
- **[plural object] DECISION (control, declared: mean M_bhi > 0 with one-sided p < 0.05, else UNINTERPRETABLE)**: control holds
- **[plural object] DECISION (behaviour, declared: respected if mean D_ko > 0, p < 0.05; partly respected if the object-agreeing preference falls more under ko than under bhi, p < 0.05; else not respected)**: respected

## [plural object] Descriptive: D_ko beside the object-masked margin toward the default form (-Mobj_none), paired per order


| quantity | mean (bits) | document bootstrap 95% |
|---|---|---|
| D_ko (margin toward the default form, object present, ko inserted) | 3.599 | [1.600, 5.971] |
| -Mobj_none (margin toward the default form, object masked, no insertion) | 4.498 | [3.128, 5.741] |
| D_ko minus -Mobj_none (paired) | -0.8985 | [-3.710, 2.065] |


## [plural object] Primary (component): the top 5 heads' attention to the object


| bhi minus ko (fall under ko) | document bootstrap 95% | one-sided document sign-flip p | none minus bhi (fall under bhi) | mean attention: none / bhi / ko |
|---|---|---|---|---|
| 0.2602 | [0.195, 0.329] | 9.999e-05 | 0.04421 | 0.572 / 0.528 / 0.268 |


## [plural object] Descriptive: the top 5 heads' attention on the inserted word beside their attention on the object


| version | attention on the object | attention on the inserted word | object + inserted word |
|---|---|---|---|
| bhi | 0.5279 | 0.0619 | 0.5898 |
| ko | 0.2678 | 0.3036 | 0.5714 |
| none | 0.5721 | - | - |

- **[plural object] DECISION (head gating, declared: gate on the marker if p < 0.05 and the fall under ko exceeds the fall under bhi; read only if the behavioural control holds). LIMIT: this cannot separate 'ko makes the noun an ineligible controller' from 'ko changes the noun's syntactic role in the model's eyes'**: gate on the marker

## P1 verdict

- **behaviour reading: all orders / feminine singular stratum / plural stratum**: respected / respected / respected
- **head-gating reading: all orders / feminine singular stratum / plural stratum**: gate on the marker / gate on the marker / gate on the marker
- **DECISION (P1 verdict; second addendum: the reading over all orders, replaced by the feminine singular stratum's if the readings differ)**: behaviour: respected; head gating: gate on the marker; taken from the reading over all orders (the readings agree)

## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `ko_xlmrlarge.csv` | 792,570 | `cf6d9d1dd4eb966f` | per fresh order and version (none, ko, bhi): margins (toward the version's correct form and toward the object-agreeing form), object-masked margins, the 10 heads' patch, attention to the object and to the inserted word |
