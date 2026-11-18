# Figure plan

| ID | Data and content | Source | Fixed conditions |
|---|---|---|---|
| 01 | Procurement limit: RP/WS/EEV and EV-policy VSS range | report_data.json fleet/ties | N0=0; HKD1m/pump; baseline CU/score assumptions |
| 02 | Spatial heterogeneity heatmap | report_data.json spatial | Capital HKD2m; beta/cost factors hypothetical |
| 03 | Eight intervention subsets | report_data.json summary | Same conditional inventory model |
| 04 | One-at-a-time endpoint effects | report_data.json oat | Four levels per factor; endpoints 0.8/1.2 |
| 05 | Paired joint perturbation distributions | report_data.json summary | 200 draws/mode, fixed seed; not confidence intervals |
| 06 | Frozen vs recomputed resource upper bounds | report_data.json corrected | Legacy model; 5 levels/resource |

Figures use vector PDF plus PNG previews. Captions are in latex_includes.tex. No external or cross-model figure review is claimed.
