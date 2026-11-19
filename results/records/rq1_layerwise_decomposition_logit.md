# rq1_layerwise_decomposition_logit

_The four-block decomposition with surprisal read from every layer, not only the output._

| provenance | |
|---|---|
| run (UTC) | 2026-09-26 15:43 |
| script | `rq1_layerwise_decomposition.py` (sha256 `f2308cd6855fd3fd`) |
| host | gnode (Linux) |
| duration | 26.3 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"bootstrap": 2000, "lens": "logit", "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "tag": "rq1_layerwise_decomposition_logit", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_layerwise_decomposition.py --lens logit --tag rq1_layerwise_decomposition_logit` |



## model: muril

- **pairs / lens layers / lens**: 8,630 / 13 / logit
- **readable layers**: 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0011 | 0.0008 | 0.2799 | 0.0002 | -0.0001 | 0.0004 |
| 1 | no | 0.0006 | 0.0004 | 0.4071 | -0.0001 | -0.0002 | 0.0000 |
| 2 | no | 0.0004 | 0.0004 | 0.1807 | -0.0000 | -0.0001 | 0.0000 |
| 3 | no | 0.0004 | 0.0004 | 0.0285 | -0.0002 | -0.0003 | -0.0001 |
| 4 | no | 0.0013 | 0.0010 | 0.1856 | 0.0000 | -0.0003 | 0.0003 |
| 5 | no | 0.0015 | 0.0005 | 0.6816 | -0.0000 | -0.0001 | 0.0001 |
| 6 | no | 0.0051 | 0.0014 | 0.7189 | 0.0003 | -0.0000 | 0.0006 |
| 7 | no | 0.0102 | 0.0051 | 0.4990 | 0.0014 | 0.0007 | 0.0021 |
| 8 | no | 0.0020 | 0.0008 | 0.6301 | 0.0001 | -0.0001 | 0.0003 |
| 9 | no | 0.0005 | 0.0005 | -0.0335 | -0.0000 | -0.0001 | 0.0001 |
| 10 | no | 0.0028 | 0.0019 | 0.3048 | 0.0003 | -0.0001 | 0.0007 |
| 11 | no | 0.0042 | 0.0032 | 0.2498 | 0.0008 | 0.0002 | 0.0014 |
| 12 | yes | 0.0867 | 0.0557 | 0.3570 | 0.0157 | 0.0135 | 0.0181 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0867, 0.357
- **layer with the largest ΔR²(T|L,S)**: 12 (0.0867, absorbed share 0.357, readable: yes)

## model: indicbert

- **pairs / lens layers / lens**: 8,630 / 13 / logit
- **readable layers**: 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0010 | 0.0008 | 0.2364 | 0.0001 | -0.0002 | 0.0003 |
| 1 | no | 0.0011 | 0.0004 | 0.6658 | -0.0000 | -0.0002 | 0.0001 |
| 2 | no | 0.0028 | 0.0008 | 0.7046 | 0.0001 | -0.0002 | 0.0004 |
| 3 | no | 0.0047 | 0.0013 | 0.7193 | 0.0003 | -0.0001 | 0.0006 |
| 4 | no | 0.0058 | 0.0016 | 0.7275 | 0.0004 | -0.0001 | 0.0008 |
| 5 | no | 0.0103 | 0.0039 | 0.6184 | 0.0010 | 0.0003 | 0.0017 |
| 6 | no | 0.0195 | 0.0077 | 0.6030 | 0.0022 | 0.0013 | 0.0032 |
| 7 | no | 0.0222 | 0.0108 | 0.5136 | 0.0030 | 0.0019 | 0.0041 |
| 8 | no | 0.0329 | 0.0177 | 0.4625 | 0.0048 | 0.0034 | 0.0063 |
| 9 | no | 0.0468 | 0.0283 | 0.3964 | 0.0077 | 0.0058 | 0.0094 |
| 10 | yes | 0.0617 | 0.0404 | 0.3443 | 0.0109 | 0.0088 | 0.0130 |
| 11 | yes | 0.0637 | 0.0429 | 0.3277 | 0.0118 | 0.0095 | 0.0139 |
| 12 | yes | 0.0727 | 0.0482 | 0.3380 | 0.0131 | 0.0109 | 0.0153 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0727, 0.338
- **layer with the largest ΔR²(T|L,S)**: 12 (0.0727, absorbed share 0.338, readable: yes)

## model: mbert

