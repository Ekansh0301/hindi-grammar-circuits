# Data

All sentences come from the news training split of the Hindi-Urdu Treebank (Bhatt et al., 2009). The treebank text is not
included (see the top-level README); this folder holds identifiers, scores and derived features.

## word_order/

| file | contents |
|---|---|
| `pairs.csv` | 8,923 written and reordered sentence pairs: identifiers, word-order class, clause type, size of the reordering, labels |
| `t_<model>_within_word_l2r_s0.csv`, `_s1.csv` | per-pair scores for four models (MuRIL, XLM-R-large, IndicBERT-v2 as `indicbert`, mBERT as `mbert`), two shards each: summed and mean surprisal of the written (`ref_*`) and reordered (`var_*`) sentence and their difference, in bits |

A model prefers the written order when `ref_Mean < var_Mean`.

## agreement/

| file | contents |
|---|---|
| `agreement_scores_<model>.csv` | summed pseudo-log-likelihood surprisal (bits) of the correct and the wrong-verb sentence for each of the 5,265 orders, four models |

The agreement margin is `sum_foil - sum_correct` in bits; the model prefers the correct verb when it is positive.
`agreement_items.csv`, which holds the sentence text of the 459 clauses and their orders, is not included.

## features/

| file | contents |
|---|---|
| `rq1_features_all.csv` | per-pair predictors and labels for the 8,923 pairs: document identifiers, word-order class, structural measures |
| `rq1_features_ngram.csv` | per-pair n-gram surprisal differences |
