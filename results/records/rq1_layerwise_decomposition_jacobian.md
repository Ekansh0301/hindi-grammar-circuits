# rq1_layerwise_decomposition_jacobian

_The four-block decomposition with surprisal read from every layer, not only the output._

| provenance | |
|---|---|
| run (UTC) | 2026-10-01 18:17 |
| script | `rq1_layerwise_decomposition.py` (sha256 `8c78ec214ab4e044`) |
| host | gnode (Linux) |
| duration | 29.2 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ? |
| args | `{"bootstrap": 2000, "lens": "jacobian", "models": ["muril", "indicbert", "mbert", "xlmrlarge"], "tag": "rq1_layerwise_decomposition_jacobian", "words_dir": "<earlier-repo>/sets/set1/Results_Checks/lm_units"}` |
| command | `scripts/rq1_layerwise_decomposition.py --lens jacobian --tag rq1_layerwise_decomposition_jacobian` |



## model: muril

- **pairs / lens layers / lens**: 8,630 / 13 / jacobian
- **readable layers**: 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0010 | 0.0005 | 0.5290 | 0.0002 | -0.0001 | 0.0004 |
| 1 | no | 0.0005 | -0.0000 | 1.0005 | 0.0000 | -0.0001 | 0.0001 |
| 2 | no | 0.0029 | 0.0005 | 0.8356 | 0.0001 | -0.0002 | 0.0003 |
| 3 | no | 0.0051 | 0.0011 | 0.7828 | 0.0002 | -0.0002 | 0.0006 |
| 4 | no | 0.0131 | 0.0045 | 0.6585 | 0.0012 | 0.0005 | 0.0019 |
| 5 | no | 0.0184 | 0.0064 | 0.6508 | 0.0019 | 0.0010 | 0.0027 |
| 6 | no | 0.0445 | 0.0207 | 0.5360 | 0.0061 | 0.0046 | 0.0076 |
| 7 | no | 0.0831 | 0.0451 | 0.4570 | 0.0128 | 0.0108 | 0.0149 |
| 8 | no | 0.1041 | 0.0620 | 0.4050 | 0.0175 | 0.0150 | 0.0200 |
| 9 | no | 0.1021 | 0.0627 | 0.3855 | 0.0176 | 0.0152 | 0.0201 |
| 10 | yes | 0.0974 | 0.0615 | 0.3679 | 0.0173 | 0.0149 | 0.0197 |
| 11 | yes | 0.0816 | 0.0512 | 0.3721 | 0.0144 | 0.0123 | 0.0167 |
| 12 | yes | 0.0867 | 0.0557 | 0.3570 | 0.0157 | 0.0135 | 0.0181 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0867, 0.357
- **layer with the largest ΔR²(T|L,S)**: 8 (0.1041, absorbed share 0.405, readable: no)

## model: indicbert

- **pairs / lens layers / lens**: 8,630 / 13 / jacobian
- **readable layers**: 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0005 | 0.0003 | 0.4207 | 0.0001 | -0.0001 | 0.0003 |
| 1 | no | 0.0025 | 0.0008 | 0.7005 | 0.0003 | -0.0001 | 0.0006 |
| 2 | no | 0.0040 | 0.0015 | 0.6322 | 0.0005 | 0.0001 | 0.0010 |
| 3 | no | 0.0109 | 0.0041 | 0.6231 | 0.0013 | 0.0006 | 0.0020 |
| 4 | no | 0.0101 | 0.0025 | 0.7533 | 0.0008 | 0.0003 | 0.0014 |
| 5 | no | 0.0173 | 0.0055 | 0.6818 | 0.0017 | 0.0009 | 0.0024 |
| 6 | no | 0.0335 | 0.0130 | 0.6110 | 0.0038 | 0.0026 | 0.0050 |
| 7 | no | 0.0528 | 0.0240 | 0.5453 | 0.0069 | 0.0053 | 0.0085 |
| 8 | no | 0.0880 | 0.0484 | 0.4505 | 0.0134 | 0.0112 | 0.0158 |
| 9 | no | 0.1063 | 0.0656 | 0.3832 | 0.0179 | 0.0153 | 0.0206 |
| 10 | yes | 0.0826 | 0.0533 | 0.3547 | 0.0142 | 0.0119 | 0.0167 |
| 11 | yes | 0.0752 | 0.0504 | 0.3307 | 0.0136 | 0.0112 | 0.0160 |
| 12 | yes | 0.0727 | 0.0482 | 0.3380 | 0.0131 | 0.0109 | 0.0153 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0727, 0.338
- **layer with the largest ΔR²(T|L,S)**: 9 (0.1063, absorbed share 0.383, readable: no)

## model: mbert