- **pairs / lens layers / lens**: 8,629 / 13 / logit
- **readable layers**: 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0006 | 0.0005 | 0.2389 | 0.0000 | -0.0002 | 0.0002 |
| 1 | no | 0.0010 | 0.0006 | 0.3848 | 0.0000 | -0.0002 | 0.0003 |
| 2 | no | 0.0011 | 0.0006 | 0.4282 | 0.0000 | -0.0002 | 0.0003 |
| 3 | no | 0.0059 | 0.0025 | 0.5748 | 0.0005 | -0.0000 | 0.0010 |
| 4 | no | 0.0085 | 0.0037 | 0.5694 | 0.0009 | 0.0003 | 0.0015 |
| 5 | no | 0.0091 | 0.0030 | 0.6664 | 0.0006 | 0.0001 | 0.0012 |
| 6 | no | 0.0033 | 0.0011 | 0.6768 | 0.0001 | -0.0002 | 0.0004 |
| 7 | no | 0.0007 | 0.0006 | 0.2044 | 0.0000 | -0.0002 | 0.0003 |
| 8 | no | 0.0016 | 0.0018 | -0.0699 | 0.0004 | -0.0001 | 0.0008 |
| 9 | no | 0.0104 | 0.0072 | 0.3065 | 0.0019 | 0.0010 | 0.0028 |
| 10 | no | 0.0184 | 0.0098 | 0.4691 | 0.0025 | 0.0015 | 0.0035 |
| 11 | no | 0.0157 | 0.0072 | 0.5432 | 0.0020 | 0.0011 | 0.0029 |
| 12 | yes | 0.0318 | 0.0162 | 0.4904 | 0.0042 | 0.0028 | 0.0055 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0318, 0.490
- **layer with the largest ΔR²(T|L,S)**: 12 (0.0318, absorbed share 0.490, readable: yes)

## model: xlmrlarge

- **pairs / lens layers / lens**: 8,630 / 25 / logit
- **readable layers**: 21, 22, 23, 24

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0003 | 0.0003 | 0.0932 | -0.0000 | -0.0001 | 0.0000 |
| 1 | no | 0.0003 | 0.0003 | 0.0971 | -0.0001 | -0.0002 | 0.0000 |
| 2 | no | 0.0007 | 0.0005 | 0.3842 | -0.0001 | -0.0003 | 0.0001 |
| 3 | no | 0.0011 | 0.0004 | 0.5819 | -0.0001 | -0.0003 | 0.0001 |
| 4 | no | 0.0013 | 0.0006 | 0.5433 | -0.0001 | -0.0003 | 0.0001 |
| 5 | no | 0.0010 | 0.0003 | 0.7037 | -0.0001 | -0.0002 | 0.0000 |
| 6 | no | 0.0020 | 0.0007 | 0.6503 | 0.0000 | -0.0002 | 0.0003 |
| 7 | no | 0.0020 | 0.0005 | 0.7593 | 0.0000 | -0.0002 | 0.0002 |
| 8 | no | 0.0050 | 0.0017 | 0.6710 | 0.0003 | -0.0001 | 0.0007 |
| 9 | no | 0.0101 | 0.0040 | 0.6027 | 0.0008 | 0.0001 | 0.0015 |
| 10 | no | 0.0109 | 0.0051 | 0.5367 | 0.0011 | 0.0003 | 0.0018 |
| 11 | no | 0.0196 | 0.0075 | 0.6154 | 0.0018 | 0.0009 | 0.0027 |
| 12 | no | 0.0230 | 0.0098 | 0.5749 | 0.0026 | 0.0016 | 0.0036 |
| 13 | no | 0.0140 | 0.0051 | 0.6314 | 0.0014 | 0.0007 | 0.0022 |
| 14 | no | 0.0208 | 0.0090 | 0.5666 | 0.0026 | 0.0016 | 0.0035 |
| 15 | no | 0.0213 | 0.0103 | 0.5186 | 0.0030 | 0.0020 | 0.0041 |
| 16 | no | 0.0345 | 0.0200 | 0.4216 | 0.0056 | 0.0041 | 0.0069 |
| 17 | no | 0.0471 | 0.0280 | 0.4054 | 0.0078 | 0.0062 | 0.0095 |
| 18 | no | 0.0739 | 0.0452 | 0.3893 | 0.0127 | 0.0106 | 0.0149 |
| 19 | no | 0.0680 | 0.0420 | 0.3831 | 0.0117 | 0.0097 | 0.0138 |
| 20 | no | 0.0659 | 0.0412 | 0.3750 | 0.0117 | 0.0097 | 0.0138 |
| 21 | yes | 0.0592 | 0.0371 | 0.3730 | 0.0107 | 0.0087 | 0.0126 |
| 22 | yes | 0.0617 | 0.0391 | 0.3653 | 0.0113 | 0.0093 | 0.0133 |
| 23 | yes | 0.0696 | 0.0445 | 0.3608 | 0.0128 | 0.0108 | 0.0150 |
| 24 | yes | 0.0837 | 0.0539 | 0.3561 | 0.0154 | 0.0132 | 0.0178 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0837, 0.356
- **layer with the largest ΔR²(T|L,S)**: 24 (0.0837, absorbed share 0.356, readable: yes)

## Summary


| model | final ΔR²(T|L,S) | final absorbed share | best layer | its ΔR²(T|L,S) | its absorbed share |
|---|---|---|---|---|---|
| muril | 0.0867 | 0.3570 | 12 | 0.0867 | 0.3570 |
| indicbert | 0.0727 | 0.3380 | 12 | 0.0727 | 0.3380 |
| mbert | 0.0318 | 0.4904 | 12 | 0.0318 | 0.4904 |
| xlmrlarge | 0.0837 | 0.3561 | 24 | 0.0837 | 0.3561 |

The dissociation the layer probes suggest would show here as a middle layer whose surprisal adds more than the output's, or whose absorbed share is lower — structure present in the representation and spent by the time the model speaks. Read only the layers marked readable; the rest are reported because hiding them would make the readable ones look like a choice.
