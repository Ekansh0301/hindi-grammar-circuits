# mi_swap_screen_wordorder_muril

_Follow-up 3, halves swapped: screen, wordorder, muril._

| provenance | |
|---|---|
| run (UTC) | 2026-10-27 14:16 |
| script | `mi_swap.py` (sha256 `b63568958fbeb51c`) |
| host | gnode (Linux) |
| duration | 0.7 min |
| versions | python 3.12.4, torch 2.5.1+cu121, transformers 4.55.4, pandas 3.0.5, numpy 2.5.3, sklearn 1.9.1, minicons 0.3.39, kenlm ?, gpu NVIDIA GeForce RTX 2080 Ti |
| args | `{"batch_size": 32, "chunk": 16, "half": "heldout", "k": 10, "k_mlp": 5, "limit": null, "max_rows": 256, "min_gap": 0.05, "model": "muril", "n_mean": 300, "n_random": 100, "n_read": 100, "record_tag": null, "sentences": "<project>/data/heldout_text/readability_sentences.txt", "stage": "screen", "task": "wordorder"}` |
| command | `scripts/mi_swap.py --model muril --max-rows 256 --chunk 16 --task wordorder --stage screen` |


- **roles**: components chosen on the HELD-OUT half (screen, exact); validated on the SELECTION half (validate)
- **half this stage reads**: heldout
Labels inside this record that say 'selection half' (the stage functions are step 4's, unchanged) mean the half the components were CHOSEN on, here the held-out half; 'held-out half' means the half they are validated on, here the selection half.

- **check: head layout (attention x value slice h against attention input slice h), worst (abs)**: 0.00e+00
- **check: unpatched runs against step 2's s_ref and s_var, worst pair (bits)**: 2.95e-05
- **pairs / skipped / with a gap above --min-gap**: 154 / 0 / 135

| component | screened share | via special | via moved_heads | via moved_psp | via moved_other | via verb | via unmoved |
|---|---|---|---|---|---|---|---|
| L10MLP | 0.7169 | 0.0000 | 0.2932 | 0.0894 | 0.1545 | 0.0951 | 0.0846 |
| L9MLP | 0.5854 | -0.0002 | 0.2482 | 0.0773 | 0.1133 | 0.0703 | 0.0765 |
| L8MLP | 0.5286 | -0.0008 | 0.1949 | 0.0839 | 0.1098 | 0.0607 | 0.0801 |
| L7MLP | 0.4508 | -0.0005 | 0.1677 | 0.0954 | 0.0913 | 0.0279 | 0.0691 |
| L6MLP | 0.3022 | -0.0005 | 0.1171 | 0.0645 | 0.0684 | 0.0029 | 0.0497 |
| L11MLP | 0.2997 | 0.0000 | 0.1781 | -0.0076 | 0.0385 | 0.0600 | 0.0307 |
| L4MLP | 0.2349 | -0.0003 | 0.0973 | 0.0465 | 0.0390 | 0.0148 | 0.0377 |
| L5MLP | 0.2263 | 0.0001 | 0.0834 | 0.0492 | 0.0456 | 0.0095 | 0.0386 |
| L3MLP | 0.1881 | -0.0007 | 0.0808 | 0.0321 | 0.0381 | 0.0168 | 0.0210 |
| L2MLP | 0.1762 | 0.0009 | 0.0799 | 0.0360 | 0.0369 | 0.0085 | 0.0140 |
| L1MLP | 0.1526 | -0.0003 | 0.0787 | 0.0225 | 0.0369 | 0.0039 | 0.0110 |
| L9H10 | 0.1083 | -0.0000 | 0.0541 | 0.0065 | 0.0285 | 0.0050 | 0.0143 |
| L3H11 | 0.0974 | -0.0000 | 0.0488 | 0.0185 | 0.0199 | 0.0003 | 0.0098 |
| L8H11 | 0.0826 | -0.0000 | 0.0397 | 0.0105 | 0.0181 | 0.0018 | 0.0127 |
| L1H3 | 0.0822 | -0.0000 | 0.0335 | 0.0074 | 0.0252 | 0.0102 | 0.0059 |
| L10H4 | 0.0793 | 0.0000 | 0.0385 | 0.0047 | 0.0164 | 0.0099 | 0.0098 |
| L0MLP | 0.0760 | -0.0001 | 0.0338 | 0.0163 | 0.0305 | 0.0004 | -0.0049 |
| L9H3 | 0.0737 | -0.0000 | 0.0227 | 0.0184 | 0.0208 | 0.0019 | 0.0099 |
| L6H4 | 0.0734 | 0.0000 | 0.0349 | 0.0135 | 0.0155 | 0.0007 | 0.0088 |
| L10H6 | 0.0711 | 0.0000 | 0.0339 | 0.0076 | 0.0130 | 0.0089 | 0.0077 |
| L9H1 | -0.0704 | 0.0000 | -0.0299 | -0.0076 | -0.0159 | -0.0063 | -0.0107 |
| L4H4 | 0.0702 | 0.0000 | 0.0373 | 0.0148 | 0.0096 | -0.0005 | 0.0089 |
| L9H11 | 0.0700 | -0.0000 | 0.0357 | 0.0069 | 0.0143 | 0.0038 | 0.0093 |
| L6H6 | 0.0699 | 0.0000 | 0.0158 | 0.0140 | 0.0192 | 0.0044 | 0.0166 |
| L8H5 | 0.0689 | -0.0002 | 0.0234 | 0.0063 | 0.0103 | 0.0244 | 0.0046 |
| L9H6 | 0.0677 | -0.0000 | 0.0175 | 0.0100 | 0.0123 | 0.0191 | 0.0088 |
| L6H10 | 0.0676 | 0.0000 | 0.0354 | 0.0138 | 0.0103 | 0.0009 | 0.0072 |
| L7H2 | 0.0672 | -0.0002 | 0.0261 | 0.0172 | 0.0163 | 0.0002 | 0.0076 |
| L6H7 | -0.0653 | -0.0000 | -0.0253 | -0.0137 | -0.0152 | -0.0024 | -0.0086 |
| L1H4 | 0.0643 | -0.0002 | 0.0306 | 0.0156 | 0.0125 | 0.0001 | 0.0058 |


## Output files

| file | bytes | sha256 | note |
|---|---|---|---|
| `screen_wordorder_muril.npz` | 1,071,819 | `e13f91a001c2e3ca` | attribution per pair x component x site class |
