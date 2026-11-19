# Earlier layer-wise results (steps 1 to 3)

Results of the authors' earlier analysis of four models (MuRIL, IndicBERT-v2, XLM-R-large, mBERT): probes, lenses,
interchange patching, concept erasure and ablation. The paper uses MuRIL and XLM-R-large.

| path | contents |
|---|---|
| `SUMMARY.md` | the results written up, with figures |
| `records/` | the run records behind them (script hash, command, library versions, output checksums); every number in `SUMMARY.md` cites one |
| `figures/` | the figures (PNG and PDF): layer probe, structure probes, distance probe, representational similarity, lenses, layer-wise decomposition, probe selectivity, attention mass, patching sites, erasure by layer |

The raw outputs (3.4 GB: per-layer scores, hidden states, trained lenses and erasers) are not included.
