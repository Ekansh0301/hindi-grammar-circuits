# rq1_layerwise_decomposition_tuned

_The four-block decomposition with surprisal read from every layer, not only the output._

| provenance | |
|---|---|
| run (UTC) | 2026-09-26 16:09 |
| script | `rq1_layerwise_decomposition.py` (sha256 `f2308cd6855fd3fd`) |
| host | gnode (Linux) |
| duration | 25.9 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"bootstrap": 2000, "lens": "tuned", "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "tag": "rq1_layerwise_decomposition_tuned", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_layerwise_decomposition.py --lens tuned --tag rq1_layerwise_decomposition_tuned` |



## model: muril

- **pairs / lens layers / lens**: 8,630 / 13 / tuned
- **readable layers**: 8, 9, 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0034 | 0.0016 | 0.5268 | 0.0003 | -0.0001 | 0.0008 |
| 1 | no | 0.0016 | 0.0004 | 0.7206 | 0.0001 | -0.0001 | 0.0003 |
| 2 | no | 0.0042 | 0.0010 | 0.7591 | 0.0001 | -0.0002 | 0.0005 |
| 3 | no | 0.0099 | 0.0026 | 0.7338 | 0.0006 | 0.0000 | 0.0011 |
| 4 | no | 0.0237 | 0.0100 | 0.5797 | 0.0026 | 0.0016 | 0.0037 |
| 5 | no | 0.0342 | 0.0168 | 0.5099 | 0.0047 | 0.0034 | 0.0060 |
| 6 | no | 0.0387 | 0.0185 | 0.5216 | 0.0057 | 0.0043 | 0.0070 |
| 7 | no | 0.0606 | 0.0346 | 0.4287 | 0.0097 | 0.0078 | 0.0116 |
| 8 | yes | 0.0750 | 0.0442 | 0.4110 | 0.0124 | 0.0103 | 0.0146 |
| 9 | yes | 0.0766 | 0.0465 | 0.3921 | 0.0132 | 0.0111 | 0.0154 |
| 10 | yes | 0.0826 | 0.0521 | 0.3692 | 0.0146 | 0.0124 | 0.0169 |
| 11 | yes | 0.0795 | 0.0501 | 0.3694 | 0.0144 | 0.0122 | 0.0167 |
| 12 | yes | 0.0867 | 0.0557 | 0.3570 | 0.0157 | 0.0135 | 0.0181 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0867, 0.357
- **layer with the largest ΔR²(T|L,S)**: 12 (0.0867, absorbed share 0.357, readable: yes)

## model: indicbert

- **pairs / lens layers / lens**: 8,630 / 13 / tuned
- **readable layers**: 5, 6, 7, 8, 9, 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0063 | 0.0033 | 0.4711 | 0.0009 | 0.0003 | 0.0016 |
| 1 | no | 0.0049 | 0.0016 | 0.6759 | 0.0004 | 0.0000 | 0.0008 |
| 2 | no | 0.0087 | 0.0031 | 0.6495 | 0.0009 | 0.0003 | 0.0015 |
| 3 | no | 0.0131 | 0.0047 | 0.6453 | 0.0014 | 0.0007 | 0.0021 |
| 4 | no | 0.0188 | 0.0074 | 0.6076 | 0.0021 | 0.0012 | 0.0030 |
| 5 | yes | 0.0294 | 0.0141 | 0.5196 | 0.0040 | 0.0027 | 0.0053 |
| 6 | yes | 0.0389 | 0.0195 | 0.4971 | 0.0057 | 0.0042 | 0.0071 |
| 7 | yes | 0.0524 | 0.0291 | 0.4441 | 0.0082 | 0.0065 | 0.0099 |
| 8 | yes | 0.0639 | 0.0386 | 0.3956 | 0.0105 | 0.0086 | 0.0126 |
| 9 | yes | 0.0743 | 0.0472 | 0.3643 | 0.0128 | 0.0107 | 0.0151 |
| 10 | yes | 0.0709 | 0.0466 | 0.3432 | 0.0125 | 0.0103 | 0.0147 |
| 11 | yes | 0.0741 | 0.0494 | 0.3333 | 0.0135 | 0.0112 | 0.0157 |
| 12 | yes | 0.0727 | 0.0482 | 0.3380 | 0.0131 | 0.0109 | 0.0153 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0727, 0.338
- **layer with the largest ΔR²(T|L,S)**: 9 (0.0743, absorbed share 0.364, readable: yes)

## model: mbert

