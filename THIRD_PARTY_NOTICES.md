# Third-party notices

This repository contains the authors' own code and derived numbers. It does not redistribute the treebank text, the
held-out corpus sample or any model weights. Licences below were checked at the source on 18 November 2026; where a
source was silent, this file says so.

## Data

| item | terms | what this repository does |
|---|---|---|
| Hindi-Urdu Treebank (HDTB), original release, LTRC, IIIT Hyderabad (Bhatt et al. 2009) | Copyright LTRC, IIIT Hyderabad. Download needs registration. No licence text or redistribution terms found; the release page returned HTTP 404 on 18 Nov 2026 and was read from an archived copy. | Sentence text and reordered sentences built from it are not published. Identifiers, per-sentence model scores and the scripts that rebuild the items from the treebank are. To rebuild, obtain the treebank from LTRC. |
| Universal Dependencies Hindi-HDTB | CC BY-NC-SA 4.0 (UD page, repository README and LICENSE.txt). Whether LTRC granted this licence for the underlying text could not be verified. | Not used for the published files. |
| Held-out Hindi text for mean ablation and the language-modelling check (a 20,000-sentence sample of IndicCorp, AI4Bharat) | IndicCorp v1: CC BY-NC 4.0. IndicCorp v2: CC0. The version of the sample was not confirmed. | Not published. |

Citations the treebank maintainers request: Bhatt et al. 2009, "A multi-representational and multi-layered treebank for
Hindi/Urdu" (Linguistic Annotation Workshop), and Bhat et al., "The Hindi/Urdu Treebank Project" (Handbook of Linguistic
Annotation, Springer).

## Models (loaded from the Hugging Face Hub, not included)

| model | licence |
|---|---|
| MuRIL (`google/muril-base-cased`), Khanuja et al. 2021 | Apache-2.0 |
| XLM-RoBERTa-large (`FacebookAI/xlm-roberta-large`), Conneau et al. 2020 | MIT |

## Software dependencies

transformers (Apache-2.0), PyTorch (BSD-3-Clause family), scikit-learn (BSD-3-Clause), minicons (MIT), pandas
(BSD-3-Clause), numpy (BSD-3-Clause), scipy (BSD), matplotlib (Matplotlib licence, PSF-style).

## ACL style files

`paper/acl.sty` and `paper/acl_natbib.bst` are the unmodified files of github.com/acl-org/acl-style-files, commit
d5adc823ff0f80f98c80405ca0ab66c68e684409 (29 June 2026), distributed under the licence stated in that repository.

## The authors' earlier code

`reference_code/` holds copies of scripts from the authors' earlier analysis work (steps 1 to 3 of the method), which the
step 4 code imports. They are released here by their authors under the same licence as the rest of the code.