- **pairs / lens layers / lens**: 8,629 / 13 / jacobian
- **readable layers**: 8, 9, 10, 11, 12

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | -0.0002 | -0.0001 | nan | -0.0001 | -0.0001 | 0.0000 |
| 1 | no | -0.0001 | -0.0001 | nan | -0.0001 | -0.0002 | 0.0001 |
| 2 | no | -0.0001 | 0.0000 | nan | -0.0002 | -0.0003 | -0.0000 |
| 3 | no | 0.0002 | -0.0001 | 1.2303 | -0.0000 | -0.0001 | 0.0000 |
| 4 | no | 0.0005 | -0.0000 | 1.0419 | -0.0000 | -0.0001 | 0.0000 |
| 5 | no | 0.0016 | 0.0003 | 0.8263 | 0.0001 | -0.0001 | 0.0003 |
| 6 | no | 0.0062 | 0.0019 | 0.6895 | 0.0005 | 0.0000 | 0.0010 |
| 7 | no | 0.0077 | 0.0027 | 0.6538 | 0.0008 | 0.0002 | 0.0013 |
| 8 | yes | 0.0212 | 0.0093 | 0.5619 | 0.0026 | 0.0016 | 0.0036 |
| 9 | yes | 0.0388 | 0.0188 | 0.5154 | 0.0050 | 0.0036 | 0.0064 |
| 10 | yes | 0.0511 | 0.0267 | 0.4787 | 0.0072 | 0.0054 | 0.0088 |
| 11 | yes | 0.0442 | 0.0229 | 0.4814 | 0.0062 | 0.0046 | 0.0077 |
| 12 | yes | 0.0318 | 0.0162 | 0.4904 | 0.0042 | 0.0028 | 0.0055 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0318, 0.490
- **layer with the largest ΔR²(T|L,S)**: 10 (0.0511, absorbed share 0.479, readable: yes)

## model: xlmrlarge

- **pairs / lens layers / lens**: 8,630 / 25 / jacobian
- **readable layers**: 21, 22, 23, 24

| layer | readable | ΔR²(T_layer | L,S) | ΔR²(T_layer | L,S,E1) | absorbed share | ΔAUC over L+S+E1 | 95% low | 95% high |
|---|---|---|---|---|---|---|---|
| 0 | no | 0.0014 | 0.0012 | 0.1699 | 0.0003 | -0.0001 | 0.0007 |
| 1 | no | -0.0001 | -0.0001 | nan | -0.0001 | -0.0001 | 0.0000 |
| 2 | no | 0.0000 | -0.0001 | 3.2752 | -0.0000 | -0.0001 | 0.0000 |
| 3 | no | 0.0000 | -0.0000 | 1.1798 | -0.0001 | -0.0002 | 0.0000 |
| 4 | no | 0.0001 | 0.0001 | -0.0825 | -0.0001 | -0.0003 | 0.0000 |
| 5 | no | 0.0002 | 0.0000 | 0.7207 | -0.0001 | -0.0003 | -0.0000 |
| 6 | no | 0.0004 | 0.0000 | 0.9670 | -0.0001 | -0.0002 | -0.0000 |
| 7 | no | 0.0006 | -0.0000 | 1.0143 | -0.0001 | -0.0002 | -0.0000 |
| 8 | no | 0.0009 | -0.0000 | 1.0010 | -0.0001 | -0.0002 | -0.0000 |
| 9 | no | 0.0029 | 0.0003 | 0.8807 | 0.0001 | -0.0002 | 0.0003 |
| 10 | no | 0.0046 | 0.0008 | 0.8249 | 0.0002 | -0.0001 | 0.0005 |
| 11 | no | 0.0077 | 0.0017 | 0.7748 | 0.0005 | 0.0001 | 0.0010 |
| 12 | no | 0.0142 | 0.0042 | 0.7044 | 0.0013 | 0.0006 | 0.0019 |
| 13 | no | 0.0156 | 0.0046 | 0.7028 | 0.0014 | 0.0007 | 0.0021 |
| 14 | no | 0.0210 | 0.0069 | 0.6719 | 0.0021 | 0.0012 | 0.0029 |
| 15 | no | 0.0399 | 0.0169 | 0.5755 | 0.0051 | 0.0037 | 0.0063 |
| 16 | no | 0.0527 | 0.0247 | 0.5316 | 0.0073 | 0.0057 | 0.0088 |
| 17 | no | 0.0713 | 0.0377 | 0.4714 | 0.0110 | 0.0091 | 0.0128 |
| 18 | no | 0.0958 | 0.0563 | 0.4129 | 0.0160 | 0.0137 | 0.0183 |
| 19 | no | 0.1167 | 0.0728 | 0.3758 | 0.0202 | 0.0177 | 0.0229 |
| 20 | no | 0.1118 | 0.0723 | 0.3536 | 0.0198 | 0.0172 | 0.0224 |
| 21 | yes | 0.0977 | 0.0646 | 0.3390 | 0.0181 | 0.0157 | 0.0206 |
| 22 | yes | 0.0791 | 0.0509 | 0.3562 | 0.0143 | 0.0122 | 0.0166 |
| 23 | yes | 0.0775 | 0.0497 | 0.3590 | 0.0141 | 0.0119 | 0.0163 |
| 24 | yes | 0.0837 | 0.0539 | 0.3561 | 0.0154 | 0.0132 | 0.0178 |

- **final layer: ΔR²(T|L,S), absorbed share**: 0.0837, 0.356
- **layer with the largest ΔR²(T|L,S)**: 19 (0.1167, absorbed share 0.376, readable: no)

## Summary


| model | final ΔR²(T|L,S) | final absorbed share | best layer | its ΔR²(T|L,S) | its absorbed share |
|---|---|---|---|---|---|
| muril | 0.0867 | 0.3570 | 8 | 0.1041 | 0.4050 |
| indicbert | 0.0727 | 0.3380 | 9 | 0.1063 | 0.3832 |
| mbert | 0.0318 | 0.4904 | 10 | 0.0511 | 0.4787 |
| xlmrlarge | 0.0837 | 0.3561 | 19 | 0.1167 | 0.3758 |

The dissociation the layer probes suggest would show here as a middle layer whose surprisal adds more than the output's, or whose absorbed share is lower — structure present in the representation and spent by the time the model speaks. Read only the layers marked readable; the rest are reported because hiding them would make the readable ones look like a choice.
