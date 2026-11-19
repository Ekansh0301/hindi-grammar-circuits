# Step 4 figures

Built by `scripts/mi_figures.py` from `course_runs/outputs` (relative to the project root).

| figure | caption | built from (sha256) |
|---|---|---|
| `f1_component_maps_object` | Share of the object-masking gap restored by patching one component at every position (selection half). MuRIL: largest L11MLP (0.45), 388 orders; XLM-R-large: largest L21MLP (0.37), 388 orders. | `exact_object_muril.npz` `8e4ed1d349941829`, `exact_object_xlmrlarge.npz` `ca14575fa4257472` |
| `f2_where_components_act` | Top 10 components of the object task, each patched at one position class at a time (selection half). | `exact_object_muril.npz` `8e4ed1d349941829`, `exact_object_xlmrlarge.npz` `ca14575fa4257472` |
| `f3_intervening_subject_by_masking` | The intervening-subject contrast of the agreement margin with nothing, the object, the subject or ne masked (all orders; p in the metric records). | `metric_muril.csv` `f00c439230487bec`, `metric_xlmrlarge.csv` `0f9bdf8420a541eb` |
| `f4_attention_osv_sov` | Change in attention from the scored verb position to the object and to the subject when the subject intervenes (OSV-type minus SOV-type, gap-matched, mean per clause, as the attention record), top 5 heads of the object task and the mean over all heads; p in the record. Descriptive: the subject is nearer the verb in OSV-type orders. | `attention_muril.csv` `2445bbcf0fd49cc7`, `attention_xlmrlarge.csv` `a76f1a3a39202487` |
| `f5_validation` | Held-out half: the circuit (dark diamond) against the matched random sets (grey ticks); rank and sign-flip p in the validate records. | `validate_object_muril.npz` `b04c89099df85689`, `validate_object_xlmrlarge.npz` `150b5a99fc83be34`, `validate_wordorder_muril.npz` `1f4ac31936170bed`, `validate_wordorder_xlmrlarge.npz` `1780a1960008b4b2` |
| `f6_wordorder_sites` | Top 5 heads and top 5 MLPs of the word-order exact stage, each patched at one site at a time (selection half). | `sites_wordorder_muril.npz` `66cb0b358dc87d0c`, `sites_wordorder_xlmrlarge.npz` `a1075841de6d1ff6` |
| `f7_screen_vs_exact` | Every head and MLP, object task: the first-order screen against exact patching; MuRIL Spearman 0.86; XLM-R-large Spearman 0.80. | `screen_object_muril.npz` `457413578c210356`, `exact_object_muril.npz` `8e4ed1d349941829`, `screen_object_xlmrlarge.npz` `a254e18167143f56`, `exact_object_xlmrlarge.npz` `ca14575fa4257472` |
