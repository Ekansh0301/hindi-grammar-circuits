# mi_paper_swap_mask_xlmrlarge

_Paper experiment P7, stage swap_mask, xlmrlarge._

| provenance | |
|---|---|
| run (UTC) | 2026-11-18 16:35 |
| script | `mi_paper_mask.py` (sha256 `583473353c39433e`) |
| host | gnode (Linux) |
| duration | 17.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce GTX 1080 Ti |
| args | `{"limit": null, "max_rows": 128, "min_gap": 0.05, "model": "xlmrlarge", "record_tag": null, "stage": "swap_mask"}` |
| command | `scripts/mi_paper_mask.py --model xlmrlarge --max-rows 128 --stage swap_mask` |


- **metric decision**: ACCEPTED by the metric stage's declared rule
- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **frozen circuit (step 4 selection half, object task): 10 heads**: L21H0, L20H0, L20H2, L22H6, L19H3, L23H15, L12H6, L23H7, L17H7, L9H13
Signs: M_<version>_<cond> is the span margin toward the version's own correct form (bits). For swap that is the form that agrees with the swapped sentence's bare noun (the ex-subject, in the object slot): M_swap > 0 means the verb follows the bare noun. Conditions: none; obj (the bare noun's slot masked, the version's obj_words); subj (the ne-marked noun's slot masked, its subj_words, without ne); ne (the marker masked).

- **check: unedited version (orig, none and obj) against the metric stage's M_none and M_obj, orders / worst (bits)**: 2132 / 9.21e-04
- **check: orig and swap(none) against P2's role_swap file, orders in common / worst (bits)**: 2132 / 3.55e-15
- **check: embedding output patched everywhere recovers the clean margin (swap, none), first five orders, worst (bits)**: 0.00e+00
- **check: orders whose two versions hold different words apart from the agreeing words (must be 0)**: 0
- **orders read / entering (all eight runs built) / skipped**: 2132 / 2132 / 0
- **timing (loop only): minutes in total / minutes per order (all eight conditions and the patch)**: 17.13 / 0.0080
- **orders in the stratum where the swap-correct form is not the default form (subject not masculine singular) / documents**: 1197 / 127

## [all orders] Mean margin M (bits) and share of orders with M > 0, by class, version and condition


| class | version | orders | documents | M none | M obj | M subj | M ne | M>0 none | M>0 obj | M>0 subj | M>0 ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 1142 | 233 | 7.475 | 0.4783 | 7.02 | 6.643 | 0.9641 | 0.563 | 0.9641 | 0.9623 |
| SOV | swap | 1142 | 233 | -2.529 | -2.274 | 1.074 | -0.9454 | 0.2776 | 0.2986 | 0.6287 | 0.4203 |
| OSV | orig | 990 | 146 | 6.538 | 0.2823 | 4.715 | 5.395 | 0.9444 | 0.5354 | 0.8687 | 0.9081 |
| OSV | swap | 990 | 146 | -4.022 | -4.05 | -0.06612 | -1.737 | 0.1495 | 0.1424 | 0.4475 | 0.3687 |
| all | orig | 2132 | 235 | 7.04 | 0.3873 | 5.95 | 6.063 | 0.955 | 0.5502 | 0.9198 | 0.9371 |
| all | swap | 2132 | 235 | -3.223 | -3.099 | 0.5443 | -1.313 | 0.2181 | 0.2261 | 0.5446 | 0.3963 |


## [swap-correct form is not the default form] Mean margin M (bits) and share of orders with M > 0, by class, version and condition


| class | version | orders | documents | M none | M obj | M subj | M ne | M>0 none | M>0 obj | M>0 subj | M>0 ne |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SOV | orig | 640 | 125 | 8.206 | 2.107 | 7.79 | 7.401 | 0.9531 | 0.8109 | 0.9578 | 0.9641 |
| SOV | swap | 640 | 125 | -3.494 | -3.682 | -0.2514 | -1.544 | 0.2188 | 0.1594 | 0.4656 | 0.3625 |
| OSV | orig | 557 | 78 | 7.416 | 2.454 | 5.762 | 6.423 | 0.9354 | 0.7953 | 0.921 | 0.9282 |
| OSV | swap | 557 | 78 | -5.254 | -5.133 | -2.097 | -2.631 | 0.1041 | 0.08079 | 0.1939 | 0.2962 |
| all | orig | 1197 | 127 | 7.838 | 2.268 | 6.846 | 6.946 | 0.9449 | 0.8037 | 0.9407 | 0.9474 |
| all | swap | 1197 | 127 | -4.313 | -4.357 | -1.11 | -2.05 | 0.1654 | 0.1228 | 0.3392 | 0.3317 |


## [all orders] Primary: R = M_swap(subj) - M_swap(none), paired per order (one-sided document sign-flip, upward)


| class | orders | mean M_swap(none) (bits) | mean R (bits) | document bootstrap 95% | one-sided p (R > 0) | mean M_swap(subj) (bits) |
|---|---|---|---|---|---|---|
| SOV | 1142 | -2.529 | 3.603 | [3.046, 4.183] | 9.999e-05 | 1.074 |
| OSV | 990 | -4.022 | 3.956 | [3.310, 4.624] | 9.999e-05 | -0.06612 |


## [all orders] Bare noun's slot: M_swap(obj) - M_swap(none), paired per order (one-sided document sign-flip, downward)


| class | orders | mean change (bits) | document bootstrap 95% | one-sided p (fall) |
|---|---|---|---|---|
| SOV | 1142 | 0.255 | [-0.212, 0.663] | 0.865 |
| OSV | 990 | -0.02796 | [-0.277, 0.230] | 0.4106 |

- **[all orders] flags per class: R >= 1.0 bit with p < 0.05 / mean M_swap(subj) > 0 / bare-noun fall >= 1.0 bit with p < 0.05**: SOV: True / True / False; OSV: True / False / False
- **DECISION (the ne-marked noun's slot, all orders; declared: the verb reads the ne-marked noun if R >= 1.0 bit with p < 0.05 and mean M_swap(subj) > 0 in both classes; partly if R >= 1.0 bit with p < 0.05 but mean M_swap(subj) <= 0 in a class; else not)**: partly
- **DECISION (the bare noun's slot, all orders; declared: a fall of at least 1.0 bit with one-sided p < 0.05 means the verb also reads the bare noun)**: does not (in both classes) also read the bare noun

## [swap-correct form is not the default form] Primary: R = M_swap(subj) - M_swap(none), paired per order (one-sided document sign-flip, upward)


| class | orders | mean M_swap(none) (bits) | mean R (bits) | document bootstrap 95% | one-sided p (R > 0) | mean M_swap(subj) (bits) |
|---|---|---|---|---|---|---|
| SOV | 640 | -3.494 | 3.243 | [2.703, 3.876] | 9.999e-05 | -0.2514 |
| OSV | 557 | -5.254 | 3.157 | [2.470, 3.940] | 9.999e-05 | -2.097 |


## [swap-correct form is not the default form] Bare noun's slot: M_swap(obj) - M_swap(none), paired per order (one-sided document sign-flip, downward)


| class | orders | mean change (bits) | document bootstrap 95% | one-sided p (fall) |
|---|---|---|---|---|
| SOV | 640 | -0.1876 | [-0.751, 0.392] | 0.2572 |
| OSV | 557 | 0.1202 | [-0.246, 0.452] | 0.7399 |

- **[swap-correct form is not the default form] flags per class: R >= 1.0 bit with p < 0.05 / mean M_swap(subj) > 0 / bare-noun fall >= 1.0 bit with p < 0.05**: SOV: True / False / False; OSV: True / False / False
- **DECISION (the ne-marked noun's slot, stratum where the swap-correct form is not the default form)**: partly
- **DECISION (the bare noun's slot, stratum where the swap-correct form is not the default form)**: does not (in both classes) also read the bare noun
- **DECISION (P7 verdict on the ne-marked noun's slot; P2 rule: the stratum's verdict if it differs from the overall one)**: partly (all orders: partly; stratum: partly)
- **DECISION (P7 reading of the bare noun's slot, same rule)**: does not (in both classes) also read the bare noun (all orders: does not (in both classes) also read the bare noun; stratum: does not (in both classes) also read the bare noun)

## Change of the margin under each mask (M_<cond> minus M_none, paired per order), all orders, both versions (orig is the unswapped reference; ne is reported and not graded); mean and document bootstrap 95% (descriptive)


| class | version | orders | obj | subj | ne |
|---|---|---|---|---|---|
| SOV | orig | 1142 | -6.997 [-7.503, -6.476] | -0.455 [-0.636, -0.284] | -0.832 [-1.074, -0.610] |
| SOV | swap | 1142 | 0.255 [-0.212, 0.663] | 3.603 [3.046, 4.183] | 1.584 [1.215, 1.960] |
| OSV | orig | 990 | -6.256 [-6.964, -5.593] | -1.823 [-2.249, -1.421] | -1.143 [-1.530, -0.804] |
| OSV | swap | 990 | -0.028 [-0.277, 0.230] | 3.956 [3.310, 4.624] | 2.285 [1.760, 2.834] |
| all | orig | 2132 | -6.653 [-7.237, -6.082] | -1.090 [-1.351, -0.839] | -0.977 [-1.254, -0.729] |
| all | swap | 2132 | 0.124 [-0.178, 0.413] | 3.767 [3.243, 4.340] | 1.910 [1.550, 2.292] |


## Masking ne on swap, two-sided document sign-flip (reported, not graded)


| class | orders | mean M_swap(ne) - M_swap(none) (bits) | two-sided p |
|---|---|---|---|
| SOV | 1142 | 1.584 | 9.999e-05 |
| OSV | 990 | 2.285 | 9.999e-05 |


## Descriptive: share of orders whose preference changes sign under each mask / share that goes from M <= 0 (none) to M > 0 (masked)


| stratum | class | version | orders | obj | subj | ne |
|---|---|---|---|---|---|---|
| all orders | SOV | orig | 1142 | 0.422 / 0.011 | 0.018 / 0.009 | 0.032 / 0.015 |
| all orders | SOV | swap | 1142 | 0.205 / 0.113 | 0.376 / 0.363 | 0.206 / 0.174 |
| all orders | OSV | orig | 990 | 0.419 / 0.005 | 0.104 / 0.014 | 0.067 / 0.015 |
| all orders | OSV | swap | 990 | 0.092 / 0.042 | 0.336 / 0.317 | 0.286 / 0.253 |
| all orders | all | orig | 2132 | 0.421 / 0.008 | 0.058 / 0.011 | 0.048 / 0.015 |
| all orders | all | swap | 2132 | 0.152 / 0.080 | 0.357 / 0.342 | 0.243 / 0.211 |
| swap-correct form is not the default form | SOV | orig | 640 | 0.180 / 0.019 | 0.017 / 0.011 | 0.030 / 0.020 |
| swap-correct form is not the default form | SOV | swap | 640 | 0.159 / 0.050 | 0.278 / 0.263 | 0.175 / 0.159 |
| swap-correct form is not the default form | OSV | orig | 557 | 0.158 / 0.009 | 0.054 / 0.020 | 0.047 / 0.020 |
| swap-correct form is not the default form | OSV | swap | 557 | 0.059 / 0.018 | 0.151 / 0.120 | 0.224 / 0.208 |
| swap-correct form is not the default form | all | orig | 1197 | 0.170 / 0.014 | 0.034 / 0.015 | 0.038 / 0.020 |
| swap-correct form is not the default form | all | swap | 1197 | 0.113 / 0.035 | 0.219 / 0.196 | 0.198 / 0.182 |


## Descriptive: the 10 frozen heads' faithfulness for the subj corruption on swap (clean none, corrupted subj); the gap is M_swap(none) - M_swap(subj), so it is negative where masking the ne-marked noun raises the margin


| class | orders | mean gap (bits) | orders above the gap floor | 10 heads: share of the gap restored |
|---|---|---|---|---|
| SOV | 1142 | -3.603 | 1118 | NOT ESTIMABLE (mean gap < 1.0 bit) |
| OSV | 990 | -3.956 | 980 | NOT ESTIMABLE (mean gap < 1.0 bit) |
| all | 2132 | -3.767 | 2098 | NOT ESTIMABLE (mean gap < 1.0 bit) |

- **DECISION (descriptive: the 10 heads' faithfulness for the subj corruption on swap, all orders; reported only if the mean gap is at least 1.0 bit)**: NOT ESTIMABLE (mean gap < 1.0 bit)
Limit: masking is a corruption that may itself change the sentence's acceptability, and the swapped sentences are odd in meaning, so a preference after the swap may reflect oddness more than agreement; P7 cannot separate the two. Pseudo-log-likelihood is not true surprisal.


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `swap_mask_xlmrlarge.csv` | 702,955 | `4931d7c6605d6fc1` | per fresh order (one row; both versions orig and swap): the span margin M_<version>_<cond> for every condition (none, obj, subj, ne), and the 10 heads' patch for the swap subj corruption |
