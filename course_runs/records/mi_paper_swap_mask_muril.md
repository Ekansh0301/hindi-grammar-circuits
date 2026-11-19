# mi_paper_swap_mask_muril

_Paper experiment P7, stage swap_mask, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 16:27 |
| script | `mi_paper_mask.py` (sha256 `583473353c39433e`) |
| host | gnode (Linux) |
| duration | 9.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "record_tag": null, "stage": "swap_mask"}` |
| command | `scripts/mi_paper_mask.py --model muril --max-rows 256 --stage swap_mask` |


- **metric decision**: REJECTED by the declared rule, used under the author's recorded override: Author decision, 23 Oct 2026: use the span margin for the object task although the declared rule REJECTED it. It passed every validity check (single-word spans against score_words, 200 orders, 1.2e-4 bits; multi-word spans against an independent full-logits computation, 50 orders, 1.1e-4 bits; Spearman with the baseline margin 0.545; correct form preferred in 93.8% of orders) and failed only the rule that it reproduce the baseline intervening-subject contrast. mi_decompose_muril.md shows that contrast is not at the verb (agreeing words -0.23 bits, p 0.15) but in the scores of other words (-1.81 bits, p 1e-4), so the rule tested the wrong place. The contrast (attraction) task is dropped.
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L10H6, L8H3, L11H1, L9H6, L11H2, L9H3, L10H3, L10H10, L9H8, L11H10
Signs: M_<version>_<cond> is the span margin toward the version's own correct form (bits). For swap that is the form that agrees with the swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the verb follows the bare noun. Conditions: none; obj (the bare noun's slot masked, the version's obj_words); subj (the ne-marked noun's slot masked, its subj_words, without ne); ne (the marker masked).

- **check: unedited version (orig, none and obj) against the metric stage's M_none and M_obj, orders / worst (bits)**: 2132 / 3.55e-15
- **check: orig and swap(none) against P2's role_swap file, orders in common / worst (bits)**: 2132 / 3.55e-15
- **check: embedding output patched everywhere recovers the clean margin (swap, none), first five orders, worst (bits)**: 0.00e+00
- **check: orders whose two versions hold different words apart from the agreeing words (must be 0)**: 0
- **orders read / entering (all eight runs built) / skipped**: 2132 / 2132 / 0
- **timing (loop only): minutes in total / minutes per order (all eight conditions and the patch)**: 9.06 / 0.0042
- **orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents**: 1197 / 127

## [all orders] Mean margin M (bits) and share of orders with M > 0, by class, version and condition


| class | version | orders | documents | M none | M obj | M subj | M ne | M>0 none | M>0 obj | M>0 subj | M>0 ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 1142 | 233 | 8.69 | 0.8067 | 8.279 | 7.834 | 0.9694 | 0.5989 | 0.9597 | 0.9606 |
| SOV | swap | 1142 | 233 | -0.7983 | -2.015 | 1.242 | -0.3856 | 0.4597 | 0.3433 | 0.6121 | 0.5 |
| OSV | orig | 990 | 146 | 6.787 | 0.7756 | 5.441 | 5.368 | 0.9081 | 0.5909 | 0.8434 | 0.8768 |
| OSV | swap | 990 | 146 | -2.987 | -3.606 | -0.484 | -1.323 | 0.2828 | 0.2586 | 0.4343 | 0.4394 |
| all | orig | 2132 | 235 | 7.807 | 0.7923 | 6.961 | 6.689 | 0.9409 | 0.5952 | 0.9057 | 0.9217 |
| all | swap | 2132 | 235 | -1.814 | -2.753 | 0.4403 | -0.8207 | 0.3776 | 0.3039 | 0.5295 | 0.4719 |


## [swap-correct form is not the default form] Mean margin M (bits) and share of orders with M > 0, by class, version and condition


| class | version | orders | documents | M none | M obj | M subj | M ne | M>0 none | M>0 obj | M>0 subj | M>0 ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 640 | 125 | 9.423 | 2.504 | 9.26 | 8.522 | 0.9719 | 0.8016 | 0.9578 | 0.9625 |
| SOV | swap | 640 | 125 | -1.979 | -3.942 | -0.2573 | -0.9804 | 0.3359 | 0.1578 | 0.4531 | 0.4562 |
| OSV | orig | 557 | 78 | 7.8 | 3.357 | 7.074 | 6.152 | 0.9533 | 0.8492 | 0.9192 | 0.9013 |
| OSV | swap | 557 | 78 | -4.789 | -5.885 | -3.02 | -2.082 | 0.1149 | 0.08977 | 0.1562 | 0.4147 |
| all | orig | 1197 | 127 | 8.668 | 2.901 | 8.243 | 7.419 | 0.9632 | 0.8237 | 0.9398 | 0.934 |
| all | swap | 1197 | 127 | -3.287 | -4.846 | -1.543 | -1.493 | 0.2331 | 0.1261 | 0.315 | 0.4369 |


## [all orders] Primary: R = M_swap(subj) - M_swap(none), paired per order (one-sided document sign-flip, upward)


| class | orders | mean M_swap(none) (bits) | mean R (bits) | document bootstrap 95% | one-sided p (R > 0) | mean M_swap(subj) (bits) |
|---|---|---|---|---|---|---|
| SOV | 1142 | -0.7983 | 2.04 | [1.554, 2.566] | 9.999e-05 | 1.242 |
| OSV | 990 | -2.987 | 2.503 | [1.880, 3.226] | 9.999e-05 | -0.484 |


## [all orders] Bare noun's slot: M_swap(obj) - M_swap(none), paired per order (one-sided document sign-flip, downward)


| class | orders | mean change (bits) | document bootstrap 95% | one-sided p (fall) |
|---|---|---|---|---|
| SOV | 1142 | -1.216 | [-1.725, -0.738] | 9.999e-05 |
| OSV | 990 | -0.6189 | [-1.283, -0.099] | 0.0124 |

- **[all orders] flags per class: R >= 1.0 bit with p < 0.05 / mean M_swap(subj) > 0 / bare-noun fall >= 1.0 bit with p < 0.05**: SOV: True / True / True; OSV: True / False / False
- **DECISION (the ne-marked noun's slot, all orders; declared: the verb reads the ne-marked noun if R >= 1.0 bit with p < 0.05 and mean M_swap(subj) > 0 in both classes; partly if R >= 1.0 bit with p < 0.05 but mean M_swap(subj) <= 0 in a class; else not)**: partly
- **DECISION (the bare noun's slot, all orders; declared: a fall of at least 1.0 bit with one-sided p < 0.05 means the verb also reads the bare noun)**: does not (in both classes) also read the bare noun

## [swap-correct form is not the default form] Primary: R = M_swap(subj) - M_swap(none), paired per order (one-sided document sign-flip, upward)


| class | orders | mean M_swap(none) (bits) | mean R (bits) | document bootstrap 95% | one-sided p (R > 0) | mean M_swap(subj) (bits) |
|---|---|---|---|---|---|---|
| SOV | 640 | -1.979 | 1.722 | [1.278, 2.232] | 9.999e-05 | -0.2573 |
| OSV | 557 | -4.789 | 1.769 | [1.240, 2.378] | 9.999e-05 | -3.02 |


## [swap-correct form is not the default form] Bare noun's slot: M_swap(obj) - M_swap(none), paired per order (one-sided document sign-flip, downward)


| class | orders | mean change (bits) | document bootstrap 95% | one-sided p (fall) |
|---|---|---|---|---|
| SOV | 640 | -1.963 | [-2.659, -1.306] | 9.999e-05 |
| OSV | 557 | -1.096 | [-2.211, -0.277] | 0.002 |

- **[swap-correct form is not the default form] flags per class: R >= 1.0 bit with p < 0.05 / mean M_swap(subj) > 0 / bare-noun fall >= 1.0 bit with p < 0.05**: SOV: True / False / True; OSV: True / False / True
- **DECISION (the ne-marked noun's slot, stratum where the swap-correct form is not the default form)**: partly
- **DECISION (the bare noun's slot, stratum where the swap-correct form is not the default form)**: also reads the bare noun
- **DECISION (P7 verdict on the ne-marked noun's slot; P2 rule: the stratum's verdict if it differs from the overall one)**: partly (all orders: partly; stratum: partly)
- **DECISION (P7 reading of the bare noun's slot, same rule)**: also reads the bare noun (all orders: does not (in both classes) also read the bare noun; stratum: also reads the bare noun)

## Change of the margin under each mask (M_<cond> minus M_none, paired per order), all orders, both versions (orig is the unswapped reference; ne is reported and not graded); mean and document bootstrap 95% (descriptive)


| class | version | orders | obj | subj | ne |
|---|---|---|---|---|---|
| SOV | orig | 1142 | -7.884 [-8.484, -7.290] | -0.411 [-0.880, 0.206] | -0.856 [-1.111, -0.632] |
| SOV | swap | 1142 | -1.216 [-1.725, -0.738] | 2.040 [1.554, 2.566] | 0.413 [-0.025, 0.879] |
| OSV | orig | 990 | -6.012 [-6.901, -5.162] | -1.346 [-1.971, -0.663] | -1.420 [-1.759, -1.103] |
| OSV | swap | 990 | -0.619 [-1.283, -0.099] | 2.503 [1.880, 3.226] | 1.664 [1.116, 2.214] |
| all | orig | 2132 | -7.014 [-7.736, -6.354] | -0.845 [-1.342, -0.211] | -1.118 [-1.379, -0.882] |
| all | swap | 2132 | -0.939 [-1.472, -0.506] | 2.255 [1.726, 2.830] | 0.994 [0.541, 1.417] |


## Masking ne on swap, two-sided document sign-flip (reported, not graded)


| class | orders | mean M_swap(ne) - M_swap(none) (bits) | two-sided p |
|---|---|---|---|
| SOV | 1142 | 0.4127 | 0.08229 |
| OSV | 990 | 1.664 | 9.999e-05 |


## Descriptive: share of orders whose preference changes sign under each mask / share that goes from M <= 0 (none) to M > 0 (masked)


| stratum | class | version | orders | obj | subj | ne |
|---|---|---|---|---|---|---|
| all orders | SOV | orig | 1142 | 0.372 / 0.001 | 0.013 / 0.002 | 0.018 / 0.004 |
| all orders | SOV | swap | 1142 | 0.206 / 0.045 | 0.194 / 0.173 | 0.177 / 0.109 |
| all orders | OSV | orig | 990 | 0.321 / 0.002 | 0.097 / 0.016 | 0.088 / 0.028 |
| all orders | OSV | swap | 990 | 0.095 / 0.035 | 0.208 / 0.180 | 0.304 / 0.230 |
| all orders | all | orig | 2132 | 0.348 / 0.001 | 0.052 / 0.008 | 0.050 / 0.015 |
| all orders | all | swap | 2132 | 0.154 / 0.040 | 0.201 / 0.176 | 0.236 / 0.165 |
| swap-correct form is not the default form | SOV | orig | 640 | 0.173 / 0.002 | 0.017 / 0.002 | 0.022 / 0.006 |
| swap-correct form is not the default form | SOV | swap | 640 | 0.231 / 0.027 | 0.155 / 0.136 | 0.183 / 0.152 |
| swap-correct form is not the default form | OSV | orig | 557 | 0.111 / 0.004 | 0.052 / 0.009 | 0.056 / 0.002 |
| swap-correct form is not the default form | OSV | swap | 557 | 0.054 / 0.014 | 0.084 / 0.063 | 0.314 / 0.307 |
| swap-correct form is not the default form | all | orig | 1197 | 0.145 / 0.003 | 0.033 / 0.005 | 0.038 / 0.004 |
| swap-correct form is not the default form | all | swap | 1197 | 0.149 / 0.021 | 0.122 / 0.102 | 0.244 / 0.224 |


## Descriptive: the 10 frozen heads' faithfulness for the subj corruption on swap (clean none, corrupted subj); the gap is M_swap(none) - M_swap(subj), so it is negative where masking the ne-marked noun raises the margin


| class | orders | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored |
|---|---|---|---|---|
| SOV | 1142 | -2.04 | 1115 | NOT ESTIMABLE (mean gap < 1.0 bit) |
| OSV | 990 | -2.503 | 970 | NOT ESTIMABLE (mean gap < 1.0 bit) |
| all | 2132 | -2.255 | 2085 | NOT ESTIMABLE (mean gap < 1.0 bit) |

- **DECISION (descriptive: the 10 heads' faithfulness for the subj corruption on swap, all orders; reported only if the mean gap is at least 1.0 bit)**: NOT ESTIMABLE (mean gap < 1.0 bit)
Limit: masking is a corruption that may itself change the sentence's acceptability, and the swapped sentences are odd in meaning, so a preference after the swap may reflect oddness more than agreement; P7 cannot separate the two. Pseudo-log-likelihood is not true surprisal.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `swap_mask_muril.csv` | 702,157 | `6851cdd6483acea0` | per fresh order (one row; both versions orig and swap): the span margin M_<version>_<cond> for every condition (none, obj, subj, ne), and the 10 heads' patch for the swap subj corruption |
