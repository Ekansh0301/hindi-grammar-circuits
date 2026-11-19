# Reference code

Scripts from the authors' earlier layer-wise analysis (steps 1 to 3 of the method), kept here because the main code in
`scripts/` imports some of them (`lm_units`, `runlog`, `pll_scorer`, `order_model`, `set1_generator`, `hutb_corpus`).

They are not standalone: they expect the earlier analysis's folder layout and environment. Each script describes its
design and built-in checks in its docstring.

| script | used for |
|---|---|
| `pll_scorer.py` | word-level pseudo-log-likelihood scoring (within-word left-to-right) |
| `hutb_corpus.py`, `set1_generator.py`, `order_model.py` | corpus access, reordering generation, constituent units |
| `runlog.py` | run records (script hash, command, outputs) |
| `rq1_lm_units.py` | per-layer scoring: per-word surprisal at every layer under each lens, and the pooled states the probes read |
| `rq1_layer_probe.py`, `rq1_probe_selectivity.py`, `rq1_structure_probe.py`, `rq1_word_state_probes.py` | probes |
| `rq1_lens_analysis.py`, `rq1_tuned_lens.py`, `rq1_jacobian_lens.py` | layer-wise readouts |
| `rq1_attention_mass.py` | attention analysis |
| `rq1_patching.py`, `rq1_das.py` | interchange patching and distributed alignment search |
| `rq1_concept_erasure.py`, `rq1_concept_erasure_all.py`, `rq1_concept_erasure_units.py`, `rq1_late_ablation.py` | LEACE erasure and mean-ablation (`rq1_concept_erasure_units.py` is the final design) |
| `rq1_layerwise_decomposition.py`, `rq1_layer_vs_output.py`, `rq1_four_block.py` | layer-wise and four-block decompositions |
| `rq1_agreement_order.py` | building and scoring the agreement set |
| `lm_units.py`, `rq1_dominance.py`, `dominance_analysis.py`, `rq1_word_attribution.py`, `materialise_set1.py` | helpers |
