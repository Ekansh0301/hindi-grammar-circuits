# Where Do Multilingual Encoders Compute Hindi Grammar?

We look inside **MuRIL** and **XLM-RoBERTa-large** and ask which attention heads and MLPs make two grammatical choices:

- **Word order.** Given a written sentence and a reordering of the same words, which one is the written one?
- **Agreement.** In a past-tense clause the verb agrees with the bare object, not with the subject marked by *ने* (ne).
  Which verb form is correct?

Both models choose well. We trace the choices to individual components and test what those components read: the
case-marked role of each noun, or cues such as position and how object-like a noun looks.

**Authors:** Ekansh Goyal, Varun Gupta

## Main results

- **Agreement runs through a small set of late attention heads.** Patching the ten leading heads restores 0.90 (MuRIL) and
  0.78 (XLM-R-large) of the agreement margin, and removing them removes about all of it.
- **Word order does not.** Its leading heads are sufficient but not necessary. The upper MLPs carry most of the preference.
- **Agreement respects the case rule at its boundary.** When the object takes *को* (ko), the verb falls back to the default
  form in 68% to 75% of the sentences, depending on the model.
- **Agreement does not simply follow the case-marked role.** When the two noun phrases swap places, both models still
  prefer the verb form that agrees with the old object.
- **The two models use different components of the same kind** (late heads, upper MLPs) at a similar relative depth.

Every number and its run record are listed in [`course_runs/README.md`](course_runs/README.md).

## Method

We combine attention-head and MLP patching, path patching and mean-ablation. Components are chosen on one half of the
documents and tested once on the other, against 100 matched random head sets, with document-level permutation tests.

Sentences are scored by word-level pseudo-log-likelihood, which is not true surprisal. The data are sentences from the
news section of the Hindi-Urdu Treebank: 8,923 written and reordered pairs for word order, and 5,265 orders of 459
clauses for agreement.

## Repository contents

| path | contents |
|---|---|
| `paper/` | the paper (ACL format) |
| `scripts/` | analysis code, figure scripts and the baseline check; see `scripts/README.md` |
| `course_runs/` | run records, per-run outputs and figures; `README.md` is the results index |
| `results/` | earlier layer-wise analyses (probes, lenses, patching, erasure) |
| `reference_code/` | the earlier analysis scripts that the main code imports |
| `data/` | word-order pairs, agreement scores and feature tables; see `data/README.md` |

## Data

The treebank text is not redistributed, because the original release states no redistribution terms. The repository holds
identifiers, per-sentence model scores and derived numbers. To rebuild the sentence-level items, obtain the treebank
from LTRC, IIIT Hyderabad, and run `scripts/mi_items.py`, `mi_items_extra.py` and `mi_items_paper.py`.

Licences for the data, models and dependencies are in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Reproducing

The models load from the Hugging Face Hub (`google/muril-base-cased`, `xlm-roberta-large`). The analysis stages need a
GPU; the figures and the cue analysis need only numpy, scipy and matplotlib.

```bash
pip install -r requirements.txt
python3 scripts/mi_figures.py
python3 scripts/mi_figures_followup.py
```

Each run writes a record to `course_runs/records/` with the script hash, library versions and output checksums.

## Licence

Code: MIT, see [`LICENSE`](LICENSE).