- **pairs / lens layers / lens**: 8,629 / 13 / tuned
- **readable layers**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0027 | 0.0011 | 0.5797 | 0.0002 | -0.0002 | 0.0006 |
| 1 | yes | 0.0017 | 0.0005 | 0.6872 | 0.0001 | -0.0001 | 0.0003 |
| 2 | yes | 0.0014 | 0.0003 | 0.7805 | -0.0000 | -0.0002 | 0.0001 |
| 3 | yes | 0.0035 | 0.0012 | 0.6474 | 0.0002 | -0.0002 | 0.0006 |
| 4 | yes | 0.0058 | 0.0022 | 0.6311 | 0.0005 | -0.0000 | 0.0010 |
| 5 | yes | 0.0101 | 0.0036 | 0.6459 | 0.0010 | 0.0003 | 0.0016 |
| 6 | yes | 0.0177 | 0.0063 | 0.6460 | 0.0018 | 0.0009 | 0.0027 |
| 7 | yes | 0.0228 | 0.0093 | 0.5944 | 0.0027 | 0.0017 | 0.0037 |
| 8 | yes | 0.0328 | 0.0146 | 0.5533 | 0.0041 | 0.0028 | 0.0054 |
| 9 | yes | 0.0413 | 0.0195 | 0.5273 | 0.0055 | 0.0040 | 0.0069 |
| 10 | yes | 0.0431 | 0.0224 | 0.4805 | 0.0062 | 0.0046 | 0.0077 |
| 11 | yes | 0.0379 | 0.0196 | 0.4824 | 0.0053 | 0.0038 | 0.0068 |
| 12 | yes | 0.0318 | 0.0162 | 0.4904 | 0.0042 | 0.0028 | 0.0055 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0318, 0.490
- **layer with the largest ΔR²(T|L,S)**: 10 (0.0431, absorbed share 0.480, readable: yes)

## model: xlmrlarge

- **pairs / lens layers / lens**: 8,630 / 25 / tuned
- **readable layers**: 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0039 | 0.0011 | 0.7213 | 0.0001 | -0.0003 | 0.0004 |
| 1 | no | 0.0038 | 0.0009 | 0.7698 | 0.0000 | -0.0003 | 0.0003 |
| 2 | no | 0.0034 | 0.0006 | 0.8080 | 0.0002 | -0.0001 | 0.0004 |
| 3 | no | 0.0042 | 0.0009 | 0.7816 | 0.0003 | -0.0000 | 0.0006 |
| 4 | no | 0.0040 | 0.0010 | 0.7523 | 0.0003 | -0.0000 | 0.0006 |
| 5 | no | 0.0046 | 0.0011 | 0.7616 | 0.0003 | 0.0000 | 0.0007 |
| 6 | no | 0.0050 | 0.0012 | 0.7668 | 0.0004 | 0.0000 | 0.0007 |
| 7 | no | 0.0092 | 0.0027 | 0.7033 | 0.0008 | 0.0003 | 0.0013 |
| 8 | no | 0.0117 | 0.0038 | 0.6726 | 0.0011 | 0.0004 | 0.0017 |
| 9 | yes | 0.0182 | 0.0066 | 0.6372 | 0.0017 | 0.0009 | 0.0026 |
| 10 | yes | 0.0260 | 0.0108 | 0.5822 | 0.0030 | 0.0019 | 0.0040 |
| 11 | yes | 0.0356 | 0.0163 | 0.5424 | 0.0045 | 0.0032 | 0.0058 |
| 12 | yes | 0.0436 | 0.0223 | 0.4886 | 0.0064 | 0.0049 | 0.0079 |
| 13 | yes | 0.0477 | 0.0253 | 0.4699 | 0.0073 | 0.0057 | 0.0089 |
| 14 | yes | 0.0504 | 0.0272 | 0.4598 | 0.0078 | 0.0061 | 0.0095 |
| 15 | yes | 0.0549 | 0.0301 | 0.4514 | 0.0089 | 0.0070 | 0.0106 |
| 16 | yes | 0.0567 | 0.0307 | 0.4581 | 0.0090 | 0.0072 | 0.0108 |
| 17 | yes | 0.0617 | 0.0348 | 0.4360 | 0.0102 | 0.0084 | 0.0120 |
| 18 | yes | 0.0656 | 0.0382 | 0.4181 | 0.0110 | 0.0090 | 0.0130 |
| 19 | yes | 0.0737 | 0.0449 | 0.3901 | 0.0128 | 0.0108 | 0.0150 |
| 20 | yes | 0.0799 | 0.0501 | 0.3725 | 0.0141 | 0.0119 | 0.0163 |
| 21 | yes | 0.0822 | 0.0524 | 0.3621 | 0.0147 | 0.0125 | 0.0171 |
| 22 | yes | 0.0784 | 0.0503 | 0.3579 | 0.0142 | 0.0121 | 0.0165 |
| 23 | yes | 0.0790 | 0.0504 | 0.3628 | 0.0142 | 0.0121 | 0.0165 |
| 24 | yes | 0.0837 | 0.0539 | 0.3561 | 0.0154 | 0.0132 | 0.0178 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0837, 0.356
- **layer with the largest ΔR²(T|L,S)**: 24 (0.0837, absorbed share 0.356, readable: yes)

## Summary


| model | final ΔR²(T|L,S) | final absorbed share | best layer | its ΔR²(T|L,S) | its absorbed share |
|---|---|---|---|---|---|
| muril | 0.0867 | 0.3570 | 12 | 0.0867 | 0.3570 |
| indicbert | 0.0727 | 0.3380 | 9 | 0.0743 | 0.3643 |
| mbert | 0.0318 | 0.4904 | 10 | 0.0431 | 0.4805 |
| xlmrlarge | 0.0837 | 0.3561 | 24 | 0.0837 | 0.3561 |

The dissociation the layer probes suggest would show here as a middle layer whose surprisal adds more than the output's, or whose absorbed share is lower — structure present in the representation and spent by the time the model speaks. Read only the layers marked readable; the rest are reported because hiding them would make the readable ones look like a choice.
