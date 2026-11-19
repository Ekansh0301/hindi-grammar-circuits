# Results index

Every result in the paper, with the run record that holds it. Records are in `records/` (script hash, library versions,
command, checks, output checksums), per-run outputs in `outputs/`, figures in `figures/`. Brackets are document-bootstrap
95% intervals (descriptive); p values are document-level sign-flip permutation tests.

## 1. Step 4: heads and MLPs

**Agreement** (object task; held-out half, `mi_validate_object_<model>.md`).

| | MuRIL | XLM-R-large |
|---|---|---|
| faithfulness: share of the object gap restored by the 10 leading heads | 0.90 [0.86, 0.93] | 0.78 [0.71, 0.85] |
| random head sets matched by block (mean) | 0.005 | -0.003 |
| necessity: share lost when the 10 heads are mean-ablated | 0.97 [0.89, 1.05] | 1.08 [0.94, 1.25] |
| rank among 100 random sets, both tests | first, p 1e-4 | first, p 1e-4 |
| language-modelling cost of ablating the heads | +0.21 nats | +0.06 nats |

The leading heads put 26 to 73% of their attention from the verb on the object (`mi_attention_<model>.md`). Path patching
sends their effect through the object's keys and values, and none through the subject or ne (`mi_path_<model>.md`; MuRIL
L8H3 0.29 of 0.32, XLM-R-large L21H0 0.23 of 0.31). Leading components: MuRIL L11MLP, L10H6, L10MLP, L8H3; XLM-R-large
L21MLP, L21H0, L20H0, L20MLP.

**Word order** (held-out half, `mi_validate_wordorder_<model>.md`).

| | MuRIL | XLM-R-large |
|---|---|---|
| faithfulness (10 heads) | 0.78 [0.72, 0.84] (random 0.16) | 0.53 [0.48, 0.59] (random 0.08) |
| necessity (10 heads ablated) | 0.06 [0.00, 0.11] (random 0.01) | 0.09 [0.04, 0.13] (random 0.01) |

The upper MLPs carry most of the preference: MuRIL blocks 6 to 10 and XLM-R-large blocks 17 to 21 each restore 22 to 56% of
the gap, mostly at the moved phrases' head words (`mi_sites_wordorder_<model>.md`).

**The intervening subject.** At the verb neither model is misled (`mi_metric_<model>.md`: MuRIL -0.05 bits, p 0.80;
XLM-R-large +0.16, p 0.26). The whole-sentence effect (MuRIL -1.75 bits) lies in how the other words are rescored
(`mi_decompose_<model>.md`).

## 2. Follow-up experiments

Records: `mi_items_extra.md`, `mi_followup_<size|case_wordorder|case_agreement>_<model>.md`,
`mi_swap_<stage>_<task>_<model>.md`, `mi_swap_compare.md`. Figures f8 to f10.

| experiment | result |
|---|---|
| reordering size (471 pairs the earlier steps never read) | the heads' share of the gap is flat or slightly rising with size; intervals about +-0.12, inconclusive |
| deleting the moved phrases' case markers (223 pairs) | costs the gap no more than deleting as many other words (p 0.19 and 0.13) |
| deleting ne (2,137 orders) | costs the agreement margin 4.2 (MuRIL) and 3.4 (XLM-R-large) bits more than an unrelated word, p 1e-4; the object-agreeing form is still preferred in 71 to 75% of orders without ne |
| document halves exchanged | faithfulness replicates in all four task-model cells and the top 5 MLPs are the same; word order in XLM-R-large shares 5 of 10 heads and its necessity does not replicate (0.019, p 0.93) |

## 3. Paper experiments

Items: `mi_items_paper.md`. All on documents step 4 did not read, with the components fixed from step 4.

| experiment | record | result |
|---|---|---|
| **ko-insertion** (956 orders) | `mi_paper_ko_<model>.md` | With ko inserted after the object, the default verb form is preferred in 74.7% (MuRIL) and 68.1% (XLM-R-large) of orders; with the control particle bhi, the object-agreeing form is preferred (margin 7.08 and 6.04 bits). The top 5 heads' attention to the object is 0.53 / 0.52 / 0.22 (none / bhi / ko) in MuRIL and 0.54 / 0.51 / 0.23 in XLM-R-large; part of the fall is attention moving to ko |
| **role swap** (2,132 orders) | `mi_paper_role_swap_<model>.md` | After the two noun phrases swap places and ne stays, the margin toward the form agreeing with the bare noun is negative in both order classes: MuRIL -0.80 bits in SOV-type orders (p 0.066) and -2.99 in OSV-type (p 1e-4); XLM-R-large -2.53 and -4.02 (p 1e-4). Where the default-form prior cannot help, MuRIL's SOV-type value is -1.98 |
| **masked slot after the swap** | `mi_paper_swap_mask_<model>.md` | Masking the ne-marked noun raises the margin by 2.04 [1.55, 2.57] (SOV-type) and 2.50 [1.88, 3.23] (OSV-type) bits in MuRIL, and by 3.60 [3.05, 4.18] and 3.96 [3.31, 4.62] in XLM-R-large (p 1e-4). The margin turns positive in SOV-type orders only. Masking the bare noun lowers it only in MuRIL (-1.22 bits, SOV-type) |
| **head-set size** | `mi_paper_setsize_<task>_<model>.md` | Agreement, mean-ablation necessity of the top K heads at K = 5, 10, 20, 40: MuRIL 0.75, 0.94, 1.00, 1.03; XLM-R-large 0.87, 0.89, 0.93, 0.97. Word order: MuRIL 0.07, 0.09, 0.10, 0.19 (zero ablation 0.03 at K = 40); XLM-R-large 0.06, 0.08, 0.09, 0.07. Patching the top K heads restores 0.47, 0.71, 0.98, 1.01 of the word-order gap in MuRIL and 0.30, 0.48, 0.70, 0.84 in XLM-R-large |
| **MLP sets** | `mi_paper_mlpsets_<task>_<model>.md` | The frozen top 5 MLPs against all other 5-subsets of MuRIL's 12 MLPs and 255 subsets of XLM-R-large's 24. How well a set restores the gap rises with its mean block index (per block: MuRIL agreement 0.023 [0.011, 0.036], XLM-R-large agreement 0.009 [0.007, 0.011], MuRIL word order 0.006 [-0.005, 0.016], XLM-R-large word order 0.010 [0.007, 0.013]). The frozen set exceeds the best other set by 0.02 or more only for XLM-R-large agreement; in MuRIL word order 30 sets are within 0.02 of it |
| **marker control matched in kind** | `mi_paper_kind_<model>.md` | Deleting the moved phrases' markers costs the gap no more than deleting distant postpositions (131 pairs). The control matched in string and place has only 17 pairs and is inconclusive |
| **cue strata** | `mi_paper_cues_<model>.md`, `mi_paper_cues_gap_<model>.md` | The n-gram cue correlates with the word-order gap (Spearman -0.50 MuRIL, -0.46 XLM-R-large). Where it favours the other order (60 pairs), the models still prefer the written order in 61.7% of pairs, and the circuit's effect in bits depends on the gap and not on the stratum |
